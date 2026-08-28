import tempfile
import unittest
from pathlib import Path

from engine.ea_mode import EAMode
from engine.generate_ea_diagrams import (
    _EAFlowLayout,
    catalog_mode_paths,
    main,
    render_autoupdate_diagrams,
    render_encoding_diagram,
    render_flow_diagram,
    render_mode,
)


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
        self.assertIn("Integer immediate operand generation", rendered)

    def test_index_autoupdate_variants_are_integrated_into_address_flows(self) -> None:
        diagrams = render_autoupdate_diagrams(
            self.load("ea/modes/EXT2/explicit_segment_index/mode.yaml")
        )

        self.assertEqual(len(diagrams), 2)
        self.assertTrue(diagrams[0].startswith(r"\clearpage"))
        self.assertIn("postincrement address generation", diagrams[0])
        self.assertIn("predecrement address generation", diagrams[1])
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

    def test_mode_reserves_space_for_encoding_and_flow_together(self) -> None:
        rendered = render_mode(self.load("ea/modes/compact/immediate/mode.yaml"))

        self.assertIn(r"\par\Needspace{5.87in}%", rendered)
        self.assertIn("EA / compact / Integer immediate", rendered)

    def test_profile_specific_mode_heading_names_the_profile(self) -> None:
        rendered = render_mode(
            self.load("extensions/FP/fea/modes/compact/immediate/mode.yaml")
        )

        self.assertIn("FP FEA / compact / Floating-point immediate", rendered)


if __name__ == "__main__":
    unittest.main()
