import unittest
from pathlib import Path

from engine.generation import ArtifactGeneratorRegistry
from engine.project import IsaProject
from engine.systemverilog.generate_decoder import OUTPUT_NAMES, render_outputs


class SystemVerilogDecoderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).parents[1]
        cls.project = IsaProject.load(cls.root)
        cls.outputs = render_outputs(Path("."))

    def test_current_outputs_and_interfaces_are_well_formed(self) -> None:
        self.assertEqual(
            set(self.outputs),
            {Path(name) for name in OUTPUT_NAMES},
        )
        package = self.outputs[Path("bedrock_decode_pkg.sv")]
        d0 = self.outputs[Path("bedrock_decode_d0.sv")]
        d1 = self.outputs[Path("bedrock_decode_d1.sv")]
        ea = self.outputs[Path("bedrock_decode_ea.sv")]
        form_count = sum(
            len(bundle.encodings.forms) for bundle in self.project.select()
        )

        self.assertIn("package bedrock_decode_pkg;", package)
        for declaration in (
            "BEDROCK_OPCODE_BITS = 10'd42",
            "BEDROCK_RECORD_BYTES = 10'd18",
            f"BEDROCK_FORM_COUNT = 10'd{form_count}",
            "BEDROCK_OPERAND_SLOTS = 10'd6",
            "BEDROCK_EA_SLOTS = 10'd2",
            "} d0_result_t;",
            "} d0_ea_result_t;",
            "} d1_opcode_result_t;",
            "} ea_decode_result_t;",
            "logic [31:0] form_high_decode;",
            "logic [31:0] form_low_decode;",
            "logic [6:0] alt_raw;",
            "logic [3:0] base_cursor;",
        ):
            self.assertIn(declaration, package)
        self.assertIn("module bedrock_decode_d0", d0)
        self.assertIn(
            """input  logic valid_i,
  input  opcode_class_e opcode_class_i,
  input  logic [BEDROCK_OPCODE_BITS-1:0] opcode_i,
  output d0_result_t result_o,
  output d0_ea_result_t ea_result_o""",
            d0,
        )
        self.assertIn("module bedrock_decode_d1", d1)
        self.assertIn(
            """input  d0_result_t d0_i,
  input  logic [BEDROCK_RECORD_BYTES*8-1:0] record_i,
  input  logic [4:0] byte_count_i,
  output d1_opcode_result_t result_o""",
            d1,
        )
        self.assertNotIn("opcode_i", d1)
        self.assertIn("d0_i.form_high_decode", d1)
        self.assertIn("d0_i.form_low_decode", d1)
        self.assertIn("unique casez", d1)
        self.assertIn("module bedrock_decode_ea", ea)
        self.assertIn(
            """input  d0_ea_result_t d0_i,
  input  logic [BEDROCK_RECORD_BYTES*8-1:0] record_i,
  input  logic [4:0] byte_count_i,
  output ea_decode_result_t result_o""",
            ea,
        )

    def test_generation_is_deterministic(self) -> None:
        self.assertEqual(self.outputs, render_outputs(Path(".")))

    def test_registered_artifacts_own_exactly_the_public_files(self) -> None:
        registry = ArtifactGeneratorRegistry.discover(self.project)
        expected = {
            "systemverilog-package": {Path("rtl/bedrock_decode_pkg.sv")},
            "systemverilog-instruction-decoder": {
                Path("rtl/bedrock_decode_d0.sv"),
                Path("rtl/bedrock_decode_d1.sv"),
            },
            "systemverilog-ea-decoder": {Path("rtl/bedrock_decode_ea.sv")},
        }
        for artifact_id, paths in expected.items():
            with self.subTest(artifact=artifact_id):
                generated = registry.generate(artifact_id, self.project, Path("output"))
                self.assertEqual(
                    {artifact.relative_path for artifact in generated.artifacts},
                    paths,
                )


if __name__ == "__main__":
    unittest.main()
