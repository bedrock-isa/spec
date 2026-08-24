from pathlib import Path
import re
import sys
import tempfile
import unittest

if __package__:
    from . import gen_isa
else:
    import gen_isa

ISA_TOOLS = gen_isa.REPOSITORY_ROOT / "isa" / "tools"
sys.path.insert(0, str(ISA_TOOLS))

from encoding_architecture import (
    ENCODING_CLASSES_BY_NAME,
    OPERATOR_SPACE_PREFIX_BITS,
    OPERATOR_SPACE_PREFIXES,
    operator_space_from_prefix,
)
import decode_ir


def _matches_pattern(value: str, pattern: str) -> bool:
    return all(
        expected in "x?" or actual == expected
        for actual, expected in zip(value, pattern, strict=True)
    )


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

    def test_emits_computed_observation_without_an_operand(self) -> None:
        definition = self.definition(kind="computed")
        del definition["repeat"]["observed"]["operand"]
        rendered = gen_isa.generated_repeat_observation(
            definition, self.entry(), [self.operand()]
        )
        self.assertEqual(rendered, "Some(RepeatObservation::Computed)")

    def test_computed_observation_rejects_an_operand(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot name an operand"):
            gen_isa.generated_repeat_observation(
                self.definition(kind="computed"), self.entry(), [self.operand()]
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
                    self.operand("imm8"),
                    self.operand("imm8s"),
                    self.operand("imm16"),
                    self.operand("imm16s"),
                    self.operand("imm32"),
                    self.operand("imm32s"),
                    self.operand("imm64"),
                    self.operand("fconst_id"),
                ],
            ),
            24,
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


class RepositoryGenerationTests(unittest.TestCase):
    def test_current_encoding_architecture_renders_the_rust_catalog(self) -> None:
        rendered = gen_isa.render(gen_isa.REPOSITORY_ROOT)
        self.assertIn("payload_bits: 7,", rendered)
        self.assertIn("payload_bits: 34,", rendered)

    def test_generated_rust_preserves_registry_and_every_form_availability_rule(
        self,
    ) -> None:
        rendered = gen_isa.render(gen_isa.REPOSITORY_ROOT)
        ir = decode_ir.load_decode_ir(
            gen_isa.REPOSITORY_ROOT / "isa" / "instructions" / "definitions"
        )
        for flag in ir.cpuid_flags:
            with self.subTest(flag=flag.id):
                self.assertIn(
                    "GeneratedCpuidFlag { "
                    f"id: {gen_isa.rust_string(flag.id)}, "
                    f"token: {gen_isa.rust_string(flag.token)}, "
                    f"selector_class: {flag.selector_class}, leaf: {flag.leaf}, "
                    f"index: {flag.index}, bit: {flag.bit} "
                    "}",
                    rendered,
                )
        generated_forms = {
            match.group(1): line
            for line in rendered.splitlines()
            if (match := re.search(r'GeneratedForm \{ .*? id: "([^"]+)"', line))
        }
        self.assertEqual(set(generated_forms), {form.key for form in ir.forms})
        for form in ir.forms:
            with self.subTest(form=form.key):
                self.assertIn(
                    f"availability: {gen_isa.generated_availability_rules(form)}",
                    generated_forms[form.key],
                )

    def test_canonical_operator_space_prefixes_drive_generated_rust_rules_and_cases(
        self,
    ) -> None:
        rendered = gen_isa.render(gen_isa.REPOSITORY_ROOT)
        generated = tuple(
            (encoding_class, int(mask, 16), int(value, 16), operator_space)
            for encoding_class, mask, value, operator_space in re.findall(
                r"\(EncodingClass::(\w+), 0x([0-9a-f]+), 0x([0-9a-f]+), "
                r"OperatorSpace::(\w+)\),",
                rendered,
            )
        )
        expected = tuple(
            (
                gen_isa.RUST_ENCODING_CLASSES[allocation.encoding_class],
                *gen_isa.pattern_mask_value(allocation.pattern),
                gen_isa.rust_variant(allocation.operator_space),
            )
            for allocation in OPERATOR_SPACE_PREFIXES
        )
        self.assertEqual(generated, expected)

        generated_cases = tuple(
            (
                encoding_class,
                int(prefix, 16),
                operator_space or None,
            )
            for encoding_class, prefix, _expected, operator_space in re.findall(
                r"\(EncodingClass::(\w+), 0x([0-9a-f]+), "
                r"(None|Some\(OperatorSpace::(\w+)\))\),",
                rendered,
            )
        )
        expected_cases = []
        for encoding_class in dict.fromkeys(
            allocation.encoding_class for allocation in OPERATOR_SPACE_PREFIXES
        ):
            selectors = ENCODING_CLASSES_BY_NAME[encoding_class].selectors
            for prefix in range(1 << OPERATOR_SPACE_PREFIX_BITS):
                bits = f"{prefix:0{OPERATOR_SPACE_PREFIX_BITS}b}"
                if not any(
                    _matches_pattern(bits[: len(selector)], selector)
                    for selector in selectors
                ):
                    continue
                operator_space = operator_space_from_prefix(encoding_class, bits)
                expected_cases.append(
                    (
                        gen_isa.RUST_ENCODING_CLASSES[encoding_class],
                        prefix,
                        None
                        if operator_space is None
                        else gen_isa.rust_variant(operator_space),
                    )
                )
        self.assertEqual(generated_cases, tuple(expected_cases))


if __name__ == "__main__":
    unittest.main()
