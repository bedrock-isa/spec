import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from engine.generation import ArtifactGeneratorRegistry, ArtifactWriter
from engine.workspace import SpecWorkspace


class InstructionSemanticsContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workspace = SpecWorkspace.load(Path(__file__).parents[1])
        cls.sail = shutil.which("sail")
        if cls.sail is None:
            raise RuntimeError("Sail executable is required for semantic tests")

    def test_signed_scalar_results_are_sign_extended(self) -> None:
        signed_results = (
            "ABS",
            "DIVS",
            "MODS",
            "DIVMODS",
            "MINS",
            "MAXS",
            "SAR",
            "EXTSW",
            "EXTSL",
            "EXTSQ",
        )
        predicates = " &\n  ".join(
            f"register_result_extension(Op_{mnemonic}) == RegisterSignExtend"
            for mnemonic in signed_results
        )
        harness = (
            "function signed_scalar_results_are_sign_extended() -> bool =\n"
            f"  {predicates}\n"
        )
        script = "signed_scalar_results_are_sign_extended()\n:run\n:quit\n"

        with tempfile.TemporaryDirectory(dir=self.workspace.root) as directory:
            output = Path(directory)
            registry = ArtifactGeneratorRegistry.discover(self.workspace)
            artifacts = registry.generate("sail-model", self.workspace, output)
            ArtifactWriter().write(artifacts, output)
            harness_path = output / "signed_result_contract.sail"
            script_path = output / "signed_result_contract.is"
            cache_path = output / "sail_smt_cache"
            harness_path.write_text(harness, encoding="utf-8")
            script_path.write_text(script, encoding="utf-8")

            listed = subprocess.run(
                (
                    self.sail,
                    "--project",
                    str(output / "bedrock-model.sail_project"),
                    "--all-modules",
                    "--list-files",
                    "--memo-z3-path",
                    str(cache_path),
                ),
                cwd=output,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(listed.returncode, 0, listed.stderr)
            sources = tuple(listed.stdout.split())
            self.assertTrue(sources)

            completed = subprocess.run(
                (
                    self.sail,
                    "-i",
                    *sources,
                    str(harness_path),
                    "--is",
                    str(script_path),
                    "--memo-z3-path",
                    str(cache_path),
                ),
                cwd=output,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                completed.stdout.splitlines()[-1],
                "Result = true",
            )


if __name__ == "__main__":
    unittest.main()
