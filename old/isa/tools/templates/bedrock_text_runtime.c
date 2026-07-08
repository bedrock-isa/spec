#define BEDROCK_TEXT_MAX_OPERANDS 8u
#define BEDROCK_TEXT_MAX_FIELDS 32u
#define BEDROCK_TEXT_OPERAND_CHARS 96u

typedef struct bedrock_text_operand {
    char text[BEDROCK_TEXT_OPERAND_CHARS];
    uint64_t value;
    uint16_t payload[5];
    size_t payload_count;
    int cost;
} bedrock_text_operand;

typedef struct bedrock_text_line {
    char mnemonic[32];
    char size_suffix;
    uint16_t condition;
    uint16_t memory_order;
    int has_condition;
    int has_memory_order;
    size_t operand_count;
    char operands[BEDROCK_TEXT_MAX_OPERANDS][BEDROCK_TEXT_OPERAND_CHARS];
} bedrock_text_line;

static int bedrock_ascii_upper(int ch)
{
    return ch >= 'a' && ch <= 'z' ? ch - ('a' - 'A') : ch;
}

static int bedrock_char_ieq(char lhs, char rhs)
{
    return bedrock_ascii_upper((unsigned char)lhs) == bedrock_ascii_upper((unsigned char)rhs);
}

static int bedrock_streq_ci(const char *lhs, const char *rhs)
{
    while (*lhs != '\0' && *rhs != '\0') {
        if (!bedrock_char_ieq(*lhs, *rhs)) {
            return 0;
        }
        ++lhs;
        ++rhs;
    }
    return *lhs == '\0' && *rhs == '\0';
}

static int bedrock_starts_ci(const char *text, const char *prefix, size_t prefix_len)
{
    size_t index;
    for (index = 0; index < prefix_len; ++index) {
        if (text[index] == '\0' || !bedrock_char_ieq(text[index], prefix[index])) {
            return 0;
        }
    }
    return 1;
}

static int bedrock_contains_ci(const char *text, const char *needle)
{
    size_t needle_len = strlen(needle);
    if (needle_len == 0u) {
        return 1;
    }
    while (*text != '\0') {
        if (bedrock_starts_ci(text, needle, needle_len)) {
            return 1;
        }
        ++text;
    }
    return 0;
}

static void bedrock_trim_copy(char *dst, size_t dst_size, const char *start, const char *end)
{
    size_t len;
    while (start < end && isspace((unsigned char)*start)) {
        ++start;
    }
    while (end > start && isspace((unsigned char)end[-1])) {
        --end;
    }
    len = (size_t)(end - start);
    if (dst_size == 0u) {
        return;
    }
    if (len >= dst_size) {
        len = dst_size - 1u;
    }
    memcpy(dst, start, len);
    dst[len] = '\0';
}

static void bedrock_compact_copy(char *dst, size_t dst_size, const char *src)
{
    size_t out = 0;
    if (dst_size == 0u) {
        return;
    }
    while (*src != '\0' && out + 1u < dst_size) {
        if (!isspace((unsigned char)*src)) {
            dst[out++] = (char)bedrock_ascii_upper((unsigned char)*src);
        }
        ++src;
    }
    dst[out] = '\0';
}

static int bedrock_parse_u64(const char *text, uint64_t *value)
{
    char *end = 0;
    unsigned long long parsed;
    while (isspace((unsigned char)*text)) {
        ++text;
    }
    if (*text == '#') {
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

static int bedrock_parse_i64(const char *text, int64_t *value)
{
    char *end = 0;
    long long parsed;
    while (isspace((unsigned char)*text)) {
        ++text;
    }
    if (*text == '#') {
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

static size_t bedrock_words_for_size_suffix(char suffix);

static int bedrock_parse_immediate_payload_text(const char *text, uint64_t *value, size_t *forced_words)
{
    char compact[96];
    size_t len;
    int64_t signed_value;
    uint64_t unsigned_value;
    *forced_words = 0;
    bedrock_compact_copy(compact, sizeof(compact), text);
    len = strlen(compact);
    if (len > 2u && compact[len - 2u] == '.') {
        char suffix = (char)bedrock_ascii_upper((unsigned char)compact[len - 1u]);
        if (suffix == 'W' || suffix == 'L' || suffix == 'Q') {
            *forced_words = bedrock_words_for_size_suffix(suffix);
            compact[len - 2u] = '\0';
        }
    }
    if (compact[0] == '-' || compact[0] == '+') {
        if (!bedrock_parse_i64(compact, &signed_value)) {
            return 0;
        }
        *value = (uint64_t)signed_value;
        return 1;
    }
    if (!bedrock_parse_u64(compact, &unsigned_value)) {
        return 0;
    }
    *value = unsigned_value;
    return 1;
}

static int bedrock_lookup_named(const bedrock_named_value *names, size_t count, const char *text, uint16_t *value)
{
    size_t index;
    for (index = 0; index < count; ++index) {
        if (names[index].name != 0 && bedrock_streq_ci(names[index].name, text)) {
            *value = names[index].value;
            return 1;
        }
    }
    return 0;
}

static const char *bedrock_name_for_value(const bedrock_named_value *names, size_t count, uint16_t value)
{
    size_t index;
    for (index = 0; index < count; ++index) {
        if (names[index].name != 0 && names[index].value == value) {
            return names[index].name;
        }
    }
    return "?";
}

static int bedrock_parse_numbered_register(const char *text, char prefix, unsigned max_index, uint64_t *value)
{
    uint64_t number;
    char digits[16];
    if (!bedrock_char_ieq(text[0], prefix)) {
        return 0;
    }
    if (text[1] == '\0') {
        return 0;
    }
    bedrock_trim_copy(digits, sizeof(digits), text + 1, text + strlen(text));
    if (!bedrock_parse_u64(digits, &number) || number > max_index) {
        return 0;
    }
    *value = number;
    return 1;
}

static int bedrock_parse_dbank_selector(const char *text, uint64_t *value)
{
    char compact[32];
    uint64_t number;
    bedrock_compact_copy(compact, sizeof(compact), text);
    if (bedrock_starts_ci(compact, "DB", 2u)) {
        if (!bedrock_parse_u64(compact + 2, &number) || number > 15u) {
            return 0;
        }
        *value = number;
        return 1;
    }
    if (!bedrock_parse_u64(compact, &number) || number > 15u) {
        return 0;
    }
    *value = number;
    return 1;
}

static void bedrock_payload_from_u64(uint64_t value, uint16_t *payload, size_t words)
{
    size_t index;
    for (index = 0; index < words; ++index) {
        payload[index] = (uint16_t)((value >> (index * 16u)) & 0xffffu);
    }
}

static size_t bedrock_words_for_size_suffix(char suffix)
{
    size_t index;
    char upper = (char)bedrock_ascii_upper((unsigned char)suffix);
    for (index = 0; index < bedrock_size_codes_count; ++index) {
        if (bedrock_char_ieq(bedrock_size_codes[index].suffix, upper)) {
            return (bedrock_size_codes[index].bytes + 1u) / 2u;
        }
    }
    return 1;
}

static size_t bedrock_bits_for_size_suffix(char suffix)
{
    size_t index;
    char upper = (char)bedrock_ascii_upper((unsigned char)suffix);
    for (index = 0; index < bedrock_size_codes_count; ++index) {
        if (bedrock_char_ieq(bedrock_size_codes[index].suffix, upper)) {
            return (size_t)bedrock_size_codes[index].bytes * 8u;
        }
    }
    return 64;
}

static int bedrock_value_fits_signed_or_unsigned_bits(uint64_t value, unsigned bits)
{
    uint64_t unsigned_max;
    uint64_t signed_min_encoded;
    if (bits >= 64u) {
        return 1;
    }
    unsigned_max = (1ull << bits) - 1ull;
    signed_min_encoded = (~0ull << (bits - 1u));
    return value <= unsigned_max || value >= signed_min_encoded;
}

static int bedrock_choose_compact_immediate_ea(int64_t signed_value, uint64_t unsigned_value, char size_suffix, bedrock_text_operand *out)
{
    size_t operand_bits = bedrock_bits_for_size_suffix(size_suffix);
    if (signed_value >= -32768 && signed_value <= 32767) {
        out->value = BEDROCK_EA_IMM16;
        out->payload_count = 1;
        bedrock_payload_from_u64((uint64_t)signed_value, out->payload, 1);
        return 1;
    }
    if (signed_value >= INT32_MIN && signed_value <= INT32_MAX) {
        out->value = BEDROCK_EA_IMM32;
        out->payload_count = 2;
        bedrock_payload_from_u64((uint64_t)signed_value, out->payload, 2);
        return 1;
    }
    if (operand_bits <= 32u && unsigned_value <= 0xffffffffull) {
        out->value = BEDROCK_EA_IMM32;
        out->payload_count = 2;
        bedrock_payload_from_u64(unsigned_value, out->payload, 2);
        return 1;
    }
    out->value = BEDROCK_EA_IMM64;
    out->payload_count = 4;
    bedrock_payload_from_u64(unsigned_value, out->payload, 4);
    return 1;
}

static int bedrock_parse_forced_immediate_ea(const char *compact, bedrock_text_operand *out)
{
    char number[96];
    size_t len = strlen(compact);
    size_t number_len;
    uint64_t unsigned_value = 0;
    int64_t signed_value = 0;
    uint64_t payload_value = 0;
    size_t words = 0;
    uint64_t code = 0;
    int is_signed_text;
    char suffix;
    if (len < 3u || compact[len - 2u] != '.') {
        return 0;
    }
    suffix = (char)bedrock_ascii_upper((unsigned char)compact[len - 1u]);
    if (suffix != 'W' && suffix != 'L' && suffix != 'Q') {
        return 0;
    }
    number_len = len - 2u;
    if (number_len == 0u || number_len >= sizeof(number)) {
        return 0;
    }
    memcpy(number, compact, number_len);
    number[number_len] = '\0';
    is_signed_text = number[0] == '-' || number[0] == '+';
    if (is_signed_text) {
        if (!bedrock_parse_i64(number, &signed_value)) {
            return 0;
        }
        payload_value = (uint64_t)signed_value;
    } else {
        if (!bedrock_parse_u64(number, &unsigned_value)) {
            return 0;
        }
        payload_value = unsigned_value;
    }
    if (suffix == 'W') {
        if (is_signed_text) {
            if (signed_value < -32768 || signed_value > 32767) {
                return 0;
            }
        } else if (unsigned_value > 0xffffull) {
            return 0;
        }
        code = BEDROCK_EA_IMM16;
        words = 1;
    } else if (suffix == 'L') {
        if (is_signed_text) {
            if (signed_value < INT32_MIN || signed_value > INT32_MAX) {
                return 0;
            }
        } else if (unsigned_value > 0xffffffffull) {
            return 0;
        }
        code = BEDROCK_EA_IMM32;
        words = 2;
    } else {
        code = BEDROCK_EA_IMM64;
        words = 4;
    }
    out->value = code;
    out->payload_count = words;
    bedrock_payload_from_u64(payload_value, out->payload, words);
    return 1;
}

static int bedrock_scale_code(uint64_t scale, uint16_t *code)
{
    switch (scale) {
    case 1: *code = 0; return 1;
    case 2: *code = 1; return 1;
    case 4: *code = 2; return 1;
    case 8: *code = 3; return 1;
    default: return 0;
    }
}

static int bedrock_segment_code(const char *segment, uint16_t *code)
{
    uint16_t value;
    if (segment == 0 || *segment == '\0') {
        return 0;
    }
    if (!bedrock_lookup_named(bedrock_ea_segment_names, bedrock_ea_segment_names_count, segment, &value)) {
        return 0;
    }
    *code = value;
    return 1;
}

static int bedrock_parse_index_term(char **cursor, uint16_t *index, uint16_t *scale_code, int *signed32_index)
{
    uint64_t reg;
    uint64_t scale;
    char *end;

    if (!bedrock_char_ieq((*cursor)[0], 'D') || !isdigit((unsigned char)(*cursor)[1])) {
        return 0;
    }
    reg = strtoull(*cursor + 1, &end, 10);
    if (end == *cursor + 1 || reg > 7u) {
        return 0;
    }
    *cursor = end;
    *signed32_index = 0;
    if (bedrock_starts_ci(*cursor, ".L", 2u)) {
        *signed32_index = 1;
        *cursor += 2;
    }
    if (**cursor != '*') {
        return 0;
    }
    ++*cursor;
    scale = strtoull(*cursor, &end, 0);
    if (end == *cursor) {
        return 0;
    }
    *cursor = end;
    if (!bedrock_scale_code(scale, scale_code)) {
        return 0;
    }
    *index = (uint16_t)reg;
    return 1;
}

static int bedrock_parse_extended_indexed_ea(char *compact, bedrock_text_operand *out)
{
    char *cursor = compact;
    char *colon;
    uint64_t base_reg = 0;
    uint16_t mode = 0;
    uint16_t segment = 1;
    uint16_t index = 0;
    uint16_t scale = 0;
    uint16_t extra = 0;
    int64_t disp = 0;
    int has_disp = 0;
    int signed32_index = 0;

    colon = strchr(cursor, ':');
    if (colon != 0) {
        *colon = '\0';
        if (!bedrock_segment_code(cursor, &segment)) {
            return 0;
        }
        cursor = colon + 1;
    }

    if (bedrock_char_ieq(cursor[0], 'A') && isdigit((unsigned char)cursor[1])) {
        char *end;
        base_reg = strtoull(cursor + 1, &end, 10);
        if (end == cursor + 1 || base_reg > 7u || *end != '+') {
            return 0;
        }
        cursor = end + 1;
        if (!bedrock_parse_index_term(&cursor, &index, &scale, &signed32_index)) {
            return 0;
        }
        if (*cursor == '+' || *cursor == '-') {
            if (!bedrock_parse_i64(cursor, &disp)) {
                return 0;
            }
            has_disp = 1;
        } else if (*cursor != '\0') {
            return 0;
        }
        if (!has_disp) {
            mode = 0x0u;
        } else if (disp >= -32768 && disp <= 32767) {
            mode = 0x1u;
        } else if (disp >= INT32_MIN && disp <= INT32_MAX) {
            mode = 0x2u;
        } else {
            mode = 0x3u;
        }
        extra = (uint16_t)((base_reg << 5) | ((uint64_t)index << 2) | (uint64_t)scale);
    } else if ((bedrock_starts_ci(cursor, "SP+", 3u) || bedrock_starts_ci(cursor, "PC+", 3u))) {
        int pc_relative = bedrock_char_ieq(cursor[0], 'P');
        segment = 0;
        cursor += 3;
        if (!bedrock_parse_index_term(&cursor, &index, &scale, &signed32_index)) {
            return 0;
        }
        if (*cursor == '+' || *cursor == '-') {
            if (!bedrock_parse_i64(cursor, &disp)) {
                return 0;
            }
        } else if (*cursor == '\0') {
            disp = 0;
        } else {
            return 0;
        }
        if (disp >= -32768 && disp <= 32767) {
            mode = pc_relative ? 0xcu : 0x9u;
        } else if (disp >= INT32_MIN && disp <= INT32_MAX) {
            mode = pc_relative ? 0xdu : 0xau;
        } else {
            mode = pc_relative ? 0xeu : 0xbu;
        }
        extra = (uint16_t)(((uint64_t)index << 2) | (uint64_t)scale);
    } else {
        return 0;
    }

    out->value = signed32_index ? BEDROCK_EA_S32_INDEXED_EXTENDED : BEDROCK_EA_EXTENDED;
    out->payload[0] = (uint16_t)((mode << 11) | (segment << 8) | extra);
    out->payload_count = 1;
    if (mode == 0x1u || mode == 0x9u || mode == 0xcu) {
        bedrock_payload_from_u64((uint64_t)disp, &out->payload[1], 1);
        out->payload_count = 2;
    } else if (mode == 0x2u || mode == 0xau || mode == 0xdu) {
        bedrock_payload_from_u64((uint64_t)disp, &out->payload[1], 2);
        out->payload_count = 3;
    } else if (mode == 0x3u || mode == 0xbu || mode == 0xeu) {
        bedrock_payload_from_u64((uint64_t)disp, &out->payload[1], 4);
        out->payload_count = 5;
    }
    return 1;
}

static int bedrock_size_value_for_kind(const char *kind, char suffix, uint64_t *value)
{
    size_t index;
    char ch = (char)bedrock_ascii_upper((unsigned char)suffix);
    if (ch == '\0') {
        return 0;
    }
    for (index = 0; index < bedrock_size_kind_values_count; ++index) {
        if (strcmp(bedrock_size_kind_values[index].kind, kind) == 0 && bedrock_char_ieq(bedrock_size_kind_values[index].code, ch)) {
            *value = bedrock_size_kind_values[index].value;
            return 1;
        }
    }
    if (strlen(kind) == 1u) {
        if (bedrock_char_ieq(kind[0], ch)) {
            *value = 0;
            return 1;
        }
        return 0;
    }
    return 0;
}

static char bedrock_size_suffix_for_kind(const char *kind, uint64_t value)
{
    size_t index;
    for (index = 0; index < bedrock_size_kind_values_count; ++index) {
        if (strcmp(bedrock_size_kind_values[index].kind, kind) == 0 && bedrock_size_kind_values[index].value == value) {
            return bedrock_size_kind_values[index].code;
        }
    }
    if (strlen(kind) == 1u) {
        return kind[0];
    }
    return '?';
}

static int bedrock_field_is_size_kind(const bedrock_field_desc *field)
{
    size_t index;
    if (strcmp(field->source, "size") == 0) {
        return 1;
    }
    for (index = 0; index < bedrock_size_kind_values_count; ++index) {
        if (strcmp(bedrock_size_kind_values[index].kind, field->kind) == 0) {
            return 1;
        }
    }
    return 0;
}

static int bedrock_parse_line_text(const char *line, bedrock_text_line *parsed)
{
    const char *cursor;
    const char *mnemonic_start;
    const char *mnemonic_end;
    const char *mnemonic_part_end;
    const char *dot;
    const char *slash;
    memset(parsed, 0, sizeof(*parsed));
    cursor = line;
    while (isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    if (*cursor == '\0') {
        return 0;
    }
    mnemonic_start = cursor;
    while (*cursor != '\0' && !isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    mnemonic_end = cursor;
    mnemonic_part_end = mnemonic_end;
    slash = 0;
    {
        const char *scan;
        for (scan = mnemonic_start; scan < mnemonic_end; ++scan) {
            if (*scan == '/') {
                slash = scan;
            }
        }
    }
    if (slash != 0) {
        char order_name[32];
        uint16_t order_value = 0;
        if ((size_t)(mnemonic_end - slash - 1) >= sizeof(order_name)) {
            return 0;
        }
        bedrock_trim_copy(order_name, sizeof(order_name), slash + 1, mnemonic_end);
        if (!bedrock_lookup_named(bedrock_memory_order_names, bedrock_memory_order_names_count, order_name, &order_value)) {
            return 0;
        }
        parsed->memory_order = order_value;
        parsed->has_memory_order = 1;
        mnemonic_part_end = slash;
    }
    dot = 0;
    {
        const char *scan;
        for (scan = mnemonic_start; scan < mnemonic_part_end; ++scan) {
            if (*scan == '.') {
                dot = scan;
            }
        }
    }
    if (dot != 0 && dot + 2 == mnemonic_part_end) {
        parsed->size_suffix = (char)bedrock_ascii_upper((unsigned char)dot[1]);
        mnemonic_part_end = dot;
    }
    bedrock_trim_copy(parsed->mnemonic, sizeof(parsed->mnemonic), mnemonic_start, mnemonic_part_end);
    while (isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    while (*cursor != '\0') {
        const char *start = cursor;
        int depth = 0;
        if (parsed->operand_count >= BEDROCK_TEXT_MAX_OPERANDS) {
            return 0;
        }
        while (*cursor != '\0') {
            if (*cursor == '[' || *cursor == '{') {
                ++depth;
            } else if (*cursor == ']' || *cursor == '}') {
                --depth;
            } else if (*cursor == ',' && depth == 0) {
                break;
            }
            ++cursor;
        }
        bedrock_trim_copy(parsed->operands[parsed->operand_count], BEDROCK_TEXT_OPERAND_CHARS, start, cursor);
        ++parsed->operand_count;
        if (*cursor == ',') {
            ++cursor;
            while (isspace((unsigned char)*cursor)) {
                ++cursor;
            }
        }
    }
    return 1;
}

static int bedrock_form_mnemonic_matches(const bedrock_form_desc *form, bedrock_text_line *parsed)
{
    size_t len = strlen(form->mnemonic);
    parsed->has_condition = 0;
    parsed->condition = 0;
    if (bedrock_streq_ci(form->mnemonic, parsed->mnemonic)) {
        return 1;
    }
    if (len > 2u && bedrock_char_ieq(form->mnemonic[len - 2u], 'c') && bedrock_char_ieq(form->mnemonic[len - 1u], 'c')) {
        uint16_t condition;
        size_t prefix_len = len - 2u;
        const char *suffix = parsed->mnemonic + prefix_len;
        if (bedrock_starts_ci(parsed->mnemonic, form->mnemonic, prefix_len)
            && *suffix != '\0'
            && bedrock_lookup_named(bedrock_condition_names, bedrock_condition_names_count, suffix, &condition)) {
            parsed->has_condition = 1;
            parsed->condition = condition;
            return 1;
        }
    }
    return 0;
}

static int bedrock_merge_prefix_byte(uint16_t *prefix_word, uint16_t prefix_byte)
{
    uint16_t low = (uint16_t)(*prefix_word & 0x00ffu);
    uint16_t high = (uint16_t)((*prefix_word >> 8) & 0x00ffu);
    if (prefix_byte == 0u || low == prefix_byte || high == prefix_byte) {
        return 1;
    }
    if (low == 0u) {
        *prefix_word = (uint16_t)((*prefix_word & 0xff00u) | prefix_byte);
        return 1;
    }
    if (high == 0u) {
        *prefix_word = (uint16_t)((*prefix_word & 0x00ffu) | (uint16_t)(prefix_byte << 8));
        return 1;
    }
    return 0;
}

static int bedrock_normalize_update_operand(char *operand, uint16_t *prefix_word)
{
    char compact[96];
    char inner[96];
    char *end;
    unsigned long reg;
    uint16_t prefix_byte = 0;
    bedrock_compact_copy(compact, sizeof(compact), operand);
    if (compact[0] != '[' || compact[strlen(compact) - 1u] != ']') {
        return 1;
    }
    bedrock_trim_copy(inner, sizeof(inner), compact + 1, compact + strlen(compact) - 1u);
    if (bedrock_char_ieq(inner[0], 'A') && isdigit((unsigned char)inner[1])) {
        reg = strtoul(inner + 1, &end, 10);
        if (end != inner + 1 && reg <= 7ul && strcmp(end, "++") == 0) {
            prefix_byte = BEDROCK_PREFIX_POSTINC;
        } else if (end != inner + 1 && reg <= 7ul && strcmp(end, "--") == 0) {
            prefix_byte = BEDROCK_PREFIX_POSTDEC;
        } else {
            return 1;
        }
    } else if (inner[0] == '+' && inner[1] == '+' && bedrock_char_ieq(inner[2], 'A') && isdigit((unsigned char)inner[3])) {
        reg = strtoul(inner + 3, &end, 10);
        if (end == inner + 3 || reg > 7ul || *end != '\0') {
            return 1;
        }
        prefix_byte = BEDROCK_PREFIX_PREINC;
    } else if (inner[0] == '-' && inner[1] == '-' && bedrock_char_ieq(inner[2], 'A') && isdigit((unsigned char)inner[3])) {
        reg = strtoul(inner + 3, &end, 10);
        if (end == inner + 3 || reg > 7ul || *end != '\0') {
            return 1;
        }
        prefix_byte = BEDROCK_PREFIX_PREDEC;
    } else {
        return 1;
    }
    if (!bedrock_merge_prefix_byte(prefix_word, prefix_byte)) {
        return 0;
    }
    snprintf(operand, BEDROCK_TEXT_OPERAND_CHARS, "[A%lu]", reg);
    return 1;
}

static int bedrock_normalize_update_operands(bedrock_text_line *parsed, uint16_t *prefix_word)
{
    size_t index;
    for (index = 0; index < parsed->operand_count; ++index) {
        if (!bedrock_normalize_update_operand(parsed->operands[index], prefix_word)) {
            return 0;
        }
    }
    return 1;
}

static int bedrock_parse_compact_ea(const char *text, bedrock_text_operand *out, char size_suffix)
{
    char compact[96];
    uint64_t reg;
    int64_t disp;
    char *plus;
    bedrock_compact_copy(compact, sizeof(compact), text);

    if (bedrock_parse_forced_immediate_ea(compact, out)) {
        return 1;
    }
    if (bedrock_parse_numbered_register(compact, 'D', 7, &reg)) {
        out->value = BEDROCK_EA_DREG + reg;
        out->cost = 1;
        return 1;
    }
    if (bedrock_parse_numbered_register(compact, 'A', 7, &reg)) {
        out->value = BEDROCK_EA_AREG + reg;
        out->cost = 1;
        return 1;
    }
    if (bedrock_streq_ci(compact, "SP")) {
        out->value = BEDROCK_EA_SPREG;
        out->cost = 1;
        return 1;
    }
    if (compact[0] != '[') {
        uint64_t imm;
        int64_t signed_imm;
        if ((compact[0] == '-' || compact[0] == '+') && bedrock_parse_i64(compact, &signed_imm)) {
            return bedrock_choose_compact_immediate_ea(signed_imm, (uint64_t)signed_imm, size_suffix, out);
        }
        if (bedrock_parse_u64(compact, &imm)) {
            signed_imm = imm <= 0x7fffffffffffffffull ? (int64_t)imm : INT64_MAX;
            return bedrock_choose_compact_immediate_ea(signed_imm, imm, size_suffix, out);
        }
        return 0;
    }
    if (compact[strlen(compact) - 1u] != ']') {
        return 0;
    }
    compact[strlen(compact) - 1u] = '\0';
    memmove(compact, compact + 1, strlen(compact));

    if (bedrock_parse_extended_indexed_ea(compact, out)) {
        return 1;
    }
    if (bedrock_parse_numbered_register(compact, 'A', 7, &reg)) {
        out->value = BEDROCK_EA_INDIRECT + reg;
        return 1;
    }
    plus = strchr(compact, '+');
    if (plus != 0) {
        *plus = '\0';
        if (bedrock_parse_numbered_register(compact, 'A', 7, &reg) && bedrock_parse_i64(plus + 1, &disp)) {
            uint64_t udisp = (uint64_t)disp;
            if (disp >= -32768 && disp <= 32767) {
                out->value = BEDROCK_EA_A_DISP16 + reg;
                out->payload_count = 1;
                bedrock_payload_from_u64(udisp, out->payload, 1);
                return 1;
            }
            out->value = BEDROCK_EA_A_DISP32 + reg;
            out->payload_count = 2;
            bedrock_payload_from_u64(udisp, out->payload, 2);
            return 1;
        }
        if (bedrock_streq_ci(compact, "PC") && bedrock_parse_i64(plus + 1, &disp)) {
            uint64_t udisp = (uint64_t)disp;
            if (disp >= -32768 && disp <= 32767) {
                out->value = BEDROCK_EA_PC_DISP16;
                out->payload_count = 1;
                bedrock_payload_from_u64(udisp, out->payload, 1);
                return 1;
            }
            out->value = BEDROCK_EA_PC_DISP32;
            out->payload_count = 2;
            bedrock_payload_from_u64(udisp, out->payload, 2);
            return 1;
        }
        if (bedrock_streq_ci(compact, "SP") && bedrock_parse_i64(plus + 1, &disp)) {
            uint64_t udisp = (uint64_t)disp;
            if (disp >= -32768 && disp <= 32767) {
                out->value = BEDROCK_EA_SP_DISP16;
                out->payload_count = 1;
                bedrock_payload_from_u64(udisp, out->payload, 1);
                return 1;
            }
            out->value = BEDROCK_EA_SP_DISP32;
            out->payload_count = 2;
            bedrock_payload_from_u64(udisp, out->payload, 2);
            return 1;
        }
    }
    {
        uint64_t absolute;
        if (bedrock_parse_u64(compact, &absolute)) {
            if (absolute <= 0xffffffffull) {
                out->value = BEDROCK_EA_ABS32;
                out->payload_count = 2;
                bedrock_payload_from_u64(absolute, out->payload, 2);
                return 1;
            }
            out->value = BEDROCK_EA_ABS64;
            out->payload_count = 4;
            bedrock_payload_from_u64(absolute, out->payload, 4);
            return 1;
        }
    }
    return 0;
}

static int bedrock_is_bitmap_kind(const char *kind)
{
    size_t range_index;
    for (range_index = 0; range_index < bedrock_bitmap_ranges_count; ++range_index) {
        if (strcmp(kind, bedrock_bitmap_ranges[range_index].kind) == 0) {
            return 1;
        }
    }
    return 0;
}

static int bedrock_parse_bitmap_register(const char *bitmap_kind, const char *text, char *kind, unsigned *index)
{
    size_t range_index;
    uint64_t value;
    if (text[0] == '\0' || !isdigit((unsigned char)text[1])) {
        return 0;
    }
    if (!bedrock_parse_u64(text + 1, &value)) {
        return 0;
    }
    for (range_index = 0; range_index < bedrock_bitmap_ranges_count; ++range_index) {
        unsigned max_index;
        if (strcmp(bitmap_kind, bedrock_bitmap_ranges[range_index].kind) != 0) {
            continue;
        }
        max_index = (unsigned)(bedrock_bitmap_ranges[range_index].high_bit - bedrock_bitmap_ranges[range_index].low_bit);
        if (bedrock_char_ieq(text[0], bedrock_bitmap_ranges[range_index].reg_prefix) && value <= max_index) {
            *kind = bedrock_bitmap_ranges[range_index].reg_prefix;
            *index = (unsigned)value;
            return 1;
        }
    }
    return 0;
}

static int bedrock_bitmap_bit_for_register(const char *bitmap_kind, char kind, unsigned index, unsigned *bit)
{
    size_t range_index;
    for (range_index = 0; range_index < bedrock_bitmap_ranges_count; ++range_index) {
        unsigned max_index;
        if (strcmp(bitmap_kind, bedrock_bitmap_ranges[range_index].kind) != 0) {
            continue;
        }
        max_index = (unsigned)(bedrock_bitmap_ranges[range_index].high_bit - bedrock_bitmap_ranges[range_index].low_bit);
        if (bedrock_char_ieq(kind, bedrock_bitmap_ranges[range_index].reg_prefix) && index <= max_index) {
            *bit = (unsigned)bedrock_bitmap_ranges[range_index].low_bit + index;
            return 1;
        }
    }
    return 0;
}

static int bedrock_parse_bitmap16(const char *bitmap_kind, const char *text, uint64_t *value)
{
    char compact[128];
    char token[32];
    char *cursor;
    int braced = 0;
    int closed = 0;
    uint64_t bitmap = 0;
    if (bedrock_parse_u64(text, value)) {
        return *value <= 0xffffu;
    }
    bedrock_compact_copy(compact, sizeof(compact), text);
    cursor = compact;
    if (*cursor == '{') {
        braced = 1;
        ++cursor;
    }
    while (*cursor != '\0') {
        char *start = cursor;
        char *dash;
        char lo_kind, hi_kind;
        unsigned lo_index, hi_index, reg;
        if (*cursor == '}') {
            closed = 1;
            ++cursor;
            break;
        }
        while (*cursor != '\0' && *cursor != ',' && *cursor != '}') {
            ++cursor;
        }
        bedrock_trim_copy(token, sizeof(token), start, cursor);
        if (token[0] == '\0') {
            return 0;
        }
        dash = strchr(token, '-');
        if (dash != 0) {
            *dash = '\0';
            if (!bedrock_parse_bitmap_register(bitmap_kind, token, &lo_kind, &lo_index)
                || !bedrock_parse_bitmap_register(bitmap_kind, dash + 1, &hi_kind, &hi_index)
                || lo_kind != hi_kind || lo_index > hi_index) {
                return 0;
            }
            for (reg = lo_index; reg <= hi_index; ++reg) {
                unsigned bit;
                if (!bedrock_bitmap_bit_for_register(bitmap_kind, lo_kind, reg, &bit)) {
                    return 0;
                }
                bitmap |= 1ull << bit;
            }
        } else {
            unsigned bit;
            if (!bedrock_parse_bitmap_register(bitmap_kind, token, &lo_kind, &lo_index)) {
                return 0;
            }
            if (!bedrock_bitmap_bit_for_register(bitmap_kind, lo_kind, lo_index, &bit)) {
                return 0;
            }
            bitmap |= 1ull << bit;
        }
        if (*cursor == ',') {
            ++cursor;
        }
    }
    if ((braced && !closed) || (!braced && closed) || *cursor != '\0') {
        return 0;
    }
    *value = bitmap;
    return 1;
}

static unsigned bedrock_immediate_kind_bits(const char *kind)
{
    if (bedrock_contains_ci(kind, "imm64")) {
        return 64u;
    }
    if (bedrock_contains_ci(kind, "imm32")) {
        return 32u;
    }
    return 16u;
}

static const bedrock_field_desc *bedrock_operand_field(const bedrock_operand_desc *desc)
{
    if (desc->field_index == BEDROCK_NO_FIELD || desc->field_index >= bedrock_fields_count) {
        return 0;
    }
    return &bedrock_fields[desc->field_index];
}

static int bedrock_field_is_compact_immediate_selector(const bedrock_field_desc *field)
{
    if (field == 0 || !bedrock_contains_ci(field->kind, "imm")) {
        return 0;
    }
    if (!bedrock_contains_ci(field->kind, "imm16")
        && !bedrock_contains_ci(field->kind, "imm32")
        && !bedrock_contains_ci(field->kind, "imm64")) {
        return 0;
    }
    return field->width > 0u && field->width < bedrock_immediate_kind_bits(field->kind);
}

static int bedrock_parse_operand_for_kind(const bedrock_operand_desc *desc, const char *text, char size_suffix, bedrock_text_operand *out)
{
    uint16_t named;
    const bedrock_field_desc *field = bedrock_operand_field(desc);
    memset(out, 0, sizeof(*out));
    bedrock_trim_copy(out->text, sizeof(out->text), text, text + strlen(text));
    if (strcmp(desc->kind, "DREG") == 0) {
        return bedrock_parse_numbered_register(out->text, 'D', 7, &out->value);
    }
    if (strcmp(desc->kind, "DBANK") == 0) {
        return bedrock_parse_dbank_selector(out->text, &out->value);
    }
    if (strcmp(desc->kind, "AREG") == 0) {
        return bedrock_parse_numbered_register(out->text, 'A', 7, &out->value);
    }
    if (strcmp(desc->kind, "SPREG") == 0) {
        out->value = 0;
        return bedrock_streq_ci(out->text, "SP");
    }
    if (strcmp(desc->kind, "FREG") == 0) {
        return bedrock_parse_numbered_register(out->text, 'F', 31, &out->value);
    }
    if (strcmp(desc->kind, "SREG") == 0) {
        if (!bedrock_lookup_named(bedrock_sreg_names, bedrock_sreg_names_count, out->text, &named)) {
            return 0;
        }
        out->value = named;
        return 1;
    }
    if (strcmp(desc->kind, "CR") == 0 || strcmp(desc->kind, "cr") == 0) {
        if (!bedrock_lookup_named(bedrock_cr_names, bedrock_cr_names_count, out->text, &named)) {
            return 0;
        }
        out->value = named;
        return 1;
    }
    if (strcmp(desc->kind, "condition") == 0) {
        if (!bedrock_lookup_named(bedrock_condition_names, bedrock_condition_names_count, out->text, &named)) {
            return 0;
        }
        out->value = named;
        return 1;
    }
    if (strcmp(desc->kind, "memory_order") == 0) {
        if (!bedrock_lookup_named(bedrock_memory_order_names, bedrock_memory_order_names_count, out->text, &named)) {
            return 0;
        }
        out->value = named;
        return 1;
    }
    if (bedrock_field_is_compact_immediate_selector(field)) {
        int ok = bedrock_parse_compact_ea(out->text, out, size_suffix);
        if (!ok) {
            return 0;
        }
        if (out->value == BEDROCK_EA_IMM16 || out->value == BEDROCK_EA_IMM32 || out->value == BEDROCK_EA_IMM64) {
            out->cost -= 4;
            return 1;
        }
        return 0;
    }
    if (strcmp(desc->kind, "EA") == 0) {
        int ok = bedrock_parse_compact_ea(out->text, out, size_suffix);
        if (ok && strcmp(desc->role, "dst") == 0 && ((out->value >= BEDROCK_EA_DREG && out->value < BEDROCK_EA_INDIRECT) || out->value == BEDROCK_EA_SPREG)) {
            out->cost += 3;
        }
        return ok;
    }
    if (bedrock_is_bitmap_kind(desc->kind) || bedrock_is_bitmap_kind(desc->declared_kind)) {
        const char *bitmap_kind = bedrock_is_bitmap_kind(desc->kind) ? desc->kind : desc->declared_kind;
        if (!bedrock_parse_bitmap16(bitmap_kind, out->text, &out->value)) {
            return 0;
        }
        out->payload_count = 1;
        out->payload[0] = (uint16_t)out->value;
        return 1;
    }
    if (strcmp(desc->kind, "small_selector") == 0) {
        if (bedrock_parse_numbered_register(out->text, 'D', 7, &out->value)) {
            return 1;
        }
        return bedrock_parse_u64(out->text, &out->value);
    }
    if (strcmp(desc->kind, "selector6") == 0 || strcmp(desc->declared_kind, "selector6") == 0) {
        if (!bedrock_parse_u64(out->text, &out->value) || out->value > 63u) {
            return 0;
        }
        return 1;
    }
    if (strcmp(desc->kind, "IMM6") == 0 || strcmp(desc->declared_kind, "imm6") == 0) {
        if (!bedrock_parse_u64(out->text, &out->value) || out->value > 63u) {
            return 0;
        }
        return 1;
    }
    if (bedrock_contains_ci(desc->kind, "imm") || bedrock_contains_ci(desc->declared_kind, "imm")) {
        size_t words = bedrock_words_for_size_suffix(size_suffix);
        size_t forced_words = 0;
        if (bedrock_contains_ci(desc->kind, "imm16") || bedrock_contains_ci(desc->declared_kind, "imm16")) {
            words = 1;
        } else if (bedrock_contains_ci(desc->kind, "imm32") || bedrock_contains_ci(desc->declared_kind, "imm32")) {
            words = 2;
        } else if (bedrock_contains_ci(desc->kind, "imm64") || bedrock_contains_ci(desc->declared_kind, "imm64")) {
            words = 4;
        }
        if (!bedrock_parse_immediate_payload_text(out->text, &out->value, &forced_words)) {
            return 0;
        }
        if (forced_words != 0u) {
            int fixed_width = bedrock_contains_ci(desc->kind, "imm16")
                || bedrock_contains_ci(desc->declared_kind, "imm16")
                || bedrock_contains_ci(desc->kind, "imm32")
                || bedrock_contains_ci(desc->declared_kind, "imm32")
                || bedrock_contains_ci(desc->kind, "imm64")
                || bedrock_contains_ci(desc->declared_kind, "imm64");
            if (fixed_width && forced_words != words) {
                return 0;
            }
            words = forced_words;
        }
        if (words == 1u && !bedrock_value_fits_signed_or_unsigned_bits(out->value, 16u)) {
            return 0;
        }
        if (words == 2u && !bedrock_value_fits_signed_or_unsigned_bits(out->value, 32u)) {
            return 0;
        }
        out->payload_count = words;
        bedrock_payload_from_u64(out->value, out->payload, words);
        return 1;
    }
    return bedrock_parse_u64(out->text, &out->value);
}

static size_t bedrock_payload_start_word(const bedrock_form_desc *form)
{
    size_t index;
    size_t start = bedrock_form_is_extended(form) ? 2u : 1u;
    for (index = 0; index < form->field_count; ++index) {
        const bedrock_field_desc *field = &bedrock_fields[form->field_index + index];
        if ((size_t)field->token + 1u > start) {
            start = (size_t)field->token + 1u;
        }
    }
    return start;
}

static int bedrock_parse_rep_prefix_line(const char *line, uint16_t *prefix_word, const char **inner_line)
{
    const char *cursor = line;
    const char *mnemonic_start;
    const char *mnemonic_end;
    char mnemonic[32];
    char condition_name[32];
    uint16_t condition = 0;
    uint64_t counter = 0;
    while (isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    mnemonic_start = cursor;
    while (*cursor != '\0' && !isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    mnemonic_end = cursor;
    if ((size_t)(mnemonic_end - mnemonic_start) >= sizeof(mnemonic)) {
        return 0;
    }
    bedrock_trim_copy(mnemonic, sizeof(mnemonic), mnemonic_start, mnemonic_end);
    if (bedrock_streq_ci(mnemonic, "REPG") || !bedrock_starts_ci(mnemonic, "REP", 3u)) {
        return 0;
    }
    if (mnemonic[3] == '\0') {
        condition = 0;
    } else {
        bedrock_trim_copy(condition_name, sizeof(condition_name), mnemonic + 3, mnemonic + strlen(mnemonic));
        if (!bedrock_lookup_named(bedrock_condition_names, bedrock_condition_names_count, condition_name, &condition)) {
            return 0;
        }
    }
    while (isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    if (!bedrock_parse_numbered_register(cursor, 'D', 7, &counter)) {
        const char *reg_start = cursor;
        const char *reg_end;
        char reg_text[8];
        while (*cursor != '\0' && *cursor != ',' && !isspace((unsigned char)*cursor)) {
            ++cursor;
        }
        reg_end = cursor;
        bedrock_trim_copy(reg_text, sizeof(reg_text), reg_start, reg_end);
        if (!bedrock_parse_numbered_register(reg_text, 'D', 7, &counter)) {
            return 0;
        }
    } else {
        while (*cursor != '\0' && *cursor != ',' && !isspace((unsigned char)*cursor)) {
            ++cursor;
        }
    }
    while (isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    if (*cursor != ',') {
        return 0;
    }
    ++cursor;
    while (isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    if (*cursor == '\0') {
        return 0;
    }
    *prefix_word = (uint16_t)(0x80u | ((condition & 0x0fu) << 3) | (uint16_t)(counter & 0x07u));
    *inner_line = cursor;
    return 1;
}

static int bedrock_apply_prefix_word(uint16_t prefix_word, uint16_t *out_words, size_t out_word_count, size_t *written_words)
{
    size_t index;
    size_t inner_words;
    size_t total_words;
    if (written_words == 0 || *written_words == 0u) {
        return BEDROCK_ERR_INVALID_ARGUMENT;
    }
    inner_words = *written_words;
    if ((out_words[0] & BEDROCK_WORD0_PREFIX_BIT) != 0u) {
        uint16_t low = (uint16_t)(prefix_word & 0x00ffu);
        uint16_t high = (uint16_t)((prefix_word >> 8) & 0x00ffu);
        if (low != 0u && !bedrock_merge_prefix_byte(&out_words[1], low)) {
            return BEDROCK_ERR_INVALID_ARGUMENT;
        }
        if (high != 0u && !bedrock_merge_prefix_byte(&out_words[1], high)) {
            return BEDROCK_ERR_INVALID_ARGUMENT;
        }
        return BEDROCK_OK;
    }
    total_words = inner_words + 1u;
    if (total_words > out_word_count || total_words > BEDROCK_MAX_INSTRUCTION_WORDS) {
        return BEDROCK_ERR_BUFFER_TOO_SMALL;
    }
    for (index = inner_words; index > 1u; --index) {
        out_words[index] = out_words[index - 1u];
    }
    out_words[1] = prefix_word;
    out_words[0] = (uint16_t)(
        (out_words[0] & (uint16_t)~BEDROCK_WORD0_LENGTH_MASK)
        | BEDROCK_WORD0_PREFIX_BIT
        | (uint16_t)((total_words - 1u) << 12)
    );
    *written_words = total_words;
    return BEDROCK_OK;
}

static int bedrock_validate_form_operands(const bedrock_form_desc *form, const bedrock_text_operand *operands)
{
    if (form == 0 || operands == 0) {
        return 0;
    }
    if (bedrock_streq_ci(form->mnemonic, "REPG")) {
        uint64_t body_bytes;
        if (form->operand_count != 2u) {
            return 0;
        }
        body_bytes = operands[1].value;
        if (body_bytes == 0u || (body_bytes & 1u) != 0u) {
            return 0;
        }
    }
    return 1;
}

int bedrock_assemble_line(const char *line, uint16_t *out_words, size_t out_word_count, size_t *written_words, const bedrock_form_desc **matched_form)
{
    bedrock_text_line parsed;
    size_t form_index;
    int best_score = 0x3fffffff;
    const bedrock_form_desc *best_form = 0;
    uint64_t best_fields[BEDROCK_TEXT_MAX_FIELDS];
    bedrock_text_operand best_operands[BEDROCK_TEXT_MAX_OPERANDS];
    uint16_t prefix_word = 0;
    uint16_t operand_prefix_word = 0;
    const char *inner_line = 0;
    if (line != 0 && out_words != 0 && bedrock_parse_rep_prefix_line(line, &prefix_word, &inner_line)) {
        int status = bedrock_assemble_line(inner_line, out_words, out_word_count, written_words, matched_form);
        if (status != BEDROCK_OK) {
            return status;
        }
        return bedrock_apply_prefix_word(prefix_word, out_words, out_word_count, written_words);
    }
    if (line == 0 || out_words == 0 || !bedrock_parse_line_text(line, &parsed)) {
        return BEDROCK_ERR_INVALID_ARGUMENT;
    }
    if (!bedrock_normalize_update_operands(&parsed, &operand_prefix_word)) {
        return BEDROCK_ERR_INVALID_ARGUMENT;
    }
    for (form_index = 0; form_index < bedrock_forms_count; ++form_index) {
        const bedrock_form_desc *form = &bedrock_forms[form_index];
        bedrock_text_line local = parsed;
        bedrock_text_operand parsed_operands[BEDROCK_TEXT_MAX_OPERANDS];
        uint64_t field_values[BEDROCK_TEXT_MAX_FIELDS];
        int score = 0;
        size_t operand_index;
        size_t field_index;
        int ok = 1;
        int form_has_memory_order = 0;
        if (form->field_count > BEDROCK_TEXT_MAX_FIELDS || form->operand_count > BEDROCK_TEXT_MAX_OPERANDS) {
            continue;
        }
        if (!bedrock_form_mnemonic_matches(form, &local) || local.operand_count != form->operand_count) {
            continue;
        }
        for (operand_index = 0; operand_index < form->operand_count; ++operand_index) {
            const bedrock_operand_desc *desc = &bedrock_operands[form->operand_index + operand_index];
            if (!bedrock_parse_operand_for_kind(desc, local.operands[operand_index], local.size_suffix, &parsed_operands[operand_index])) {
                ok = 0;
                break;
            }
            score += parsed_operands[operand_index].cost;
            score += (int)parsed_operands[operand_index].payload_count;
        }
        if (!ok) {
            continue;
        }
        for (field_index = 0; field_index < form->field_count; ++field_index) {
            const bedrock_field_desc *field = &bedrock_fields[form->field_index + field_index];
            int found = 0;
            if (bedrock_field_is_size_kind(field)) {
                if (!bedrock_size_value_for_kind(field->kind, local.size_suffix, &field_values[field_index])) {
                    ok = 0;
                    break;
                }
                found = 1;
            } else if (strcmp(field->source, "cc") == 0 || strcmp(field->kind, "condition") == 0) {
                if (!local.has_condition && form->alias_condition[0] != '\0') {
                    uint16_t alias_condition = 0;
                    if (bedrock_lookup_named(bedrock_condition_names, bedrock_condition_names_count, form->alias_condition, &alias_condition)) {
                        local.condition = alias_condition;
                        local.has_condition = 1;
                    }
                }
                field_values[field_index] = local.has_condition ? local.condition : 0;
                found = 1;
            } else if (strcmp(field->kind, "memory_order") == 0) {
                form_has_memory_order = 1;
                if (!local.has_memory_order) {
                    ok = 0;
                    break;
                }
                field_values[field_index] = local.memory_order;
                found = 1;
            } else {
                for (operand_index = 0; operand_index < form->operand_count; ++operand_index) {
                    const bedrock_operand_desc *desc = &bedrock_operands[form->operand_index + operand_index];
                    if (desc->field_index == form->field_index + field_index) {
                        field_values[field_index] = parsed_operands[operand_index].value;
                        found = 1;
                        break;
                    }
                }
            }
            if (!found) {
                ok = 0;
                break;
            }
        }
        if (local.has_memory_order && !form_has_memory_order) {
            ok = 0;
        }
        if (!ok) {
            continue;
        }
        score += (int)form->required_words;
        if (bedrock_form_is_extended(form)) {
            score += 4;
        }
        if (score < best_score) {
            best_score = score;
            best_form = form;
            memcpy(best_fields, field_values, sizeof(uint64_t) * form->field_count);
            memcpy(best_operands, parsed_operands, sizeof(bedrock_text_operand) * form->operand_count);
        }
    }
    if (best_form == 0) {
        return BEDROCK_ERR_NO_MATCH;
    }
    if (!bedrock_validate_form_operands(best_form, best_operands)) {
        return BEDROCK_ERR_NO_MATCH;
    }
    {
        size_t emitted = 0;
        size_t payload_cursor;
        size_t operand_index;
        int status = bedrock_encode_form_words(best_form, best_fields, best_form->field_count, out_words, out_word_count, &emitted);
        if (status != BEDROCK_OK) {
            return status;
        }
        payload_cursor = bedrock_payload_start_word(best_form);
        for (operand_index = 0; operand_index < best_form->operand_count; ++operand_index) {
            const bedrock_operand_desc *desc = &bedrock_operands[best_form->operand_index + operand_index];
            size_t payload_index;
            if (desc->field_index != BEDROCK_NO_FIELD && best_operands[operand_index].payload_count == 0u) {
                continue;
            }
            for (payload_index = 0; payload_index < best_operands[operand_index].payload_count; ++payload_index) {
                if (payload_cursor >= out_word_count || payload_cursor >= BEDROCK_MAX_INSTRUCTION_WORDS) {
                    return BEDROCK_ERR_BUFFER_TOO_SMALL;
                }
                out_words[payload_cursor++] = best_operands[operand_index].payload[payload_index];
            }
        }
        if (payload_cursor > emitted) {
            emitted = payload_cursor;
            out_words[0] = (uint16_t)((out_words[0] & (uint16_t)~BEDROCK_WORD0_LENGTH_MASK) | (uint16_t)((emitted - 1u) << 12));
        }
        if (operand_prefix_word != 0u) {
            status = bedrock_apply_prefix_word(operand_prefix_word, out_words, out_word_count, &emitted);
            if (status != BEDROCK_OK) {
                return status;
            }
        }
        if (written_words != 0) {
            *written_words = emitted;
        }
        if (matched_form != 0) {
            *matched_form = best_form;
        }
    }
    return BEDROCK_OK;
}

static const bedrock_field_desc *bedrock_find_field_by_symbol(const bedrock_form_desc *form, const char *symbol, unsigned occurrence)
{
    size_t index;
    unsigned seen = 0;
    for (index = 0; index < form->field_count; ++index) {
        const bedrock_field_desc *field = &bedrock_fields[form->field_index + index];
        if (strcmp(field->symbol, symbol) == 0) {
            if (seen == occurrence) {
                return field;
            }
            ++seen;
        }
    }
    return 0;
}

static const bedrock_field_desc *bedrock_first_field_by_source_or_kind(const bedrock_form_desc *form, const char *source, const char *kind)
{
    size_t index;
    for (index = 0; index < form->field_count; ++index) {
        const bedrock_field_desc *field = &bedrock_fields[form->field_index + index];
        if ((source != 0 && strcmp(field->source, source) == 0) || (kind != 0 && strcmp(field->kind, kind) == 0)) {
            return field;
        }
    }
    return 0;
}

static int bedrock_append_text(char *out, size_t out_size, size_t *used, const char *text)
{
    size_t len = strlen(text);
    if (*used + len + 1u > out_size) {
        return 0;
    }
    memcpy(out + *used, text, len);
    *used += len;
    out[*used] = '\0';
    return 1;
}

static int bedrock_append_format(char *out, size_t out_size, size_t *used, const char *fmt, unsigned value)
{
    char buf[64];
    int written = snprintf(buf, sizeof(buf), fmt, value);
    if (written < 0 || (size_t)written >= sizeof(buf)) {
        return 0;
    }
    return bedrock_append_text(out, out_size, used, buf);
}

static int bedrock_append_hex64(char *out, size_t out_size, size_t *used, uint64_t value)
{
    char buf[32];
    int written = snprintf(buf, sizeof(buf), "0x%llx", (unsigned long long)value);
    if (written < 0 || (size_t)written >= sizeof(buf)) {
        return 0;
    }
    return bedrock_append_text(out, out_size, used, buf);
}

static int bedrock_append_selector6(char *out, size_t out_size, size_t *used, uint64_t value)
{
    return bedrock_append_format(out, out_size, used, "%u", (unsigned)(value & 0x3fu));
}

static int bedrock_append_bitmap_item(char *out, size_t out_size, size_t *used, int *first, char kind, unsigned start, unsigned end)
{
    char buf[32];
    int written;
    if (!*first && !bedrock_append_text(out, out_size, used, ",")) {
        return 0;
    }
    *first = 0;
    if (start == end) {
        written = snprintf(buf, sizeof(buf), "%c%u", kind, start);
    } else {
        written = snprintf(buf, sizeof(buf), "%c%u-%c%u", kind, start, kind, end);
    }
    if (written < 0 || (size_t)written >= sizeof(buf)) {
        return 0;
    }
    return bedrock_append_text(out, out_size, used, buf);
}

static int bedrock_append_bitmap16(const char *bitmap_kind, char *out, size_t out_size, size_t *used, uint64_t value)
{
    int first = 1;
    if (!bedrock_append_text(out, out_size, used, "{")) {
        return 0;
    }
    for (size_t range_index = 0; range_index < bedrock_bitmap_ranges_count; ++range_index) {
        char kind;
        unsigned base;
        unsigned max_index;
        unsigned index = 0;
        if (strcmp(bitmap_kind, bedrock_bitmap_ranges[range_index].kind) != 0) {
            continue;
        }
        kind = bedrock_bitmap_ranges[range_index].reg_prefix;
        base = bedrock_bitmap_ranges[range_index].low_bit;
        max_index = (unsigned)(bedrock_bitmap_ranges[range_index].high_bit - bedrock_bitmap_ranges[range_index].low_bit);
        while (index <= max_index) {
            unsigned start;
            if ((value & (1ull << (base + index))) == 0u) {
                ++index;
                continue;
            }
            start = index;
            while (index + 1u <= max_index && (value & (1ull << (base + index + 1u))) != 0u) {
                ++index;
            }
            if (!bedrock_append_bitmap_item(out, out_size, used, &first, kind, start, index)) {
                return 0;
            }
            ++index;
        }
    }
    return bedrock_append_text(out, out_size, used, "}");
}

static const char *bedrock_form_bitmap_kind(const bedrock_form_desc *form)
{
    size_t index;
    for (index = 0; index < form->operand_count; ++index) {
        const bedrock_operand_desc *operand = &bedrock_operands[form->operand_index + index];
        if (bedrock_is_bitmap_kind(operand->kind)) {
            return operand->kind;
        }
        if (bedrock_is_bitmap_kind(operand->declared_kind)) {
            return operand->declared_kind;
        }
    }
    return "bitmap16";
}

static uint64_t bedrock_read_payload_words(const uint16_t *words, size_t start, size_t count)
{
    uint64_t value = 0;
    size_t index;
    for (index = 0; index < count && index < 4u; ++index) {
        value |= ((uint64_t)words[start + index]) << (index * 16u);
    }
    return value;
}

static int bedrock_format_ea_value(uint64_t value, char *out, size_t out_size)
{
    if (value >= BEDROCK_EA_DREG && value < BEDROCK_EA_AREG) {
        return snprintf(out, out_size, "D%u", (unsigned)(value - BEDROCK_EA_DREG)) > 0;
    }
    if (value >= BEDROCK_EA_AREG && value < BEDROCK_EA_INDIRECT) {
        return snprintf(out, out_size, "A%u", (unsigned)(value - BEDROCK_EA_AREG)) > 0;
    }
    if (value >= BEDROCK_EA_INDIRECT && value < BEDROCK_EA_A_DISP16) {
        return snprintf(out, out_size, "[A%u]", (unsigned)(value - BEDROCK_EA_INDIRECT)) > 0;
    }
    if (value >= BEDROCK_EA_A_DISP16 && value < BEDROCK_EA_A_DISP32) {
        return snprintf(out, out_size, "[A%u + disp16]", (unsigned)(value - BEDROCK_EA_A_DISP16)) > 0;
    }
    if (value >= BEDROCK_EA_A_DISP32 && value < BEDROCK_EA_PC_DISP16) {
        return snprintf(out, out_size, "[A%u + disp32]", (unsigned)(value - BEDROCK_EA_A_DISP32)) > 0;
    }
    if (value == BEDROCK_EA_PC_DISP16) { return snprintf(out, out_size, "[PC + disp16]") > 0; }
    if (value == BEDROCK_EA_PC_DISP32) { return snprintf(out, out_size, "[PC + disp32]") > 0; }
    if (value == BEDROCK_EA_PC_DISP64) { return snprintf(out, out_size, "[PC + disp64]") > 0; }
    if (value == BEDROCK_EA_SP_DISP16) { return snprintf(out, out_size, "[SP + disp16]") > 0; }
    if (value == BEDROCK_EA_SP_DISP32) { return snprintf(out, out_size, "[SP + disp32]") > 0; }
    if (value == BEDROCK_EA_SP_DISP64) { return snprintf(out, out_size, "[SP + disp64]") > 0; }
    if (value == BEDROCK_EA_SPREG) { return snprintf(out, out_size, "SP") > 0; }
    if (value == BEDROCK_EA_ABS32) { return snprintf(out, out_size, "[abs32]") > 0; }
    if (value == BEDROCK_EA_ABS64) { return snprintf(out, out_size, "[abs64]") > 0; }
    if (value == BEDROCK_EA_IMM16) { return snprintf(out, out_size, "imm16") > 0; }
    if (value == BEDROCK_EA_IMM32) { return snprintf(out, out_size, "imm32") > 0; }
    if (value == BEDROCK_EA_IMM64) { return snprintf(out, out_size, "imm64") > 0; }
    if (value == BEDROCK_EA_S32_INDEXED_EXTENDED) { return snprintf(out, out_size, "<long-indexed-ea>") > 0; }
    if (value == BEDROCK_EA_EXTENDED) { return snprintf(out, out_size, "<extended-ea>") > 0; }
    return snprintf(out, out_size, "<ea:0x%02x>", (unsigned)value) > 0;
}

int bedrock_disassemble_line(const uint16_t *words, size_t word_count, char *out_text, size_t out_text_size, const bedrock_form_desc **matched_form)
{
    const bedrock_form_desc *form;
    const char *cursor;
    size_t used = 0;
    size_t payload_cursor;
    unsigned declared_words;
    unsigned symbol_occurrence[256];
    if (out_text == 0 || out_text_size == 0u) {
        return BEDROCK_ERR_INVALID_ARGUMENT;
    }
    out_text[0] = '\0';
    form = bedrock_decode_form(words, word_count);
    if (form == 0) {
        return BEDROCK_ERR_NO_MATCH;
    }
    memset(symbol_occurrence, 0, sizeof(symbol_occurrence));
    declared_words = bedrock_declared_words(words[0]);
    payload_cursor = bedrock_payload_start_word(form);
    cursor = form->syntax;
    while (*cursor != '\0') {
        if (strncmp(cursor, "<bitmap>", 8) == 0) {
            if (payload_cursor >= declared_words) {
                return BEDROCK_ERR_UNDERSIZED_ENCODING;
            }
            if (!bedrock_append_bitmap16(bedrock_form_bitmap_kind(form), out_text, out_text_size, &used, words[payload_cursor++])) {
                return BEDROCK_ERR_BUFFER_TOO_SMALL;
            }
            cursor += 8;
            continue;
        }
        if (strncmp(cursor, "imm64", 5) == 0 || strncmp(cursor, "imm32", 5) == 0 || strncmp(cursor, "imm16", 5) == 0 || strncmp(cursor, "imm", 3) == 0) {
            size_t payload_words = 1;
            size_t token_len = 3;
            if (strncmp(cursor, "imm64", 5) == 0) {
                payload_words = 4;
                token_len = 5;
            } else if (strncmp(cursor, "imm32", 5) == 0) {
                payload_words = 2;
                token_len = 5;
            } else if (strncmp(cursor, "imm16", 5) == 0) {
                payload_words = 1;
                token_len = 5;
            } else if (declared_words > payload_cursor) {
                payload_words = declared_words - payload_cursor;
                if (payload_words > 4u) {
                    payload_words = 4u;
                }
            }
            if (payload_cursor + payload_words > declared_words) {
                return BEDROCK_ERR_UNDERSIZED_ENCODING;
            }
            if (!bedrock_append_hex64(out_text, out_text_size, &used, bedrock_read_payload_words(words, payload_cursor, payload_words))) {
                return BEDROCK_ERR_BUFFER_TOO_SMALL;
            }
            payload_cursor += payload_words;
            cursor += token_len;
            continue;
        }
        if (strncmp(cursor, ".X(", 3) == 0) {
            const bedrock_field_desc *field = bedrock_first_field_by_source_or_kind(form, "size", 0);
            if (field != 0) {
                char suffix[3];
                suffix[0] = '.';
                suffix[1] = bedrock_size_suffix_for_kind(field->kind, bedrock_extract_field(words, field));
                suffix[2] = '\0';
                if (!bedrock_append_text(out_text, out_text_size, &used, suffix)) {
                    return BEDROCK_ERR_BUFFER_TOO_SMALL;
                }
                cursor = strchr(cursor, ')');
                if (cursor == 0) {
                    return BEDROCK_ERR_INVALID_ARGUMENT;
                }
                ++cursor;
                continue;
            }
        }
        if (strncmp(cursor, "{condition}", 11) == 0) {
            const bedrock_field_desc *field = bedrock_first_field_by_source_or_kind(form, "cc", "condition");
            uint16_t condition = 0;
            if (field != 0) {
                condition = (uint16_t)bedrock_extract_field(words, field);
            } else if (form->alias_condition[0] != '\0') {
                (void)bedrock_lookup_named(bedrock_condition_names, bedrock_condition_names_count, form->alias_condition, &condition);
            }
            if (!bedrock_append_text(out_text, out_text_size, &used, bedrock_name_for_value(bedrock_condition_names, bedrock_condition_names_count, condition))) {
                return BEDROCK_ERR_BUFFER_TOO_SMALL;
            }
            cursor += 11;
            continue;
        }
        if ((strncmp(cursor, "Dn(", 3) == 0 || strncmp(cursor, "DBn(", 4) == 0 || strncmp(cursor, "An(", 3) == 0 || strncmp(cursor, "Fn(", 3) == 0 || strncmp(cursor, "Sreg(", 5) == 0 || strncmp(cursor, "ORDER(", 6) == 0 || strncmp(cursor, "order(", 6) == 0 || strncmp(cursor, "<ea(", 4) == 0 || strncmp(cursor, "<imm(", 5) == 0 || strncmp(cursor, "<cr(", 4) == 0 || strncmp(cursor, "<count(", 7) == 0 || strncmp(cursor, "<bit_index(", 11) == 0)) {
            const char *open = strchr(cursor, '(');
            const char *close = open != 0 ? strchr(open, ')') : 0;
            char symbol[16];
            const bedrock_field_desc *field;
            uint64_t value;
            unsigned char key;
            if (open == 0 || close == 0 || (size_t)(close - open - 1) >= sizeof(symbol)) {
                return BEDROCK_ERR_INVALID_ARGUMENT;
            }
            bedrock_trim_copy(symbol, sizeof(symbol), open + 1, close);
            key = (unsigned char)symbol[0];
            field = bedrock_find_field_by_symbol(form, symbol, symbol_occurrence[key]++);
            if (field == 0) {
                return BEDROCK_ERR_INVALID_ARGUMENT;
            }
            value = bedrock_extract_field(words, field);
            if (strncmp(cursor, "Dn(", 3) == 0) {
                if (!bedrock_append_format(out_text, out_text_size, &used, "D%u", (unsigned)value)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strncmp(cursor, "DBn(", 4) == 0) {
                if (!bedrock_append_format(out_text, out_text_size, &used, "DB%u", (unsigned)value)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strncmp(cursor, "An(", 3) == 0) {
                if (!bedrock_append_format(out_text, out_text_size, &used, "A%u", (unsigned)value)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strncmp(cursor, "Fn(", 3) == 0) {
                if (!bedrock_append_format(out_text, out_text_size, &used, "F%u", (unsigned)value)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strncmp(cursor, "Sreg(", 5) == 0) {
                if (!bedrock_append_text(out_text, out_text_size, &used, bedrock_name_for_value(bedrock_sreg_names, bedrock_sreg_names_count, (uint16_t)value))) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strncmp(cursor, "<cr(", 4) == 0) {
                if (!bedrock_append_text(out_text, out_text_size, &used, bedrock_name_for_value(bedrock_cr_names, bedrock_cr_names_count, (uint16_t)value))) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strncmp(cursor, "ORDER(", 6) == 0 || strncmp(cursor, "order(", 6) == 0) {
                if (!bedrock_append_text(out_text, out_text_size, &used, bedrock_name_for_value(bedrock_memory_order_names, bedrock_memory_order_names_count, (uint16_t)value))) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strcmp(field->kind, "selector6") == 0) {
                if (!bedrock_append_selector6(out_text, out_text_size, &used, value)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strcmp(field->kind, "IMM6") == 0) {
                if (!bedrock_append_selector6(out_text, out_text_size, &used, value)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strcmp(field->kind, "small_selector") == 0) {
                if (!bedrock_append_format(out_text, out_text_size, &used, "%u", (unsigned)value)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else {
                char ea_text[64];
                if (!bedrock_format_ea_value(value, ea_text, sizeof(ea_text)) || !bedrock_append_text(out_text, out_text_size, &used, ea_text)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            }
            cursor = close + 1;
            if (*cursor == '>') {
                ++cursor;
            }
            continue;
        }
        {
            char one[2];
            one[0] = *cursor++;
            one[1] = '\0';
            if (!bedrock_append_text(out_text, out_text_size, &used, one)) {
                return BEDROCK_ERR_BUFFER_TOO_SMALL;
            }
        }
    }
    if (matched_form != 0) {
        *matched_form = form;
    }
    return BEDROCK_OK;
}
