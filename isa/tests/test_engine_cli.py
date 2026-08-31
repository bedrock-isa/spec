import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from engine.__main__ import main


class EngineCliTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1]

    def test_json_success_is_empty_array(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            result = main(
                [
                    "--isa-root",
                    str(self.isa_root),
                    "check",
                    "ADD",
                    "--format",
                    "json",
                ]
            )

        self.assertEqual(result, 0)
        self.assertEqual(json.loads(output.getvalue()), [])

    def test_unknown_target_is_reported_as_structured_diagnostic(self) -> None:
        errors = io.StringIO()
        with redirect_stderr(errors):
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
        diagnostics = json.loads(errors.getvalue())
        self.assertEqual(
            [item["code"] for item in diagnostics],
            ["project.lookup.unknown-instruction"],
        )
        self.assertEqual([item["severity"] for item in diagnostics], ["error"])

    def test_alloc_entries_uses_class_name_and_operator_space(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            result = main(
                [
                    "--isa-root",
                    str(self.isa_root),
                    "alloc",
                    "entries",
                    "extralong",
                    "--space",
                    "vector",
                    "--grep",
                    "VADD",
                    "--format",
                    "json",
                ]
            )

        self.assertEqual(result, 0)
        entries = json.loads(output.getvalue())
        self.assertTrue(entries)
        self.assertTrue(all(item["instruction"].endswith(".VADD") for item in entries))
        self.assertTrue(all("reclaimed" in item for item in entries))

    def test_alloc_holes_json_reports_namespace_scoped_blocks(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            result = main(
                [
                    "--isa-root",
                    str(self.isa_root),
                    "alloc",
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
        self.assertTrue(all(item["pattern"].startswith("1111111100") for item in document))

    def test_alloc_check_rejects_pattern_outside_class_namespace(self) -> None:
        errors = io.StringIO()
        with redirect_stderr(errors):
            result = main(
                [
                    "--isa-root",
                    str(self.isa_root),
                    "alloc",
                    "check",
                    "xxlong",
                    "0000",
                    "--format",
                    "json",
                ]
            )

        self.assertEqual(result, 1)
        diagnostic = json.loads(errors.getvalue())
        self.assertEqual(
            [item["code"] for item in diagnostic],
            ["allocation.candidate-outside-namespace"],
        )


if __name__ == "__main__":
    unittest.main()
