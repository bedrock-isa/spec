#!/usr/bin/env python3
"""Regression tests for the frozen versioned YAML schema contract."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import is_dataclass
from pathlib import Path
import sys
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from defs_schema import (  # noqa: E402
    DecodeError,
    decode_abi_vectors,
    decode_condition_registry,
    decode_ea_registry,
    decode_encodings,
    decode_extension_catalog,
    decode_extension_manifest,
    decode_instruction,
    decode_instruction_index,
    decode_memory_validation,
    decode_operand_registry,
    decode_register_registry,
    decode_size_registry,
    decode_yaml,
    verify_schema_lock,
)
from validate_schema import validate_schema  # noqa: E402


def load(path: Path) -> object:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class FrozenSchemaTests(unittest.TestCase):
    def test_version_lock_and_all_documents(self) -> None:
        verify_schema_lock()
        paths = list((ROOT / "isa" / "defs").rglob("*.yaml"))
        paths.extend(
            (
                ROOT / "isa" / "abi" / "plt_golden_vectors.yaml",
                ROOT / "isa" / "memory_model" / "validation.yaml",
            )
        )
        for path in paths:
            with self.subTest(path=path):
                self.assertTrue(is_dataclass(decode_yaml(path)))
        count, errors = validate_schema(ROOT)
        self.assertEqual(count, len(paths))
        self.assertEqual(errors, [])

    def test_lock_rejects_unreviewed_decoder_or_contract_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            lock = Path(directory) / "schema.lock"
            locked = (ROOT / "isa" / "defs" / "schema.lock").read_text(encoding="utf-8")
            for field, message in (
                ("decoder_sha256", "decoder changed"),
                ("contract_sha256", "displayed contract changed"),
            ):
                candidate = "\n".join(
                    field + "=" + "0" * 64 if line.startswith(field + "=") else line
                    for line in locked.splitlines()
                )
                lock.write_text(candidate + "\n", encoding="utf-8")
                with self.subTest(field=field), self.assertRaisesRegex(DecodeError, message):
                    verify_schema_lock(lock)

    def test_every_document_family_rejects_unknown_root_fields(self) -> None:
        defs = ROOT / "isa" / "defs"
        cases = (
            (decode_instruction, defs / "instructions" / "ADD" / "instruction.yaml"),
            (decode_encodings, defs / "instructions" / "ADD" / "encodings.yaml"),
            (decode_instruction_index, defs / "instructions.yaml"),
            (decode_extension_catalog, defs / "extensions.yaml"),
            (decode_extension_manifest, defs / "extensions" / "fpu" / "extension.yaml"),
            (decode_operand_registry, defs / "operands.yaml"),
            (decode_size_registry, defs / "sizes.yaml"),
            (decode_register_registry, defs / "registers.yaml"),
            (decode_condition_registry, defs / "conditions.yaml"),
            (decode_ea_registry, defs / "ea.yaml"),
            (decode_abi_vectors, ROOT / "isa" / "abi" / "plt_golden_vectors.yaml"),
            (decode_memory_validation, ROOT / "isa" / "memory_model" / "validation.yaml"),
        )
        for decoder, path in cases:
            raw = load(path)
            self.assertIsInstance(raw, dict)
            candidate = deepcopy(raw)
            candidate["unknown_schema_field"] = True
            with self.subTest(path=path), self.assertRaisesRegex(DecodeError, "unknown fields"):
                decoder(path, candidate)

    def test_nested_types_and_discriminants_are_frozen(self) -> None:
        defs = ROOT / "isa" / "defs"
        mutations = []

        operands = load(defs / "operands.yaml")
        operands["operand_types"]["Rn"]["signed"] = False
        mutations.append((decode_operand_registry, defs / "operands.yaml", operands, "not valid"))

        sizes = load(defs / "sizes.yaml")
        sizes["size_codes"]["B"]["bytes"] = True
        mutations.append((decode_size_registry, defs / "sizes.yaml", sizes, "expected integer"))

        registers = load(defs / "registers.yaml")
        registers["registers"]["general"]["entries"][0]["width"] = "64"
        mutations.append((decode_register_registry, defs / "registers.yaml", registers, "expected integer"))

        conditions = load(defs / "conditions.yaml")
        conditions["conditions"][0]["aliases"] = "ALL"
        mutations.append((decode_condition_registry, defs / "conditions.yaml", conditions, "expected list"))

        ea = load(defs / "ea.yaml")
        ea["compact"]["forms"][0]["fields"]["r"]["role"] = 1
        mutations.append((decode_ea_registry, defs / "ea.yaml", ea, "expected non-empty string"))

        extension = load(defs / "extensions" / "fpu" / "extension.yaml")
        extension["availability"]["cpuid"]["bit"] = 64
        mutations.append((decode_extension_manifest, defs / "extensions" / "fpu" / "extension.yaml", extension, "expected 0..63"))

        abi_path = ROOT / "isa" / "abi" / "plt_golden_vectors.yaml"
        abi = load(abi_path)
        abi["ordinary_plt"]["instruction"]["opcode_bytes"][0] = 256
        mutations.append((decode_abi_vectors, abi_path, abi, "byte out of range"))

        memory_path = ROOT / "isa" / "memory_model" / "validation.yaml"
        memory = load(memory_path)
        memory["target"]["afence_is_full_cumulative"] = "true"
        mutations.append((decode_memory_validation, memory_path, memory, "expected boolean"))

        for decoder, path, candidate, message in mutations:
            with self.subTest(path=path), self.assertRaisesRegex(DecodeError, message):
                decoder(path, candidate)

    def test_instruction_flag_effects_reject_unknown_or_empty_entries(self) -> None:
        path = ROOT / "isa" / "defs" / "instructions" / "CMP" / "instruction.yaml"
        base = load(path)
        cases = []

        unknown_bank = deepcopy(base)
        unknown_bank["flag_effects"]["STATUS"] = {"Z": "set"}
        cases.append((unknown_bank, "unknown flag banks STATUS"))

        unknown_flag = deepcopy(base)
        unknown_flag["flag_effects"]["FLAGS"]["NX"] = "set"
        cases.append((unknown_flag, "unknown flags NX"))

        empty_effect = deepcopy(base)
        empty_effect["flag_effects"]["FLAGS"]["Z"] = ""
        cases.append((empty_effect, "expected non-empty string"))

        for candidate, message in cases:
            with self.subTest(message=message), self.assertRaisesRegex(DecodeError, message):
                decode_instruction(path, candidate)

    def test_ea_operands_require_consistent_role_and_width(self) -> None:
        path = ROOT / "isa" / "defs" / "instructions" / "ADD" / "encodings.yaml"
        base = load(path)
        ea_form = next(
            form
            for form in base["forms"]
            if any(operand.get("type") == "EA" for operand in form.get("operands", []))
        )
        ea_index = next(
            index
            for index, operand in enumerate(ea_form["operands"])
            if operand.get("type") == "EA"
        )

        missing = deepcopy(base)
        candidate = next(
            form for form in missing["forms"] if form["id"] == ea_form["id"]
        )
        candidate["operands"][ea_index].pop("ea_width")
        with self.assertRaisesRegex(DecodeError, "require ea_role and ea_width"):
            decode_encodings(path, missing)

        wrong_role = deepcopy(base)
        candidate = next(
            form for form in wrong_role["forms"] if form["id"] == ea_form["id"]
        )
        candidate["operands"][ea_index]["ea_role"] = "address"
        with self.assertRaisesRegex(DecodeError, "address role requires address access"):
            decode_encodings(path, wrong_role)

        wrong_control_target = deepcopy(base)
        candidate = next(
            form for form in wrong_control_target["forms"] if form["id"] == ea_form["id"]
        )
        candidate["operands"][ea_index]["ea_role"] = "control_target"
        with self.assertRaisesRegex(DecodeError, "control_target role requires read access"):
            decode_encodings(path, wrong_control_target)

        nonsized = deepcopy(base)
        candidate = next(
            form for form in nonsized["forms"] if form["id"] == ea_form["id"]
        )
        candidate["sizes"] = []
        with self.assertRaisesRegex(DecodeError, "operation_size requires"):
            decode_encodings(path, nonsized)


if __name__ == "__main__":
    unittest.main()
