#!/usr/bin/env python3
"""Regression tests for the ISA reference's semantic visual components."""

from __future__ import annotations

from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from gen_docs import load_model, render_latex  # noqa: E402


TEMPLATES = ROOT / "isa" / "tools" / "latex_builder" / "templates"
INPUT_RE = re.compile(r"\\input\{([^}]+)\}")


def expand_inputs(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        path = ROOT / match.group(1)
        return expand_inputs(path.read_text(encoding="utf-8"))

    return INPUT_RE.sub(replace, text)


class VisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_model(ROOT / "isa" / "defs", ROOT / "isa" / "alloc")
        cls.rendered = render_latex(cls.model)
        cls.expanded = expand_inputs(cls.rendered)

    def test_instruction_descriptions_use_the_new_field_contract(self) -> None:
        described = sum(bool(inst.doc.get("description")) for inst in self.model.instructions)
        self.assertEqual(self.rendered.count(r"\begin{manualinstruction}"), 206)
        self.assertEqual(self.rendered.count(r"\manualinstructionfield{Summary}"), 0)
        self.assertEqual(self.rendered.count(r"\manualinstructionfield{Description}"), described)
        self.assertEqual(described, 206)
        self.assertEqual(self.rendered.count(r"\manualinstructionfield{Operation}"), 0)
        self.assertEqual(self.rendered.count(r"\manualinstructionfield{Assembler Syntax}"), 206)
        self.assertEqual(self.rendered.count(r"\manualinstructionfield{Attributes}"), 206)
        self.assertEqual(
            self.rendered.count(r"\manualinstructiondescriptionheading{Detailed Semantics}"),
            60,
        )
        self.assertNotIn(r"\manualinstructionmetadata{", self.rendered)
        self.assertEqual(self.rendered.count(r"\manualformmetadata{"), 403)
        self.assertNotRegex(self.rendered, r"\\begin\{tabularx\}.*p\{0\.88in\}")

    def test_ea_profiles_and_code_examples_are_not_tables(self) -> None:
        ea_source = "\n".join(
            (TEMPLATES / "fragments" / name).read_text(encoding="utf-8")
            for name in ("compact_ea_reference_blocks.tex", "ext0_reference_blocks.tex")
        )
        self.assertEqual(ea_source.count(r"\begin{manualeaprofile}"), 14)
        self.assertNotRegex(ea_source, r"\\begin\{(?:tabular|tabularx)\}")
        for syntax in re.findall(r"\\manualeaprofilesyntax\{([^}]*(?:\}\{[^}]*)*)\}", ea_source):
            with self.subTest(syntax=syntax):
                self.assertNotIn(", ", syntax)

        for name in (
            "memcpy_example.tex",
            "memmove_example.tex",
            "memset_example.tex",
            "memcmp_example.tex",
            "bulk_extension_example.tex",
        ):
            source = (TEMPLATES / "fragments" / name).read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assertIn(r"\begin{manualcode}", source)
                self.assertNotRegex(source, r"\\begin\{(?:tabular|tabularx)\}")

    def test_removed_tables_are_absent_and_survivors_are_all_listed(self) -> None:
        removed = (
            "Instruction Set Summary",
            "CPUID Instruction",
            "SAVE/RESTORE Instructions",
            "Fence Instructions",
            "Supervisor Control-Flow Instructions",
            "Architectural Event Processing Instructions",
            "Instruction Header Fields",
            "Instruction Families",
            "EXT0 Encoding",
        )
        for title in removed:
            self.assertNotIn(rf"\manualtablecaption{{{title}}}", self.expanded)
        formal_tables = self.expanded.count(r"\manualtablecaption{") + self.expanded.count(
            r"\begin{manuallistedstructlayout}"
        )
        self.assertEqual(formal_tables, 55)
        self.assertNotIn(r"\section{Instruction Set Summary}", self.expanded)
        document_body = self.expanded.split(r"\begin{document}", 1)[1]
        listed_visuals = re.findall(r"\\begin\{(manuallisted[^}]+)\}", document_body)
        formal_figures = document_body.count(r"\manualfigurecaption{") + sum(
            environment != "manuallistedstructlayout" for environment in listed_visuals
        )
        self.assertEqual(formal_figures, 26)
        removed_caption_macro = "manual" + "unlistedtablecaption"
        self.assertNotIn(removed_caption_macro, self.expanded)
        common = (ROOT / "isa" / "tex" / "bedrock-reference-common.tex").read_text(encoding="utf-8")
        self.assertNotIn(removed_caption_macro, common)

    def test_group_summary_tables_have_brief_descriptions_but_no_global_duplicate_index(self) -> None:
        for title in (
            "General Instructions Summary",
            "Virtualization Acceleration Instructions Summary",
            "Floating-Point Instructions Summary",
            "Approximate Floating-Point Transcendental Instructions Summary",
        ):
            self.assertIn(rf"\manualtablecaption{{{title}}}", self.rendered)
        self.assertEqual(self.rendered.count(r"\manualsummarymnemonic{"), 206)
        self.assertEqual(self.rendered.count(r"\textbf{Mnemonic} & \textbf{Brief description}"), 8)
        self.assertNotIn(r"\begin{manualmnemonicindex}", self.rendered)
        self.assertNotIn(r"\textbf{Summary} & \textbf{Forms}", self.rendered)

    def test_fptransa_accuracy_contracts_are_discoverable_and_rendered(self) -> None:
        self.assertIn(r"\manualtablecaption{FPTRANSA Accuracy Result}", self.rendered)
        self.assertIn(r"\manualtablecaption{FPTRANSA Accuracy Contracts}", self.rendered)
        self.assertEqual(self.rendered.count(r"\manualinstructionfield{Approximation Contract}"), 19)
        self.assertIn(r"\texttt{0x0000000100010000}", self.rendered)
        self.assertIn(r"\texttt{0x0000000100010042}", self.rendered)
        self.assertIn(r"\texttt{0x8000000102000180}", self.rendered)
        self.assertIn(r"\hyperref[instr:fsincosa]{\texttt{FSINCOSA}}", self.rendered)
        approx_sources = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "isa" / "defs" / "extensions" / "fpu_transcendental_approx").rglob("*.yaml")
        )
        self.assertNotIn("unbounded precision", approx_sources)
        self.assertNotIn("using FSTATUS.RM", approx_sources)

    def test_diagram_and_condition_code_semantics_are_preserved(self) -> None:
        self.assertEqual(self.rendered.count(r"\begin{manualbitdiagram}"), 403)
        self.assertEqual(self.rendered.count(r"\begin{manualstatusstrip}"), 20)
        self.assertEqual(self.rendered.count(r"Format \textemdash{} Instruction format"), 403)
        self.assertRegex(
            self.rendered,
            r"(?s)\\textbf\{\\texttt\{RDSEG CS, Rn\(d\)\}\}.*?"
            r"\\manualformmetadata\{long\}\{4 bytes\}\{unprivileged\}",
        )

    def test_every_longtable_has_first_and_continued_headers(self) -> None:
        longtables = len(re.findall(r"\\begin\{manual(?:dense)?longtable\}", self.expanded))
        self.assertGreater(longtables, 0)
        self.assertEqual(self.expanded.count(r"\endfirsthead"), longtables)
        self.assertEqual(self.expanded.count(r"(continued)"), longtables)

    def test_save_context_is_a_compact_layout_not_a_row_per_register_table(self) -> None:
        source = (TEMPLATES / "fragments" / "save_area_diagram.tex").read_text(encoding="utf-8")
        common = (ROOT / "isa" / "tex" / "bedrock-reference-common.tex").read_text(encoding="utf-8")
        self.assertIn(r"\begin{manuallistedstructlayout}", source)
        self.assertIn(r"\manualstructextensionfield{8}", source)
        self.assertIn(r"\NewDocumentEnvironment{manuallistedstructlayout}", common)
        self.assertIn(r"\newcommand{\manualstructrow}", common)
        self.assertIn(r"\newcommand{\manualstructslotfield}", common)
        self.assertNotIn(r"\begin{tikzpicture}", source)
        self.assertNotIn(r"\path[manualLayout", source)
        self.assertNotIn(r"\node[", source)
        self.assertNotIn(r"\begin{manualdenselongtable}", source)
        self.assertNotIn(r"\texttt{R15} &", source)
        self.assertIn(r"\manualformatfield{GSV}{6}", source)
        self.assertIn(r"\manualstructoptionalseries{GS}{0}{6}", source)
        self.assertNotIn(r"\texttt{0x0b8}", source)

    def test_frame_control_uses_true_bit_widths_and_ext0_raw_matrix_is_removed(self) -> None:
        frame = (TEMPLATES / "fragments" / "frame_control_diagram.tex").read_text(encoding="utf-8")
        ext0 = (TEMPLATES / "ext0_addressing_modes.tex").read_text(encoding="utf-8")
        self.assertIn(r"\begin{manuallistedformatdiagram}{FRAME\_CONTROL Format}{1}", frame)
        self.assertNotIn("@EXT0_TABLE@", ext0)
        self.assertNotIn("table:ext0-encoding", self.expanded)

    def test_table_header_fill_is_joined_to_rules_by_environment_spacing(self) -> None:
        common = (ROOT / "isa" / "tex" / "bedrock-reference-common.tex").read_text(encoding="utf-8")
        self.assertGreaterEqual(common.count(r"\setlength{\aboverulesep}{0pt}"), 3)
        self.assertGreaterEqual(common.count(r"\setlength{\belowrulesep}{0pt}"), 3)
        self.assertIn(r"\mbox{\texttt{#1}}", common)


if __name__ == "__main__":
    unittest.main()
