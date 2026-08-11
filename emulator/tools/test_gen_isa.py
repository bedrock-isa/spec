from pathlib import Path
import tempfile
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


class FixedOperandBytesGenerationTests(unittest.TestCase):
    @staticmethod
    def operand(operand_type: str, field: str | None = None) -> dict:
        return {"name": operand_type, "type": operand_type, "field": field}

    def test_counts_each_fieldless_fixed_width_operand(self) -> None:
        self.assertEqual(
            gen_isa.fixed_operand_bytes(
                "test.form",
                [
                    self.operand("imm8s"),
                    self.operand("imm16s"),
                    self.operand("imm16"),
                    self.operand("imm32s"),
                    self.operand("imm64"),
                    self.operand("fconst_id"),
                ],
            ),
            19,
        )

    def test_repg_body_length_is_an_ordinary_fieldless_imm16(self) -> None:
        self.assertEqual(
            gen_isa.fixed_operand_bytes(
                "medium.repg_rn_r_ea", [self.operand("imm16")]
            ),
            2,
        )

    def test_encoded_operand_payload_is_not_fixed(self) -> None:
        self.assertEqual(
            gen_isa.fixed_operand_bytes(
                "medium.mov_x_ea_e_rn_d", [self.operand("imm64", "e")]
            ),
            0,
        )

    def test_unknown_fieldless_type_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown payload width"):
            gen_isa.fixed_operand_bytes(
                "test.form", [self.operand("future_operand")]
            )


class GeneratedOutputPathTests(unittest.TestCase):
    def assert_rejected(self, output: Path) -> None:
        with self.assertRaisesRegex(ValueError, "repository src directory"):
            gen_isa.validated_output_path(output)

    def test_rejects_active_crate_src(self) -> None:
        self.assert_rejected(
            gen_isa.REPOSITORY_ROOT
            / "emulator/crates/bedrock-isa/src/generated.rs"
        )

    def test_rejects_ignored_candidate_src(self) -> None:
        self.assert_rejected(
            gen_isa.REPOSITORY_ROOT
            / ".codex/.agent/bedrock-emulator-candidate/crates/bedrock-isa/src/generated.rs"
        )

    def test_rejects_normalized_nested_src(self) -> None:
        self.assert_rejected(
            gen_isa.REPOSITORY_ROOT
            / "emulator/crates/bedrock-isa/src/nested/../nested/generated.rs"
        )

    def test_rejects_symlink_resolving_into_src(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            link = Path(temporary) / "linked-src"
            link.symlink_to(
                gen_isa.REPOSITORY_ROOT / "emulator/crates/bedrock-isa/src",
                target_is_directory=True,
            )
            self.assert_rejected(link / "generated.rs")

    def test_allows_non_src_output(self) -> None:
        output = gen_isa.REPOSITORY_ROOT / "build/generated/bedrock-isa.rs"
        self.assertEqual(gen_isa.validated_output_path(output), output.resolve())


if __name__ == "__main__":
    unittest.main()
