.DEFAULT_GOAL := all

export PYTHONDONTWRITEBYTECODE := 1

PYTHON ?= python3
CARGO ?= cargo
LATEXMK ?= latexmk
PANDOC ?= pandoc
LATEXPAND ?= latexpand
MKDOCS ?= mkdocs
export LATEXMK PANDOC LATEXPAND MKDOCS

OUTPUT_ROOT ?= output
SAIL_OUTPUT_ROOT ?= $(OUTPUT_ROOT)/sail-doc
SV_OUTPUT_ROOT ?= $(OUTPUT_ROOT)/systemverilog-decoder
EMULATOR_MANIFEST := emulator/Cargo.toml
EMULATOR_TARGET_DIR ?= $(abspath $(OUTPUT_ROOT)/emulator-target)
SPEC_PYTHON_TEST_PATHS := $(shell find tests -type f -name 'test_*.py' -print)
ALL_PYTHON_TEST_MODULES := $(sort $(subst /,.,$(patsubst %.py,%,$(SPEC_PYTHON_TEST_PATHS))))
SYSTEMVERILOG_TEST_MODULES := tests.test_systemverilog_decoder tests.test_systemverilog_architecture_artifacts
SPEC_PYTHON_TEST_MODULES := $(filter-out $(SYSTEMVERILOG_TEST_MODULES),$(ALL_PYTHON_TEST_MODULES))
LLVM_PROJECT_ROOT ?= $(abspath ../llvm-project)
export LLVM_PROJECT_ROOT
LLVM_BUILD_DIR ?= $(BEDROCK_LLVM_ROOT)
LLVM_BIN ?= $(if $(BEDROCK_LLVM_BIN),$(abspath $(BEDROCK_LLVM_BIN)),$(if $(BEDROCK_LLVM_ROOT),$(abspath $(BEDROCK_LLVM_ROOT)/bin)))

.PHONY: all isa sail emulator sv-decoder
.PHONY: docs docs-site sail-docs
.PHONY: emulator-isa-generate emulator-isa-check emulator-format emulator-test emulator-validate
.PHONY: test-fast test-hardware test-pr
.PHONY: llvm-sync llvm samples samples-check tiny-kernel clean-samples

all: isa sail emulator samples

isa: docs

sail: sail-docs

sv-decoder:
	$(PYTHON) -m engine artifacts generate systemverilog-package \
		systemverilog-instruction-decoder --output-root "$(SV_OUTPUT_ROOT)"

emulator: emulator-isa-check
	$(CARGO) build --manifest-path "$(EMULATOR_MANIFEST)" --workspace --target-dir "$(EMULATOR_TARGET_DIR)"

docs:
	$(PYTHON) -m engine docs build --output-root "$(OUTPUT_ROOT)"

docs-site: docs
	$(PYTHON) -m engine artifacts generate web-reference --output-root "$(OUTPUT_ROOT)"

sail-docs:
	$(PYTHON) -m engine artifacts generate sail-model --output-root "$(SAIL_OUTPUT_ROOT)"

emulator-isa-generate:
	PYTHON="$(PYTHON)" $(CARGO) check --manifest-path "$(EMULATOR_MANIFEST)" -p bedrock-sail-core --target-dir "$(EMULATOR_TARGET_DIR)"

emulator-isa-check: emulator-isa-generate

emulator-format:
	$(CARGO) fmt --manifest-path "$(EMULATOR_MANIFEST)" --all -- --check

emulator-test:
	$(CARGO) test --manifest-path "$(EMULATOR_MANIFEST)" --workspace --target-dir "$(EMULATOR_TARGET_DIR)"

emulator-validate:
	+$(MAKE) -j1 emulator-isa-check emulator-format emulator-test

test-fast:
	$(PYTHON) -m engine check
	+$(MAKE) -j1 samples-check
	$(PYTHON) -m unittest $(SPEC_PYTHON_TEST_MODULES)
	+$(MAKE) -j1 emulator-isa-check
	+$(MAKE) -j1 emulator-format
	$(CARGO) test --manifest-path "$(EMULATOR_MANIFEST)" --workspace \
		--exclude bedrock-lldb --exclude bedrock-gui \
		--target-dir "$(EMULATOR_TARGET_DIR)"

test-hardware:
	$(PYTHON) -m unittest $(SYSTEMVERILOG_TEST_MODULES)

test-pr:
	+$(MAKE) -j1 test-fast
	+$(MAKE) -j1 test-hardware

llvm-sync:
	$(PYTHON) tools/sync_llvm_artifacts.py "$(LLVM_PROJECT_ROOT)"

llvm:
	@test -n "$(LLVM_BUILD_DIR)" || { echo "BEDROCK_LLVM_ROOT is required" >&2; exit 1; }
	+$(MAKE) llvm-sync
	$(MAKE) -C "$(LLVM_BUILD_DIR)" bin/clang bin/llc bin/lld \
		bin/llvm-mc bin/llvm-objcopy bin/llvm-objdump bin/llvm-readelf

samples:
	$(MAKE) -C samples LLVM_BIN="$(LLVM_BIN)" PYTHON="$(PYTHON)" \
		OUTPUT_ROOT="$(abspath $(OUTPUT_ROOT)/samples)" all

samples-check:
	$(MAKE) -C samples LLVM_BIN="$(LLVM_BIN)" PYTHON="$(PYTHON)" \
		OUTPUT_ROOT="$(abspath $(OUTPUT_ROOT)/samples)" check

tiny-kernel:
	$(MAKE) -C samples/tiny_kernel LLVM_BIN="$(LLVM_BIN)" PYTHON="$(PYTHON)" \
		OUTPUT_ROOT="$(abspath $(OUTPUT_ROOT)/samples/tiny_kernel)" build

clean-samples:
	$(MAKE) -C samples OUTPUT_ROOT="$(abspath $(OUTPUT_ROOT)/samples)" clean
