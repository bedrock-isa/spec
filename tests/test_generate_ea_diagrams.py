import tempfile
import unittest
from pathlib import Path

from engine.ea_mode import EABaseSource, EAMode, EAModeCatalog
from engine.generate_ea_diagrams import catalog_mode_paths, main, project_mode
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

    def test_autoupdate_projection_follows_encoding_variants(self) -> None:
        mode = self.load("ea/modes/EXT2/explicit_segment_index/mode.yaml")
        projection = project_mode(mode)

        self.assertEqual(
            tuple(update.encoding_index for update in projection.autoupdates),
            tuple(
                index
                for index, encoding in enumerate(mode["encodings"])
                if "autoupdate" in encoding
            ),
        )
        self.assertTrue(
            all(
                projection.encodings[update.encoding_index].autoupdate is update
                for update in projection.autoupdates
            )
        )
        self.assertEqual(projection.flow.base_source, EABaseSource.ENCODED)
        self.assertIsNotNone(projection.flow.index_operand)
        self.assertTrue(projection.flow.has_displacement)
        self.assertTrue(projection.flow.has_scale)
        self.assertTrue(projection.flow.has_memory_tail)

    def test_mode_without_autoupdate_has_no_update_projection(self) -> None:
        mode = self.load("ea/modes/compact/register/mode.yaml")
        projection = project_mode(mode)

        self.assertEqual(projection.autoupdates, ())
        self.assertTrue(projection.encodings)
        self.assertTrue(
            all(
                sum(field.bits for field in encoding.fields)
                == len("".join(mode["encodings"][index]["pattern"]))
                for index, encoding in enumerate(projection.encodings)
            )
        )

    def test_cli_serializes_the_declared_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "ea-diagrams.tex"

            status = main(["--isa-root", str(self.isa_root), "--output", str(output)])

            self.assertEqual(status, 0)
            self.assertTrue(output.read_bytes())


if __name__ == "__main__":
    unittest.main()
