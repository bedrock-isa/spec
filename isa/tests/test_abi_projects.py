import unittest
from pathlib import Path
from types import SimpleNamespace

from abi.c.model import CAbiProject
from abi.elf.model import ElfAbiProject
from abi.elf.model.project import _validate_debug_register_ranges
from abi.elf.model.relocation_metasyntax import (
    RelocationMetasyntax,
    RelocationMetasyntaxError,
)
from engine.project import IsaProject
from engine.workspace import SpecWorkspace


class AbiProjectTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = Path(__file__).parents[2]
        cls.isa = IsaProject.load(cls.repository / "isa")
        cls.workspace = SpecWorkspace.from_isa(cls.isa)

    def test_elf_inventory_loads_hierarchical_members(self) -> None:
        project = self.workspace.require_provider("abi.elf")
        self.assertIsInstance(project, ElfAbiProject)
        relocation = project.relocations.resolve(
            "base.relocations.R_BEDROCK_CALL32S"
        )
        self.assertEqual(relocation.value, 21)
        self.assertEqual(relocation.calculation.code, "symbol + addend - next_pc")
        entry = project.process_entry
        self.assertEqual(entry.entry_point.local.element, "PC")
        self.assertEqual(entry.stack_alignment_bytes, 16)
        self.assertEqual(entry.stack_permissions, ("read", "write"))
        self.assertEqual(
            tuple(entry.segment_contexts), ("code", "data", "stack")
        )
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

        with self.assertRaisesRegex(ValueError, "unbounded.*must be last"):
            _validate_debug_register_ranges(
                [assignment(0, None), assignment(1, None)]
            )
        with self.assertRaisesRegex(ValueError, "width 1.*assigns 0"):
            _validate_debug_register_ranges(
                [assignment(0, 0, status="assigned"), assignment(1, None)]
            )
        with self.assertRaisesRegex(ValueError, "must end with an unbounded"):
            _validate_debug_register_ranges([assignment(0, 0)])

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
            "base.atomic_lowerings.EXCHANGE"
        )
        self.assertEqual(exchange.strategy, "compare_exchange_loop")
        self.assertEqual(exchange.instructions[0].local.element, "CMPXCHG")

if __name__ == "__main__":
    unittest.main()
