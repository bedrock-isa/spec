import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from engine.generation import ArtifactGeneratorRegistry
from engine.project import IsaProject
from engine.workspace import SpecWorkspace


class SpecificationArtifactsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = Path(__file__).parents[1]
        cls.workspace = SpecWorkspace.load(cls.repository)
        cls.project = cls.workspace.require_provider("isa")
        if not isinstance(cls.project, IsaProject):
            raise TypeError("workspace isa provider must be an IsaProject")
        cls.registry = ArtifactGeneratorRegistry.discover(cls.workspace)

    def test_workspace_entity_dependencies_are_uniform_and_resolvable(self) -> None:
        for provider in self.workspace.providers.values():
            for dependency in provider.entity_dependencies():
                provider.entities.resolve(dependency.source)
                self.workspace.resolve(dependency.target)

    def test_c_target_headers_cover_the_complete_interface_catalog(self) -> None:
        generator = self.registry.generator("c-target-headers")
        interface = self.workspace.require_provider("interfaces.c")
        projection = generator.project(interface)
        generated = self.registry.generate(
            "c-target-headers", self.workspace, self.repository / "output"
        )
        expected_builtins = {
            intrinsic.clang_builtin for intrinsic in interface.intrinsics.values()
        }
        projected_builtins = {
            intrinsic.builtin_spelling
            for group in projection.groups
            for intrinsic in group.intrinsics
        }

        self.assertEqual(projected_builtins, expected_builtins)
        compiler = shutil.which("clang") or shutil.which("cc")
        if compiler is None:
            self.skipTest("no C preprocessor is available")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for artifact in generated.artifacts:
                path = root / artifact.relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(artifact.content, encoding="utf-8")
            source = root / "consume.c"
            source.write_text(
                "\n".join(
                    f"#include <{group.path.relative_to('include').as_posix()}>"
                    for group in projection.groups
                ),
                encoding="utf-8",
            )
            completed = subprocess.run(
                (
                    compiler,
                    "-E",
                    "-x",
                    "c",
                    "-I",
                    str(root / "include"),
                    str(source),
                ),
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_reference_graph_is_a_standalone_workspace_visualization(self) -> None:
        def local(reference) -> str:
            return ".".join(
                (reference.owner, *reference.path, reference.element)
            )

        generator = self.registry.generator("reference-graph")
        generated = self.registry.generate(
            "reference-graph", self.workspace, self.repository / "output"
        )
        graph = json.loads(
            generated.artifact(generator.definition.outputs["data"]).content
        )

        expected_nodes = {
            f"{domain}:{local(reference)}"
            for domain, provider in self.workspace.providers.items()
            for reference in provider.entities.references
        }
        self.assertEqual(graph["node_count"], len(expected_nodes))
        self.assertEqual(graph["link_count"], len(graph["links"]))
        nodes = {node["id"]: node for node in graph["nodes"]}
        self.assertEqual(set(nodes), expected_nodes)
        self.assertTrue(
            all(
                "anchor" not in node and "latex_label" not in node
                for node in nodes.values()
            )
        )

        expected_occurrences: dict[tuple[str, str, str], int] = {}
        for domain, provider in self.workspace.providers.items():
            for dependency in provider.entity_dependencies():
                source = f"{domain}:{local(dependency.source)}"
                target = (
                    f"{dependency.target.domain}:"
                    f"{local(dependency.target.local)}"
                )
                if source == target:
                    continue
                key = (source, target, dependency.kind)
                expected_occurrences[key] = expected_occurrences.get(key, 0) + 1
        projected_occurrences = {
            (link["source"], link["target"], link["kind"]): link["weight"]
            for link in graph["links"]
        }
        self.assertEqual(projected_occurrences, expected_occurrences)

if __name__ == "__main__":
    unittest.main()
