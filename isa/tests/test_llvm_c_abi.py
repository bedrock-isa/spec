from __future__ import annotations

from importlib import import_module
from pathlib import Path
import re
import unittest

from engine.generation import ArtifactDefinition, ArtifactGenerationContext
from engine.project import IsaProject
from engine.reference import Reference
from engine.workspace import SpecWorkspace
from engine.yaml_document import YamlDocumentLoader


ROOT = Path(__file__).resolve().parents[2]


class LlvmCAbiArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workspace = SpecWorkspace.load(ROOT)
        cls.isa = cls.workspace.require_provider("isa")
        if not isinstance(cls.isa, IsaProject):
            raise TypeError("workspace isa provider must be an IsaProject")
        cls.c_abi = cls.workspace.require_provider("abi.c")
        cls.namespace = cls.c_abi.namespaces["base"]
        cls.convention = cls.c_abi.calling_convention
        schema = YamlDocumentLoader().mapping(ROOT / "artifacts/schema.yaml")
        definition = ArtifactDefinition.load(
            ROOT / "artifacts/llvm-c-abi/artifact.yaml", schema
        )
        generated = import_module("artifacts.llvm-c-abi.generator").Generator(
            definition
        ).generate(ArtifactGenerationContext.create(cls.workspace, ROOT))
        cls.tablegen = generated.artifact("BedrockGenCallingConv.td").content
        cls.catalog = generated.artifact("BedrockGenCABI.inc").content

    def test_type_inventory_is_projected_completely(self) -> None:
        actual = set(re.findall(
            r"^BEDROCK_C_TYPE\(([A-Z][A-Z0-9_]+),",
            self.catalog,
            flags=re.MULTILINE,
        ))
        self.assertEqual(actual, set(self.namespace.type_inventory.declared))
        self.assertIn(
            'BEDROCK_C_TYPE(VECTOR, "scalable vector", VECTOR, SYMBOLIC, '
            '0, "VLEN * 8", 16, SCALABLE_VECTOR)',
            self.catalog,
        )
        self.assertIn(
            'BEDROCK_C_TYPE(LONG_DOUBLE, "long double", LONG_DOUBLE, '
            'FIXED, 64, "", 8, BINARY64)',
            self.catalog,
        )

    def test_stack_and_register_classes_come_from_the_convention(self) -> None:
        stack = self.convention.stack
        self.assertIn(
            f"BEDROCK_C_CALLING_CONVENTION("
            f"{stack.pointer.local.element}, DESCENDING, "
            f"{stack.entry_alignment_bytes}, {stack.first_argument_offset_bytes}, "
            f"{stack.argument_slot_bytes}, {stack.sret_register.local.element}, "
            f"{stack.red_zone_bytes})",
            self.catalog,
        )
        for reference in self.convention.register_classes:
            item = self.c_abi.register_classes.resolve(reference)
            self.assertIn(
                f"BEDROCK_C_REGISTER_CLASS({item.id},",
                self.catalog,
            )
            for index, register in enumerate(item.arguments):
                self.assertIn(
                    f"BEDROCK_C_ARGUMENT_REGISTER({item.id}, "
                    f"{index}, {register.local.element})",
                    self.catalog,
                )
            for index, register in enumerate(item.results):
                self.assertIn(
                    f"BEDROCK_C_RESULT_REGISTER({item.id}, "
                    f"{index}, {register.local.element})",
                    self.catalog,
                )

    def test_value_policy_sources_project_directly_to_llvm_catalog(self) -> None:
        for reference, direction in (
            ("base.value_classes.VECTOR_VALUE", "ARGUMENT"),
            ("base.value_classes.PREDICATE_VALUE", "ARGUMENT"),
            ("base.value_classes.AGGREGATE", "RESULT"),
        ):
            item = self.c_abi.value_classes.resolve(Reference.parse(reference))
            policy = item.argument if direction == "ARGUMENT" else item.result
            register_class = self.c_abi.register_classes.resolve(
                policy.register_class
            )
            self.assertEqual(
                self._location_policy(item.id, direction),
                (
                    policy.mode.upper(),
                    register_class.id,
                    policy.units,
                    policy.alignment_units,
                    policy.direct_maximum_bytes or 0,
                ),
            )

        promotion = self.c_abi.promotions.resolve(
            Reference.parse("base.promotions.DEFAULT_FLOAT")
        )
        self.assertIn(
            f"BEDROCK_C_PROMOTION({promotion.id}, F32, "
            f"{promotion.target_kind.upper()})",
            self.catalog,
        )

    def test_preservation_and_tablegen_callee_saved_sets_match(self) -> None:
        by_disposition = {
            item.disposition: tuple(register.local.element for register in item.registers)
            for item in self.convention.preservation
        }
        for disposition, registers in by_disposition.items():
            for register in registers:
                self.assertIn(
                    f"BEDROCK_C_PRESERVATION_REGISTER("
                    f"{disposition.upper()}, {register})",
                    self.catalog,
                )
        self.assertEqual(
            self._tablegen_registers("CSR_Bedrock"),
            by_disposition["callee_saved"],
        )
        expected_spills = tuple(
            register.local.element
            for item in self.convention.preservation
            if item.disposition == "callee_saved"
            for register in item.registers
            if register.local.path[-1] in {"GPR", "FPR", "VECTOR", "PREDICATE"}
        )
        self.assertEqual(
            self._tablegen_registers("CSR_Bedrock_Save"), expected_spills
        )

    def test_tablegen_return_rules_cover_catalog_register_classes(self) -> None:
        for reference in self.convention.register_classes:
            register_class = self.c_abi.register_classes.resolve(reference)
            registers = tuple(
                register.local.element for register in register_class.results
            )
            if not registers:
                continue
            self.assertIn(
                "CCAssignToReg<[" + ", ".join(registers) + "]>", self.tablegen
            )
        self.assertIn(
            "CCIfType<[i1, i8, i16], CCPromoteToType<i32>>", self.tablegen
        )

    def test_runtime_helper_signatures_are_projected(self) -> None:
        for entity_id in self.namespace.runtime_helper_inventory.declared:
            helper = self.c_abi.runtime_helpers.resolve(
                Reference.parse(f"base.runtime_helpers.{entity_id}")
            )
            self.assertIn(
                f'BEDROCK_C_RUNTIME_HELPER({helper.id}, "{helper.symbol}", '
                f"{helper.result.element})",
                self.catalog,
            )
            for index, parameter in enumerate(helper.parameters):
                self.assertIn(
                    f"BEDROCK_C_RUNTIME_PARAMETER({helper.id}, {index}, "
                    f"{parameter.element})",
                    self.catalog,
                )

    def test_memory_order_sequences_are_projected_without_inference(self) -> None:
        for entity_id in self.namespace.memory_order_inventory.declared:
            mapping = self.c_abi.memory_orders.resolve(
                Reference.parse(f"base.memory_orders.{entity_id}")
            )
            self.assertIn(
                f"BEDROCK_C_MEMORY_ORDER({mapping.id}, "
                f"{mapping.instruction_order.upper()}, "
                f"{int(mapping.load is not None)}, "
                f"{int(mapping.store is not None)})",
                self.catalog,
            )
            for operation, sequence in (
                ("LOAD", mapping.load), ("STORE", mapping.store),
                ("THREAD_FENCE", mapping.thread_fence),
            ):
                for index, step in enumerate(sequence or ()):
                    kind = "ACCESS" if step == "access" else "INSTRUCTION"
                    value = "NONE" if step == "access" else step.local.element
                    self.assertIn(
                        f"BEDROCK_C_MEMORY_ORDER_STEP({mapping.id}, "
                        f"{operation}, {index}, {kind}, {value})",
                        self.catalog,
                    )
        self.assertIn(
            "BEDROCK_C_MEMORY_ORDER_STEP(SEQ_CST, LOAD, 0, "
            "INSTRUCTION, AFENCE)",
            self.catalog,
        )

    def test_atomic_lowerings_are_projected_completely(self) -> None:
        for entity_id in self.namespace.atomic_lowering_inventory.declared:
            lowering = self.c_abi.atomic_lowerings.resolve(
                Reference.parse(f"base.atomic_lowerings.{entity_id}")
            )
            self.assertIn(
                f"BEDROCK_C_ATOMIC_LOWERING({lowering.id}, "
                f"{lowering.strategy.upper()})",
                self.catalog,
            )
            for operation in lowering.c_operations:
                self.assertIn(
                    f"BEDROCK_C_ATOMIC_OPERATION({lowering.id}, "
                    f"{operation.upper()})",
                    self.catalog,
                )
            for index, instruction in enumerate(lowering.instructions):
                self.assertIn(
                    f"BEDROCK_C_ATOMIC_INSTRUCTION({lowering.id}, {index}, "
                    f"{instruction.local.element})",
                    self.catalog,
                )

    def test_generated_macro_defaults_do_not_leak(self) -> None:
        macros = re.findall(
            r"^#ifndef (BEDROCK_C_[A-Z0-9_]+)$",
            self.catalog,
            flags=re.MULTILINE,
        )
        for macro in macros:
            self.assertIn(f"#undef {macro}", self.catalog)
            self.assertIn(
                f"#undef BEDROCK_GEN_DEFINED_{macro}", self.catalog
            )

    def _tablegen_registers(self, name: str) -> tuple[str, ...]:
        match = re.search(
            rf"def {name} : CalleeSavedRegs<\s*\(add (.*?)\)>;",
            self.tablegen,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        return tuple(re.findall(r"\b(?:R|F|V|P)\d+\b|CS|DS|SS|GS0|FSTATUS", match.group(1)))

    def _location_policy(
        self, value_class: str, direction: str
    ) -> tuple[str, str, int, int, int]:
        match = re.search(
            rf"^BEDROCK_C_LOCATION_POLICY\({value_class}, {direction}, "
            rf"([A-Z_]+), ([A-Z_]+), (\d+), (\d+), (\d+)\)$",
            self.catalog,
            flags=re.MULTILINE,
        )
        self.assertIsNotNone(match)
        return (
            match.group(1),
            match.group(2),
            int(match.group(3)),
            int(match.group(4)),
            int(match.group(5)),
        )


if __name__ == "__main__":
    unittest.main()
