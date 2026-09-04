LLVM_BIN ?= $(if $(BEDROCK_LLVM_BIN),$(BEDROCK_LLVM_BIN),$(if $(BEDROCK_LLVM_ROOT),$(BEDROCK_LLVM_ROOT)/bin))
OUTPUT_ROOT ?= $(abspath ../output/samples)
PYTHON ?= python3

CLANG := $(LLVM_BIN)/clang
LD_LLD := $(LLVM_BIN)/ld.lld
READELF := $(LLVM_BIN)/llvm-readelf

STANDALONE_NAMES := echo fixed3d
STANDALONE_ELFS := $(STANDALONE_NAMES:%=$(OUTPUT_ROOT)/%.elf)
SMALL_SOURCES := $(sort $(wildcard small/*.c))
SMALL_OBJECTS := $(patsubst small/%.c,$(OUTPUT_ROOT)/small/%.o,$(SMALL_SOURCES))
BASIC_ELF := $(OUTPUT_ROOT)/userland/basic/basic.elf
TINY_KERNEL_ELF := $(OUTPUT_ROOT)/tiny_kernel/tiny_kernel.elf

.DEFAULT_GOAL := all

.PHONY: all standalone small userland-basic tiny-kernel check clean
.PHONY: check-clang check-standalone-toolchain check-readelf

all: standalone small userland-basic tiny-kernel

check-clang:
	@test -x "$(CLANG)" || { \
		echo "Bedrock clang not found at $(CLANG)" >&2; \
		echo "set BEDROCK_LLVM_BIN or BEDROCK_LLVM_ROOT" >&2; \
		exit 1; \
	}

check-standalone-toolchain: check-clang
	@test -x "$(LD_LLD)" || { \
		echo "Bedrock ld.lld not found at $(LD_LLD)" >&2; \
		echo "set BEDROCK_LLVM_BIN or BEDROCK_LLVM_ROOT" >&2; \
		exit 1; \
	}

check-readelf:
	@test -x "$(READELF)" || { \
		echo "Bedrock llvm-readelf not found at $(READELF)" >&2; \
		echo "set BEDROCK_LLVM_BIN or BEDROCK_LLVM_ROOT" >&2; \
		exit 1; \
	}

standalone: check-standalone-toolchain $(STANDALONE_ELFS)

small: check-clang $(SMALL_OBJECTS)

userland-basic:
	$(MAKE) -C userland/basic LLVM_BIN="$(LLVM_BIN)" \
		OUTPUT_ROOT="$(OUTPUT_ROOT)/userland/basic" build

tiny-kernel:
	$(MAKE) -C tiny_kernel LLVM_BIN="$(LLVM_BIN)" PYTHON="$(PYTHON)" \
		OUTPUT_ROOT="$(OUTPUT_ROOT)/tiny_kernel" build

check: check-readelf all
	$(READELF) -h $(STANDALONE_ELFS) $(BASIC_ELF) \
		$(TINY_KERNEL_ELF) $(SMALL_OBJECTS)

clean:
	rm -rf $(OUTPUT_ROOT)
	$(MAKE) -C tiny_kernel PYTHON="$(PYTHON)" \
		OUTPUT_ROOT="$(OUTPUT_ROOT)/tiny_kernel" clean
	$(MAKE) -C userland/basic OUTPUT_ROOT="$(OUTPUT_ROOT)/userland/basic" clean

$(OUTPUT_ROOT):
	mkdir -p $@

$(OUTPUT_ROOT)/small:
	mkdir -p $@

$(OUTPUT_ROOT)/echo.elf: echo/main.c | $(OUTPUT_ROOT) check-standalone-toolchain
	$(CLANG) --target=bedrock-unknown-unknown -ffreestanding -nostdlib \
		--ld-path="$(LD_LLD)" -O2 -Wl,-e,_start -Wl,-Ttext=0x1000 \
		-Wl,--image-base=0 $< -o $@

$(OUTPUT_ROOT)/fixed3d.elf: fixed3d/main.c | $(OUTPUT_ROOT) check-standalone-toolchain
	$(CLANG) --target=bedrock-unknown-unknown -ffreestanding -nostdlib \
		--ld-path="$(LD_LLD)" -O2 -Wl,-e,_start -Wl,-Ttext=0x1000 \
		-Wl,--image-base=0 $< -o $@

$(OUTPUT_ROOT)/small/%.o: small/%.c | $(OUTPUT_ROOT)/small check-clang
	$(CLANG) --target=bedrock-unknown-unknown -ffreestanding -nostdlib -O2 \
		-std=gnu89 -Wno-implicit-int \
		-c $< -o $@
