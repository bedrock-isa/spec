#!/usr/bin/env python3
"""Focused owner-level checks for the canonical Decode IR."""

from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import sys
import unittest


TOOLS_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_ROOT))

import decode_ir


class DecodeIrTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ir = decode_ir.load_decode_ir()
        cls.forms = {form.key: form for form in cls.ir.forms}

    def replace_form(self, replacement: decode_ir.FormIR) -> decode_ir.DecodeIR:
        forms = tuple(
            replacement if form.key == replacement.key else form
            for form in self.ir.forms
        )
        return replace(
            self.ir,
            forms=forms,
        )

    def test_live_inventory_and_derived_limits(self) -> None:
        self.assertEqual(len(self.ir.forms), 422)
        self.assertEqual(len(self.ir.mnemonics), 205)
        self.assertEqual(
            tuple(form.index for form in self.ir.forms),
            tuple(range(422)),
        )
        self.assertEqual(
            (
                self.ir.limits.max_opcode_width,
                self.ir.limits.max_operands,
                self.ir.limits.max_ea_operands,
                self.ir.limits.max_fields,
            ),
            (34, 4, 2, 5),
        )
        self.assertEqual(self.ir.limits.max_required_bytes, 25)
        self.assertEqual(self.ir.limits.max_record_bytes, 18)
        self.assertGreater(
            self.ir.limits.max_required_bytes,
            self.ir.limits.max_record_bytes,
        )
        decode_ir.validate_decode_ir(self.ir)

    def test_non_contiguous_fields_use_msb_to_lsb_gathers(self) -> None:
        form = self.forms["medium.abs_x_ea"]
        ea_field = next(field for field in form.fields if field.symbol == "e")
        self.assertEqual(ea_field.positions, (16, 15, 14, 3, 2, 1, 0))
        self.assertTrue(all(
            left > right for left, right in zip(ea_field.positions, ea_field.positions[1:])
        ))

    def test_operand_source_variants_come_from_live_forms(self) -> None:
        tags = {
            operand.source.tag
            for form in self.ir.forms
            for operand in form.operands
        }
        self.assertEqual(
            tags,
            {"encoded-field", "fixed", "appended-payload", "effective-address"},
        )
        fixed = self.forms["extrashort.add_q_8_sp"].operands
        self.assertEqual(fixed[0].source, decode_ir.FixedSourceIR(8, ""))
        self.assertEqual(fixed[1].source, decode_ir.FixedSourceIR(None, "SP"))
        appended = self.forms["long.fmovcr_x_imm16_fn_d"].operands[0].source
        self.assertEqual(appended, decode_ir.AppendedPayloadSourceIR(16, False))
        ea = self.forms["medium.abs_x_ea"].operands[0].source
        self.assertIsInstance(ea, decode_ir.EffectiveAddressSourceIR)

    def test_layout_orders_all_eas_before_appended_payloads(self) -> None:
        two_ea = self.forms["long.cmp_x_ea_s_ea_d"]
        self.assertEqual(
            [(item.tag, item.operand_name) for item in two_ea.layout],
            [("ParseEa", "lhs"), ("ParseEa", "rhs")],
        )
        ea_and_payload = self.forms["long.add_q_imm64_ea_e"]
        self.assertEqual(
            [(item.tag, item.operand_name) for item in ea_and_payload.layout],
            [("ParseEa", "dst"), ("ReadPayload", "src")],
        )
        self.assertEqual(ea_and_payload.fixed_required_bytes, 12)
        self.assertEqual(ea_and_payload.maximum_required_bytes, 22)

    def test_compact_table_is_complete_and_reserved_values_are_explicit(self) -> None:
        entries = self.ir.effective_addresses.compact_entries
        self.assertEqual(tuple(entry.raw for entry in entries), tuple(range(128)))
        invalid = [entry for entry in entries if not entry.valid]
        self.assertEqual([entry.raw for entry in invalid], list(range(0x7A, 0x80)))
        self.assertTrue(all(entry.reserved and entry.invalid_reason for entry in invalid))
        self.assertTrue(all(
            entry.descriptor_bytes in {0, 1, 2}
            and entry.consumed_bytes == entry.descriptor_bytes + entry.payload_width // 8
            for entry in entries
            if entry.valid
        ))

    def test_descriptor_families_keep_exact_lengths_and_mask_value_forms(self) -> None:
        families = {
            family.name: family
            for family in self.ir.effective_addresses.descriptor_families
        }
        self.assertEqual(families["ext1"].descriptor_bytes, 1)
        self.assertEqual(families["ext2"].descriptor_bytes, 2)
        for name, family in families.items():
            expected_width = family.descriptor_bytes * 8
            with self.subTest(family=name):
                self.assertTrue(family.forms)
                self.assertTrue(all(
                    form.member_of_descriptor_family == name
                    and not form.referenced_descriptor_family
                    for form in family.forms
                ))
                self.assertTrue(all(form.width == expected_width for form in family.forms))
                self.assertTrue(all(form.value & ~form.mask == 0 for form in family.forms))
                self.assertTrue(all(
                    len(form.patterns) == family.descriptor_bytes
                    for form in family.forms
                ))
        compact_escape = next(
            form
            for form in self.ir.effective_addresses.compact_forms
            if form.referenced_descriptor_family == "ext1"
        )
        self.assertEqual(compact_escape.member_of_descriptor_family, "")
        serialized_ea = decode_ir.decode_ir_dict(self.ir)["effective_addresses"]
        serialized_compact = next(
            form
            for form in serialized_ea["compact_forms"]
            if form["name"] == compact_escape.name
        )
        serialized_ext1 = serialized_ea["descriptor_families"][0]["forms"][0]
        self.assertEqual(serialized_compact["referenced_descriptor_family"], "ext1")
        self.assertEqual(serialized_compact["member_of_descriptor_family"], "")
        self.assertEqual(serialized_ext1["member_of_descriptor_family"], "ext1")
        self.assertEqual(serialized_ext1["referenced_descriptor_family"], "")
        self.assertNotIn("descriptor_family", serialized_compact)
        self.assertNotIn("descriptor", serialized_compact)

    def test_control_and_free_text_annotations_remain_inspectable(self) -> None:
        setcc = next(form for form in self.ir.forms if form.mnemonic == "SETcc")
        self.assertEqual(setcc.control.predicate_mode, "write_boolean")
        annotated = [form for form in self.ir.forms if form.annotations.flag_effects]
        exceptional = [
            form for form in self.ir.forms if form.annotations.exception_conditions
        ]
        self.assertTrue(annotated)
        self.assertTrue(exceptional)
        self.assertTrue(all(
            item.effect_text
            for form in annotated
            for item in form.annotations.flag_effects
        ))
        self.assertTrue(all(
            item.condition_text
            for form in exceptional
            for item in form.annotations.exception_conditions
        ))

    def test_serialization_is_deterministic_and_json_friendly(self) -> None:
        first = decode_ir.decode_ir_json(self.ir)
        second = decode_ir.decode_ir_json(decode_ir.load_decode_ir())
        self.assertEqual(first, second)
        parsed = json.loads(first)
        self.assertEqual(parsed["limits"]["form_count"], 422)
        self.assertEqual(parsed["forms"][0]["index"], 0)
        self.assertEqual(parsed["forms"][0]["key"], self.ir.forms[0].key)

    def test_owner_validation_rejects_direct_live_ir_invariant_breaks(self) -> None:
        first = self.ir.forms[0]
        duplicate_index = self.replace_form(replace(first, index=1))
        duplicate_key = replace(
            self.ir,
            forms=(replace(first, key=self.ir.forms[1].key),) + self.ir.forms[1:],
        )
        bad_limits = replace(
            self.ir,
            limits=replace(self.ir.limits, max_operands=3),
        )

        encoded_form = next(
            form
            for form in self.ir.forms
            if any(
                isinstance(operand.source, decode_ir.EncodedFieldSourceIR)
                for operand in form.operands
            )
        )
        operand_index = next(
            index
            for index, operand in enumerate(encoded_form.operands)
            if isinstance(operand.source, decode_ir.EncodedFieldSourceIR)
        )
        broken_operand = replace(
            encoded_form.operands[operand_index],
            source=decode_ir.EncodedFieldSourceIR("missing", (0,)),
        )
        broken_operands = (
            encoded_form.operands[:operand_index]
            + (broken_operand,)
            + encoded_form.operands[operand_index + 1 :]
        )
        missing_field = self.replace_form(replace(encoded_form, operands=broken_operands))

        layout_form = self.forms["long.add_q_imm64_ea_e"]
        bad_layout = self.replace_form(
            replace(layout_form, layout=tuple(reversed(layout_form.layout)))
        )

        incomplete_ea = replace(
            self.ir,
            effective_addresses=replace(
                self.ir.effective_addresses,
                compact_entries=self.ir.effective_addresses.compact_entries[:-1],
            ),
        )

        ext1, ext2 = self.ir.effective_addresses.descriptor_families
        bad_length_ea = replace(
            self.ir.effective_addresses,
            descriptor_families=(replace(ext1, descriptor_bytes=2), ext2),
        )
        bad_descriptor_length = replace(self.ir, effective_addresses=bad_length_ea)

        ext2_form = ext2.forms[0]
        descriptor_positions = ext2_form.fields[0].positions
        bad_field = replace(
            ext2_form.fields[0],
            positions=(ext2_form.width,) + descriptor_positions[1:],
        )
        bad_ext2_form = replace(
            ext2_form,
            fields=(bad_field,) + ext2_form.fields[1:],
        )
        bad_field_ea = replace(
            self.ir.effective_addresses,
            descriptor_families=(
                ext1,
                replace(ext2, forms=(bad_ext2_form,) + ext2.forms[1:]),
            ),
        )
        bad_descriptor_field = replace(self.ir, effective_addresses=bad_field_ea)

        for label, broken in (
            ("dense index", duplicate_index),
            ("stable key", duplicate_key),
            ("derived slot limits", bad_limits),
            ("source field", missing_field),
            ("layout order", bad_layout),
            ("compact completeness", incomplete_ea),
            ("descriptor length", bad_descriptor_length),
            ("descriptor field range", bad_descriptor_field),
        ):
            with self.subTest(label=label), self.assertRaises(ValueError):
                decode_ir.validate_decode_ir(broken)


if __name__ == "__main__":
    unittest.main()
