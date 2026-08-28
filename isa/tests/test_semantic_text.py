import unittest
from pathlib import Path

from engine.semantic_text import (
    EntityReferenceText,
    LiteralText,
    SemanticText,
    SemanticTextError,
    TermForm,
    TermReferenceText,
    TextOrigin,
)


class SemanticTextTest(unittest.TestCase):
    def setUp(self) -> None:
        self.origin = TextOrigin(Path("term.yaml"), ("definition",))

    def test_plain_text_is_one_literal_part(self) -> None:
        text = SemanticText.parse("plain text", origin=self.origin)

        self.assertEqual(text.parts, (LiteralText("plain text", 0, 10),))
        self.assertEqual(text.dependencies, ())

    def test_parses_entity_and_term_references(self) -> None:
        raw = (
            "The (:term:base.terms.effective_address|short:) is reported by "
            "(:ref:base.instructions.SEGLEA:)."
        )
        text = SemanticText.parse(raw, origin=self.origin)

        term = next(part for part in text.parts if isinstance(part, TermReferenceText))
        entity = next(
            part for part in text.parts if isinstance(part, EntityReferenceText)
        )
        self.assertEqual(str(term.reference), "base.terms.effective_address")
        self.assertIs(term.form, TermForm.SHORT)
        self.assertEqual(str(entity.reference), "base.instructions.SEGLEA")
        self.assertEqual(
            tuple(map(str, text.dependencies)),
            ("base.terms.effective_address", "base.instructions.SEGLEA"),
        )

    def test_non_reserved_parenthesis_colon_text_remains_literal(self) -> None:
        raw = "f(x): value and (: note)"

        self.assertEqual(
            SemanticText.parse(raw, origin=self.origin).parts,
            (LiteralText(raw, 0, len(raw)),),
        )

    def test_rejects_unknown_unterminated_and_modified_ref_escapes(self) -> None:
        cases = (
            ("(:reff:base.instructions.ADD:)", "unknown semantic escape kind"),
            ("(:ref:base.instructions.ADD", "unterminated semantic escape"),
            ("(:ref:base.instructions.ADD|name:)", "do not accept a modifier"),
            ("(:term:base.terms.address|many:)", "unknown term form"),
        )

        for raw, message in cases:
            with self.subTest(raw=raw), self.assertRaisesRegex(
                SemanticTextError, message
            ):
                SemanticText.parse(raw, origin=self.origin)


if __name__ == "__main__":
    unittest.main()
