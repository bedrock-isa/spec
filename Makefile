PYTHON ?= python3
PDFLATEX ?= pdflatex
LATEXMK ?= latexmk
CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -pedantic
PYTHONDONTWRITEBYTECODE ?= 1
COMPARE_CLANG ?= $(shell if [ -x /opt/homebrew/opt/llvm/bin/clang ]; then printf '%s\n' /opt/homebrew/opt/llvm/bin/clang; else command -v clang; fi)
BEDROCK_CMODEL ?= small

BUILD_DIR ?= build
HOST_BUILD_DIR := $(BUILD_DIR)/host
SMOKE_BUILD_DIR := $(BUILD_DIR)/smoke
LATEX_BUILD_ROOT := $(BUILD_DIR)/latex
COMPARE_BUILD_DIR := $(BUILD_DIR)/compare/arch
ISA_DIR := isa
ISA_SPEC_DIR := $(ISA_DIR)/spec
ISA_TOOLS_DIR := $(ISA_DIR)/tools
ISA_SPEC_YAML := $(wildcard $(ISA_SPEC_DIR)/*.yaml)
LATEX_BUILDER_PY := $(wildcard $(ISA_TOOLS_DIR)/latex_builder/*.py)
LATEX_TEMPLATES := $(wildcard $(ISA_TOOLS_DIR)/latex_builder/templates/*.tex)
ALLOCATION_TOOL_PY := $(ISA_TOOLS_DIR)/alloc_z3.py $(ISA_TOOLS_DIR)/alloc_candidates.py $(ISA_TOOLS_DIR)/alloc_field_layout.py $(ISA_TOOLS_DIR)/alloc_model.py $(ISA_TOOLS_DIR)/alloc_markdown.py
QBE_DIR := qbe
QBE_BIN := $(BUILD_DIR)/qbe/obj/qbe
QBE_MINIC := $(QBE_DIR)/minic/minic
ARCH_COMPARE_REPORT := $(BUILD_DIR)/compare/arch_compare.md
ARCH_COMPARE_JSON := $(BUILD_DIR)/compare/arch_compare.json
ISA_GENERATED_DIR := $(BUILD_DIR)/generated
GENERATED_CPPFLAGS := -I$(ISA_GENERATED_DIR)

ALLOCATION_PLAN := $(ISA_GENERATED_DIR)/allocation_plan.json
OPCODE_TABLE_MD := $(ISA_GENERATED_DIR)/opcode_table.md
OPCODE_ALLOCATION_MD := $(ISA_GENERATED_DIR)/opcode_allocation.md
OPCODE_MAP_MD := $(ISA_GENERATED_DIR)/opcode_map.md
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
BEDROCK_DECODE_PKG_SV := $(ISA_GENERATED_DIR)/bedrock_decode_pkg.sv
BEDROCK_DECODE_SV := $(ISA_GENERATED_DIR)/bedrock_decode.sv
BEDROCK_DECODE_SYNTH_SV := $(ISA_GENERATED_DIR)/bedrock_decode_synth.sv
BEDROCK_PREFIX_DECODE_PKG_SV := $(ISA_GENERATED_DIR)/bedrock_prefix_decode_pkg.sv
BEDROCK_PREFIX_DECODE_SV := $(ISA_GENERATED_DIR)/bedrock_prefix_decode.sv
BEDROCK_PREFIX_DECODE_SYNTH_SV := $(ISA_GENERATED_DIR)/bedrock_prefix_decode_synth.sv
BEDROCK_EA_DECODE_PKG_SV := $(ISA_GENERATED_DIR)/bedrock_ea_decode_pkg.sv
BEDROCK_EA_DECODE_SV := $(ISA_GENERATED_DIR)/bedrock_ea_decode.sv
BEDROCK_EA_DECODE_SYNTH_SV := $(ISA_GENERATED_DIR)/bedrock_ea_decode_synth.sv
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

.PHONY: help validate yaml-audit allocation opcode-map qbe-bedrock arch-compare asm-disasm-c asm-disasm-smoke bedrock-as bedrock-as-smoke rtl-predecode-synth rtl-decode-sv rtl-decode-lint rtl-decode-test rtl-decode-synth rtl-execute-lint rtl-execute-test rtl-execute-synth rtl-lint rtl-test manual-tex manual-pdf manual-pdf-final manual-section-list manual-section-tex manual-section-pdf manual-section-pdf-final abi-tex abi-pdf abi-pdf-final c-abi-tex c-abi-pdf c-abi-pdf-final abi-all-tex abi-all-pdf-final clean-manual-build clean-manual-section-build clean-abi-build clean-c-abi-build clean-rtl-build clean-build

help:
	@printf '%s\n' 'Targets:'
	@printf '  %-18s %s\n' 'validate' 'Validate the ISA spec.'
	@printf '  %-18s %s\n' 'yaml-audit' 'Report prose-like scalar policy tokens in YAML specs.'
	@printf '  %-18s %s\n' 'allocation' 'Generate build/generated/allocation_plan.json and opcode_table.md.'
	@printf '  %-18s %s\n' 'opcode-map' 'Generate the validated-pattern opcode map.'
	@printf '  %-18s %s\n' 'qbe-bedrock' 'Build the Bedrock-only QBE backend.'
	@printf '  %-18s %s\n' 'arch-compare' 'Compare Bedrock code density with x86/ARM/RISC-V reference targets.'
	@printf '  %-18s %s\n' 'asm-disasm-c' 'Generate C assembler/disassembler tables and form helpers.'
	@printf '  %-18s %s\n' 'asm-disasm-smoke' 'Build and run generated C assembler/disassembler smoke tests.'
	@printf '  %-18s %s\n' 'bedrock-as' 'Build the standalone Bedrock ELF assembler.'
	@printf '  %-18s %s\n' 'bedrock-as-smoke' 'Assemble a small ELF64 ET_REL smoke object.'
	@printf '  %-18s %s\n' 'rtl-predecode-synth' 'Synthesize the line predecoder with Yosys statistics.'
	@printf '  %-18s %s\n' 'rtl-decode-sv' 'Generate SystemVerilog instruction/prefix/EA decode snippets.'
	@printf '  %-18s %s\n' 'rtl-decode-lint' 'Generate and lint the generated SystemVerilog decoders.'
	@printf '  %-18s %s\n' 'rtl-decode-test' 'Generate and run the SystemVerilog decoder/precheck smoke tests.'
	@printf '  %-18s %s\n' 'rtl-decode-synth' 'Generate and synthesize decoders/precheck logic with Yosys statistics.'
	@printf '  %-18s %s\n' 'rtl-execute-lint' 'Generate dependencies and lint hand-written execute-stage helper units.'
	@printf '  %-18s %s\n' 'rtl-execute-test' 'Generate dependencies and run execute-stage helper tests.'
	@printf '  %-18s %s\n' 'rtl-execute-synth' 'Generate dependencies and synthesize execute-stage helper units.'
	@printf '  %-18s %s\n' 'rtl-lint' 'Lint the SystemVerilog RTL with Verilator.'
	@printf '  %-18s %s\n' 'rtl-test' 'Build and run the SystemVerilog Verilator smoke testbench.'
	@printf '  %-18s %s\n' 'manual-tex' 'Generate build/generated/isa_reference.tex.'
	@printf '  %-18s %s\n' 'manual-pdf' 'Generate the manual PDF with latexmk.'
	@printf '  %-18s %s\n' 'manual-pdf-final' 'Force-regenerate the manual PDF with latexmk -g.'
	@printf '  %-18s %s\n' 'manual-section-list' 'List section slugs accepted by SECTION=... preview builds.'
	@printf '  %-18s %s\n' 'manual-section-tex' 'Generate one section preview TeX. Example: make manual-section-tex SECTION=memory-address-translation.'
	@printf '  %-18s %s\n' 'manual-section-pdf' 'Generate one section preview PDF with latexmk. Example: make manual-section-pdf SECTION=memory-model.'
	@printf '  %-18s %s\n' 'manual-section-pdf-final' 'Force-regenerate one section preview PDF with latexmk -g.'
	@printf '  %-18s %s\n' 'abi-tex' 'Generate build/generated/abi_reference.tex.'
	@printf '  %-18s %s\n' 'abi-pdf' 'Generate the language-neutral ABI PDF with latexmk.'
	@printf '  %-18s %s\n' 'abi-pdf-final' 'Force-regenerate the language-neutral ABI PDF with latexmk -g.'
	@printf '  %-18s %s\n' 'c-abi-tex' 'Generate build/generated/c_abi_reference.tex.'
	@printf '  %-18s %s\n' 'c-abi-pdf' 'Generate the C ABI PDF with latexmk.'
	@printf '  %-18s %s\n' 'c-abi-pdf-final' 'Force-regenerate the C ABI PDF with latexmk -g.'
	@printf '  %-18s %s\n' 'abi-all-tex' 'Generate both ABI TeX documents.'
	@printf '  %-18s %s\n' 'abi-all-pdf-final' 'Generate both ABI PDFs with PDF_PASSES=2.'
	@printf '  %-18s %s\n' 'clean-manual-build' 'Remove the temporary LaTeX build directory.'
	@printf '  %-18s %s\n' 'clean-manual-section-build' 'Remove the temporary section-preview LaTeX build directory.'
	@printf '  %-18s %s\n' 'clean-abi-build' 'Remove the temporary language-neutral ABI LaTeX build directory.'
	@printf '  %-18s %s\n' 'clean-c-abi-build' 'Remove the temporary C ABI LaTeX build directory.'
	@printf '  %-18s %s\n' 'clean-rtl-build' 'Remove Verilator build artifacts.'
	@printf '  %-18s %s\n' 'clean-build' 'Remove all build/ artifacts.'

validate:
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/validate.py $(ISA_SPEC_DIR)

yaml-audit:
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/yaml_style_audit.py $(ISA_SPEC_DIR)

allocation: $(ALLOCATION_PLAN) $(OPCODE_TABLE_MD)

$(ALLOCATION_PLAN) $(OPCODE_TABLE_MD): $(ISA_SPEC_DIR)/*.yaml $(ALLOCATION_TOOL_PY)
	@mkdir -p "$(ISA_GENERATED_DIR)"
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/alloc_z3.py $(ISA_SPEC_DIR) -o $(ALLOCATION_PLAN) --md-output $(OPCODE_TABLE_MD)
	@cp "$(OPCODE_TABLE_MD)" "$(OPCODE_ALLOCATION_MD)"

opcode-map: $(OPCODE_MAP_MD)

$(OPCODE_MAP_MD): $(ALLOCATION_PLAN) $(ISA_TOOLS_DIR)/gen_tables.py
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_tables.py $(ISA_SPEC_DIR) --allocation $(ALLOCATION_PLAN) -o $(OPCODE_MAP_MD)

qbe-bedrock: $(QBE_BIN)

$(QBE_BIN): $(QBE_DIR)/Makefile $(QBE_DIR)/*.c $(QBE_DIR)/*.h $(QBE_DIR)/bedrock/*.c $(QBE_DIR)/bedrock/all.h
	$(MAKE) -C $(QBE_DIR)

$(QBE_MINIC): $(QBE_DIR)/minic/minic.y $(QBE_DIR)/minic/yacc.c
	$(MAKE) -C $(QBE_DIR)/minic

arch-compare: $(QBE_BIN) $(QBE_MINIC) bedrock-as
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) tools/compare_arch.py --qbe $(QBE_BIN) --minic $(QBE_MINIC) --bedrock-as $(BEDROCK_AS) --bedrock-cmodel $(BEDROCK_CMODEL) --clang $(COMPARE_CLANG) --out-dir $(COMPARE_BUILD_DIR) --report $(ARCH_COMPARE_REPORT) --json $(ARCH_COMPARE_JSON)

asm-disasm-c: $(BEDROCK_ASM_DISASM_H) $(BEDROCK_ASM_DISASM_C)

$(BEDROCK_ASM_DISASM_H) $(BEDROCK_ASM_DISASM_C): $(ALLOCATION_PLAN) $(ISA_TOOLS_DIR)/gen_asm_disasm_c.py $(ISA_TOOLS_DIR)/gen_instruction_tables.py
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_asm_disasm_c.py --allocation $(ALLOCATION_PLAN) --header $(BEDROCK_ASM_DISASM_H) --source $(BEDROCK_ASM_DISASM_C)

asm-disasm-smoke: $(BEDROCK_ASM_DISASM_H) $(BEDROCK_ASM_DISASM_C)
	@mkdir -p "$(HOST_BUILD_DIR)"
	$(CC) $(CFLAGS) $(GENERATED_CPPFLAGS) $(BEDROCK_ASM_DISASM_C) $(ISA_DIR)/tests/asm_disasm_smoke.c -o $(ASM_DISASM_SMOKE)
	$(ASM_DISASM_SMOKE)

bedrock-as: $(BEDROCK_ASM_DISASM_H) $(BEDROCK_ASM_DISASM_C)
	@mkdir -p "$(HOST_BUILD_DIR)"
	$(CC) $(CFLAGS) $(GENERATED_CPPFLAGS) $(BEDROCK_ASM_DISASM_C) $(ISA_DIR)/asm/context.c $(ISA_DIR)/asm/parser.c $(ISA_DIR)/asm/elf64_writer.c $(ISA_DIR)/asm/bedrock-as.c -o $(BEDROCK_AS)

bedrock-as-smoke: bedrock-as
	@mkdir -p "$(SMOKE_BUILD_DIR)"
	$(BEDROCK_AS) -o $(BEDROCK_AS_SMOKE_OBJ) $(ISA_DIR)/tests/assembler_smoke.s
	@printf 'wrote %s\n' "$(BEDROCK_AS_SMOKE_OBJ)"

rtl-predecode-synth:
	$(MAKE) -C rtl predecode-synth

rtl-decode-sv: $(BEDROCK_DECODE_PKG_SV) $(BEDROCK_DECODE_SV) $(BEDROCK_DECODE_SYNTH_SV) $(BEDROCK_PREFIX_DECODE_PKG_SV) $(BEDROCK_PREFIX_DECODE_SV) $(BEDROCK_PREFIX_DECODE_SYNTH_SV) $(BEDROCK_EA_DECODE_PKG_SV) $(BEDROCK_EA_DECODE_SV) $(BEDROCK_EA_DECODE_SYNTH_SV)

$(BEDROCK_DECODE_PKG_SV) $(BEDROCK_DECODE_SV) $(BEDROCK_DECODE_SYNTH_SV): $(ALLOCATION_PLAN) $(ISA_SPEC_DIR)/instructions.yaml $(ISA_TOOLS_DIR)/gen_sv_decode.py $(ISA_TOOLS_DIR)/gen_asm_disasm_c.py $(ISA_TOOLS_DIR)/gen_instruction_tables.py $(ISA_TOOLS_DIR)/isa_spec.py
	@mkdir -p "$(ISA_GENERATED_DIR)"
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_sv_decode.py --allocation $(ALLOCATION_PLAN) --spec $(ISA_SPEC_DIR) --package $(BEDROCK_DECODE_PKG_SV) --module $(BEDROCK_DECODE_SV) --synth-module $(BEDROCK_DECODE_SYNTH_SV)

$(BEDROCK_PREFIX_DECODE_PKG_SV) $(BEDROCK_PREFIX_DECODE_SV) $(BEDROCK_PREFIX_DECODE_SYNTH_SV) $(BEDROCK_EA_DECODE_PKG_SV) $(BEDROCK_EA_DECODE_SV) $(BEDROCK_EA_DECODE_SYNTH_SV): $(ISA_SPEC_DIR)/prefixes.yaml $(ISA_SPEC_DIR)/ea.yaml $(ISA_TOOLS_DIR)/gen_sv_aux_decode.py $(ISA_TOOLS_DIR)/isa_spec.py
	@mkdir -p "$(ISA_GENERATED_DIR)"
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_sv_aux_decode.py $(ISA_SPEC_DIR) --prefix-package $(BEDROCK_PREFIX_DECODE_PKG_SV) --prefix-module $(BEDROCK_PREFIX_DECODE_SV) --prefix-synth-module $(BEDROCK_PREFIX_DECODE_SYNTH_SV) --ea-package $(BEDROCK_EA_DECODE_PKG_SV) --ea-module $(BEDROCK_EA_DECODE_SV) --ea-synth-module $(BEDROCK_EA_DECODE_SYNTH_SV)

rtl-decode-lint: rtl-decode-sv
	$(MAKE) -C rtl decode-lint

rtl-decode-test: rtl-decode-sv
	$(MAKE) -C rtl decode-test

rtl-decode-synth: rtl-decode-sv
	$(MAKE) -C rtl decode-synth

rtl-execute-lint: rtl-decode-sv
	$(MAKE) -C rtl execute-lint

rtl-execute-test: rtl-decode-sv
	$(MAKE) -C rtl execute-test

rtl-execute-synth: rtl-decode-sv
	$(MAKE) -C rtl execute-synth

rtl-lint:
	$(MAKE) -C rtl lint

rtl-test:
	$(MAKE) -C rtl test

manual-tex: $(ISA_REFERENCE_TEX)

$(ISA_REFERENCE_TEX): $(ISA_SPEC_YAML) $(ALLOCATION_PLAN) $(ISA_TOOLS_DIR)/gen_latex.py $(LATEX_BUILDER_PY) $(LATEX_TEMPLATES)
	@mkdir -p "$(ISA_GENERATED_DIR)"
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_latex.py $(ISA_SPEC_DIR) --allocation $(ALLOCATION_PLAN) -o $(ISA_REFERENCE_TEX)

manual-pdf: $(ISA_REFERENCE_TEX)
	@mkdir -p "$(LATEX_BUILD_DIR)"
	@if ! cmp -s "$(ISA_REFERENCE_TEX)" "$(LATEX_BUILD_DIR)/isa_reference.tex"; then cp "$(ISA_REFERENCE_TEX)" "$(LATEX_BUILD_DIR)/isa_reference.tex"; fi
	@(cd "$(LATEX_BUILD_DIR)" && $(LATEXMK) $(LATEXMKFLAGS) $(LATEXMK_FORCE) -pdflatex='$(LATEXMK_PDFLATEX)' isa_reference.tex)
	@cp "$(LATEX_BUILD_DIR)/isa_reference.pdf" "$(ISA_REFERENCE_PDF)"
	@printf 'wrote %s\n' "$(ISA_REFERENCE_PDF)"

manual-pdf-final:
	$(MAKE) manual-pdf LATEXMK_FORCE=-g

manual-section-list:
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) $(ISA_TOOLS_DIR)/gen_latex.py $(ISA_SPEC_DIR) --allocation $(ALLOCATION_PLAN) --list-preview-sections -o -

manual-section-tex:
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

clean-rtl-build:
	$(MAKE) -C rtl clean

clean-build:
	rm -rf "$(BUILD_DIR)"
