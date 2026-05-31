#ifndef BEDROCK_ASM_H
#define BEDROCK_ASM_H

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

#include "bedrock_asm_disasm.h"

#define BEDROCK_EMACHINE 0xffb0u

enum {
    BEDROCK_SHT_NULL = 0,
    BEDROCK_SHT_PROGBITS = 1,
    BEDROCK_SHT_SYMTAB = 2,
    BEDROCK_SHT_STRTAB = 3,
    BEDROCK_SHT_RELA = 4,
    BEDROCK_SHT_NOBITS = 8
};

enum {
    BEDROCK_SHF_WRITE = 0x1,
    BEDROCK_SHF_ALLOC = 0x2,
    BEDROCK_SHF_EXECINSTR = 0x4
};

enum {
    BEDROCK_STB_LOCAL = 0,
    BEDROCK_STB_GLOBAL = 1,
    BEDROCK_STB_WEAK = 2
};

enum {
    BEDROCK_STT_NOTYPE = 0,
    BEDROCK_STT_OBJECT = 1,
    BEDROCK_STT_FUNC = 2,
    BEDROCK_STT_SECTION = 3,
    BEDROCK_STT_FILE = 4,
    BEDROCK_STT_GNU_IFUNC = 10
};

typedef enum BedrockRelocType {
    BEDROCK_R_NONE = 0,
    BEDROCK_R_ABS8 = 1,
    BEDROCK_R_ABS16 = 2,
    BEDROCK_R_ABS32 = 3,
    BEDROCK_R_ABS64 = 4,
    BEDROCK_R_PCREL16 = 5,
    BEDROCK_R_PCREL32 = 6,
    BEDROCK_R_PCREL64 = 7,
    BEDROCK_R_WORD_PCREL16 = 8,
    BEDROCK_R_WORD_PCREL32 = 9,
    BEDROCK_R_IMM16 = 10,
    BEDROCK_R_IMM32 = 11,
    BEDROCK_R_IMM64 = 12,
    BEDROCK_R_DISP16 = 13,
    BEDROCK_R_DISP32 = 14,
    BEDROCK_R_DISP64 = 15,
    BEDROCK_R_SECTION_REL32 = 16,
    BEDROCK_R_SECTION_REL64 = 17,
    BEDROCK_R_CALL_TARGET = 18,
    BEDROCK_R_JMP_TARGET = 19,
    BEDROCK_R_LONG_CONTROL_TARGET = 20,
    BEDROCK_R_GOT64 = 21,
    BEDROCK_R_GOTPCREL32 = 22,
    BEDROCK_R_GOTPCREL64 = 23,
    BEDROCK_R_GOTOFF32 = 24,
    BEDROCK_R_GOTOFF64 = 25,
    BEDROCK_R_GOT_BASE_PCREL32 = 26,
    BEDROCK_R_GOT_BASE_PCREL64 = 27,
    BEDROCK_R_PLT32 = 28,
    BEDROCK_R_PLT64 = 29,
    BEDROCK_R_RELATIVE = 30,
    BEDROCK_R_GLOB_DAT = 31,
    BEDROCK_R_JUMP_SLOT = 32,
    BEDROCK_R_COPY = 33,
    BEDROCK_R_IRELATIVE = 34,
    BEDROCK_R_TLS_OFFSET32 = 35,
    BEDROCK_R_TLS_OFFSET64 = 36,
    BEDROCK_R_TLSDESC_GOTPCREL32 = 37,
    BEDROCK_R_TLSDESC_GOTPCREL64 = 38,
    BEDROCK_R_TLSDESC_CALL = 39,
    BEDROCK_R_TLSDESC = 40
} BedrockRelocType;

typedef struct BedrockBuffer {
    uint8_t *data;
    size_t size;
    size_t capacity;
} BedrockBuffer;

typedef struct BedrockReloc {
    size_t offset;
    int symbol;
    unsigned type;
    int64_t addend;
} BedrockReloc;

typedef struct BedrockSection {
    char *name;
    uint32_t type;
    uint64_t flags;
    uint64_t align;
    BedrockBuffer data;
    size_t logical_size;
    BedrockReloc *relocs;
    size_t reloc_count;
    size_t reloc_capacity;
    unsigned sh_index;
    unsigned rela_sh_index;
} BedrockSection;

typedef struct BedrockSymbol {
    char *name;
    int section;
    uint64_t value;
    uint64_t size;
    unsigned bind;
    unsigned type;
    unsigned visibility;
    int defined;
    unsigned symtab_index;
} BedrockSymbol;

typedef struct BedrockAsm {
    BedrockSection *sections;
    size_t section_count;
    size_t section_capacity;
    BedrockSymbol *symbols;
    size_t symbol_count;
    size_t symbol_capacity;
    int current_section;
    const char *input_name;
    unsigned line_number;
    unsigned error_count;
} BedrockAsm;

typedef struct BedrockExpr {
    int is_symbol;
    int symbol;
    int64_t value;
    unsigned reloc_type;
} BedrockExpr;

void bedrock_asm_init(BedrockAsm *ctx);
void bedrock_asm_free(BedrockAsm *ctx);
void bedrock_asm_error(BedrockAsm *ctx, const char *fmt, ...);

BedrockSection *bedrock_asm_section(BedrockAsm *ctx, int index);
BedrockSection *bedrock_asm_current_section(BedrockAsm *ctx);
int bedrock_asm_switch_section(BedrockAsm *ctx, const char *name);
int bedrock_asm_find_symbol(BedrockAsm *ctx, const char *name);
int bedrock_asm_get_symbol(BedrockAsm *ctx, const char *name);
void bedrock_asm_define_symbol(BedrockAsm *ctx, const char *name);
void bedrock_asm_set_symbol_bind(BedrockAsm *ctx, const char *name, unsigned bind);
void bedrock_asm_set_symbol_type(BedrockAsm *ctx, const char *name, unsigned type);
void bedrock_asm_set_symbol_visibility(BedrockAsm *ctx, const char *name, unsigned visibility);
void bedrock_asm_set_symbol_size(BedrockAsm *ctx, const char *name, uint64_t size);

int bedrock_buffer_reserve(BedrockBuffer *buffer, size_t extra);
int bedrock_section_emit(BedrockSection *section, const void *data, size_t size);
int bedrock_section_emit_zero(BedrockSection *section, size_t size);
int bedrock_section_align(BedrockSection *section, size_t align);
int bedrock_section_add_reloc(BedrockSection *section, size_t offset, int symbol, unsigned type, int64_t addend);

int bedrock_asm_parse_file(BedrockAsm *ctx, const char *path);
int bedrock_asm_write_elf64(BedrockAsm *ctx, const char *path);
int bedrock_reloc_type_by_name(const char *name, unsigned *type, unsigned *width_bits);
unsigned bedrock_default_abs_reloc_for_size(size_t size);
unsigned bedrock_reloc_width_bits(unsigned type);

#endif
