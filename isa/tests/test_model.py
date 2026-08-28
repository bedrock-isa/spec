import tempfile
import unittest
from pathlib import Path

from engine.extension import ExtensionMetadata, ExtensionSetCatalog
from engine.model import ModelCatalog


SCHEMA = Path(__file__).parents[1] / "schemas/model.yaml"


class ModelCatalogTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "schemas").mkdir()
        (self.root / "schemas/model.yaml").write_text(SCHEMA.read_text())
        (self.root / "extensions").mkdir()
        (self.root / "extensions/extensions.yaml").write_text(
            "extensions: [FP, FPTRANSA]\n"
        )
        self.extensions = {
            "FP": self._extension("FP"),
            "FPTRANSA": self._extension("FPTRANSA", ("FP",)),
        }
        for owner in ("base", *self.extensions):
            self._manifest(owner, "sail:\n  units: []\n")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _extension(
        self, extension_id: str, requires: tuple[str, ...] = ()
    ) -> ExtensionMetadata:
        root = self.root / "extensions" / extension_id
        root.mkdir()
        source = root / "extension.yaml"
        source.write_text(f"id: {extension_id}\nname: {extension_id}\n")
        return ExtensionMetadata(extension_id, extension_id, requires, (), source, root)

    def _source(self, owner: str, relative: str) -> None:
        root = self.root if owner == "base" else self.root / "extensions" / owner
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "$property\n"
            if path.suffix == ".sail"
            else "\\subsection{Topic}\nText.\n"
        )

    def _manifest(self, owner: str, text: str) -> None:
        root = self.root if owner == "base" else self.root / "extensions" / owner
        (root / "model.yaml").write_text(text)

    def _load(self) -> ModelCatalog:
        return ModelCatalog.load(
            self.root, ExtensionSetCatalog.load(self.root), self.extensions
        )

    def test_sail_dependencies_and_document_order_are_independent(self) -> None:
        self._source("base", "execution/semantics/types.sail")
        self._source("base", "execution/semantics/dispatch.sail")
        self._source("base", "execution/documents/overview.tex")
        self._source("base", "execution/documents/dispatch.tex")
        self._manifest(
            "base",
            "sail:\n"
            "  units:\n"
            "  - id: execution.dispatch\n"
            "    sources:\n"
            "    - execution/semantics/types.sail\n"
            "    - execution/semantics/dispatch.sail\n"
            "documents:\n"
            "  topics:\n"
            "  - id: execution.overview\n"
            "    source: execution/documents/overview.tex\n"
            "  - id: execution.dispatch\n"
            "    source: execution/documents/dispatch.tex\n"
            "    concept: execution.dispatch\n",
        )
        self._source("FP", "environment/semantics/environment.sail")
        self._source("FP", "environment/documents/environment.tex")
        self._manifest(
            "FP",
            "sail:\n"
            "  units:\n"
            "  - id: environment\n"
            "    sources: [environment/semantics/environment.sail]\n"
            "    requires: [base.execution.dispatch]\n"
            "documents:\n"
            "  topics:\n"
            "  - id: environment\n"
            "    source: environment/documents/environment.tex\n",
        )

        catalog = self._load()

        self.assertEqual(
            catalog.sail_order, ("base.execution.dispatch", "FP.environment")
        )
        self.assertEqual(
            catalog.document_order,
            (
                "base.execution.overview",
                "base.execution.dispatch",
                "FP.environment",
            ),
        )
        self.assertEqual(
            tuple(path.name for path in catalog.sail_units["base.execution.dispatch"].sources),
            ("types.sail", "dispatch.sail"),
        )
        self.assertEqual(
            catalog.document_topics["base.execution.dispatch"].concept,
            "execution.dispatch",
        )
        self.assertEqual(
            tuple(
                topic.reference
                for topic in catalog.selected_document_topics(
                    frozenset({"base", "FP"})
                )
            ),
            catalog.document_order,
        )

    def test_accepts_sail_only_and_document_only_manifests(self) -> None:
        self._source("base", "state/semantics/state.sail")
        self._manifest(
            "base",
            "sail:\n  units:\n  - id: state\n"
            "    sources: [state/semantics/state.sail]\n",
        )
        self._source("FP", "documents/overview.tex")
        self._manifest(
            "FP",
            "documents:\n  topics:\n  - id: overview\n"
            "    source: documents/overview.tex\n",
        )

        catalog = self._load()

        self.assertEqual(catalog.sail_order, ("base.state",))
        self.assertEqual(catalog.document_order, ("FP.overview",))

    def test_requires_every_owner_model_manifest(self) -> None:
        (self.root / "extensions/FP/model.yaml").unlink()

        with self.assertRaisesRegex(FileNotFoundError, "required model manifest"):
            self._load()

    def test_rejects_base_ownership_of_extension_source(self) -> None:
        self._source("FP", "semantics/environment.sail")
        self._manifest(
            "base",
            "sail:\n  units:\n  - id: stolen\n"
            "    sources: [extensions/FP/semantics/environment.sail]\n",
        )

        with self.assertRaisesRegex(ValueError, "owned by an extension"):
            self._load()

    def test_rejects_duplicate_source_ownership(self) -> None:
        self._source("base", "state/semantics/state.sail")
        self._manifest(
            "base",
            "sail:\n  units:\n"
            "  - id: state.left\n"
            "    sources: [state/semantics/state.sail]\n"
            "  - id: state.right\n"
            "    sources: [state/semantics/state.sail]\n",
        )

        with self.assertRaisesRegex(ValueError, "owned by both"):
            self._load()

    def test_rejects_document_with_more_than_one_topic_heading(self) -> None:
        self._source("base", "documents/topic.tex")
        (self.root / "documents/topic.tex").write_text(
            "\\subsection{First}\nA.\n\\subsection{Second}\nB.\n"
        )
        self._manifest(
            "base",
            "documents:\n  topics:\n  - id: topic\n"
            "    source: documents/topic.tex\n",
        )

        with self.assertRaisesRegex(ValueError, "exactly one section heading"):
            self._load()

    def test_explicit_cross_extension_dependency_is_ordered(self) -> None:
        self._source("FP", "environment/semantics/environment.sail")
        self._source("FPTRANSA", "approximation/semantics/contracts.sail")
        self._manifest(
            "FP",
            "sail:\n  units:\n  - id: environment\n"
            "    sources: [environment/semantics/environment.sail]\n"
            "    requires: [FPTRANSA.approximation]\n",
        )
        self._manifest(
            "FPTRANSA",
            "sail:\n  units:\n  - id: approximation\n"
            "    sources: [approximation/semantics/contracts.sail]\n",
        )

        self.assertEqual(
            self._load().sail_order,
            ("FPTRANSA.approximation", "FP.environment"),
        )

    def test_base_composition_unit_may_depend_on_an_extension(self) -> None:
        self._source("FP", "environment/semantics/environment.sail")
        self._source("base", "execution/semantics/dispatch.sail")
        self._manifest(
            "base",
            "sail:\n  units:\n  - id: execution\n"
            "    sources: [execution/semantics/dispatch.sail]\n"
            "    requires: [FP.environment]\n",
        )
        self._manifest(
            "FP",
            "sail:\n  units:\n  - id: environment\n"
            "    sources: [environment/semantics/environment.sail]\n",
        )

        catalog = self._load()

        self.assertEqual(catalog.sail_order, ("FP.environment", "base.execution"))

    def test_rejects_sail_dependency_cycle(self) -> None:
        self._source("FP", "semantics/left.sail")
        self._source("FP", "semantics/right.sail")
        self._manifest(
            "FP",
            "sail:\n  units:\n"
            "  - id: left\n"
            "    sources: [semantics/left.sail]\n"
            "    requires: [FP.right]\n"
            "  - id: right\n"
            "    sources: [semantics/right.sail]\n"
            "    requires: [FP.left]\n",
        )

        with self.assertRaisesRegex(ValueError, "FP.left -> FP.right -> FP.left"):
            self._load()


if __name__ == "__main__":
    unittest.main()
