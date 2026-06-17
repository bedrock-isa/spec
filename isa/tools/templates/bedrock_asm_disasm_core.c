static uint16_t bedrock_word0_payload(uint16_t word0)
{
    return (uint16_t)(word0 & BEDROCK_WORD0_PAYLOAD_MASK);
}

static unsigned bedrock_declared_words(uint16_t word0)
{
    return (unsigned)(((word0 & BEDROCK_WORD0_LENGTH_MASK) >> 12) + 1u);
}

static int bedrock_primary_matches(const bedrock_form_desc *form, uint16_t payload)
{
    if (form->primary_value_count != 0u) {
        size_t index;
        for (index = 0; index < form->primary_value_count; ++index) {
            if (bedrock_primary_values[form->primary_value_index + index] == payload) {
                return 1;
            }
        }
        return 0;
    }
    return payload >= form->primary_start && payload <= form->primary_end;
}

static int bedrock_form_is_extended(const bedrock_form_desc *form)
{
    return form->kind == BEDROCK_FORM_EXTENDED || form->kind == BEDROCK_FORM_EXTENDED_ALIAS;
}

size_t bedrock_form_count(void)
{
    return bedrock_forms_count;
}

const bedrock_form_desc *bedrock_form_at(size_t index)
{
    return index < bedrock_forms_count ? &bedrock_forms[index] : 0;
}

const bedrock_field_desc *bedrock_form_field(const bedrock_form_desc *form, size_t index)
{
    if (form == 0 || index >= form->field_count) {
        return 0;
    }
    return &bedrock_fields[form->field_index + index];
}

const bedrock_operand_desc *bedrock_form_operand(const bedrock_form_desc *form, size_t index)
{
    if (form == 0 || index >= form->operand_count) {
        return 0;
    }
    return &bedrock_operands[form->operand_index + index];
}

const bedrock_form_desc *bedrock_find_form_by_id(const char *id)
{
    size_t index;
    if (id == 0) {
        return 0;
    }
    for (index = 0; index < bedrock_forms_count; ++index) {
        if (strcmp(bedrock_forms[index].id, id) == 0) {
            return &bedrock_forms[index];
        }
    }
    return 0;
}

const bedrock_form_desc *bedrock_find_first_mnemonic(const char *mnemonic)
{
    size_t index;
    if (mnemonic == 0) {
        return 0;
    }
    for (index = 0; index < bedrock_forms_count; ++index) {
        if (strcmp(bedrock_forms[index].mnemonic, mnemonic) == 0) {
            return &bedrock_forms[index];
        }
    }
    return 0;
}

const bedrock_form_desc *bedrock_find_form_by_signature(const char *mnemonic, const char *const *operand_kinds, size_t operand_count)
{
    size_t index;
    if (mnemonic == 0 || (operand_count != 0u && operand_kinds == 0)) {
        return 0;
    }
    for (index = 0; index < bedrock_forms_count; ++index) {
        const bedrock_form_desc *form = &bedrock_forms[index];
        size_t operand_index;
        int matches = 1;
        if (strcmp(form->mnemonic, mnemonic) != 0 || form->operand_count != operand_count) {
            continue;
        }
        for (operand_index = 0; operand_index < operand_count; ++operand_index) {
            const bedrock_operand_desc *operand = &bedrock_operands[form->operand_index + operand_index];
            if (operand_kinds[operand_index] == 0 || strcmp(operand->kind, operand_kinds[operand_index]) != 0) {
                matches = 0;
                break;
            }
        }
        if (matches) {
            return form;
        }
    }
    return 0;
}

const bedrock_form_desc *bedrock_decode_form(const uint16_t *words, size_t word_count)
{
    uint16_t payload;
    unsigned declared_words;
    size_t index;
    if (words == 0 || word_count == 0u) {
        return 0;
    }
    declared_words = bedrock_declared_words(words[0]);
    if (word_count < declared_words) {
        return 0;
    }
    payload = bedrock_word0_payload(words[0]);
    for (index = 0; index < bedrock_forms_count; ++index) {
        const bedrock_form_desc *form = &bedrock_forms[index];
        if (declared_words < form->required_words || declared_words > form->max_words) {
            continue;
        }
        if (!bedrock_primary_matches(form, payload)) {
            continue;
        }
        if (bedrock_form_is_extended(form)) {
            if (declared_words < 2u || words[1] < form->ext_start || words[1] > form->ext_end) {
                continue;
            }
        }
        {
            size_t field_index;
            int fields_valid = 1;
            for (field_index = 0; field_index < form->field_count; ++field_index) {
                const bedrock_field_desc *field = &bedrock_fields[form->field_index + field_index];
                if (strcmp(field->kind, "memory_order") == 0) {
                    uint16_t value = (uint16_t)bedrock_extract_field(words, field);
                    size_t named_index;
                    int valid_order = 0;
                    for (named_index = 0; named_index < bedrock_memory_order_names_count; ++named_index) {
                        if (bedrock_memory_order_names[named_index].name != 0 && bedrock_memory_order_names[named_index].value == value) {
                            valid_order = 1;
                            break;
                        }
                    }
                    if (!valid_order) {
                        fields_valid = 0;
                        break;
                    }
                }
            }
            if (!fields_valid) {
                continue;
            }
        }
        return form;
    }
    return 0;
}

uint64_t bedrock_extract_field(const uint16_t *words, const bedrock_field_desc *field)
{
    uint64_t mask;
    uint16_t word;
    if (words == 0 || field == 0 || field->width == 0u) {
        return 0;
    }
    word = words[field->token];
    mask = field->width >= 16u ? 0xffffu : ((1ull << field->width) - 1ull);
    return ((uint64_t)word >> field->low_bit) & mask;
}

int bedrock_insert_field(uint16_t *words, size_t word_count, const bedrock_field_desc *field, uint64_t value)
{
    uint64_t mask;
    uint16_t shifted_mask;
    if (words == 0 || field == 0 || field->width == 0u) {
        return BEDROCK_ERR_INVALID_ARGUMENT;
    }
    if ((size_t)field->token >= word_count) {
        return BEDROCK_ERR_BUFFER_TOO_SMALL;
    }
    mask = field->width >= 16u ? 0xffffu : ((1ull << field->width) - 1ull);
    if ((value & ~mask) != 0ull) {
        return BEDROCK_ERR_FIELD_VALUE_TOO_LARGE;
    }
    shifted_mask = (uint16_t)(mask << field->low_bit);
    words[field->token] = (uint16_t)((words[field->token] & (uint16_t)~shifted_mask) | (uint16_t)((value & mask) << field->low_bit));
    return BEDROCK_OK;
}

int bedrock_encode_form_words(const bedrock_form_desc *form, const uint64_t *field_values, size_t field_value_count, uint16_t *out_words, size_t out_word_count, size_t *written_words)
{
    size_t index;
    size_t required;
    if (form == 0 || out_words == 0) {
        return BEDROCK_ERR_INVALID_ARGUMENT;
    }
    required = form->required_words;
    if (required == 0u || required > BEDROCK_MAX_INSTRUCTION_WORDS) {
        return BEDROCK_ERR_INVALID_ARGUMENT;
    }
    if (out_word_count < required) {
        return BEDROCK_ERR_BUFFER_TOO_SMALL;
    }
    if (form->field_count != 0u && field_values == 0) {
        return BEDROCK_ERR_INVALID_ARGUMENT;
    }
    if (field_value_count < form->field_count) {
        return BEDROCK_ERR_INVALID_ARGUMENT;
    }
    for (index = 0; index < required; ++index) {
        out_words[index] = 0;
    }
    out_words[0] = (uint16_t)((((uint16_t)(required - 1u)) << 12) | (form->primary_start & BEDROCK_WORD0_PAYLOAD_MASK));
    if (bedrock_form_is_extended(form)) {
        out_words[1] = form->ext_start;
    }
    for (index = 0; index < form->field_count; ++index) {
        int status = bedrock_insert_field(out_words, required, &bedrock_fields[form->field_index + index], field_values[index]);
        if (status != BEDROCK_OK) {
            return status;
        }
    }
    if (!bedrock_primary_matches(form, bedrock_word0_payload(out_words[0]))) {
        return BEDROCK_ERR_INVALID_ARGUMENT;
    }
    if (written_words != 0) {
        *written_words = required;
    }
    return BEDROCK_OK;
}
