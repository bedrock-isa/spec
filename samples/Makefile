LLVM_BIN ?= $(if $(BEDROCK_LLVM_BIN),$(BEDROCK_LLVM_BIN),$(if $(BEDROCK_LLVM_ROOT),$(BEDROCK_LLVM_ROOT)/bin,$(abspath ../../llvm-project/build/bin)))
BUILD_DIR ?= build
PYTHON ?= python3

CLANG := $(LLVM_BIN)/clang
READELF := $(LLVM_BIN)/llvm-readelf

STANDALONE_NAMES := echo fixed3d
STANDALONE_ELFS := $(STANDALONE_NAMES:%=$(BUILD_DIR)/%.elf)
SMALL_SOURCES := $(sort $(wildcard small/*.c))
SMALL_OBJECTS := $(patsubst small/%.c,$(BUILD_DIR)/small/%.o,$(SMALL_SOURCES))

.DEFAULT_GOAL := all

.PHONY: all standalone small tiny-kernel check clean

all: standalone small tiny-kernel

standalone: $(STANDALONE_ELFS)

small: $(SMALL_OBJECTS)

tiny-kernel:
	$(MAKE) -C tiny_kernel LLVM_BIN="$(LLVM_BIN)" PYTHON="$(PYTHON)" build

check: all
	$(READELF) -h $(BUILD_DIR)/echo.elf
	$(READELF) -h $(BUILD_DIR)/fixed3d.elf
	$(READELF) -h tiny_kernel/build/tiny_kernel.elf

clean:
	rm -rf $(BUILD_DIR)
	$(MAKE) -C tiny_kernel PYTHON="$(PYTHON)" clean
	$(MAKE) -C userland/basic clean

$(BUILD_DIR):
	mkdir -p $@

$(BUILD_DIR)/small:
	mkdir -p $@

$(BUILD_DIR)/echo.elf: echo/main.c | $(BUILD_DIR)
	$(CLANG) --target=bedrock-unknown-none -ffreestanding -nostdlib \
		-fuse-ld=lld -O2 -Wl,-e,_start -Wl,-Ttext=0x1000 \
		-Wl,--image-base=0 $< -o $@

$(BUILD_DIR)/fixed3d.elf: fixed3d/main.c | $(BUILD_DIR)
	$(CLANG) --target=bedrock-unknown-none -ffreestanding -nostdlib \
		-fuse-ld=lld -O2 -Wl,-e,_start -Wl,-Ttext=0x1000 \
		-Wl,--image-base=0 $< -o $@

$(BUILD_DIR)/small/%.o: small/%.c | $(BUILD_DIR)/small
	$(CLANG) --target=bedrock-unknown-none -ffreestanding -nostdlib -O2 \
		-std=gnu89 -Wno-implicit-int \
		-c $< -o $@
