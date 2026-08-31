import re
import unittest
from pathlib import Path

from engine.generation import (
    ArtifactDefinition,
    ArtifactGenerationContext,
    ArtifactGeneratorRegistry,
)
from engine.project import IsaProject
from engine.workspace import SpecWorkspace


def _declared_identifier(value: object) -> str:
    text = str(value)
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", text) is None:
        raise AssertionError(f"source identifier is not directly projectable: {text}")
    return text.upper()


class SystemVerilogArchitectureArtifactsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = Path(__file__).parents[2]
        cls.workspace = SpecWorkspace.load(cls.repository)
        project = cls.workspace.require_provider("isa")
        if not isinstance(project, IsaProject):
            raise TypeError("workspace isa provider must be an IsaProject")
        cls.project = project
        cls.registry = ArtifactGeneratorRegistry.discover(cls.workspace)

    def _generate(self, artifact_id: str):
        return self.registry.generate(
            artifact_id, self.workspace, self.repository / "output"
        )

    def test_manifest_role_selects_a_renamed_output_path(self) -> None:
        registered = self.registry.generator("systemverilog-condition-evaluator")
        definition = ArtifactDefinition(
            "systemverilog-condition-evaluator",
            registered.definition.source,
            {"outputs": {"evaluator": "renamed/condition-contract.sv"}},
        )

        generated = type(registered)(definition).generate(
            ArtifactGenerationContext.create(self.workspace, self.repository / "output")
        )

        self.assertEqual(
            {artifact.relative_path for artifact in generated.artifacts},
            {Path("renamed/condition-contract.sv")},
        )

    def test_cpuid_projection_preserves_a_canonical_query_record(self) -> None:
        package = (
            self._generate("systemverilog-cpuid")
            .artifact("rtl/bedrock_cpuid_pkg.sv")
            .content
        )
        cpuid_class = next(
            item
            for namespace in self.project.cpuid.namespaces.values()
            for item in namespace.classes.values()
            if item.value is not None
            for leaf in item.leaves.values()
            for query in leaf.queries
            if query.indexes.first != query.indexes.last and query.fields
        )
        leaf = next(
            leaf
            for leaf in cpuid_class.leaves.values()
            if any(
                query.indexes.first != query.indexes.last and query.fields
                for query in leaf.queries
            )
        )
        query = next(
            query
            for query in leaf.queries
            if query.indexes.first != query.indexes.last and query.fields
        )
        field = query.fields[0]
        prefix = "_".join(
            (
                "CPUID",
                _declared_identifier(cpuid_class.reference.owner),
                _declared_identifier(cpuid_class.id),
                _declared_identifier(leaf.id),
                _declared_identifier(query.id),
            )
        )
        field_prefix = f"{prefix}_{_declared_identifier(field.id)}"
        mask = ((1 << field.bits) - 1) << field.lsb

        self.assertIn(
            f"{prefix}_FIRST = 16'h{query.indexes.first:04x}", package
        )
        self.assertIn(f"{prefix}_LAST = 16'h{query.indexes.last:04x}", package)
        self.assertIn(f"{prefix}_STRIDE = 16'd{query.indexes.stride}", package)
        self.assertIn(f"{field_prefix}_LSB = 7'd{field.lsb}", package)
        self.assertIn(f"{field_prefix}_BITS = 7'd{field.bits}", package)
        self.assertIn(f"{field_prefix}_MASK = 64'h{mask:016x}", package)

    def test_event_projection_preserves_fixed_and_dynamic_event_routes(self) -> None:
        generated = self._generate("systemverilog-event-codec")
        package = generated.artifact("rtl/bedrock_event_pkg.sv").content
        codec = generated.artifact("rtl/bedrock_event_codec.sv").content
        resolved = self.project.events.resolved_events()
        fixed = next(item for item in resolved if item.code.value is not None)
        dynamic = next(item for item in resolved if item.code.value is None)
        fixed_name = (
            f"EVENT_{_declared_identifier(fixed.owner)}_"
            f"{_declared_identifier(fixed.event.id)}"
        )
        fixed_frame = f"EVENT_FRAME_{_declared_identifier(fixed.event.frame)}"
        dynamic_frame = f"EVENT_FRAME_{_declared_identifier(dynamic.event.frame)}"

        self.assertIn(
            f"{fixed_name} = 32'h{fixed.code.value:08x}", package
        )
        self.assertIn(
            f"{fixed_name}: begin frame_o = {fixed_frame};", codec
        )
        self.assertIn(
            f"8'h{dynamic.code.class_value:02x}: frame_o = {dynamic_frame};",
            codec,
        )
        self.assertNotIn(
            f"EVENT_{_declared_identifier(dynamic.owner)}_"
            f"{_declared_identifier(dynamic.event.id)} =",
            package,
        )

    def test_register_projection_preserves_selector_and_write_mask(self) -> None:
        generated = self._generate("systemverilog-register-contracts")
        package = generated.artifact("rtl/bedrock_register_pkg.sv").content
        contracts = generated.artifact("rtl/bedrock_register_contracts.sv").content
        register = next(
            register
            for namespace in self.project.registers.namespaces.values()
            for group in namespace.groups.values()
            for register in group.registers.values()
            if register.encoding is not None
            and register.layout is not None
            and register.layout.fields
        )
        prefix = "_".join(
            (
                "REGISTER",
                _declared_identifier(register.owner),
                _declared_identifier(register.group),
                _declared_identifier(register.id),
            )
        )
        group_name = (
            f"REGISTER_GROUP_{_declared_identifier(register.owner)}_"
            f"{_declared_identifier(register.group)}"
        )
        writable_mask = sum(
            ((1 << field.bits) - 1) << field.lsb
            for field in register.layout.fields
        )

        self.assertIn(f"{prefix} = 16'h{register.encoding:04x}", package)
        self.assertIn(f"{{{group_name}, {prefix}}}: begin", contracts)
        self.assertIn(
            f"writable_mask_o = 64'h{writable_mask:016x}", contracts
        )

    def test_vector_geometry_projects_owner_register_counts(self) -> None:
        generated = self._generate("systemverilog-vector-geometry")
        package = generated.artifact("rtl/bedrock_vector_geometry_pkg.sv").content
        vector = self.project.registers.namespaces["VECTOR"]

        self.assertIn(
            "BEDROCK_VECTOR_REGISTER_COUNT = "
            f"{len(vector.groups['VECTOR'].registers)}",
            package,
        )
        self.assertIn(
            "BEDROCK_PREDICATE_REGISTER_COUNT = "
            f"{len(vector.groups['PREDICATE'].registers)}",
            package,
        )


if __name__ == "__main__":
    unittest.main()
