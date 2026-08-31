import unittest
from pathlib import Path
import shutil
import subprocess
import tempfile

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
        cls.root = Path(__file__).parents[1] / "isa"
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

    def test_decoder_projection_owns_public_ports_and_derived_limits(self) -> None:
        generator = ArtifactGeneratorRegistry.discover(self.workspace).generator(
            "systemverilog-instruction-decoder"
        )
        projection = generator.project()

        self.assertEqual(
            tuple((port.direction, port.name) for port in projection.d0_ports),
            (
                ("input", "valid_i"),
                ("input", "opcode_class_i"),
                ("input", "opcode_i"),
                ("output", "result_o"),
                ("output", "ea_result_o"),
            ),
        )
        self.assertEqual(
            tuple((port.direction, port.name) for port in projection.d1_ports),
            (
                ("input", "d0_i"),
                ("input", "record_i"),
                ("input", "byte_count_i"),
                ("output", "result_o"),
            ),
        )
        self.assertEqual(projection.limits.form_count, len(self.ir.forms))
        self.assertEqual(
            projection.limits.max_overlaps,
            max(len(form.overlaps) for form in self.ir.forms),
        )
        self.assertEqual(
            projection.limits.max_required_bytes,
            max(form.maximum_required_bytes for form in self.ir.forms),
        )

    def test_decode_ir_preserves_effective_form_cpuid_requirements(self) -> None:
        expected = {
            f"{bundle.owner}.{bundle.instruction.mnemonic}.{form.id}": {
                field.id for field in bundle.required_cpuid_flags_for(form)
            }
            for bundle in self.project.select()
            for form in bundle.encodings.forms
        }
        actual = {
            form.key: set(form.required_cpuid_flags) for form in self.ir.forms
        }

        self.assertEqual(actual, expected)
        self.assertEqual(
            {field.id for field in self.ir.cpuid_flags},
            set().union(*expected.values()),
        )

    def test_d1_overlap_projection_maps_operand_names_to_public_slots(self) -> None:
        generator = ArtifactGeneratorRegistry.discover(self.workspace).generator(
            "systemverilog-instruction-decoder"
        )
        projection = generator.project()
        expected = []
        for form in self.ir.forms:
            slots = {operand.name: index for index, operand in enumerate(form.operands)}
            expected.extend(
                (form.key, slots[overlap.left], slots[overlap.right], overlap.rule)
                for overlap in form.overlaps
            )

        self.assertEqual(
            tuple(
                (
                    overlap.form_key,
                    overlap.left_operand,
                    overlap.right_operand,
                    overlap.rule,
                )
                for overlap in projection.d1_overlaps
            ),
            tuple(expected),
        )

    def test_generated_decoder_is_accepted_by_a_systemverilog_consumer(self) -> None:
        verilator = shutil.which("verilator")
        if verilator is None:
            self.skipTest("verilator is not available")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = []
            registry = ArtifactGeneratorRegistry.discover(self.workspace)
            for artifact_id in (
                "systemverilog-package",
                "systemverilog-instruction-decoder",
                "systemverilog-ea-decoder",
            ):
                generated = registry.generate(artifact_id, self.workspace, root)
                for artifact in generated.artifacts:
                    source = root / artifact.relative_path
                    source.parent.mkdir(parents=True, exist_ok=True)
                    source.write_text(str(artifact.content), encoding="utf-8")
                    sources.append(source)
            projection = registry.generator(
                "systemverilog-instruction-decoder"
            ).project()
            declarations = []
            instances = []
            for module_name, prefix, ports in (
                ("bedrock_decode_d0", "d0", projection.d0_ports),
                ("bedrock_decode_d1", "d1", projection.d1_ports),
            ):
                connections = []
                for port in ports:
                    signal = f"{prefix}_{port.name}"
                    declarations.append(f"  {port.type_name} {signal};")
                    connections.append(f"    .{port.name}({signal})")
                instances.append(
                    f"  {module_name} {prefix}_instance (\n"
                    + ",\n".join(connections)
                    + "\n  );"
                )
            consumer = root / "decoder_consumer.sv"
            consumer.write_text(
                "module decoder_consumer;\n"
                "  import bedrock_decode_pkg::*;\n"
                + "\n".join(declarations)
                + "\n"
                + "\n".join(instances)
                + "\nendmodule\n",
                encoding="utf-8",
            )
            sources.append(consumer)
            sources.sort(key=lambda path: (not path.name.endswith("_pkg.sv"), path.name))
            completed = subprocess.run(
                [
                    verilator,
                    "--lint-only",
                    "--sv",
                    "-Wno-fatal",
                    *(str(source) for source in sources),
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)

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
