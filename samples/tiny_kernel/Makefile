ifeq ($(strip $(LLVM_BIN)),)
ifneq ($(strip $(BEDROCK_LLVM_BIN)),)
LLVM_BIN := $(BEDROCK_LLVM_BIN)
else ifneq ($(strip $(BEDROCK_LLVM_ROOT)),)
LLVM_BIN := $(BEDROCK_LLVM_ROOT)/bin
endif
endif
OUTPUT_ROOT ?= $(abspath ../../output/samples/tiny_kernel)
PYTHON ?= python3

CLANG := $(LLVM_BIN)/clang
LLVM_MC := $(LLVM_BIN)/llvm-mc
LD_LLD := $(LLVM_BIN)/ld.lld
OBJCOPY := $(LLVM_BIN)/llvm-objcopy
OBJDUMP := $(LLVM_BIN)/llvm-objdump

TARGET := tiny_kernel
ELF := $(OUTPUT_ROOT)/$(TARGET).elf
DISASM := $(OUTPUT_ROOT)/$(TARGET).dis
BASIC_DIR := ../userland/basic
APP_DIR := ../userland/apps
BASIC_ELF := $(OUTPUT_ROOT)/basic.elf
BASIC_PACKED_ELF := $(OUTPUT_ROOT)/basic-packed.elf
BASIC_IMAGE_C := $(OUTPUT_ROOT)/basic_image.c
BASIC_IMAGE_OBJECT := $(OUTPUT_ROOT)/basic_image.o
APP_NAMES := demo math sort mem fault halt far pfault sfault
APP_IMAGE_OBJECTS := $(APP_NAMES:%=$(OUTPUT_ROOT)/%-image.o)

C_SOURCES := app_loader.c display.c kernel.c memory.c process.c shell.c syscall.c user.c
ASM_SOURCES := boot.s user_entry.s
C_OBJECTS := $(C_SOURCES:%.c=$(OUTPUT_ROOT)/%.o)
ASM_OBJECTS := $(ASM_SOURCES:%.s=$(OUTPUT_ROOT)/%.o)
OBJECTS := $(ASM_OBJECTS) $(C_OBJECTS) $(BASIC_IMAGE_OBJECT) $(APP_IMAGE_OBJECTS)
BASIC_C_SOURCES := $(BASIC_DIR)/main.c $(BASIC_DIR)/runtime.c $(BASIC_DIR)/tty.c
BASIC_ASM_SOURCES := $(BASIC_DIR)/brcrt.s
BASIC_C_OBJECTS := $(OUTPUT_ROOT)/basic-main.o $(OUTPUT_ROOT)/basic-runtime.o $(OUTPUT_ROOT)/basic-tty.o $(OUTPUT_ROOT)/basic-program.o $(OUTPUT_ROOT)/basic-vm.o $(OUTPUT_ROOT)/basic-fp.o
BASIC_ASM_OBJECTS := $(OUTPUT_ROOT)/basic-brcrt.o
BASIC_OBJECTS := $(BASIC_ASM_OBJECTS) $(BASIC_C_OBJECTS)
APP_COMMON_OBJECTS = $(OUTPUT_ROOT)/$(1)-brcrt.o $(OUTPUT_ROOT)/$(1)-runtime.o $(OUTPUT_ROOT)/$(1)-main.o

CFLAGS ?= -O2
BEDROCK_CFLAGS := -target bedrock-unknown-unknown -ffreestanding -nostdlib $(CFLAGS)
BASIC_CFLAGS ?= -O0
BASIC_BEDROCK_CFLAGS := -target bedrock-unknown-unknown -ffreestanding -nostdlib $(BASIC_CFLAGS)
APP_CFLAGS ?= -O2
APP_BEDROCK_CFLAGS := -target bedrock-unknown-unknown -ffreestanding -nostdlib $(APP_CFLAGS)
BEDROCK_LDFLAGS := -m elf64bedrock -T tiny_kernel.ld

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
	@test -x "$(OBJCOPY)" || { \
		echo "Bedrock llvm-objcopy not found at $(OBJCOPY)" >&2; \
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

$(OUTPUT_ROOT)/%.o: %.c tiny_kernel.h | $(OUTPUT_ROOT)/.dir check-toolchain
	$(CLANG) $(BEDROCK_CFLAGS) -c $< -o $@

$(OUTPUT_ROOT)/%.o: %.s | $(OUTPUT_ROOT)/.dir check-toolchain
	$(LLVM_MC) -triple=bedrock-unknown-unknown -filetype=obj $< -o $@

$(OUTPUT_ROOT)/basic-main.o: $(BASIC_DIR)/main.c $(BASIC_DIR)/basic.h ../common/bedrock_syscalls.h | $(OUTPUT_ROOT)/.dir check-toolchain
	$(CLANG) $(BASIC_BEDROCK_CFLAGS) -c $< -o $@

$(OUTPUT_ROOT)/basic-runtime.o: $(BASIC_DIR)/runtime.c $(BASIC_DIR)/basic.h ../common/bedrock_syscalls.h | $(OUTPUT_ROOT)/.dir check-toolchain
	$(CLANG) $(BASIC_BEDROCK_CFLAGS) -c $< -o $@

$(OUTPUT_ROOT)/basic-tty.o: $(BASIC_DIR)/tty.c $(BASIC_DIR)/basic.h ../common/bedrock_syscalls.h | $(OUTPUT_ROOT)/.dir check-toolchain
	$(CLANG) $(BASIC_BEDROCK_CFLAGS) -c $< -o $@

$(OUTPUT_ROOT)/basic-program.o: $(BASIC_DIR)/program.c $(BASIC_DIR)/basic.h ../common/bedrock_syscalls.h | $(OUTPUT_ROOT)/.dir check-toolchain
	$(CLANG) $(BASIC_BEDROCK_CFLAGS) -c $< -o $@

$(OUTPUT_ROOT)/basic-vm.o: $(BASIC_DIR)/vm.c $(BASIC_DIR)/basic.h ../common/bedrock_syscalls.h | $(OUTPUT_ROOT)/.dir check-toolchain
	$(CLANG) $(BASIC_BEDROCK_CFLAGS) -c $< -o $@

$(OUTPUT_ROOT)/basic-fp.o: $(BASIC_DIR)/fp.c $(BASIC_DIR)/basic.h ../common/bedrock_syscalls.h | $(OUTPUT_ROOT)/.dir check-toolchain
	$(CLANG) $(BASIC_BEDROCK_CFLAGS) -c $< -o $@

$(OUTPUT_ROOT)/basic-brcrt.o: $(BASIC_DIR)/brcrt.s | $(OUTPUT_ROOT)/.dir check-toolchain
	$(LLVM_MC) -triple=bedrock-unknown-unknown -filetype=obj $< -o $@

$(BASIC_ELF): $(BASIC_OBJECTS) $(BASIC_DIR)/basic.ld | check-toolchain
	$(LD_LLD) -m elf64bedrock -T $(BASIC_DIR)/basic.ld $(BASIC_OBJECTS) -o $@

$(BASIC_PACKED_ELF): $(BASIC_ELF) | check-toolchain
	$(OBJCOPY) --strip-all $< $@

$(BASIC_IMAGE_C): $(BASIC_PACKED_ELF) ../common/bin2c.py
	$(PYTHON) ../common/bin2c.py $< g_basic_app_elf > $@

$(BASIC_IMAGE_OBJECT): $(BASIC_IMAGE_C) tiny_kernel.h | $(OUTPUT_ROOT)/.dir check-toolchain
	$(CLANG) $(BEDROCK_CFLAGS) -I. -c $< -o $@

define APP_TEMPLATE
$(OUTPUT_ROOT)/$(1)-brcrt.o: $$(APP_DIR)/brcrt.s | $$(OUTPUT_ROOT)/.dir check-toolchain
	$$(LLVM_MC) -triple=bedrock-unknown-unknown -filetype=obj $$< -o $$@

$(OUTPUT_ROOT)/$(1)-runtime.o: $$(APP_DIR)/runtime.c $$(APP_DIR)/app.h ../common/bedrock_syscalls.h | $$(OUTPUT_ROOT)/.dir check-toolchain
	$$(CLANG) $$(APP_BEDROCK_CFLAGS) -c $$< -o $$@

$(OUTPUT_ROOT)/$(1)-main.o: $$(APP_DIR)/$(1).c $$(APP_DIR)/app.h ../common/bedrock_syscalls.h | $$(OUTPUT_ROOT)/.dir check-toolchain
	$$(CLANG) $$(APP_BEDROCK_CFLAGS) -c $$< -o $$@

$(OUTPUT_ROOT)/$(1).elf: $$(call APP_COMMON_OBJECTS,$(1)) $$(APP_DIR)/app.ld | check-toolchain
	$$(LD_LLD) -m elf64bedrock -T $$(APP_DIR)/app.ld $$(call APP_COMMON_OBJECTS,$(1)) -o $$@

$(OUTPUT_ROOT)/$(1)-packed.elf: $(OUTPUT_ROOT)/$(1).elf | check-toolchain
	$$(OBJCOPY) --strip-all $$< $$@

$(OUTPUT_ROOT)/$(1)_image.c: $(OUTPUT_ROOT)/$(1)-packed.elf ../common/bin2c.py
	$$(PYTHON) ../common/bin2c.py $$< g_$(1)_app_elf > $$@

$(OUTPUT_ROOT)/$(1)-image.o: $(OUTPUT_ROOT)/$(1)_image.c tiny_kernel.h | $$(OUTPUT_ROOT)/.dir check-toolchain
	$$(CLANG) $$(BEDROCK_CFLAGS) -I. -c $$< -o $$@
endef

$(foreach app,$(APP_NAMES),$(eval $(call APP_TEMPLATE,$(app))))

$(ELF): $(OBJECTS) tiny_kernel.ld | check-toolchain
	$(LD_LLD) $(BEDROCK_LDFLAGS) $(OBJECTS) -o $@

$(DISASM): $(ELF) | check-objdump
	$(OBJDUMP) -d --no-show-raw-insn $< > $@
