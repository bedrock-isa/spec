import unittest
from pathlib import Path

import yaml

from engine.ea_mode import EABaseSource, EAMode, EAModeCatalog
from engine.reference import Reference
from engine.type_system import TypeSystem


class EAModeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1]

    def test_all_concrete_modes_validate(self) -> None:
        paths = [
            path
            for path in self.isa_root.rglob("mode.yaml")
            if "<" not in str(path)
        ]

        for path in paths:
            with self.subTest(path=path):
                EAMode.load(path, self.isa_root)

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
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["fields"]["r"]["type"] = "Rn"

        with self.assertRaisesRegex(ValueError, "does not match"):
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

    def test_vector_descriptor_update_amounts_are_profile_owned(self) -> None:
        types = TypeSystem.load(self.isa_root)
        catalogs = {
            (catalog.profile, catalog.mode_type): catalog
            for catalog in EAModeCatalog.discover(self.isa_root, types)
        }

        scalar_base = EAMode.load(
            catalogs["ea", "EXT1"].mode_path("default_segment_base"),
            self.isa_root,
            types,
        )
        vector_base = EAMode.load(
            catalogs["vea", "EXT1"].mode_path("default_segment_base"),
            self.isa_root,
            types,
        )
        scalar_index = EAMode.load(
            catalogs["ea", "EXT2"].mode_path("explicit_segment_index"),
            self.isa_root,
            types,
        )
        vector_index = EAMode.load(
            catalogs["vea", "EXT2"].mode_path("explicit_segment_index"),
            self.isa_root,
            types,
        )

        self.assertEqual(
            scalar_base["encodings"][0]["autoupdate"]["difference"], "scale"
        )
        self.assertEqual(
            vector_base["encodings"][0]["autoupdate"]["difference"], "vlen_bytes"
        )
        self.assertEqual(
            scalar_index["encodings"][0]["autoupdate"]["difference"], 1
        )
        self.assertEqual(
            vector_index["encodings"][0]["autoupdate"]["difference"],
            "element_count",
        )

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
