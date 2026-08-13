#!/usr/bin/env python3
"""Owner-level checks for the generated combinational D0/D1 decoder."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


TOOLS_ROOT = Path(__file__).resolve().parent
ISA_TOOLS = TOOLS_ROOT.parent
sys.path.insert(0, str(TOOLS_ROOT))
sys.path.insert(0, str(ISA_TOOLS))

import decode_ir
import generate_decoder


def _record_value(bytes_: tuple[int, ...] | list[int]) -> int:
    return sum(byte << (index * 8) for index, byte in enumerate(bytes_))


def _set_gather(payload: int, positions: tuple[int, ...], value: int) -> int:
    for value_bit, position in zip(range(len(positions) - 1, -1, -1), positions):
        if value & (1 << value_bit):
            payload |= 1 << position
        else:
            payload &= ~(1 << position)
    return payload


def _generation_temporary_directory() -> tempfile.TemporaryDirectory[str]:
    raw_root = os.environ.get("SV_TEST_ROOT")
    if not raw_root:
        return tempfile.TemporaryDirectory(prefix="isa-sv-decoder-")
    task_root = Path(raw_root)
    task_root.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(prefix="generation-", dir=task_root)


class SystemVerilogGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ir = decode_ir.load_decode_ir()
        cls.forms = {form.key: form for form in cls.ir.forms}
        cls.temporary_directory = _generation_temporary_directory()
        cls.build_dir = Path(cls.temporary_directory.name)
        generate_decoder.write_outputs(cls.build_dir)
        cls.outputs = generate_decoder.render_outputs(cls.build_dir)
        cls.package_text, cls.names = generate_decoder._render_package(cls.ir)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary_directory.cleanup()

    def form_case_text(self, form: decode_ir.FormIR) -> str:
        d1 = self.outputs[self.build_dir / "bedrock_decode_d1.sv"]
        start = d1.index(f"{self.names.form[form.key]}: begin")
        if form.index + 1 == len(self.ir.forms):
            end = d1.index("        default: result_o.stage", start)
        else:
            next_form = self.ir.forms[form.index + 1]
            end = d1.index(f"{self.names.form[next_form.key]}: begin", start)
        return d1[start:end]

    def compact_case_text(self, raw: int) -> str:
        d1 = self.outputs[self.build_dir / "bedrock_decode_d1.sv"]
        start = d1.index(f"7'h{raw:02x}: begin")
        if raw == 0x7F:
            end = d1.index("        default: begin end", start)
        else:
            end = d1.index(f"7'h{raw + 1:02x}: begin", start)
        return d1[start:end]

    def test_deterministic_round_trip_check_and_stale_output(self) -> None:
        first = generate_decoder.render_outputs(self.build_dir)
        second = generate_decoder.render_outputs(self.build_dir)
        self.assertEqual(first, second)
        self.assertEqual(set(first), {self.build_dir / name for name in generate_decoder.OUTPUT_NAMES})
        self.assertTrue(generate_decoder.check_outputs(self.build_dir))
        stale = self.build_dir / generate_decoder.OUTPUT_NAMES[1]
        stale.write_text(stale.read_text(encoding="utf-8") + "// stale\n", encoding="utf-8")
        self.assertFalse(generate_decoder.check_outputs(self.build_dir))
        generate_decoder.write_outputs(self.build_dir)
        self.assertTrue(generate_decoder.check_outputs(self.build_dir))

    def test_build_directory_safety(self) -> None:
        repository_build = generate_decoder.ROOT / "build" / "sv-decoder"
        self.assertEqual(
            generate_decoder.validate_build_dir(repository_build),
            repository_build.resolve(),
        )
        with tempfile.TemporaryDirectory(prefix="bedrock-sv-safe-", dir="/private/tmp") as temporary:
            external = Path(temporary) / "generated"
            self.assertEqual(generate_decoder.validate_build_dir(external), external.resolve())
        for rejected in (
            generate_decoder.ROOT,
            generate_decoder.ROOT / "isa" / "generated",
            Path("/private/tmp"),
        ):
            with self.subTest(path=rejected), self.assertRaises(ValueError):
                generate_decoder.validate_build_dir(rejected)

    def test_unset_test_root_uses_unique_os_temporary_directories(self) -> None:
        with mock.patch.dict(os.environ, {"SV_TEST_ROOT": ""}):
            first = _generation_temporary_directory()
            second = _generation_temporary_directory()
        first_path = Path(first.name)
        second_path = Path(second.name)
        try:
            self.assertNotEqual(first_path, second_path)
            self.assertEqual(first_path.parent.resolve(), Path(tempfile.gettempdir()).resolve())
            self.assertEqual(second_path.parent.resolve(), Path(tempfile.gettempdir()).resolve())
            self.assertTrue(first_path.is_dir())
            self.assertTrue(second_path.is_dir())
        finally:
            first.cleanup()
            second.cleanup()
        self.assertFalse(first_path.exists())
        self.assertFalse(second_path.exists())

    def test_live_inventory_limits_and_public_interface(self) -> None:
        package = self.outputs[self.build_dir / "bedrock_decode_pkg.sv"]
        d0 = self.outputs[self.build_dir / "bedrock_decode_d0.sv"]
        d1 = self.outputs[self.build_dir / "bedrock_decode_d1.sv"]
        self.assertEqual(
            (
                self.ir.limits.form_count,
                self.ir.limits.mnemonic_count,
                self.ir.limits.max_opcode_width,
                self.ir.limits.max_operands,
                self.ir.limits.max_ea_operands,
                self.ir.limits.max_fields,
                self.ir.limits.max_layout_ops,
                self.ir.limits.max_record_bytes,
            ),
            (422, 205, 34, 4, 2, 5, 2, 18),
        )
        for text in (package, d0, d1):
            self.assertNotIn(" string ", text)
            self.assertNotIn("input wire", text)
        self.assertNotIn("localparam int", package)
        self.assertIn("input  logic valid_i", d0)
        self.assertIn("input  logic [BEDROCK_OPCODE_BITS-1:0] opcode_i", d0)
        self.assertIn("input  logic [BEDROCK_RECORD_BYTES*8-1:0] record_i", d1)
        self.assertIn("input  logic [4:0] byte_count_i", d1)
        self.assertIn("logic statically_legal", package)
        self.assertNotIn("legal_values", package)
        self.assertIn("decoded_ea_t [BEDROCK_EA_SLOTS-1:0] eas", package)
        self.assertNotIn("input logic clk", d0 + d1)
        self.assertNotIn("input logic reset", d0 + d1)
        self.assertNotIn("always_ff", d0 + d1)

    def test_generated_outputs_use_bounded_readable_lines(self) -> None:
        for path, generated in self.outputs.items():
            overlong = [
                (line_number, len(line))
                for line_number, line in enumerate(generated.splitlines(), 1)
                if len(line) > 200
            ]
            self.assertEqual(overlong, [], path.name)

        d0 = self.outputs[self.build_dir / "bedrock_decode_d0.sv"]
        self.assertNotIn("if (!selected && (", d0)
        for form in self.ir.forms:
            for constraint_index, constraint in enumerate(form.constraints):
                signal = f"form_{form.index:03d}_constraint_{constraint_index}_value"
                self.assertIn(
                    f"  logic [{len(constraint.positions) - 1}:0] {signal};",
                    d0,
                )
                assignment = "\n".join(
                    [
                        f"  assign {signal} = {{",
                        *(
                            f"    opcode_i[{position}],"
                            for position in constraint.positions[:-1]
                        ),
                        f"    opcode_i[{constraint.positions[-1]}]",
                        "  };",
                    ]
                )
                self.assertIn(assignment, d0)
                form_comment = f"// form {form.index}: {form.key}"
                self.assertLess(d0.index(form_comment), d0.index(signal, d0.index(form_comment)))

        d1 = self.outputs[self.build_dir / "bedrock_decode_d1.sv"]
        self.assertNotIn("if (!layout_failed && !((", d1)
        for form in self.ir.forms:
            case = self.form_case_text(form)
            for slot, operand in enumerate(form.operands):
                if not operand.legal_values:
                    continue
                comment = f"        // legal values for operand {slot}: {operand.name}"
                self.assertIn(comment, case)
                for value in operand.legal_values:
                    self.assertIn(
                        f"            (result_o.operands[{slot}].value == 64'h{value:016x})",
                        case,
                    )

    def test_public_mask_orders_and_ea_field_bound_are_live_derived(self) -> None:
        package = self.outputs[self.build_dir / "bedrock_decode_pkg.sv"]
        layout = generate_decoder.derive_public_layout(self.ir)
        expected_orders = {
            "SIZE": tuple(sorted({value for form in self.ir.forms for value in form.sizes})),
            "TOUCHED_FLAG": tuple(
                sorted(
                    {
                        value
                        for form in self.ir.forms
                        for value in form.annotations.touched_flags
                    }
                )
            ),
            "POSSIBLE_EVENT": tuple(
                sorted(
                    {
                        value
                        for form in self.ir.forms
                        for value in form.annotations.possible_events
                    }
                )
            ),
        }
        self.assertEqual(layout.size_order, expected_orders["SIZE"])
        self.assertEqual(layout.touched_flag_order, expected_orders["TOUCHED_FLAG"])
        self.assertEqual(layout.possible_event_order, expected_orders["POSSIBLE_EVENT"])

        dimension_names = {
            "SIZE": "BEDROCK_SIZE_MASK_BITS",
            "TOUCHED_FLAG": "BEDROCK_TOUCHED_FLAG_MASK_BITS",
            "POSSIBLE_EVENT": "BEDROCK_POSSIBLE_EVENT_MASK_BITS",
        }
        result_fields = {
            "SIZE": "size_mask",
            "TOUCHED_FLAG": "touched_flag_mask",
            "POSSIBLE_EVENT": "possible_event_mask",
        }
        form_values = {
            "SIZE": lambda form: form.sizes,
            "TOUCHED_FLAG": lambda form: form.annotations.touched_flags,
            "POSSIBLE_EVENT": lambda form: form.annotations.possible_events,
        }
        constant_names: dict[str, dict[str, str]] = {}
        for prefix, order in expected_orders.items():
            dimension = dimension_names[prefix]
            self.assertIn(
                f"localparam logic [9:0] {dimension} = 10'd{len(order)};",
                package,
            )
            names = {
                value: f"BEDROCK_{prefix}_MASK_{generate_decoder._identifier(value)}"
                for value in order
            }
            constant_names[prefix] = names
            for index, value in enumerate(order):
                literal = generate_decoder._hex(len(order), 1 << index)
                self.assertIn(
                    f"localparam logic [{dimension}-1:0] {names[value]} = {literal}; // bit {index}: {value}",
                    package,
                )
        for form in self.ir.forms:
            case = self.form_case_text(form)
            for prefix, order in expected_orders.items():
                selected = set(form_values[prefix](form))
                selected_names = [
                    constant_names[prefix][value]
                    for value in order
                    if value in selected
                ]
                target = f"result_o.{result_fields[prefix]}"
                if not selected_names:
                    assignment = f"        {target} = '0;"
                elif len(selected_names) == 1:
                    assignment = f"        {target} = {selected_names[0]};"
                else:
                    assignment = "\n".join(
                        [
                            f"        {target} =",
                            *(
                                f"          {name}{' |' if index + 1 < len(selected_names) else ';'}"
                                for index, name in enumerate(selected_names)
                            ),
                        ]
                    )
                self.assertIn(assignment, case)

        families = {
            family.name: family
            for family in self.ir.effective_addresses.descriptor_families
        }
        combined_counts = []
        for compact in self.ir.effective_addresses.compact_forms:
            if compact.referenced_descriptor_family:
                combined_counts.extend(
                    len(compact.fields) + len(descriptor.fields)
                    for descriptor in families[compact.referenced_descriptor_family].forms
                )
            else:
                combined_counts.append(len(compact.fields))
        expected_ea_slots = max(combined_counts, default=0)
        self.assertEqual(layout.ea_field_slots, expected_ea_slots)
        self.assertIn(
            f"localparam logic [9:0] BEDROCK_EA_FIELD_SLOTS = 10'd{expected_ea_slots};",
            package,
        )

    def test_appended_payload_signedness_is_public_and_complete(self) -> None:
        package = self.outputs[self.build_dir / "bedrock_decode_pkg.sv"]
        self.assertIn("logic payload_signed;", package)
        appended_signedness = []
        for form in self.ir.forms:
            case = self.form_case_text(form)
            for slot, operand in enumerate(form.operands):
                source = operand.source
                expected = isinstance(source, decode_ir.AppendedPayloadSourceIR) and source.signed
                self.assertIn(
                    f"result_o.operands[{slot}].payload_signed = 1'b{int(expected)};",
                    case,
                )
                if isinstance(source, decode_ir.AppendedPayloadSourceIR):
                    appended_signedness.append(source.signed)
        self.assertIn(True, appended_signedness)
        self.assertIn(False, appended_signedness)

    def test_every_live_form_has_exact_d0_reference_recognition(self) -> None:
        for form in self.ir.forms:
            with self.subTest(form=form.key):
                opcode = generate_decoder.representative_opcode(form)
                self.assertEqual(
                    generate_decoder.reference_d0(
                        self.ir, True, form.opcode_class, opcode
                    ),
                    ("success", form.index),
                )
        self.assertEqual(
            generate_decoder.reference_d0(self.ir, False, "extrashort", 0),
            ("invalid_input", None),
        )
        unallocated_class, unallocated = next(
            (opcode_class, opcode)
            for opcode_class in sorted({form.opcode_class for form in self.ir.forms})
            for opcode in range(
                1
                << min(
                    20,
                    next(
                        form.opcode_width
                        for form in self.ir.forms
                        if form.opcode_class == opcode_class
                    ),
                )
            )
            if generate_decoder.reference_d0(
                self.ir, True, opcode_class, opcode
            )[0]
            == "unallocated_opcode"
        )
        self.assertEqual(
            generate_decoder.reference_d0(
                self.ir, True, unallocated_class, unallocated
            )[0],
            "unallocated_opcode",
        )
        rejected = None
        for form in self.ir.forms:
            for constraint in form.constraints:
                candidates = (
                    [constraint.ranges[0].upper + 1]
                    if constraint.kind == "allow_ranges"
                    else [0, 0x68, 0x6C]
                )
                for value in candidates:
                    if value >= 1 << len(constraint.positions):
                        continue
                    opcode = _set_gather(
                        generate_decoder.representative_opcode(form),
                        constraint.positions,
                        value,
                    )
                    if generate_decoder.reference_d0(
                        self.ir, True, form.opcode_class, opcode
                    )[0] == "constraint_rejected":
                        rejected = (form.opcode_class, opcode)
                        break
                if rejected:
                    break
            if rejected:
                break
        self.assertIsNotNone(rejected)

    def test_complete_compact_and_descriptor_lowering(self) -> None:
        entries = self.ir.effective_addresses.compact_entries
        self.assertEqual(tuple(item.raw for item in entries), tuple(range(128)))
        self.assertEqual(
            [item.raw for item in entries if not item.valid], list(range(0x7A, 0x80))
        )
        d1 = self.outputs[self.build_dir / "bedrock_decode_d1.sv"]
        for entry in entries:
            self.assertIn(f"7'h{entry.raw:02x}: begin", d1)
        for family in self.ir.effective_addresses.descriptor_families:
            self.assertIn(f"cursor + {family.descriptor_bytes}", d1)
            for form in family.forms:
                self.assertIn(f"// {form.name}", d1)
                self.assertIn(self.names.ea_form[form.name], d1)
        self.assertIn(
            "descriptor = {record[(cursor * 8) +: 8], record[((cursor + 1) * 8) +: 8]};",
            d1,
        )
        self.assertIn(
            "payload[0 +: 8] = record[((cursor + 0) * 8) +: 8]",
            d1,
        )
        families = {
            family.name: family
            for family in self.ir.effective_addresses.descriptor_families
        }
        cursor = 2
        for entry in entries:
            record = [0] * 18
            if entry.descriptor_family:
                family = families[entry.descriptor_family]
                descriptor = family.forms[0].value
                for byte in range(family.descriptor_bytes):
                    shift = (family.descriptor_bytes - byte - 1) * 8
                    record[cursor + byte] = (descriptor >> shift) & 0xFF
            stage, decoded, _ = generate_decoder.reference_ea(
                self.ir, entry.raw, record, 18, cursor
            )
            with self.subTest(compact=entry.raw):
                self.assertEqual(stage, "success" if entry.valid else "ea_descriptor")
                self.assertEqual(decoded is not None, entry.valid)
        for family in families.values():
            compact = next(
                form
                for form in self.ir.effective_addresses.compact_forms
                if form.referenced_descriptor_family == family.name
                and form.payload_width == 0
            )
            for descriptor_form in family.forms:
                record = [0] * 18
                for byte in range(family.descriptor_bytes):
                    shift = (family.descriptor_bytes - byte - 1) * 8
                    record[cursor + byte] = (descriptor_form.value >> shift) & 0xFF
                stage, decoded, next_cursor = generate_decoder.reference_ea(
                    self.ir, compact.value, record, 18, cursor
                )
                with self.subTest(family=family.name, descriptor=descriptor_form.name):
                    self.assertEqual(stage, "success")
                    self.assertEqual(decoded["descriptor_form"], descriptor_form.name)
                    self.assertEqual(next_cursor, cursor + family.descriptor_bytes)
        payload_compact = next(
            form
            for form in self.ir.effective_addresses.compact_forms
            if form.payload_width == 64 and not form.referenced_descriptor_family
        )
        record = [0] * 18
        record[cursor : cursor + 8] = range(1, 9)
        stage, decoded, _ = generate_decoder.reference_ea(
            self.ir, payload_compact.value, record, 18, cursor
        )
        self.assertEqual(stage, "success")
        self.assertEqual(decoded["payload"], 0x0807060504030201)
        ext2 = next(
            form
            for form in self.ir.effective_addresses.compact_forms
            if form.referenced_descriptor_family == "ext2"
        )
        self.assertEqual(
            generate_decoder.reference_ea(
                self.ir, ext2.value, [0] * 18, cursor + 1, cursor
            )[0],
            "ea_descriptor",
        )

    def test_invalid_compact_eas_preserve_form_cursor(self) -> None:
        invalid_entries = tuple(
            entry
            for entry in self.ir.effective_addresses.compact_entries
            if not entry.valid
        )
        self.assertEqual(tuple(entry.raw for entry in invalid_entries), tuple(range(0x7A, 0x80)))

        d1 = self.outputs[self.build_dir / "bedrock_decode_d1.sv"]
        initialization = "\n".join(
            [
                "      parse_one_ea = '0;",
                "      parse_one_ea.stage = D1_STAGE_EA_DESCRIPTOR;",
                "      parse_one_ea.next_cursor = cursor_in;",
            ]
        )
        self.assertEqual(d1.count(initialization), 1)
        self.assertLess(d1.index(initialization), d1.index("      unique case (compact_raw)"))

        ea_form = self.forms["medium.abs_x_ea"]
        ea_operand = next(
            operand
            for operand in ea_form.operands
            if isinstance(operand.source, decode_ir.EffectiveAddressSourceIR)
        )
        form_cursor = ea_form.opcode_bytes
        form_case = self.form_case_text(ea_form)
        self.assertIn(
            ");\n          cursor = ea_parse.next_cursor;\n          if (!ea_parse.ok) begin",
            form_case,
        )
        self.assertIn("        result_o.required_bytes = cursor;", form_case)

        for entry in invalid_entries:
            opcode = _set_gather(
                generate_decoder.representative_opcode(ea_form),
                ea_operand.source.positions,
                entry.raw,
            )
            ea_stage, decoded_ea, next_cursor = generate_decoder.reference_ea(
                self.ir,
                entry.raw,
                [0] * self.ir.limits.max_record_bytes,
                self.ir.limits.max_record_bytes,
                form_cursor,
            )
            d1_stage, d1_result = generate_decoder.reference_d1(
                self.ir,
                ea_form,
                opcode,
                [0] * self.ir.limits.max_record_bytes,
                self.ir.limits.max_record_bytes,
            )
            with self.subTest(compact=entry.raw):
                self.assertEqual(ea_stage, "ea_descriptor")
                self.assertIsNone(decoded_ea)
                self.assertEqual(next_cursor, form_cursor)
                self.assertEqual(d1_stage, "ea_descriptor")
                self.assertEqual(d1_result["required_bytes"], form_cursor)
                self.assertEqual(
                    self.compact_case_text(entry.raw).strip(),
                    "\n".join(
                        [
                            f"7'h{entry.raw:02x}: begin // {entry.invalid_reason}",
                            "        parse_one_ea.stage = D1_STAGE_EA_DESCRIPTOR;",
                            "      end",
                        ]
                    ),
                )

    def test_d1_layout_and_boundary_cases_come_from_live_ir(self) -> None:
        two_ea = self.forms["long.cmp_x_ea_s_ea_d"]
        mixed = self.forms["long.add_q_imm64_ea_e"]
        self.assertEqual(
            [item.tag for item in two_ea.layout], ["ParseEa", "ParseEa"]
        )
        self.assertEqual(
            [item.tag for item in mixed.layout], ["ParseEa", "ReadPayload"]
        )
        self.assertEqual(mixed.maximum_required_bytes, 22)
        self.assertGreater(mixed.maximum_required_bytes, self.ir.limits.max_record_bytes)
        d1 = self.outputs[self.build_dir / "bedrock_decode_d1.sv"]
        mixed_start = d1.index(f"{self.names.form[mixed.key]}: begin")
        next_form = self.ir.forms[mixed.index + 1]
        mixed_end = d1.index(f"{self.names.form[next_form.key]}: begin", mixed_start)
        mixed_case = d1[mixed_start:mixed_end]
        self.assertLess(mixed_case.index("parse_one_ea"), mixed_case.index("D1_STAGE_STANDALONE_PAYLOAD"))
        self.assertIn("result_o = '0;", d1)
        self.assertIn("result_o.stage = D1_STAGE_D0_REJECTED;", d1)
        self.assertIn("if (byte_count_i > BEDROCK_RECORD_BYTES)", d1)

        no_layout = next(
            form
            for form in self.ir.forms
            if not form.layout and form.representative_record is not None
        )
        no_layout_record = no_layout.representative_record or ()
        self.assertEqual(
            generate_decoder.reference_d1(
                self.ir,
                no_layout,
                generate_decoder.representative_opcode(no_layout),
                no_layout_record,
                len(no_layout_record),
            )[0],
            "success",
        )

        payload_form = self.forms["long.fmovcr_x_imm16_fn_d"]
        payload_record = list(payload_form.representative_record or ())
        payload_record[payload_form.opcode_bytes : payload_form.opcode_bytes + 2] = [
            0x10,
            0x00,
        ]
        stage, decoded = generate_decoder.reference_d1(
            self.ir,
            payload_form,
            generate_decoder.representative_opcode(payload_form),
            payload_record,
            len(payload_record),
        )
        self.assertEqual(stage, "success")
        self.assertEqual(decoded["values"]["constant_id"], 0x10)
        payload_record[payload_form.opcode_bytes : payload_form.opcode_bytes + 2] = [
            0xFF,
            0xFF,
        ]
        self.assertEqual(
            generate_decoder.reference_d1(
                self.ir,
                payload_form,
                generate_decoder.representative_opcode(payload_form),
                payload_record,
                len(payload_record),
            )[0],
            "static_legality",
        )

        mixed_operand = next(
            operand
            for operand in mixed.operands
            if isinstance(operand.source, decode_ir.EffectiveAddressSourceIR)
        )
        payload64_ea = next(
            form
            for form in self.ir.effective_addresses.compact_forms
            if form.payload_width == 64 and not form.referenced_descriptor_family
        )
        mixed_opcode = _set_gather(
            generate_decoder.representative_opcode(mixed),
            mixed_operand.source.positions,
            payload64_ea.value,
        )
        self.assertEqual(
            generate_decoder.reference_d1(
                self.ir, mixed, mixed_opcode, [0] * 18, 18
            )[0],
            "standalone_payload",
        )

    def test_failed_reads_report_complete_required_thresholds(self) -> None:
        standalone_form = self.forms["long.fmovcr_x_imm16_fn_d"]
        standalone_layout = next(
            layout
            for layout in standalone_form.layout
            if isinstance(layout, decode_ir.ReadPayloadIR)
        )
        standalone_bytes = standalone_layout.width // 8
        standalone_required = standalone_form.opcode_bytes + standalone_bytes
        standalone_stage, standalone_result = generate_decoder.reference_d1(
            self.ir,
            standalone_form,
            generate_decoder.representative_opcode(standalone_form),
            [0] * self.ir.limits.max_record_bytes,
            standalone_required - 1,
        )
        self.assertEqual(standalone_stage, "standalone_payload")
        self.assertEqual(standalone_result["required_bytes"], standalone_required)
        standalone_case = self.form_case_text(standalone_form)
        self.assertIn(
            "\n".join(
                [
                    f"          if ((cursor + {standalone_bytes}) > byte_count_i || (cursor + {standalone_bytes}) > BEDROCK_RECORD_BYTES) begin",
                    "            layout_failed = 1'b1;",
                    "            result_o.stage = D1_STAGE_STANDALONE_PAYLOAD;",
                    f"            cursor = cursor + {standalone_bytes};",
                ]
            ),
            standalone_case,
        )
        self.assertIn("        result_o.required_bytes = cursor;", standalone_case)

        ea_form = self.forms["medium.abs_x_ea"]
        ea_operand = next(
            operand
            for operand in ea_form.operands
            if isinstance(operand.source, decode_ir.EffectiveAddressSourceIR)
        )
        descriptor_family = next(
            family
            for family in self.ir.effective_addresses.descriptor_families
            if family.name == "ext2"
        )
        descriptor_compact = next(
            compact
            for compact in self.ir.effective_addresses.compact_forms
            if compact.referenced_descriptor_family == descriptor_family.name
            and compact.payload_width == 0
        )
        descriptor_opcode = _set_gather(
            generate_decoder.representative_opcode(ea_form),
            ea_operand.source.positions,
            descriptor_compact.value,
        )
        descriptor_required = ea_form.opcode_bytes + descriptor_family.descriptor_bytes
        descriptor_stage, descriptor_result = generate_decoder.reference_d1(
            self.ir,
            ea_form,
            descriptor_opcode,
            [0] * self.ir.limits.max_record_bytes,
            descriptor_required - 1,
        )
        self.assertEqual(descriptor_stage, "ea_descriptor")
        self.assertEqual(descriptor_result["required_bytes"], descriptor_required)
        descriptor_case = self.compact_case_text(descriptor_compact.value)
        self.assertIn(
            "\n".join(
                [
                    f"        if ((cursor + {descriptor_family.descriptor_bytes}) > byte_count || (cursor + {descriptor_family.descriptor_bytes}) > BEDROCK_RECORD_BYTES) begin",
                    "          parse_one_ea.stage = D1_STAGE_EA_DESCRIPTOR;",
                    f"          cursor = cursor + {descriptor_family.descriptor_bytes};",
                ]
            ),
            descriptor_case,
        )

        payload_compact = max(
            (
                compact
                for compact in self.ir.effective_addresses.compact_forms
                if compact.referenced_descriptor_family == descriptor_family.name
                and compact.payload_width
            ),
            key=lambda compact: compact.payload_width,
        )
        payload_opcode = _set_gather(
            generate_decoder.representative_opcode(ea_form),
            ea_operand.source.positions,
            payload_compact.value,
        )
        ea_payload_bytes = payload_compact.payload_width // 8
        payload_required = (
            ea_form.opcode_bytes
            + descriptor_family.descriptor_bytes
            + ea_payload_bytes
        )
        payload_record = [0] * self.ir.limits.max_record_bytes
        descriptor_value = descriptor_family.forms[0].value
        for byte in range(descriptor_family.descriptor_bytes):
            shift = (descriptor_family.descriptor_bytes - byte - 1) * 8
            payload_record[ea_form.opcode_bytes + byte] = (
                descriptor_value >> shift
            ) & 0xFF
        payload_stage, payload_result = generate_decoder.reference_d1(
            self.ir,
            ea_form,
            payload_opcode,
            payload_record,
            payload_required - 1,
        )
        self.assertEqual(payload_stage, "ea_payload")
        self.assertEqual(payload_result["required_bytes"], payload_required)
        payload_case = self.compact_case_text(payload_compact.value)
        self.assertIn(
            "\n".join(
                [
                    f"            if ((cursor + {ea_payload_bytes}) > byte_count || (cursor + {ea_payload_bytes}) > BEDROCK_RECORD_BYTES) begin",
                    "              parse_one_ea.stage = D1_STAGE_EA_PAYLOAD;",
                    f"              cursor = cursor + {ea_payload_bytes};",
                ]
            ),
            payload_case,
        )

        two_ea = self.forms["long.cmp_x_ea_s_ea_d"]
        parse_count = sum(
            isinstance(layout, decode_ir.ParseEaIR) for layout in two_ea.layout
        )
        two_ea_case = self.form_case_text(two_ea)
        self.assertEqual(
            two_ea_case.count("          cursor = ea_parse.next_cursor;"),
            parse_count,
        )
        self.assertEqual(
            two_ea_case.count(
                ");\n          cursor = ea_parse.next_cursor;\n          if (!ea_parse.ok) begin"
            ),
            parse_count,
        )

    def _testbench(self) -> str:
        names = self.names
        lines = [
            "`timescale 1ns/1ps",
            "module tb;",
            "  import bedrock_decode_pkg::*;",
            "  logic valid_i; opcode_class_e opcode_class_i; logic [33:0] opcode_i; d0_result_t d0;",
            "  d0_result_t d0_direct; logic [143:0] record_i; logic [4:0] byte_count_i; d1_result_t d1;",
            "  bedrock_decode_d0 u_d0(.valid_i, .opcode_class_i, .opcode_i, .result_o(d0));",
            "  bedrock_decode_d1 u_d1(.d0_i(d0_direct), .record_i, .byte_count_i, .result_o(d1));",
            "  initial begin",
            "    valid_i = 1'b0; opcode_class_i = OPCODE_CLASS_INVALID; opcode_i = '0;",
            "    d0_direct = '0; record_i = '0; byte_count_i = '0; #1;",
            "    if (d0.status != D0_INVALID_INPUT) $fatal(1, \"D0 invalid-input state\");",
        ]
        for form in self.ir.forms:
            opcode = generate_decoder.representative_opcode(form)
            lines.extend(
                [
                    f"    valid_i = 1'b1; opcode_class_i = {names.opcode_class[form.opcode_class]}; opcode_i = 34'h{opcode:09x}; #1;",
                    f"    if (d0.status != D0_SUCCESS || d0.form != {names.form[form.key]}) $fatal(1, \"D0 {form.key}\");",
                ]
            )

        ea_form = self.forms["medium.abs_x_ea"]
        ea_operand = next(
            operand
            for operand in ea_form.operands
            if isinstance(operand.source, decode_ir.EffectiveAddressSourceIR)
        )
        base_opcode = generate_decoder.representative_opcode(ea_form)
        lines.extend(
            [
                "    valid_i = 1'b0;",
                "    d0_direct = '0; d0_direct.status = D0_SUCCESS;",
                f"    d0_direct.opcode_class = {names.opcode_class[ea_form.opcode_class]};",
                f"    d0_direct.form = {names.form[ea_form.key]};",
                "    record_i = '0; byte_count_i = 5'd18;",
            ]
        )
        family_by_name = {
            family.name: family
            for family in self.ir.effective_addresses.descriptor_families
        }
        for entry in self.ir.effective_addresses.compact_entries:
            opcode = _set_gather(base_opcode, ea_operand.source.positions, entry.raw)
            record = [0] * 18
            if entry.descriptor_family:
                family = family_by_name[entry.descriptor_family]
                descriptor = family.forms[0].value
                for byte in range(family.descriptor_bytes):
                    shift = (family.descriptor_bytes - byte - 1) * 8
                    record[ea_form.opcode_bytes + byte] = (descriptor >> shift) & 0xFF
            lines.append(
                f"    d0_direct.opcode = 34'h{opcode:09x}; record_i = 144'h{_record_value(record):036x}; #1;"
            )
            expected_valid = 1 if entry.valid else 0
            lines.append(
                f"    if (d1.valid != 1'b{expected_valid}) $fatal(1, \"compact EA {entry.raw:02x}\");"
            )

        family_compact = {
            family.name: next(
                form
                for form in self.ir.effective_addresses.compact_forms
                if form.referenced_descriptor_family == family.name
                and form.payload_width == 0
            )
            for family in self.ir.effective_addresses.descriptor_families
        }
        cursor = ea_form.opcode_bytes
        for family in self.ir.effective_addresses.descriptor_families:
            compact = family_compact[family.name]
            opcode = _set_gather(base_opcode, ea_operand.source.positions, compact.value)
            for descriptor in family.forms:
                record = [0] * 18
                for byte in range(family.descriptor_bytes):
                    shift = (family.descriptor_bytes - byte - 1) * 8
                    record[cursor + byte] = (descriptor.value >> shift) & 0xFF
                lines.extend(
                    [
                        f"    d0_direct.opcode = 34'h{opcode:09x}; record_i = 144'h{_record_value(record):036x}; byte_count_i = 5'd18; #1;",
                        f"    if (!d1.valid || d1.eas[0].descriptor_form != {names.ea_form[descriptor.name]}) $fatal(1, \"descriptor {family.name}/{descriptor.name}\");",
                    ]
                )

        payload_form = self.forms["long.fmovcr_x_imm16_fn_d"]
        payload_record = list(payload_form.representative_record or ())
        payload_record[payload_form.opcode_bytes : payload_form.opcode_bytes + 2] = [0x34, 0x12]
        payload_operand = next(
            index
            for index, operand in enumerate(payload_form.operands)
            if isinstance(operand.source, decode_ir.AppendedPayloadSourceIR)
        )
        lines.extend(
            [
                "    d0_direct = '0; d0_direct.status = D0_SUCCESS;",
                f"    d0_direct.opcode_class = {names.opcode_class[payload_form.opcode_class]}; d0_direct.form = {names.form[payload_form.key]};",
                f"    d0_direct.opcode = 34'h{generate_decoder.representative_opcode(payload_form):09x};",
                f"    record_i = 144'h{_record_value(payload_record):036x}; byte_count_i = 5'd{len(payload_record)}; #1;",
                f"    if (!d1.valid || d1.operands[{payload_operand}].value != 64'h0000000000001234) $fatal(1, \"standalone LE payload\");",
                f"    byte_count_i = 5'd{payload_form.opcode_bytes + 1}; #1;",
                "    if (d1.valid || d1.stage != D1_STAGE_STANDALONE_PAYLOAD) $fatal(1, \"standalone bounds\");",
            ]
        )

        ext2 = family_compact["ext2"]
        ext2_opcode = _set_gather(base_opcode, ea_operand.source.positions, ext2.value)
        lines.extend(
            [
                f"    d0_direct.form = {names.form[ea_form.key]}; d0_direct.opcode = 34'h{ext2_opcode:09x}; record_i = '0; byte_count_i = 5'd{cursor + 1}; #1;",
                "    if (d1.valid || d1.stage != D1_STAGE_EA_DESCRIPTOR) $fatal(1, \"descriptor bounds\");",
                "    d0_direct = '0; #1;",
                "    if (d1.valid || d1.operation != OP_INVALID || d1.operands != '0) $fatal(1, \"stale output\");",
                "    $finish;",
                "  end",
                "endmodule",
                "",
            ]
        )
        return "\n".join(lines)

    def _d0_testbench(self) -> str:
        lines = [
            "`timescale 1ns/1ps",
            "module tb;",
            "  import bedrock_decode_pkg::*;",
            "  logic valid_i; opcode_class_e opcode_class_i; logic [33:0] opcode_i; d0_result_t d0;",
            "  bedrock_decode_d0 dut(.valid_i, .opcode_class_i, .opcode_i, .result_o(d0));",
            "  initial begin",
            "    valid_i = 1'b0; opcode_class_i = OPCODE_CLASS_INVALID; opcode_i = '0; #1;",
            "    if (d0.status != D0_INVALID_INPUT) $fatal(1, \"invalid input\");",
        ]
        for form in self.ir.forms:
            opcode = generate_decoder.representative_opcode(form)
            lines.extend(
                [
                    f"    valid_i = 1'b1; opcode_class_i = {self.names.opcode_class[form.opcode_class]}; opcode_i = 34'h{opcode:09x}; #1;",
                    f"    if (d0.status != D0_SUCCESS || d0.form != {self.names.form[form.key]}) $fatal(1, \"{form.key}\");",
                ]
            )
        lines.extend(["    $finish;", "  end", "endmodule", ""])
        return "\n".join(lines)

    def test_verilator_lint_and_d0_simulation_when_available(self) -> None:
        verilator = shutil.which("verilator")
        if verilator is None:
            self.skipTest("Verilator is not available")
        common = [
            verilator,
            "--Wno-fatal",
            "--Wno-WIDTH",
            "--Wno-UNSIGNED",
            "--Wno-CMPCONST",
            "--Wno-CASEOVERLAP",
        ]
        package, d0, d1 = (str(self.build_dir / name) for name in generate_decoder.OUTPUT_NAMES)
        subprocess.run(
            common + ["--lint-only", "--top-module", "bedrock_decode_d0", package, d0],
            check=True,
            cwd=generate_decoder.ROOT,
        )
        subprocess.run(
            common + ["--lint-only", "--top-module", "bedrock_decode_d1", package, d1],
            check=True,
            cwd=generate_decoder.ROOT,
        )
        testbench = self.build_dir / "tb.sv"
        testbench.write_text(self._d0_testbench(), encoding="utf-8")
        object_dir = self.build_dir / "obj"
        subprocess.run(
            common
            + [
                "--binary",
                "--timing",
                "--top-module",
                "tb",
                "--build-jobs",
                "4",
                "--output-split",
                "2000",
                "--output-split-cfuncs",
                "100",
                "-CFLAGS",
                "-O0",
                "--Mdir",
                str(object_dir),
                package,
                d0,
                str(testbench),
            ],
            check=True,
            cwd=generate_decoder.ROOT,
        )
        subprocess.run([str(object_dir / "Vtb")], check=True, cwd=generate_decoder.ROOT)


if __name__ == "__main__":
    unittest.main()
