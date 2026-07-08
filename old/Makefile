SUBDIRS := isa rtl qbe benchmarks
TARGET ?= help

.PHONY: help $(SUBDIRS) clean-build

help:
	@printf '%s\n' 'Top-level targets:'
	@printf '  %-14s %s\n' 'help' 'Show this summary and each subdirectory target summary.'
	@printf '  %-14s %s\n' 'isa' 'Run TARGET in isa/. Example: make isa TARGET=validate'
	@printf '  %-14s %s\n' 'rtl' 'Run TARGET in rtl/. Example: make rtl TARGET=decode-test'
	@printf '  %-14s %s\n' 'qbe' 'Run TARGET in qbe/. Example: make qbe TARGET=bedrock'
	@printf '  %-14s %s\n' 'benchmarks' 'Run TARGET in benchmarks/. Example: make benchmarks TARGET=arch-compare'
	@printf '  %-14s %s\n' 'clean-build' 'Remove all build/ artifacts.'
	@printf '\n%s\n' 'Subdirectory targets:'
	@for dir in $(SUBDIRS); do \
		printf '\n[%s]\n' "$$dir"; \
		$(MAKE) -s -C "$$dir" help; \
	done

$(SUBDIRS):
	$(MAKE) -C $@ $(TARGET)

clean-build:
	rm -rf build
