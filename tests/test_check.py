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
from engine.encoding import (
    AllowedOperandConstraint,
    EncodingForm,
    ExcludedOperandConstraint,
    FieldBinding,
)
from engine.encoding_metasyntax import EncodingMetasyntax
from engine.instruction_metasyntax import InstructionMetasyntax
from engine.project import ArtifactSet, IsaProject
from engine.reference import Reference


class CheckServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1] / "isa"
        cls.project = IsaProject.load(cls.isa_root)

    def test_check_service_accepts_independent_validation_rules(self) -> None:
        class RecordingRule(ValidationRule):
            def __init__(self) -> None:
                self.scope = None

            def validate(self, scope: ValidationScope):
                self.scope = scope
                return iter(())

        rule = RecordingRule()
        selected = self.project.select()[0]
        diagnostics = CheckService((rule,)).check(
            self.project, (selected.reference,)
        )

        self.assertEqual(list(diagnostics), [])
        self.assertIsNotNone(rule.scope)
        self.assertFalse(rule.scope.complete)
        self.assertEqual(rule.scope.selected, (selected,))

    def test_missing_companion_is_reported_without_stopping_validation(self) -> None:
        bundle = self.project.select()[0]
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
        bundle = self.project.select()[0]
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

    def test_operand_constraints_separate_overlapping_raw_encodings(self) -> None:
        field = FieldBinding(
            "a",
            "selector",
            Reference.parse("base.field_types.SYNTHETIC"),
        )
        raw = EncodingForm(
            "raw",
            EncodingMetasyntax.parse("aa"),
            InstructionMetasyntax.parse("SYN"),
            fields=(field,),
        )
        constrained = replace(
            raw,
            id="constrained",
            constraints=(
                ExcludedOperandConstraint(
                    role="selector",
                    reason="reserved",
                    values=(0,),
                ),
            ),
        )
        reserved = replace(
            raw,
            id="reserved",
            constraints=(
                AllowedOperandConstraint(
                    role="selector",
                    reason="reserved",
                    values=(0,),
                ),
            ),
        )

        self.assertTrue(raw.pattern.overlaps(reserved.pattern))
        self.assertFalse(forms_overlap(constrained, reserved))
        self.assertTrue(forms_overlap(raw, reserved))

if __name__ == "__main__":
    unittest.main()
