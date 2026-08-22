from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import validate_defs


class DescriptionTexValidationTests(unittest.TestCase):
    def test_generated_description_accepts_source_template(self):
        with tempfile.TemporaryDirectory() as directory:
            repository_root = Path(directory)
            definitions_root = repository_root / "isa" / "instructions" / "definitions"
            details = definitions_root / "instructions" / "RDPMC" / "details.tex"
            details.parent.mkdir(parents=True)
            details.with_suffix(".tex.in").write_text(
                "Generated instruction details.\n", encoding="utf-8"
            )

            with patch.object(validate_defs, "ROOT", definitions_root):
                self.assertEqual(validate_defs.validate_description_tex(details), [])

    def test_missing_description_and_template_remains_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            repository_root = Path(directory)
            definitions_root = repository_root / "isa" / "instructions" / "definitions"
            details = definitions_root / "instructions" / "MISSING" / "details.tex"

            with patch.object(validate_defs, "ROOT", definitions_root):
                errors = validate_defs.validate_description_tex(details)

            self.assertEqual(errors, [f"{details}: referenced TeX file does not exist"])


if __name__ == "__main__":
    unittest.main()
