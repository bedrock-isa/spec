#include "bedrock_asm.h"

#include <stdlib.h>
#include <string.h>

typedef struct StringTable {
    BedrockBuffer data;
} StringTable;

typedef struct OutSection {
    const char *name;
    char *owned_name;
    uint32_t type;
    uint64_t flags;
    uint64_t offset;
    uint64_t size;
    uint64_t align;
    uint64_t entsize;
    uint32_t link;
    uint32_t info;
    BedrockBuffer data;
    int source_section;
    uint32_t name_offset;
} OutSection;

static char *writer_strdup(const char *text)
{
    size_t len = strlen(text) + 1u;
    char *copy = (char *)malloc(len);
    if (copy != 0) {
        memcpy(copy, text, len);
    }
    return copy;
}

static void put16(uint8_t *buf, uint16_t value)
{
    buf[0] = (uint8_t)(value & 0xffu);
    buf[1] = (uint8_t)((value >> 8) & 0xffu);
}

static void put32(uint8_t *buf, uint32_t value)
{
    put16(buf, (uint16_t)(value & 0xffffu));
    put16(buf + 2, (uint16_t)((value >> 16) & 0xffffu));
}

static void put64(uint8_t *buf, uint64_t value)
{
    put32(buf, (uint32_t)(value & 0xffffffffu));
    put32(buf + 4, (uint32_t)((value >> 32) & 0xffffffffu));
}

static int buffer_append(BedrockBuffer *buffer, const void *data, size_t size)
{
    if (!bedrock_buffer_reserve(buffer, size)) {
        return 0;
    }
    memcpy(buffer->data + buffer->size, data, size);
    buffer->size += size;
    return 1;
}

static uint32_t string_table_add(StringTable *table, const char *text)
{
    uint32_t offset = (uint32_t)table->data.size;
    (void)buffer_append(&table->data, text, strlen(text) + 1u);
    return offset;
}

static size_t align_to(size_t value, size_t align)
{
    size_t mask;
    if (align <= 1u) {
        return value;
    }
    mask = align - 1u;
    return (value + mask) & ~mask;
}

static int write_padding(FILE *fp, size_t count)
{
    static const uint8_t zero[32] = {0};
    while (count != 0u) {
        size_t chunk = count < sizeof(zero) ? count : sizeof(zero);
        if (fwrite(zero, 1u, chunk, fp) != chunk) {
            return 0;
        }
        count -= chunk;
    }
    return 1;
}

static void append_sym(BedrockBuffer *symtab, uint32_t name, uint8_t info, uint8_t other, uint16_t shndx, uint64_t value, uint64_t size)
{
    uint8_t entry[24];
    memset(entry, 0, sizeof(entry));
    put32(entry + 0, name);
    entry[4] = info;
    entry[5] = other;
    put16(entry + 6, shndx);
    put64(entry + 8, value);
    put64(entry + 16, size);
    (void)buffer_append(symtab, entry, sizeof(entry));
}

static int symbol_is_local_named(const BedrockSymbol *symbol)
{
    return symbol->bind == BEDROCK_STB_LOCAL && symbol->defined;
}

static void assign_undefined_bindings(BedrockAsm *ctx)
{
    size_t index;
    for (index = 0; index < ctx->symbol_count; ++index) {
        if (!ctx->symbols[index].defined && ctx->symbols[index].bind == BEDROCK_STB_LOCAL) {
            ctx->symbols[index].bind = BEDROCK_STB_GLOBAL;
        }
    }
}

static int build_symtab(BedrockAsm *ctx, BedrockBuffer *symtab, StringTable *strtab, uint32_t *first_global)
{
    size_t index;
    uint32_t sym_index = 0;
    append_sym(symtab, 0, 0, 0, 0, 0, 0);
    ++sym_index;
    for (index = 0; index < ctx->section_count; ++index) {
        append_sym(symtab, 0, (uint8_t)((BEDROCK_STB_LOCAL << 4) | BEDROCK_STT_SECTION), 0, (uint16_t)ctx->sections[index].sh_index, 0, 0);
        ++sym_index;
    }
    for (index = 0; index < ctx->symbol_count; ++index) {
        BedrockSymbol *symbol = &ctx->symbols[index];
        if (symbol_is_local_named(symbol)) {
            uint32_t name = string_table_add(strtab, symbol->name);
            append_sym(
                symtab,
                name,
                (uint8_t)((symbol->bind << 4) | (symbol->type & 0xfu)),
                (uint8_t)symbol->visibility,
                (uint16_t)ctx->sections[symbol->section].sh_index,
                symbol->value,
                symbol->size
            );
            symbol->symtab_index = sym_index++;
        }
    }
    *first_global = sym_index;
    for (index = 0; index < ctx->symbol_count; ++index) {
        BedrockSymbol *symbol = &ctx->symbols[index];
        if (!symbol_is_local_named(symbol)) {
            uint32_t name = string_table_add(strtab, symbol->name);
            uint16_t shndx = 0;
            if (symbol->defined && symbol->section >= 0) {
                shndx = (uint16_t)ctx->sections[symbol->section].sh_index;
            }
            append_sym(
                symtab,
                name,
                (uint8_t)((symbol->bind << 4) | (symbol->type & 0xfu)),
                (uint8_t)symbol->visibility,
                shndx,
                symbol->defined ? symbol->value : 0,
                symbol->size
            );
            symbol->symtab_index = sym_index++;
        }
    }
    return 1;
}

static int build_rela_section(BedrockSection *section, BedrockBuffer *rela)
{
    size_t index;
    for (index = 0; index < section->reloc_count; ++index) {
        uint8_t entry[24];
        BedrockReloc *reloc = &section->relocs[index];
        uint64_t info;
        memset(entry, 0, sizeof(entry));
        info = ((uint64_t)section->relocs[index].symbol << 32) | (uint64_t)reloc->type;
        put64(entry + 0, reloc->offset);
        put64(entry + 8, info);
        put64(entry + 16, (uint64_t)reloc->addend);
        (void)buffer_append(rela, entry, sizeof(entry));
    }
    return 1;
}

static void patch_rela_symbols(BedrockAsm *ctx)
{
    size_t section_index;
    for (section_index = 0; section_index < ctx->section_count; ++section_index) {
        BedrockSection *section = &ctx->sections[section_index];
        size_t reloc_index;
        for (reloc_index = 0; reloc_index < section->reloc_count; ++reloc_index) {
            int symbol = section->relocs[reloc_index].symbol;
            section->relocs[reloc_index].symbol = (int)ctx->symbols[symbol].symtab_index;
        }
    }
}

static void free_out_sections(OutSection *sections, size_t count)
{
    size_t index;
    for (index = 0; index < count; ++index) {
        free(sections[index].owned_name);
        free(sections[index].data.data);
    }
    free(sections);
}

int bedrock_asm_write_elf64(BedrockAsm *ctx, const char *path)
{
    FILE *fp;
    OutSection *out = 0;
    StringTable strtab = {{0}};
    StringTable shstrtab = {{0}};
    BedrockBuffer symtab = {0};
    size_t reloc_section_count = 0;
    size_t out_count;
    size_t out_index;
    size_t source_index;
    size_t offset;
    size_t section_header_offset;
    uint32_t first_global = 0;
    uint32_t symtab_index;
    uint32_t strtab_index;
    uint32_t shstrtab_index;
    uint16_t shstrndx;

    assign_undefined_bindings(ctx);

    for (source_index = 0; source_index < ctx->section_count; ++source_index) {
        if (ctx->sections[source_index].reloc_count != 0u) {
            ++reloc_section_count;
        }
    }
    out_count = 1u + ctx->section_count + reloc_section_count + 3u;
    out = (OutSection *)calloc(out_count, sizeof(out[0]));
    if (out == 0) {
        return 0;
    }

    out_index = 1u;
    for (source_index = 0; source_index < ctx->section_count; ++source_index) {
        BedrockSection *section = &ctx->sections[source_index];
        section->sh_index = (unsigned)out_index;
        out[out_index].name = section->name;
        out[out_index].type = section->type;
        out[out_index].flags = section->flags;
        out[out_index].align = section->align == 0u ? 1u : section->align;
        out[out_index].source_section = (int)source_index;
        if (section->type == BEDROCK_SHT_NOBITS) {
            out[out_index].size = section->logical_size;
        } else {
            out[out_index].data = section->data;
            out[out_index].size = section->data.size;
            section->data.data = 0;
            section->data.size = 0;
            section->data.capacity = 0;
        }
        ++out_index;
    }

    symtab_index = (uint32_t)(out_count - 3u);
    strtab_index = (uint32_t)(out_count - 2u);
    shstrtab_index = (uint32_t)(out_count - 1u);

    if (!buffer_append(&strtab.data, "", 1u) || !buffer_append(&shstrtab.data, "", 1u)) {
        free_out_sections(out, out_count);
        return 0;
    }
    (void)build_symtab(ctx, &symtab, &strtab, &first_global);
    patch_rela_symbols(ctx);

    for (source_index = 0; source_index < ctx->section_count; ++source_index) {
        BedrockSection *section = &ctx->sections[source_index];
        if (section->reloc_count != 0u) {
            char rela_name[256];
            snprintf(rela_name, sizeof(rela_name), ".rela%s", section->name);
            section->rela_sh_index = (unsigned)out_index;
            out[out_index].owned_name = writer_strdup(rela_name);
            out[out_index].name = out[out_index].owned_name;
            out[out_index].type = BEDROCK_SHT_RELA;
            out[out_index].align = 8;
            out[out_index].entsize = 24;
            out[out_index].link = symtab_index;
            out[out_index].info = section->sh_index;
            (void)build_rela_section(section, &out[out_index].data);
            out[out_index].size = out[out_index].data.size;
            ++out_index;
        }
    }

    out[symtab_index].name = ".symtab";
    out[symtab_index].type = BEDROCK_SHT_SYMTAB;
    out[symtab_index].align = 8;
    out[symtab_index].entsize = 24;
    out[symtab_index].link = strtab_index;
    out[symtab_index].info = first_global;
    out[symtab_index].data = symtab;
    out[symtab_index].size = symtab.size;

    out[strtab_index].name = ".strtab";
    out[strtab_index].type = BEDROCK_SHT_STRTAB;
    out[strtab_index].align = 1;
    out[strtab_index].data = strtab.data;
    out[strtab_index].size = strtab.data.size;

    out[shstrtab_index].name = ".shstrtab";
    out[shstrtab_index].type = BEDROCK_SHT_STRTAB;
    out[shstrtab_index].align = 1;

    for (out_index = 1u; out_index < out_count; ++out_index) {
        out[out_index].name_offset = string_table_add(&shstrtab, out[out_index].name);
    }
    out[shstrtab_index].data = shstrtab.data;
    out[shstrtab_index].size = shstrtab.data.size;
    shstrndx = (uint16_t)shstrtab_index;

    offset = 64u;
    for (out_index = 1u; out_index < out_count; ++out_index) {
        OutSection *section = &out[out_index];
        offset = align_to(offset, (size_t)(section->align == 0u ? 1u : section->align));
        section->offset = offset;
        if (section->type != BEDROCK_SHT_NOBITS) {
            offset += section->data.size;
        }
    }
    section_header_offset = align_to(offset, 8u);

    fp = fopen(path, "wb");
    if (fp == 0) {
        free_out_sections(out, out_count);
        return 0;
    }
    {
        uint8_t ehdr[64];
        memset(ehdr, 0, sizeof(ehdr));
        ehdr[0] = 0x7f;
        ehdr[1] = 'E';
        ehdr[2] = 'L';
        ehdr[3] = 'F';
        ehdr[4] = 2;
        ehdr[5] = 1;
        ehdr[6] = 1;
        put16(ehdr + 16, 1);
        put16(ehdr + 18, BEDROCK_EMACHINE);
        put32(ehdr + 20, 1);
        put64(ehdr + 40, section_header_offset);
        put16(ehdr + 52, 64);
        put16(ehdr + 58, 64);
        put16(ehdr + 60, (uint16_t)out_count);
        put16(ehdr + 62, shstrndx);
        if (fwrite(ehdr, 1u, sizeof(ehdr), fp) != sizeof(ehdr)) {
            fclose(fp);
            free_out_sections(out, out_count);
            return 0;
        }
    }
    offset = 64u;
    for (out_index = 1u; out_index < out_count; ++out_index) {
        OutSection *section = &out[out_index];
        if (!write_padding(fp, (size_t)section->offset - offset)) {
            fclose(fp);
            free_out_sections(out, out_count);
            return 0;
        }
        offset = (size_t)section->offset;
        if (section->type != BEDROCK_SHT_NOBITS) {
            if (section->data.size != 0u && fwrite(section->data.data, 1u, section->data.size, fp) != section->data.size) {
                fclose(fp);
                free_out_sections(out, out_count);
                return 0;
            }
            offset += section->data.size;
        }
    }
    if (!write_padding(fp, section_header_offset - offset)) {
        fclose(fp);
        free_out_sections(out, out_count);
        return 0;
    }
    {
        uint8_t shdr[64];
        memset(shdr, 0, sizeof(shdr));
        if (fwrite(shdr, 1u, sizeof(shdr), fp) != sizeof(shdr)) {
            fclose(fp);
            free_out_sections(out, out_count);
            return 0;
        }
        for (out_index = 1u; out_index < out_count; ++out_index) {
            OutSection *section = &out[out_index];
            memset(shdr, 0, sizeof(shdr));
            put32(shdr + 0, section->name_offset);
            put32(shdr + 4, section->type);
            put64(shdr + 8, section->flags);
            put64(shdr + 24, section->offset);
            put64(shdr + 32, section->size);
            put32(shdr + 40, section->link);
            put32(shdr + 44, section->info);
            put64(shdr + 48, section->align == 0u ? 1u : section->align);
            put64(shdr + 56, section->entsize);
            if (fwrite(shdr, 1u, sizeof(shdr), fp) != sizeof(shdr)) {
                fclose(fp);
                free_out_sections(out, out_count);
                return 0;
            }
        }
    }
    fclose(fp);
    free_out_sections(out, out_count);
    return 1;
}
