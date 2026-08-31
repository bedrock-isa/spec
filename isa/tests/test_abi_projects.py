import unittest
from pathlib import Path
from types import SimpleNamespace

from abi.c.model import CAbiProject
from abi.c.model.call_layout import Argument, Call, ReturnValue, default_rules, layout_call
from abi.elf.model import ElfAbiProject
from abi.elf.model.project import (
    DebugRegisterRangeError,
    DebugRegisterRangeErrorReason,
    DebugRegisterRangeTopology,
)
from abi.elf.model.relocation_metasyntax import (
    RelocationMetasyntax,
    RelocationMetasyntaxError,
)
from engine.project import IsaProject
from engine.reference import Reference
from engine.workspace import SpecWorkspace


class AbiProjectTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = Path(__file__).parents[2]
        cls.workspace = SpecWorkspace.load(cls.repository)
        cls.isa = cls.workspace.require_provider("isa")
        if not isinstance(cls.isa, IsaProject):
            raise TypeError("workspace isa provider must be an IsaProject")

    def test_elf_inventory_loads_hierarchical_members(self) -> None:
        project = self.workspace.require_provider("abi.elf")
        self.assertIsInstance(project, ElfAbiProject)
        relocation = project.relocations.resolve(
            Reference.parse("base.relocations.R_BEDROCK_CALL32S")
        )
        self.assertEqual(relocation.value, 21)
        self.assertEqual(relocation.calculation.code, "symbol + addend - next_pc")
        entry = project.process_entry
        self.assertEqual(entry.entry_point.local.element, "PC")
        self.assertEqual(entry.stack_alignment_bytes, 16)
        self.assertEqual(entry.stack_permissions, ("read", "write"))
        self.assertEqual(set(entry.segment_contexts), {"code", "data", "stack"})
        self.assertEqual(entry.payload_owner, "external-process-entry-abi")
        vector_numbers = next(
            item for item in project.resolved_debug_registers(self.workspace)
            if item.group == "VECTOR"
        )
        self.assertEqual((vector_numbers.first, vector_numbers.last), (64, 95))
        self.assertEqual(len(vector_numbers.registers), 32)

    def test_debug_register_ranges_reject_invalid_boundaries(self) -> None:
        def assignment(first, last, *, status="reserved", registers=()):
            return SimpleNamespace(
                first=first,
                last=last,
                status=status,
                registers=tuple(registers),
                source=Path(f"range-{first}.yaml"),
            )

        with self.assertRaises(DebugRegisterRangeError) as caught:
            DebugRegisterRangeTopology.create(
                (assignment(0, None), assignment(1, None))
            )
        self.assertIs(
            caught.exception.reason,
            DebugRegisterRangeErrorReason.UNBOUNDED_NOT_LAST,
        )
        with self.assertRaises(DebugRegisterRangeError) as caught:
            DebugRegisterRangeTopology.create(
                (assignment(0, 0, status="assigned"), assignment(1, None))
            )
        self.assertIs(
            caught.exception.reason,
            DebugRegisterRangeErrorReason.ASSIGNMENT_WIDTH,
        )
        with self.assertRaises(DebugRegisterRangeError) as caught:
            DebugRegisterRangeTopology.create((assignment(0, 0),))
        self.assertIs(
            caught.exception.reason,
            DebugRegisterRangeErrorReason.MISSING_UNBOUNDED_TAIL,
        )

    def test_relocation_metasyntax_preserves_and_parses_authored_expression(self) -> None:
        expression = RelocationMetasyntax.parse("got(symbol) + addend - place")
        self.assertEqual(expression.code, "got(symbol) + addend - place")
        self.assertEqual(expression.expression.kind, "sub")
        self.assertEqual(
            expression.evaluate(
                {"symbol": 7, "got:7": 100, "addend": 4, "place": 20}
            ),
            84,
        )
        with self.assertRaises(RelocationMetasyntaxError):
            RelocationMetasyntax.parse("symbol + mystery")

    def test_c_inventory_resolves_calling_convention_children(self) -> None:
        project = self.workspace.require_provider("abi.c")
        self.assertIsInstance(project, CAbiProject)
        convention = project.resolved_calling_convention(self.workspace)
        self.assertEqual(convention.promotions["f32"], "f64")
        general = next(
            item
            for item in convention.register_classes.values()
            if item.definition.id == "GENERAL"
        )
        self.assertEqual(
            tuple(register.id for register in general.arguments),
            tuple(f"R{index}" for index in range(8)),
        )
        exchange = project.atomic_lowerings.resolve(
            Reference.parse("base.atomic_lowerings.EXCHANGE")
        )
        self.assertEqual(exchange.strategy, "compare_exchange_loop")
        self.assertEqual(exchange.instructions[0].local.element, "CMPXCHG")

    def test_c_call_layout_applies_declared_exhaustion_and_result_policies(self) -> None:
        rules = default_rules()
        vector_class = rules.value_class("vector").argument_register_class
        predicate_class = rules.value_class("predicate").argument_register_class
        self.assertIsNotNone(vector_class)
        self.assertIsNotNone(predicate_class)
        assert vector_class is not None
        assert predicate_class is not None
        vector_arguments = tuple(
            Argument(f"v{index}", "vector")
            for index in range(len(vector_class.arguments) + 1)
        )
        predicate_arguments = tuple(
            Argument(f"p{index}", "predicate")
            for index in range(len(predicate_class.arguments) + 1)
        )
        argument_layout = layout_call(
            Call(vector_arguments + predicate_arguments, ReturnValue("void")),
            rules,
        )
        projected = argument_layout["arguments"]
        vector_overflow = len(vector_class.arguments)
        predicate_start = len(vector_arguments)
        predicate_overflow = predicate_start + len(predicate_class.arguments)
        general = rules.register_classes_by_id["GENERAL"]
        self.assertEqual(
            tuple(item["location"] for item in projected[:vector_overflow]),
            tuple(register.id for register in vector_class.arguments),
        )
        self.assertEqual(
            projected[vector_overflow],
            {
                "name": f"v{vector_overflow}",
                "source_kind": "vector",
                "effective_kind": "vector",
                "mode": "copy-address",
                "location": general.arguments[0].id,
            },
        )
        self.assertEqual(
            tuple(
                item["location"]
                for item in projected[predicate_start:predicate_overflow]
            ),
            tuple(register.id for register in predicate_class.arguments),
        )
        self.assertEqual(
            projected[predicate_overflow],
            {
                "name": f"p{len(predicate_class.arguments)}",
                "source_kind": "predicate",
                "effective_kind": "predicate",
                "mode": "copy-address",
                "location": general.arguments[1].id,
            },
        )

        aggregate = rules.value_class("aggregate")
        maximum = aggregate.definition.result.direct_maximum_bytes
        self.assertIsNotNone(maximum)
        assert maximum is not None
        direct_result = layout_call(
            Call((), ReturnValue("aggregate", maximum)), rules
        )
        indirect_result = layout_call(
            Call((), ReturnValue("aggregate", maximum + 1)), rules
        )
        result_class = aggregate.result_register_class
        self.assertIsNotNone(result_class)
        assert result_class is not None
        result_units = aggregate.definition.result.units
        self.assertIsNotNone(result_units)
        assert result_units is not None
        self.assertEqual(
            direct_result["return_location"],
            ":".join(
                register.id
                for register in reversed(result_class.results[:result_units])
            ),
        )
        self.assertIsNone(direct_result["sret"])
        self.assertEqual(
            indirect_result["return_location"],
            rules.convention.sret_register.id,
        )
        self.assertEqual(
            indirect_result["sret"],
            rules.convention.sret_register.id,
        )

if __name__ == "__main__":
    unittest.main()
