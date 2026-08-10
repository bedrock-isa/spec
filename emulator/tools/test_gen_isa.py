import unittest

if __package__:
    from tools import gen_isa
else:
    import gen_isa


class RepeatObservationGenerationTests(unittest.TestCase):
    @staticmethod
    def definition(kind: str = "result", operand: str = "dst") -> dict:
        return {
            "mnemonic": "TEST",
            "repeat": {
                "contexts": ["REPcc"],
                "observed": {"kind": kind, "operand": operand},
            },
        }

    @staticmethod
    def entry() -> dict:
        return {
            "id": "short.test_rn_d",
            "fields": {"d": {"kind": "rn", "width": 4}},
        }

    @staticmethod
    def operand(**overrides: object) -> dict:
        operand = {
            "name": "dst",
            "type": "Rn",
            "access": "write",
            "field": "d",
        }
        operand.update(overrides)
        return operand

    def test_emits_canonical_field_and_strong_location(self) -> None:
        rendered = gen_isa.generated_repeat_observation(
            self.definition(), self.entry(), [self.operand()]
        )
        self.assertEqual(
            rendered,
            "Some(RepeatObservation::Result { operand: RepeatObservedOperand { "
            'name: "dst", field: Some(\'d\'), location: RepeatOperandLocation::Rn } })',
        )

    def test_unknown_operand_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown operand"):
            gen_isa.generated_repeat_observation(
                self.definition(operand="missing"), self.entry(), [self.operand()]
            )

    def test_duplicate_canonical_operand_name_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "is duplicated"):
            gen_isa.generated_repeat_observation(
                self.definition(), self.entry(), [self.operand(), self.operand()]
            )

    def test_unknown_observation_kind_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown repeat observation kind"):
            gen_isa.generated_repeat_observation(
                self.definition(kind="mystery"), self.entry(), [self.operand()]
            )

    def test_unsupported_operand_type_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported type"):
            gen_isa.generated_repeat_observation(
                self.definition(),
                self.entry(),
                [self.operand(type="Fn")],
            )


if __name__ == "__main__":
    unittest.main()
