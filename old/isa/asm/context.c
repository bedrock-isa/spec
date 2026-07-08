#include "bedrock_asm.h"

#include <stdarg.h>
#include <stdlib.h>
#include <string.h>

static char *bedrock_strdup(const char *text)
{
    size_t len = strlen(text) + 1u;
    char *copy = (char *)malloc(len);
    if (copy != 0) {
        memcpy(copy, text, len);
    }
    return copy;
}

static int reserve_bytes(void **ptr, size_t *capacity, size_t elem_size, size_t count)
{
    size_t new_capacity;
    void *new_ptr;
    if (count <= *capacity) {
        return 1;
    }
    new_capacity = *capacity == 0u ? 8u : *capacity;
    while (new_capacity < count) {
        new_capacity *= 2u;
    }
    new_ptr = realloc(*ptr, new_capacity * elem_size);
    if (new_ptr == 0) {
        return 0;
    }
    *ptr = new_ptr;
    *capacity = new_capacity;
    return 1;
}

static void default_section_attrs(const char *name, uint32_t *type, uint64_t *flags, uint64_t *align)
{
    *type = BEDROCK_SHT_PROGBITS;
    *flags = 0;
    *align = 1;
    if (strcmp(name, ".text") == 0 || strcmp(name, ".init") == 0 || strcmp(name, ".fini") == 0 || strcmp(name, ".plt") == 0) {
        *flags = BEDROCK_SHF_ALLOC | BEDROCK_SHF_EXECINSTR;
        *align = 2;
        return;
    }
    if (strcmp(name, ".rodata") == 0) {
        *flags = BEDROCK_SHF_ALLOC;
        *align = 8;
        return;
    }
    if (strcmp(name, ".data") == 0 || strcmp(name, ".got") == 0 || strcmp(name, ".got.plt") == 0) {
        *flags = BEDROCK_SHF_ALLOC | BEDROCK_SHF_WRITE;
        *align = 8;
        return;
    }
    if (strcmp(name, ".bss") == 0) {
        *type = BEDROCK_SHT_NOBITS;
        *flags = BEDROCK_SHF_ALLOC | BEDROCK_SHF_WRITE;
        *align = 8;
        return;
    }
    if (strncmp(name, ".rela.", 6) == 0) {
        *type = BEDROCK_SHT_RELA;
        *align = 8;
    }
}

void bedrock_asm_init(BedrockAsm *ctx)
{
    memset(ctx, 0, sizeof(*ctx));
    ctx->current_section = -1;
    (void)bedrock_asm_switch_section(ctx, ".text");
}

void bedrock_asm_free(BedrockAsm *ctx)
{
    size_t index;
    for (index = 0; index < ctx->section_count; ++index) {
        free(ctx->sections[index].name);
        free(ctx->sections[index].data.data);
        free(ctx->sections[index].relocs);
    }
    for (index = 0; index < ctx->symbol_count; ++index) {
        free(ctx->symbols[index].name);
    }
    free(ctx->sections);
    free(ctx->symbols);
    memset(ctx, 0, sizeof(*ctx));
    ctx->current_section = -1;
}

void bedrock_asm_error(BedrockAsm *ctx, const char *fmt, ...)
{
    va_list ap;
    fprintf(stderr, "%s:%u: error: ", ctx->input_name ? ctx->input_name : "<input>", ctx->line_number);
    va_start(ap, fmt);
    vfprintf(stderr, fmt, ap);
    va_end(ap);
    fputc('\n', stderr);
    ++ctx->error_count;
}

BedrockSection *bedrock_asm_section(BedrockAsm *ctx, int index)
{
    if (index < 0 || (size_t)index >= ctx->section_count) {
        return 0;
    }
    return &ctx->sections[index];
}

BedrockSection *bedrock_asm_current_section(BedrockAsm *ctx)
{
    return bedrock_asm_section(ctx, ctx->current_section);
}

int bedrock_asm_switch_section(BedrockAsm *ctx, const char *name)
{
    size_t index;
    uint32_t type;
    uint64_t flags;
    uint64_t align;
    for (index = 0; index < ctx->section_count; ++index) {
        if (strcmp(ctx->sections[index].name, name) == 0) {
            ctx->current_section = (int)index;
            return (int)index;
        }
    }
    if (!reserve_bytes((void **)&ctx->sections, &ctx->section_capacity, sizeof(ctx->sections[0]), ctx->section_count + 1u)) {
        bedrock_asm_error(ctx, "out of memory while creating section");
        return -1;
    }
    default_section_attrs(name, &type, &flags, &align);
    memset(&ctx->sections[ctx->section_count], 0, sizeof(ctx->sections[ctx->section_count]));
    ctx->sections[ctx->section_count].name = bedrock_strdup(name);
    ctx->sections[ctx->section_count].type = type;
    ctx->sections[ctx->section_count].flags = flags;
    ctx->sections[ctx->section_count].align = align;
    ctx->current_section = (int)ctx->section_count;
    ++ctx->section_count;
    return ctx->current_section;
}

int bedrock_asm_find_symbol(BedrockAsm *ctx, const char *name)
{
    size_t index;
    for (index = 0; index < ctx->symbol_count; ++index) {
        if (strcmp(ctx->symbols[index].name, name) == 0) {
            return (int)index;
        }
    }
    return -1;
}

int bedrock_asm_get_symbol(BedrockAsm *ctx, const char *name)
{
    int found = bedrock_asm_find_symbol(ctx, name);
    if (found >= 0) {
        return found;
    }
    if (!reserve_bytes((void **)&ctx->symbols, &ctx->symbol_capacity, sizeof(ctx->symbols[0]), ctx->symbol_count + 1u)) {
        bedrock_asm_error(ctx, "out of memory while creating symbol");
        return -1;
    }
    memset(&ctx->symbols[ctx->symbol_count], 0, sizeof(ctx->symbols[ctx->symbol_count]));
    ctx->symbols[ctx->symbol_count].name = bedrock_strdup(name);
    ctx->symbols[ctx->symbol_count].section = -1;
    ctx->symbols[ctx->symbol_count].bind = BEDROCK_STB_LOCAL;
    ctx->symbols[ctx->symbol_count].type = BEDROCK_STT_NOTYPE;
    return (int)ctx->symbol_count++;
}

void bedrock_asm_define_symbol(BedrockAsm *ctx, const char *name)
{
    int symbol_index = bedrock_asm_get_symbol(ctx, name);
    BedrockSection *section = bedrock_asm_current_section(ctx);
    if (symbol_index < 0 || section == 0) {
        return;
    }
    ctx->symbols[symbol_index].section = ctx->current_section;
    ctx->symbols[symbol_index].value = section->logical_size;
    ctx->symbols[symbol_index].defined = 1;
}

void bedrock_asm_set_symbol_bind(BedrockAsm *ctx, const char *name, unsigned bind)
{
    int symbol_index = bedrock_asm_get_symbol(ctx, name);
    if (symbol_index >= 0) {
        ctx->symbols[symbol_index].bind = bind;
    }
}

void bedrock_asm_set_symbol_type(BedrockAsm *ctx, const char *name, unsigned type)
{
    int symbol_index = bedrock_asm_get_symbol(ctx, name);
    if (symbol_index >= 0) {
        ctx->symbols[symbol_index].type = type;
    }
}

void bedrock_asm_set_symbol_visibility(BedrockAsm *ctx, const char *name, unsigned visibility)
{
    int symbol_index = bedrock_asm_get_symbol(ctx, name);
    if (symbol_index >= 0) {
        ctx->symbols[symbol_index].visibility = visibility;
    }
}

void bedrock_asm_set_symbol_size(BedrockAsm *ctx, const char *name, uint64_t size)
{
    int symbol_index = bedrock_asm_get_symbol(ctx, name);
    if (symbol_index >= 0) {
        ctx->symbols[symbol_index].size = size;
    }
}

int bedrock_buffer_reserve(BedrockBuffer *buffer, size_t extra)
{
    if (extra > (size_t)-1 - buffer->size) {
        return 0;
    }
    return reserve_bytes((void **)&buffer->data, &buffer->capacity, 1u, buffer->size + extra);
}

int bedrock_section_emit(BedrockSection *section, const void *data, size_t size)
{
    if (section->type == BEDROCK_SHT_NOBITS) {
        section->logical_size += size;
        return 1;
    }
    if (!bedrock_buffer_reserve(&section->data, size)) {
        return 0;
    }
    memcpy(section->data.data + section->data.size, data, size);
    section->data.size += size;
    section->logical_size += size;
    return 1;
}

int bedrock_section_emit_zero(BedrockSection *section, size_t size)
{
    static const uint8_t zero[16] = {0};
    while (size != 0u) {
        size_t chunk = size < sizeof(zero) ? size : sizeof(zero);
        if (!bedrock_section_emit(section, zero, chunk)) {
            return 0;
        }
        size -= chunk;
    }
    return 1;
}

int bedrock_section_align(BedrockSection *section, size_t align)
{
    size_t mask;
    size_t padding;
    if (align <= 1u) {
        return 1;
    }
    mask = align - 1u;
    padding = ((section->logical_size + mask) & ~mask) - section->logical_size;
    if (section->align < align) {
        section->align = align;
    }
    return bedrock_section_emit_zero(section, padding);
}

int bedrock_section_add_reloc(BedrockSection *section, size_t offset, int symbol, unsigned type, int64_t addend)
{
    if (!reserve_bytes((void **)&section->relocs, &section->reloc_capacity, sizeof(section->relocs[0]), section->reloc_count + 1u)) {
        return 0;
    }
    section->relocs[section->reloc_count].offset = offset;
    section->relocs[section->reloc_count].symbol = symbol;
    section->relocs[section->reloc_count].type = type;
    section->relocs[section->reloc_count].addend = addend;
    ++section->reloc_count;
    return 1;
}

typedef struct RelocName {
    const char *name;
    unsigned type;
    unsigned width_bits;
} RelocName;

static const RelocName reloc_names[] = {
    {"NONE", BEDROCK_R_NONE, 0}, {"ABS8", BEDROCK_R_ABS8, 8}, {"ABS16", BEDROCK_R_ABS16, 16},
    {"ABS32", BEDROCK_R_ABS32, 32}, {"ABS64", BEDROCK_R_ABS64, 64},
    {"PCREL16", BEDROCK_R_PCREL16, 16}, {"PCREL32", BEDROCK_R_PCREL32, 32}, {"PCREL64", BEDROCK_R_PCREL64, 64},
    {"WORD_PCREL16", BEDROCK_R_WORD_PCREL16, 16}, {"WORD_PCREL32", BEDROCK_R_WORD_PCREL32, 32},
    {"IMM16", BEDROCK_R_IMM16, 16}, {"IMM32", BEDROCK_R_IMM32, 32}, {"IMM64", BEDROCK_R_IMM64, 64},
    {"DISP16", BEDROCK_R_DISP16, 16}, {"DISP32", BEDROCK_R_DISP32, 32}, {"DISP64", BEDROCK_R_DISP64, 64},
    {"SECTION_REL32", BEDROCK_R_SECTION_REL32, 32}, {"SECTION_REL64", BEDROCK_R_SECTION_REL64, 64},
    {"CALL_TARGET", BEDROCK_R_CALL_TARGET, 0}, {"JMP_TARGET", BEDROCK_R_JMP_TARGET, 0},
    {"LONG_CONTROL_TARGET", BEDROCK_R_LONG_CONTROL_TARGET, 0}, {"GOT64", BEDROCK_R_GOT64, 64},
    {"GOT", BEDROCK_R_GOT64, 64}, {"GOTPCREL32", BEDROCK_R_GOTPCREL32, 32},
    {"GOTPCREL64", BEDROCK_R_GOTPCREL64, 64}, {"GOTOFF32", BEDROCK_R_GOTOFF32, 32},
    {"GOTOFF64", BEDROCK_R_GOTOFF64, 64}, {"GOT_BASE_PCREL32", BEDROCK_R_GOT_BASE_PCREL32, 32},
    {"GOT_BASE_PCREL64", BEDROCK_R_GOT_BASE_PCREL64, 64}, {"PLT32", BEDROCK_R_PLT32, 32},
    {"PLT", BEDROCK_R_PLT32, 32}, {"PLT64", BEDROCK_R_PLT64, 64},
    {"TLS_OFFSET32", BEDROCK_R_TLS_OFFSET32, 32}, {"TLS_OFFSET64", BEDROCK_R_TLS_OFFSET64, 64},
    {"TLSDESC_GOTPCREL32", BEDROCK_R_TLSDESC_GOTPCREL32, 32},
    {"TLSDESC_GOTPCREL64", BEDROCK_R_TLSDESC_GOTPCREL64, 64},
    {"TLSDESC_CALL", BEDROCK_R_TLSDESC_CALL, 0}, {"TLSDESC", BEDROCK_R_TLSDESC, 128}
};

int bedrock_reloc_type_by_name(const char *name, unsigned *type, unsigned *width_bits)
{
    size_t index;
    const char *trimmed = name;
    if (strncmp(trimmed, "R_BEDROCK_", 10) == 0) {
        trimmed += 10;
    }
    for (index = 0; index < sizeof(reloc_names) / sizeof(reloc_names[0]); ++index) {
        if (strcmp(reloc_names[index].name, trimmed) == 0) {
            *type = reloc_names[index].type;
            *width_bits = reloc_names[index].width_bits;
            return 1;
        }
    }
    return 0;
}

unsigned bedrock_default_abs_reloc_for_size(size_t size)
{
    if (size == 1u) {
        return BEDROCK_R_ABS8;
    }
    if (size == 2u) {
        return BEDROCK_R_ABS16;
    }
    if (size == 4u) {
        return BEDROCK_R_ABS32;
    }
    return BEDROCK_R_ABS64;
}

unsigned bedrock_reloc_width_bits(unsigned type)
{
    size_t index;
    for (index = 0; index < sizeof(reloc_names) / sizeof(reloc_names[0]); ++index) {
        if (reloc_names[index].type == type) {
            return reloc_names[index].width_bits;
        }
    }
    return 0;
}
