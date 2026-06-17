PYTHON ?= python3
PDFLATEX ?= pdflatex
LATEXMK ?= latexmk
CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -pedantic
PYTHONDONTWRITEBYTECODE ?= 1

BUILD_DIR ?= ../build
HOST_BUILD_DIR := $(BUILD_DIR)/host
SMOKE_BUILD_DIR := $(BUILD_DIR)/smoke
LATEX_BUILD_ROOT := $(BUILD_DIR)/latex
ISA_SPEC_DIR := spec
ISA_TOOLS_DIR := tools
ISA_SPEC_YAML := $(shell find $(ISA_SPEC_DIR) -type f -name '*.yaml' 2>/dev/null | sort)
LATEX_BUILDER_PY := $(wildcard $(ISA_TOOLS_DIR)/latex_builder/*.py)
LATEX_TEMPLATES := $(wildcard $(ISA_TOOLS_DIR)/latex_builder/templates/*.tex)
ASM_DISASM_C_TEMPLATES := $(ISA_TOOLS_DIR)/templates/bedrock_asm_disasm.h $(ISA_TOOLS_DIR)/templates/bedrock_asm_disasm.c $(ISA_TOOLS_DIR)/templates/bedrock_asm_disasm_core.c $(ISA_TOOLS_DIR)/templates/bedrock_text_runtime.c
DECODE_SV_TEMPLATES := $(ISA_TOOLS_DIR)/templates/bedrock_decode_pkg.sv $(ISA_TOOLS_DIR)/templates/bedrock_decode.sv $(ISA_TOOLS_DIR)/templates/bedrock_decode_synth.sv
AUX_DECODE_SV_TEMPLATES := $(ISA_TOOLS_DIR)/templates/bedrock_prefix_decode_pkg.sv $(ISA_TOOLS_DIR)/templates/bedrock_prefix_decode.sv $(ISA_TOOLS_DIR)/templates/bedrock_prefix_decode_synth.sv $(ISA_TOOLS_DIR)/templates/bedrock_ea_decode_pkg.sv $(ISA_TOOLS_DIR)/templates/bedrock_ea_decode.sv $(ISA_TOOLS_DIR)/templates/bedrock_ea_decode_synth.sv
ALLOCATION_TOOL_PY := $(ISA_TOOLS_DIR)/alloc_z3.py $(ISA_TOOLS_DIR)/alloc_candidates.py $(ISA_TOOLS_DIR)/alloc_field_layout.py $(ISA_TOOLS_DIR)/alloc_model.py $(ISA_TOOLS_DIR)/alloc_markdown.py
ISA_GENERATED_DIR := $(BUILD_DIR)/generated
GENERATED_CPPFLAGS := -I$(ISA_GENERATED_DIR)

ALLOCATION_PLAN := $(ISA_GENERATED_DIR)/allocation_plan.json
OPCODE_TABLE_MD := $(ISA_GENERATED_DIR)/opcode_table.md
OPCODE_ALLOCATION_MD := $(ISA_GENERATED_DIR)/opcode_allocation.md
ALLOCATION_STAMP := $(ISA_GENERATED_DIR)/.allocation.stamp
OPCODE_MAP_MD := $(ISA_GENERATED_DIR)/opcode_map.md
SLEIGH_SPEC := $(ISA_GENERATED_DIR)/isa.slaspec
ISA_REFERENCE_TEX := $(ISA_GENERATED_DIR)/isa_reference.tex
ISA_REFERENCE_PDF := $(ISA_GENERATED_DIR)/isa_reference.pdf
MANUAL_SECTION_TEX ?= $(ISA_GENERATED_DIR)/section_preview.tex
MANUAL_SECTION_PDF ?= $(ISA_GENERATED_DIR)/section_preview.pdf
ABI_SPEC := $(ISA_SPEC_DIR)/abi.yaml
ABI_REFERENCE_TEX := $(ISA_GENERATED_DIR)/abi_reference.tex
ABI_REFERENCE_PDF := $(ISA_GENERATED_DIR)/abi_reference.pdf
C_ABI_SPEC := $(ISA_SPEC_DIR)/c_abi.yaml
C_ABI_REFERENCE_TEX := $(ISA_GENERATED_DIR)/c_abi_reference.tex
C_ABI_REFERENCE_PDF := $(ISA_GENERATED_DIR)/c_abi_reference.pdf
BEDROCK_ASM_DISASM_H := $(ISA_GENERATED_DIR)/bedrock_asm_disasm.h
BEDROCK_ASM_DISASM_C := $(ISA_GENERATED_DIR)/bedrock_asm_disasm.c
ASM_DISASM_C_STAMP := $(ISA_GENERATED_DIR)/.asm-disasm-c.stamp
BEDROCK_DECODE_PKG_SV := $(ISA_GENERATED_DIR)/bedrock_decode_pkg.sv
BEDROCK_DECODE_SV := $(ISA_GENERATED_DIR)/bedrock_decode.sv
BEDROCK_DECODE_SYNTH_SV := $(ISA_GENERATED_DIR)/bedrock_decode_synth.sv
DECODE_SV_STAMP := $(ISA_GENERATED_DIR)/.decode-sv.stamp
BEDROCK_PREFIX_DECODE_PKG_SV := $(ISA_GENERATED_DIR)/bedrock_prefix_decode_pkg.sv
BEDROCK_PREFIX_DECODE_SV := $(ISA_GENERATED_DIR)/bedrock_prefix_decode.sv
BEDROCK_PREFIX_DECODE_SYNTH_SV := $(ISA_GENERATED_DIR)/bedrock_prefix_decode_synth.sv
BEDROCK_EA_DECODE_PKG_SV := $(ISA_GENERATED_DIR)/bedrock_ea_decode_pkg.sv
BEDROCK_EA_DECODE_SV := $(ISA_GENERATED_DIR)/bedrock_ea_decode.sv
BEDROCK_EA_DECODE_SYNTH_SV := $(ISA_GENERATED_DIR)/bedrock_ea_decode_synth.sv
AUX_DECODE_SV_STAMP := $(ISA_GENERATED_DIR)/.aux-decode-sv.stamp
DECODE_SV_OUTPUTS := $(BEDROCK_DECODE_PKG_SV) $(BEDROCK_DECODE_SV) $(BEDROCK_DECODE_SYNTH_SV)
AUX_DECODE_SV_OUTPUTS := $(BEDROCK_PREFIX_DECODE_PKG_SV) $(BEDROCK_PREFIX_DECODE_SV) $(BEDROCK_PREFIX_DECODE_SYNTH_SV) $(BEDROCK_EA_DECODE_PKG_SV) $(BEDROCK_EA_DECODE_SV) $(BEDROCK_EA_DECODE_SYNTH_SV)
ASM_DISASM_SMOKE := $(HOST_BUILD_DIR)/bedrock_asm_disasm_smoke
BEDROCK_AS := $(HOST_BUILD_DIR)/bedrock-as
BEDROCK_AS_SMOKE_OBJ := $(SMOKE_BUILD_DIR)/bedrock-as-smoke.o
LATEX_BUILD_DIR ?= $(LATEX_BUILD_ROOT)/isa_reference
SECTION_LATEX_BUILD_DIR ?= $(LATEX_BUILD_ROOT)/section_preview
ABI_LATEX_BUILD_DIR ?= $(LATEX_BUILD_ROOT)/abi_reference
C_ABI_LATEX_BUILD_DIR ?= $(LATEX_BUILD_ROOT)/c_abi_reference
LATEXMK_FORCE ?=
LATEXMKFLAGS ?= -pdf
LATEXMK_PDFLATEX := $(PDFLATEX) -interaction=nonstopmode -halt-on-error %O %S
SECTION ?= memory-address-translation

.PHONY: help validate allocation opcode-map sleigh asm-disasm-c asm-disasm-smoke bedrock-as bedrock-as-smoke decode-sv manual-tex manual-pdf manual-pdf-final manual-section-list manual-section-tex manual-section-pdf manual-section-pdf-final abi-tex abi-pdf abi-pdf-final c-abi-tex c-abi-pdf c-abi-pdf-final abi-all-tex abi-all-pdf-final clean-manual-build clean-manual-section-build clean-abi-build clean-c-abi-build

help:
	@printf '%s\n' 'ISA targets:'
	@printf '  %-28s %s\n' 'validate' 'Validate the ISA spec.'
	@printf '  %-28s %s\n' 'allocation' 'Generate allocation_plan.json and opcode_table.md.'
	@printf '  %-28s %s\n' 'opcode-map' 'Generate the validated-pattern opcode map.'
	@printf '  %-28s %s\n' 'sleigh' 'Generate the Ghidra SLEIGH specification.'
	@printf '  %-28s %s\n' 'asm-disasm-c' 'Generate C assembler/disassembler tables and form helpers.'
	@printf '  %-28s %s\n' 'asm-disasm-smoke' 'Build and run generated C assembler/disassembler smoke tests.'
	@printf '  %-28s %s\n' 'bedrock-as' 'Build the standalone Bedrock ELF assembler.'
	@printf '  %-28s %s\n' 'bedrock-as-smoke' 'Assemble a small ELF64 ET_REL smoke object.'
	@printf '  %-28s %s\n' 'decode-sv' 'Generate SystemVerilog instruction/prefix/EA decode snippets.'
	@printf '  %-28s %s\n' 'manual-tex' 'Generate isa_reference.tex.'
	@printf '  %-28s %s\n' 'manual-pdf' 'Generate the manual PDF with latexmk.'
	@printf '  %-28s %s\n' 'manual-pdf-final' 'Force-regenerate the manual PDF with latexmk -g.'
	@printf '  %-28s %s\n' 'manual-section-list' 'List section slugs accepted by SECTION=... preview builds.'
	@printf '  %-28s %s\n' 'manual-section-tex' 'Generate one section preview TeX.'
	@printf '  %-28s %s\n' 'manual-section-pdf' 'Generate one section preview PDF with latexmk.'
	@printf '  %-28s %s\n' 'manual-section-pdf-final' 'Force-regenerate one section preview PDF with latexmk -g.'
	@printf '  %-28s %s\n' 'abi-tex' 'Generate abi_reference.tex.'
	@printf '  %-28s %s\n' 'abi-pdf' 'Generate the language-neutral ABI PDF with latexmk.'
	@printf '  %-28s %s\n' 'abi-pdf-final' 'Force-regenerate the language-neutral ABI PDF with latexmk -g.'
	@printf '  %-28s %s\n' 'c-abi-tex' 'Generate c_abi_reference.tex.'
	@printf '  %-28s %s\n' 'c-abi-pdf' 'Generate the C ABI PDF with latexmk.'
	@printf '  %-28s %s\n' 'c-abi-pdf-final' 'Force-regenerate the C ABI PDF with latexmk -g.'
	@printf '  %-28s %s\n' 'abi-all-tex' 'Generate both ABI TeX documents.'
	@printf '  %-28s %s\n' 'abi-all-pdf-final' 'Generate both ABI PDFs.'
	@printf '  %-28s %s\n' 'clean-manual-build' 'Remove the temporary manual LaTeX build directory.'
	@printf '  %-28s %s\n' 'clean-manual-section-build' 'Remove the temporary section-preview LaTeX build directory.'
	@printf '  %-28s %s\n' 'clean-abi-build' 'Remove the temporary language-neutral ABI LaTeX build directory.'
	@printf '  %-28s %s\n' 'clean-c-abi-build' 'Remove the temporary C ABI LaTeX build directory.'

validate:
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/validate.py $(ISA_SPEC_DIR)

allocation:
	@missing=0; for path in $(ALLOCATION_PLAN) $(OPCODE_TABLE_MD) $(OPCODE_ALLOCATION_MD); do if [ ! -f "$$path" ]; then missing=1; fi; done; if [ "$$missing" -ne 0 ]; then rm -f "$(ALLOCATION_STAMP)"; fi
	$(MAKE) $(ALLOCATION_STAMP)

$(ALLOCATION_STAMP): $(ISA_SPEC_YAML) $(ALLOCATION_TOOL_PY)
	@mkdir -p "$(ISA_GENERATED_DIR)"
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/alloc_z3.py $(ISA_SPEC_DIR) -o $(ALLOCATION_PLAN) --md-output $(OPCODE_TABLE_MD)
	@cp "$(OPCODE_TABLE_MD)" "$(OPCODE_ALLOCATION_MD)"
	@touch "$@"

opcode-map: allocation
	$(MAKE) $(OPCODE_MAP_MD)

$(OPCODE_MAP_MD): $(ALLOCATION_STAMP) $(ISA_TOOLS_DIR)/gen_tables.py
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_tables.py $(ISA_SPEC_DIR) --allocation $(ALLOCATION_PLAN) -o $(OPCODE_MAP_MD)

sleigh: allocation
	$(MAKE) $(SLEIGH_SPEC)

$(SLEIGH_SPEC): $(ISA_SPEC_YAML) $(ALLOCATION_STAMP) $(ISA_TOOLS_DIR)/gen_sleigh.py $(ISA_TOOLS_DIR)/templates/sleigh_header.slaspec
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_sleigh.py $(ISA_SPEC_DIR) --allocation $(ALLOCATION_PLAN) -o $(SLEIGH_SPEC)

asm-disasm-c: allocation
	@missing=0; for path in $(BEDROCK_ASM_DISASM_H) $(BEDROCK_ASM_DISASM_C); do if [ ! -f "$$path" ]; then missing=1; fi; done; if [ "$$missing" -ne 0 ]; then rm -f "$(ASM_DISASM_C_STAMP)"; fi
	$(MAKE) $(ASM_DISASM_C_STAMP)

$(ASM_DISASM_C_STAMP): $(ALLOCATION_STAMP) $(ISA_TOOLS_DIR)/gen_asm_disasm_c.py $(ISA_TOOLS_DIR)/template_utils.py $(ISA_TOOLS_DIR)/gen_instruction_tables.py $(ASM_DISASM_C_TEMPLATES)
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_asm_disasm_c.py $(ISA_SPEC_DIR) --allocation $(ALLOCATION_PLAN) --header $(BEDROCK_ASM_DISASM_H) --source $(BEDROCK_ASM_DISASM_C)
	@touch "$@"

asm-disasm-smoke: asm-disasm-c
	@mkdir -p "$(HOST_BUILD_DIR)"
	$(CC) $(CFLAGS) $(GENERATED_CPPFLAGS) $(BEDROCK_ASM_DISASM_C) tests/asm_disasm_smoke.c -o $(ASM_DISASM_SMOKE)
	$(ASM_DISASM_SMOKE)

bedrock-as: asm-disasm-c
	@mkdir -p "$(HOST_BUILD_DIR)"
	$(CC) $(CFLAGS) $(GENERATED_CPPFLAGS) $(BEDROCK_ASM_DISASM_C) asm/context.c asm/parser.c asm/elf64_writer.c asm/bedrock-as.c -o $(BEDROCK_AS)

bedrock-as-smoke: bedrock-as
	@mkdir -p "$(SMOKE_BUILD_DIR)"
	$(BEDROCK_AS) -o $(BEDROCK_AS_SMOKE_OBJ) tests/assembler_smoke.s
	@printf 'wrote %s\n' "$(BEDROCK_AS_SMOKE_OBJ)"

decode-sv: allocation
	@missing=0; for path in $(DECODE_SV_OUTPUTS); do if [ ! -f "$$path" ]; then missing=1; fi; done; if [ "$$missing" -ne 0 ]; then rm -f "$(DECODE_SV_STAMP)"; fi
	@missing=0; for path in $(AUX_DECODE_SV_OUTPUTS); do if [ ! -f "$$path" ]; then missing=1; fi; done; if [ "$$missing" -ne 0 ]; then rm -f "$(AUX_DECODE_SV_STAMP)"; fi
	$(MAKE) $(DECODE_SV_STAMP) $(AUX_DECODE_SV_STAMP)

$(DECODE_SV_STAMP): $(ALLOCATION_STAMP) $(ISA_SPEC_YAML) $(ISA_TOOLS_DIR)/gen_sv_decode.py $(ISA_TOOLS_DIR)/template_utils.py $(ISA_TOOLS_DIR)/gen_asm_disasm_c.py $(ISA_TOOLS_DIR)/gen_instruction_tables.py $(ISA_TOOLS_DIR)/isa_spec.py $(DECODE_SV_TEMPLATES)
	@mkdir -p "$(ISA_GENERATED_DIR)"
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_sv_decode.py --allocation $(ALLOCATION_PLAN) --spec $(ISA_SPEC_DIR) --package $(BEDROCK_DECODE_PKG_SV) --module $(BEDROCK_DECODE_SV) --synth-module $(BEDROCK_DECODE_SYNTH_SV)
	@touch "$@"

$(AUX_DECODE_SV_STAMP): $(ISA_SPEC_YAML) $(ISA_TOOLS_DIR)/gen_sv_aux_decode.py $(ISA_TOOLS_DIR)/template_utils.py $(ISA_TOOLS_DIR)/isa_spec.py $(AUX_DECODE_SV_TEMPLATES)
	@mkdir -p "$(ISA_GENERATED_DIR)"
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_sv_aux_decode.py $(ISA_SPEC_DIR) --prefix-package $(BEDROCK_PREFIX_DECODE_PKG_SV) --prefix-module $(BEDROCK_PREFIX_DECODE_SV) --prefix-synth-module $(BEDROCK_PREFIX_DECODE_SYNTH_SV) --ea-package $(BEDROCK_EA_DECODE_PKG_SV) --ea-module $(BEDROCK_EA_DECODE_SV) --ea-synth-module $(BEDROCK_EA_DECODE_SYNTH_SV)
	@touch "$@"

manual-tex: allocation
	$(MAKE) $(ISA_REFERENCE_TEX)

$(ISA_REFERENCE_TEX): $(ISA_SPEC_YAML) $(ALLOCATION_STAMP) $(ISA_TOOLS_DIR)/gen_latex.py $(LATEX_BUILDER_PY) $(LATEX_TEMPLATES)
	@mkdir -p "$(ISA_GENERATED_DIR)"
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_latex.py $(ISA_SPEC_DIR) --allocation $(ALLOCATION_PLAN) -o $(ISA_REFERENCE_TEX)

manual-pdf: manual-tex
	@mkdir -p "$(LATEX_BUILD_DIR)"
	@if ! cmp -s "$(ISA_REFERENCE_TEX)" "$(LATEX_BUILD_DIR)/isa_reference.tex"; then cp "$(ISA_REFERENCE_TEX)" "$(LATEX_BUILD_DIR)/isa_reference.tex"; fi
	@(cd "$(LATEX_BUILD_DIR)" && $(LATEXMK) $(LATEXMKFLAGS) $(LATEXMK_FORCE) -pdflatex='$(LATEXMK_PDFLATEX)' isa_reference.tex)
	@cp "$(LATEX_BUILD_DIR)/isa_reference.pdf" "$(ISA_REFERENCE_PDF)"
	@printf 'wrote %s\n' "$(ISA_REFERENCE_PDF)"

manual-pdf-final:
	$(MAKE) manual-pdf LATEXMK_FORCE=-g

manual-section-list: allocation
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_latex.py $(ISA_SPEC_DIR) --allocation $(ALLOCATION_PLAN) --list-preview-sections -o -

manual-section-tex: allocation
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_latex.py $(ISA_SPEC_DIR) --allocation $(ALLOCATION_PLAN) --preview-section "$(SECTION)" -o $(MANUAL_SECTION_TEX)

manual-section-pdf: manual-section-tex
	@mkdir -p "$(SECTION_LATEX_BUILD_DIR)"
	@if ! cmp -s "$(MANUAL_SECTION_TEX)" "$(SECTION_LATEX_BUILD_DIR)/section_preview.tex"; then cp "$(MANUAL_SECTION_TEX)" "$(SECTION_LATEX_BUILD_DIR)/section_preview.tex"; fi
	@(cd "$(SECTION_LATEX_BUILD_DIR)" && $(LATEXMK) $(LATEXMKFLAGS) $(LATEXMK_FORCE) -pdflatex='$(LATEXMK_PDFLATEX)' section_preview.tex)
	@cp "$(SECTION_LATEX_BUILD_DIR)/section_preview.pdf" "$(MANUAL_SECTION_PDF)"
	@printf 'wrote %s\n' "$(MANUAL_SECTION_PDF)"

manual-section-pdf-final:
	$(MAKE) manual-section-pdf LATEXMK_FORCE=-g

abi-tex: $(ABI_REFERENCE_TEX)

$(ABI_REFERENCE_TEX): $(ABI_SPEC) $(ISA_TOOLS_DIR)/gen_abi_latex.py
	@mkdir -p "$(ISA_GENERATED_DIR)"
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_abi_latex.py $(ABI_SPEC) -o $(ABI_REFERENCE_TEX)

abi-pdf: $(ABI_REFERENCE_TEX)
	@mkdir -p "$(ABI_LATEX_BUILD_DIR)"
	@if ! cmp -s "$(ABI_REFERENCE_TEX)" "$(ABI_LATEX_BUILD_DIR)/abi_reference.tex"; then cp "$(ABI_REFERENCE_TEX)" "$(ABI_LATEX_BUILD_DIR)/abi_reference.tex"; fi
	@(cd "$(ABI_LATEX_BUILD_DIR)" && $(LATEXMK) $(LATEXMKFLAGS) $(LATEXMK_FORCE) -pdflatex='$(LATEXMK_PDFLATEX)' abi_reference.tex)
	@cp "$(ABI_LATEX_BUILD_DIR)/abi_reference.pdf" "$(ABI_REFERENCE_PDF)"
	@printf 'wrote %s\n' "$(ABI_REFERENCE_PDF)"

abi-pdf-final:
	$(MAKE) abi-pdf LATEXMK_FORCE=-g

c-abi-tex: $(C_ABI_REFERENCE_TEX)

$(C_ABI_REFERENCE_TEX): $(C_ABI_SPEC) $(ISA_TOOLS_DIR)/gen_abi_latex.py
	@mkdir -p "$(ISA_GENERATED_DIR)"
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_abi_latex.py $(C_ABI_SPEC) -o $(C_ABI_REFERENCE_TEX)

c-abi-pdf: $(C_ABI_REFERENCE_TEX)
	@mkdir -p "$(C_ABI_LATEX_BUILD_DIR)"
	@if ! cmp -s "$(C_ABI_REFERENCE_TEX)" "$(C_ABI_LATEX_BUILD_DIR)/c_abi_reference.tex"; then cp "$(C_ABI_REFERENCE_TEX)" "$(C_ABI_LATEX_BUILD_DIR)/c_abi_reference.tex"; fi
	@(cd "$(C_ABI_LATEX_BUILD_DIR)" && $(LATEXMK) $(LATEXMKFLAGS) $(LATEXMK_FORCE) -pdflatex='$(LATEXMK_PDFLATEX)' c_abi_reference.tex)
	@cp "$(C_ABI_LATEX_BUILD_DIR)/c_abi_reference.pdf" "$(C_ABI_REFERENCE_PDF)"
	@printf 'wrote %s\n' "$(C_ABI_REFERENCE_PDF)"

c-abi-pdf-final:
	$(MAKE) c-abi-pdf LATEXMK_FORCE=-g

abi-all-tex: abi-tex c-abi-tex

abi-all-pdf-final: abi-pdf-final c-abi-pdf-final

clean-manual-build:
	rm -rf "$(LATEX_BUILD_DIR)"

clean-manual-section-build:
	rm -rf "$(SECTION_LATEX_BUILD_DIR)"

clean-abi-build:
	rm -rf "$(ABI_LATEX_BUILD_DIR)"

clean-c-abi-build:
	rm -rf "$(C_ABI_LATEX_BUILD_DIR)"
