import unittest
from pathlib import Path

import yaml

from engine.ea_mode import EAMode


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

    def test_unqualified_type_reference_is_rejected(self) -> None:
        path = self.isa_root / "ea/modes/compact/register/mode.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["fields"]["r"]["type"] = "Rn"

        with self.assertRaisesRegex(ValueError, "does not match"):
            EAMode(data, path, self.isa_root)

if __name__ == "__main__":
    unittest.main()
