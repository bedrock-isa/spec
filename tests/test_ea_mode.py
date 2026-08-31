import unittest
from pathlib import Path

from engine.ea_mode import EABaseSource, EAMode, EAModeCatalog, EAModeSchemaError
from engine.reference import Reference
from engine.type_system import TypeSystem


class EAModeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1] / "isa"

    def test_all_concrete_modes_validate(self) -> None:
        types = TypeSystem.load(self.isa_root)
        for catalog in EAModeCatalog.discover(self.isa_root, types):
            actual = {
                path.name
                for path in catalog.source.parent.iterdir()
                if path.is_dir() and not path.name.startswith(".")
            }
            self.assertEqual(set(catalog.modes), actual)
            for mode_id in catalog.modes:
                path = catalog.mode_path(mode_id)
                with self.subTest(path=path):
                    EAMode.load(path, self.isa_root, types)

    def test_catalog_name_is_explicit_reader_text(self) -> None:
        catalogs = EAModeCatalog.discover(
            self.isa_root,
            TypeSystem.load(self.isa_root),
        )
        fp = next(catalog for catalog in catalogs if catalog.owner == "FP")

        self.assertEqual(fp.name, "FP FEA compact")
        self.assertEqual(fp.profile, "fea")
        self.assertEqual(fp.mode_type, "compact")
        self.assertEqual(
            fp.reference("immediate"),
            Reference.parse("FP.fea.modes.compact.immediate"),
        )

    def test_unqualified_type_reference_is_rejected(self) -> None:
        path = self.isa_root / "ea/modes/compact/register/mode.yaml"
        import yaml
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["fields"]["r"]["type"] = "Rn"

        with self.assertRaises(EAModeSchemaError):
            EAMode(data, path, self.isa_root)

    def test_each_profile_resolves_modes_from_its_own_closed_world_catalog(self) -> None:
        catalogs = EAModeCatalog.discover(
            self.isa_root,
            TypeSystem.load(self.isa_root),
        )
        by_profile_type = {
            (catalog.profile, catalog.mode_type): catalog for catalog in catalogs
        }

        for profile in ("ea", "fea", "vea"):
            compact = by_profile_type[profile, "compact"]
            self.assertTrue(compact.modes)
            for mode_id in compact.modes:
                with self.subTest(profile=profile, mode=mode_id):
                    self.assertTrue(compact.mode_path(mode_id).is_file())
                    self.assertEqual(
                        EAMode.load(compact.mode_path(mode_id), self.isa_root).catalog,
                        compact,
                    )
            for family in ("EXT1", "EXT2"):
                descriptor = by_profile_type[profile, family]
                self.assertTrue(descriptor.modes)
                for mode_id in descriptor.modes:
                    with self.subTest(profile=profile, family=family, mode=mode_id):
                        self.assertTrue(descriptor.mode_path(mode_id).is_file())

    def test_base_source_is_parsed_from_the_mode_expression(self) -> None:
        types = TypeSystem.load(self.isa_root)
        catalogs = {
            (catalog.profile, catalog.mode_type): catalog
            for catalog in EAModeCatalog.discover(self.isa_root, types)
        }
        compact = catalogs["ea", "compact"]
        ext1 = catalogs["ea", "EXT1"]

        self.assertEqual(
            EAMode.load(compact.mode_path("register"), self.isa_root, types).base_source,
            EABaseSource.ENCODED,
        )
        self.assertEqual(
            EAMode.load(
                compact.mode_path("stack_pointer_displaced"), self.isa_root, types
            ).base_source,
            EABaseSource.STACK_POINTER,
        )
        self.assertEqual(
            EAMode.load(
                compact.mode_path("program_counter_displaced"), self.isa_root, types
            ).base_source,
            EABaseSource.PROGRAM_COUNTER,
        )
        self.assertEqual(
            EAMode.load(
                ext1.mode_path("explicit_segment_zero_base"), self.isa_root, types
            ).base_source,
            EABaseSource.ZERO,
        )
        self.assertEqual(
            EAMode.load(compact.mode_path("absolute"), self.isa_root, types).base_source,
            EABaseSource.NONE,
        )

if __name__ == "__main__":
    unittest.main()
