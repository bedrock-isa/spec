import unittest
from pathlib import Path

from engine.ea_mode import EAMode, EAModeCatalog
from engine.generate_ea_diagrams import catalog_mode_paths, project_mode
from engine.type_system import TypeSystem


class GenerateEADiagramsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1] / "isa"
        cls.types = TypeSystem.load(cls.isa_root)

    def load(self, relative: str) -> EAMode:
        return EAMode.load(self.isa_root / relative, self.isa_root, self.types)

    def test_catalog_paths_are_the_declared_mode_inventory(self) -> None:
        catalogs = EAModeCatalog.discover(self.isa_root, self.types)
        expected = tuple(
            catalog.mode_path(mode_id)
            for catalog in catalogs
            for mode_id in catalog.modes
        )

        self.assertEqual(tuple(catalog_mode_paths(self.isa_root)), expected)

    def test_mode_projection_preserves_declared_encoding_relations(self) -> None:
        for path in catalog_mode_paths(self.isa_root):
            with self.subTest(mode=path):
                mode = EAMode.load(path, self.isa_root, self.types)
                projection = project_mode(mode)
                updates = tuple(
                    index
                    for index, encoding in enumerate(mode.encodings)
                    if encoding.autoupdate is not None
                )

                self.assertEqual(
                    tuple(
                        update.encoding_index for update in projection.autoupdates
                    ),
                    updates,
                )
                self.assertTrue(
                    all(
                        projection.encodings[update.encoding_index].autoupdate
                        is update
                        for update in projection.autoupdates
                    )
                )
                self.assertEqual(
                    tuple(
                        sum(field.bits for field in encoding.fields)
                        for encoding in projection.encodings
                    ),
                    tuple(
                        len(
                            "".join(patterns)
                        )
                        for patterns in (encoding.patterns for encoding in mode.encodings)
                    ),
                )


if __name__ == "__main__":
    unittest.main()
