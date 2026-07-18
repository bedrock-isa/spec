#!/usr/bin/env python3
"""Integration tests for strict definitions and safe per-instruction editing."""

from __future__ import annotations

import subprocess
from pathlib import Path
import sys
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from defs_loader import load_extensions, load_instruction_sets  # noqa: E402
from defs_schema import DecodeError, decode_encodings, decode_instruction  # noqa: E402
from encoding_store import allocation_entry_dict, load_encoding_store  # noqa: E402
from gen_alloc_report import analyze_store  # noqa: E402
from gen_docs import (  # noqa: E402
    AllocationEntry,
    IsaModel,
    latex_allocated_instruction_form_block,
    latex_extension_directory_table,
    load_instructions,
)
from validate_defs import validate_defs  # noqa: E402


def write_yaml(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True, width=1000),
        encoding="utf-8",
    )


def make_minimal_defs(root: Path) -> Path:
    defs = root / "defs"
    write_yaml(defs / "extensions.yaml", {"extensions": []})
    write_yaml(
        defs / "operands.yaml",
        {
            "operand_types": {
                "Rn": {
                    "kind": "register",
                    "register_group": "general",
                    "field_width": 2,
                }
            }
        },
    )
    write_yaml(
        defs / "sizes.yaml",
        {
            "size_codes": {"B": {"suffix": ".B", "bytes": 1}},
            "size_kinds": {},
        },
    )
    write_yaml(
        defs / "registers.yaml",
        {"registers": {"general": {"entries": [{"name": "R0", "width": 64}]}}},
    )
    write_yaml(
        defs / "encoding_classes.yaml",
        {
            "classes": [
                {
                    "name": "extrashort",
                    "instruction_bytes": 1,
                    "payload_bits": 7,
                    "namespace": ["???????"],
                }
            ]
        },
    )
    write_yaml(
        defs / "instructions.yaml",
        {"title": "Base", "include": ["instructions/BASE"]},
    )
    write_yaml(
        defs / "instructions" / "BASE" / "instruction.yaml",
        {
            "mnemonic": "BASE",
            "title": "Base Test",
            "summary": "Exercises the base test instruction.",
            "description": "Reads one synthetic register operand for integration testing.",
            "attributes": {
                "class": "test",
                "family": "test",
                "privilege": "unprivileged",
            },
        },
    )
    write_yaml(
        defs / "instructions" / "BASE" / "encodings.yaml",
        {
            "forms": [
                {
                    "id": "extrashort.base.rn",
                    "class": "extrashort",
                    "bits": "00000rr",
                    "syntax": "BASE Rn(r)",
                    "operands": [
                        {"name": "src", "type": "Rn", "access": "read", "field": "r"}
                    ],
                    "sizes": ["B"],
                }
            ]
        },
    )
    return defs


class StrictSchemaTests(unittest.TestCase):
    def test_rejects_legacy_instruction_fields_and_bad_operand_marker(self) -> None:
        path = Path("instruction.yaml")
        base = {
            "mnemonic": "TEST",
            "title": "Test",
            "summary": "Tests one instruction.",
            "description": "Defines one synthetic instruction for strict decoding.",
            "attributes": {"class": "test", "family": "test", "privilege": "unprivileged"},
        }
        for legacy in ("doc", "forms", "flags"):
            with self.subTest(field=legacy), self.assertRaisesRegex(DecodeError, "unknown fields"):
                decode_instruction(path, {**base, legacy: {} if legacy != "forms" else []})

        with self.assertRaisesRegex(DecodeError, "marker must occur in bits"):
            decode_encodings(
                Path("encodings.yaml"),
                {
                    "forms": [
                        {
                            "id": "extrashort.test",
                            "class": "extrashort",
                            "bits": "00000000",
                            "syntax": "TEST Rn(r)",
                            "operands": [
                                {"name": "src", "type": "Rn", "access": "read", "field": "r"}
                            ],
                        }
                    ]
                },
            )

    def test_tree_validation_rejects_unknown_type_and_missing_tex(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            defs = make_minimal_defs(Path(directory))
            encodings_path = defs / "instructions" / "BASE" / "encodings.yaml"
            encodings = yaml.safe_load(encodings_path.read_text(encoding="utf-8"))
            encodings["forms"][0]["operands"][0]["type"] = "UNREGISTERED"
            write_yaml(encodings_path, encodings)
            _summary, errors = validate_defs(defs)
            self.assertTrue(any("unknown operand type UNREGISTERED" in error for error in errors))

            encodings["forms"][0]["operands"][0]["type"] = "Rn"
            write_yaml(encodings_path, encodings)
            instruction_path = defs / "instructions" / "BASE" / "instruction.yaml"
            instruction = yaml.safe_load(instruction_path.read_text(encoding="utf-8"))
            instruction["additional_description"] = "missing.tex"
            write_yaml(instruction_path, instruction)
            _summary, errors = validate_defs(defs)
            self.assertTrue(any("referenced TeX file does not exist" in error for error in errors))


class AllocationEditorTests(unittest.TestCase):
    def run_editor(self, defs: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL_DIR / "alloc_edit.py"), "--defs-root", str(defs), *args],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_dry_run_apply_edit_and_collision_are_safe(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            defs = make_minimal_defs(root)
            target = defs / "instructions" / "BASE" / "encodings.yaml"
            original = target.read_text(encoding="utf-8")
            snippet = root / "form.yaml"
            write_yaml(
                snippet,
                {
                    "id": "extrashort.base.fixed",
                    "class": "extrashort",
                    "bits": "0000100",
                    "syntax": "BASE",
                },
            )

            dry_run = self.run_editor(defs, "add", "BASE", str(snippet))
            self.assertEqual(dry_run.returncode, 0, dry_run.stderr)
            self.assertIn("extrashort.base.fixed", dry_run.stdout)
            self.assertEqual(target.read_text(encoding="utf-8"), original)

            applied = self.run_editor(defs, "add", "BASE", str(snippet), "--apply")
            self.assertEqual(applied.returncode, 0, applied.stderr)
            self.assertEqual(len(yaml.safe_load(target.read_text(encoding="utf-8"))["forms"]), 2)
            self.assertFalse(target.with_name("encodings.yaml.tmp").exists())

            moved = self.run_editor(
                defs, "move", "extrashort.base.fixed", "--bits", "0000101", "--apply"
            )
            self.assertEqual(moved.returncode, 0, moved.stderr)
            after_move = target.read_text(encoding="utf-8")
            self.assertIn("0000101", after_move)

            constraints = root / "constraints.yaml"
            write_yaml(
                constraints,
                [{"field": "r", "allow": ["0x0..0x1"], "reason": "test_reclaim"}],
            )
            edited = self.run_editor(
                defs,
                "edit",
                "extrashort.base.rn",
                "--constraints",
                str(constraints),
                "--apply",
            )
            self.assertEqual(edited.returncode, 0, edited.stderr)
            before_collision = target.read_text(encoding="utf-8")

            collision = self.run_editor(
                defs, "move", "extrashort.base.fixed", "--bits", "0000000", "--apply"
            )
            self.assertEqual(collision.returncode, 2)
            self.assertIn("overlaps", collision.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), before_collision)
            self.assertFalse(target.with_name("encodings.yaml.tmp").exists())


class NoCodeExtensionTests(unittest.TestCase):
    def test_extension_files_join_docs_and_allocation_without_python_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            defs = make_minimal_defs(Path(directory))
            write_yaml(defs / "extensions.yaml", {"extensions": ["toy"]})
            extension_root = defs / "extensions" / "toy"
            write_yaml(
                extension_root / "extension.yaml",
                {
                    "name": "toy",
                    "instructions": "instructions.yaml",
                    "availability": {
                        "cpuid": {"feature": "TOY", "class": 1, "leaf": 0, "index": 1, "bit": 7}
                    },
                },
            )
            write_yaml(
                extension_root / "instructions.yaml",
                {"title": "Toy Extension", "include": ["instructions/TOY"]},
            )
            write_yaml(
                extension_root / "instructions" / "TOY" / "instruction.yaml",
                {
                    "mnemonic": "TOY",
                    "title": "Toy",
                    "summary": "Exercises one extension instruction.",
                    "description": "Defines a file-only extension instruction for integration testing.",
                    "attributes": {
                        "class": "test",
                        "family": "test",
                        "privilege": "unprivileged",
                    },
                },
            )
            write_yaml(
                extension_root / "instructions" / "TOY" / "encodings.yaml",
                {
                    "forms": [
                        {
                            "id": "extrashort.toy",
                            "class": "extrashort",
                            "bits": "1000000",
                            "syntax": "TOY",
                        }
                    ]
                },
            )

            summary, errors = validate_defs(defs)
            self.assertEqual(errors, [])
            self.assertEqual((summary["instructions"], summary["encodings"]), (2, 2))
            extensions = load_extensions(defs)
            availability = extensions["toy"].data["availability"]["cpuid"]
            self.assertEqual(availability, {"feature": "TOY", "class": 1, "leaf": 0, "index": 1, "bit": 7})
            self.assertEqual(
                [item.name for item in load_instruction_sets(defs, extensions)],
                ["base", "toy"],
            )

            store = load_encoding_store(defs)
            classes, entries = analyze_store(defs)
            self.assertEqual(len(store.encodings), 2)
            self.assertEqual(classes[0].allocated_slots, 5)
            self.assertEqual(
                {entry.entry_id for entry in entries},
                {"extrashort.base.rn", "extrashort.toy"},
            )

            located = next(item for item in store.encodings if item.form.id == "extrashort.toy")
            raw = allocation_entry_dict(located)
            allocation = AllocationEntry(
                path=located.path,
                cls="extrashort",
                payload_bits=7,
                entry_id=located.form.id,
                bits=located.form.bits,
                text=located.form.syntax,
                assigned=1,
                skipped=0,
                fields=raw["fields"],
                constraints=raw["constraints"],
                instruction_bytes=1,
            )
            toy = next(item for item in load_instructions(defs) if item.mnemonic == "TOY")
            model = IsaModel(
                defs,
                {"ea": {}, "extensions": {"toy": extensions["toy"].data}},
                [toy],
                [],
                {"TOY": [allocation]},
            )
            rendered = latex_allocated_instruction_form_block(model, toy, allocation)
            self.assertIn(r"\texttt{TOY}", rendered)
            self.assertIn(r"\manualformmetadata{extrashort}{1 byte}", rendered)
            self.assertIn(r"\begin{manualbitdiagram}", rendered)
            cpuid_table = latex_extension_directory_table(model)
            self.assertIn(r"\texttt{TOY}", cpuid_table)
            self.assertIn(r"\texttt{7}", cpuid_table)


if __name__ == "__main__":
    unittest.main()
