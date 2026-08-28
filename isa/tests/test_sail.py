import unittest
from dataclasses import replace
from pathlib import Path
import re
import tempfile

from engine.instruction import Instruction
from engine.model import SailUnit
from engine.project import IsaProject
from engine.sail import (
    ArtifactWriter,
    IsaConfiguration,
    SailComposer,
    SailCatalogRenderer,
    SailDispatchRenderer,
    SailEntryValidator,
    ArtifactGenerationContext,
    ArtifactGeneratorRegistry,
    SailProjectRenderer,
    SailRegistryRenderer,
)


class SailCompositionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.project = IsaProject.load(Path(__file__).parents[1])
        cls.composer = SailComposer()

    def compose(self, extensions=None):
        configuration = IsaConfiguration.resolve(self.project, extensions)
        return self.composer.compose(self.project, configuration)

    def test_default_composition_contains_all_owned_instructions(self) -> None:
        program = self.compose()

        self.assertEqual(
            program.configuration.extension_ids, ("FP", "FPTRANSA", "VECTOR")
        )
        self.assertEqual(program.bundles, self.project.select())
        self.assertEqual(
            tuple(item.bundle for item in program.instruction_semantics),
            program.bundles,
        )
        self.assertEqual(
            program.semantic_sources,
            tuple(item.source for item in program.instruction_semantics),
        )
        self.assertEqual(
            tuple(unit.reference for unit in program.sail_units),
            self.project.model.sail_order,
        )

    def test_configuration_rejects_unknown_extension(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown extension"):
            IsaConfiguration.resolve(self.project, ("DOES_NOT_EXIST",))

    def test_extension_selection_closes_declared_dependencies(self) -> None:
        program = self.compose(("FPTRANSA",))
        registry = SailRegistryRenderer().render(program)

        self.assertEqual(program.configuration.extension_ids, ("FP", "FPTRANSA"))
        self.assertEqual(
            program.bundles,
            tuple(
                bundle
                for bundle in self.project.select()
                if bundle.reference.owner in {"base", "FP", "FPTRANSA"}
            ),
        )
        self.assertIn("Op_FADD", registry)
        self.assertIn("Op_FLOG2A", registry)
        self.assertNotIn("Op_VADD", registry)
        self.assertNotIn("RouteVector", registry)

    def test_registry_derives_route_from_instruction_owner(self) -> None:
        registry = SailRegistryRenderer().render(self.compose(()))

        self.assertIn("Op_ADD => RouteIntegerAlu", registry)
        self.assertIn("BaseSet", registry)
        self.assertNotIn("RouteFpu", registry)
        self.assertNotIn("FloatingPointFault", registry)
        self.assertNotIn("RouteVector", registry)

    def test_registry_adds_types_only_for_active_extensions(self) -> None:
        fptransa = SailRegistryRenderer().render(self.compose(("FPTRANSA",)))
        vector = SailRegistryRenderer().render(self.compose(("VECTOR",)))

        self.assertIn("FpuSet", fptransa)
        self.assertIn("FpuTranscendentalSet", fptransa)
        self.assertIn("FloatingPointFault", fptransa)
        self.assertIn("TranscendentalCompute", fptransa)
        self.assertNotIn("VectorRangeFault", fptransa)
        self.assertIn("VectorSet", vector)
        self.assertIn("VectorRangeFault", vector)
        self.assertNotIn("VectorFpuSet", vector)
        self.assertNotIn("FloatingPointFault", vector)

    def test_registry_projects_only_active_leaf_events(self) -> None:
        base = SailRegistryRenderer().render(self.compose(()))
        fp = SailRegistryRenderer().render(self.compose(("FP",)))
        vector = SailRegistryRenderer().render(self.compose(("VECTOR",)))

        self.assertIn("Event_PAGE_PERMISSION_VIOLATION", base)
        self.assertIn(
            "Event_PAGE_PERMISSION_VIOLATION => Some(0x000021)", base
        )
        self.assertNotIn("Event_FLOATING_POINT_EXCEPTION", base)
        self.assertIn("Event_FLOATING_POINT_EXCEPTION", fp)
        self.assertNotIn("Event_VECTOR_LANE_INDEX_OUT_OF_RANGE", fp)
        self.assertIn("Event_VECTOR_LANE_INDEX_OUT_OF_RANGE", vector)
        self.assertNotIn("Event_FLOATING_POINT_EXCEPTION", vector)

    def test_dispatch_preserves_ordered_multi_entry_fallback(self) -> None:
        dispatch = SailDispatchRenderer().render(self.compose())

        self.assertIn(
            "match execute_VADD_integer(instruction, state) { Some(result) => result, "
            "None() => match execute_VADD_floating(instruction, state)",
            dispatch,
        )

    def test_single_entry_dispatch_does_not_require_local_ownership_guards(self) -> None:
        program = self.compose()
        dispatch = SailDispatchRenderer().render(program)

        self.assertIn(
            "Op_BNDSII => match execute_BNDSII(instruction, state)",
            dispatch,
        )
        self.assertNotIn("execute_BNDSII_local_entry", dispatch)

        for semantics in program.instruction_semantics:
            if len(semantics.entries) != 1:
                continue
            source = semantics.source.read_text()
            entry = semantics.entries[0]
            self.assertNotIn(f"function {entry}_local_entry", source)
            self.assertNotIn(
                f"instruction.form.operation != {semantics.operation}",
                source,
            )

    def test_instruction_semantics_do_not_identify_other_instructions(self) -> None:
        for source_path in self.project.root.glob(
            "**/instructions/definitions/*/semantics.sail"
        ):
            owner = source_path.parent.name
            referenced_operations = set(
                re.findall(r"\bOp_([A-Za-z0-9_]+)\b", source_path.read_text())
            )
            foreign_operations = referenced_operations - {owner}
            self.assertEqual(
                foreign_operations,
                set(),
                f"{source_path} identifies instructions owned elsewhere",
            )

    def test_repeatable_instruction_owns_its_observation_semantics(self) -> None:
        repeat = (
            self.project.root / "repeat/semantics/repeat.sail"
        ).read_text()
        continuation = (
            self.project.root / "repeat/semantics/continuation.sail"
        ).read_text()
        catalog = SailCatalogRenderer().render(self.compose())
        repeatcc_operations = set(
            re.findall(
                r"operation = Op_([A-Za-z0-9_]+),.*repeat_repcc = true",
                catalog,
            )
        )

        self.assertNotRegex(repeat, r"\bOp_[A-Za-z0-9_]+\b")
        self.assertNotIn("repeat_body_control_forbidden", continuation)
        self.assertTrue(repeatcc_operations)
        for semantics_path in self.project.root.glob(
            "**/instructions/definitions/*/semantics.sail"
        ):
            mnemonic = semantics_path.parent.name
            semantics = semantics_path.read_text()
            self.assertIn(
                f"function clause repeat_semantics(Op_{mnemonic})",
                semantics,
            )

    def test_instruction_owns_register_result_extension(self) -> None:
        for semantics in self.project.root.glob(
            "**/instructions/definitions/*/semantics.sail"
        ):
            mnemonic = semantics.parent.name
            self.assertIn(
                f"function clause register_result_extension(Op_{mnemonic})",
                semantics.read_text(),
                semantics,
            )

        for source in (
            "execution/semantics/integer_bits.sail",
            "execution/semantics/instruction_properties.sail",
            "instructions/semantics/integer/arithmetic.sail",
            "instructions/semantics/integer/data_control.sail",
            "instructions/semantics/integer/routing.sail",
        ):
            text = (self.project.root / source).read_text()
            self.assertNotRegex(text, r"\bOp_[A-Za-z0-9_]+\b", source)

    def test_fp_instruction_owns_its_form_semantics(self) -> None:
        catalog_path = self.project.root / "extensions/FP/semantics/operation_catalog.sail"
        catalog = catalog_path.read_text()

        self.assertNotRegex(catalog, r"\bOp_[A-Za-z0-9_]+\b")
        self.assertNotIn("fp_base_semantics", catalog)
        for semantics_path in self.project.root.glob(
            "extensions/FP/instructions/definitions/*/semantics.sail"
        ):
            mnemonic = semantics_path.parent.name
            self.assertIn(
                f"function clause fp_semantics(Op_{mnemonic})",
                semantics_path.read_text(),
                semantics_path,
            )

        primitives = self.project.root / "extensions/FP/semantics/primitives"
        for source_name, removed_classifier in {
            "arithmetic.sail": "fp_arithmetic_operation",
            "comparison.sail": "fp_compare_operation",
            "conversion.sail": "fp_conversion_operation",
            "data.sail": "fp_data_operation",
        }.items():
            self.assertNotIn(
                f"function {removed_classifier}(",
                (primitives / source_name).read_text(),
            )

        primitive_runtime = (
            self.project.root / "extensions/FP/semantics/primitives.sail"
        ).read_text()
        self.assertNotIn("fp_shared_numeric_semantic_operation", primitive_runtime)

    def test_add_and_move_own_their_uop_programs(self) -> None:
        uops = (
            self.project.root / "execution/semantics/uops.sail"
        ).read_text()
        lowering = (
            self.project.root / "execution/semantics/uops/lowering.sail"
        ).read_text()

        for mnemonic in ("ADD", "MOV"):
            semantics = (
                self.project.root
                / "instructions/definitions"
                / mnemonic
                / "semantics.sail"
            ).read_text()
            self.assertIn(f"function lower_{mnemonic}_uops", semantics)
            self.assertIn("uop_program_execute", semantics)
            self.assertNotIn("start_memory_transaction", semantics)

            self.assertNotIn(f"lower_{mnemonic}_uops", uops)
            self.assertNotIn(f"Op_{mnemonic}", uops)

        self.assertIn("uop_ea_update_program(operand, width, true)", lowering)
        self.assertIn("uop_ea_update_program(operand, width, false)", lowering)

    def test_uop_primitives_own_scattered_tag_and_execution_clause(self) -> None:
        types = (
            self.project.root / "execution/semantics/types.sail"
        ).read_text()
        runtime = (
            self.project.root / "execution/semantics/uops.sail"
        ).read_text()
        primitives = self.project.root / "execution/semantics/uops/primitives"

        self.assertIn("scattered union Uop_kind", types)
        self.assertIn("scattered function execute_uop", runtime)
        self.assertIn("execute_uop(uop.kind", runtime)
        self.assertNotIn("if uop.kind", runtime)

        owned = {
            "calc_ea.sail": "UopCalcEa",
            "integer_add.sail": "UopIntegerAdd",
            "move.sail": "UopMove",
            "memory_load.sail": "UopMemoryLoad",
            "memory_probe.sail": "UopMemoryProbe",
            "memory_store.sail": "UopMemoryStore",
            "commit.sail": "UopCommit",
        }
        for source_name, constructor in owned.items():
            source = (primitives / source_name).read_text()
            self.assertIn(
                f"union clause Uop_kind = {constructor} : unit",
                source,
            )
            self.assertIn(
                f"function clause execute_uop({constructor}()",
                source,
            )
            self.assertNotIn(constructor, types)

        self.assertIn(
            "uop_step_wait(",
            (primitives / "memory_load.sail").read_text(),
        )
        self.assertIn(
            "uop_step_wait(",
            (primitives / "memory_store.sail").read_text(),
        )
        self.assertIn(
            "union clause Uop_kind = UopIntegerAlu : Integer_alu_uop_operation",
            (primitives / "integer_add.sail").read_text(),
        )
        self.assertNotIn("PhaseUopWait", types)
        self.assertNotIn("PhaseUopWait", runtime)

    def test_uop_api_uses_domain_first_names(self) -> None:
        core_sources = [
            self.project.root / "execution/semantics/uops.sail",
            self.project.root / "execution/semantics/uops/lowering.sail",
            *(self.project.root / "execution/semantics/uops/primitives").glob(
                "*.sail"
            ),
        ]
        core = "\n".join(source.read_text() for source in core_sources)
        declarations = re.findall(
            r"^(?:function|val)\s+(?:clause\s+)?([A-Za-z][A-Za-z0-9_]*)",
            core,
            re.MULTILINE,
        )

        self.assertTrue(declarations)
        self.assertTrue(
            all(name == "execute_uop" or name.startswith("uop_") for name in declarations)
        )

        types = (self.project.root / "execution/semantics/types.sail").read_text()
        self.assertIn("struct Uop =", types)
        self.assertNotIn("Micro_operation", types)

        all_sail = "\n".join(
            source.read_text() for source in self.project.root.rglob("*.sail")
        )
        for legacy_name in (
            "make_uop",
            "append_uops",
            "lower_uop_operand",
            "execute_uop_program",
            "run_uop_program",
            "resume_uop_phase",
            "uop_complete",
            "uop_fault",
            "fp_execute_uop_operation",
            "execute_vector_fp_uop",
        ):
            self.assertNotRegex(all_sail, rf"\b{legacy_name}\b")

    def test_pending_execution_uses_typed_continuation_payloads(self) -> None:
        types = (
            self.project.root / "execution/semantics/types.sail"
        ).read_text()
        runtime = (
            self.project.root / "execution/semantics/uops.sail"
        ).read_text()
        results = (
            self.project.root / "execution/semantics/results.sail"
        ).read_text()

        self.assertIn("struct Uop_continuation", types)
        self.assertIn("PendingUop : Uop_continuation", types)
        self.assertNotIn("uop_program :", types)
        self.assertNotIn("uop_cursor :", types)
        self.assertNotIn("uop_values :", types)
        self.assertNotIn("uop_pending_destination :", types)
        self.assertIn("uop_continuation_get(previous.pending)", runtime)

        self.assertIn("struct Repeat_continuation", types)
        self.assertIn("repeat_parent : option(Repeat_continuation)", types)
        self.assertNotIn("repeat_parent_active :", types)
        self.assertNotIn("repeat_body :", types)
        self.assertNotIn("repeat_bytes :", types)

        self.assertIn("struct Event_continuation", types)
        self.assertIn("PendingEvent : Event_continuation", types)
        self.assertNotIn("event_attempt :", types)

        self.assertIn("struct Transaction_continuation", types)
        for variant in (
            "PendingControl",
            "PendingEventReturn",
            "PendingSystem",
            "PendingRepeat",
        ):
            self.assertIn(f"{variant} : Transaction_continuation", types)
        self.assertNotIn("PendingMemory :", types)
        self.assertNotIn("PendingTransaction :", types)
        self.assertIn("continuation : Pending_continuation", types)
        pending = types.split("struct Pending_commit = {", 1)[1].split("}", 1)[0]
        self.assertNotIn("uop : option", pending)
        self.assertNotIn("transaction : Transaction_continuation", pending)
        self.assertNotIn("event : option", pending)
        for flattened in (
            "phase : Continuation_phase",
            "ordinal : int",
            "captured_first : bits(64)",
            "captured_second : bits(64)",
        ):
            self.assertNotIn(flattened, pending)

        common = (
            self.project.root / "execution/semantics/continuation/common.sail"
        ).read_text()
        dispatch = (
            self.project.root / "execution/semantics/continuation/dispatch.sail"
        ).read_text()
        self.assertIn("function response_matches_request", common)
        self.assertNotIn("PhaseUopWait", common)
        self.assertIn("uop_continuation_get(previous.pending)", dispatch)
        self.assertNotIn("PhaseUopWait", dispatch)
        self.assertNotIn("PendingMemory", dispatch)
        self.assertNotIn("resume_memory_phase", dispatch)
        self.assertIn("PendingSystem(_) => resume_system_phase", dispatch)
        self.assertIn("PendingRepeat(_) => resume_repeat_phase", dispatch)
        self.assertIn("PendingEvent(_) => resume_events_phase", dispatch)
        self.assertIn("PendingEventReturn(_) => resume_events_phase", dispatch)
        self.assertIn("PendingControl(_) => resume_control_phase", dispatch)
        self.assertNotIn("transaction.phase == PhaseEventFrameHeader", dispatch)
        self.assertNotIn("_ => PendingControl(transaction)", results)

    def test_fadd_owns_fp_arithmetic_uop_program(self) -> None:
        semantics = (
            self.project.root
            / "extensions/FP/instructions/definitions/FADD/semantics.sail"
        ).read_text()
        primitive = (
            self.project.root
            / "extensions/FP/semantics/uops/fp_compute.sail"
        ).read_text()

        self.assertIn("function lower_FADD_uops", semantics)
        self.assertIn("UopFpArithmetic(FpArithmeticAdd)", semantics)
        self.assertIn("uop_program_execute", semantics)
        self.assertNotIn("start_fp_transaction", semantics)
        self.assertIn(
            "union clause Uop_kind = UopFpArithmetic",
            primitive,
        )
        self.assertIn(
            "function clause execute_uop(UopFpArithmetic(operation)",
            primitive,
        )

    def test_basic_integer_alu_instructions_own_their_uop_programs(self) -> None:
        operations = {
            "SUB": "IntegerAluSubtract",
            "AND": "IntegerAluAnd",
            "OR": "IntegerAluOr",
            "XOR": "IntegerAluXor",
        }
        for mnemonic, operation in operations.items():
            semantics = (
                self.project.root
                / "instructions/definitions"
                / mnemonic
                / "semantics.sail"
            ).read_text()
            self.assertIn(f"function lower_{mnemonic}_uops", semantics)
            self.assertIn(f"UopIntegerAlu({operation})", semantics)
            self.assertIn("uop_program_execute", semantics)
            self.assertNotIn("start_memory_transaction", semantics)

        flags_operations = {
            "CMP": "IntegerFlagsCompare",
            "TEST": "IntegerFlagsTest",
        }
        for mnemonic, operation in flags_operations.items():
            semantics = (
                self.project.root / "instructions/definitions" / mnemonic / "semantics.sail"
            ).read_text()
            self.assertIn(f"function lower_{mnemonic}_uops", semantics)
            self.assertIn(f"UopIntegerFlags({operation})", semantics)
            self.assertIn("uop_program_execute", semantics)
            self.assertNotIn("start_memory_transaction", semantics)

        migrated = {
            "FADD": "FpArithmeticAdd",
            "FSUB": "FpArithmeticSubtract",
            "FMUL": "FpArithmeticMultiply",
            "FDIV": "FpArithmeticDivide",
            "FSQRT": "FpArithmeticSquareRoot",
            "FMADD": "FpArithmeticFusedMultiplyAdd",
            "FMSUB": "FpArithmeticFusedMultiplySubtract",
            "FNMADD": "FpArithmeticFusedNegatedMultiplyAdd",
            "FNMSUB": "FpArithmeticFusedNegatedMultiplySubtract",
            "FABS": "FpArithmeticAbsolute",
            "FNEG": "FpArithmeticNegate",
        }
        for mnemonic, operation in migrated.items():
            source = (
                self.project.root
                / "extensions/FP/instructions/definitions"
                / mnemonic
                / "semantics.sail"
            ).read_text()
            self.assertIn(f"function lower_{mnemonic}_uops", source)
            self.assertIn(f"UopFpArithmetic({operation})", source)
            self.assertNotIn("start_fp_transaction", source)

    def test_instruction_semantics_owns_dispatch_inputs(self) -> None:
        semantics = next(
            item
            for item in self.compose().instruction_semantics
            if item.bundle.instruction.mnemonic == "CMPJcc"
        )

        self.assertEqual(semantics.operation, "Op_CMPJcc")
        self.assertEqual(semantics.entries, ("execute_CMPJcc",))
        self.assertEqual(semantics.source.name, "semantics.sail")

    def test_compare_jump_kind_is_selected_by_instruction_semantics(self) -> None:
        shared = (
            self.project.root
            / "instructions/semantics/integer/data_control.sail"
        ).read_text()
        compare = (
            self.project.root
            / "instructions/definitions/CMPJcc/semantics.sail"
        ).read_text()
        test = (
            self.project.root
            / "instructions/definitions/TESTJcc/semantics.sail"
        ).read_text()

        self.assertNotIn("Op_CMPJcc", shared)
        self.assertNotIn("Op_TESTJcc", shared)
        self.assertIn("UopFusedJump(FusedCompareJump)", compare)
        self.assertIn("UopFusedJump(FusedTestJump)", test)
        self.assertIn("uop_program_execute", compare)
        self.assertIn("uop_program_execute", test)

    def test_single_consumer_integer_operations_are_instruction_local(self) -> None:
        shared_primitives = "\n".join(
            path.read_text()
            for path in (self.project.root / "execution/semantics/primitives").glob("*.sail")
        )

        for mnemonic in ():
            semantics = (
                self.project.root / "instructions/definitions" / mnemonic / "semantics.sail"
            ).read_text()
            self.assertIn(f"execute_{mnemonic}_primitive", semantics)

        for mnemonic in ("ABS", "ADC", "CLR", "NEG", "NOT", "OR", "SBB", "XOR"):
            semantics = (
                self.project.root / "instructions/definitions" / mnemonic / "semantics.sail"
            ).read_text()
            self.assertIn(f"function lower_{mnemonic}_uops", semantics)
            self.assertIn("uop_program_execute", semantics)
            self.assertNotIn(f"execute_{mnemonic}_primitive", semantics)

        for constructor in (
            "IntegerArithmeticAddCarry",
            "IntegerArithmeticSubtractBorrow",
            "IntegerArithmeticNegate",
            "IntegerArithmeticAbsolute",
            "IntegerLogicalOr",
            "IntegerLogicalXor",
            "IntegerLogicalComplement",
            "IntegerDataClear",
        ):
            self.assertNotIn(constructor, shared_primitives)

    def test_basic_integer_operation_kinds_are_instruction_owned(self) -> None:
        shared = (
            self.project.root
            / "instructions/semantics/integer/arithmetic.sail"
        ).read_text()

        for mnemonic in (
            "ABS", "ADC", "ADD", "AND", "CLR", "CMP", "DEC", "DECF",
            "INC", "INCF", "MOV", "MOVCU", "MOVUC", "MOVUU", "MOVcc",
            "NEG", "NOT", "OR", "SBB", "SUB", "TEST", "XOR",
        ):
            self.assertNotIn(f"Op_{mnemonic}", shared)

    def test_fptransa_semantics_are_owned_by_fptransa(self) -> None:
        fp_catalog = (
            self.project.root / "extensions/FP/semantics/operation_catalog.sail"
        ).read_text()
        fptransa_catalog = (
            self.project.root
            / "extensions/FPTRANSA/semantics/operation_catalog.sail"
        ).read_text()

        self.assertIn("scattered function fp_semantics", fp_catalog)
        for mnemonic in (
            "FACOSA", "FASINA", "FATANA", "FATANHA", "FCOSA", "FCOSHA",
            "FETOXA", "FETOXM1A", "FLOG10A", "FLOG2A", "FLOGNA",
            "FLOGNP1A", "FSINA", "FSINCOSA", "FSINHA", "FTANA", "FTANHA",
            "FTENTOXA", "FTWOTOXA",
        ):
            self.assertNotIn(f"Op_{mnemonic}", fp_catalog)
            self.assertNotIn(f"Op_{mnemonic}", fptransa_catalog)
            semantics = (
                self.project.root
                / "extensions/FPTRANSA/instructions/definitions"
                / mnemonic
                / "semantics.sail"
            ).read_text()
            self.assertIn(f"function clause fp_semantics(Op_{mnemonic})", semantics)

        old_contract = (
            self.project.root
            / "extensions/FP/semantics/transcendental_contract.sail"
        )
        self.assertFalse(old_contract.exists())
        self.assertTrue(
            (
                self.project.root
                / "extensions/FPTRANSA/semantics/transcendental_contract.sail"
            ).exists()
        )

    def test_vector_reuses_fp_owned_primitives(self) -> None:
        vector = (
            self.project.root / "extensions/VECTOR/semantics/vector.sail"
        ).read_text()
        vector_owned = vector + "\n".join(
            path.read_text()
            for path in (
                self.project.root / "extensions/VECTOR/instructions/definitions"
            ).glob("*/semantics.sail")
        )

        for constructor in (
            "FpArithmeticAbsolute",
            "FpArithmeticNegate",
            "FpArithmeticAdd",
            "FpArithmeticSubtract",
            "FpArithmeticMultiply",
            "FpArithmeticDivide",
            "FpArithmeticSquareRoot",
            "FpCompareOrdered",
            "FpCompareMinimum",
            "FpCompareMaximum",
            "FpConvertSigned",
            "FpConvertUnsigned",
            "FpDataCopySign",
            "FpDataClassify",
        ):
            self.assertIn(constructor, vector_owned)

        for scalar_operation in (
            "Op_FADD",
            "Op_FSUB",
            "Op_FMUL",
            "Op_FDIV",
            "Op_FCMP",
        ):
            self.assertNotIn(scalar_operation, vector)

        self.assertNotRegex(vector, r"\bOp_[A-Za-z0-9_]+\b")

        conversion_call = vector.split("function vector_fp_conversion_lanes", 1)[1]
        self.assertRegex(
            conversion_call,
            r"fp_primitive_evaluate\(\s+instruction\.form\.operation",
        )

    def test_vector_instruction_owns_its_scattered_semantics_clause(self) -> None:
        definitions = (
            self.project.root / "extensions/VECTOR/instructions/definitions"
        )
        for semantics in definitions.glob("*/semantics.sail"):
            mnemonic = semantics.parent.name
            source = semantics.read_text()
            self.assertIn(
                f"function clause vector_semantics(Op_{mnemonic})",
                source,
                semantics,
            )

    def test_fp_and_vector_instructions_use_the_common_uop_engine(self) -> None:
        for extension in ("FP", "FPTRANSA"):
            definitions = (
                self.project.root / "extensions" / extension / "instructions/definitions"
            )
            for semantics in definitions.glob("*/semantics.sail"):
                source = semantics.read_text()
                self.assertIn("uop_program_execute", source, semantics)
                self.assertNotIn("start_fp_transaction", source, semantics)

        vector_definitions = (
            self.project.root / "extensions/VECTOR/instructions/definitions"
        )
        for semantics in vector_definitions.glob("*/semantics.sail"):
            source = semantics.read_text()
            self.assertIn("uop_program_execute", source, semantics)
            self.assertNotIn("start_vector_", source, semantics)

    def test_fp_and_vector_dedicated_continuation_state_is_removed(self) -> None:
        sources = [
            self.project.root / "execution/semantics/types.sail",
            self.project.root / "execution/semantics/results.sail",
            self.project.root / "execution/semantics/continuation/common.sail",
            self.project.root / "execution/semantics/continuation/dispatch.sail",
            self.project.root / "extensions/VECTOR/semantics/vector.sail",
        ]
        combined = "\n".join(source.read_text() for source in sources)

        for legacy in (
            "PhaseFp",
            "PhaseVector",
            "fp_pending",
            "vector_payload",
            "start_fp_transaction",
            "start_vector_fp_transaction",
            "start_vector_memory_transaction",
            "resume_fp_phase",
            "resume_vector_phase",
        ):
            self.assertNotIn(legacy, combined)

        self.assertNotIn("PhaseUopWait", combined)
        self.assertIn("PendingUop : Uop_continuation", combined)
        self.assertIn("UopVectorMemoryLoad", combined)
        self.assertIn("UopVectorStepPrepare", combined)

    def test_catalog_projects_every_form_and_representative_record(self) -> None:
        catalog = SailCatalogRenderer().render(self.compose())
        primary, remainder = catalog.split(
            "let effective_address_catalog_cache", 1
        )
        effective_address, representatives = remainder.split(
            "let representative_form_records_cache", 1
        )

        form_count = sum(len(bundle.encodings.forms) for bundle in self.compose().bundles)
        self.assertEqual(primary.count("  struct { form_id = Form_"), form_count)
        self.assertIn("  struct { name = EaForm_", effective_address)
        self.assertEqual(
            representatives.count("  struct { form_id = Form_"), form_count
        )
        self.assertIn(
            "form_id = Form_short_abs_l_q_z_rn_r, bytes = [|0xA8, 0x40|]",
            representatives,
        )

    def test_catalog_initializers_are_split_into_bounded_chunks(self) -> None:
        catalog = SailCatalogRenderer().render(self.compose())
        chunks = re.findall(
            r"let primary_form_catalog_[a-z]+_chunk_\d+ : list\(Catalog_entry\) = "
            r"\[\|(.*?)\|\]",
            catalog,
            re.DOTALL,
        )

        self.assertTrue(chunks)
        self.assertTrue(
            all(
                chunk.count("  struct { form_id = Form_")
                <= SailCatalogRenderer._CATALOG_CHUNK_SIZE
                for chunk in chunks
            )
        )
        self.assertIn("append_catalog_entry_chunks", catalog)

    def test_catalog_binds_fixed_sp_by_operand_role(self) -> None:
        catalog = SailCatalogRenderer().render(self.compose())
        add = next(
            line
            for line in catalog.splitlines()
            if "form_id = Form_short_add_q_imm8_i_sp" in line
            and "operands =" in line
        )

        self.assertIn(
            "name = Operand_dst, operand_type = OperandType_SP, access = AccessReadWrite",
            add,
        )
        self.assertNotIn("name = Operand_src", add)

    def test_registry_declares_generated_catalog_identifiers(self) -> None:
        registry = SailRegistryRenderer().render(self.compose())

        self.assertIn("enum Form_id = Form_invalid", registry)
        self.assertIn("enum Field_id = Field_a", registry)
        self.assertIn("CpuidFlag_FPTRANSA", registry)

    def test_declared_entries_are_defined_by_their_instruction_source(self) -> None:
        SailEntryValidator().require(self.compose())

    def test_declared_full_model_artifact_writes_sail_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            generator = ArtifactGeneratorRegistry.discover(self.project).generator(
                "sail-model"
            )
            self.assertEqual(type(generator).__module__, "_bedrock_artifact_sail_model")
            artifacts = generator.generate(
                ArtifactGenerationContext.create(self.project, directory)
            )
            outputs = ArtifactWriter().write(artifacts, directory)
            project = (Path(directory) / "bedrock-model.sail_project").read_text()
            registry = (Path(directory) / "generated/registry.sail").read_text()

            self.assertEqual(len(outputs), 4)
            self.assertIn("model_base_architectural_types", project)
            self.assertIn("operation_entries", project)
            self.assertIn("model_base_boundary", project)
            self.assertIn("requires registry", project)
            self.assertIn("Op_FADD", registry)
            self.assertIn("Op_VADD", registry)
            self.assertEqual(artifacts.artifact_id, "sail-model")

    def test_project_renderer_preserves_multi_source_unit_order(self) -> None:
        program = self.compose(())
        unit = SailUnit(
            owner="base",
            id="sample",
            source=self.project.root / "model.yaml",
            sources=(
                self.project.root / "privilege/semantics/privilege.sail",
                self.project.root / "predication/semantics/predication.sail",
            ),
            requires=(),
        )
        rendered = SailProjectRenderer().render(
            replace(program, sail_units=(unit,)), self.project.root
        )

        self.assertIn(
            "files\n"
            "    privilege/semantics/privilege.sail,\n"
            "    predication/semantics/predication.sail",
            rendered,
        )

    def test_missing_declared_entry_is_rejected(self) -> None:
        program = self.compose(())
        first = program.bundles[0]
        data = first.instruction.to_dict()
        data["sail_entries"] = ["execute_DOES_NOT_EXIST"]
        bad_instruction = Instruction(
            data, first.instruction.source, first.instruction.isa_root
        )
        bad_bundle = replace(first, instruction=bad_instruction)
        bad_semantics = replace(
            program.instruction_semantics[0], bundle=bad_bundle
        )
        bad_program = replace(program, instruction_semantics=(bad_semantics,))

        with self.assertRaisesRegex(ValueError, "execute_DOES_NOT_EXIST"):
            SailEntryValidator().require(bad_program)


if __name__ == "__main__":
    unittest.main()
