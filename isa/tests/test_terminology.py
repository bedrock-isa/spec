import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from engine.check import TerminologyValidator
from engine.extension import ExtensionSetCatalog
from engine.reference import Reference
from engine.semantic_text import SemanticText
from engine.terminology import TermCatalog


class TermCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1]
        cls.catalog = TermCatalog.load(
            cls.isa_root, ExtensionSetCatalog.load(cls.isa_root)
        )

    def test_loads_owner_local_groups_and_terms_into_shared_indexes(self) -> None:
        with self.fixture() as directory:
            root = Path(directory)
            terms_root = root / "terminology/groups/sample/terms"
            self.write_yaml(terms_root / "terms.yaml", {"terms": ["address"]})
            self.write_yaml(
                terms_root / "address/term.yaml",
                {
                    "id": "address",
                    "display": {"canonical": "sample address"},
                    "abbreviation": {"canonical": "SA"},
                    "definition": "A sample address.",
                },
            )

            catalog = TermCatalog.load(root, ExtensionSetCatalog.load(root))

        group = catalog.references.groups[Reference.parse("base.term_groups.sample")]
        term = catalog.references.terms[Reference.parse("base.terms.address")]
        self.assertEqual(set(group.terms), {"address"})
        self.assertIsInstance(term.definition, SemanticText)
        self.assertEqual(term.abbreviation.canonical, "SA")
        self.assertEqual(
            catalog.spellings["sample address"][0].reference, term.reference
        )

    def test_validator_reports_inventory_and_unknown_definition_references(
        self,
    ) -> None:
        with self.fixture() as directory:
            root = Path(directory)
            terms_root = root / "terminology/groups/sample/terms"
            self.write_yaml(terms_root / "terms.yaml", {"terms": ["known", "missing"]})
            self.write_yaml(
                terms_root / "known/term.yaml",
                {
                    "id": "known",
                    "display": {"canonical": "known term"},
                    "definition": "See (:term:base.terms.unknown:).",
                },
            )

            catalog = TermCatalog.load(root, ExtensionSetCatalog.load(root))
            codes = [item.code for item in TerminologyValidator().validate(catalog)]

        self.assertCountEqual(
            codes,
            (
                "terminology.term.missing-directory",
                "terminology.definition.unknown-term",
            ),
        )

    def test_validator_reports_spelling_conflicts_and_broader_cycles(self) -> None:
        with self.fixture() as directory:
            root = Path(directory)
            terms_root = root / "terminology/groups/sample/terms"
            self.write_yaml(terms_root / "terms.yaml", {"terms": ["first", "second"]})
            for term_id, broader in (("first", "second"), ("second", "first")):
                self.write_yaml(
                    terms_root / term_id / "term.yaml",
                    {
                        "id": term_id,
                        "display": {
                            "canonical": (
                                "same-term" if term_id == "first" else "same term"
                            )
                        },
                        "definition": f"The {term_id} term.",
                        "relations": {"broader": [f"base.terms.{broader}"]},
                    },
                )

            catalog = TermCatalog.load(root, ExtensionSetCatalog.load(root))
            codes = [item.code for item in TerminologyValidator().validate(catalog)]

        self.assertCountEqual(
            codes,
            (
                "terminology.spelling.conflict",
                "terminology.relation.broader-cycle",
            ),
        )

    def fixture(self):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "schemas").mkdir()
        (root / "extensions").mkdir()
        for schema in ("terminology-group.yaml", "term.yaml"):
            shutil.copy2(self.isa_root / "schemas" / schema, root / "schemas" / schema)
        self.write_yaml(root / "extensions/extensions.yaml", {"extensions": []})
        self.write_yaml(root / "terminology/groups/groups.yaml", {"groups": ["sample"]})
        self.write_yaml(
            root / "terminology/groups/sample/group.yaml",
            {"id": "sample", "title": "Sample"},
        )
        return temporary

    @staticmethod
    def write_yaml(path: Path, document: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            yaml.safe_dump(document, sort_keys=False, width=120), encoding="utf-8"
        )


if __name__ == "__main__":
    unittest.main()
