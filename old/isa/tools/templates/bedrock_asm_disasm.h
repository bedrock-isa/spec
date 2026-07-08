/* Generated from build/generated/allocation_plan.json. */
#ifndef BEDROCK_ASM_DISASM_H
#define BEDROCK_ASM_DISASM_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define BEDROCK_MAX_INSTRUCTION_WORDS 8u
#define BEDROCK_WORD0_PREFIX_BIT 0x8000u
#define BEDROCK_WORD0_LENGTH_MASK 0x7000u
#define BEDROCK_WORD0_PAYLOAD_MASK 0x0fffu
#define BEDROCK_NO_FIELD 0xffffu

typedef enum bedrock_form_kind {
    BEDROCK_FORM_COMPACT = 0,
    BEDROCK_FORM_COMPACT_ALIAS = 1,
    BEDROCK_FORM_EXTENDED = 2,
    BEDROCK_FORM_EXTENDED_ALIAS = 3
} bedrock_form_kind;

typedef enum bedrock_status {
    BEDROCK_OK = 0,
    BEDROCK_ERR_INVALID_ARGUMENT = -1,
    BEDROCK_ERR_BUFFER_TOO_SMALL = -2,
    BEDROCK_ERR_FIELD_VALUE_TOO_LARGE = -3,
    BEDROCK_ERR_UNDERSIZED_ENCODING = -4,
    BEDROCK_ERR_NO_MATCH = -5
} bedrock_status;

typedef struct bedrock_field_desc {
    const char *name;
    const char *kind;
    const char *source;
    const char *symbol;
    uint8_t token;
    uint8_t low_bit;
    uint8_t width;
} bedrock_field_desc;

typedef struct bedrock_named_value {
    const char *name;
    uint16_t value;
} bedrock_named_value;

typedef struct bedrock_operand_desc {
    const char *role;
    const char *declared_kind;
    const char *kind;
    uint16_t field_index;
} bedrock_operand_desc;

typedef struct bedrock_form_desc {
    const char *id;
    const char *mnemonic;
    const char *syntax;
    bedrock_form_kind kind;
    const char *category;
    const char *group;
    const char *privilege;
    uint16_t primary_start;
    uint16_t primary_end;
    uint16_t ext_start;
    uint16_t ext_end;
    uint8_t min_words;
    uint8_t max_words;
    uint8_t required_words;
    uint16_t field_index;
    uint16_t field_count;
    uint16_t operand_index;
    uint16_t operand_count;
    uint16_t primary_value_index;
    uint16_t primary_value_count;
    const char *alias_of;
    const char *alias_condition;
} bedrock_form_desc;

extern const bedrock_form_desc bedrock_forms[];
extern const bedrock_field_desc bedrock_fields[];
extern const bedrock_operand_desc bedrock_operands[];
extern const uint16_t bedrock_primary_values[];
extern const bedrock_named_value bedrock_condition_names[];
extern const bedrock_named_value bedrock_sreg_names[];
extern const bedrock_named_value bedrock_cr_names[];
extern const bedrock_named_value bedrock_memory_order_names[];
extern const size_t bedrock_forms_count;
extern const size_t bedrock_fields_count;
extern const size_t bedrock_operands_count;
extern const size_t bedrock_primary_values_count;
extern const size_t bedrock_condition_names_count;
extern const size_t bedrock_sreg_names_count;
extern const size_t bedrock_cr_names_count;
extern const size_t bedrock_memory_order_names_count;

size_t bedrock_form_count(void);
const bedrock_form_desc *bedrock_form_at(size_t index);
const bedrock_field_desc *bedrock_form_field(const bedrock_form_desc *form, size_t index);
const bedrock_operand_desc *bedrock_form_operand(const bedrock_form_desc *form, size_t index);
const bedrock_form_desc *bedrock_find_form_by_id(const char *id);
const bedrock_form_desc *bedrock_find_first_mnemonic(const char *mnemonic);
const bedrock_form_desc *bedrock_find_form_by_signature(const char *mnemonic, const char *const *operand_kinds, size_t operand_count);
const bedrock_form_desc *bedrock_decode_form(const uint16_t *words, size_t word_count);
int bedrock_assemble_line(const char *line, uint16_t *out_words, size_t out_word_count, size_t *written_words, const bedrock_form_desc **matched_form);
int bedrock_disassemble_line(const uint16_t *words, size_t word_count, char *out_text, size_t out_text_size, const bedrock_form_desc **matched_form);

uint64_t bedrock_extract_field(const uint16_t *words, const bedrock_field_desc *field);
int bedrock_insert_field(uint16_t *words, size_t word_count, const bedrock_field_desc *field, uint64_t value);
int bedrock_encode_form_words(const bedrock_form_desc *form, const uint64_t *field_values, size_t field_value_count, uint16_t *out_words, size_t out_word_count, size_t *written_words);

#ifdef __cplusplus
}
#endif

#endif
