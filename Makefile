PYTHON ?= python3
LATEXMK ?= latexmk
LATEX_FLAGS = -pdf -interaction=nonstopmode -halt-on-error

.PHONY: docs isa-reference elf-abi c-abi c-far-extensions target-intrinsics c-extensions compiler-abi intrinsics validate-docs validate-abi-model

docs: isa-reference elf-abi c-abi c-far-extensions target-intrinsics

isa-reference:
	$(PYTHON) isa/tools/gen_docs.py --format latex -o build/isa_reference.tex
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build build/isa_reference.tex

elf-abi:
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build/latex/bedrock-elf-abi isa/abi/bedrock-elf-abi.tex

c-abi:
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build/latex/bedrock-c-abi isa/abi/bedrock-c-abi.tex

c-far-extensions:
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build/latex/bedrock-c-far-extensions isa/c/bedrock-c-far-extensions.tex

target-intrinsics:
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build/latex/bedrock-target-intrinsics isa/c/bedrock-target-intrinsics.tex

c-extensions: c-far-extensions

compiler-abi: target-intrinsics

intrinsics: target-intrinsics

validate-docs:
	$(PYTHON) isa/tools/validate_abi_docs.py

validate-abi-model:
	$(PYTHON) isa/tools/abi_call_model.py
