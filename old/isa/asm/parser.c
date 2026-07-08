#include "bedrock_asm.h"

#include <ctype.h>
#include <stdlib.h>
#include <string.h>

static int is_ident_char(int ch)
{
    return isalnum((unsigned char)ch) || ch == '_' || ch == '.' || ch == '$';
}

static int ieq(const char *lhs, const char *rhs)
{
    while (*lhs != '\0' && *rhs != '\0') {
        if (toupper((unsigned char)*lhs) != toupper((unsigned char)*rhs)) {
            return 0;
        }
        ++lhs;
        ++rhs;
    }
    return *lhs == '\0' && *rhs == '\0';
}

static char *trim(char *text)
{
    char *end;
    while (isspace((unsigned char)*text)) {
        ++text;
    }
    end = text + strlen(text);
    while (end > text && isspace((unsigned char)end[-1])) {
        *--end = '\0';
    }
    return text;
}

static void strip_comment(char *line)
{
    int in_string = 0;
    char *cursor;
    for (cursor = line; *cursor != '\0'; ++cursor) {
        if (*cursor == '"' && (cursor == line || cursor[-1] != '\\')) {
            in_string = !in_string;
        }
        if (!in_string && *cursor == '#') {
            *cursor = '\0';
            return;
        }
        if (!in_string && cursor[0] == '/' && cursor[1] == '/') {
            *cursor = '\0';
            return;
        }
        if (!in_string && cursor[0] == '/' && cursor[1] == '*') {
            *cursor = '\0';
            return;
        }
    }
}

static int parse_u64_text(const char *text, uint64_t *value)
{
    char *end = 0;
    unsigned long long parsed;
    while (isspace((unsigned char)*text)) {
        ++text;
    }
    parsed = strtoull(text, &end, 0);
    if (end == text) {
        return 0;
    }
    while (isspace((unsigned char)*end)) {
        ++end;
    }
    if (*end != '\0') {
        return 0;
    }
    *value = (uint64_t)parsed;
    return 1;
}

static int parse_i64_text(const char *text, int64_t *value)
{
    char *end = 0;
    long long parsed;
    while (isspace((unsigned char)*text)) {
        ++text;
    }
    parsed = strtoll(text, &end, 0);
    if (end == text) {
        return 0;
    }
    while (isspace((unsigned char)*end)) {
        ++end;
    }
    if (*end != '\0') {
        return 0;
    }
    *value = (int64_t)parsed;
    return 1;
}

static void emit_integer(BedrockSection *section, uint64_t value, size_t size)
{
    uint8_t bytes[8];
    size_t index;
    for (index = 0; index < size; ++index) {
        bytes[index] = (uint8_t)((value >> (index * 8u)) & 0xffu);
    }
    (void)bedrock_section_emit(section, bytes, size);
}

static int parse_symbol_expr(BedrockAsm *ctx, char *text, unsigned default_reloc, BedrockExpr *expr)
{
    char *at;
    char *sign;
    char *name_end;
    char saved;
    uint64_t number;
    memset(expr, 0, sizeof(*expr));
    text = trim(text);
    if (parse_u64_text(text, &number)) {
        expr->value = (int64_t)number;
        return 1;
    }
    if (*text == '\0') {
        return 0;
    }
    name_end = text;
    while (is_ident_char((unsigned char)*name_end)) {
        ++name_end;
    }
    if (name_end == text) {
        return 0;
    }
    saved = *name_end;
    *name_end = '\0';
    expr->symbol = bedrock_asm_get_symbol(ctx, text);
    *name_end = saved;
    if (expr->symbol < 0) {
        return 0;
    }
    expr->is_symbol = 1;
    expr->reloc_type = default_reloc;
    at = name_end;
    if (*at == '@') {
        char reloc_name[64];
        size_t len = 0;
        unsigned width = 0;
        ++at;
        while ((isalnum((unsigned char)*at) || *at == '_') && len + 1u < sizeof(reloc_name)) {
            reloc_name[len++] = *at++;
        }
        reloc_name[len] = '\0';
        if (!bedrock_reloc_type_by_name(reloc_name, &expr->reloc_type, &width)) {
            bedrock_asm_error(ctx, "unknown relocation annotation @%s", reloc_name);
            return 0;
        }
    }
    sign = at;
    while (isspace((unsigned char)*sign)) {
        ++sign;
    }
    if (*sign == '+' || *sign == '-') {
        int negative = *sign == '-';
        int64_t addend = 0;
        ++sign;
        if (!parse_i64_text(sign, &addend)) {
            return 0;
        }
        expr->value = negative ? -addend : addend;
    } else if (*sign != '\0') {
        return 0;
    }
    return 1;
}

static char *next_csv(char **cursor)
{
    char *start = *cursor;
    char *scan = start;
    int in_string = 0;
    int bracket_depth = 0;
    while (*scan != '\0') {
        if (*scan == '"' && (scan == start || scan[-1] != '\\')) {
            in_string = !in_string;
        } else if (!in_string && *scan == '[') {
            ++bracket_depth;
        } else if (!in_string && *scan == ']') {
            --bracket_depth;
        } else if (!in_string && bracket_depth == 0 && *scan == ',') {
            *scan++ = '\0';
            *cursor = scan;
            return trim(start);
        }
        ++scan;
    }
    *cursor = scan;
    return trim(start);
}

static void emit_data_expr(BedrockAsm *ctx, char *expr_text, size_t size)
{
    BedrockSection *section = bedrock_asm_current_section(ctx);
    BedrockExpr expr;
    size_t offset;
    if (section == 0) {
        return;
    }
    if (!parse_symbol_expr(ctx, expr_text, bedrock_default_abs_reloc_for_size(size), &expr)) {
        bedrock_asm_error(ctx, "invalid expression `%s`", expr_text);
        return;
    }
    offset = section->logical_size;
    emit_integer(section, expr.is_symbol ? 0u : (uint64_t)expr.value, size);
    if (expr.is_symbol && !bedrock_section_add_reloc(section, offset, expr.symbol, expr.reloc_type, expr.value)) {
        bedrock_asm_error(ctx, "out of memory while adding relocation");
    }
}

static void handle_data_directive(BedrockAsm *ctx, char *args, size_t size)
{
    char *cursor = args;
    while (*cursor != '\0') {
        char *part = next_csv(&cursor);
        if (*part != '\0') {
            emit_data_expr(ctx, part, size);
        }
    }
}

static void handle_fill_directive(BedrockAsm *ctx, char *args)
{
    char *cursor = args;
    char *count_text = next_csv(&cursor);
    char *size_text = next_csv(&cursor);
    char *value_text = next_csv(&cursor);
    uint64_t count = 0;
    uint64_t size = 0;
    uint64_t value = 0;
    uint64_t index;
    BedrockSection *section = bedrock_asm_current_section(ctx);
    if (section == 0) {
        return;
    }
    if (!parse_u64_text(count_text, &count) || !parse_u64_text(size_text, &size) || !parse_u64_text(value_text, &value)) {
        bedrock_asm_error(ctx, ".fill requires numeric count, size, and value");
        return;
    }
    if (size == 0u || size > 8u) {
        bedrock_asm_error(ctx, ".fill size must be between 1 and 8 bytes");
        return;
    }
    for (index = 0; index < count; ++index) {
        emit_integer(section, value, (size_t)size);
    }
}

static int parse_string_piece(BedrockAsm *ctx, char *text, int nul_terminate)
{
    BedrockSection *section = bedrock_asm_current_section(ctx);
    char *cursor = trim(text);
    if (section == 0 || *cursor != '"') {
        return 0;
    }
    ++cursor;
    while (*cursor != '\0' && *cursor != '"') {
        uint8_t ch;
        if (*cursor == '\\') {
            ++cursor;
            if (*cursor == 'n') {
                ch = '\n';
            } else if (*cursor == 't') {
                ch = '\t';
            } else if (*cursor == '0') {
                ch = '\0';
            } else {
                ch = (uint8_t)*cursor;
            }
        } else {
            ch = (uint8_t)*cursor;
        }
        if (!bedrock_section_emit(section, &ch, 1u)) {
            bedrock_asm_error(ctx, "out of memory while emitting string");
            return 0;
        }
        ++cursor;
    }
    if (*cursor != '"') {
        return 0;
    }
    if (nul_terminate) {
        uint8_t zero = 0;
        if (!bedrock_section_emit(section, &zero, 1u)) {
            bedrock_asm_error(ctx, "out of memory while emitting string terminator");
            return 0;
        }
    }
    return 1;
}

static uint64_t parse_size_expr(BedrockAsm *ctx, char *text)
{
    char *trimmed = trim(text);
    uint64_t value = 0;
    if (parse_u64_text(trimmed, &value)) {
        return value;
    }
    if (strncmp(trimmed, ".-", 2) == 0) {
        char *name = trim(trimmed + 2);
        int symbol = bedrock_asm_find_symbol(ctx, name);
        BedrockSection *section = bedrock_asm_current_section(ctx);
        if (symbol >= 0 && section != 0 && ctx->symbols[symbol].defined && ctx->symbols[symbol].section == ctx->current_section) {
            return section->logical_size - ctx->symbols[symbol].value;
        }
    }
    bedrock_asm_error(ctx, "unsupported size expression `%s`", text);
    return 0;
}

static void handle_type(BedrockAsm *ctx, char *args)
{
    char *cursor = args;
    char *name = next_csv(&cursor);
    char *type = next_csv(&cursor);
    if (*name == '\0' || *type == '\0') {
        bedrock_asm_error(ctx, ".type requires symbol and type");
        return;
    }
    if (ieq(type, "@function") || ieq(type, "%function")) {
        bedrock_asm_set_symbol_type(ctx, name, BEDROCK_STT_FUNC);
    } else if (ieq(type, "@object") || ieq(type, "%object")) {
        bedrock_asm_set_symbol_type(ctx, name, BEDROCK_STT_OBJECT);
    } else if (ieq(type, "@gnu_indirect_function")) {
        bedrock_asm_set_symbol_type(ctx, name, BEDROCK_STT_GNU_IFUNC);
    }
}

static void handle_size(BedrockAsm *ctx, char *args)
{
    char *cursor = args;
    char *name = next_csv(&cursor);
    char *expr = next_csv(&cursor);
    if (*name == '\0' || *expr == '\0') {
        bedrock_asm_error(ctx, ".size requires symbol and expression");
        return;
    }
    bedrock_asm_set_symbol_size(ctx, name, parse_size_expr(ctx, expr));
}

static void handle_section(BedrockAsm *ctx, char *args)
{
    char *cursor = args;
    char *name = next_csv(&cursor);
    if (*name == '\0') {
        bedrock_asm_error(ctx, ".section requires a section name");
        return;
    }
    (void)bedrock_asm_switch_section(ctx, name);
}

static void handle_directive(BedrockAsm *ctx, char *line)
{
    char *name = line;
    char *args;
    while (*line != '\0' && !isspace((unsigned char)*line)) {
        ++line;
    }
    if (*line != '\0') {
        *line++ = '\0';
    }
    args = trim(line);
    if (strcmp(name, ".text") == 0 || strcmp(name, ".data") == 0 || strcmp(name, ".rodata") == 0 || strcmp(name, ".bss") == 0) {
        (void)bedrock_asm_switch_section(ctx, name);
    } else if (strcmp(name, ".section") == 0) {
        handle_section(ctx, args);
    } else if (strcmp(name, ".globl") == 0 || strcmp(name, ".global") == 0) {
        bedrock_asm_set_symbol_bind(ctx, args, BEDROCK_STB_GLOBAL);
    } else if (strcmp(name, ".weak") == 0) {
        bedrock_asm_set_symbol_bind(ctx, args, BEDROCK_STB_WEAK);
    } else if (strcmp(name, ".hidden") == 0) {
        bedrock_asm_set_symbol_visibility(ctx, args, 2u);
    } else if (strcmp(name, ".type") == 0) {
        handle_type(ctx, args);
    } else if (strcmp(name, ".size") == 0) {
        handle_size(ctx, args);
    } else if (strcmp(name, ".byte") == 0) {
        handle_data_directive(ctx, args, 1u);
    } else if (strcmp(name, ".word") == 0 || strcmp(name, ".short") == 0) {
        handle_data_directive(ctx, args, 2u);
    } else if (strcmp(name, ".long") == 0 || strcmp(name, ".int") == 0) {
        handle_data_directive(ctx, args, 4u);
    } else if (strcmp(name, ".quad") == 0) {
        handle_data_directive(ctx, args, 8u);
    } else if (strcmp(name, ".fill") == 0) {
        handle_fill_directive(ctx, args);
    } else if (strcmp(name, ".zero") == 0 || strcmp(name, ".space") == 0) {
        uint64_t count = parse_size_expr(ctx, args);
        (void)bedrock_section_emit_zero(bedrock_asm_current_section(ctx), (size_t)count);
    } else if (strcmp(name, ".align") == 0 || strcmp(name, ".balign") == 0) {
        uint64_t align = parse_size_expr(ctx, args);
        (void)bedrock_section_align(bedrock_asm_current_section(ctx), (size_t)align);
    } else if (strcmp(name, ".p2align") == 0) {
        uint64_t power = parse_size_expr(ctx, args);
        (void)bedrock_section_align(bedrock_asm_current_section(ctx), (size_t)1u << power);
    } else if (strcmp(name, ".ascii") == 0) {
        if (!parse_string_piece(ctx, args, 0)) {
            bedrock_asm_error(ctx, "invalid .ascii string");
        }
    } else if (strcmp(name, ".asciz") == 0 || strcmp(name, ".string") == 0) {
        if (!parse_string_piece(ctx, args, 1)) {
            bedrock_asm_error(ctx, "invalid .asciz string");
        }
    } else if (strcmp(name, ".file") == 0 || strcmp(name, ".loc") == 0 || strncmp(name, ".cfi_", 5) == 0) {
        /* Debug directives are accepted and ignored until the DWARF ABI is fixed. */
    } else {
        bedrock_asm_error(ctx, "unsupported directive `%s`", name);
    }
}

static size_t instruction_payload_start(const bedrock_form_desc *form)
{
    size_t index;
    size_t start = (form->kind == BEDROCK_FORM_EXTENDED || form->kind == BEDROCK_FORM_EXTENDED_ALIAS) ? 2u : 1u;
    for (index = 0; index < form->field_count; ++index) {
        const bedrock_field_desc *field = bedrock_form_field(form, index);
        if (field != 0 && (size_t)field->token + 1u > start) {
            start = (size_t)field->token + 1u;
        }
    }
    return start;
}

static uint64_t relocation_placeholder(unsigned type)
{
    unsigned width = bedrock_reloc_width_bits(type);
    if (width == 32u) {
        return 65536u;
    }
    if (width == 64u) {
        return 0x100000000ull;
    }
    return 0u;
}

static size_t instruction_reloc_fixup_offset(
    BedrockSection *section,
    size_t offset,
    size_t word_count,
    unsigned type,
    size_t fallback_offset
) {
    unsigned width = bedrock_reloc_width_bits(type);
    size_t byte_width = width == 0u ? 0u : (size_t)(width / 8u);
    size_t end = offset + word_count * 2u;
    uint64_t placeholder = relocation_placeholder(type);
    size_t cursor;
    size_t index;

    if (byte_width <= 2u || byte_width > 8u || end > section->data.size) {
        return fallback_offset;
    }
    for (cursor = offset; cursor + byte_width <= end; ++cursor) {
        int match = 1;
        for (index = 0; index < byte_width; ++index) {
            if (section->data.data[cursor + index] != (uint8_t)((placeholder >> (index * 8u)) & 0xffu)) {
                match = 0;
                break;
            }
        }
        if (match) {
            return cursor;
        }
    }
    return fallback_offset;
}

static int find_instruction_reloc(BedrockAsm *ctx, char *line, BedrockExpr *expr, char *out, size_t out_size)
{
    char *at = strchr(line, '@');
    char *start;
    char *end;
    char saved;
    char expr_text[160];
    char placeholder[64];
    char mnemonic[32];
    char mnemonic_base[32];
    char *dot;
    char *operand_start;
    size_t prefix_len;
    uint64_t ph;
    if (at == 0) {
        return 0;
    }
    start = at;
    while (start > line && is_ident_char((unsigned char)start[-1])) {
        --start;
    }
    end = at + 1;
    while (isalnum((unsigned char)*end) || *end == '_') {
        ++end;
    }
    if (*end == '+' || *end == '-') {
        ++end;
        while (isspace((unsigned char)*end)) {
            ++end;
        }
        while (isalnum((unsigned char)*end) || *end == 'x' || *end == 'X') {
            ++end;
        }
    }
    if ((size_t)(end - start) >= sizeof(expr_text)) {
        return 0;
    }
    memcpy(expr_text, start, (size_t)(end - start));
    expr_text[end - start] = '\0';
    if (!parse_symbol_expr(ctx, expr_text, BEDROCK_R_NONE, expr)) {
        return 0;
    }
    ph = relocation_placeholder(expr->reloc_type);
    snprintf(placeholder, sizeof(placeholder), "0x%llx", (unsigned long long)ph);

    operand_start = line;
    while (*operand_start != '\0' && !isspace((unsigned char)*operand_start)) {
        ++operand_start;
    }
    prefix_len = (size_t)(operand_start - line);
    if (prefix_len >= sizeof(mnemonic)) {
        prefix_len = sizeof(mnemonic) - 1u;
    }
    memcpy(mnemonic, line, prefix_len);
    mnemonic[prefix_len] = '\0';
    strncpy(mnemonic_base, mnemonic, sizeof(mnemonic_base) - 1u);
    mnemonic_base[sizeof(mnemonic_base) - 1u] = '\0';
    dot = strchr(mnemonic_base, '.');
    if (dot != 0) {
        *dot = '\0';
    }
    while (isspace((unsigned char)*operand_start)) {
        ++operand_start;
    }

    saved = *start;
    *start = '\0';
    snprintf(out, out_size, "%s%s%s", line, placeholder, end);
    *start = saved;
    return 1;
}

static void emit_instruction_words(BedrockAsm *ctx, const uint16_t *words, size_t word_count)
{
    BedrockSection *section = bedrock_asm_current_section(ctx);
    size_t index;
    if (section == 0) {
        return;
    }
    for (index = 0; index < word_count; ++index) {
        uint8_t bytes[2];
        bytes[0] = (uint8_t)(words[index] & 0xffu);
        bytes[1] = (uint8_t)((words[index] >> 8) & 0xffu);
        if (!bedrock_section_emit(section, bytes, sizeof(bytes))) {
            bedrock_asm_error(ctx, "out of memory while emitting instruction");
            return;
        }
    }
}

static void emit_instruction(BedrockAsm *ctx, char *line)
{
    BedrockSection *section = bedrock_asm_current_section(ctx);
    uint16_t words[BEDROCK_MAX_INSTRUCTION_WORDS];
    size_t word_count = 0;
    size_t offset;
    const bedrock_form_desc *form = 0;
    int status;
    BedrockExpr expr;
    char transformed[512];
    int has_reloc = find_instruction_reloc(ctx, line, &expr, transformed, sizeof(transformed));
    if (section == 0) {
        return;
    }
    status = bedrock_assemble_line(has_reloc ? transformed : line, words, BEDROCK_MAX_INSTRUCTION_WORDS, &word_count, &form);
    if (status != BEDROCK_OK) {
        bedrock_asm_error(ctx, "cannot assemble instruction `%s`", line);
        return;
    }
    offset = section->logical_size;
    emit_instruction_words(ctx, words, word_count);
    if (has_reloc) {
        size_t payload_word = instruction_payload_start(form) + ((words[0] & BEDROCK_WORD0_PREFIX_BIT) != 0u ? 1u : 0u);
        size_t fixup_offset = instruction_reloc_fixup_offset(section, offset, word_count, expr.reloc_type, offset + payload_word * 2u);
        unsigned width = bedrock_reloc_width_bits(expr.reloc_type);
        size_t byte_width = width == 0u ? 0u : (size_t)(width / 8u);
        if (byte_width != 0u && fixup_offset + byte_width <= section->data.size) {
            memset(section->data.data + fixup_offset, 0, byte_width);
        }
        if (!bedrock_section_add_reloc(section, fixup_offset, expr.symbol, expr.reloc_type, expr.value)) {
            bedrock_asm_error(ctx, "out of memory while adding instruction relocation");
        }
    }
}

static char *consume_labels(BedrockAsm *ctx, char *line)
{
    for (;;) {
        char *colon = strchr(line, ':');
        char *scan;
        if (colon == 0) {
            return line;
        }
        for (scan = line; scan < colon; ++scan) {
            if (!is_ident_char((unsigned char)*scan)) {
                return line;
            }
        }
        *colon = '\0';
        bedrock_asm_define_symbol(ctx, trim(line));
        line = trim(colon + 1);
    }
}

int bedrock_asm_parse_file(BedrockAsm *ctx, const char *path)
{
    FILE *fp = fopen(path, "r");
    char line_buf[4096];
    if (fp == 0) {
        fprintf(stderr, "%s: cannot open input\n", path);
        return 0;
    }
    ctx->input_name = path;
    ctx->line_number = 0;
    while (fgets(line_buf, sizeof(line_buf), fp) != 0) {
        char *line;
        ++ctx->line_number;
        line_buf[strcspn(line_buf, "\r\n")] = '\0';
        strip_comment(line_buf);
        line = trim(line_buf);
        if (*line == '\0') {
            continue;
        }
        line = consume_labels(ctx, line);
        if (*line == '\0') {
            continue;
        }
        if (*line == '.') {
            handle_directive(ctx, line);
        } else {
            emit_instruction(ctx, line);
        }
    }
    fclose(fp);
    return ctx->error_count == 0u;
}
