import os
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import validate_defs
import artifact_overlay
import defs_loader
import defs_schema
import gen_docs
import site_markdown


class EncodingTransportValidationTests(unittest.TestCase):
    def test_closed_vector_value_destination_transport_pair(self):
        declared = defs_schema.LogicalOperandDefinition(
            id="dst",
            role="destination",
            access="read_write",
            value_domain="vector",
            profiles=("Vn", "VEA"),
        )
        register = defs_schema.EncodingOperand(
            name="dst",
            type="Vn",
            access="read_write",
        )
        effective_address_write = defs_schema.EncodingOperand(
            name="dst",
            type="VEA",
            access="write",
            ea_role="value",
            ea_width="vector",
        )
        effective_address_read_write = replace(
            effective_address_write,
            access="read_write",
        )

        accepted = (
            register,
            effective_address_write,
            effective_address_read_write,
        )
        rejected = (
            replace(register, access="write"),
            replace(register, ea_role="value"),
            replace(effective_address_write, access="read"),
            replace(effective_address_write, ea_role=None),
        )
        for encoded in accepted:
            with self.subTest(expected="accepted", encoded=encoded):
                self.assertTrue(
                    defs_loader._encoding_transport_matches_logical_access(
                        declared, encoded
                    )
                )
        for encoded in rejected:
            with self.subTest(expected="rejected", encoded=encoded):
                self.assertFalse(
                    defs_loader._encoding_transport_matches_logical_access(
                        declared, encoded
                    )
                )

    def test_vector_value_transport_near_misses_use_exact_access_equality(self):
        declared = defs_schema.LogicalOperandDefinition(
            id="dst",
            role="destination",
            access="read_write",
            value_domain="vector",
            profiles=("Vn", "VEA"),
        )
        encoded = defs_schema.EncodingOperand(
            name="dst",
            type="VEA",
            access="write",
            ea_role="value",
            ea_width="vector",
        )
        near_misses = (
            (replace(declared, role="source"), False),
            (replace(declared, access="write"), True),
            (replace(declared, value_domain="integer"), False),
            (replace(declared, profiles=("Vn", "VEA", "Fn")), False),
        )
        for near_miss, expected in near_misses:
            with self.subTest(declared=near_miss, expected=expected):
                self.assertEqual(
                    defs_loader._encoding_transport_matches_logical_access(
                        near_miss, encoded
                    ),
                    expected,
                )


class DescriptionTexValidationTests(unittest.TestCase):
    def test_missing_description_remains_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            repository_root = Path(directory)
            definitions_root = repository_root / "isa" / "instructions" / "definitions"
            details = definitions_root / "instructions" / "MISSING" / "details.tex"

            with patch.object(validate_defs, "ROOT", definitions_root):
                errors = validate_defs.validate_description_tex(details)

            self.assertEqual(errors, [f"{details}: referenced TeX file does not exist"])


class OperationArtifactOverlayTests(unittest.TestCase):
    def test_generated_overlay_artifact_is_accepted_without_source_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            repository_root = Path(directory) / "repository"
            bundle = repository_root / "isa" / "instructions" / "definitions" / "instructions" / "GENERATED"
            bundle.mkdir(parents=True)
            manifest = bundle / "operation.yaml"
            logical_artifact = bundle / "details.tex"
            overlay = Path(directory) / "overlay"
            generated_artifact = overlay / logical_artifact.relative_to(repository_root)
            generated_artifact.parent.mkdir(parents=True)
            generated_artifact.write_text("Generated details.\n", encoding="utf-8")
            reference = defs_schema.OperationArtifactRef("details.tex", "tex")

            with patch.object(defs_loader, "REPOSITORY_ROOT", repository_root), patch.dict(
                os.environ, {artifact_overlay.OVERLAY_ENV: str(overlay)}
            ):
                resolved = defs_loader._artifact_file(bundle, manifest, reference)

            self.assertEqual(resolved, generated_artifact.resolve())
            self.assertFalse(logical_artifact.exists())

    def test_artifact_absent_from_source_and_overlay_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            repository_root = Path(directory) / "repository"
            bundle = repository_root / "isa" / "instructions" / "definitions" / "instructions" / "MISSING"
            bundle.mkdir(parents=True)
            manifest = bundle / "operation.yaml"
            overlay = Path(directory) / "overlay"
            reference = defs_schema.OperationArtifactRef("details.tex", "tex")

            with patch.object(defs_loader, "REPOSITORY_ROOT", repository_root), patch.dict(
                os.environ, {artifact_overlay.OVERLAY_ENV: str(overlay)}
            ):
                with self.assertRaisesRegex(ValueError, "does not exist as a file"):
                    defs_loader._artifact_file(bundle, manifest, reference)

    def test_artifact_escape_is_rejected_before_overlay_resolution(self):
        with tempfile.TemporaryDirectory() as directory:
            repository_root = Path(directory) / "repository"
            bundle = repository_root / "isa" / "instructions" / "definitions" / "instructions" / "ESCAPE"
            bundle.mkdir(parents=True)
            manifest = bundle / "operation.yaml"
            outside = bundle.parent / "outside.tex"
            outside.write_text("Outside bundle.\n", encoding="utf-8")
            reference = defs_schema.OperationArtifactRef("../outside.tex", "tex")

            with patch.object(defs_loader, "REPOSITORY_ROOT", repository_root):
                with self.assertRaisesRegex(ValueError, "resolves outside its operation bundle"):
                    defs_loader._artifact_file(bundle, manifest, reference)

    def test_ordinary_source_artifact_resolution_is_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            repository_root = Path(directory) / "repository"
            bundle = repository_root / "isa" / "instructions" / "definitions" / "instructions" / "SOURCE"
            bundle.mkdir(parents=True)
            manifest = bundle / "operation.yaml"
            source = bundle / "description.tex"
            source.write_text("Source details.\n", encoding="utf-8")
            overlay = Path(directory) / "overlay"
            reference = defs_schema.OperationArtifactRef("description.tex", "tex")

            with patch.object(defs_loader, "REPOSITORY_ROOT", repository_root), patch.dict(
                os.environ, {artifact_overlay.OVERLAY_ENV: str(overlay)}
            ):
                resolved = defs_loader._artifact_file(bundle, manifest, reference)

            self.assertEqual(resolved, source.resolve())


class OperationDocumentCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = gen_docs.load_model(gen_docs.DEF_ROOT)
        cls.instructions = {
            instruction.mnemonic: instruction
            for instruction in cls.model.instructions
        }

    def test_semantic_condition_registry_owns_reader_text(self):
        path = gen_docs.DEF_ROOT / "semantic_conditions.yaml"
        decoded = defs_schema.decode_semantic_condition_registry(
            path, defs_loader.load_yaml(path)
        )
        decoded_projection = {
            item.id: item.reader_text for item in decoded.conditions
        }
        self.assertTrue(decoded_projection)
        self.assertEqual(
            defs_loader.load_semantic_conditions(gen_docs.DEF_ROOT),
            decoded_projection,
        )
        referenced_conditions = {
            event.condition
            for instruction in self.model.instructions
            if instruction.operation is not None
            for case in instruction.operation.cases
            for event in case.events
        }
        self.assertTrue(referenced_conditions)
        self.assertLessEqual(referenced_conditions, decoded_projection.keys())
        for instruction in self.model.instructions:
            operation = instruction.operation
            if operation is None:
                continue
            rendered = gen_docs.latex_instruction_entry(self.model, instruction)
            for case in operation.cases:
                for event in case.events:
                    self.assertNotIn(event.condition, rendered)
                    self.assertIn(decoded_projection[event.condition], rendered)
                    public_event = event.event
                    if event.cause is not None:
                        public_event += "." + event.cause
                    self.assertIn(gen_docs.tex_code(public_event), rendered)

    def test_cpuid_registry_owns_identity_location_and_inherited_conjunction(self):
        root = gen_docs.DEF_ROOT
        flags = defs_loader.load_cpuid_flags(root)
        extensions = defs_loader.load_extensions(root)
        known, requirements = defs_loader.extension_cpuid_requirements(
            extensions, flags
        )
        self.assertEqual(known, frozenset(flags))
        self.assertEqual(requirements["base"], ())
        self.assertEqual(
            requirements["fpu.transcendental_approx"], ("FP", "FPTRANSA")
        )
        locations = {
            (
                flag.location.selector_class,
                flag.location.leaf,
                flag.location.index,
                flag.location.bit,
            )
            for flag in flags.values()
        }
        self.assertEqual(len(locations), len(flags))
        duplicated = dict(extensions)
        nested = extensions["fpu.transcendental_approx"]
        nested_data = __import__("copy").deepcopy(nested.data)
        nested_data["availability"]["required_cpuid_flags"].append("FP")
        duplicated[nested.name] = replace(nested, data=nested_data)
        with self.assertRaisesRegex(
            ValueError, "duplicates an inherited requirement"
        ):
            defs_loader.extension_cpuid_requirements(duplicated, flags)
        unknown = dict(extensions)
        vector = extensions["vector"]
        vector_data = __import__("copy").deepcopy(vector.data)
        vector_data["availability"]["required_cpuid_flags"] = ["UNKNOWN"]
        unknown[vector.name] = replace(vector, data=vector_data)
        with self.assertRaisesRegex(ValueError, "unknown required CPUID flag"):
            defs_loader.extension_cpuid_requirements(unknown, flags)

        raw = defs_loader.load_yaml(root / "cpuid_flags.yaml")
        for label, mutate, diagnostic in (
            (
                "duplicate token",
                lambda value: value["cpuid_flags"][1].update(
                    token=value["cpuid_flags"][0]["token"]
                ),
                "duplicate value",
            ),
            (
                "duplicate location",
                lambda value: value["cpuid_flags"][1].update(
                    location=dict(value["cpuid_flags"][0]["location"])
                ),
                "duplicate value",
            ),
            (
                "malformed bit",
                lambda value: value["cpuid_flags"][0]["location"].update(bit=64),
                "expected 0..63",
            ),
        ):
            candidate = __import__("copy").deepcopy(raw)
            mutate(candidate)
            with self.subTest(label=label), self.assertRaisesRegex(
                defs_schema.DecodeError, diagnostic
            ):
                defs_schema.decode_cpuid_flag_registry(
                    root / "cpuid_flags.yaml", candidate
                )

    def test_cpuid_directory_uses_public_flags_without_reverse_index(self):
        directory = gen_docs.latex_extension_directory_table(self.model)
        self.assertNotIn("fpu.transcendental_approx", directory)
        self.assertNotIn("Extension &", directory)
        reference_indexes = gen_docs.latex_reference_navigation_section()
        self.assertNotIn("CPUID Feature Index", reference_indexes)
        self.assertNotIn("Available instructions", reference_indexes)

    def test_destination_overlap_conditions_reuse_encoding_relations(self):
        for instruction in self.model.instructions:
            operation = instruction.operation
            if operation is None:
                continue
            bundle_root = Path(operation.artifacts.bundle_root)
            encodings_path = bundle_root / "encodings.yaml"
            encodings = defs_schema.decode_encodings(
                encodings_path, defs_loader.load_yaml(encodings_path)
            )
            forms_by_id = {form.id: form for form in encodings.forms}
            for case in operation.cases:
                if not any(
                    event.condition == "destination_overlap"
                    for event in case.events
                ):
                    continue
                for form_id in case.applies_to.forms:
                    self.assertTrue(
                        any(
                            relation.rule == "illegal_instruction"
                            for relation in forms_by_id[form_id].destination_overlap
                        ),
                        (instruction.mnemonic, case.id, form_id),
                    )

    def test_flag_effect_registry_owns_typed_reader_text(self):
        path = gen_docs.DEF_ROOT / "flag_effect_definitions.yaml"
        decoded = defs_schema.decode_flag_effect_definition_registry(
            path, defs_loader.load_yaml(path)
        )
        decoded_projection = {item.id: item for item in decoded.definitions}
        self.assertTrue(decoded_projection)
        self.assertEqual(
            defs_loader.load_flag_effect_definitions(gen_docs.DEF_ROOT),
            decoded_projection,
        )
        for instruction in self.model.instructions:
            if instruction.operation is None:
                continue
            for case in instruction.operation.cases:
                for bank in case.flags or ():
                    for effect in bank.effects:
                        if effect.reference is None:
                            continue
                        definition = decoded_projection[effect.reference]
                        self.assertEqual(
                            definition.kind,
                            defs_schema.FLAG_EFFECT_REFERENCE_KIND[effect.effect],
                            (instruction.mnemonic, case.id, bank.bank, effect.flag),
                        )

    def test_named_value_registry_owns_predicate_observations(self):
        path = gen_docs.DEF_ROOT / "named_values.yaml"
        decoded = defs_schema.decode_named_value_registry(
            path, defs_loader.load_yaml(path)
        )
        decoded_projection = {item.id: item for item in decoded.values}
        self.assertTrue(decoded_projection)
        self.assertEqual(
            defs_loader.load_named_values(gen_docs.DEF_ROOT),
            decoded_projection,
        )
        referenced_values = {
            case.predicate.observed
            for instruction in self.model.instructions
            if instruction.operation is not None
            for case in instruction.operation.cases
            if case.predicate.observed is not None
        }
        self.assertTrue(referenced_values)
        self.assertLessEqual(referenced_values, decoded_projection.keys())

    def test_document_candidates_project_titles_and_summaries(self):
        expected = {
            "ADD": ("Add", "Adds the source operand to the destination operand."),
            "FADD": (
                "Floating-Point Add",
                "Adds the source operand to the destination operand.",
            ),
            "VADD": (
                "Vector Add",
                "Adds corresponding active vector elements using integer or floating-point arithmetic.",
            ),
        }
        for mnemonic, (title, summary) in expected.items():
            with self.subTest(mnemonic=mnemonic):
                instruction = self.instructions[mnemonic]
                self.assertIsNotNone(instruction.operation)
                self.assertEqual(instruction.doc["title"], title)
                self.assertEqual(instruction.doc["summary"], summary)
        self.assertTrue(all(
            instruction.path.name == "operation.yaml"
            for instruction in self.model.instructions
            if instruction.operation is not None
        ))

    def test_candidate_entries_use_typed_presentation(self):
        add = gen_docs.latex_instruction_entry(
            self.model, self.instructions["ADD"]
        )
        fadd = gen_docs.latex_instruction_entry(
            self.model, self.instructions["FADD"]
        )
        vadd = gen_docs.latex_instruction_entry(
            self.model, self.instructions["VADD"]
        )
        rendered_by_mnemonic = {"ADD": add, "FADD": fadd, "VADD": vadd}
        for mnemonic, rendered in rendered_by_mnemonic.items():
            self.assertNotIn("\\manualinstructionfield{Attributes}", rendered)
            self.assertNotIn("Class =", rendered)
            self.assertNotIn("Family =", rendered)
            self.assertNotIn("Length =", rendered)
            self.assertNotIn("Feature =", rendered)
            instruction = self.instructions[mnemonic]
            detail = gen_docs.operation_description_tex(instruction.operation)
            self.assertIn(
                "\\manualoperationfield{Operation}{"
                + gen_docs.latex_escape(instruction.operation.summary)
                + "}",
                rendered,
            )
            self.assertNotIn(
                f"\\manualoperationfield{{Operation}}{{{detail}}}",
                rendered,
            )
            semantics_heading = rendered.index(
                "\\manualinstructiondescriptionheading{Detailed Semantics}"
            )
            self.assertGreater(rendered.index(detail), semantics_heading)
            self.assertEqual(rendered.count(detail), 1)
            summary_table = gen_docs.latex_instruction_summary_table(
                "Candidate", [instruction]
            )
            self.assertIn(instruction.doc["summary"], summary_table)
        self.assertNotIn("Required CPUID flags", add)
        self.assertIn("Repeat eligibility", add)
        self.assertIn("Required CPUID flags", fadd)
        self.assertIn("\\texttt{FP}", fadd)
        self.assertNotIn("Effect &", fadd)
        self.assertIn("\\texttt{NV} & \\texttt{DZ}", fadd)
        self.assertIn("* & - & * & * & *", fadd)
        self.assertIn("\\texttt{*}: accrual of an operation-generated cause.", fadd)
        self.assertIn("\\texttt{-}: preserved.", fadd)
        self.assertIn(
            "when a generated floating-point exception is enabled", fadd
        )
        self.assertNotIn("enabled_floating_point_exception", fadd)
        self.assertNotIn("Repeat eligibility", vadd)
        self.assertIn("H/S/D cases: \\texttt{FP}", vadd)

    def test_site_normalizes_candidate_fields_at_the_reader_boundary(self):
        rendered = gen_docs.latex_instruction_entry(
            self.model, self.instructions["FADD"]
        )
        self.assertIn("\\manualoperationfield{Required CPUID flags}", rendered)
        normalized = site_markdown._normalize_reader_macros(rendered)
        self.assertNotIn("\\manualoperationfield", normalized)
        self.assertIn("\\subsection*{Required CPUID flags}", normalized)
        self.assertIn("\\subsection*{Repeat eligibility}", normalized)
        self.assertIn("\\subsection*{Exceptions}", normalized)

    def test_site_preserves_public_metasyntax_alternatives_in_code(self):
        normalized = site_markdown.normalize_latex_for_site(
            r"\texttt{VADD.\{B\textbar{}W\textbar{}L\textbar{}Q\}}"
        )
        self.assertEqual(normalized, r"\texttt{VADD.\{B|W|L|Q\}}")

    def test_candidate_flag_tables_have_stable_markers_and_local_legends(self):
        fixed_markers = {
            "preserve": "-",
            "clear": "0",
            "set": "1",
        }
        for instruction in self.model.instructions:
            operation = instruction.operation
            if operation is None:
                continue
            cases = [case for case in operation.cases if case.flags]
            if not cases:
                continue
            rendered = gen_docs.latex_instruction_entry(self.model, instruction)
            cursor = 0
            for case in cases:
                formats = gen_docs._operation_case_formats(case)
                case_label = (
                    gen_docs.latex_escape(f"{formats} elements") + r"\par"
                    if formats
                    else None
                )
                for bank_index, bank in enumerate(case.flags):
                    with self.subTest(
                        mnemonic=instruction.mnemonic,
                        case=case.id,
                        bank=bank.bank,
                    ):
                        header = f"\\textbf{{{bank.bank} Effects}}\\par"
                        has_case_label = case_label is not None and bank_index == 0
                        label_start = (
                            rendered.find(case_label, cursor)
                            if has_case_label
                            else -1
                        )
                        start = rendered.find(
                            header,
                            label_start + len(case_label)
                            if has_case_label
                            else cursor,
                        )
                        self.assertGreaterEqual(start, 0)
                        next_header = rendered.find("\\textbf{", start + len(header))
                        end = len(rendered) if next_header < 0 else next_header
                        table = rendered[start:end]
                        nontrivial = tuple(dict.fromkeys(
                            (effect.effect, effect.reference)
                            for effect in bank.effects
                            if effect.effect not in fixed_markers
                        ))
                        assigned = {
                            key: "*" if len(nontrivial) == 1 else chr(ord("a") + index)
                            for index, key in enumerate(nontrivial)
                        }
                        markers = [
                            fixed_markers[effect.effect]
                            if effect.effect in fixed_markers
                            else assigned[(effect.effect, effect.reference)]
                            for effect in bank.effects
                        ]
                        expected_needspace = gen_docs._latex_flag_effect_needspace(
                            len(tuple(dict.fromkeys(markers))),
                            has_case_label=has_case_label,
                        )
                        boundary = start
                        if has_case_label:
                            self.assertGreaterEqual(label_start, 0)
                            self.assertEqual(
                                rendered[label_start + len(case_label) : start],
                                "\n",
                            )
                            boundary = label_start
                        self.assertTrue(
                            rendered[:boundary].endswith(expected_needspace + "\n"),
                            (
                                instruction.mnemonic,
                                case.id,
                                bank.bank,
                                expected_needspace,
                            ),
                        )
                        self.assertIn(" & ".join(markers) + r"\\", table)
                        self.assertNotIn("Effect &", table)
                        for marker in dict.fromkeys(markers):
                            self.assertIn(gen_docs.tex_code(marker) + ": ", table)
                        cursor = start + len(header)


if __name__ == "__main__":
    unittest.main()
