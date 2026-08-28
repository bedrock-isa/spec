ifeq ($(strip $(LLVM_BIN)),)
ifneq ($(strip $(BEDROCK_LLVM_BIN)),)
LLVM_BIN := $(BEDROCK_LLVM_BIN)
else ifneq ($(strip $(BEDROCK_LLVM_ROOT)),)
LLVM_BIN := $(BEDROCK_LLVM_ROOT)/bin
else
LLVM_BIN := $(abspath ../../../llvm-project/build/bin)
endif
endif
BUILD_DIR ?= build
PYTHON ?= python3

CLANG := $(LLVM_BIN)/clang
LLVM_MC := $(LLVM_BIN)/llvm-mc
LD_LLD := $(LLVM_BIN)/ld.lld
OBJCOPY := $(LLVM_BIN)/llvm-objcopy
OBJDUMP := $(LLVM_BIN)/llvm-objdump

TARGET := tiny_kernel
ELF := $(BUILD_DIR)/$(TARGET).elf
DISASM := $(BUILD_DIR)/$(TARGET).dis
BASIC_DIR := ../userland/basic
APP_DIR := ../userland/apps
BASIC_ELF := $(BUILD_DIR)/basic.elf
BASIC_PACKED_ELF := $(BUILD_DIR)/basic-packed.elf
BASIC_IMAGE_C := $(BUILD_DIR)/basic_image.c
BASIC_IMAGE_OBJECT := $(BUILD_DIR)/basic_image.o
APP_NAMES := demo math sort mem fault halt far pfault sfault
APP_IMAGE_OBJECTS := $(APP_NAMES:%=$(BUILD_DIR)/%-image.o)

C_SOURCES := app_loader.c display.c kernel.c memory.c process.c shell.c syscall.c user.c
ASM_SOURCES := boot.s user_entry.s
C_OBJECTS := $(C_SOURCES:%.c=$(BUILD_DIR)/%.o)
ASM_OBJECTS := $(ASM_SOURCES:%.s=$(BUILD_DIR)/%.o)
OBJECTS := $(ASM_OBJECTS) $(C_OBJECTS) $(BASIC_IMAGE_OBJECT) $(APP_IMAGE_OBJECTS)
BASIC_C_SOURCES := $(BASIC_DIR)/main.c $(BASIC_DIR)/runtime.c $(BASIC_DIR)/tty.c
BASIC_ASM_SOURCES := $(BASIC_DIR)/brcrt.s
BASIC_C_OBJECTS := $(BUILD_DIR)/basic-main.o $(BUILD_DIR)/basic-runtime.o $(BUILD_DIR)/basic-tty.o $(BUILD_DIR)/basic-program.o $(BUILD_DIR)/basic-vm.o $(BUILD_DIR)/basic-fp.o
BASIC_ASM_OBJECTS := $(BUILD_DIR)/basic-brcrt.o
BASIC_OBJECTS := $(BASIC_ASM_OBJECTS) $(BASIC_C_OBJECTS)
APP_COMMON_OBJECTS = $(BUILD_DIR)/$(1)-brcrt.o $(BUILD_DIR)/$(1)-runtime.o $(BUILD_DIR)/$(1)-main.o

CFLAGS ?= -O2
BEDROCK_CFLAGS := -target bedrock-unknown-unknown -ffreestanding -nostdlib $(CFLAGS)
BASIC_CFLAGS ?= -O0
BASIC_BEDROCK_CFLAGS := -target bedrock-unknown-unknown -ffreestanding -nostdlib $(BASIC_CFLAGS)
APP_CFLAGS ?= -O2
APP_BEDROCK_CFLAGS := -target bedrock-unknown-unknown -ffreestanding -nostdlib $(APP_CFLAGS)
BEDROCK_LDFLAGS := -m elf64bedrock -T tiny_kernel.ld

.PHONY: all build disasm clean test check-toolchain

all: build

build: check-toolchain $(ELF)

disasm: $(DISASM)

test: build
	PYTHON="$(PYTHON)" cargo test --release --manifest-path ../../emulator/Cargo.toml -p bedrock-machine --test llvm_toolchain machine_executes_tiny_kernel_sample_with_syscall_and_event_return -- --ignored --nocapture

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

$(BUILD_DIR)/%.o: %.c tiny_kernel.h | $(BUILD_DIR)/.dir
	$(CLANG) $(BEDROCK_CFLAGS) -c $< -o $@

$(BUILD_DIR)/%.o: %.s | $(BUILD_DIR)/.dir
	$(LLVM_MC) -triple=bedrock-unknown-unknown -filetype=obj $< -o $@

$(BUILD_DIR)/basic-main.o: $(BASIC_DIR)/main.c $(BASIC_DIR)/basic.h ../common/bedrock_syscalls.h | $(BUILD_DIR)/.dir
	$(CLANG) $(BASIC_BEDROCK_CFLAGS) -c $< -o $@

$(BUILD_DIR)/basic-runtime.o: $(BASIC_DIR)/runtime.c $(BASIC_DIR)/basic.h ../common/bedrock_syscalls.h | $(BUILD_DIR)/.dir
	$(CLANG) $(BASIC_BEDROCK_CFLAGS) -c $< -o $@

$(BUILD_DIR)/basic-tty.o: $(BASIC_DIR)/tty.c $(BASIC_DIR)/basic.h ../common/bedrock_syscalls.h | $(BUILD_DIR)/.dir
	$(CLANG) $(BASIC_BEDROCK_CFLAGS) -c $< -o $@

$(BUILD_DIR)/basic-program.o: $(BASIC_DIR)/program.c $(BASIC_DIR)/basic.h ../common/bedrock_syscalls.h | $(BUILD_DIR)/.dir
	$(CLANG) $(BASIC_BEDROCK_CFLAGS) -c $< -o $@

$(BUILD_DIR)/basic-vm.o: $(BASIC_DIR)/vm.c $(BASIC_DIR)/basic.h ../common/bedrock_syscalls.h | $(BUILD_DIR)/.dir
	$(CLANG) $(BASIC_BEDROCK_CFLAGS) -c $< -o $@

$(BUILD_DIR)/basic-fp.o: $(BASIC_DIR)/fp.c $(BASIC_DIR)/basic.h ../common/bedrock_syscalls.h | $(BUILD_DIR)/.dir
	$(CLANG) $(BASIC_BEDROCK_CFLAGS) -c $< -o $@

$(BUILD_DIR)/basic-brcrt.o: $(BASIC_DIR)/brcrt.s | $(BUILD_DIR)/.dir
	$(LLVM_MC) -triple=bedrock-unknown-unknown -filetype=obj $< -o $@

$(BASIC_ELF): $(BASIC_OBJECTS) $(BASIC_DIR)/basic.ld
	$(LD_LLD) -m elf64bedrock -T $(BASIC_DIR)/basic.ld $(BASIC_OBJECTS) -o $@

$(BASIC_PACKED_ELF): $(BASIC_ELF)
	$(OBJCOPY) --strip-all $< $@

$(BASIC_IMAGE_C): $(BASIC_PACKED_ELF) ../common/bin2c.py
	$(PYTHON) ../common/bin2c.py $< g_basic_app_elf > $@

$(BASIC_IMAGE_OBJECT): $(BASIC_IMAGE_C) tiny_kernel.h | $(BUILD_DIR)/.dir
	$(CLANG) $(BEDROCK_CFLAGS) -I. -c $< -o $@

define APP_TEMPLATE
$(BUILD_DIR)/$(1)-brcrt.o: $$(APP_DIR)/brcrt.s | $$(BUILD_DIR)/.dir
	$$(LLVM_MC) -triple=bedrock-unknown-unknown -filetype=obj $$< -o $$@

$(BUILD_DIR)/$(1)-runtime.o: $$(APP_DIR)/runtime.c $$(APP_DIR)/app.h ../common/bedrock_syscalls.h | $$(BUILD_DIR)/.dir
	$$(CLANG) $$(APP_BEDROCK_CFLAGS) -c $$< -o $$@

$(BUILD_DIR)/$(1)-main.o: $$(APP_DIR)/$(1).c $$(APP_DIR)/app.h ../common/bedrock_syscalls.h | $$(BUILD_DIR)/.dir
	$$(CLANG) $$(APP_BEDROCK_CFLAGS) -c $$< -o $$@

$(BUILD_DIR)/$(1).elf: $$(call APP_COMMON_OBJECTS,$(1)) $$(APP_DIR)/app.ld
	$$(LD_LLD) -m elf64bedrock -T $$(APP_DIR)/app.ld $$(call APP_COMMON_OBJECTS,$(1)) -o $$@

$(BUILD_DIR)/$(1)-packed.elf: $(BUILD_DIR)/$(1).elf
	$$(OBJCOPY) --strip-all $$< $$@

$(BUILD_DIR)/$(1)_image.c: $(BUILD_DIR)/$(1)-packed.elf ../common/bin2c.py
	$$(PYTHON) ../common/bin2c.py $$< g_$(1)_app_elf > $$@

$(BUILD_DIR)/$(1)-image.o: $(BUILD_DIR)/$(1)_image.c tiny_kernel.h | $$(BUILD_DIR)/.dir
	$$(CLANG) $$(BEDROCK_CFLAGS) -I. -c $$< -o $$@
endef

$(foreach app,$(APP_NAMES),$(eval $(call APP_TEMPLATE,$(app))))

$(ELF): $(OBJECTS) tiny_kernel.ld
	$(LD_LLD) $(BEDROCK_LDFLAGS) $(OBJECTS) -o $@

$(DISASM): $(ELF)
	$(OBJDUMP) -d --no-show-raw-insn $< > $@
