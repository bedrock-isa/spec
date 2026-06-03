#include "bedrock_asm.h"

#include <ctype.h>
#include <stdlib.h>
#include <string.h>

#define BEDROCK_REPG_START_PREFIX 0x70u
#define BEDROCK_REPG_END_PREFIX 0x78u
#define BEDROCK_REPG_MAX_GROUP_INSTRUCTIONS 32u

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

static int starts_ci(const char *text, const char *prefix)
{
    while (*prefix != '\0') {
        if (*text == '\0' || toupper((unsigned char)*text) != toupper((unsigned char)*prefix)) {
            return 0;
        }
        ++text;
        ++prefix;
    }
    return 1;
}

static int contains_ci(const char *text, const char *needle)
{
    size_t needle_len = strlen(needle);
    if (needle_len == 0u) {
        return 1;
    }
    while (*text != '\0') {
        if (starts_ci(text, needle)) {
            return 1;
        }
        ++text;
    }
    return 0;
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

static int parse_dreg_token(char *text, unsigned *reg)
{
    char *cursor = trim(text);
    char *end;
    unsigned long value;
    if (toupper((unsigned char)cursor[0]) != 'D' || !isdigit((unsigned char)cursor[1])) {
        return 0;
    }
    value = strtoul(cursor + 1, &end, 10);
    end = trim(end);
    if (*end != '\0' || value > 7ul) {
        return 0;
    }
    *reg = (unsigned)value;
    return 1;
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

static int prefix_is_repeat(uint16_t prefix)
{
    return prefix >= 0x80u || (prefix >= 0x70u && prefix <= 0x78u);
}

static int prefix_word_has_repeat(uint16_t word)
{
    uint16_t low = (uint16_t)(word & 0x00ffu);
    uint16_t high = (uint16_t)((word >> 8) & 0x00ffu);
    return prefix_is_repeat(low) || prefix_is_repeat(high);
}

static int merge_prefix_byte(uint16_t *word, uint16_t prefix)
{
    uint16_t low = (uint16_t)(*word & 0x00ffu);
    uint16_t high = (uint16_t)((*word >> 8) & 0x00ffu);
    if (prefix == 0u || low == prefix || high == prefix) {
        return 1;
    }
    if (low == 0u) {
        *word = (uint16_t)((*word & 0xff00u) | prefix);
        return 1;
    }
    if (high == 0u) {
        *word = (uint16_t)((*word & 0x00ffu) | (uint16_t)(prefix << 8));
        return 1;
    }
    return 0;
}

static int add_prefix_to_instruction(uint16_t *words, size_t *word_count, uint16_t prefix)
{
    size_t index;
    if (*word_count == 0u) {
        return 0;
    }
    if ((words[0] & BEDROCK_WORD0_PREFIX_BIT) != 0u) {
        return merge_prefix_byte(&words[1], prefix);
    }
    if (*word_count + 1u > BEDROCK_MAX_INSTRUCTION_WORDS) {
        return 0;
    }
    for (index = *word_count; index > 1u; --index) {
        words[index] = words[index - 1u];
    }
    words[1] = prefix;
    ++*word_count;
    words[0] = (uint16_t)(
        (words[0] & (uint16_t)~BEDROCK_WORD0_LENGTH_MASK)
        | BEDROCK_WORD0_PREFIX_BIT
        | (uint16_t)((*word_count - 1u) << 12)
    );
    return 1;
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

static int append_repg_piece(BedrockAsm *ctx, char *piece, char items[][512], size_t *count)
{
    char *line = trim(piece);
    if (*line == '\0') {
        return 1;
    }
    if (*line == '.' || strchr(line, ':') != 0) {
        bedrock_asm_error(ctx, "directives and labels are not supported inside REPG blocks");
        return 0;
    }
    if (strchr(line, '@') != 0) {
        bedrock_asm_error(ctx, "relocations are not supported inside REPG blocks yet");
        return 0;
    }
    if (*count >= BEDROCK_REPG_MAX_GROUP_INSTRUCTIONS) {
        bedrock_asm_error(ctx, "REPG group is too large to fit in one 64-byte grouping window");
        return 0;
    }
    strncpy(items[*count], line, 511u);
    items[*count][511] = '\0';
    ++*count;
    return 1;
}

static int append_repg_content(BedrockAsm *ctx, char *text, char items[][512], size_t *count, int *closed)
{
    char *cursor = text;
    char *piece_start = cursor;
    int bracket_depth = 0;
    while (*cursor != '\0') {
        if (*cursor == '[') {
            ++bracket_depth;
        } else if (*cursor == ']') {
            --bracket_depth;
        } else if (bracket_depth == 0 && (*cursor == ';' || *cursor == '}')) {
            char delimiter = *cursor;
            *cursor = '\0';
            if (!append_repg_piece(ctx, piece_start, items, count)) {
                return 0;
            }
            if (delimiter == '}') {
                *closed = 1;
                return 1;
            }
            piece_start = cursor + 1;
        }
        ++cursor;
    }
    return append_repg_piece(ctx, piece_start, items, count);
}

static int is_repg_header_name(const char *line)
{
    const char *cursor = line;
    while (isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    if (starts_ci(cursor, "REPGF") && (cursor[5] == '\0' || isspace((unsigned char)cursor[5]))) {
        return 1;
    }
    return starts_ci(cursor, "REPG") && (cursor[4] == '\0' || isspace((unsigned char)cursor[4]));
}

static int parse_repg_header(BedrockAsm *ctx, char *line, unsigned *counter, char **content_start, int *fast_required)
{
    char *cursor = trim(line);
    char *reg_start;
    char *reg_end;
    char saved;
    if (starts_ci(cursor, "REPGF") && (cursor[5] == '\0' || isspace((unsigned char)cursor[5]))) {
        *fast_required = 1;
        cursor = trim(cursor + 5);
    } else if (starts_ci(cursor, "REPG") && (cursor[4] == '\0' || isspace((unsigned char)cursor[4]))) {
        *fast_required = 0;
        cursor = trim(cursor + 4);
    } else {
        return 0;
    }
    reg_start = cursor;
    while (*cursor != '\0' && *cursor != ',' && *cursor != '{' && !isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    reg_end = cursor;
    saved = *reg_end;
    *reg_end = '\0';
    if (!parse_dreg_token(reg_start, counter)) {
        *reg_end = saved;
        bedrock_asm_error(ctx, "REPG/REPGF requires a D register counter");
        return 0;
    }
    *reg_end = saved;
    cursor = trim(reg_end);
    if (*cursor == ',') {
        cursor = trim(cursor + 1);
    }
    if (*cursor != '{') {
        bedrock_asm_error(ctx, "REPG/REPGF requires `{` after the counter");
        return 0;
    }
    *content_start = cursor + 1;
    return 1;
}

static size_t split_instruction_operands(const char *line, char operands[][128], size_t max_operands)
{
    char buffer[512];
    char *cursor;
    size_t count = 0;
    while (isspace((unsigned char)*line)) {
        ++line;
    }
    while (*line != '\0' && !isspace((unsigned char)*line)) {
        ++line;
    }
    while (isspace((unsigned char)*line)) {
        ++line;
    }
    if (*line == '\0') {
        return 0;
    }
    strncpy(buffer, line, sizeof(buffer) - 1u);
    buffer[sizeof(buffer) - 1u] = '\0';
    cursor = buffer;
    while (*cursor != '\0' && count < max_operands) {
        char *part = next_csv(&cursor);
        if (*part != '\0') {
            strncpy(operands[count], part, 127u);
            operands[count][127] = '\0';
            ++count;
        }
    }
    return count;
}

static int operand_is_selected_dreg(const char *operand, unsigned counter)
{
    char buffer[128];
    char *cursor;
    char *end;
    unsigned long value;
    strncpy(buffer, operand, sizeof(buffer) - 1u);
    buffer[sizeof(buffer) - 1u] = '\0';
    cursor = trim(buffer);
    if (toupper((unsigned char)cursor[0]) != 'D' || !isdigit((unsigned char)cursor[1])) {
        return 0;
    }
    value = strtoul(cursor + 1, &end, 10);
    end = trim(end);
    return *end == '\0' && value == (unsigned long)counter;
}

static int repg_form_is_forbidden(const bedrock_form_desc *form)
{
    const char *mnemonic = form->mnemonic != 0 ? form->mnemonic : "";
    const char *category = form->category != 0 ? form->category : "";
    const char *group = form->group != 0 ? form->group : "";
    const char *id = form->id != 0 ? form->id : "";
    if (contains_ci(category, "control") || contains_ci(category, "system") || contains_ci(category, "atomic")) {
        return 1;
    }
    if (contains_ci(group, "TLB") || contains_ci(group, "CACHE") || contains_ci(group, "FENCE")) {
        return 1;
    }
    if (contains_ci(id, "TLB") || contains_ci(id, "CACHE") || contains_ci(id, "FENCE")) {
        return 1;
    }
    if (ieq(mnemonic, "PUSH") || ieq(mnemonic, "POP") || ieq(mnemonic, "PUSHM") || ieq(mnemonic, "POPM")) {
        return 1;
    }
    if (starts_ci(mnemonic, "MOVSET") || starts_ci(mnemonic, "XCHGSET") || starts_ci(mnemonic, "XCHG")) {
        return 1;
    }
    if (ieq(mnemonic, "WAIT") || ieq(mnemonic, "YIELD") || ieq(mnemonic, "CPUID")) {
        return 1;
    }
    return 0;
}

static int repgf_writes_selected_counter(const bedrock_form_desc *form, const char *line, unsigned counter)
{
    char operands[5][128];
    size_t count = split_instruction_operands(line, operands, 5u);
    const char *mnemonic = form->mnemonic != 0 ? form->mnemonic : "";
    if (count == 0u) {
        return 0;
    }
    if (ieq(mnemonic, "CMP") || ieq(mnemonic, "TEST") || ieq(mnemonic, "BTEST") || ieq(mnemonic, "PREFETCH")) {
        return 0;
    }
    if (ieq(mnemonic, "DIVMODU") || ieq(mnemonic, "DIVMODS")) {
        return (count >= 2u && operand_is_selected_dreg(operands[count - 1u], counter))
            || (count >= 3u && operand_is_selected_dreg(operands[count - 2u], counter));
    }
    if (starts_ci(mnemonic, "XCHG")) {
        size_t index;
        for (index = 0; index < count; ++index) {
            if (operand_is_selected_dreg(operands[index], counter)) {
                return 1;
            }
        }
        return 0;
    }
    return operand_is_selected_dreg(operands[count - 1u], counter);
}

static int repgf_uses_pc_relative_addressing(const char *line)
{
    const char *start = line;
    int bracket_depth = 0;
    while (*line != '\0') {
        if (*line == '[') {
            ++bracket_depth;
        } else if (*line == ']') {
            if (bracket_depth > 0) {
                --bracket_depth;
            }
        } else if (bracket_depth > 0 && toupper((unsigned char)line[0]) == 'P' && toupper((unsigned char)line[1]) == 'C') {
            int before_ok = line == start || !is_ident_char((unsigned char)line[-1]);
            int after_ok = !is_ident_char((unsigned char)line[2]);
            if (before_ok && after_ok) {
                return 1;
            }
        }
        ++line;
    }
    return 0;
}

static int validate_repg_instruction(BedrockAsm *ctx, char *line, const bedrock_form_desc *form)
{
    if (form == 0) {
        bedrock_asm_error(ctx, "REPG could not classify grouped instruction `%s`", line);
        return 0;
    }
    if (repg_form_is_forbidden(form)) {
        bedrock_asm_error(ctx, "REPG instruction `%s` is not eligible for grouped repeat", line);
        return 0;
    }
    return 1;
}

static int validate_repgf_instruction(BedrockAsm *ctx, unsigned counter, char *line, const bedrock_form_desc *form)
{
    if (!validate_repg_instruction(ctx, line, form)) {
        return 0;
    }
    if (repgf_uses_pc_relative_addressing(line)) {
        bedrock_asm_error(ctx, "REPGF instruction `%s` uses PC-relative addressing", line);
        return 0;
    }
    if (repgf_writes_selected_counter(form, line, counter)) {
        bedrock_asm_error(ctx, "REPGF instruction `%s` writes the selected counter D%u", line, counter);
        return 0;
    }
    return 1;
}

static void emit_repg_group(BedrockAsm *ctx, unsigned counter, char items[][512], size_t count, int fast_required)
{
    uint16_t inner_words[BEDROCK_REPG_MAX_GROUP_INSTRUCTIONS][BEDROCK_MAX_INSTRUCTION_WORDS];
    size_t inner_counts[BEDROCK_REPG_MAX_GROUP_INSTRUCTIONS];
    size_t total_words;
    size_t index;
    const bedrock_form_desc *form = 0;
    BedrockSection *section = bedrock_asm_current_section(ctx);
    if (count == 0u || count > BEDROCK_REPG_MAX_GROUP_INSTRUCTIONS) {
        bedrock_asm_error(ctx, "REPG requires at least one grouped instruction within one 64-byte grouping window");
        return;
    }
    if (section == 0) {
        return;
    }
    total_words = 0u;
    for (index = 0; index < count; ++index) {
        int status = bedrock_assemble_line(items[index], inner_words[index], BEDROCK_MAX_INSTRUCTION_WORDS, &inner_counts[index], &form);
        if (status != BEDROCK_OK) {
            bedrock_asm_error(ctx, "cannot assemble REPG instruction `%s`", items[index]);
            return;
        }
        if ((inner_words[index][0] & BEDROCK_WORD0_PREFIX_BIT) != 0u && prefix_word_has_repeat(inner_words[index][1])) {
            bedrock_asm_error(ctx, "nested repeat prefixes are not supported inside REPG blocks");
            return;
        }
        if (!validate_repg_instruction(ctx, items[index], form)) {
            return;
        }
        if (fast_required && !validate_repgf_instruction(ctx, counter, items[index], form)) {
            return;
        }
        total_words += inner_counts[index];
    }
    if (!add_prefix_to_instruction(
            inner_words[0],
            &inner_counts[0],
            (uint16_t)(BEDROCK_REPG_START_PREFIX | (uint16_t)(counter & 0x07u))
        )) {
        bedrock_asm_error(ctx, "first REPG instruction cannot fit its prefix within the 8-word instruction limit");
        return;
    }
    if (!add_prefix_to_instruction(
            inner_words[count - 1u],
            &inner_counts[count - 1u],
            BEDROCK_REPG_END_PREFIX
        )) {
        bedrock_asm_error(ctx, "final REPG instruction cannot fit its ENDG prefix within the 8-word instruction limit");
        return;
    }
    total_words = 0u;
    for (index = 0; index < count; ++index) {
        total_words += inner_counts[index];
    }
    if (total_words * 2u > 64u) {
        bedrock_asm_error(ctx, "REPG group exceeds one 64-byte grouping window");
        return;
    }
    if (((section->logical_size & 63u) + total_words * 2u) > 64u) {
        if (!bedrock_section_align(section, 64u)) {
            bedrock_asm_error(ctx, "out of memory while aligning REPG group");
            return;
        }
    }
    for (index = 0; index < count; ++index) {
        emit_instruction_words(ctx, inner_words[index], inner_counts[index]);
    }
}

static int handle_repg_block(BedrockAsm *ctx, FILE *fp, char *line)
{
    unsigned counter = 0;
    char *content = 0;
    int fast_required = 0;
    char items[BEDROCK_REPG_MAX_GROUP_INSTRUCTIONS][512];
    size_t count = 0;
    int closed = 0;
    char line_buf[4096];
    if (!parse_repg_header(ctx, line, &counter, &content, &fast_required)) {
        return 0;
    }
    if (!append_repg_content(ctx, content, items, &count, &closed)) {
        return 1;
    }
    while (!closed && fgets(line_buf, sizeof(line_buf), fp) != 0) {
        char *piece;
        ++ctx->line_number;
        line_buf[strcspn(line_buf, "\r\n")] = '\0';
        strip_comment(line_buf);
        piece = trim(line_buf);
        if (*piece == '\0') {
            continue;
        }
        if (!append_repg_content(ctx, piece, items, &count, &closed)) {
            return 1;
        }
    }
    if (!closed) {
        bedrock_asm_error(ctx, "unterminated REPG block");
        return 1;
    }
    emit_repg_group(ctx, counter, items, count, fast_required);
    return 1;
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
        if (is_repg_header_name(line)) {
            (void)handle_repg_block(ctx, fp, line);
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
