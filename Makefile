.DEFAULT_GOAL := all

export PYTHONDONTWRITEBYTECODE := 1

PYTHON ?= python3
CARGO ?= cargo
LATEXMK ?= latexmk
PANDOC ?= pandoc
LATEXPAND ?= latexpand
MKDOCS ?= mkdocs
export LATEXMK PANDOC LATEXPAND MKDOCS

BUILD_DIR ?= build
SAIL_BUILD_DIR ?= $(BUILD_DIR)/sail-doc
SV_BUILD_DIR ?= $(BUILD_DIR)/systemverilog-decoder
SV_TEST_ROOT ?= $(SV_BUILD_DIR)/tests
EMULATOR_MANIFEST := emulator/Cargo.toml
EMULATOR_TARGET_DIR ?= $(abspath $(BUILD_DIR)/emulator-target)
ISA_PYTHON_TEST_PATHS := $(shell find isa/tools -type f -name 'test_*.py' ! -path '*/systemverilog/*' -print)
ISA_PYTHON_TEST_MODULES := $(sort $(subst /,.,$(patsubst %.py,%,$(ISA_PYTHON_TEST_PATHS))))

.PHONY: all isa sail emulator sv-decoder
.PHONY: docs docs-pdf docs-site sail-docs
.PHONY: emulator-isa-generate emulator-isa-check emulator-format emulator-test emulator-validate
.PHONY: test-fast test-hardware test-pr

all: isa sail emulator

isa: docs

sail: sail-docs

sv-decoder:
	$(PYTHON) isa/tools/systemverilog/generate_decoder.py "$(SV_BUILD_DIR)"

emulator: emulator-isa-check
	$(CARGO) build --manifest-path "$(EMULATOR_MANIFEST)" --workspace --target-dir "$(EMULATOR_TARGET_DIR)"

docs:
	$(PYTHON) isa/tools/compile_documents.py --format all --output-root "$(BUILD_DIR)"

docs-pdf:
	$(PYTHON) isa/tools/compile_documents.py --format pdf --output-root "$(BUILD_DIR)"

docs-site:
	$(PYTHON) isa/tools/compile_documents.py --format site --output-root "$(BUILD_DIR)"

sail-docs:
	$(PYTHON) isa/tools/sail/build_docs.py "$(SAIL_BUILD_DIR)"

emulator-isa-generate:
	PYTHON="$(PYTHON)" $(CARGO) check --manifest-path "$(EMULATOR_MANIFEST)" -p bedrock-isa --target-dir "$(EMULATOR_TARGET_DIR)"

emulator-isa-check: emulator-isa-generate
	cd emulator && $(PYTHON) -m unittest tools/test_gen_isa.py

emulator-format:
	$(CARGO) fmt --manifest-path "$(EMULATOR_MANIFEST)" --all -- --check

emulator-test:
	$(CARGO) test --manifest-path "$(EMULATOR_MANIFEST)" --workspace --target-dir "$(EMULATOR_TARGET_DIR)"

emulator-validate:
	+$(MAKE) -j1 emulator-isa-check emulator-format emulator-test

test-fast:
	$(PYTHON) isa/tools/validate_isa.py
	$(PYTHON) isa/tools/validate_conformance.py
	$(PYTHON) -m unittest $(ISA_PYTHON_TEST_MODULES)
	+$(MAKE) -j1 emulator-isa-check
	+$(MAKE) -j1 emulator-format
	$(CARGO) test --manifest-path "$(EMULATOR_MANIFEST)" --workspace \
		--exclude bedrock-lldb --exclude bedrock-gui \
		--target-dir "$(EMULATOR_TARGET_DIR)"

test-hardware:
	SV_TEST_ROOT="$(SV_TEST_ROOT)" \
		$(PYTHON) -m unittest isa.tools.systemverilog.test_generation

test-pr:
	+$(MAKE) -j1 test-fast
	+$(MAKE) -j1 test-hardware
