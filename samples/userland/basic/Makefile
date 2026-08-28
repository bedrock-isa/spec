ifeq ($(strip $(LLVM_BIN)),)
ifneq ($(strip $(BEDROCK_LLVM_BIN)),)
LLVM_BIN := $(BEDROCK_LLVM_BIN)
else ifneq ($(strip $(BEDROCK_LLVM_ROOT)),)
LLVM_BIN := $(BEDROCK_LLVM_ROOT)/bin
else
LLVM_BIN := $(abspath ../../../../llvm-project/build/bin)
endif
endif
BUILD_DIR ?= build

CLANG := $(LLVM_BIN)/clang
LLVM_MC := $(LLVM_BIN)/llvm-mc
LD_LLD := $(LLVM_BIN)/ld.lld
OBJDUMP := $(LLVM_BIN)/llvm-objdump

TARGET := basic
ELF := $(BUILD_DIR)/$(TARGET).elf
DISASM := $(BUILD_DIR)/$(TARGET).dis

C_SOURCES := main.c runtime.c tty.c program.c vm.c fp.c
ASM_SOURCES := brcrt.s
C_OBJECTS := $(C_SOURCES:%.c=$(BUILD_DIR)/%.o)
ASM_OBJECTS := $(ASM_SOURCES:%.s=$(BUILD_DIR)/%.o)
OBJECTS := $(ASM_OBJECTS) $(C_OBJECTS)

BASIC_CFLAGS ?= -O0
CFLAGS ?= $(BASIC_CFLAGS)
BEDROCK_CFLAGS := -target bedrock-unknown-unknown -ffreestanding -nostdlib $(CFLAGS)
BEDROCK_LDFLAGS := -m elf64bedrock -T basic.ld

.PHONY: all build disasm clean check-toolchain

all: build

build: check-toolchain $(ELF)

disasm: $(DISASM)

clean:
	rm -rf $(BUILD_DIR)

check-toolchain:
	@test -x "$(CLANG)" || { \
		echo "Bedrock clang not found at $(CLANG)" >&2; \
		echo "build LLVM first or set LLVM_BIN/BEDROCK_LLVM_BIN/BEDROCK_LLVM_ROOT" >&2; \
		exit 1; \
	}

$(BUILD_DIR)/.dir:
	mkdir -p $(BUILD_DIR)
	touch $@

$(BUILD_DIR)/%.o: %.c basic.h ../../common/bedrock_syscalls.h | $(BUILD_DIR)/.dir
	$(CLANG) $(BEDROCK_CFLAGS) -c $< -o $@

$(BUILD_DIR)/%.o: %.s | $(BUILD_DIR)/.dir
	$(LLVM_MC) -triple=bedrock-unknown-unknown -filetype=obj $< -o $@

$(ELF): $(OBJECTS) basic.ld
	$(LD_LLD) $(BEDROCK_LDFLAGS) $(OBJECTS) -o $@

$(DISASM): $(ELF)
	$(OBJDUMP) -d --no-show-raw-insn $< > $@
