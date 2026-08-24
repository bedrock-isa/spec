#!/usr/bin/env python3
"""Direct checks for generated Sail metadata and representative records."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest import mock


TOOLS_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_ROOT))

import generate_catalog
import build_docs


class CatalogGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_directory = tempfile.TemporaryDirectory(prefix="bedrock-sail-generated-")
        cls.addClassCleanup(cls.temporary_directory.cleanup)
        cls.build_dir = Path(cls.temporary_directory.name)
        generate_catalog.write_outputs(cls.build_dir)
        cls.store, cls.operand_types, cls.ea_registry, cls.documents = generate_catalog._load_inputs()
        cls.ir = generate_catalog.decode_ir.load_decode_ir()

    def test_every_mnemonic_has_a_generated_route(self) -> None:
        self.assertEqual(
            {document.execution_route for document in self.documents.values()},
            set(generate_catalog.ROUTE_CONSTRUCTORS),
        )
        self.assertEqual(
            {item.mnemonic for item in self.store.encodings},
            set(self.documents),
        )

    def test_build_outputs_round_trip_and_are_current(self) -> None:
        outputs = generate_catalog.render_outputs(self.build_dir)
        self.assertEqual(
            {path.relative_to(self.build_dir).as_posix() for path in outputs},
            {
                "generated/operations.sail",
                "generated/local_operations.sail",
                "generated/catalog.sail",
                "bedrock-generated.sail_project",
            },
        )
        for path, expected in outputs.items():
            self.assertEqual(path.read_text(encoding="utf-8"), expected, path.name)
        self.assertTrue(generate_catalog.check_outputs(self.build_dir))

    def test_representative_records_cover_every_form(self) -> None:
        for item in self.store.encodings:
            form_id = item.form.id
            record = generate_catalog._representative_record(item, self.operand_types)
            self.assertGreaterEqual(len(record), 1, form_id)
            self.assertLessEqual(len(record), 18, form_id)
            if record[0] & 0xC0 == 0xC0:
                self.assertEqual(3 + ((record[0] >> 2) & 0xF), len(record), form_id)

    def test_full_metadata_inputs_are_schema_decoded(self) -> None:
        self.assertTrue(all(item.form.id.startswith(item.form.encoding_class + ".") for item in self.store.encodings))
        self.assertGreater(len(self.ea_registry.compact_forms), 0)
        self.assertGreater(len(self.ea_registry.ext1_forms), 0)
        self.assertGreater(len(self.ea_registry.ext2_forms), 0)
        self.assertEqual(self.ea_registry.compact_field_width, 7)

    def test_registry_and_every_form_availability_rule_reach_typed_sail_catalog(
        self,
    ) -> None:
        operations = (
            self.build_dir / "generated" / "operations.sail"
        ).read_text(encoding="utf-8")
        catalog = (
            self.build_dir / "generated" / "catalog.sail"
        ).read_text(encoding="utf-8")
        for flag in self.ir.cpuid_flags:
            with self.subTest(flag=flag.id):
                self.assertIn(f"CpuidFlag_{flag.id}", operations)
                self.assertIn(
                    f"CpuidFlag_{flag.id} => {json.dumps(flag.token)}",
                    operations,
                )
        records = {
            match.group(1): line
            for line in catalog.splitlines()
            if "availability_rules =" in line
            and (match := re.search(r'form_id = "([^"]+)"', line))
        }
        self.assertEqual(set(records), {form.key for form in self.ir.forms})
        for form in self.ir.forms:
            record = records[form.key]
            with self.subTest(form=form.key):
                for rule in form.availability_rules:
                    self.assertIn(f'case_id = {json.dumps(rule.case_id)}', record)
                    for flag in rule.required_cpuid_flags:
                        self.assertIn(f"CpuidFlag_{flag}", record)
                    for selector in rule.selectors:
                        self.assertIn(
                            f"field_symbol = {json.dumps(selector.field_symbol)}",
                            record,
                        )
                        for value in selector.encoded_values:
                            self.assertIn(str(value), record)

    def test_selected_primary_bytes_and_endpoints(self) -> None:
        forms = {item.form.id: item.form.bits for item in self.store.encodings}
        self.assertEqual(forms["extrashort.clr_q_rn_r"], "111rrrr")
        self.assertEqual(forms["short.mov_x_rn_s_rn_d"], "00000zssssdddd")
        self.assertEqual(forms["short.and_x_rn_s_rn_d"], "00100zssssdddd")
        self.assertEqual(forms["short.or_x_rn_s_rn_d"], "00101zssssdddd")
        self.assertEqual(forms["short.xor_x_rn_s_rn_d"], "00110zssssdddd")

    def test_operation_entry_boundary_precedes_generated_dependents(self) -> None:
        core_types = (generate_catalog.ROOT / "isa" / "execution" / "core" / "types.sail")
        project = (generate_catalog.ROOT / "isa" / "bedrock.sail_project")
        self.assertIn(
            "val execute_operation_entry : (Decoded_instruction, Cpu_state) -> Execution_result",
            core_types.read_text(encoding="utf-8"),
        )
        self.assertIn("requires prelude, operations, catalog_types, catalog, decode, fp, core", generate_catalog.render_overlay_project())
        self.assertIn("core, operation_entries", project.read_text(encoding="utf-8"))

class DocumentationBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        store, operand_types, ea_registry, documents = generate_catalog._load_inputs()
        rendered_operations = generate_catalog.render_operations(documents)
        rendered_catalog = generate_catalog.render_catalog(
            store, operand_types, ea_registry, documents
        )
        rendered_entries = generate_catalog.render_operation_entries(documents)
        operation_type = re.search(
            r"enum Semantic_operation =.*?(?=\n\nfunction semantic_route)",
            rendered_operations,
            re.DOTALL,
        )
        if operation_type is None:
            raise AssertionError("generated operation enum not found")
        functions = {
            "semantic_route": {
                "function": {
                    "source": rendered_operations,
                    "path": ["operations"],
                },
                "path": ["operations"],
            },
            "primary_form_catalog": {
                "function": {
                    "source": rendered_catalog,
                    "path": ["catalog"],
                },
                "path": ["catalog"],
            },
        }
        declarations = list(re.finditer(
            r"(?m)^function\s+([A-Za-z_][A-Za-z0-9_]*)\b", rendered_entries,
        ))
        for index, declaration in enumerate(declarations):
            end = declarations[index + 1].start() if index + 1 < len(declarations) else len(rendered_entries)
            functions[declaration.group(1)] = {
                "function": {
                    "source": rendered_entries[declaration.start():end],
                    "path": ["operation_entries"],
                },
                "path": ["operation_entries"],
            }
        for group in sorted(build_docs.OWNER_MODULES):
            for source_path in build_docs.OWNER_SOURCE_PATHS[group]:
                text = source_path.read_text(encoding="utf-8")
                declarations = list(re.finditer(
                    r"(?m)^function\s+([A-Za-z_][A-Za-z0-9_]*)\b",
                    text,
                ))
                for index, declaration in enumerate(declarations):
                    end = declarations[index + 1].start() if index + 1 < len(declarations) else len(text)
                    name = declaration.group(1)
                    source = text[declaration.start():end]
                    existing = functions.get(name)
                    if existing is not None:
                        source = existing["function"]["source"] + "\n" + source
                    functions[name] = {
                        "function": {"source": source, "path": [group]},
                        "path": [group],
                    }
        cls.doc_bundle = {
            "types": {"Semantic_operation": {"type": operation_type.group(0)}},
            "functions": functions,
        }

    def test_build_directory_safety(self) -> None:
        self.assertEqual(
            generate_catalog.validate_build_dir(build_docs.ROOT / "build" / "sail-doc"),
            (build_docs.ROOT / "build" / "sail-doc").resolve(),
        )
        with tempfile.TemporaryDirectory(prefix="bedrock-sail-doc-safe-") as temporary:
            external = Path(temporary) / "artifact"
            self.assertEqual(generate_catalog.validate_build_dir(external), external.resolve())
        for source_root in (
            build_docs.ROOT,
            build_docs.SAIL_SOURCE_ROOT,
            build_docs.SAIL_PROJECT,
            build_docs.SAIL_SOURCE_ROOT / "README.md",
            build_docs.ROOT / "isa" / "tools" / "sail",
        ):
            with self.subTest(source_root=source_root):
                with self.assertRaises(ValueError):
                    generate_catalog.validate_build_dir(source_root)

    def test_semantic_index_is_complete_and_stable(self) -> None:
        first = build_docs.render_semantic_index(self.doc_bundle)
        second = build_docs.render_semantic_index(self.doc_bundle)
        self.assertEqual(first, second)
        index = json.loads(first)
        store, _, _, documents = generate_catalog._load_inputs()
        self.assertEqual(
            {item["mnemonic"] for item in index["operations"]},
            set(documents),
        )
        self.assertEqual(
            {item["form_id"] for item in index["forms"]},
            {item.form.id for item in store.encodings},
        )
        self.assertTrue(all(item["route"] for item in index["operations"]))
        operations = {item["mnemonic"]: item for item in index["operations"]}
        expected_entries = {
            document.public_instruction.mnemonic: [
                f"operation_entries.{entry}"
                for entry in dict.fromkeys(case.sail_entry for case in document.cases)
            ]
            for document in documents.values()
        }
        self.assertEqual(
            {mnemonic: item["direct_functions"] for mnemonic, item in operations.items()},
            expected_entries,
        )
        self.assertEqual(operations["NOP"]["direct_functions"], ["operation_entries.execute_NOP"])
        self.assertEqual(operations["ILLEGAL"]["direct_functions"], ["operation_entries.execute_ILLEGAL"])
        setcc = operations["SETcc"]
        self.assertEqual(setcc["ownership"], "direct")
        self.assertEqual(setcc["direct_functions"], ["operation_entries.execute_SETcc"])
        self.assertEqual(operations["BNDUXX"]["direct_functions"], ["operation_entries.execute_BNDUXX"])
        self.assertEqual(operations["FETCHXOR"]["direct_functions"], ["operation_entries.execute_FETCHXOR"])
        self.assertEqual(operations["LEA"]["direct_functions"], ["operation_entries.execute_LEA"])
        self.assertTrue(all(
            "." in owner
            for item in index["operations"]
            for owner in item["direct_functions"] + item["route_owner_functions"]
        ))
        self.assertTrue(all(
            item["direct_functions"] or item["route_owner_functions"]
            for item in index["operations"]
        ))

    def test_operation_entry_derivation_fails_closed(self) -> None:
        broken = json.loads(json.dumps(self.doc_bundle))
        broken["functions"].pop("execute_FETCHXOR")
        with self.assertRaises(ValueError):
            build_docs.build_semantic_index(broken)

    def test_mocked_build_is_confined_and_repeatable(self) -> None:
        semantic_source_roots = tuple(
            build_docs.SAIL_SOURCE_ROOT / topic
            for topic in (
                "foundations",
                "encoding",
                "addressing",
                "execution",
                "memory",
                "system",
                "instructions",
            )
        )
        source_roots = semantic_source_roots + (
            build_docs.SAIL_SOURCE_ROOT / "tests",
            build_docs.ROOT / "isa" / "tools" / "sail",
        )
        exact_source_paths = (
            build_docs.SAIL_PROJECT,
            build_docs.SAIL_SOURCE_ROOT / "README.md",
        )
        def source_snapshot() -> dict[Path, bytes]:
            snapshot = {
                path.relative_to(build_docs.ROOT): path.read_bytes()
                for source_root in source_roots
                for path in source_root.rglob("*")
                if path.is_file()
            }
            snapshot.update({
                path.relative_to(build_docs.ROOT): path.read_bytes()
                for path in exact_source_paths
            })
            return snapshot

        before = source_snapshot()

        def fake_sail(command, *, cwd, check):
            self.assertTrue(check)
            self.assertEqual(Path(cwd), build_docs.SAIL_SOURCE_ROOT)
            self.assertIn("--require-version", command)
            self.assertIn("0.20.2", command)
            self.assertIn("--no-memo-z3", command)
            self.assertIn("--all-modules", command)
            self.assertIn("--doc-compact", command)
            output_dir = Path(command[command.index("-o") + 1])
            output = output_dir / "bedrock-sail.json"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(self.doc_bundle, sort_keys=True), encoding="utf-8")
            return None

        with tempfile.TemporaryDirectory(prefix="bedrock-sail-doc-build-") as temporary:
            build_dir = Path(temporary) / "artifact"
            with mock.patch.object(build_docs.subprocess, "run", side_effect=fake_sail):
                bundle, semantic_index = build_docs.build_docs(build_dir)
                first_index = semantic_index.read_bytes()
                first_bundle = bundle.read_bytes()
                build_docs.build_docs(build_dir)
            self.assertEqual(semantic_index.read_bytes(), first_index)
            self.assertEqual(bundle.read_bytes(), first_bundle)
            self.assertFalse((build_dir / "sail_doc").exists())

        after = source_snapshot()
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
