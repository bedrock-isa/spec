import json
import re
import tempfile
import unittest
from pathlib import Path

from abi.c.model import CAbiProject
from abi.c.model.call_layout import Argument, Call, ReturnValue, default_rules, layout_call
from abi.elf.model import ElfAbiProject
from engine.generation import ArtifactGeneratorRegistry
from engine.project import IsaProject
from engine.workspace import SpecWorkspace
from interfaces.c.model import CInterfaceProject
from interfaces.c.model.naming import intrinsic_group_header


class SpecificationArtifactsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = Path(__file__).parents[2]
        cls.project = IsaProject.load(cls.repository / "isa")
        cls.workspace = SpecWorkspace.from_isa(cls.project)
        cls.registry = ArtifactGeneratorRegistry.discover(cls.workspace)

    def test_workspace_exposes_typed_source_owned_domains(self) -> None:
        self.assertEqual(
            tuple(self.workspace.providers),
            ("isa", "abi.elf", "abi.c", "interfaces.c"),
        )
        self.assertIsInstance(
            self.workspace.require_provider("abi.elf"), ElfAbiProject
        )
        self.assertIsInstance(
            self.workspace.require_provider("abi.c"), CAbiProject
        )
        self.assertIsInstance(
            self.workspace.require_provider("interfaces.c"), CInterfaceProject
        )

    def test_workspace_resolves_qualified_interface_references(self) -> None:
        intrinsic = self.workspace.resolve(
            "interfaces.c:FP.intrinsics.fpu.fclass_f32"
        )
        interface_type = self.workspace.resolve(
            "interfaces.c:base.types.sysreg.control_register"
        )

        self.assertEqual(intrinsic.id, "fclass_f32")
        self.assertEqual(
            str(intrinsic.operation), "isa:FP.instructions.FCLASS"
        )
        self.assertEqual(interface_type.id, "control_register")

    def test_c_interface_catalog_has_strict_grouped_inventory(self) -> None:
        project = self.workspace.require_provider("interfaces.c")

        self.assertEqual(tuple(project.extensions), ("FP", "FPTRANSA", "VECTOR"))
        self.assertEqual(intrinsic_group_header("sysreg"), "bedrocksysregintrin.h")

    def test_c_target_headers_cover_the_complete_interface_catalog(self) -> None:
        generated = self.registry.generate(
            "c-target-headers", self.workspace, self.repository / "output"
        )
        interface = self.workspace.require_provider("interfaces.c")
        expected_builtins = {
            intrinsic.clang_builtin for intrinsic in interface.intrinsics.values()
        }
        actual_builtins: set[str] = set()
        for group in interface.intrinsic_groups.values():
            header = generated.artifact(
                f"include/{intrinsic_group_header(group.id)}"
            ).content
            actual_builtins.update(
                re.findall(r"__builtin_bedrock_[a-zA-Z0-9_]+", header)
            )

        self.assertEqual(actual_builtins, expected_builtins)
        self.assertIn(
            "__BEDROCK_CR_UINFO",
            generated.artifact("include/bedrocksysregintrin.h").content,
        )

    def test_reference_documents_are_first_class_artifacts(self) -> None:
        expected = {
            "elf-abi": "tex/bedrock-elf-abi.tex",
            "c-abi": "tex/bedrock-c-abi.tex",
            "c-target-intrinsics": "tex/bedrock-target-intrinsics.tex",
        }
        with tempfile.TemporaryDirectory() as directory:
            for artifact_id, output in expected.items():
                with self.subTest(artifact=artifact_id):
                    generated = self.registry.generate(
                        artifact_id, self.workspace, directory
                    )
                    content = generated.artifact(output).content
                    self.assertTrue(content.strip())
                    self.assertNotIn("BedrockGenerated", content)
                    if artifact_id == "elf-abi":
                        self.assertIn("symbol + addend - next\\_pc", content)
                    if artifact_id == "c-abi":
                        self.assertIn("AFENCE; load; AFENCE", content)

    def test_reference_graph_is_a_standalone_workspace_visualization(self) -> None:
        generated = self.registry.generate(
            "reference-graph", self.workspace, self.repository / "output"
        )
        graph = json.loads(
            generated.artifact("reference/graph.json").content
        )
        view = generated.artifact("reference/graph.html").content

        interface = self.workspace.require_provider("interfaces.c")
        interface_entities = sum(
            len(index)
            for index in (
                interface.type_groups,
                interface.intrinsic_groups,
                interface.utility_groups,
                interface.types,
                interface.intrinsics,
                interface.utilities,
            )
        )
        elf = self.workspace.require_provider("abi.elf")
        c_abi = self.workspace.require_provider("abi.c")
        expected_nodes = (
            len(self.project.entities.references)
            + len(elf.entities.references)
            + len(c_abi.entities.references)
            + interface_entities
        )
        self.assertEqual(graph["schema_version"], 1)
        self.assertEqual(graph["node_count"], expected_nodes)
        self.assertEqual(graph["link_count"], len(graph["links"]))
        self.assertIn('<canvas id="graph"></canvas>', view)
        self.assertIn('id="graph-data"', view)
        self.assertNotIn("mkdocs", view.lower())

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

        lowering = next(
            link
            for link in graph["links"]
            if link["source"]
            == "interfaces.c:FP.intrinsics.fpu.fclass_f32"
            and link["target"] == "isa:FP.instructions.FCLASS"
        )
        self.assertEqual(lowering["kind"], "structured")
        self.assertGreaterEqual(lowering["weight"], 1)
        abi_topic_edge = next(
            link
            for link in graph["links"]
            if link["source"] == "abi.elf:base.document_topics.RELOCATIONS"
            and link["target"]
            == "abi.elf:base.relocations.R_BEDROCK_CALL32S"
        )
        self.assertEqual(abi_topic_edge["kind"], "structured")
        self.assertTrue(
            all(
                link["source"] in nodes and link["target"] in nodes
                for link in graph["links"]
            )
        )

        topics = graph["topic_connectivity"]
        self.assertEqual(topics["metric"], "tf-idf-cosine")
        self.assertEqual(topics["link_count"], len(topics["links"]))
        self.assertTrue(topics["links"])
        self.assertTrue(
            all(
                nodes[link["source"]]["kind"] == "topic"
                and nodes[link["target"]]["kind"] == "topic"
                and link["shared_reference_count"] >= 2
                and link["evidence"]
                for link in topics["links"]
                if link["kind"] == "similarity"
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
