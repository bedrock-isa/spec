import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


class InstructionSchemaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        isa_root = Path(__file__).parents[1]
        cls.schema = yaml.safe_load(
            (isa_root / "schemas/instruction.yaml").read_text(encoding="utf-8")
        )
        cls.validator = Draft202012Validator(cls.schema)

    def assert_valid(self, document: dict) -> None:
        self.assertEqual(list(self.validator.iter_errors(document)), [])

    def assert_invalid(self, document: dict) -> None:
        self.assertNotEqual(list(self.validator.iter_errors(document)), [])

    def test_instruction_without_repeat(self) -> None:
        self.assert_valid(
            {
                "mnemonic": "NOP",
                "name": "No Operation",
                "summary": "Performs no operation.",
                "route": "core_control",
                "privileged": False,
                "operands": {},
            }
        )

    def test_rep_instruction(self) -> None:
        self.assert_valid(
            {
                "mnemonic": "FMUL",
                "name": "Floating Multiply",
                "summary": "Multiplies two floating-point values.",
                "route": "fpu",
                "privileged": False,
                "repeat": {"type": "rep"},
                "operands": {
                    "src": {
                        "role": "source",
                        "access": "read",
                        "value_type": "floating",
                    }
                },
            }
        )

    def test_repcc_instruction(self) -> None:
        self.assert_valid(
            {
                "mnemonic": "ADD",
                "name": "Add",
                "summary": "Adds the source operand to the destination operand.",
                "route": "integer_alu",
                "privileged": False,
                "repeat": {"type": "repcc", "observed_value": "dst"},
                "operands": {
                    "src": {
                        "role": "source",
                        "access": "read",
                        "value_type": "integer",
                    },
                    "dst": {
                        "role": "destination",
                        "access": "read_write",
                        "value_type": "integer",
                    },
                },
            }
        )

    def test_rejects_incomplete_repeat_variants(self) -> None:
        base = {
            "mnemonic": "ADD",
            "name": "Add",
            "summary": "Adds values.",
            "route": "integer_alu",
            "privileged": False,
            "operands": {},
        }
        self.assert_invalid({**base, "repeat": {"type": "rep", "observed_value": "dst"}})
        self.assert_invalid({**base, "repeat": {"type": "repcc"}})

    def test_rejects_unknown_fields_and_incomplete_operands(self) -> None:
        base = {
            "mnemonic": "ADD",
            "name": "Add",
            "summary": "Adds values.",
            "route": "integer_alu",
            "privileged": False,
            "operands": {},
        }
        self.assert_invalid({**base, "category": "integer_alu"})
        self.assert_invalid(
            {
                **base,
                "operands": {
                    "src": {"role": "source", "access": "read"},
                },
            }
        )


if __name__ == "__main__":
    unittest.main()
