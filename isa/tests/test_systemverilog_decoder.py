import re
import unittest
from pathlib import Path

from engine.generation import (
    ArtifactDefinition,
    ArtifactGenerationContext,
    ArtifactGeneratorRegistry,
)
from engine.ea_mode import EAMode, EAModeCatalog
from engine.encoding_metasyntax import EncodingMetasyntax
from engine.project import IsaProject
from engine.reference import Reference
from engine.systemverilog import decoder_ir, lowering
from engine.systemverilog.generate_decoder import render_outputs
from engine.workspace import SpecWorkspace


class SystemVerilogDecoderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).parents[1]
        cls.workspace = SpecWorkspace.load(cls.root.parent)
        project = cls.workspace.require_provider("isa")
        if not isinstance(project, IsaProject):
            raise TypeError("workspace isa provider must be an IsaProject")
        cls.project = project
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

    def _form(
        self, reference: Reference[decoder_ir.FormIR]
    ) -> decoder_ir.FormIR:
        key = ".".join((reference.owner, *reference.path, reference.element))
        return next(form for form in self.ir.forms if form.key == key)

    def test_package_projects_decode_ir_limits(self) -> None:
        package = self.outputs[Path("bedrock_decode_pkg.sv")]
        expected = {
            "BEDROCK_OPCODE_BITS": self.ir.limits.max_opcode_width,
            "BEDROCK_RECORD_BYTES": self.ir.limits.max_record_bytes,
            "BEDROCK_FORM_COUNT": self.ir.limits.form_count,
            "BEDROCK_OPERAND_SLOTS": self.ir.limits.max_operands,
            "BEDROCK_EA_SLOTS": self.ir.limits.max_ea_operands,
            "BEDROCK_OVERLAP_SLOTS": self.ir.limits.max_overlaps,
        }
        for parameter, value in expected.items():
            with self.subTest(parameter=parameter):
                self.assertRegex(
                    package,
                    rf"\b{parameter} = 10'd{value};",
                )

    def test_rendered_modules_keep_the_public_decoder_ports(self) -> None:
        package = self.outputs[Path("bedrock_decode_pkg.sv")]
        d0 = self.outputs[Path("bedrock_decode_d0.sv")]
        d1 = self.outputs[Path("bedrock_decode_d1.sv")]
        ea = self.outputs[Path("bedrock_decode_ea.sv")]

        self.assertIn("package bedrock_decode_pkg;", package)
        for public_type in (
            "} d0_result_t;",
            "} d0_ea_result_t;",
            "} d1_opcode_result_t;",
            "} ea_decode_result_t;",
        ):
            self.assertIn(public_type, package)
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
        self.assertIn("module bedrock_decode_ea", ea)
        self.assertIn(
            """input  d0_ea_result_t d0_i,
  input  logic [BEDROCK_RECORD_BYTES*8-1:0] record_i,
  input  logic [4:0] byte_count_i,
  output ea_decode_result_t result_o""",
            ea,
        )

    def test_d1_emits_every_operand_overlap_constraint(self) -> None:
        d1 = self.outputs[Path("bedrock_decode_d1.sv")]
        gather = self._form(
            Reference.parse("VECTOR.VGATHER.l_pn_p_pn_c_vn_x_vn_v")
        )
        match = re.search(
            rf"begin // \d+: {re.escape(gather.key)}\n(.*?)"
            rf"(?=\n\s+64'b|\n\s+default:)",
            d1,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match, gather.key)
        case = match.group(1)
        self.assertIn(
            f"decoded_result.overlap_count = 2'd{len(gather.overlaps)};",
            case,
        )
        operand_indexes = {
            operand.name: index for index, operand in enumerate(gather.operands)
        }
        for index, overlap in enumerate(gather.overlaps):
            with self.subTest(overlap=index, form=gather.key):
                self.assertEqual(overlap.rule, "illegal_instruction")
                self.assertIn(
                    f"decoded_result.overlaps[{index}].valid = 1'b1;", case
                )
                self.assertIn(
                    "decoded_result.overlaps["
                    f"{index}].rule = OVERLAP_ILLEGAL_INSTRUCTION;",
                    case,
                )
                self.assertIn(
                    "decoded_result.overlaps["
                    f"{index}].left_operand = 2'd{operand_indexes[overlap.left]};",
                    case,
                )
                self.assertIn(
                    "decoded_result.overlaps["
                    f"{index}].right_operand = 2'd{operand_indexes[overlap.right]};",
                    case,
                )

    def test_reference_decoder_consumes_all_ea_descriptors_before_payloads(
        self,
    ) -> None:
        form = self._form(Reference.parse("base.MOV.b_w_l_q_z_ea_s_ea_d"))
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
        form = self._form(Reference.parse("base.ADD.b_w_l_q_z_imm8s_ea_e"))
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

    def test_descriptor_resolution_preserves_profile_owned_update_amount(self) -> None:
        base_stage, base, _ = lowering.reference_ea_descriptor(
            self.ir, "ea", 0x63, [0x84], 1, 0
        )
        vector_stage, vector, _ = lowering.reference_ea_descriptor(
            self.ir, "vea", 0x63, [0x84], 1, 0
        )

        self.assertEqual(base_stage, "success")
        self.assertEqual(vector_stage, "success")
        self.assertEqual(base["update_difference"], "scale")
        self.assertEqual(vector["update_difference"], "vlen_bytes")

        base_stage, base, _ = lowering.reference_ea_descriptor(
            self.ir, "ea", 0x68, [0x80, 0x00], 2, 0
        )
        vector_stage, vector, _ = lowering.reference_ea_descriptor(
            self.ir, "vea", 0x68, [0x80, 0x00], 2, 0
        )

        self.assertEqual(base_stage, "success")
        self.assertEqual(vector_stage, "success")
        self.assertEqual(base["update_difference"], "constant_1")
        self.assertEqual(vector["update_difference"], "element_count")

    def test_profile_compact_membership_follows_owner_catalogs(self) -> None:
        profiles = {
            profile.name: profile for profile in self.ir.effective_addresses.profiles
        }
        compact_catalogs = {
            catalog.profile: catalog
            for catalog in EAModeCatalog.discover(
                self.root, self.project.types
            )
            if catalog.mode_type == "compact"
        }
        self.assertEqual(set(profiles), set(compact_catalogs))

        for profile_name, catalog in compact_catalogs.items():
            profile = profiles[profile_name]
            expected = set()
            for mode_id in catalog.modes:
                mode = EAMode.load(
                    catalog.mode_path(mode_id),
                    self.root,
                    self.project.types,
                    catalog=catalog,
                )
                for encoding in mode["encodings"]:
                    pattern = EncodingMetasyntax.parse(encoding["pattern"])
                    expected.update(
                        raw
                        for raw in range(1 << pattern.bit_width)
                        if pattern.matches(raw)
                    )
            actual = {
                entry.raw for entry in profile.compact_entries if entry.valid
            }
            self.assertEqual(actual, expected, profile_name)

    def test_generation_is_deterministic(self) -> None:
        self.assertEqual(self.outputs, render_outputs(Path(".")))

    def test_manifest_role_selects_a_renamed_output_path(self) -> None:
        registered = ArtifactGeneratorRegistry.discover(self.workspace).generator(
            "systemverilog-package"
        )
        definition = ArtifactDefinition(
            "systemverilog-package",
            registered.definition.source,
            {"outputs": {"package": "renamed/decode-contract.sv"}},
        )

        generated = type(registered)(definition).generate(
            ArtifactGenerationContext.create(self.workspace, Path("output"))
        )

        self.assertEqual(
            {artifact.relative_path for artifact in generated.artifacts},
            {Path("renamed/decode-contract.sv")},
        )


if __name__ == "__main__":
    unittest.main()
