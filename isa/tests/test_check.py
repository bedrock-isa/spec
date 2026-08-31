import unittest
from dataclasses import replace
from pathlib import Path
import shutil
import tempfile

import yaml

from engine.allocation import forms_overlap
from engine.check import (
    BundleValidator,
    CheckService,
    ValidationRule,
    ValidationScope,
)
from engine.project import ArtifactSet, IsaProject


class CheckServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1]
        cls.project = IsaProject.load(cls.isa_root)

    def test_complete_current_tree_has_no_diagnostics(self) -> None:
        diagnostics = CheckService().check(self.project)
        self.assertEqual(list(diagnostics), [])
        self.assertFalse(diagnostics.has_errors)

    def test_check_service_accepts_independent_validation_rules(self) -> None:
        class RecordingRule(ValidationRule):
            def __init__(self) -> None:
                self.scope = None

            def validate(self, scope: ValidationScope):
                self.scope = scope
                return iter(())

        rule = RecordingRule()
        diagnostics = CheckService((rule,)).check(self.project, ("ADD",))

        self.assertEqual(list(diagnostics), [])
        self.assertIsNotNone(rule.scope)
        self.assertFalse(rule.scope.complete)
        self.assertEqual(rule.scope.selected[0].instruction.mnemonic, "ADD")

    def test_missing_companion_is_reported_without_stopping_validation(self) -> None:
        bundle = self.project.bundle("ADD")
        missing = replace(
            bundle,
            artifacts=ArtifactSet(
                semantics=bundle.artifacts.semantics.with_name("missing.sail"),
                description=bundle.artifacts.description,
            ),
        )

        diagnostics = list(BundleValidator().validate(missing, self.project))

        self.assertEqual([item.code for item in diagnostics], ["artifact.missing"])

    def test_missing_instruction_owned_sail_entry_is_reported(self) -> None:
        bundle = self.project.bundle("ADD")
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "semantics.sail"
            source.write_text("function execute_other() -> unit = ()\n")
            diagnostics = list(
                BundleValidator().validate(
                    replace(
                        bundle,
                        artifacts=replace(bundle.artifacts, semantics=source),
                    ),
                    self.project,
                )
            )

        self.assertEqual([item.code for item in diagnostics], ["sail.entry"])

    def test_missing_declared_directory_is_a_catalog_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "schemas").mkdir()
            (root / "instructions/definitions").mkdir(parents=True)
            for filename in (
                "instruction.yaml",
                "instruction-encodings.yaml",
                "model.yaml",
                "ea-mode-compact.yaml",
                "ea-mode-extended.yaml",
            ):
                shutil.copy2(
                    self.isa_root / "schemas" / filename,
                    root / "schemas" / filename,
                )
            for filename in ("field_types.yaml", "payload_types.yaml"):
                shutil.copy2(self.isa_root / filename, root / filename)
            shutil.copytree(self.isa_root / "ea/modes", root / "ea/modes")
            (root / "instructions/definitions/instructions.yaml").write_text(
                yaml.safe_dump({"instructions": ["MISSING"]}), encoding="utf-8"
            )
            (root / "model.yaml").write_text(
                "sail:\n  units: []\n", encoding="utf-8"
            )

            project = IsaProject.load(root)
            diagnostics = CheckService().check(project)

        self.assertEqual(
            [item.code for item in diagnostics], ["catalog.missing-directory"]
        )

    def test_constraints_separate_reclaimed_set_encoding(self) -> None:
        setcc = self.project.bundle("SETcc").encodings.forms[0]
        set_form = self.project.bundle("SET").encodings.forms[0]

        self.assertTrue(setcc.pattern.overlaps(set_form.pattern))
        self.assertFalse(forms_overlap(setcc, set_form))
        self.assertTrue(forms_overlap(replace(setcc, constraints=()), set_form))

if __name__ == "__main__":
    unittest.main()
