from __future__ import annotations

from importlib import import_module
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from abi.c.model import CAbiProject
from engine.generation import ArtifactDefinition, ArtifactGenerationContext
from engine.workspace import SpecWorkspace
from engine.yaml_document import YamlDocumentLoader


ROOT = Path(__file__).resolve().parents[1]


class LlvmCAbiArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workspace = SpecWorkspace.load(ROOT)
        schema = YamlDocumentLoader().mapping(ROOT / "artifacts/schema.yaml")
        definition = ArtifactDefinition.load(
            ROOT / "artifacts/llvm-c-abi/artifact.yaml", schema
        )
        generated = (
            import_module("artifacts.llvm-c-abi.generator")
            .Generator(definition)
            .generate(ArtifactGenerationContext.create(cls.workspace, ROOT))
        )
        cls.generator_module = import_module("artifacts.llvm-c-abi.generator")
        project = cls.workspace.require_provider("abi.c")
        if not isinstance(project, CAbiProject):
            raise TypeError("workspace abi.c provider must be a CAbiProject")
        cls.project = project
        cls.catalog = generated.artifact("BedrockGenCABI.inc").content
        cls.calling_convention = generated.artifact("BedrockGenCallingConv.td").content
        cls.calling_convention_projection = (
            cls.generator_module._project_calling_convention(
                project, project.calling_convention, cls.workspace
            )
        )

    def test_catalog_families_have_authoritative_model_cardinality(self) -> None:
        compiler = shutil.which("clang++") or shutil.which("c++")
        if compiler is None:
            self.skipTest("no C++ compiler is available")
        convention = self.project.calling_convention
        namespace = self.project.namespaces["base"]
        register_classes = [
            self.project.register_classes.resolve(reference)
            for reference in convention.register_classes
        ]
        value_classes = [
            self.project.value_classes.resolve(reference)
            for reference in convention.value_classes
        ]
        promotions = [
            self.project.promotions.resolve(reference)
            for reference in convention.promotions
        ]
        helpers = list(namespace.runtime_helpers.values())
        memory_orders = list(namespace.memory_orders.values())
        atomic_lowerings = list(namespace.atomic_lowerings.values())
        expected = {
            "BEDROCK_C_TYPE": len(namespace.types),
            "BEDROCK_C_CALLING_CONVENTION": 1,
            "BEDROCK_C_REGISTER_CLASS": len(register_classes),
            "BEDROCK_C_ARGUMENT_REGISTER": sum(
                len(item.arguments) for item in register_classes
            ),
            "BEDROCK_C_RESULT_REGISTER": sum(
                len(item.results) for item in register_classes
            ),
            "BEDROCK_C_VALUE_CLASS": len(value_classes),
            "BEDROCK_C_VALUE_KIND": sum(len(item.kinds) for item in value_classes),
            "BEDROCK_C_LOCATION_POLICY": 2 * len(value_classes),
            "BEDROCK_C_PROMOTION": sum(len(item.source_kinds) for item in promotions),
            "BEDROCK_C_PRESERVATION_REGISTER": sum(
                len(item.registers) for item in convention.preservation
            ),
            "BEDROCK_C_RUNTIME_HELPER": len(helpers),
            "BEDROCK_C_RUNTIME_PARAMETER": sum(
                len(item.parameters) for item in helpers
            ),
            "BEDROCK_C_MEMORY_ORDER": len(memory_orders),
            "BEDROCK_C_MEMORY_ORDER_STEP": sum(
                len(sequence or ())
                for item in memory_orders
                for sequence in (item.load, item.store, item.thread_fence)
            ),
            "BEDROCK_C_ATOMIC_LOWERING": len(atomic_lowerings),
            "BEDROCK_C_ATOMIC_OPERATION": sum(
                len(item.c_operations) for item in atomic_lowerings
            ),
            "BEDROCK_C_ATOMIC_INSTRUCTION": sum(
                len(item.instructions) for item in atomic_lowerings
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "BedrockGenCABI.inc").write_text(self.catalog, encoding="utf-8")
            source = []
            for index, (macro, count) in enumerate(expected.items()):
                source.extend(
                    (
                        f"constexpr int family_{index} = 0",
                        f"#define {macro}(...) + 1",
                        '#include "BedrockGenCABI.inc"',
                        ";",
                        f"static_assert(family_{index} == {count});",
                        f"#undef {macro}",
                    )
                )
            source.extend(
                (
                    "#define BEDROCK_C_TYPE(id, ...) "
                    "constexpr bool seen_type_##id = true;",
                    "#define BEDROCK_C_REGISTER_CLASS(id, ...) "
                    "constexpr bool seen_register_class_##id = true;",
                    "#define BEDROCK_C_VALUE_CLASS(id) "
                    "constexpr bool seen_value_class_##id = true;",
                    "#define BEDROCK_C_RUNTIME_HELPER(id, ...) "
                    "constexpr bool seen_runtime_helper_##id = true;",
                    "#define BEDROCK_C_MEMORY_ORDER(id, ...) "
                    "constexpr bool seen_memory_order_##id = true;",
                    "#define BEDROCK_C_ATOMIC_LOWERING(id, ...) "
                    "constexpr bool seen_atomic_lowering_##id = true;",
                    '#include "BedrockGenCABI.inc"',
                )
            )
            source.extend(
                f"static_assert(seen_type_{item.id});"
                for item in namespace.types.values()
            )
            source.extend(
                f"static_assert(seen_register_class_{item.id});"
                for item in register_classes
            )
            source.extend(
                f"static_assert(seen_value_class_{item.id});" for item in value_classes
            )
            source.extend(
                f"static_assert(seen_runtime_helper_{item.id});" for item in helpers
            )
            source.extend(
                f"static_assert(seen_memory_order_{item.id});" for item in memory_orders
            )
            source.extend(
                f"static_assert(seen_atomic_lowering_{item.id});"
                for item in atomic_lowerings
            )
            source.append("int main() { return 0; }")
            path = root / "consume.cc"
            path.write_text("\n".join(source), encoding="utf-8")
            completed = subprocess.run(
                [compiler, "-std=c++17", "-fsyntax-only", str(path)],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_calling_convention_projection_preserves_owned_relations(self) -> None:
        convention = self.project.calling_convention
        value_classes = {
            self.project.value_classes.resolve(
                reference
            ).id: self.project.value_classes.resolve(reference)
            for reference in convention.value_classes
        }
        expected_returns = {}
        for value_id, value_class in value_classes.items():
            if value_id not in {
                rule.value_class
                for rule in self.calling_convention_projection.return_rules
            }:
                continue
            policy = value_class.result
            if policy.register_class is None:
                continue
            register_class = self.project.register_classes.resolve(
                policy.register_class
            )
            expected_returns[value_id] = tuple(
                self.workspace.resolve(reference).id
                for reference in register_class.results
            )
        actual_returns = {
            rule.value_class: rule.registers
            for rule in self.calling_convention_projection.return_rules
        }
        self.assertEqual(actual_returns, expected_returns)
        callee_saved = next(
            item
            for item in convention.preservation
            if item.disposition == "callee_saved"
        )
        self.assertEqual(
            self.calling_convention_projection.all_callee_saved,
            tuple(
                self.workspace.resolve(reference).id
                for reference in callee_saved.registers
            ),
        )

    def test_calling_convention_is_accepted_by_llvm_tablegen(self) -> None:
        tablegen = ROOT.parent / "llvm-project/build/bin/llvm-tblgen"
        if not tablegen.is_file():
            self.skipTest("workspace llvm-tblgen is unavailable")
        registers = {
            register
            for rule in self.calling_convention_projection.return_rules
            for register in rule.registers
        } | set(self.calling_convention_projection.all_callee_saved)
        wrapper = ['include "llvm/Target/Target.td"']
        wrapper.extend(
            f'def {register} : Register<"{register}">;'
            for register in sorted(registers)
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            generated = root / "BedrockGenCallingConv.td"
            generated.write_text(self.calling_convention, encoding="utf-8")
            wrapper.append(f'include "{generated}"')
            source = root / "consume.td"
            source.write_text("\n".join(wrapper), encoding="utf-8")
            completed = subprocess.run(
                [
                    str(tablegen),
                    "-I",
                    str(ROOT.parent / "llvm-project/llvm/include"),
                    "-print-records",
                    str(source),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
