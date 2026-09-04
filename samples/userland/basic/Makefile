ifeq ($(strip $(LLVM_BIN)),)
ifneq ($(strip $(BEDROCK_LLVM_BIN)),)
LLVM_BIN := $(BEDROCK_LLVM_BIN)
else ifneq ($(strip $(BEDROCK_LLVM_ROOT)),)
LLVM_BIN := $(BEDROCK_LLVM_ROOT)/bin
endif
endif
OUTPUT_ROOT ?= $(abspath ../../../output/samples/userland/basic)

CLANG := $(LLVM_BIN)/clang
LLVM_MC := $(LLVM_BIN)/llvm-mc
LD_LLD := $(LLVM_BIN)/ld.lld
OBJDUMP := $(LLVM_BIN)/llvm-objdump

TARGET := basic
ELF := $(OUTPUT_ROOT)/$(TARGET).elf
DISASM := $(OUTPUT_ROOT)/$(TARGET).dis

C_SOURCES := main.c runtime.c tty.c program.c vm.c fp.c
ASM_SOURCES := brcrt.s
C_OBJECTS := $(C_SOURCES:%.c=$(OUTPUT_ROOT)/%.o)
ASM_OBJECTS := $(ASM_SOURCES:%.s=$(OUTPUT_ROOT)/%.o)
OBJECTS := $(ASM_OBJECTS) $(C_OBJECTS)

BASIC_CFLAGS ?= -O0
CFLAGS ?= $(BASIC_CFLAGS)
BEDROCK_CFLAGS := -target bedrock-unknown-unknown -ffreestanding -nostdlib $(CFLAGS)
BEDROCK_LDFLAGS := -m elf64bedrock -T basic.ld

.PHONY: all build disasm clean check-toolchain check-objdump

all: build

build: check-toolchain $(ELF)

disasm: check-toolchain check-objdump $(DISASM)

clean:
	rm -rf $(OUTPUT_ROOT)

check-toolchain:
	@test -x "$(CLANG)" || { \
		echo "Bedrock clang not found at $(CLANG)" >&2; \
		echo "set LLVM_BIN, BEDROCK_LLVM_BIN, or BEDROCK_LLVM_ROOT" >&2; \
		exit 1; \
	}
	@test -x "$(LLVM_MC)" || { \
		echo "Bedrock llvm-mc not found at $(LLVM_MC)" >&2; \
		echo "set LLVM_BIN, BEDROCK_LLVM_BIN, or BEDROCK_LLVM_ROOT" >&2; \
		exit 1; \
	}
	@test -x "$(LD_LLD)" || { \
		echo "Bedrock ld.lld not found at $(LD_LLD)" >&2; \
		echo "set LLVM_BIN, BEDROCK_LLVM_BIN, or BEDROCK_LLVM_ROOT" >&2; \
		exit 1; \
	}

check-objdump:
	@test -x "$(OBJDUMP)" || { \
		echo "Bedrock llvm-objdump not found at $(OBJDUMP)" >&2; \
		echo "set LLVM_BIN, BEDROCK_LLVM_BIN, or BEDROCK_LLVM_ROOT" >&2; \
		exit 1; \
	}

$(OUTPUT_ROOT)/.dir:
	mkdir -p $(OUTPUT_ROOT)
	touch $@

$(OUTPUT_ROOT)/%.o: %.c basic.h ../../common/bedrock_syscalls.h | $(OUTPUT_ROOT)/.dir check-toolchain
	$(CLANG) $(BEDROCK_CFLAGS) -c $< -o $@

$(OUTPUT_ROOT)/%.o: %.s | $(OUTPUT_ROOT)/.dir check-toolchain
	$(LLVM_MC) -triple=bedrock-unknown-unknown -filetype=obj $< -o $@

$(ELF): $(OBJECTS) basic.ld | check-toolchain
	$(LD_LLD) $(BEDROCK_LDFLAGS) $(OBJECTS) -o $@

$(DISASM): $(ELF) | check-objdump
	$(OBJDUMP) -d --no-show-raw-insn $< > $@
