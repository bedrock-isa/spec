.DEFAULT_GOAL := all

export PYTHONDONTWRITEBYTECODE := 1

PYTHON ?= python3
CARGO ?= cargo
LATEXMK ?= latexmk
PANDOC ?= pandoc
LATEXPAND ?= latexpand
MKDOCS ?= mkdocs
export LATEXMK PANDOC LATEXPAND MKDOCS

BUILD_DIR ?= output
SAIL_BUILD_DIR ?= $(BUILD_DIR)/sail-doc
SV_BUILD_DIR ?= $(BUILD_DIR)/systemverilog-decoder
SV_TEST_ROOT ?= $(SV_BUILD_DIR)/tests
EMULATOR_MANIFEST := emulator/Cargo.toml
EMULATOR_TARGET_DIR ?= $(abspath $(BUILD_DIR)/emulator-target)
ISA_PYTHON_TEST_PATHS := $(shell find isa/tests -type f -name 'test_*.py' -print)
ISA_PYTHON_TEST_MODULES := $(sort $(subst /,.,$(patsubst %.py,%,$(ISA_PYTHON_TEST_PATHS))))
LLVM_PROJECT_ROOT ?= $(abspath ../llvm-project)
LLVM_BUILD_DIR ?= $(LLVM_PROJECT_ROOT)/build
LLVM_BIN ?= $(LLVM_BUILD_DIR)/bin

.PHONY: all isa sail emulator sv-decoder
.PHONY: docs docs-pdf docs-site sail-docs
.PHONY: emulator-isa-generate emulator-isa-check emulator-format emulator-test emulator-validate
.PHONY: test-fast test-hardware test-pr
.PHONY: llvm-sync llvm samples samples-check tiny-kernel clean-samples

all: isa sail emulator

isa: docs

sail: sail-docs

sv-decoder:
	$(PYTHON) -m engine artifacts generate systemverilog-package \
		systemverilog-instruction-decoder --output-root "$(SV_BUILD_DIR)"

emulator: emulator-isa-check
	$(CARGO) build --manifest-path "$(EMULATOR_MANIFEST)" --workspace --target-dir "$(EMULATOR_TARGET_DIR)"

docs:
	$(PYTHON) -m engine docs build --output-root "$(BUILD_DIR)"

docs-pdf:
	$(PYTHON) -m engine docs build --output-root "$(BUILD_DIR)"

docs-site:
	$(PYTHON) -m engine artifacts generate web-reference --output-root "$(BUILD_DIR)"

sail-docs:
	$(PYTHON) -m engine artifacts generate sail-model --output-root "$(SAIL_BUILD_DIR)"

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
	$(PYTHON) -m unittest $(ISA_PYTHON_TEST_MODULES)
	+$(MAKE) -j1 emulator-isa-check
	+$(MAKE) -j1 emulator-format
	$(CARGO) test --manifest-path "$(EMULATOR_MANIFEST)" --workspace \
		--exclude bedrock-lldb --exclude bedrock-gui \
		--target-dir "$(EMULATOR_TARGET_DIR)"

test-hardware:
	SV_TEST_ROOT="$(SV_TEST_ROOT)" \
		$(PYTHON) -m unittest isa.tests.test_systemverilog_decoder \
		isa.tests.test_systemverilog_architecture_artifacts

test-pr:
	+$(MAKE) -j1 test-fast
	+$(MAKE) -j1 test-hardware

llvm-sync:
	$(PYTHON) tools/sync_llvm_artifacts.py "$(LLVM_PROJECT_ROOT)"

llvm: llvm-sync
	$(MAKE) -C "$(LLVM_BUILD_DIR)" bin/clang bin/llc bin/lld \
		bin/llvm-mc bin/llvm-objcopy bin/llvm-objdump bin/llvm-readelf

samples:
	$(MAKE) -C samples LLVM_BIN="$(LLVM_BIN)" PYTHON="$(PYTHON)" all

samples-check:
	$(MAKE) -C samples LLVM_BIN="$(LLVM_BIN)" PYTHON="$(PYTHON)" check

tiny-kernel:
	$(MAKE) -C samples/tiny_kernel LLVM_BIN="$(LLVM_BIN)" PYTHON="$(PYTHON)" build

clean-samples:
	$(MAKE) -C samples clean
