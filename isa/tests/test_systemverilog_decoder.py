import unittest
from pathlib import Path

from engine.generation import ArtifactGeneratorRegistry
from engine.project import IsaProject
from engine.systemverilog import decoder_ir, lowering
from engine.systemverilog.generate_decoder import OUTPUT_NAMES, render_outputs


class SystemVerilogDecoderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).parents[1]
        cls.project = IsaProject.load(cls.root)
        cls.ir = decoder_ir.load_decode_ir()
        cls.outputs = render_outputs(Path("."))

    @staticmethod
    def _set_field(opcode: int, positions: tuple[int, ...], value: int) -> int:
        for value_bit, position in zip(range(len(positions) - 1, -1, -1), positions):
            if value & (1 << value_bit):
                opcode |= 1 << position
            else:
                opcode &= ~(1 << position)
        return opcode

    def _form(self, key: str) -> decoder_ir.FormIR:
        return next(form for form in self.ir.forms if form.key == key)

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
            "BEDROCK_OVERLAP_SLOTS = 10'd2",
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
        self.assertIn("alt_span.descriptor_bytes", d0)
        self.assertIn("descriptor_end_cursor", ea)
        self.assertIn("ea_static_payload_prefix_bytes", ea)
        self.assertIn("ea_payload_byte_count", ea)
        self.assertIn("ea_descriptor_byte_count", ea)
        for offset in range(3):
            self.assertIn(f"descriptor_ext1_{offset}", ea)
            self.assertIn(f"descriptor_ext2_{offset}", ea)
        self.assertNotIn(
            "descriptor_end_cursor = low_descriptor_parse.next_cursor", ea
        )
        self.assertNotIn(
            "descriptor_end_cursor = alt_descriptor_parse.next_cursor", ea
        )

    def test_d1_emits_every_operand_overlap_constraint(self) -> None:
        d1 = self.outputs[Path("bedrock_decode_d1.sv")]
        gather = self._form("VECTOR.instructions.VGATHER.l_pn_p_pn_c_vn_x_vn_v")
        self.assertEqual(len(gather.overlaps), 2)
        self.assertIn("decoded_result.overlap_count = 2'd2;", d1)
        self.assertIn("decoded_result.overlaps[0].valid = 1'b1;", d1)
        self.assertIn("decoded_result.overlaps[1].valid = 1'b1;", d1)

    def test_reference_decoder_consumes_all_ea_descriptors_before_payloads(
        self,
    ) -> None:
        form = self._form("base.instructions.MOV.b_w_l_q_z_ea_s_ea_d")
        opcode = lowering.representative_opcode(form)
        for operand in form.operands:
            if isinstance(operand.source, decoder_ir.EffectiveAddressSourceIR):
                opcode = self._set_field(opcode, operand.source.positions, 0x5F)

        record = [0] * form.opcode_space_bytes + [0x01, 0x02, 0xF1, 0xF2]
        stage, decoded = lowering.reference_d1(
            self.ir, form, opcode, record, len(record)
        )

        self.assertEqual(stage, "success")
        self.assertEqual(decoded["eas"]["src"]["descriptor"], 0x01)
        self.assertEqual(decoded["eas"]["dst"]["descriptor"], 0x02)
        self.assertEqual(decoded["eas"]["src"]["payload"], 0xF1)
        self.assertEqual(decoded["eas"]["dst"]["payload"], 0xF2)

    def test_reference_decoder_uses_operand_order_after_descriptor_prefix(self) -> None:
        form = self._form("base.instructions.ADD.b_w_l_q_z_imm8s_ea_e")
        opcode = lowering.representative_opcode(form)
        destination = next(
            operand for operand in form.operands if operand.name == "dst"
        )
        self.assertIsInstance(destination.source, decoder_ir.EffectiveAddressSourceIR)
        opcode = self._set_field(opcode, destination.source.positions, 0x5F)

        record = [0] * form.opcode_space_bytes + [0x01, 0x7A, 0x5C]
        stage, decoded = lowering.reference_d1(
            self.ir, form, opcode, record, len(record)
        )

        self.assertEqual(stage, "success")
        self.assertEqual(decoded["values"]["src"], 0x7A)
        self.assertEqual(decoded["eas"]["dst"]["descriptor"], 0x01)
        self.assertEqual(decoded["eas"]["dst"]["payload"], 0x5C)

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
