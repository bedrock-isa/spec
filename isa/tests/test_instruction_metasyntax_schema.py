import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


class InstructionMetasyntaxSchemaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        isa_root = Path(__file__).parents[1]
        cls.schema = yaml.safe_load(
            (isa_root / "schemas/instruction-metasyntax.yaml").read_text(
                encoding="utf-8"
            )
        )

    def test_accepts_nonempty_instruction_syntax(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        validator = Draft202012Validator(self.schema)
        self.assertEqual(list(validator.iter_errors("ADD.Q Rn(s), Rn(d)")), [])

    def test_rejects_empty_and_non_string_instruction_syntax(self) -> None:
        validator = Draft202012Validator(self.schema)
        for value in ("", None, []):
            with self.subTest(value=value):
                self.assertTrue(list(validator.iter_errors(value)))


if __name__ == "__main__":
    unittest.main()
