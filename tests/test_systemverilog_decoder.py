import unittest
from dataclasses import replace
from pathlib import Path
import shutil
import subprocess
import tempfile

from engine.generation import ArtifactGeneratorRegistry
from engine.ea_mode import EAMode, EAModeCatalog
from engine.encoding_metasyntax import EncodingMetasyntax
from engine.project import IsaProject
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
        for value_bit, position in zip(
            range(len(positions) - 1, -1, -1), positions
        ):
            if value & (1 << value_bit):
                opcode |= 1 << position
            else:
                opcode &= ~(1 << position)
        return opcode

    def _descriptor_case(
        self, profile_name: str
    ) -> tuple[int, decoder_ir.EaFormIR, bytes]:
        profile = next(
            item
            for item in self.ir.effective_addresses.profiles
            if item.name == profile_name
        )
        entry = next(
            item
            for item in profile.compact_entries
            if item.valid
            and item.payload_width == 8
            and next(
                form
                for form in profile.compact_forms
                if form.name == item.form_name
            ).referenced_descriptor_family
        )
        compact = next(
            form for form in profile.compact_forms if form.name == entry.form_name
        )
        family = next(
            item
            for item in self.ir.effective_addresses.descriptor_families
            if item.name == compact.referenced_descriptor_family
        )
        descriptor = family.forms[0]
        return (
            entry.raw,
            descriptor,
            descriptor.value.to_bytes(family.descriptor_bytes, "big"),
        )

    def test_reference_decoder_consumes_all_ea_descriptors_before_payloads(
        self,
    ) -> None:
        form = next(
            item
            for item in self.ir.forms
            if sum(
                isinstance(operand.source, decoder_ir.EffectiveAddressSourceIR)
                for operand in item.operands
            )
            >= 2
        )
        opcode = lowering.representative_opcode(form)
        descriptors = bytearray()
        payload_values: dict[str, int] = {}
        for index, layout in enumerate(
            item for item in form.layout if isinstance(item, decoder_ir.ParseEaIR)
        ):
            operand = next(
                item for item in form.operands if item.name == layout.operand_name
            )
            assert isinstance(operand.source, decoder_ir.EffectiveAddressSourceIR)
            raw, _descriptor, encoded = self._descriptor_case(layout.profile)
            opcode = self._set_field(opcode, operand.source.positions, raw)
            descriptors.extend(encoded)
            payload_values[operand.name] = index + 1

        record = bytearray(form.opcode_space_bytes)
        record.extend(descriptors)
        record.extend(payload_values.values())
        stage, decoded = lowering.reference_d1(
            self.ir, form, opcode, record, len(record)
        )

        self.assertEqual(stage, "success")
        for operand_name, payload in payload_values.items():
            with self.subTest(operand=operand_name):
                self.assertEqual(decoded["eas"][operand_name]["payload"], payload)

    def test_reference_decoder_uses_layout_order_after_descriptor_prefix(self) -> None:
        form = next(
            item
            for item in self.ir.forms
            if any(
                isinstance(operand.source, decoder_ir.EffectiveAddressSourceIR)
                for operand in item.operands
            )
            and any(
                isinstance(operand.source, decoder_ir.AppendedPayloadSourceIR)
                for operand in item.operands
            )
        )
        ea_layout = next(
            item for item in form.layout if isinstance(item, decoder_ir.ParseEaIR)
        )
        payload_layout = next(
            item for item in form.layout if isinstance(item, decoder_ir.ReadPayloadIR)
        )
        form = replace(form, layout=(payload_layout, ea_layout))
        ea_operand = next(
            item for item in form.operands if item.name == ea_layout.operand_name
        )
        assert isinstance(ea_operand.source, decoder_ir.EffectiveAddressSourceIR)
        raw, _descriptor, encoded = self._descriptor_case(ea_layout.profile)
        opcode = self._set_field(
            lowering.representative_opcode(form), ea_operand.source.positions, raw
        )
        scalar_bytes = payload_layout.width // 8
        scalar_value = 0x35
        ea_payload = 0x79
        record = bytearray(form.opcode_space_bytes)
        record.extend(encoded)
        record.extend(scalar_value.to_bytes(scalar_bytes, "little"))
        record.append(ea_payload)

        stage, decoded = lowering.reference_d1(
            self.ir, form, opcode, record, len(record)
        )

        self.assertEqual(stage, "success")
        self.assertEqual(decoded["values"][payload_layout.operand_name], scalar_value)
        self.assertEqual(decoded["eas"][ea_layout.operand_name]["payload"], ea_payload)

    def test_descriptor_resolution_preserves_profile_owned_update_semantics(
        self,
    ) -> None:
        for profile in self.ir.effective_addresses.profiles:
            for compact in profile.compact_forms:
                if not compact.referenced_descriptor_family:
                    continue
                raw = next(
                    entry.raw
                    for entry in profile.compact_entries
                    if entry.valid and entry.form_name == compact.name
                )
                family = next(
                    item
                    for item in self.ir.effective_addresses.descriptor_families
                    if item.name == compact.referenced_descriptor_family
                )
                for descriptor in family.forms:
                    with self.subTest(
                        profile=profile.name,
                        compact=compact.name,
                        descriptor=descriptor.name,
                    ):
                        record = descriptor.value.to_bytes(
                            family.descriptor_bytes, "big"
                        )
                        stage, decoded, consumed = lowering.reference_ea_descriptor(
                            self.ir,
                            profile.name,
                            raw,
                            record,
                            len(record),
                            0,
                        )
                        self.assertEqual(stage, "success")
                        self.assertEqual(consumed, family.descriptor_bytes)
                        assert decoded is not None
                        self.assertEqual(
                            (
                                decoded["update_target"],
                                decoded["update_mode"],
                                decoded["update_difference"],
                            ),
                            (
                                descriptor.update_target,
                                descriptor.update_mode,
                                descriptor.update_difference,
                            ),
                        )

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
            {port.name: port.direction for port in projection.d0_ports},
            {
                "valid_i": "input",
                "opcode_class_i": "input",
                "opcode_i": "input",
                "result_o": "output",
                "ea_result_o": "output",
            },
        )
        self.assertEqual(
            {port.name: port.direction for port in projection.d1_ports},
            {
                "d0_i": "input",
                "record_i": "input",
                "byte_count_i": "input",
                "result_o": "output",
            },
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


if __name__ == "__main__":
    unittest.main()
