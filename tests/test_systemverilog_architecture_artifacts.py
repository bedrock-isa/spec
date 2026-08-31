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
from engine.project import IsaProject
from engine.workspace import SpecWorkspace


class SystemVerilogArchitectureArtifactsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = Path(__file__).parents[1]
        cls.workspace = SpecWorkspace.load(cls.repository)
        cls.registry = ArtifactGeneratorRegistry.discover(cls.workspace)
        project = cls.workspace.require_provider("isa")
        if not isinstance(project, IsaProject):
            raise TypeError("workspace isa provider must be an IsaProject")
        cls.project = project
        cls.context = ArtifactGenerationContext.create(
            cls.workspace, cls.repository / "output"
        )

    def test_cpuid_projection_owns_queries_fields_and_masks(self) -> None:
        projection = self.registry.generator("systemverilog-cpuid").project(
            self.context
        )
        expected_queries = {
            (owner, cpuid_class.id, leaf.id, query.id)
            for owner, namespace in self.project.cpuid.namespaces.items()
            for cpuid_class in namespace.classes.values()
            for leaf in cpuid_class.leaves.values()
            for query in leaf.queries
        }

        self.assertEqual(
            {
                (query.owner, query.class_id, query.leaf_id, query.query_id)
                for query in projection.queries
            },
            expected_queries,
        )
        for query in projection.queries:
            self.assertLessEqual(query.first_index, query.last_index)
            self.assertGreater(query.stride, 0)
            for field in query.fields:
                self.assertEqual(field.mask, ((1 << field.bits) - 1) << field.lsb)

    def test_event_projection_owns_fixed_and_dynamic_routes(self) -> None:
        projection = self.registry.generator("systemverilog-event-codec").project(
            self.context
        )
        resolved = self.project.events.resolved_events()
        expected_fixed = {
            (item.owner, item.event.id, item.code.value, item.event.frame)
            for item in resolved
            if item.code.value is not None
        }
        expected_dynamic = {
            (item.code.class_value, item.event.frame)
            for item in resolved
            if item.code.selector.kind != "fixed"
        }

        self.assertEqual(
            {
                (route.owner, route.event_id, route.code, route.frame)
                for route in projection.fixed_routes
            },
            expected_fixed,
        )
        self.assertEqual(
            {(route.class_value, route.frame) for route in projection.dynamic_routes},
            expected_dynamic,
        )

    def test_register_projection_owns_selectors_and_write_masks(self) -> None:
        projection = self.registry.generator(
            "systemverilog-register-contracts"
        ).project(self.context)
        expected = {}
        for owner, namespace in self.project.registers.namespaces.items():
            for group in namespace.groups.values():
                for register in group.registers.values():
                    if register.encoding is None:
                        continue
                    expected[(owner, group.id, register.id)] = (
                        register.encoding,
                        (1 << 64) - 1
                        if register.layout is None
                        else sum(
                            ((1 << field.bits) - 1) << field.lsb
                            for field in register.layout.fields
                        ),
                    )

        self.assertEqual(
            {
                (register.owner, register.group_id, register.register_id): (
                    register.encoding,
                    register.writable_mask,
                )
                for register in projection.registers
            },
            expected,
        )

    def test_vector_projection_owns_architectural_register_counts(self) -> None:
        projection = self.registry.generator("systemverilog-vector-geometry").project(
            self.context
        )
        namespace = self.project.registers.namespaces["VECTOR"]

        self.assertEqual(
            projection.vector_register_count,
            len(namespace.groups["VECTOR"].registers),
        )
        self.assertEqual(
            projection.predicate_register_count,
            len(namespace.groups["PREDICATE"].registers),
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

    def test_generators_populate_their_declared_output_roles(self) -> None:
        for artifact_id in (
            "systemverilog-condition-evaluator",
            "systemverilog-cpuid",
            "systemverilog-event-codec",
            "systemverilog-register-contracts",
            "systemverilog-vector-geometry",
        ):
            with self.subTest(artifact=artifact_id):
                generator = self.registry.generator(artifact_id)
                generated = self.registry.generate(
                    artifact_id, self.workspace, self.repository / "output"
                )
                self.assertEqual(
                    {artifact.relative_path for artifact in generated.artifacts},
                    set(generator.definition.outputs.values()),
                )

    def test_generated_contracts_are_accepted_by_a_systemverilog_consumer(self) -> None:
        verilator = shutil.which("verilator")
        if verilator is None:
            self.skipTest("verilator is not available")
        for artifact_id in (
            "systemverilog-condition-evaluator",
            "systemverilog-cpuid",
            "systemverilog-event-codec",
            "systemverilog-register-contracts",
            "systemverilog-vector-geometry",
        ):
            with self.subTest(artifact=artifact_id), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                generated = self.registry.generate(
                    artifact_id, self.workspace, root
                )
                sources = []
                for artifact in generated.artifacts:
                    source = root / artifact.relative_path
                    source.parent.mkdir(parents=True, exist_ok=True)
                    source.write_text(str(artifact.content), encoding="utf-8")
                    sources.append(source)
                sources.sort(
                    key=lambda path: (not path.name.endswith("_pkg.sv"), path.name)
                )
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
