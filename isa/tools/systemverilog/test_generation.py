#!/usr/bin/env python3
"""Owner-level checks for the generated combinational D0/D1 decoder."""

from __future__ import annotations

from dataclasses import replace
import os
from pathlib import Path
import re
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
from encoding_architecture import (
    ENCODING_CLASSES_BY_NAME,
    OPERATOR_SPACE_PREFIX_BITS,
    OPERATOR_SPACE_PREFIXES,
    operator_space_from_prefix,
)


def _record_value(bytes_: tuple[int, ...] | list[int]) -> int:
    return sum(byte << (index * 8) for index, byte in enumerate(bytes_))


def _set_gather(payload: int, positions: tuple[int, ...], value: int) -> int:
    for value_bit, position in zip(range(len(positions) - 1, -1, -1), positions):
        if value & (1 << value_bit):
            payload |= 1 << position
        else:
            payload &= ~(1 << position)
    return payload


def _struct_body(package: str, type_name: str) -> str:
    end = package.index(f"  }} {type_name};")
    start = package.rindex("  typedef struct packed {", 0, end)
    return package[start:end]


def _gather_value(raw: int, positions: tuple[int, ...]) -> int:
    value = 0
    for position in positions:
        value = (value << 1) | ((raw >> position) & 1)
    return value


def _canonical_ea(form: decode_ir.EaFormIR, raw: int) -> dict[str, object]:
    result: dict[str, object] = {
        "kind": form.kind,
        "segment": form.segment,
        "base": form.base,
        "register_name": form.register_name,
        "update_target": form.update_target,
        "update_mode": form.update_mode,
        "direct_register_valid": False,
        "direct_register": 0,
        "base_register_valid": False,
        "base_register": 0,
        "index_register_valid": False,
        "index_register": 0,
        "stride_register_valid": False,
        "stride_register": 0,
        "segment_register_valid": False,
        "segment_register": 0,
    }
    member_by_role = {
        "value": "direct_register",
        "base": "base_register",
        "index": "index_register",
        "stride": "stride_register",
        "segment": "segment_register",
    }
    for field in form.fields:
        member = member_by_role[field.role]
        result[f"{member}_valid"] = True
        result[member] = _gather_value(raw, field.positions)
    return result


def _generation_temporary_directory() -> tempfile.TemporaryDirectory[str]:
    raw_root = os.environ.get("SV_TEST_ROOT")
    if not raw_root:
        return tempfile.TemporaryDirectory(prefix="isa-sv-decoder-")
    task_root = Path(raw_root)
    task_root.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(prefix="generation-", dir=task_root)


def _matches_pattern(value: str, pattern: str) -> bool:
    return all(
        expected in "x?" or actual == expected
        for actual, expected in zip(value, pattern, strict=True)
    )


def _class_operator_prefixes(encoding_class: str) -> tuple[int, ...]:
    selectors = ENCODING_CLASSES_BY_NAME[encoding_class].selectors
    return tuple(
        prefix
        for prefix in range(1 << OPERATOR_SPACE_PREFIX_BITS)
        if any(
            _matches_pattern(
                f"{prefix:0{OPERATOR_SPACE_PREFIX_BITS}b}"[: len(selector)],
                selector,
            )
            for selector in selectors
        )
    )


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

    def d0_form_case_text(self, form: decode_ir.FormIR) -> str:
        d0 = self.outputs[self.build_dir / "bedrock_decode_d0.sv"]
        start = d0.index(f"// form {form.index}: {form.key}")
        end = d0.find("\n        // form ", start + 1)
        return d0[start:] if end < 0 else d0[start:end]

    def compact_case_text(self, raw: int, profile: str = "ea") -> str:
        ea = self.outputs[self.build_dir / "bedrock_decode_ea.sv"]
        marker = f"{{{self.names.ea_profile[profile]}, 7'h{raw:02x}}}: begin"
        start = ea.index(marker)
        if raw == 0x7F:
            profile_names = [item.name for item in self.ir.effective_addresses.profiles]
            profile_index = profile_names.index(profile)
            if profile_index + 1 < len(profile_names):
                next_profile = profile_names[profile_index + 1]
                end = ea.index(
                    f"{{{self.names.ea_profile[next_profile]}, 7'h00}}: begin",
                    start,
                )
            else:
                end = ea.index("      default: begin end", start)
        else:
            next_marker = (
                f"{{{self.names.ea_profile[profile]}, 7'h{raw + 1:02x}}}: begin"
            )
            end = ea.index(next_marker, start)
        return ea[start:end]

    def span_case_text(self, raw: int, profile: str = "ea") -> str:
        d1 = self.outputs[self.build_dir / "bedrock_decode_d1.sv"]
        profile_start = d1.index(f"{self.names.ea_profile[profile]}: begin")
        start = d1.index(f"7'h{raw:02x}: begin", profile_start)
        if raw == 0x7F:
            end = d1.index("          default: begin end", start)
        else:
            end = d1.index(f"7'h{raw + 1:02x}: begin", start)
        return d1[start:end]

    def d0_span_case_text(self, raw: int, profile: str = "ea") -> str:
        d0 = self.outputs[self.build_dir / "bedrock_decode_d0.sv"]
        profile_start = d0.index(f"{self.names.ea_profile[profile]}: begin")
        start = d0.index(f"7'h{raw:02x}: begin", profile_start)
        if raw == 0x7F:
            end = d0.index("          default: begin end", start)
        else:
            end = d0.index(f"7'h{raw + 1:02x}: begin", start)
        return d0[start:end]

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

    def test_public_interface(self) -> None:
        package = self.outputs[self.build_dir / "bedrock_decode_pkg.sv"]
        d0 = self.outputs[self.build_dir / "bedrock_decode_d0.sv"]
        d1 = self.outputs[self.build_dir / "bedrock_decode_d1.sv"]
        ea_decoder = self.outputs[self.build_dir / "bedrock_decode_ea.sv"]
        for text in (package, d0, d1, ea_decoder):
            self.assertNotIn(" string ", text)
            self.assertNotIn("input wire", text)
        self.assertNotIn("localparam int", package)
        self.assertIn("BEDROCK_OPCODE_BITS = 10'd42", package)
        self.assertIn("OPCODE_CLASS_XXLONG", package)
        operator_spaces = tuple(
            dict.fromkeys(
                allocation.operator_space for allocation in OPERATOR_SPACE_PREFIXES
            )
        )
        operator_space_width = generate_decoder._width(len(operator_spaces) + 1)
        self.assertIn(
            f"OPERATOR_SPACE_NONE = {operator_space_width}'d0", package
        )
        for operator_space in operator_spaces:
            self.assertIn(
                f"OPERATOR_SPACE_{generate_decoder._identifier(operator_space)}",
                package,
            )
        self.assertIn("input  logic valid_i", d0)
        self.assertIn("input  logic [BEDROCK_OPCODE_BITS-1:0] opcode_i", d0)
        self.assertIn("output d0_ea_result_t ea_result_o", d0)
        self.assertIn("input  logic [BEDROCK_RECORD_BYTES*8-1:0] record_i", d1)
        self.assertIn("input  logic [4:0] byte_count_i", d1)
        self.assertIn("input  logic [BEDROCK_RECORD_BYTES*8-1:0] record_i", ea_decoder)
        self.assertIn("input  logic [4:0] byte_count_i", ea_decoder)
        d0_result = _struct_body(package, "d0_result_t")
        d0_ea_result = _struct_body(package, "d0_ea_result_t")
        operand = _struct_body(package, "decoded_operand_t")
        ea = _struct_body(package, "decoded_ea_t")
        d1_result = _struct_body(package, "d1_opcode_result_t")
        ea_result = _struct_body(package, "ea_decode_result_t")
        parse_result = _struct_body(package, "ea_parse_result_t")
        self.assertIn("ea_layout_e ea_layout;", d0_result)
        self.assertIn("operator_space_e operator_space;", d0_result)
        self.assertNotIn("operator_space", d0_ea_result)
        self.assertNotIn("operator_space", d1_result)
        self.assertNotIn("operator_space", d1)
        self.assertNotIn("operator_space", ea_decoder)
        self.assertIn(
            "operand_ea_width_e [BEDROCK_EA_SLOTS-1:0] ea_widths;",
            d0_result,
        )
        for field in (
            "d0_status_e status;",
            "ea_layout_e ea_layout;",
            "operand_ea_width_e [BEDROCK_EA_SLOTS-1:0] ea_widths;",
            "logic [6:0] low_raw;",
            "logic [6:0] alt_raw;",
            "logic [3:0] base_cursor;",
            "logic [3:0] post_alt_cursor;",
        ):
            self.assertIn(field, d0_ea_result)
        for opcode_field in (
            "opcode_class_e opcode_class;",
            "form_id_e form;",
            "logic [BEDROCK_OPCODE_BITS-1:0] opcode;",
        ):
            self.assertNotIn(opcode_field, d0_ea_result)
        self.assertIn("BEDROCK_EA_LOW_SLOT = 1'd0", package)
        self.assertIn("BEDROCK_EA_ALT_SLOT = 1'd1", package)
        for former in (
            "operand_name_e name;",
            "operand_domain_e domain;",
            "operand_ea_role_e ea_role;",
            "operand_source_e source;",
            "fixed_identity_e fixed_identity;",
            "logic [6:0] width;",
            "logic statically_legal;",
        ):
            self.assertNotIn(former, operand)
        for former in (
            "compact_form",
            "descriptor_form",
            "descriptor_family",
            "payload_name",
            "payload_kind",
            "logic [6:0] raw;",
            "descriptor_bytes",
            "logic [15:0] descriptor;",
            "field_count",
            "decoded_ea_field_t",
            "consumed_bytes",
        ):
            self.assertNotIn(former, ea)
        for former in (
            "d0_status_e d0_status;",
            "opcode_class_e opcode_class;",
            "logic [BEDROCK_OPCODE_BITS-1:0] opcode;",
            "field_count",
            "decoded_field_t",
        ):
            self.assertNotIn(former, d1_result)
        self.assertIn("decoded_ea_t ea;", parse_result)
        self.assertNotIn("decoded_field_t", package)
        self.assertNotIn("decoded_ea_field_t", package)
        self.assertNotIn("result_o.fields", d1)
        self.assertNotIn("result_o.d0_status", d1)
        self.assertNotIn("result_o.opcode_class", d1)
        self.assertNotIn("result_o.opcode =", d1)
        self.assertNotIn("parse_one_ea", d1)
        self.assertNotIn("result_o.eas", d1)
        self.assertNotIn("result_o.ea_count", d1)
        self.assertNotIn("legal_values", package)
        self.assertNotIn("decoded_ea_t", d1_result)
        self.assertNotIn("ea_count", d1_result)
        self.assertIn("decoded_ea_t [BEDROCK_EA_SLOTS-1:0] eas", ea_result)
        self.assertIn("output d1_opcode_result_t result_o", d1)
        self.assertIn("output ea_decode_result_t result_o", ea_decoder)
        self.assertIn("input  d0_ea_result_t d0_i", ea_decoder)
        self.assertNotIn("d1_opcode_result_t", ea_decoder)
        self.assertNotIn("ea_decode_result_t", d1)
        self.assertNotIn("d1_result_t", package)
        self.assertNotIn("d0_i.form", ea_decoder)
        self.assertNotIn("FORM_", ea_decoder)
        self.assertEqual(ea_decoder.count(" = parse_one_ea("), 2)
        self.assertEqual(
            d0.count("function automatic ea_span_result_t encoded_ea_span("),
            1,
        )
        self.assertEqual(
            d1.count("function automatic ea_span_result_t encoded_ea_span("),
            1,
        )
        self.assertNotIn("function automatic ea_span_result_t encoded_ea_span(", ea_decoder)
        self.assertIn("ea_result_o.low_raw = opcode_i[6:0];", d0)
        self.assertIn(
            "ea_result_o.alt_raw = {opcode_i[16:14], opcode_i[3:0]};",
            d0,
        )
        self.assertIn("ea_result_o.alt_raw = opcode_i[13:7];", d0)
        self.assertIn(
            "alt_span = encoded_ea_span(\n"
            "      class_selection.ea_profiles[BEDROCK_EA_ALT_SLOT],\n"
            "      ea_result_o.alt_raw\n"
            "    );",
            d0,
        )
        self.assertIn(
            "if (alt_span.valid)\n"
            "      ea_result_o.post_alt_cursor =\n"
            "        ea_result_o.base_cursor + {2'b0, alt_span.encoded_bytes};",
            d0,
        )
        self.assertIn("low_cursor = d0_i.base_cursor;", ea_decoder)
        self.assertIn(
            "if (d0_i.ea_layout == EA_LAYOUT_ALT_THEN_LOW)\n"
            "      low_cursor = d0_i.post_alt_cursor;",
            ea_decoder,
        )
        self.assertNotIn("d0_i.opcode", ea_decoder)
        self.assertNotIn("d0_i.opcode_class", ea_decoder)
        self.assertNotIn("opcode_class_bytes", ea_decoder)
        self.assertNotIn("alt_span", ea_decoder)
        self.assertNotIn("low_cursor = alt_parse.next_cursor;", ea_decoder)
        self.assertIn(
            "if (low_parse.ok &&\n"
            "            (d0_i.ea_layout != EA_LAYOUT_ALT_THEN_LOW || alt_parse.ok))",
            ea_decoder,
        )
        self.assertNotIn("input logic clk", d0 + d1 + ea_decoder)
        self.assertNotIn("input logic reset", d0 + d1 + ea_decoder)
        self.assertNotIn("always_ff", d0 + d1 + ea_decoder)
        for form in self.ir.forms:
            marker = f"{self.names.form[form.key]}: begin // {form.index}: {form.key}"
            self.assertIn(marker, d1)
            self.assertNotIn(marker, ea_decoder)

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
        self.assertNotIn("logic selected;", d0)
        self.assertNotIn("selected =", d0)
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

    def test_two_class_position_candidates_cover_every_form(self) -> None:
        d0 = self.outputs[self.build_dir / "bedrock_decode_d0.sv"]
        for form in self.ir.forms:
            layout = generate_decoder._ea_layout(form)
            low_width, alt_width = generate_decoder._ea_candidate_widths(
                form, self.names
            )
            low_profile, alt_profile = generate_decoder._ea_candidate_profiles(
                form, self.names
            )
            selection = f"form_{form.index:03d}_selection"
            self.assertIn(f"assign {selection}.ea_layout = {layout};", d0)
            self.assertIn(
                f"assign {selection}.ea_widths[BEDROCK_EA_LOW_SLOT] = "
                f"{low_width};",
                d0,
            )
            self.assertIn(
                f"assign {selection}.ea_widths[BEDROCK_EA_ALT_SLOT] = "
                f"{alt_width};",
                d0,
            )
            self.assertIn(
                f"assign {selection}.ea_profiles[BEDROCK_EA_LOW_SLOT] = "
                f"{low_profile};",
                d0,
            )
            self.assertIn(
                f"assign {selection}.ea_profiles[BEDROCK_EA_ALT_SLOT] = "
                f"{alt_profile};",
                d0,
            )
            d1_case = self.form_case_text(form)
            for slot, operand in enumerate(form.operands):
                if isinstance(
                    operand.source, decode_ir.EffectiveAddressSourceIR
                ):
                    candidate = generate_decoder._ea_candidate_slot(form, operand)
                    self.assertIn(
                        f"result_o.operands[{slot}].ea_slot = 1'd{candidate};",
                        d1_case,
                    )
    def test_d0_rejects_overlapping_accepted_forms(self) -> None:
        left = self.ir.forms[0]
        right = self.ir.forms[1]
        overlapping_right = replace(
            right,
            opcode_class=left.opcode_class,
            opcode_space_bytes=left.opcode_space_bytes,
            opcode_width=left.opcode_width,
            opcode_value=left.opcode_value,
            opcode_mask=left.opcode_mask,
            constraints=left.constraints,
        )
        forms = list(self.ir.forms)
        forms[right.index] = overlapping_right
        overlapping_ir = replace(self.ir, forms=tuple(forms))
        with self.assertRaisesRegex(
            ValueError,
            rf"D0 accepted forms overlap.*{re.escape(left.key)}.*"
            rf"{re.escape(right.key)}",
        ):
            generate_decoder._render_d0(overlapping_ir, self.names)

    def test_d0_uses_complete_balanced_form_and_metadata_trees(self) -> None:
        d0 = self.outputs[self.build_dir / "bedrock_decode_d0.sv"]
        selection_nodes = {
            match.group(1): (match.group(2), match.group(3))
            for match in re.finditer(
                r"  assign (\w+_selection_node_\d+) = "
                r"(\w+)\.valid \? \2 : (\w+);",
                d0,
            )
        }
        raw_nodes = {
            match.group(1): (match.group(2), match.group(3))
            for match in re.finditer(
                r"  assign (\w+_raw_node_\d+) = \((\w+) \| (\w+)\);",
                d0,
            )
        }
        form_nodes = {
            match.group(1): (match.group(2), match.group(3))
            for match in re.finditer(
                r"  assign (\w+_form_node_\d+) = \((\w+) \| (\w+)\);",
                d0,
            )
        }

        def tree(root: str, nodes: dict[str, tuple[str, str]]) -> tuple[list[str], int]:
            if root not in nodes:
                return [root], 0
            left, right = nodes[root]
            left_leaves, left_depth = tree(left, nodes)
            right_leaves, right_depth = tree(right, nodes)
            return left_leaves + right_leaves, max(left_depth, right_depth) + 1

        by_class: dict[str, list[decode_ir.FormIR]] = {}
        for form in self.ir.forms:
            by_class.setdefault(form.opcode_class, []).append(form)
        expected_interleaved_nodes: list[str] = []
        for opcode_class in sorted(by_class):
            forms = by_class[opcode_class]
            class_name = generate_decoder._identifier(opcode_class).lower()
            for node_index in range(len(forms) - 1):
                expected_interleaved_nodes.extend(
                    [
                        f"{class_name}_selection_node_{node_index:03d}",
                        f"{class_name}_form_node_{node_index:03d}",
                    ]
                )
            case = re.search(
                rf"{self.names.opcode_class[opcode_class]}: begin\n"
                rf"        class_raw_match = (\w+);\n"
                rf"        class_selection = (\w+);\n"
                rf"        class_form = (\w+);",
                d0,
            )
            self.assertIsNotNone(case, opcode_class)
            assert case is not None
            raw_leaves, raw_depth = tree(case.group(1), raw_nodes)
            selection_leaves, selection_depth = tree(
                case.group(2), selection_nodes
            )
            form_leaves, form_depth = tree(case.group(3), form_nodes)
            expected_raw = [f"form_{form.index:03d}_raw_match" for form in forms]
            expected_form = [
                f"form_{form.index:03d}_onehot_form" for form in forms
            ]
            expected_selection = [
                f"form_{form.index:03d}_selection" for form in forms
            ]
            expected_depth = (len(forms) - 1).bit_length()
            self.assertEqual(raw_leaves, expected_raw)
            self.assertEqual(form_leaves, expected_form)
            self.assertEqual(selection_leaves, expected_selection)
            self.assertEqual(raw_depth, expected_depth)
            self.assertEqual(form_depth, expected_depth)
            self.assertEqual(selection_depth, expected_depth)
            self.assertIn(
                f"// {opcode_class}: {len(forms)} parallel form leaves, "
                f"{expected_depth} balanced form-OR/EA-priority levels",
                d0,
            )
        form_bits = generate_decoder._width(len(self.ir.forms) + 1)
        declaration_order = re.findall(
            rf"^  (?:d0_selection_t|logic \[{form_bits - 1}:0\]) "
            r"(\w+_(?:selection|form)_node_\d+);$",
            d0,
            re.MULTILINE,
        )
        assignment_order = re.findall(
            r"^  assign (\w+_(?:selection|form)_node_\d+) =",
            d0,
            re.MULTILINE,
        )
        self.assertEqual(declaration_order, expected_interleaved_nodes)
        self.assertEqual(assignment_order, expected_interleaved_nodes)
        self.assertEqual(len(raw_nodes), len(self.ir.forms) - len(by_class))
        self.assertEqual(len(form_nodes), len(self.ir.forms) - len(by_class))
        self.assertEqual(
            len(selection_nodes), len(self.ir.forms) - len(by_class)
        )
        for form in self.ir.forms:
            accepted = f"form_{form.index:03d}_accepted_match"
            form_signal = f"form_{form.index:03d}_onehot_form"
            selection = f"form_{form.index:03d}_selection"
            self.assertIn(
                f"assign {form_signal} = {accepted} ? "
                f"{self.names.form[form.key]} : FORM_INVALID;",
                d0,
            )
            self.assertIn(
                f"assign {selection}.form = FORM_INVALID;",
                d0,
            )
        self.assertIn("result_o.form = form_id_e'(class_form);", d0)

    def test_public_mask_orders_are_live_derived(self) -> None:
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

    def test_operands_gather_directly_and_keep_fixed_payload_values(self) -> None:
        for form in self.ir.forms:
            case = self.form_case_text(form)
            for slot, operand in enumerate(form.operands):
                source = operand.source
                if isinstance(
                    source,
                    (decode_ir.EncodedFieldSourceIR, decode_ir.EffectiveAddressSourceIR),
                ):
                    self.assertIn(
                        f"result_o.operands[{slot}].value = "
                        f"64'({generate_decoder._gather('d0_i.opcode', source.positions)});",
                        case,
                    )
                elif isinstance(source, decode_ir.FixedSourceIR):
                    self.assertIn(
                        f"result_o.operands[{slot}].value = "
                        f"64'h{(source.value or 0):016x};",
                        case,
                    )

    def test_payload_width_codes_and_canonical_ea_assignments_are_complete(self) -> None:
        package = self.outputs[self.build_dir / "bedrock_decode_pkg.sv"]
        widths = tuple(
            sorted(
                {
                    compact.payload_width
                    for compact in self.ir.effective_addresses.compact_forms
                }
            )
        )
        self.assertEqual(widths, (0, 8, 16, 32, 64))
        for code, width in enumerate(widths, 1):
            name = self.names.ea_payload_width[str(width)]
            self.assertIn(f"{name} = 3'd{code}", package)

        def assert_assignments(
            text: str,
            form: decode_ir.EaFormIR,
            raw_signal: str,
        ) -> None:
            static = (
                ("kind", self.names.ea_kind[form.kind]),
                ("segment", self.names.ea_segment[form.segment]),
                ("base", self.names.ea_base[form.base]),
                ("register_name", self.names.ea_register[form.register_name]),
                ("update_target", self.names.update_target[form.update_target]),
                ("update_mode", self.names.update_mode[form.update_mode]),
            )
            for member, value in static:
                self.assertIn(f"parse_one_ea.ea.{member} = {value};", text)
            role_members = {
                "value": "direct_register",
                "base": "base_register",
                "index": "index_register",
                "stride": "stride_register",
                "segment": "segment_register",
            }
            for field in form.fields:
                member = role_members[field.role]
                gathered = generate_decoder._gather(raw_signal, field.positions)
                self.assertIn(
                    f"parse_one_ea.ea.{member}_valid = 1'b1;", text
                )
                self.assertIn(
                    f"parse_one_ea.ea.{member} = 4'({gathered});", text
                )

        compact_by_name = {
            compact.name: compact
            for compact in self.ir.effective_addresses.compact_forms
        }
        for entry in self.ir.effective_addresses.compact_entries:
            case = self.compact_case_text(entry.raw)
            if not entry.valid:
                self.assertNotIn("parse_one_ea.ea.payload_width =", case)
                continue
            compact = compact_by_name[entry.form_name]
            self.assertIn(
                "parse_one_ea.ea.payload_width = "
                f"{self.names.ea_payload_width[str(compact.payload_width)]};",
                case,
            )
            self.assertIn(
                f"parse_one_ea.ea.payload_signed = 1'b{int(compact.payload_signed)};",
                case,
            )
            assert_assignments(case, compact, "compact_raw")

        for family in self.ir.effective_addresses.descriptor_families:
            profile, compact = next(
                (profile, item)
                for profile in self.ir.effective_addresses.profiles
                for item in profile.compact_forms
                if item.referenced_descriptor_family == family.name
            )
            case = self.compact_case_text(compact.value, profile.name)
            for descriptor in family.forms:
                assert_assignments(case, descriptor, "descriptor")

    def test_compact_ea_contains_no_direct_register_forms(self) -> None:
        self.assertFalse(
            any(
                compact.kind == "register"
                for compact in self.ir.effective_addresses.compact_forms
            )
        )
        for compact in self.ir.effective_addresses.compact_forms:
            if compact.referenced_descriptor_family:
                continue
            stage, decoded, _ = generate_decoder.reference_ea(
                self.ir,
                "ea",
                compact.value,
                [0] * self.ir.limits.max_record_bytes,
                self.ir.limits.max_record_bytes,
                0,
            )
            self.assertEqual(stage, "success")
            self.assertIsNotNone(decoded)
            self.assertEqual(decoded["register_name"], "")
            self.assertFalse(decoded["direct_register_valid"])
            self.assertEqual(decoded["direct_register"], 0)

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
                    else [0x5B]
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

    def test_vcmp_domain_matrix_at_d0_reference_boundary(self) -> None:
        by_class: dict[str, list[decode_ir.FormIR]] = {}
        for form in self.ir.forms:
            if form.mnemonic == "VCMPcc":
                by_class.setdefault(form.opcode_class, []).append(form)
        self.assertEqual(set(by_class), {"extralong", "xxlong"})

        integer_conditions = {2, 3, 4, 5, 10, 11, 12, 13, 14, 15}
        floating_conditions = {2, 3, 8, 9, 12, 13, 14, 15}
        for opcode_class, forms in by_class.items():
            self.assertEqual(len(forms), 2)
            base = forms[0]
            positions = {field.symbol: field.positions for field in base.fields}
            for size in range(8):
                for condition in range(16):
                    opcode = _set_gather(base.opcode_value, positions["x"], size)
                    opcode = _set_gather(opcode, positions["c"], condition)
                    stage, form_index = generate_decoder.reference_d0(
                        self.ir, True, opcode_class, opcode
                    )
                    legal = (
                        size < 4 and condition in integer_conditions
                    ) or (
                        size > 4 and condition in floating_conditions
                    )
                    with self.subTest(
                        opcode_class=opcode_class,
                        size=size,
                        condition=condition,
                    ):
                        if legal:
                            self.assertEqual(stage, "success")
                            self.assertIn(form_index, {form.index for form in forms})
                        else:
                            self.assertEqual(stage, "constraint_rejected")
                            self.assertIsNone(form_index)

    def test_complete_compact_and_descriptor_lowering(self) -> None:
        entries = self.ir.effective_addresses.compact_entries
        self.assertEqual(tuple(item.raw for item in entries), tuple(range(128)))
        self.assertEqual(
            [item.raw for item in entries if not item.valid], list(range(0x69, 0x80))
        )
        d1 = self.outputs[self.build_dir / "bedrock_decode_d1.sv"]
        d0 = self.outputs[self.build_dir / "bedrock_decode_d0.sv"]
        ea_decoder = self.outputs[self.build_dir / "bedrock_decode_ea.sv"]
        for entry in entries:
            self.assertIn(f"7'h{entry.raw:02x}: begin", d1)
            self.assertIn(f"7'h{entry.raw:02x}: begin", d0)
            self.assertIn(
                f"{{{self.names.ea_profile['ea']}, 7'h{entry.raw:02x}}}: begin",
                ea_decoder,
            )
            span_case = self.span_case_text(entry.raw)
            self.assertEqual(self.d0_span_case_text(entry.raw), span_case)
            if entry.valid:
                compact = next(
                    item
                    for item in self.ir.effective_addresses.compact_forms
                    if item.name == entry.form_name
                )
                expected_span = compact.descriptor_bytes + compact.payload_width // 8
                self.assertIn("encoded_ea_span.valid = 1'b1;", span_case)
                self.assertIn(
                    f"encoded_ea_span.encoded_bytes = 4'd{expected_span};",
                    span_case,
                )
            else:
                self.assertNotIn("encoded_ea_span.valid = 1'b1;", span_case)
        for family in self.ir.effective_addresses.descriptor_families:
            self.assertIn(f"cursor + {family.descriptor_bytes}", ea_decoder)
            selector = (
                f"unique casez (descriptor[{family.descriptor_bytes * 8 - 1}:0])"
            )
            expected_selectors = sum(
                entry.valid
                and entry.descriptor_bytes == family.descriptor_bytes
                and bool(entry.descriptor_family)
                for profile in self.ir.effective_addresses.profiles
                for entry in profile.compact_entries
            )
            self.assertEqual(ea_decoder.count(selector), expected_selectors)
            for index, first in enumerate(family.forms):
                self.assertIn(
                    f"{generate_decoder._casez(family.descriptor_bytes * 8, first.value, first.mask)}: begin // {first.name}",
                    ea_decoder,
                )
                for second in family.forms[index + 1 :]:
                    self.assertNotEqual(
                        (first.value ^ second.value) & first.mask & second.mask,
                        0,
                        (family.name, first.name, second.name),
                    )
            for form in family.forms:
                self.assertIn(f"// {form.name}", ea_decoder)
        self.assertNotIn("if (!descriptor_match &&", ea_decoder)
        self.assertIn(
            "descriptor = {record[(cursor * 8) +: 8], record[((cursor + 1) * 8) +: 8]};",
            ea_decoder,
        )
        self.assertIn(
            "payload[0 +: 8] = record[((cursor + 0) * 8) +: 8]",
            ea_decoder,
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
                self.ir, "ea", entry.raw, record, 18, cursor
            )
            with self.subTest(compact=entry.raw):
                self.assertEqual(stage, "success" if entry.valid else "ea_descriptor")
                self.assertEqual(decoded is not None, entry.valid)
                if decoded is not None:
                    compact = next(
                        form
                        for form in self.ir.effective_addresses.compact_forms
                        if form.name == entry.form_name
                    )
                    expected_form = (
                        families[entry.descriptor_family].forms[0]
                        if entry.descriptor_family
                        else compact
                    )
                    expected_raw = (
                        families[entry.descriptor_family].forms[0].value
                        if entry.descriptor_family
                        else entry.raw
                    )
                    for member, expected in _canonical_ea(
                        expected_form, expected_raw
                    ).items():
                        self.assertEqual(decoded[member], expected, member)
                    self.assertEqual(decoded["payload_width"], compact.payload_width)
                    self.assertEqual(decoded["payload_signed"], compact.payload_signed)
        for family in families.values():
            profile, compact = next(
                (profile, form)
                for profile in self.ir.effective_addresses.profiles
                for form in profile.compact_forms
                if form.referenced_descriptor_family == family.name
                and form.payload_width == 0
            )
            for descriptor_form in family.forms:
                record = [0] * 18
                for byte in range(family.descriptor_bytes):
                    shift = (family.descriptor_bytes - byte - 1) * 8
                    record[cursor + byte] = (descriptor_form.value >> shift) & 0xFF
                stage, decoded, next_cursor = generate_decoder.reference_ea(
                    self.ir, profile.name, compact.value, record, 18, cursor
                )
                with self.subTest(family=family.name, descriptor=descriptor_form.name):
                    self.assertEqual(stage, "success")
                    for member, expected in _canonical_ea(
                        descriptor_form, descriptor_form.value
                    ).items():
                        self.assertEqual(decoded[member], expected, member)
                    self.assertEqual(next_cursor, cursor + family.descriptor_bytes)
        observed_signedness = set()
        for payload_width in (0, 8, 16, 32, 64):
            payload_compact = next(
                form
                for form in self.ir.effective_addresses.compact_forms
                if form.payload_width == payload_width
                and not form.referenced_descriptor_family
            )
            payload_bytes = payload_width // 8
            record = [0] * 18
            record[cursor : cursor + payload_bytes] = range(1, payload_bytes + 1)
            stage, decoded, _ = generate_decoder.reference_ea(
                self.ir, "ea", payload_compact.value, record, 18, cursor
            )
            with self.subTest(payload_width=payload_width):
                self.assertEqual(stage, "success")
                self.assertEqual(
                    decoded["payload"],
                    sum(
                        byte << (offset * 8)
                        for offset, byte in enumerate(range(1, payload_bytes + 1))
                    ),
                )
                self.assertEqual(decoded["payload_width"], payload_width)
                self.assertEqual(
                    decoded["payload_signed"], payload_compact.payload_signed
                )
            observed_signedness.add(payload_compact.payload_signed)
        observed_signedness.update(
            compact.payload_signed
            for compact in self.ir.effective_addresses.compact_forms
        )
        self.assertEqual(observed_signedness, {False, True})
        ext2 = next(
            form
            for form in self.ir.effective_addresses.compact_forms
            if form.referenced_descriptor_family == "ext2"
        )
        self.assertEqual(
            generate_decoder.reference_ea(
                self.ir, "ea", ext2.value, [0] * 18, cursor + 1, cursor
            )[0],
            "ea_descriptor",
        )

    def test_invalid_compact_eas_preserve_form_cursor(self) -> None:
        invalid_entries = tuple(
            entry
            for entry in self.ir.effective_addresses.compact_entries
            if not entry.valid
        )
        self.assertEqual(tuple(entry.raw for entry in invalid_entries), tuple(range(0x69, 0x80)))

        d1 = self.outputs[self.build_dir / "bedrock_decode_d1.sv"]
        ea_decoder = self.outputs[self.build_dir / "bedrock_decode_ea.sv"]
        initialization = "\n".join(
            [
                "      parse_one_ea = '0;",
                "      parse_one_ea.stage = D1_STAGE_EA_DESCRIPTOR;",
                "      parse_one_ea.next_cursor = cursor_in;",
            ]
        )
        self.assertEqual(ea_decoder.count(initialization), 1)
        self.assertLess(
            ea_decoder.index(initialization),
            ea_decoder.index("      unique case ({profile, compact_raw})"),
        )

        ea_form = self.forms["medium.abs_x_ea"]
        ea_operand = next(
            operand
            for operand in ea_form.operands
            if isinstance(operand.source, decode_ir.EffectiveAddressSourceIR)
        )
        self.assertEqual(generate_decoder._ea_candidate_slot(ea_form, ea_operand), 0)
        form_cursor = ea_form.opcode_space_bytes
        self.assertIn(
            "result_o.required_bytes = alt_parse.next_cursor;", ea_decoder
        )
        self.assertIn("result_o.stage = alt_parse.stage;", ea_decoder)
        opcode_case = self.form_case_text(ea_form)
        self.assertIn("ea_span = encoded_ea_span", opcode_case)
        self.assertIn("result_o.stage = D1_STAGE_EA_DESCRIPTOR;", opcode_case)

        for entry in invalid_entries:
            opcode = _set_gather(
                generate_decoder.representative_opcode(ea_form),
                ea_operand.source.positions,
                entry.raw,
            )
            ea_stage, decoded_ea, next_cursor = generate_decoder.reference_ea(
                self.ir,
                "ea",
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
                            f"{{{self.names.ea_profile['ea']}, 7'h{entry.raw:02x}}}: begin // EA {entry.invalid_reason}",
                            "        parse_one_ea.stage = D1_STAGE_EA_DESCRIPTOR;",
                            "      end",
                        ]
                    ),
                )

    def test_d1_layout_and_boundary_cases_come_from_live_ir(self) -> None:
        two_ea = self.forms["long.cmp_x_ea_s_ea_d"]
        mixed = self.forms["medium.add_q_imm64_ea_e"]
        self.assertEqual(
            [item.tag for item in two_ea.layout], ["ParseEa", "ParseEa"]
        )
        self.assertEqual(
            [item.tag for item in mixed.layout], ["ParseEa", "ReadPayload"]
        )
        self.assertEqual(mixed.maximum_required_bytes, 21)
        self.assertGreater(mixed.maximum_required_bytes, self.ir.limits.max_record_bytes)
        d1 = self.outputs[self.build_dir / "bedrock_decode_d1.sv"]
        mixed_start = d1.index(f"{self.names.form[mixed.key]}: begin")
        next_form = self.ir.forms[mixed.index + 1]
        mixed_end = d1.index(f"{self.names.form[next_form.key]}: begin", mixed_start)
        mixed_case = d1[mixed_start:mixed_end]
        self.assertLess(
            mixed_case.index("encoded_ea_span"),
            mixed_case.index("D1_STAGE_STANDALONE_PAYLOAD"),
        )
        self.assertNotIn("parse_one_ea", mixed_case)
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

        payload_form = self.forms["medium.fmovcr_x_imm16_fn_d"]
        payload_record = list(payload_form.representative_record or ())
        payload_record[payload_form.opcode_space_bytes : payload_form.opcode_space_bytes + 2] = [
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
        payload_record[payload_form.opcode_space_bytes : payload_form.opcode_space_bytes + 2] = [
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
        standalone_form = self.forms["medium.fmovcr_x_imm16_fn_d"]
        standalone_layout = next(
            layout
            for layout in standalone_form.layout
            if isinstance(layout, decode_ir.ReadPayloadIR)
        )
        standalone_bytes = standalone_layout.width // 8
        standalone_required = standalone_form.opcode_space_bytes + standalone_bytes
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
        descriptor_required = ea_form.opcode_space_bytes + descriptor_family.descriptor_bytes
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
            ea_form.opcode_space_bytes
            + descriptor_family.descriptor_bytes
            + ea_payload_bytes
        )
        payload_record = [0] * self.ir.limits.max_record_bytes
        descriptor_value = descriptor_family.forms[0].value
        for byte in range(descriptor_family.descriptor_bytes):
            shift = (descriptor_family.descriptor_bytes - byte - 1) * 8
            payload_record[ea_form.opcode_space_bytes + byte] = (
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

        ea_decoder = self.outputs[self.build_dir / "bedrock_decode_ea.sv"]
        d0 = self.outputs[self.build_dir / "bedrock_decode_d0.sv"]
        self.assertEqual(ea_decoder.count(" = parse_one_ea("), 2)
        self.assertIn(
            "alt_span = encoded_ea_span(\n"
            "      class_selection.ea_profiles[BEDROCK_EA_ALT_SLOT],\n"
            "      ea_result_o.alt_raw\n"
            "    );\n"
            "    if (alt_span.valid)\n"
            "      ea_result_o.post_alt_cursor =\n"
            "        ea_result_o.base_cursor + {2'b0, alt_span.encoded_bytes};",
            d0,
        )
        self.assertIn(
            "low_cursor = d0_i.base_cursor;\n"
            "    if (d0_i.ea_layout == EA_LAYOUT_ALT_THEN_LOW)\n"
            "      low_cursor = d0_i.post_alt_cursor;",
            ea_decoder,
        )
        self.assertNotIn("low_cursor = alt_parse.next_cursor;", ea_decoder)
        dual_start = ea_decoder.index("EA_LAYOUT_ALT_THEN_LOW: begin")
        dual_end = ea_decoder.index("        endcase", dual_start)
        dual_case = ea_decoder[dual_start:dual_end]
        self.assertLess(dual_case.index("if (!alt_parse.ok)"), dual_case.index("if (!low_parse.ok)"))
        self.assertIn(
            "result_o.required_bytes = alt_parse.next_cursor;", dual_case
        )
        self.assertIn(
            "result_o.required_bytes = low_parse.next_cursor;", dual_case
        )

    def _testbench(self) -> str:
        names = self.names
        lines = [
            "`timescale 1ns/1ps",
            "module tb;",
            "  import bedrock_decode_pkg::*;",
            "  logic valid_i; opcode_class_e opcode_class_i; logic [41:0] opcode_i;",
            "  d0_result_t d0; d0_ea_result_t d0_ea;",
            "  logic direct_valid_i; opcode_class_e direct_opcode_class_i; logic [41:0] direct_opcode_i;",
            "  d0_result_t d0_direct; d0_ea_result_t d0_ea_direct;",
            "  logic [143:0] record_i; logic [4:0] byte_count_i;",
            "  d1_opcode_result_t d1; ea_decode_result_t ea;",
            "  bedrock_decode_d0 u_d0(.valid_i, .opcode_class_i, .opcode_i, .result_o(d0), .ea_result_o(d0_ea));",
            "  bedrock_decode_d0 u_d0_direct(.valid_i(direct_valid_i), .opcode_class_i(direct_opcode_class_i), .opcode_i(direct_opcode_i), .result_o(d0_direct), .ea_result_o(d0_ea_direct));",
            "  bedrock_decode_d1 u_d1(.d0_i(d0_direct), .record_i, .byte_count_i, .result_o(d1));",
            "  bedrock_decode_ea u_ea(.d0_i(d0_ea_direct), .record_i, .byte_count_i, .result_o(ea));",
            "  initial begin",
            "    valid_i = 1'b0; opcode_class_i = OPCODE_CLASS_INVALID; opcode_i = '0;",
            "    direct_valid_i = 1'b0; direct_opcode_class_i = OPCODE_CLASS_INVALID; direct_opcode_i = '0;",
            "    record_i = '0; byte_count_i = '0; #1;",
            "    if (d0.status != D0_INVALID_INPUT) $fatal(1, \"D0 invalid-input state\");",
        ]
        for form in self.ir.forms:
            opcode = generate_decoder.representative_opcode(form)
            lines.extend(
                [
                    f"    valid_i = 1'b1; opcode_class_i = {names.opcode_class[form.opcode_class]}; opcode_i = 42'h{opcode:09x}; #1;",
                    f"    if (d0.status != D0_SUCCESS || d0.form != {names.form[form.key]}) $fatal(1, \"D0 {form.key}\");",
                ]
            )

        ea_form = self.forms["medium.lea_x_ea_rn"]
        ea_operand = next(
            operand
            for operand in ea_form.operands
            if isinstance(operand.source, decode_ir.EffectiveAddressSourceIR)
        )
        ea_candidate = generate_decoder._ea_candidate_slot(ea_form, ea_operand)
        base_opcode = generate_decoder.representative_opcode(ea_form)
        lines.extend(
            [
                "    valid_i = 1'b0;",
                "    direct_valid_i = 1'b1;",
                f"    direct_opcode_class_i = {names.opcode_class[ea_form.opcode_class]};",
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
                    record[ea_form.opcode_space_bytes + byte] = (descriptor >> shift) & 0xFF
            lines.append(
                f"    direct_opcode_i = 42'h{opcode:09x}; record_i = 144'h{_record_value(record):036x}; #1;"
            )
            expected_valid = 1 if entry.valid else 0
            lines.append(
                f"    if (d1.valid != 1'b{expected_valid} || ea.valid != 1'b{expected_valid}) $fatal(1, \"compact EA {entry.raw:02x}\");"
            )

        family_compact = {
            family.name: next(
                form
                for form in self.ir.effective_addresses.compact_forms
                if form.referenced_descriptor_family == family.name
                and form.payload_width == 0
            )
            for family in self.ir.effective_addresses.descriptor_families
            if any(
                form.referenced_descriptor_family == family.name
                for form in self.ir.effective_addresses.compact_forms
            )
        }
        cursor = ea_form.opcode_space_bytes
        for family in self.ir.effective_addresses.descriptor_families:
            if family.name not in family_compact:
                continue
            compact = family_compact[family.name]
            opcode = _set_gather(base_opcode, ea_operand.source.positions, compact.value)
            for descriptor in family.forms:
                record = [0] * 18
                for byte in range(family.descriptor_bytes):
                    shift = (family.descriptor_bytes - byte - 1) * 8
                    record[cursor + byte] = (descriptor.value >> shift) & 0xFF
                expected = _canonical_ea(descriptor, descriptor.value)
                checks = [
                    f"ea.eas[{ea_candidate}].kind != {names.ea_kind[descriptor.kind]}",
                    f"ea.eas[{ea_candidate}].segment != {names.ea_segment[descriptor.segment]}",
                    f"ea.eas[{ea_candidate}].base != {names.ea_base[descriptor.base]}",
                    f"ea.eas[{ea_candidate}].register_name != {names.ea_register[descriptor.register_name]}",
                    f"ea.eas[{ea_candidate}].update_target != {names.update_target[descriptor.update_target]}",
                    f"ea.eas[{ea_candidate}].update_mode != {names.update_mode[descriptor.update_mode]}",
                ]
                for member in (
                    "direct_register",
                    "base_register",
                    "index_register",
                    "stride_register",
                    "segment_register",
                ):
                    valid = int(bool(expected[f"{member}_valid"]))
                    value = int(expected[member])
                    checks.extend(
                        [
                            f"ea.eas[{ea_candidate}].{member}_valid != 1'b{valid}",
                            f"ea.eas[{ea_candidate}].{member} != 4'd{value}",
                        ]
                    )
                lines.extend(
                    [
                        f"    direct_opcode_i = 42'h{opcode:09x}; record_i = 144'h{_record_value(record):036x}; byte_count_i = 5'd18; #1;",
                        "    if (!ea.valid || "
                        + " || ".join(checks)
                        + f") $fatal(1, \"descriptor {family.name}/{descriptor.name}\");",
                    ]
                )

        payload_form = self.forms["medium.fmovcr_x_imm16_fn_d"]
        payload_record = list(payload_form.representative_record or ())
        payload_record[payload_form.opcode_space_bytes : payload_form.opcode_space_bytes + 2] = [0x10, 0x00]
        payload_operand = next(
            index
            for index, operand in enumerate(payload_form.operands)
            if isinstance(operand.source, decode_ir.AppendedPayloadSourceIR)
        )
        lines.extend(
            [
                f"    direct_opcode_class_i = {names.opcode_class[payload_form.opcode_class]};",
                f"    direct_opcode_i = 42'h{generate_decoder.representative_opcode(payload_form):09x};",
                f"    record_i = 144'h{_record_value(payload_record):036x}; byte_count_i = 5'd{len(payload_record)}; #1;",
                f"    if (!d1.valid || d1.operands[{payload_operand}].value != 64'h0000000000000010) $fatal(1, \"standalone LE payload\");",
                f"    byte_count_i = 5'd{payload_form.opcode_space_bytes + 1}; #1;",
                "    if (d1.valid || d1.stage != D1_STAGE_STANDALONE_PAYLOAD) $fatal(1, \"standalone bounds\");",
            ]
        )

        ext2 = family_compact["ext2"]
        ext2_opcode = _set_gather(base_opcode, ea_operand.source.positions, ext2.value)
        dual_form = self.forms["long.movuc_x_ea_s_ea_d"]
        dual_alt_operand = next(
            operand
            for operand in dual_form.operands
            if generate_decoder._ea_candidate_slot(dual_form, operand) == 1
        )
        dual_low_operand = next(
            operand
            for operand in dual_form.operands
            if generate_decoder._ea_candidate_slot(dual_form, operand) == 0
        )
        ext2_payload = next(
            compact
            for compact in self.ir.effective_addresses.compact_forms
            if compact.referenced_descriptor_family == "ext2"
            and compact.payload_width == 8
        )
        dual_opcode = generate_decoder.representative_opcode(dual_form)
        dual_opcode = _set_gather(
            dual_opcode, dual_alt_operand.source.positions, ext2_payload.value
        )
        dual_opcode = _set_gather(dual_opcode, dual_low_operand.source.positions, 1)
        dual_record = [0] * self.ir.limits.max_record_bytes
        dual_descriptor = family_by_name["ext2"].forms[0].value
        for byte in range(family_by_name["ext2"].descriptor_bytes):
            shift = (family_by_name["ext2"].descriptor_bytes - byte - 1) * 8
            dual_record[dual_form.opcode_space_bytes + byte] = (
                dual_descriptor >> shift
            ) & 0xFF
        dual_record[
            dual_form.opcode_space_bytes + family_by_name["ext2"].descriptor_bytes
        ] = 0x5A
        malformed_dual_opcode = generate_decoder.representative_opcode(dual_form)
        malformed_dual_opcode = _set_gather(
            malformed_dual_opcode, dual_alt_operand.source.positions, ext2.value
        )
        malformed_dual_opcode = _set_gather(
            malformed_dual_opcode, dual_low_operand.source.positions, 1
        )
        lines.extend(
            [
                f"    direct_opcode_class_i = {names.opcode_class[ea_form.opcode_class]};",
                f"    direct_opcode_i = 42'h{ext2_opcode:09x}; record_i = '0; byte_count_i = 5'd{cursor + 1}; #1;",
                "    if (ea.valid || ea.stage != D1_STAGE_EA_DESCRIPTOR) $fatal(1, \"descriptor bounds\");",
                f"    direct_opcode_class_i = {names.opcode_class[dual_form.opcode_class]};",
                f"    direct_opcode_i = 42'h{dual_opcode:09x}; record_i = 144'h{_record_value(dual_record):036x}; byte_count_i = 5'd7; #1;",
                "    if (!ea.valid || ea.ea_count != 2'd2 || ea.required_bytes != 6'd7 || !ea.eas[BEDROCK_EA_LOW_SLOT].valid || !ea.eas[BEDROCK_EA_ALT_SLOT].valid || ea.eas[BEDROCK_EA_ALT_SLOT].payload[7:0] != 8'h5a) $fatal(1, \"parallel dual EA\");",
                f"    direct_opcode_i = 42'h{malformed_dual_opcode:09x}; record_i = '0; byte_count_i = 5'd18; #1;",
                f"    if (ea.valid || ea.stage != D1_STAGE_EA_DESCRIPTOR || ea.ea_count != 2'd2 || ea.required_bytes != 6'd{dual_form.opcode_space_bytes} || ea.eas[BEDROCK_EA_LOW_SLOT] != '0) $fatal(1, \"failed ALT normalizes LOW\");",
                "    direct_valid_i = 1'b0; direct_opcode_class_i = OPCODE_CLASS_INVALID; direct_opcode_i = '0; #1;",
                "    if (d1.valid || d1.operation != OP_INVALID || d1.operands != '0 || ea.valid || ea.eas != '0) $fatal(1, \"stale output\");",
                "    $finish;",
                "  end",
                "endmodule",
                "",
            ]
        )
        return "\n".join(lines)

    def _d0_testbench(self) -> str:
        invalid_allocation = OPERATOR_SPACE_PREFIXES[0]
        invalid_prefix = int(
            invalid_allocation.pattern.replace("x", "0").replace("?", "0"), 2
        )
        invalid_lower_bits = (
            ENCODING_CLASSES_BY_NAME[invalid_allocation.encoding_class].allocation_bits
            - OPERATOR_SPACE_PREFIX_BITS
        )
        invalid_opcode = invalid_prefix << invalid_lower_bits
        lines = [
            "`timescale 1ns/1ps",
            "module tb;",
            "  import bedrock_decode_pkg::*;",
            "  logic valid_i; opcode_class_e opcode_class_i; logic [41:0] opcode_i;",
            "  d0_result_t d0; d0_ea_result_t d0_ea;",
            "  bedrock_decode_d0 dut(.valid_i, .opcode_class_i, .opcode_i, .result_o(d0), .ea_result_o(d0_ea));",
            "  initial begin",
            f"    valid_i = 1'b0; opcode_class_i = {self.names.opcode_class[invalid_allocation.encoding_class]}; opcode_i = 42'h{invalid_opcode:011x}; #1;",
            "    if (d0.status != D0_INVALID_INPUT) $fatal(1, \"invalid input\");",
            "    if (d0.operator_space != OPERATOR_SPACE_NONE) $fatal(1, \"invalid operator space expected=NONE actual=%0d\", d0.operator_space);",
            "    if (d0_ea.status != D0_INVALID_INPUT) $fatal(1, \"EA invalid input\");",
        ]
        for encoding_class in ("extrashort", "short", "medium", "long"):
            lines.extend(
                [
                    f"    valid_i = 1'b1; opcode_class_i = {self.names.opcode_class[encoding_class]}; opcode_i = '0; #1;",
                    f"    if (d0.operator_space != OPERATOR_SPACE_NONE) $fatal(1, \"operator space class={encoding_class} expected=NONE actual=%0d\", d0.operator_space);",
                ]
            )
        for encoding_class in ("extralong", "xxlong"):
            architecture_class = ENCODING_CLASSES_BY_NAME[encoding_class]
            lower_bits = architecture_class.allocation_bits - OPERATOR_SPACE_PREFIX_BITS
            lower_values = (0, (1 << lower_bits) - 1)
            for prefix in _class_operator_prefixes(encoding_class):
                prefix_bits = f"{prefix:0{OPERATOR_SPACE_PREFIX_BITS}b}"
                operator_space = operator_space_from_prefix(
                    encoding_class, prefix_bits
                )
                expected = (
                    "OPERATOR_SPACE_NONE"
                    if operator_space is None
                    else f"OPERATOR_SPACE_{generate_decoder._identifier(operator_space)}"
                )
                for lower in lower_values:
                    opcode = (prefix << lower_bits) | lower
                    lines.extend(
                        [
                            f"    valid_i = 1'b1; opcode_class_i = {self.names.opcode_class[encoding_class]}; opcode_i = 42'h{opcode:011x}; #1;",
                            f"    if (d0.operator_space != {expected}) $fatal(1, \"operator space class={encoding_class} prefix={prefix_bits} expected={expected} actual=%0d\", d0.operator_space);",
                        ]
                    )
        for form in self.ir.forms:
            opcode = generate_decoder.representative_opcode(form)
            low_width, alt_width = generate_decoder._ea_candidate_widths(
                form, self.names
            )
            low_profile, alt_profile = generate_decoder._ea_candidate_profiles(
                form, self.names
            )
            low_raw = opcode & 0x7F
            alt_raw = 0
            if form.opcode_class == "medium":
                alt_raw = (((opcode >> 14) & 0x7) << 4) | (opcode & 0xF)
            elif form.opcode_class in ("long", "extralong", "xxlong"):
                alt_raw = (opcode >> 7) & 0x7F
            post_alt_cursor = form.opcode_space_bytes
            alt_profile_name = next(
                (
                    operand.source.profile
                    for operand in generate_decoder._ea_operands(form)
                    if generate_decoder._ea_candidate_slot(form, operand) == 1
                ),
                None,
            )
            if alt_profile_name is not None:
                profile = next(
                    item
                    for item in self.ir.effective_addresses.profiles
                    if item.name == alt_profile_name
                )
                compact_by_name = {
                    compact.name: compact for compact in profile.compact_forms
                }
                entry = profile.compact_entries[alt_raw]
                if entry.valid:
                    compact = compact_by_name[entry.form_name]
                    post_alt_cursor += (
                        compact.descriptor_bytes + compact.payload_width // 8
                    )
            lines.extend(
                [
                    f"    valid_i = 1'b1; opcode_class_i = {self.names.opcode_class[form.opcode_class]}; opcode_i = 42'h{opcode:09x}; #1;",
                    f"    if (d0.status != D0_SUCCESS || d0.form != {self.names.form[form.key]}) $fatal(1, \"{form.key}\");",
                    f"    if (d0.ea_layout != {generate_decoder._ea_layout(form)}) $fatal(1, \"EA layout {form.key}\");",
                    f"    if (d0.ea_widths[BEDROCK_EA_LOW_SLOT] != {low_width}) $fatal(1, \"EA low width {form.key}\");",
                    f"    if (d0.ea_widths[BEDROCK_EA_ALT_SLOT] != {alt_width}) $fatal(1, \"EA alt width {form.key}\");",
                    f"    if (d0.ea_profiles[BEDROCK_EA_LOW_SLOT] != {low_profile}) $fatal(1, \"EA low profile {form.key}\");",
                    f"    if (d0.ea_profiles[BEDROCK_EA_ALT_SLOT] != {alt_profile}) $fatal(1, \"EA alt profile {form.key}\");",
                    f"    if (d0_ea.status != d0.status || d0_ea.ea_layout != d0.ea_layout || d0_ea.ea_widths != d0.ea_widths || d0_ea.ea_profiles != d0.ea_profiles) $fatal(1, \"EA metadata {form.key}\");",
                    f"    if (d0_ea.low_raw != 7'h{low_raw:02x} || d0_ea.alt_raw != 7'h{alt_raw:02x}) $fatal(1, \"EA raw {form.key}\");",
                    f"    if (d0_ea.base_cursor != 6'd{form.opcode_space_bytes} || d0_ea.post_alt_cursor != 6'd{post_alt_cursor}) $fatal(1, \"EA cursor {form.key}\");",
                ]
            )
        lines.extend(["    $finish;", "  end", "endmodule", ""])
        return "\n".join(lines)

    def test_verilator_split_d1_lint_when_explicitly_enabled(self) -> None:
        if os.environ.get("SV_RUN_LARGE_LINT") != "1":
            self.skipTest("large split-D1 lint requires SV_RUN_LARGE_LINT=1")
        verilator = shutil.which("verilator")
        if verilator is None:
            self.skipTest("Verilator is not available")
        package = str(self.build_dir / generate_decoder.OUTPUT_NAMES[0])
        for module, output_index in (
            ("bedrock_decode_d1", 2),
            ("bedrock_decode_ea", 3),
        ):
            subprocess.run(
                [
                    verilator,
                    "--Wno-fatal",
                    "--Wno-WIDTH",
                    "--Wno-UNSIGNED",
                    "--Wno-CMPCONST",
                    "--Wno-CASEOVERLAP",
                    "--lint-only",
                    "--top-module",
                    module,
                    package,
                    str(self.build_dir / generate_decoder.OUTPUT_NAMES[output_index]),
                ],
                check=True,
                cwd=generate_decoder.ROOT,
            )

    def test_verilator_package_widths_and_d0_simulation_when_available(self) -> None:
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
        package, d0 = (
            str(self.build_dir / name)
            for name in generate_decoder.OUTPUT_NAMES[:2]
        )
        subprocess.run(
            common + ["--lint-only", "--top-module", "bedrock_decode_d0", package, d0],
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
