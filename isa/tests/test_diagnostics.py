import json
import unittest
from pathlib import Path

from engine.diagnostics import (
    Diagnostic,
    DiagnosticBag,
    RelatedLocation,
    Severity,
)


class DiagnosticBagTest(unittest.TestCase):
    def test_renders_text_and_json_with_related_location(self) -> None:
        bag = DiagnosticBag(
            [
                Diagnostic(
                    Severity.ERROR,
                    "allocation.overlap",
                    Path("left.yaml"),
                    "forms overlap",
                    ("encodings", "left", "pattern"),
                    (RelatedLocation(Path("right.yaml"), "conflicting form"),),
                )
            ]
        )

        self.assertTrue(bag.has_errors)
        self.assertIn("error[allocation.overlap]", bag.render_text())
        rendered = json.loads(bag.render_json())
        self.assertEqual(rendered[0]["path"], ["encodings", "left", "pattern"])
        self.assertEqual(rendered[0]["related"][0]["source"], "right.yaml")


if __name__ == "__main__":
    unittest.main()
