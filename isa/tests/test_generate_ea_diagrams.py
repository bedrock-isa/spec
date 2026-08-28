import tempfile
import unittest
from pathlib import Path

from engine.ea_mode import EAMode
from engine.generate_ea_diagrams import (
    _EAFlowLayout,
    _mode_context,
    _title_case,
    catalog_mode_paths,
    main,
    render_autoupdate_diagrams,
    render_encoding_diagram,
    render_flow_diagram,
    render_modes,
    render_mode,
)
from engine.reference import Reference


class GenerateEADiagramsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1]

    def load(self, relative: str) -> EAMode:
        return EAMode.load(self.isa_root / relative, self.isa_root)

    def test_compact_encoding_groups_fixed_and_variable_bits(self) -> None:
        rendered = render_encoding_diagram(
            self.load("ea/modes/compact/register/mode.yaml")
        )

        self.assertIn(r"\BedrockFormatFixed{000}{3}", rendered)
        self.assertIn(r"\BedrockFormatFieldCode{r}{4}", rendered)
        self.assertIn(r"\BedrockFormatRow{DISP8S}", rendered)

    def test_mixed_fixed_bits_stay_in_one_visual_field(self) -> None:
        rendered = render_encoding_diagram(
            self.load("ea/modes/EXT1/explicit_segment_zero_base/mode.yaml")
        )

        self.assertIn(r"\BedrockFormatFixed{0011}{4}", rendered)

    def test_indexed_mode_uses_computed_flow_layout(self) -> None:
        rendered = render_flow_diagram(
            self.load("ea/modes/EXT2/explicit_segment_index/mode.yaml")
        )

        self.assertIsNotNone(rendered)
        self.assertIn(r"\BedrockEAFlowStart", rendered)
        source_x = _EAFlowLayout._number(_EAFlowLayout._lane_x("source"))
        word_width = _EAFlowLayout._number(_EAFlowLayout.WORD_WIDTH)
        self.assertIn(
            rf"\BedrockEAFlowLabeledBox{{DISPLACEMENT}}{{disp}}{{0.18}}"
            rf"{{{source_x}}}{{{word_width}}}",
            rendered,
        )
        self.assertIn(
            rf"\BedrockEAFlowLabeledBox{{INDEX REGISTER}}{{idx}}{{-0.54}}"
            rf"{{{source_x}}}{{{word_width}}}",
            rendered,
        )

    def test_immediate_flow_is_described_as_operand_generation(self) -> None:
        rendered = render_flow_diagram(
            self.load("ea/modes/compact/immediate/mode.yaml")
        )

        self.assertIsNotNone(rendered)
        self.assertIn("Integer Immediate Operand Generation", rendered)

    def test_index_autoupdate_variants_are_integrated_into_address_flows(self) -> None:
        diagrams = render_autoupdate_diagrams(
            self.load("ea/modes/EXT2/explicit_segment_index/mode.yaml")
        )

        self.assertEqual(len(diagrams), 2)
        self.assertTrue(diagrams[0].startswith(r"\clearpage"))
        self.assertIn("Postincrement Address Generation", diagrams[0])
        self.assertIn("Predecrement Address Generation", diagrams[1])
        self.assertIn("{INDEX UPDATE}{update}", diagrams[0])
        self.assertIn("{1}{0}%", diagrams[0])
        self.assertIn("updateopfeedbackout", diagrams[0])

    def test_scale_based_base_autoupdate_is_preserved(self) -> None:
        diagrams = render_autoupdate_diagrams(
            self.load("ea/modes/EXT1/default_segment_base/mode.yaml")
        )

        self.assertEqual(len(diagrams), 2)
        self.assertIn("{Rn(b)}{1}%", diagrams[0])
        self.assertIn("{scale}{0}%", diagrams[0])
        self.assertIn("{displacement}{1}%", diagrams[0])
        self.assertIn("{updateop}{4.62}{0.18}{$-$}", diagrams[1])

    def test_generated_mode_keeps_manual_explanation_block_format(self) -> None:
        rendered = render_mode(
            self.load("ea/modes/EXT2/explicit_segment_base/mode.yaml")
        )

        self.assertEqual(rendered.count(r"\begin{BedrockEAProfile}"), 2)
        self.assertIn(
            r"\BedrockEAProfileSyntax{[SEG(s):Rn(b)++ + displacement]}",
            rendered,
        )
        self.assertIn(
            r"\BedrockEAProfileSyntax{[SEG(s):{-}{-}Rn(b) + displacement]}",
            rendered,
        )
        self.assertIn(r"\BedrockEAProfileLine{Descriptor}", rendered)
        self.assertIn(r"\BedrockEAProfileLine{Generation}", rendered)
        self.assertIn(r"\BedrockEAProfileLine{Segment}", rendered)
        self.assertIn(r"\BedrockEAProfileLine{Payload}", rendered)
        self.assertIn(r"\BedrockEAProfileLine{Update}", rendered)
        self.assertIn("Postincrement uses the current temporary base register", rendered)
        self.assertIn(r"Predecrement subtracts \texttt{scale}", rendered)
        postincrement, predecrement = rendered.split(
            r"\BedrockEAProfileTitle{EXT2 Explicit-Segment Base with Autoupdate / Predecrement}"
        )
        self.assertIn("Rn(b)++", postincrement)
        self.assertNotIn(r"{-}{-}Rn(b)", postincrement)
        self.assertIn("base postincrement", postincrement)
        self.assertNotIn("base predecrement", postincrement)
        self.assertIn(r"{-}{-}Rn(b)", predecrement)
        self.assertNotIn("Rn(b)++", predecrement)
        self.assertIn("base predecrement", predecrement)
        self.assertNotIn("base postincrement", predecrement)
        self.assertNotIn("/ postincrement / postincrement", rendered)
        self.assertNotIn("/ predecrement / predecrement", rendered)
        self.assertNotIn(r"\BedrockInstructionLead", rendered)
        self.assertEqual(rendered.count(r"\clearpage"), 1)
        self.assertLess(
            rendered.index("Postincrement Address Generation"),
            rendered.index(r"\clearpage"),
        )
        self.assertGreater(
            rendered.index("Predecrement Address Generation"),
            rendered.index(r"\clearpage"),
        )

    def test_ea_style_uses_heading_title_and_plain_flow_caption(self) -> None:
        style_root = self.isa_root.parent / "style" / "bedrock-reference"
        instruction = (style_root / "instruction.sty").read_text(encoding="utf-8")
        flow = (style_root / "ea-flow.sty").read_text(encoding="utf-8")

        title_definition = instruction.split(
            r"\newcommand{\BedrockEAProfileTitle}", 1
        )[1].split(r"\newcommand", 1)[0]
        self.assertIn(r"\large\bfseries", title_definition)
        self.assertNotIn(r"\texttt", title_definition)
        self.assertIn(r"\BedrockCaption{\BedrockEAFlowCaption}", flow)
        self.assertNotIn(r"\BedrockSchemaCaption{\BedrockEAFlowCaption}", flow)

    def test_plain_and_autoupdate_encodings_get_independent_blocks(self) -> None:
        rendered = render_mode(
            self.load("ea/modes/EXT2/explicit_segment_index/mode.yaml")
        )

        self.assertEqual(rendered.count(r"\begin{BedrockEAProfile}"), 3)
        self.assertIn("/ Plain}", rendered)
        self.assertIn("/ Postincrement}", rendered)
        self.assertIn("/ Predecrement}", rendered)

    def test_title_case_is_shared_and_preserves_architecture_tokens(self) -> None:
        self.assertEqual(
            _title_case("compact integer immediate"), "Compact Integer Immediate"
        )
        self.assertEqual(
            _title_case("FP FEA compact floating-point immediate"),
            "FP FEA Compact Floating-Point Immediate",
        )
        self.assertEqual(
            _title_case("EXT2 explicit-segment base with autoupdate"),
            "EXT2 Explicit-Segment Base with Autoupdate",
        )

    def test_mode_heading_context_uses_logical_reference(self) -> None:
        self.assertEqual(
            _mode_context(Reference("base", ("ea", "compact"), "immediate")),
            "compact",
        )
        self.assertEqual(
            _mode_context(Reference("FP", ("fea", "compact"), "immediate")),
            "FP FEA compact",
        )

    def test_non_autoupdate_mode_says_no_update(self) -> None:
        rendered = render_mode(
            self.load("ea/modes/EXT1/explicit_segment_base/mode.yaml")
        )

        self.assertIn(r"\BedrockEAProfileLine{Update}{No auto-update.}", rendered)

    def test_layout_geometry_is_derived_from_shared_grid_rules(self) -> None:
        self.assertEqual(
            _EAFlowLayout._lane_x("source"),
            _EAFlowLayout.MAIN_X
            - _EAFlowLayout.OP_RADIUS
            - _EAFlowLayout.OP_GAP
            - _EAFlowLayout.WORD_WIDTH / 2,
        )
        self.assertEqual(
            _EAFlowLayout._lane_x("side", "aux"),
            _EAFlowLayout._lane_x("secondary")
            - _EAFlowLayout.OP_RADIUS
            - _EAFlowLayout.OP_GAP
            - _EAFlowLayout.AUX_WIDTH / 2,
        )
        self.assertEqual(
            _EAFlowLayout._row_y(3),
            _EAFlowLayout.TOP_Y - 3 * _EAFlowLayout.ROW_PITCH,
        )
        self.assertGreater(_EAFlowLayout.OP_GAP, _EAFlowLayout.ARROW_HEAD_LENGTH)
        source_right = (
            _EAFlowLayout._lane_x("source") + _EAFlowLayout.WORD_WIDTH / 2
        )
        operation_left = _EAFlowLayout.MAIN_X - _EAFlowLayout.OP_RADIUS
        self.assertAlmostEqual(
            operation_left - source_right, _EAFlowLayout.OP_GAP
        )

    def test_mode_without_autoupdate_has_no_timing_diagram(self) -> None:
        diagrams = render_autoupdate_diagrams(
            self.load("ea/modes/compact/register/mode.yaml")
        )

        self.assertEqual(diagrams, [])

    def test_catalogs_include_base_and_profile_specific_modes(self) -> None:
        paths = catalog_mode_paths(self.isa_root)
        relative = {path.relative_to(self.isa_root).as_posix() for path in paths}

        self.assertIn("ea/modes/compact/register/mode.yaml", relative)
        self.assertIn(
            "extensions/FP/fea/modes/compact/immediate/mode.yaml", relative
        )
        self.assertIn(
            "extensions/VECTOR/vea/modes/EXT2/explicit_segment_index/mode.yaml",
            relative,
        )

    def test_cli_writes_complete_fragment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "ea-diagrams.tex"
            status = main(["--isa-root", str(self.isa_root), "--output", str(output)])

            rendered = output.read_text(encoding="utf-8")
            self.assertEqual(status, 0)
            self.assertTrue(rendered.startswith("% Generated by"))
            self.assertIn("BedrockEAFlowStart", rendered)
            self.assertNotIn("BedrockEAIndexedMemoryFlow", rendered)
            self.assertNotIn("BedrockEABasePostincrementMemoryFlow", rendered)
            self.assertGreater(rendered.count(r"\clearpage"), 22)

    def test_loaded_mode_inventory_renders_without_catalog_reload(self) -> None:
        modes = (
            self.load("ea/modes/compact/register/mode.yaml"),
            self.load("ea/modes/compact/immediate/mode.yaml"),
        )

        rendered = render_modes(modes)

        self.assertEqual(rendered.count("% Generated from "), 2)
        self.assertIn("Register Memory", rendered)
        self.assertIn("Integer Immediate", rendered)

    def test_mode_reserves_space_for_encoding_and_flow_together(self) -> None:
        rendered = render_mode(self.load("ea/modes/compact/immediate/mode.yaml"))

        self.assertIn(r"\par\Needspace{5.87in}%", rendered)
        self.assertIn(
            r"\BedrockEAProfileTitle{Compact Integer Immediate}", rendered
        )

    def test_profile_specific_mode_heading_names_the_profile(self) -> None:
        rendered = render_mode(
            self.load("extensions/FP/fea/modes/compact/immediate/mode.yaml")
        )

        self.assertIn(
            r"\BedrockEAProfileTitle{FP FEA Compact Floating-Point Immediate}",
            rendered,
        )


if __name__ == "__main__":
    unittest.main()
