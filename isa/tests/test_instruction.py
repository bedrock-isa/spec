import tempfile
import unittest
from pathlib import Path

import yaml

from engine.instruction import (
    Instruction,
    MnemonicDirectoryMismatchError,
    UnknownRepeatObservedValueError,
)


class InstructionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1]

    @staticmethod
    def document() -> dict:
        return {
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

    def test_constructs_and_exposes_defensive_values(self) -> None:
        source = self.isa_root / "instructions/definitions/ADD/instruction.yaml"
        instruction = Instruction(self.document(), source, self.isa_root)

        self.assertEqual(instruction.mnemonic, "ADD")
        operands = instruction["operands"]
        operands["src"]["access"] = "write"
        self.assertEqual(instruction["operands"]["src"]["access"], "read")

    def test_rejects_mnemonic_directory_mismatch(self) -> None:
        source = self.isa_root / "instructions/definitions/SUB/instruction.yaml"
        with self.assertRaises(MnemonicDirectoryMismatchError):
            Instruction(self.document(), source, self.isa_root)

    def test_rejects_unknown_repeat_observed_value(self) -> None:
        document = self.document()
        document["repeat"]["observed_value"] = "missing"
        source = self.isa_root / "instructions/definitions/ADD/instruction.yaml"

        with self.assertRaises(UnknownRepeatObservedValueError):
            Instruction(document, source, self.isa_root)

    def test_accepts_computed_repeat_observed_value(self) -> None:
        document = self.document()
        document["repeat"]["observed_value"] = "computed"
        source = self.isa_root / "instructions/definitions/ADD/instruction.yaml"

        Instruction(document, source, self.isa_root)

    def test_failed_mutation_is_rolled_back(self) -> None:
        source = self.isa_root / "instructions/definitions/ADD/instruction.yaml"
        instruction = Instruction(self.document(), source, self.isa_root)

        with self.assertRaises(ValueError):
            instruction["privileged"] = "no"

        self.assertIs(instruction["privileged"], False)

    def test_loads_and_saves_instruction_yaml(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            instruction_dir = Path(directory) / "ADD"
            instruction_dir.mkdir()
            source = instruction_dir / "instruction.yaml"
            source.write_text(
                yaml.safe_dump(self.document(), sort_keys=False), encoding="utf-8"
            )

            instruction = Instruction.load(source, self.isa_root)
            instruction["summary"] = "Adds two integer values."
            instruction.save()

            saved = yaml.safe_load(source.read_text(encoding="utf-8"))
            self.assertEqual(saved["summary"], "Adds two integer values.")


if __name__ == "__main__":
    unittest.main()
