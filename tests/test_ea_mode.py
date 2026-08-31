import unittest
from pathlib import Path

from engine.ea_mode import EAMode, EAModeCatalog
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
                    mode = EAMode.load(path, self.isa_root, types)
                    self.assertEqual(mode.catalog, catalog)

if __name__ == "__main__":
    unittest.main()
