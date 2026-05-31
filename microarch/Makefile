PYTHON ?= python3
BUILD_DIR ?= ../build/microarch

DOC_OUT := $(BUILD_DIR)/bedrock_microarchitecture.md
DOC_MANIFEST := src/manifest.txt
DOC_SRCS := $(wildcard src/*.md)

.PHONY: help doc clean

help:
	@printf '%s\n' 'Microarchitecture targets:'
	@printf '  %-10s %s\n' 'doc' 'Synthesize the microarchitecture document.'
	@printf '  %-10s %s\n' 'clean' 'Remove generated microarchitecture artifacts.'

doc: $(DOC_OUT)

$(DOC_OUT): $(DOC_MANIFEST) $(DOC_SRCS) tools/build_doc.py
	@mkdir -p "$(BUILD_DIR)"
	$(PYTHON) tools/build_doc.py --manifest $(DOC_MANIFEST) --src-dir src --output $(DOC_OUT)

clean:
	rm -rf "$(BUILD_DIR)"
