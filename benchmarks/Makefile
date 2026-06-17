PYTHON ?= python3
PYTHONDONTWRITEBYTECODE ?= 1
COMPARE_CLANG ?= $(shell if [ -x /opt/homebrew/opt/llvm/bin/clang ]; then printf '%s\n' /opt/homebrew/opt/llvm/bin/clang; else command -v clang; fi)
BEDROCK_CMODEL ?= small

BUILD_DIR ?= ../build
QBE_BIN := $(BUILD_DIR)/qbe/obj/qbe
QBE_MINIC := ../qbe/minic/minic
BEDROCK_AS := $(BUILD_DIR)/host/bedrock-as
COMPARE_BUILD_DIR := $(BUILD_DIR)/compare/arch
ARCH_COMPARE_REPORT := $(BUILD_DIR)/compare/arch_compare.md
ARCH_COMPARE_JSON := $(BUILD_DIR)/compare/arch_compare.json
ARCH_COMPARE_CASES := arch_compare

.PHONY: help qbe-bedrock qbe-minic bedrock-as arch-compare clean

help:
	@printf '%s\n' 'Benchmark targets:'
	@printf '  %-14s %s\n' 'arch-compare' 'Compare Bedrock code density with x86/ARM/RISC-V reference targets.'
	@printf '  %-14s %s\n' 'clean' 'Remove benchmark comparison build artifacts.'

qbe-bedrock:
	$(MAKE) -C ../qbe bedrock

qbe-minic:
	$(MAKE) -C ../qbe/minic

bedrock-as:
	$(MAKE) -C ../isa bedrock-as

arch-compare: qbe-bedrock qbe-minic bedrock-as
	PYTHONDONTWRITEBYTECODE=$(PYTHONDONTWRITEBYTECODE) $(PYTHON) ../tools/compare_arch.py $(ARCH_COMPARE_CASES) --qbe $(QBE_BIN) --minic $(QBE_MINIC) --bedrock-as $(BEDROCK_AS) --bedrock-cmodel $(BEDROCK_CMODEL) --clang $(COMPARE_CLANG) --out-dir $(COMPARE_BUILD_DIR) --report $(ARCH_COMPARE_REPORT) --json $(ARCH_COMPARE_JSON)

clean:
	rm -rf "$(COMPARE_BUILD_DIR)" "$(ARCH_COMPARE_REPORT)" "$(ARCH_COMPARE_JSON)"
