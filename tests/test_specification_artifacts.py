import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from abi.c.model import CAbiProject
from abi.c.model.call_layout import Argument, Call, ReturnValue, default_rules, layout_call
from abi.elf.model import ElfAbiProject
from engine.generation import ArtifactGeneratorRegistry
from engine.project import IsaProject
from engine.reference import QualifiedReference
from engine.workspace import SpecWorkspace
from interfaces.c.model import CInterfaceProject
from interfaces.c.model.naming import intrinsic_group_header


class SpecificationArtifactsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = Path(__file__).parents[1]
        cls.workspace = SpecWorkspace.load(cls.repository)
        cls.project = cls.workspace.require_provider("isa")
        if not isinstance(cls.project, IsaProject):
            raise TypeError("workspace isa provider must be an IsaProject")
        cls.registry = ArtifactGeneratorRegistry.discover(cls.workspace)

    def test_workspace_exposes_typed_source_owned_domains(self) -> None:
        self.assertIsInstance(
            self.workspace.require_provider("abi.elf"), ElfAbiProject
        )
        self.assertIsInstance(
            self.workspace.require_provider("abi.c"), CAbiProject
        )
        self.assertIsInstance(
            self.workspace.require_provider("interfaces.c"), CInterfaceProject
        )

    def test_workspace_entity_dependencies_are_uniform_and_resolvable(self) -> None:
        for provider in self.workspace.providers.values():
            for dependency in provider.entity_dependencies():
                provider.entities.resolve(dependency.source)
                self.workspace.resolve(dependency.target)

    def test_workspace_resolves_qualified_interface_references(self) -> None:
        intrinsic = self.workspace.resolve(
            "interfaces.c:FP.intrinsics.fpu.fclass_f32"
        )
        interface_type = self.workspace.resolve(
            "interfaces.c:base.types.sysreg.control_register"
        )

        self.assertEqual(intrinsic.id, "fclass_f32")
        self.assertEqual(
            intrinsic.operation,
            QualifiedReference.parse("isa:FP.instructions.FCLASS"),
        )
        self.assertEqual(interface_type.id, "control_register")

    def test_c_interface_group_header_uses_its_declared_group(self) -> None:
        self.assertEqual(intrinsic_group_header("sysreg"), "bedrocksysregintrin.h")

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
        self.assertEqual(
            {group.path for group in projection.groups},
            {
                Path("include") / intrinsic_group_header(group.id)
                for group in interface.intrinsic_groups.values()
            },
        )

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
                    f"#include <{intrinsic_group_header(group.id)}>"
                    for group in interface.intrinsic_groups.values()
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
        generated = self.registry.generate(
            "reference-graph", self.workspace, self.repository / "output"
        )
        graph = json.loads(
            generated.artifact("reference/graph.json").content
        )

        interface = self.workspace.require_provider("interfaces.c")
        elf = self.workspace.require_provider("abi.elf")
        c_abi = self.workspace.require_provider("abi.c")
        expected_nodes = (
            len(self.project.entities.references)
            + len(elf.entities.references)
            + len(c_abi.entities.references)
            + len(interface.entities.references)
        )
        self.assertEqual(graph["node_count"], expected_nodes)
        self.assertEqual(graph["link_count"], len(graph["links"]))
        nodes = {node["id"]: node for node in graph["nodes"]}
        self.assertEqual(
            nodes["isa:base.instructions.ADD"]["label"],
            "ADD",
        )
        self.assertNotIn("anchor", nodes["isa:base.instructions.ADD"])
        self.assertNotIn("latex_label", nodes["isa:base.instructions.ADD"])
        self.assertEqual(
            nodes["isa:base.instructions.ADD"]["source"],
            "isa/instructions/definitions/ADD/instruction.yaml",
        )
        self.assertTrue(all("source" in node for node in nodes.values()))

        lowering = next(
            link
            for link in graph["links"]
            if link["source"]
            == "interfaces.c:FP.intrinsics.fpu.fclass_f32"
            and link["target"] == "isa:FP.instructions.FCLASS"
        )
        self.assertEqual(lowering["kind"], "intrinsic-instruction")
        self.assertGreaterEqual(lowering["weight"], 1)
        self.assertTrue(
            any(
                link["source"] == "isa:base.instructions.ADD"
                and link["target"] == "isa:base.field_types.Rn"
                and link["kind"] == "instruction-field-type"
                for link in graph["links"]
            )
        )
        self.assertTrue(
            any(
                link["source"] == "isa:FP.instructions.FADD"
                and link["target"]
                == "isa:FP.cpuid.EXTENSIONS.DIRECTORY.FEATURES.FP"
                and link["kind"] == "requires-cpuid"
                for link in graph["links"]
            )
        )
        self.assertTrue(
            any(
                link["source"] == "isa:base.ea.modes.compact.register"
                and link["target"] == "isa:base.field_types.EA"
                and link["kind"] == "ea-profile-type"
                for link in graph["links"]
            )
        )
        self.assertTrue(
            any(
                link["source"] == "isa:FP.cpuid.EXTENSIONS"
                and link["target"] == "isa:base.cpuid.EXTENSIONS"
                and link["kind"] == "cpuid-class-overlay"
                for link in graph["links"]
            )
        )
        self.assertTrue(
            any(
                link["source"] == "isa:base.registers.SPECIAL.PC"
                and link["target"] == "isa:base.registers.CONTROL.BOOTPC"
                and link["kind"] == "register-reset-source"
                for link in graph["links"]
            )
        )
        self.assertTrue(
            all(
                link["source"] in nodes and link["target"] in nodes
                for link in graph["links"]
            )
        )

    def test_c_abi_call_layout_uses_resolved_calling_convention(self) -> None:
        call = Call(
            (
                Argument("tag", "u64"),
                Argument("wide", "i128"),
                Argument("factor", "f64"),
            ),
            ReturnValue("aggregate", 24),
        )

        self.assertEqual(
            layout_call(call, default_rules()),
            {
                "sret": "R0",
                "return_location": "R0",
                "arguments": [
                    {
                        "name": "tag",
                        "source_kind": "u64",
                        "effective_kind": "u64",
                        "mode": "value",
                        "location": "R1",
                    },
                    {
                        "name": "wide",
                        "source_kind": "i128",
                        "effective_kind": "i128",
                        "mode": "value",
                        "location": "R3:R2",
                    },
                    {
                        "name": "factor",
                        "source_kind": "f64",
                        "effective_kind": "f64",
                        "mode": "value",
                        "location": "F0",
                    },
                ],
                "stack_size": 0,
            },
        )

if __name__ == "__main__":
    unittest.main()
