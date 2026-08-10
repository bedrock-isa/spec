PYTHON ?= python3
LATEXMK ?= latexmk
PANDOC ?= pandoc
LATEXPAND ?= latexpand
MKDOCS ?= mkdocs

.PHONY: docs docs-pdf docs-site sail-docs

docs:
	$(PYTHON) isa/tools/compile_documents.py --format all --latexmk "$(LATEXMK)" --pandoc "$(PANDOC)" --latexpand "$(LATEXPAND)" --mkdocs "$(MKDOCS)"

docs-pdf:
	$(PYTHON) isa/tools/compile_documents.py --format pdf --latexmk "$(LATEXMK)"

docs-site:
	$(PYTHON) isa/tools/compile_documents.py --format site --latexmk "$(LATEXMK)" --pandoc "$(PANDOC)" --latexpand "$(LATEXPAND)" --mkdocs "$(MKDOCS)"

sail-docs:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) sail/tools/build_docs.py --build-dir build/sail-doc
