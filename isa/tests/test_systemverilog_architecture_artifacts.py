import unittest
from pathlib import Path

from engine.generation import ArtifactGeneratorRegistry
from engine.project import IsaProject


class SystemVerilogArchitectureArtifactsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = Path(__file__).parents[2]
        cls.project = IsaProject.load(cls.repository / "isa")
        cls.registry = ArtifactGeneratorRegistry.discover(cls.project)
        cls.artifact_ids = (
            "systemverilog-condition-evaluator",
            "systemverilog-cpuid",
            "systemverilog-event-codec",
            "systemverilog-register-contracts",
            "systemverilog-vector-geometry",
            "systemverilog-assertions",
        )

    def _generate(self, artifact_id: str):
        return self.registry.generate(
            artifact_id, self.project, self.repository / "output"
        )

    def test_all_reserved_systemverilog_artifacts_are_implemented(self) -> None:
        for artifact_id in self.artifact_ids:
            with self.subTest(artifact=artifact_id):
                self.assertIn(artifact_id, self.registry.implemented_ids)
                generated = self._generate(artifact_id)
                declared = set(
                    self.registry.generator(artifact_id).definition.declared_outputs
                )
                self.assertEqual(
                    {artifact.relative_path for artifact in generated.artifacts},
                    declared,
                )

    def test_architecture_artifacts_are_deterministic(self) -> None:
        for artifact_id in self.artifact_ids:
            with self.subTest(artifact=artifact_id):
                self.assertEqual(
                    self._generate(artifact_id), self._generate(artifact_id)
                )

    def test_condition_evaluator_covers_the_complete_encoding(self) -> None:
        source = (
            self._generate("systemverilog-condition-evaluator")
            .artifact("rtl/bedrock_condition_eval.sv")
            .content
        )
        for value in range(16):
            self.assertIn(f"4'h{value:x}: holds_o", source)
        self.assertIn("flag_z = flags_i[3]", source)
        self.assertIn("flag_v = flags_i[0]", source)

    def test_cpuid_projection_contains_selectors_ranges_and_field_masks(self) -> None:
        package = (
            self._generate("systemverilog-cpuid")
            .artifact("rtl/bedrock_cpuid_pkg.sv")
            .content
        )
        self.assertIn("CPUID_BASE_BASE_CLASS = 32'h00000000", package)
        self.assertIn("CPUID_BASE_BASE_IDENTITY_LEAF = 16'h0000", package)
        self.assertIn("CPUID_BASE_BASE_IDENTITY_VENDOR_NAME_FIRST = 16'h0003", package)
        self.assertIn("CPUID_BASE_BASE_IDENTITY_VENDOR_NAME_LAST = 16'h000a", package)
        self.assertIn(
            "CPUID_BASE_BASE_IDENTITY_HEADER_MAX_CLASS_MASK = 64'hffffffff00000000",
            package,
        )

    def test_event_projection_distinguishes_fixed_and_dynamic_codes(self) -> None:
        generated = self._generate("systemverilog-event-codec")
        package = generated.artifact("rtl/bedrock_event_pkg.sv").content
        codec = generated.artifact("rtl/bedrock_event_codec.sv").content
        frame = generated.artifact("rtl/bedrock_event_frame.sv").content
        self.assertIn("EVENT_BASE_BREAKPOINT = 32'h00000001", package)
        self.assertIn("EVENT_FP_FLOATING_POINT_EXCEPTION = 32'h00000060", package)
        self.assertIn("unique case (code_i[31:24])", codec)
        self.assertNotIn("8'h00: frame_o", codec)
        self.assertIn("saved_dfa_i, 2'b0, frame_type_i, frame_slots_o", frame)

    def test_register_projection_emits_reserved_mask_and_reset_contract(self) -> None:
        generated = self._generate("systemverilog-register-contracts")
        package = generated.artifact("rtl/bedrock_register_pkg.sv").content
        contracts = generated.artifact("rtl/bedrock_register_contracts.sv").content
        self.assertIn("REGISTER_BASE_CONTROL_UCTL = 16'h010d", package)
        self.assertIn(
            "REGISTER_BASE_CONTROL_UCTL_V_MASK = 64'h0000000100000000", package
        )
        self.assertIn("writable_mask_o = 64'h00000001ffffffff", contracts)
        self.assertIn("reserved_zero_o = valid_o", contracts)

    def test_vector_geometry_tracks_architectural_register_counts(self) -> None:
        generated = self._generate("systemverilog-vector-geometry")
        package = generated.artifact("rtl/bedrock_vector_geometry_pkg.sv").content
        permute = generated.artifact("rtl/bedrock_vector_permute.sv").content
        self.assertIn("BEDROCK_VECTOR_REGISTER_COUNT = 32", package)
        self.assertIn("BEDROCK_PREDICATE_REGISTER_COUNT = 16", package)
        self.assertIn("parameter integer VLEN = 256", permute)
        self.assertIn("if (valid_o) begin", permute)


if __name__ == "__main__":
    unittest.main()
