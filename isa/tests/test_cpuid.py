import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from engine.check import CpuidValidator
from engine.cpuid import CpuidCatalog, compose_selector
from engine.extension import ExtensionSetCatalog
from engine.project import IsaProject


class CpuidCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1]
        cls.project = IsaProject.load(cls.isa_root)

    def test_loads_distributed_namespaces_and_canonical_references(self) -> None:
        cpuid = self.project.cpuid

        self.assertEqual(tuple(cpuid.namespaces), ("base", "FP", "FPTRANSA", "VECTOR"))
        self.assertEqual(cpuid.references.classes["base.cpuid.BASE"].value, 0)
        self.assertEqual(
            cpuid.references.leaves["VECTOR.cpuid.EXTENSIONS.VECTOR_PARAMETERS"].value,
            2,
        )
        self.assertEqual(
            cpuid.references.queries[
                "FPTRANSA.cpuid.EXTENSIONS.FPTRANSA_ACCURACY.FLOG2A"
            ].indexes.first,
            0x0043,
        )
        self.assertEqual(
            cpuid.references.fields["FP.cpuid.EXTENSIONS.DIRECTORY.FEATURES.FP"].lsb,
            0,
        )

    def test_matches_architectural_numeric_allocations(
        self,
    ) -> None:
        cpuid = self.project.cpuid
        self.assertEqual(cpuid.references.classes["base.cpuid.EXTENSIONS"].value, 1)
        self.assertEqual(cpuid.references.classes["base.cpuid.IMPLEMENTATION"].value, 2)
        self.assertEqual(
            cpuid.references.leaves["base.cpuid.IMPLEMENTATION.SAVE_AREA_LAYOUT"].value,
            4,
        )
        self.assertEqual(
            compose_selector(1, 1, 0x0043),
            0x0000000100010043,
        )

    def test_reports_each_numeric_allocation_boundary(self) -> None:
        cases = (
            (
                "cpuid/classes/IMPLEMENTATION/class.yaml",
                lambda document: document.update(value=1),
                "cpuid.class.value-overlap",
            ),
            (
                "extensions/VECTOR/cpuid/classes/EXTENSIONS/leaves/"
                "VECTOR_PARAMETERS/leaf.yaml",
                lambda document: document.update(value=1),
                "cpuid.leaf.value-overlap",
            ),
            (
                "cpuid/classes/IMPLEMENTATION/leaves/ADDRESS_WIDTHS/leaf.yaml",
                lambda document: document["queries"][1].update(index=0),
                "cpuid.query.index-overlap",
            ),
            (
                "extensions/VECTOR/cpuid/classes/EXTENSIONS/leaves/DIRECTORY/leaf.yaml",
                lambda document: document["queries"][0]["fields"][0].update(lsb=0),
                "cpuid.field.overlay-overlap",
            ),
        )

        for relative, mutate, expected_code in cases:
            with self.subTest(code=expected_code), self.cpuid_fixture() as directory:
                root = Path(directory)
                path = root / relative
                document = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutate(document)
                path.write_text(
                    yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
                )

                catalog = CpuidCatalog.load(root, ExtensionSetCatalog.load(root))
                codes = [item.code for item in CpuidValidator().validate(catalog)]

                self.assertIn(expected_code, codes)

    def cpuid_fixture(self):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "schemas").mkdir()
        (root / "extensions").mkdir()
        for schema in ("cpuid-class.yaml", "cpuid-leaf.yaml"):
            shutil.copy2(self.isa_root / "schemas" / schema, root / "schemas" / schema)
        shutil.copytree(self.isa_root / "cpuid", root / "cpuid")
        extension_ids = ("FP", "FPTRANSA", "VECTOR")
        (root / "extensions/extensions.yaml").write_text(
            yaml.safe_dump({"extensions": list(extension_ids)}, sort_keys=False),
            encoding="utf-8",
        )
        for extension_id in extension_ids:
            destination = root / "extensions" / extension_id
            destination.mkdir()
            shutil.copytree(
                self.isa_root / "extensions" / extension_id / "cpuid",
                destination / "cpuid",
            )
        return temporary


if __name__ == "__main__":
    unittest.main()
