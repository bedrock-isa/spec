PYTHON ?= python3
LATEXMK ?= latexmk
PANDOC ?= pandoc
LATEX_FLAGS = -pdf -interaction=nonstopmode -halt-on-error

.PHONY: docs docs-markdown abi-markdown abi-tables check-abi-tables target-intrinsics-tables check-target-intrinsics-tables architecture-tables check-architecture-tables isa-reference isa-reference-markdown elf-abi elf-abi-markdown c-abi c-abi-markdown c-far-extensions c-far-extensions-markdown target-intrinsics target-intrinsics-markdown programming-guide programming-guide-markdown c-extensions compiler-abi intrinsics validate-docs validate-abi-model

docs: isa-reference elf-abi c-abi c-far-extensions target-intrinsics programming-guide

docs-markdown: isa-reference-markdown elf-abi-markdown c-abi-markdown c-far-extensions-markdown target-intrinsics-markdown programming-guide-markdown

abi-markdown: elf-abi-markdown c-abi-markdown

abi-tables:
	$(PYTHON) isa/tools/gen_abi_tables.py

check-abi-tables:
	$(PYTHON) isa/tools/gen_abi_tables.py --check

target-intrinsics-tables:
	$(PYTHON) isa/tools/gen_target_intrinsics.py

check-target-intrinsics-tables:
	$(PYTHON) isa/tools/gen_target_intrinsics.py --check

architecture-tables:
	$(PYTHON) isa/tools/gen_architecture_tables.py

check-architecture-tables:
	$(PYTHON) isa/tools/gen_architecture_tables.py --check

isa-reference: architecture-tables
	$(PYTHON) isa/tools/gen_docs.py -o build/isa_reference.tex
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build build/isa_reference.tex

isa-reference-markdown: architecture-tables
	$(PYTHON) isa/tools/gen_docs.py --format markdown --pandoc "$(PANDOC)" -o build/isa_reference.md

elf-abi: abi-tables
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build/latex/bedrock-elf-abi isa/abi/bedrock-elf-abi.tex

elf-abi-markdown: abi-tables
	$(PYTHON) isa/tools/latex_to_markdown.py --pandoc "$(PANDOC)" isa/abi/bedrock-elf-abi.tex build/markdown/bedrock-elf-abi.md

c-abi: abi-tables
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build/latex/bedrock-c-abi isa/abi/bedrock-c-abi.tex

c-abi-markdown: abi-tables
	$(PYTHON) isa/tools/latex_to_markdown.py --pandoc "$(PANDOC)" isa/abi/bedrock-c-abi.tex build/markdown/bedrock-c-abi.md

c-far-extensions:
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build/latex/bedrock-c-far-extensions isa/c/bedrock-c-far-extensions.tex

c-far-extensions-markdown:
	$(PYTHON) isa/tools/latex_to_markdown.py --pandoc "$(PANDOC)" isa/c/bedrock-c-far-extensions.tex build/markdown/bedrock-c-far-extensions.md

target-intrinsics: target-intrinsics-tables
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build/latex/bedrock-target-intrinsics isa/c/bedrock-target-intrinsics.tex

target-intrinsics-markdown: target-intrinsics-tables
	$(PYTHON) isa/tools/latex_to_markdown.py --pandoc "$(PANDOC)" isa/c/bedrock-target-intrinsics.tex build/markdown/bedrock-target-intrinsics.md

programming-guide:
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build/latex/bedrock-programming-toolchain-guide isa/guides/bedrock-programming-toolchain-guide.tex

programming-guide-markdown:
	$(PYTHON) isa/tools/latex_to_markdown.py --pandoc "$(PANDOC)" isa/guides/bedrock-programming-toolchain-guide.tex build/markdown/bedrock-programming-toolchain-guide.md

c-extensions: c-far-extensions

compiler-abi: target-intrinsics

intrinsics: target-intrinsics

validate-docs: check-architecture-tables
	$(PYTHON) isa/tools/validate_abi_docs.py

validate-abi-model:
	$(PYTHON) isa/tools/abi_call_model.py
