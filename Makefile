.DEFAULT_GOAL := all

export PYTHONDONTWRITEBYTECODE := 1

PYTHON ?= python3
CARGO ?= cargo
LATEXMK ?= latexmk
PANDOC ?= pandoc
LATEXPAND ?= latexpand
MKDOCS ?= mkdocs

BUILD_DIR ?= build
SAIL_BUILD_DIR ?= $(BUILD_DIR)/sail-doc
EMULATOR_MANIFEST := emulator/Cargo.toml
EMULATOR_TARGET_DIR ?= $(abspath $(BUILD_DIR)/emulator-target)

.PHONY: all isa sail emulator
.PHONY: docs docs-pdf docs-site sail-docs
.PHONY: emulator-isa-generate emulator-isa-check emulator-format emulator-test emulator-validate

all: isa sail emulator

isa: docs

sail: sail-docs

emulator: emulator-isa-check
	$(CARGO) build --manifest-path "$(EMULATOR_MANIFEST)" --workspace --target-dir "$(EMULATOR_TARGET_DIR)"

docs:
	$(PYTHON) isa/tools/compile_documents.py --format all --output-root "$(BUILD_DIR)" --latexmk "$(LATEXMK)" --pandoc "$(PANDOC)" --latexpand "$(LATEXPAND)" --mkdocs "$(MKDOCS)"

docs-pdf:
	$(PYTHON) isa/tools/compile_documents.py --format pdf --output-root "$(BUILD_DIR)" --latexmk "$(LATEXMK)"

docs-site:
	$(PYTHON) isa/tools/compile_documents.py --format site --output-root "$(BUILD_DIR)" --latexmk "$(LATEXMK)" --pandoc "$(PANDOC)" --latexpand "$(LATEXPAND)" --mkdocs "$(MKDOCS)"

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

.NOTPARALLEL: emulator-validate
emulator-validate: emulator-isa-check emulator-format emulator-test
