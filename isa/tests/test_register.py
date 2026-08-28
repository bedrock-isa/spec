import shutil
import tempfile
import unittest
from pathlib import Path

from engine.extension import ExtensionSetCatalog
from engine.register import RegisterCatalog
from engine.type_system import PayloadTypeKind, TypeSystem


class RegisterCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1]
        cls.extensions = ExtensionSetCatalog.load(cls.isa_root)
        cls.catalog = RegisterCatalog.load(cls.isa_root, cls.extensions)
        cls.types = TypeSystem.load(cls.isa_root, cls.extensions)

    def test_loads_owner_local_group_hierarchy(self) -> None:
        self.assertEqual(
            tuple(self.catalog.namespaces), ("base", "FP", "FPTRANSA", "VECTOR")
        )
        self.assertEqual(
            self.catalog.references.groups["base.registers.CONTROL"].source,
            self.isa_root / "registers/groups/CONTROL/group.yaml",
        )
        self.assertEqual(
            self.catalog.references.groups["FP.registers.FPR"].source,
            self.isa_root / "extensions/FP/registers/groups/FPR/group.yaml",
        )

    def test_expands_regular_groups_without_member_directories(self) -> None:
        gpr = self.catalog.references.groups["base.registers.GPR"]
        vector = self.catalog.references.groups["VECTOR.registers.VECTOR"]

        self.assertIsNone(gpr.register_inventory)
        self.assertFalse((gpr.root / "registers").exists())
        self.assertEqual(tuple(gpr.registers)[:3], ("R0", "R1", "R2"))
        self.assertEqual(gpr.registers["R15"].encoding, 15)
        self.assertEqual(vector.registers["V31"].width, "VLEN")
        self.assertEqual(vector.registers["V31"].encoding, 31)

    def test_loads_fixed_explicit_inventory_and_layout_companions(self) -> None:
        control = self.catalog.references.groups["base.registers.CONTROL"]
        ptcr = control.registers["PTCR"]
        flags = self.catalog.references.registers["base.registers.STATE.FLAGS"]

        self.assertEqual(
            control.register_inventory.source,
            control.root / "registers/registers.yaml",
        )
        self.assertEqual(ptcr.encoding, 0x0000)
        self.assertEqual(ptcr.layout.source, ptcr.root / "layout.yaml")
        self.assertEqual(
            [(field.id, field.lsb, field.bits) for field in ptcr.layout.fields],
            [("ROOT_PAGE", 12, 44), ("LA57", 7, 1), ("PE", 0, 1)],
        )
        self.assertEqual(flags.layout.bits, 16)

    def test_preserves_control_and_performance_selector_allocations(self) -> None:
        registers = self.catalog.references.registers

        self.assertEqual(registers["base.registers.CONTROL.PMC"].encoding, 0x1100)
        self.assertEqual(registers["base.registers.CONTROL.UCTL"].encoding, 0x010D)
        self.assertEqual(registers["base.registers.PERFORMANCE.CYCLE"].encoding, 1)
        self.assertEqual(registers["base.registers.PERFORMANCE.PTWALK"].encoding, 3)

    def test_type_declarations_own_selector_shape(self) -> None:
        rn = self.types.field_types["base.field_types.Rn"]
        pair = self.types.field_types["base.field_types.PAIRn"]
        cr = self.types.payload_types["base.payload_types.CR"]

        self.assertEqual(rn.register_group, "base.registers.GPR")
        self.assertEqual(pair.register_group, "base.registers.GPR")
        self.assertEqual(cr.kind, PayloadTypeKind.REGISTER_SELECTOR)
        self.assertEqual(cr.register_group, "base.registers.CONTROL")
        self.assertEqual(cr.bytes, 2)

    def test_rejects_series_with_explicit_register_directory(self) -> None:
        with self.fixture() as directory:
            root = Path(directory)
            group = root / "registers/groups/GPR"
            (group / "registers").mkdir()
            (group / "registers/registers.yaml").write_text(
                "registers: []\n", encoding="utf-8"
            )

            with self.assertRaisesRegex(ValueError, "exactly one"):
                RegisterCatalog.load(root)

    def fixture(self):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "schemas").mkdir()
        (root / "extensions").mkdir()
        (root / "registers/groups/GPR").mkdir(parents=True)
        for schema in (
            "register-group.yaml",
            "register.yaml",
            "register-layout.yaml",
        ):
            shutil.copy2(self.isa_root / "schemas" / schema, root / "schemas" / schema)
        (root / "extensions/extensions.yaml").write_text("extensions: []\n")
        (root / "registers/groups/groups.yaml").write_text("groups: [GPR]\n")
        (root / "registers/groups/GPR/group.yaml").write_text(
            "id: GPR\nwidth: 64\nseries: {prefix: R, count: 2}\n"
        )
        return temporary


if __name__ == "__main__":
    unittest.main()
