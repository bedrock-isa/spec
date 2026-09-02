import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from engine.__main__ import main
from engine.encoding_space import EncodingSpaceAnalyzer
from engine.encoding_architecture import operator_space
from engine.project import IsaProject
from engine.workspace import SpecWorkspace


class EngineCliTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1] / "isa"
        cls.project = IsaProject.load(cls.isa_root)
        cls.workspace = SpecWorkspace.create(
            cls.isa_root.parent,
            {"isa": cls.project},
        )

    def test_json_success_is_empty_array(self) -> None:
        output = io.StringIO()
        errors = io.StringIO()
        selected = self.project.select()[0]
        with redirect_stdout(output), redirect_stderr(errors):
            result = main(
                [
                    "--isa-root",
                    str(self.isa_root),
                    "check",
                    selected.instruction.mnemonic,
                    "--format",
                    "json",
                ]
            )

        self.assertEqual(result, 0)
        self.assertEqual(json.loads(output.getvalue()), [])
        self.assertEqual(errors.getvalue(), "")

    def test_verbose_keeps_error_json_separate_from_logs(self) -> None:
        output = io.StringIO()
        errors = io.StringIO()
        with (
            patch.object(SpecWorkspace, "load", return_value=self.workspace),
            redirect_stdout(output),
            redirect_stderr(errors),
        ):
            result = main(
                [
                    "--verbose",
                    "--isa-root",
                    str(self.isa_root),
                    "check",
                    "DOESNOTEXIST",
                    "--format",
                    "json",
                ]
            )

        self.assertEqual(result, 1)
        diagnostics = json.loads(output.getvalue())
        self.assertEqual(
            [item["code"] for item in diagnostics],
            ["project.lookup.unknown-instruction"],
        )
        self.assertIn("[engine] INFO check failed", errors.getvalue())
        self.assertNotIn('"severity"', errors.getvalue())

    def test_debug_reports_caught_exception_traceback(self) -> None:
        output = io.StringIO()
        errors = io.StringIO()
        with (
            patch.object(SpecWorkspace, "load", return_value=self.workspace),
            redirect_stdout(output),
            redirect_stderr(errors),
        ):
            result = main(
                [
                    "--debug",
                    "--isa-root",
                    str(self.isa_root),
                    "check",
                    "DOESNOTEXIST",
                    "--format",
                    "json",
                ]
            )

        self.assertEqual(result, 1)
        self.assertEqual(len(json.loads(output.getvalue())), 1)
        self.assertIn("Traceback (most recent call last)", errors.getvalue())

    def test_unknown_target_is_reported_as_structured_diagnostic(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            result = main(
                [
                    "--isa-root",
                    str(self.isa_root),
                    "check",
                    "DOESNOTEXIST",
                    "--format",
                    "json",
                ]
            )

        self.assertEqual(result, 1)
        diagnostics = json.loads(output.getvalue())
        self.assertEqual(
            [item["code"] for item in diagnostics],
            ["project.lookup.unknown-instruction"],
        )
        self.assertEqual([item["severity"] for item in diagnostics], ["error"])

    def test_encoding_space_entries_uses_class_name_and_operator_space(self) -> None:
        selected = EncodingSpaceAnalyzer().entries(
            self.project, "extralong", space="vector"
        )[0]
        output = io.StringIO()
        with redirect_stdout(output):
            result = main(
                [
                    "--isa-root",
                    str(self.isa_root),
                    "encoding-space",
                    "entries",
                    "extralong",
                    "--space",
                    "vector",
                    "--grep",
                    selected.mnemonic,
                    "--format",
                    "json",
                ]
            )

        self.assertEqual(result, 0)
        entries = json.loads(output.getvalue())
        self.assertTrue(entries)
        self.assertTrue(
            all(item["instruction"].endswith(f".{selected.mnemonic}") for item in entries)
        )
        self.assertTrue(all("reclaimed" in item for item in entries))

    def test_encoding_space_holes_json_reports_namespace_scoped_blocks(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            result = main(
                [
                    "--isa-root",
                    str(self.isa_root),
                    "encoding-space",
                    "holes",
                    "xxlong",
                    "--space",
                    "vector",
                    "--limit",
                    "2",
                    "--format",
                    "json",
                ]
            )

        document = json.loads(output.getvalue())
        self.assertEqual(result, 0)
        self.assertEqual(len(document), 2)
        prefix = operator_space("xxlong", "vector").prefix.replace("x", "?")
        self.assertTrue(all(item["pattern"].startswith(prefix) for item in document))

    def test_encoding_space_check_rejects_pattern_outside_class_namespace(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            result = main(
                [
                    "--isa-root",
                    str(self.isa_root),
                    "encoding-space",
                    "check",
                    "xxlong",
                    "0000",
                    "--format",
                    "json",
                ]
            )

        self.assertEqual(result, 1)
        diagnostic = json.loads(output.getvalue())
        self.assertEqual(
            [item["code"] for item in diagnostic],
            ["encoding-space.candidate-outside-namespace"],
        )


if __name__ == "__main__":
    unittest.main()
