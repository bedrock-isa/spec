PYTHON ?= python3
LATEXMK ?= latexmk
PANDOC ?= pandoc
LATEXPAND ?= latexpand

.PHONY: docs docs-pdf docs-markdown

docs:
	$(PYTHON) isa/tools/compile_documents.py --format all --latexmk "$(LATEXMK)" --pandoc "$(PANDOC)" --latexpand "$(LATEXPAND)"

docs-pdf:
	$(PYTHON) isa/tools/compile_documents.py --format pdf --latexmk "$(LATEXMK)"

docs-markdown:
	$(PYTHON) isa/tools/compile_documents.py --format markdown --pandoc "$(PANDOC)" --latexpand "$(LATEXPAND)"
