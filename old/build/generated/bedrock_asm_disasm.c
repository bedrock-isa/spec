/* Generated from build/generated/allocation_plan.json. */
#include "bedrock_asm_disasm.h"

#include <ctype.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct bedrock_size_code_desc { char code; char suffix; uint8_t bytes; } bedrock_size_code_desc;
typedef struct bedrock_size_kind_value_desc { const char *kind; uint16_t value; char code; } bedrock_size_kind_value_desc;
typedef struct bedrock_bitmap_range_desc { const char *kind; uint8_t low_bit; uint8_t high_bit; char reg_prefix; } bedrock_bitmap_range_desc;

#define BEDROCK_PREFIX_POSTINC 0x04u
#define BEDROCK_PREFIX_PREINC 0x05u
#define BEDROCK_PREFIX_POSTDEC 0x06u
#define BEDROCK_PREFIX_PREDEC 0x07u
#define BEDROCK_EA_ABS32 0x30u
#define BEDROCK_EA_ABS64 0x31u
#define BEDROCK_EA_AREG 0x08u
#define BEDROCK_EA_A_DISP16 0x18u
#define BEDROCK_EA_A_DISP32 0x20u
#define BEDROCK_EA_DREG 0x00u
#define BEDROCK_EA_EXTENDED 0x3fu
#define BEDROCK_EA_IMM16 0x32u
#define BEDROCK_EA_IMM32 0x33u
#define BEDROCK_EA_IMM64 0x34u
#define BEDROCK_EA_INDIRECT 0x10u
#define BEDROCK_EA_PC_DISP16 0x28u
#define BEDROCK_EA_PC_DISP32 0x29u
#define BEDROCK_EA_PC_DISP64 0x2au
#define BEDROCK_EA_S32_INDEXED_EXTENDED 0x3eu
#define BEDROCK_EA_SPREG 0x2fu
#define BEDROCK_EA_SP_DISP16 0x2cu
#define BEDROCK_EA_SP_DISP32 0x2du
#define BEDROCK_EA_SP_DISP64 0x2eu

const bedrock_size_code_desc bedrock_size_codes[] = {
    {'B', 'B', 1u},
    {'W', 'W', 2u},
    {'L', 'L', 4u},
    {'Q', 'Q', 8u},
    {'S', 'S', 4u},
    {'D', 'D', 8u},
};

const bedrock_size_kind_value_desc bedrock_size_kind_values[] = {
    {"BW", 0u, 'B'},
    {"BW", 1u, 'W'},
    {"BWL", 0u, 'B'},
    {"BWL", 1u, 'W'},
    {"BWL", 2u, 'L'},
    {"BWLQ", 0u, 'B'},
    {"BWLQ", 1u, 'W'},
    {"BWLQ", 2u, 'L'},
    {"BWLQ", 3u, 'Q'},
    {"BWLX", 0u, 'B'},
    {"BWLX", 1u, 'W'},
    {"BWLX", 2u, 'L'},
    {"LQ", 0u, 'L'},
    {"LQ", 1u, 'Q'},
    {"S_D", 0u, 'S'},
    {"S_D", 1u, 'D'},
    {"WL", 0u, 'W'},
    {"WL", 1u, 'L'},
};

const bedrock_bitmap_range_desc bedrock_bitmap_ranges[] = {
    {"bitmap16", 0u, 7u, 'D'},
    {"bitmap16", 8u, 15u, 'A'},
    {"fbitmap16", 0u, 15u, 'F'},
};

const bedrock_field_desc bedrock_fields[] = {
    {"d", "DREG", "reg", "d", 0u, 0u, 3u},
    {"d", "DREG", "dst", "d", 0u, 0u, 3u},
    {"z", "WL", "size", "z", 0u, 3u, 1u},
    {"d", "DREG", "dst", "d", 0u, 0u, 3u},
    {"s", "BWLQ", "size", "s", 0u, 3u, 2u},
    {"d", "DREG", "src", "d", 0u, 0u, 3u},
    {"D", "DREG", "dst", "D", 0u, 3u, 3u},
    {"d", "DREG", "src", "d", 0u, 0u, 3u},
    {"D", "DREG", "dst", "D", 0u, 3u, 3u},
    {"z", "LQ", "size", "z", 0u, 6u, 1u},
    {"d", "DREG", "src", "d", 0u, 0u, 3u},
    {"D", "DREG", "dst", "D", 0u, 3u, 3u},
    {"s", "BWL", "size", "s", 0u, 6u, 2u},
    {"d", "DREG", "dst", "d", 0u, 0u, 3u},
    {"s", "BWLQ", "size", "s", 0u, 3u, 2u},
    {"d", "DREG", "dst", "d", 0u, 0u, 3u},
    {"s", "BWLQ", "size", "s", 0u, 3u, 2u},
    {"d", "DREG", "src", "d", 0u, 0u, 3u},
    {"D", "DREG", "dst", "D", 0u, 3u, 3u},
    {"s", "BWL", "size", "s", 0u, 6u, 2u},
    {"d", "DREG", "dst", "d", 0u, 0u, 3u},
    {"s", "BWLQ", "size", "s", 0u, 3u, 2u},
    {"d", "DREG", "dst", "d", 0u, 0u, 3u},
    {"s", "BWLQ", "size", "s", 0u, 3u, 2u},
    {"d", "DREG", "src", "d", 0u, 0u, 3u},
    {"D", "DREG", "dst", "D", 0u, 3u, 3u},
    {"z", "LQ", "size", "z", 0u, 6u, 1u},
    {"d", "DREG", "src", "d", 0u, 0u, 3u},
    {"D", "DREG", "dst", "D", 0u, 3u, 3u},
    {"z", "LQ", "size", "z", 0u, 6u, 1u},
    {"d", "DREG", "dst", "d", 0u, 6u, 3u},
    {"z", "WL", "size", "z", 0u, 9u, 1u},
    {"d", "DREG", "rhs", "r", 0u, 6u, 3u},
    {"z", "WL", "size", "z", 0u, 9u, 1u},
    {"d", "DREG", "dst", "d", 0u, 6u, 3u},
    {"z", "WL", "size", "z", 0u, 9u, 1u},
    {"d", "DREG", "rhs", "r", 0u, 6u, 3u},
    {"z", "WL", "size", "z", 0u, 9u, 1u},
    {"e", "EA", "dst", "e", 0u, 0u, 6u},
    {"d", "DREG", "src", "d", 0u, 6u, 3u},
    {"z", "LQ", "size", "z", 0u, 9u, 1u},
    {"e", "EA", "src", "e", 0u, 0u, 6u},
    {"d", "DREG", "dst", "d", 0u, 6u, 3u},
    {"z", "LQ", "size", "z", 0u, 9u, 1u},
    {"d", "DREG", "src", "d", 0u, 0u, 3u},
    {"D", "DREG", "dst", "D", 0u, 3u, 3u},
    {"z", "LQ", "size", "z", 0u, 6u, 1u},
    {"d", "DREG", "src", "d", 0u, 0u, 3u},
    {"D", "DREG", "dst", "D", 0u, 3u, 3u},
    {"z", "LQ", "size", "z", 0u, 6u, 1u},
    {"d", "DREG", "src", "d", 0u, 0u, 3u},
    {"D", "DREG", "dst", "D", 0u, 3u, 3u},
    {"z", "LQ", "size", "z", 0u, 6u, 1u},
    {"d", "DREG", "src", "d", 0u, 0u, 3u},
    {"D", "DREG", "dst", "D", 0u, 3u, 3u},
    {"z", "LQ", "size", "z", 0u, 6u, 1u},
    {"d", "DREG", "src", "d", 0u, 0u, 3u},
    {"D", "DREG", "dst", "D", 0u, 3u, 3u},
    {"s", "BW", "size", "s", 0u, 6u, 1u},
    {"d", "DREG", "dst", "d", 0u, 0u, 3u},
    {"s", "BWLQ", "size", "s", 0u, 3u, 2u},
    {"d", "DREG", "dst", "d", 0u, 0u, 3u},
    {"s", "BWLQ", "size", "s", 0u, 3u, 2u},
    {"z", "WL", "size", "z", 0u, 4u, 1u},
    {"c", "condition", "cc", "c", 0u, 0u, 4u},
    {"z", "WL", "size", "z", 0u, 4u, 1u},
    {"d", "DREG", "dst", "d", 0u, 0u, 3u},
    {"z", "WL", "size", "z", 0u, 3u, 1u},
    {"d", "DREG", "dst", "d", 0u, 0u, 3u},
    {"z", "WL", "size", "z", 0u, 3u, 1u},
    {"a", "AREG", "reg", "a", 0u, 0u, 3u},
    {"d", "DREG", "reg", "d", 0u, 0u, 3u},
    {"a", "AREG", "reg", "a", 0u, 0u, 3u},
    {"a", "AREG", "dst", "a", 0u, 0u, 3u},
    {"d", "DREG", "dst", "d", 0u, 0u, 3u},
    {"a", "AREG", "dst", "a", 0u, 0u, 3u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"a", "AREG", "dst", "a", 1u, 0u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 3u, 2u},
    {"b", "bitmap16", "regs", "b", 2u, 0u, 16u},
    {"d", "DREG", "dst", "d", 1u, 0u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 3u, 2u},
    {"b", "bitmap16", "regs", "b", 2u, 0u, 16u},
    {"d", "DREG", "src", "d", 1u, 0u, 3u},
    {"D", "DREG", "dst", "D", 1u, 3u, 3u},
    {"s", "BW", "size", "s", 1u, 6u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"a", "AREG", "dst", "a", 1u, 6u, 3u},
    {"e", "EA", "lhs", "e", 1u, 0u, 6u},
    {"a", "AREG", "rhs", "r", 1u, 6u, 3u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "rhs", "e", 1u, 0u, 6u},
    {"d", "DREG", "lhs", "l", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "lhs", "e", 1u, 0u, 6u},
    {"d", "DREG", "rhs", "r", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BW", "size", "s", 1u, 9u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BW", "size", "s", 1u, 9u, 1u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWL", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWL", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BW", "size", "s", 1u, 9u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BW", "size", "s", 1u, 9u, 1u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWL", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWL", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"d", "DREG", "src", "d", 1u, 0u, 3u},
    {"D", "DREG", "dst", "D", 1u, 3u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"a", "AREG", "dst", "a", 1u, 6u, 3u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "rhs", "e", 1u, 0u, 6u},
    {"d", "DREG", "lhs", "l", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "lhs", "e", 1u, 0u, 6u},
    {"d", "DREG", "rhs", "r", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"i", "IMM6", "imm", "i", 1u, 8u, 6u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"i", "IMM6", "imm", "i", 1u, 8u, 6u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"i", "IMM6", "imm", "i", 1u, 8u, 6u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"i", "IMM6", "imm", "i", 1u, 8u, 6u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"i", "IMM6", "imm", "i", 1u, 8u, 6u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"i", "IMM6", "imm", "i", 1u, 8u, 6u},
    {"e", "EA", "rhs", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"i", "IMM6", "imm", "i", 1u, 8u, 6u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"i", "IMM6", "imm", "i", 1u, 8u, 6u},
    {"e", "EA", "lhs", "e", 1u, 0u, 6u},
    {"E", "EA", "rhs", "E", 1u, 6u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "rhs", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"i", "IMM6", "imm", "i", 1u, 8u, 6u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"E", "EA", "dst", "E", 1u, 6u, 6u},
    {"s", "BW", "size", "s", 1u, 12u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"E", "EA", "dst", "E", 1u, 6u, 6u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"E", "EA", "dst", "E", 1u, 6u, 6u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"E", "EA", "dst", "E", 1u, 6u, 6u},
    {"s", "BWL", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"E", "EA", "dst", "E", 1u, 6u, 6u},
    {"s", "BW", "size", "s", 1u, 12u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"E", "EA", "dst", "E", 1u, 6u, 6u},
    {"s", "BWL", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "value", "e", 1u, 0u, 6u},
    {"d", "DREG", "lo", "l", 1u, 6u, 3u},
    {"D", "DREG", "hi", "h", 1u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "value", "e", 1u, 0u, 6u},
    {"d", "DREG", "lo", "l", 1u, 6u, 3u},
    {"D", "DREG", "hi", "h", 1u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "value", "e", 1u, 0u, 6u},
    {"d", "DREG", "lo", "l", 1u, 6u, 3u},
    {"D", "DREG", "hi", "h", 1u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "value", "e", 1u, 0u, 6u},
    {"d", "DREG", "lo", "l", 1u, 6u, 3u},
    {"D", "DREG", "hi", "h", 1u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "value", "e", 1u, 0u, 6u},
    {"d", "DREG", "lo", "l", 1u, 6u, 3u},
    {"D", "DREG", "hi", "h", 1u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "value", "e", 1u, 0u, 6u},
    {"d", "DREG", "lo", "l", 1u, 6u, 3u},
    {"D", "DREG", "hi", "h", 1u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "value", "e", 1u, 0u, 6u},
    {"d", "DREG", "lo", "l", 1u, 6u, 3u},
    {"D", "DREG", "hi", "h", 1u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "value", "e", 1u, 0u, 6u},
    {"d", "DREG", "lo", "l", 1u, 6u, 3u},
    {"D", "DREG", "hi", "h", 1u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 2u, 0u, 6u},
    {"d", "DREG", "quotient", "q", 2u, 6u, 3u},
    {"D", "DREG", "remainder", "r", 2u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 2u, 12u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "quotient", "q", 1u, 6u, 3u},
    {"D", "DREG", "remainder", "r", 1u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "multiplier", "d", 1u, 6u, 3u},
    {"D", "DREG", "acc", "D", 1u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "multiplier", "d", 1u, 6u, 3u},
    {"D", "DREG", "acc", "D", 1u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"n", "DREG", "bit_index", "b", 1u, 0u, 3u},
    {"d", "DREG", "bit_index", "b", 1u, 3u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"n", "DREG", "bit_index", "b", 1u, 0u, 3u},
    {"d", "DREG", "bit_index", "b", 1u, 3u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"n", "DREG", "bit_index", "b", 1u, 0u, 3u},
    {"d", "DREG", "bit_index", "b", 1u, 3u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"n", "DREG", "bit_index", "b", 1u, 0u, 3u},
    {"d", "DREG", "bit_index", "b", 1u, 3u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"n", "DREG", "count", "n", 1u, 0u, 3u},
    {"d", "DREG", "count", "d", 1u, 3u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"n", "DREG", "count", "n", 1u, 0u, 3u},
    {"d", "DREG", "count", "d", 1u, 3u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"d", "DREG", "src", "d", 1u, 0u, 3u},
    {"D", "DREG", "dst", "D", 1u, 3u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "DREG", "bit_index", "b", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "DREG", "bit_index", "b", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "DREG", "bit_index", "b", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "DREG", "bit_index", "b", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "DREG", "count", "n", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "DREG", "count", "n", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"n", "DREG", "count", "n", 1u, 0u, 3u},
    {"d", "DREG", "count", "d", 1u, 3u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"n", "DREG", "count", "n", 1u, 0u, 3u},
    {"d", "DREG", "count", "d", 1u, 3u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"n", "DREG", "count", "n", 1u, 0u, 3u},
    {"d", "DREG", "count", "d", 1u, 3u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"n", "DREG", "count", "n", 1u, 0u, 3u},
    {"d", "DREG", "count", "d", 1u, 3u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"n", "DREG", "count", "n", 1u, 0u, 3u},
    {"d", "DREG", "count", "d", 1u, 3u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "DREG", "count", "n", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "DREG", "count", "n", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "DREG", "count", "n", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "DREG", "count", "n", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "DREG", "count", "n", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "selector6", "bit_index", "b", 1u, 6u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "selector6", "bit_index", "b", 1u, 6u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "selector6", "bit_index", "b", 1u, 6u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "selector6", "bit_index", "b", 1u, 6u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "selector6", "count", "n", 1u, 6u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "selector6", "count", "n", 1u, 6u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "selector6", "count", "n", 1u, 6u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "selector6", "count", "n", 1u, 6u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "selector6", "count", "n", 1u, 6u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "selector6", "count", "n", 1u, 6u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"n", "selector6", "count", "n", 1u, 6u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "rhs", "e", 1u, 0u, 6u},
    {"d", "DREG", "lhs", "l", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "lhs", "e", 1u, 0u, 6u},
    {"d", "DREG", "rhs", "r", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"E", "EA", "dst", "E", 1u, 6u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 12u, 2u},
    {"d", "DREG", "dst", "d", 1u, 0u, 3u},
    {"d", "DREG", "selector", "d", 1u, 0u, 3u},
    {"k", "DBANK", "src_bank", "k", 1u, 0u, 4u},
    {"b", "bitmap16", "regs", "b", 2u, 0u, 16u},
    {"k", "DBANK", "dst_bank", "k", 1u, 0u, 4u},
    {"b", "bitmap16", "regs", "b", 2u, 0u, 16u},
    {"k", "DBANK", "selector", "k", 1u, 0u, 4u},
    {"k", "DBANK", "bank", "k", 1u, 0u, 4u},
    {"b", "bitmap16", "regs", "b", 2u, 0u, 16u},
    {"k", "DBANK", "bank", "k", 1u, 0u, 4u},
    {"b", "bitmap16", "regs", "b", 2u, 0u, 16u},
    {"k", "DBANK", "dst_bank", "k", 1u, 0u, 4u},
    {"K", "DBANK", "src_bank", "K", 1u, 4u, 4u},
    {"b", "bitmap16", "regs", "b", 2u, 0u, 16u},
    {"k", "DBANK", "bank_a", "k", 1u, 0u, 4u},
    {"K", "DBANK", "bank_b", "K", 1u, 4u, 4u},
    {"b", "bitmap16", "regs", "b", 2u, 0u, 16u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"a", "AREG", "dst", "a", 1u, 6u, 3u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"a", "AREG", "dst", "a", 1u, 6u, 3u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"e", "EA", "target", "e", 1u, 0u, 6u},
    {"e", "EA", "target", "e", 1u, 0u, 6u},
    {"d", "DREG", "new_cs", "d", 1u, 6u, 3u},
    {"e", "EA", "target", "e", 1u, 0u, 6u},
    {"d", "DREG", "new_cs", "d", 1u, 6u, 3u},
    {"c", "condition", "cc", "c", 0u, 0u, 4u},
    {"e", "EA", "target", "e", 1u, 0u, 6u},
    {"d", "DREG", "counter", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"c", "condition", "cc", "c", 0u, 0u, 4u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"c", "condition", "cc", "c", 0u, 0u, 4u},
    {"z", "WL", "size", "z", 1u, 0u, 1u},
    {"e", "EA", "target", "e", 1u, 1u, 6u},
    {"c", "condition", "cc", "c", 0u, 0u, 4u},
    {"e", "EA", "target", "e", 1u, 0u, 6u},
    {"z", "WL", "size", "z", 1u, 6u, 1u},
    {"c", "condition", "cc", "c", 0u, 0u, 4u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"s", "BWLQ", "size", "s", 1u, 6u, 2u},
    {"c", "condition", "cc", "c", 0u, 0u, 4u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"a", "AREG", "src", "a", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"c", "condition", "cc", "c", 0u, 0u, 4u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"d", "DREG", "src", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"c", "condition", "cc", "c", 0u, 0u, 4u},
    {"e", "EA", "target", "e", 1u, 0u, 6u},
    {"d", "DREG", "index", "d", 1u, 6u, 3u},
    {"D", "DREG", "bound", "D", 1u, 9u, 3u},
    {"z", "LQ", "size", "z", 1u, 12u, 1u},
    {"c", "condition", "cc", "c", 0u, 0u, 4u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"a", "AREG", "dst", "a", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"c", "condition", "cc", "c", 0u, 0u, 4u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 6u, 3u},
    {"s", "BWLQ", "size", "s", 1u, 9u, 2u},
    {"c", "condition", "cc", "c", 0u, 0u, 4u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"c", "condition", "cc", "c", 0u, 0u, 4u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"f", "FREG", "src", "f", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"s", "BWLQ", "size", "s", 1u, 0u, 2u},
    {"o", "memory_order", "order", "o", 2u, 0u, 3u},
    {"e", "EA", "memory", "e", 2u, 3u, 6u},
    {"d", "DREG", "expected", "x", 2u, 9u, 3u},
    {"D", "DREG", "desired", "y", 2u, 12u, 3u},
    {"o", "memory_order", "order", "o", 2u, 0u, 3u},
    {"e", "EA", "memory", "e", 2u, 3u, 6u},
    {"d", "DREG", "src", "d", 2u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 2u, 12u, 2u},
    {"o", "memory_order", "order", "o", 2u, 0u, 3u},
    {"e", "EA", "memory", "e", 2u, 3u, 6u},
    {"d", "DREG", "src", "d", 2u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 2u, 12u, 2u},
    {"o", "memory_order", "order", "o", 2u, 0u, 3u},
    {"e", "EA", "memory", "e", 2u, 3u, 6u},
    {"d", "DREG", "src", "d", 2u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 2u, 12u, 2u},
    {"o", "memory_order", "order", "o", 2u, 0u, 3u},
    {"e", "EA", "memory", "e", 2u, 3u, 6u},
    {"d", "DREG", "src", "d", 2u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 2u, 12u, 2u},
    {"o", "memory_order", "order", "o", 2u, 0u, 3u},
    {"e", "EA", "memory", "e", 2u, 3u, 6u},
    {"d", "DREG", "src", "d", 2u, 9u, 3u},
    {"s", "BWLQ", "size", "s", 2u, 12u, 2u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"i", "IMM16", "asid", "i", 2u, 0u, 16u},
    {"d", "DREG", "new_ptcr", "d", 1u, 0u, 3u},
    {"d", "DREG", "dst", "d", 1u, 0u, 3u},
    {"e", "EA", "page", "e", 1u, 0u, 6u},
    {"d", "DREG", "new_ptcr", "d", 1u, 0u, 3u},
    {"D", "DREG", "asid", "D", 1u, 3u, 3u},
    {"e", "EA", "target", "e", 1u, 0u, 6u},
    {"e", "EA", "target", "e", 1u, 0u, 6u},
    {"e", "EA", "target", "e", 1u, 0u, 6u},
    {"e", "EA", "target", "e", 1u, 0u, 6u},
    {"e", "EA", "target", "e", 1u, 0u, 6u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 0u, 3u},
    {"i", "CR", "cr", "i", 2u, 0u, 16u},
    {"d", "DREG", "src", "d", 1u, 0u, 3u},
    {"i", "CR", "cr", "i", 2u, 0u, 16u},
    {"d", "DREG", "dst", "d", 1u, 0u, 3u},
    {"d", "DREG", "src", "d", 1u, 0u, 3u},
    {"d", "DREG", "dst", "d", 1u, 0u, 3u},
    {"d", "DREG", "src", "d", 1u, 0u, 3u},
    {"d", "DREG", "reg", "d", 1u, 0u, 3u},
    {"d", "DREG", "dst", "d", 1u, 0u, 3u},
    {"g", "SREG", "seg", "g", 1u, 0u, 3u},
    {"d", "DREG", "dst", "d", 1u, 3u, 3u},
    {"d", "DREG", "src", "d", 1u, 0u, 3u},
    {"g", "SREG", "seg", "g", 1u, 3u, 3u},
    {"e", "EA", "memory", "e", 1u, 0u, 6u},
    {"e", "EA", "memory", "e", 1u, 0u, 6u},
    {"d", "DREG", "dst", "d", 1u, 0u, 3u},
    {"i", "IMM16", "counter_id", "i", 2u, 0u, 16u},
    {"d", "DREG", "src", "d", 1u, 0u, 3u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"z", "S_D", "size", "z", 1u, 4u, 1u},
    {"f", "FREG", "dst", "d", 1u, 0u, 4u},
    {"i", "IMM16", "constant_id", "i", 2u, 0u, 16u},
    {"d", "DREG", "src", "d", 1u, 0u, 3u},
    {"f", "FREG", "dst", "d", 1u, 3u, 4u},
    {"d", "DREG", "dst", "d", 1u, 0u, 3u},
    {"f", "FREG", "src", "f", 1u, 3u, 4u},
    {"z", "S_D", "size", "z", 1u, 7u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"d", "DREG", "dst", "d", 1u, 0u, 3u},
    {"f", "FREG", "src", "f", 1u, 3u, 4u},
    {"d", "DREG", "src", "d", 1u, 0u, 3u},
    {"f", "FREG", "dst", "d", 1u, 3u, 4u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"z", "S_D", "size", "z", 1u, 6u, 1u},
    {"d", "DREG", "dst", "d", 1u, 0u, 3u},
    {"f", "FREG", "src", "f", 1u, 3u, 4u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"f", "FREG", "src", "f", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"f", "FREG", "src", "f", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"e", "EA", "value", "e", 2u, 0u, 6u},
    {"f", "FREG", "lo", "l", 2u, 6u, 4u},
    {"F", "FREG", "hi", "h", 2u, 10u, 4u},
    {"z", "S_D", "size", "z", 2u, 14u, 1u},
    {"f", "FREG", "lo", "l", 2u, 0u, 4u},
    {"F", "FREG", "value", "x", 2u, 4u, 4u},
    {"f3", "FREG", "hi", "h", 2u, 8u, 4u},
    {"z", "S_D", "size", "z", 2u, 12u, 1u},
    {"e", "EA", "value", "e", 2u, 0u, 6u},
    {"f", "FREG", "lo", "l", 2u, 6u, 4u},
    {"F", "FREG", "hi", "h", 2u, 10u, 4u},
    {"z", "S_D", "size", "z", 2u, 14u, 1u},
    {"f", "FREG", "lo", "l", 2u, 0u, 4u},
    {"F", "FREG", "value", "x", 2u, 4u, 4u},
    {"f3", "FREG", "hi", "h", 2u, 8u, 4u},
    {"z", "S_D", "size", "z", 2u, 12u, 1u},
    {"e", "EA", "value", "e", 2u, 0u, 6u},
    {"f", "FREG", "lo", "l", 2u, 6u, 4u},
    {"F", "FREG", "hi", "h", 2u, 10u, 4u},
    {"z", "S_D", "size", "z", 2u, 14u, 1u},
    {"f", "FREG", "lo", "l", 2u, 0u, 4u},
    {"F", "FREG", "value", "x", 2u, 4u, 4u},
    {"f3", "FREG", "hi", "h", 2u, 8u, 4u},
    {"z", "S_D", "size", "z", 2u, 12u, 1u},
    {"e", "EA", "value", "e", 2u, 0u, 6u},
    {"f", "FREG", "lo", "l", 2u, 6u, 4u},
    {"F", "FREG", "hi", "h", 2u, 10u, 4u},
    {"z", "S_D", "size", "z", 2u, 14u, 1u},
    {"f", "FREG", "lo", "l", 2u, 0u, 4u},
    {"F", "FREG", "value", "x", 2u, 4u, 4u},
    {"f3", "FREG", "hi", "h", 2u, 8u, 4u},
    {"z", "S_D", "size", "z", 2u, 12u, 1u},
    {"f", "FREG", "sign_src", "f", 2u, 0u, 4u},
    {"F", "FREG", "magnitude_src", "F", 2u, 4u, 4u},
    {"f3", "FREG", "dst", "d", 2u, 8u, 4u},
    {"z", "S_D", "size", "z", 2u, 12u, 1u},
    {"e", "EA", "lhs", "e", 2u, 0u, 6u},
    {"f", "FREG", "rhs", "r", 2u, 6u, 4u},
    {"F", "FREG", "dst", "d", 2u, 10u, 4u},
    {"z", "S_D", "size", "z", 2u, 14u, 1u},
    {"e", "EA", "rhs", "e", 2u, 0u, 6u},
    {"f", "FREG", "lhs", "l", 2u, 6u, 4u},
    {"F", "FREG", "dst", "d", 2u, 10u, 4u},
    {"z", "S_D", "size", "z", 2u, 14u, 1u},
    {"f", "FREG", "lhs", "l", 2u, 0u, 4u},
    {"F", "FREG", "rhs", "r", 2u, 4u, 4u},
    {"f3", "FREG", "dst", "d", 2u, 8u, 4u},
    {"z", "S_D", "size", "z", 2u, 12u, 1u},
    {"e", "EA", "lhs", "e", 2u, 0u, 6u},
    {"f", "FREG", "rhs", "r", 2u, 6u, 4u},
    {"F", "FREG", "dst", "d", 2u, 10u, 4u},
    {"z", "S_D", "size", "z", 2u, 14u, 1u},
    {"e", "EA", "rhs", "e", 2u, 0u, 6u},
    {"f", "FREG", "lhs", "l", 2u, 6u, 4u},
    {"F", "FREG", "dst", "d", 2u, 10u, 4u},
    {"z", "S_D", "size", "z", 2u, 14u, 1u},
    {"f", "FREG", "lhs", "l", 2u, 0u, 4u},
    {"F", "FREG", "rhs", "r", 2u, 4u, 4u},
    {"f3", "FREG", "dst", "d", 2u, 8u, 4u},
    {"z", "S_D", "size", "z", 2u, 12u, 1u},
    {"e", "EA", "lhs", "e", 2u, 0u, 6u},
    {"f", "FREG", "rhs", "r", 2u, 6u, 4u},
    {"F", "FREG", "dst", "d", 2u, 10u, 4u},
    {"z", "S_D", "size", "z", 2u, 14u, 1u},
    {"f", "FREG", "dst", "d", 1u, 0u, 4u},
    {"e", "EA", "rhs", "e", 2u, 0u, 6u},
    {"f", "FREG", "lhs", "l", 2u, 6u, 4u},
    {"F", "FREG", "dst", "d", 2u, 10u, 4u},
    {"z", "S_D", "size", "z", 2u, 14u, 1u},
    {"f", "FREG", "lhs", "l", 2u, 0u, 4u},
    {"F", "FREG", "rhs", "r", 2u, 4u, 4u},
    {"f3", "FREG", "dst", "d", 2u, 8u, 4u},
    {"z", "S_D", "size", "z", 2u, 12u, 1u},
    {"e", "EA", "lhs", "e", 2u, 0u, 6u},
    {"f", "FREG", "rhs", "r", 2u, 6u, 4u},
    {"F", "FREG", "dst", "d", 2u, 10u, 4u},
    {"z", "S_D", "size", "z", 2u, 14u, 1u},
    {"e", "EA", "rhs", "e", 2u, 0u, 6u},
    {"f", "FREG", "lhs", "l", 2u, 6u, 4u},
    {"F", "FREG", "dst", "d", 2u, 10u, 4u},
    {"z", "S_D", "size", "z", 2u, 14u, 1u},
    {"f", "FREG", "lhs", "l", 2u, 0u, 4u},
    {"F", "FREG", "rhs", "r", 2u, 4u, 4u},
    {"f3", "FREG", "dst", "d", 2u, 8u, 4u},
    {"z", "S_D", "size", "z", 2u, 12u, 1u},
    {"b", "fbitmap16", "regs", "b", 2u, 0u, 16u},
    {"b", "fbitmap16", "regs", "b", 2u, 0u, 16u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"f", "FREG", "lhs", "l", 1u, 0u, 4u},
    {"F", "FREG", "rhs", "r", 1u, 4u, 4u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"f", "FREG", "src", "f", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"f", "FREG", "src", "f", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"f", "FREG", "src", "f", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"f", "FREG", "src", "f", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"f", "FREG", "src", "f", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"f", "FREG", "src", "f", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"f", "FREG", "src", "f", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "src", "e", 1u, 0u, 6u},
    {"f", "FREG", "dst", "d", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"e", "EA", "dst", "e", 1u, 0u, 6u},
    {"f", "FREG", "src", "f", 1u, 6u, 4u},
    {"z", "S_D", "size", "z", 1u, 10u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"f", "FREG", "src", "f", 1u, 0u, 4u},
    {"F", "FREG", "dst", "d", 1u, 4u, 4u},
    {"z", "S_D", "size", "z", 1u, 8u, 1u},
    {"d", "DREG", "counter", "d", 0u, 0u, 3u},
};

const bedrock_operand_desc bedrock_operands[] = {
    {"target", "imm32", "imm32", 65535u},
    {"target", "imm64", "imm64", 65535u},
    {"target", "imm16", "imm16", 65535u},
    {"reg", "DREG", "DREG", 0u},
    {"imm", "imm", "imm", 65535u},
    {"dst", "DREG", "DREG", 1u},
    {"dst", "DREG", "DREG", 3u},
    {"src", "DREG", "DREG", 5u},
    {"dst", "DREG", "DREG", 6u},
    {"src", "DREG", "DREG", 7u},
    {"dst", "DREG", "DREG", 8u},
    {"src", "DREG", "DREG", 10u},
    {"dst", "DREG", "DREG", 11u},
    {"dst", "DREG", "DREG", 13u},
    {"dst", "DREG", "DREG", 15u},
    {"src", "DREG", "DREG", 17u},
    {"dst", "DREG", "DREG", 18u},
    {"dst", "DREG", "DREG", 20u},
    {"dst", "DREG", "DREG", 22u},
    {"src", "DREG", "DREG", 24u},
    {"dst", "DREG", "DREG", 25u},
    {"src", "DREG", "DREG", 27u},
    {"dst", "DREG", "DREG", 28u},
    {"imm", "imm", "imm", 65535u},
    {"dst", "DREG", "DREG", 30u},
    {"imm", "imm", "imm", 65535u},
    {"rhs", "DREG", "DREG", 32u},
    {"imm", "imm", "imm", 65535u},
    {"dst", "DREG", "DREG", 34u},
    {"imm", "imm", "imm", 65535u},
    {"rhs", "DREG", "DREG", 36u},
    {"src", "DREG", "DREG", 39u},
    {"dst", "EA", "EA", 38u},
    {"src", "EA", "EA", 41u},
    {"dst", "DREG", "DREG", 42u},
    {"src", "DREG", "DREG", 44u},
    {"dst", "DREG", "DREG", 45u},
    {"src", "DREG", "DREG", 47u},
    {"dst", "DREG", "DREG", 48u},
    {"src", "DREG", "DREG", 50u},
    {"dst", "DREG", "DREG", 51u},
    {"src", "DREG", "DREG", 53u},
    {"dst", "DREG", "DREG", 54u},
    {"src", "DREG", "DREG", 56u},
    {"dst", "DREG", "DREG", 57u},
    {"dst", "DREG", "DREG", 59u},
    {"dst", "DREG", "DREG", 61u},
    {"target", "relative_imm", "imm", 65535u},
    {"target", "relative_imm", "imm", 65535u},
    {"imm", "imm", "imm", 65535u},
    {"dst", "DREG", "DREG", 66u},
    {"imm", "imm", "imm", 65535u},
    {"dst", "DREG", "DREG", 68u},
    {"reg", "AREG", "AREG", 70u},
    {"reg", "DREG", "DREG", 71u},
    {"reg", "AREG", "AREG", 72u},
    {"dst", "AREG", "AREG", 73u},
    {"dst", "DREG", "DREG", 74u},
    {"src", "imm64", "imm64", 65535u},
    {"dst", "AREG", "AREG", 75u},
    {"regs", "bitmap16", "bitmap16", 65535u},
    {"regs", "bitmap16", "bitmap16", 65535u},
    {"regs", "bitmap16", "bitmap16", 65535u},
    {"regs", "bitmap16", "bitmap16", 65535u},
    {"regs", "bitmap16", "bitmap16", 65535u},
    {"regs", "bitmap16", "bitmap16", 65535u},
    {"marker", "imm16", "imm16", 65535u},
    {"dst", "EA", "EA", 76u},
    {"dst", "EA", "EA", 78u},
    {"regs", "bitmap16", "bitmap16", 81u},
    {"dst", "AREG", "AREG", 79u},
    {"regs", "bitmap16", "bitmap16", 84u},
    {"dst", "DREG", "DREG", 82u},
    {"src", "DREG", "DREG", 85u},
    {"dst", "DREG", "DREG", 86u},
    {"src", "EA", "EA", 88u},
    {"dst", "AREG", "AREG", 89u},
    {"lhs", "EA", "EA", 90u},
    {"rhs", "AREG", "AREG", 91u},
    {"dst", "EA", "EA", 92u},
    {"dst", "EA", "EA", 94u},
    {"src", "EA", "EA", 96u},
    {"dst", "DREG", "DREG", 97u},
    {"lhs", "DREG", "DREG", 100u},
    {"rhs", "EA", "EA", 99u},
    {"lhs", "EA", "EA", 102u},
    {"rhs", "DREG", "DREG", 103u},
    {"src", "DREG", "DREG", 106u},
    {"dst", "EA", "EA", 105u},
    {"src", "EA", "EA", 108u},
    {"dst", "DREG", "DREG", 109u},
    {"src", "DREG", "DREG", 112u},
    {"dst", "EA", "EA", 111u},
    {"src", "EA", "EA", 114u},
    {"dst", "DREG", "DREG", 115u},
    {"src", "DREG", "DREG", 118u},
    {"dst", "EA", "EA", 117u},
    {"src", "EA", "EA", 119u},
    {"dst", "DREG", "DREG", 120u},
    {"src", "DREG", "DREG", 122u},
    {"dst", "EA", "EA", 121u},
    {"src", "EA", "EA", 124u},
    {"dst", "DREG", "DREG", 125u},
    {"dst", "EA", "EA", 127u},
    {"dst", "EA", "EA", 129u},
    {"dst", "EA", "EA", 131u},
    {"dst", "EA", "EA", 133u},
    {"src", "DREG", "DREG", 136u},
    {"dst", "EA", "EA", 135u},
    {"src", "EA", "EA", 138u},
    {"dst", "DREG", "DREG", 139u},
    {"src", "DREG", "DREG", 142u},
    {"dst", "EA", "EA", 141u},
    {"src", "EA", "EA", 144u},
    {"dst", "DREG", "DREG", 145u},
    {"src", "DREG", "DREG", 148u},
    {"dst", "EA", "EA", 147u},
    {"src", "EA", "EA", 150u},
    {"dst", "DREG", "DREG", 151u},
    {"src", "DREG", "DREG", 154u},
    {"dst", "EA", "EA", 153u},
    {"src", "EA", "EA", 156u},
    {"dst", "DREG", "DREG", 157u},
    {"src", "DREG", "DREG", 160u},
    {"dst", "EA", "EA", 159u},
    {"src", "EA", "EA", 162u},
    {"dst", "DREG", "DREG", 163u},
    {"src", "DREG", "DREG", 166u},
    {"dst", "EA", "EA", 165u},
    {"src", "EA", "EA", 168u},
    {"dst", "DREG", "DREG", 169u},
    {"src", "DREG", "DREG", 171u},
    {"dst", "DREG", "DREG", 172u},
    {"src", "EA", "EA", 174u},
    {"dst", "AREG", "AREG", 175u},
    {"src", "DREG", "DREG", 177u},
    {"dst", "EA", "EA", 176u},
    {"src", "EA", "EA", 179u},
    {"dst", "DREG", "DREG", 180u},
    {"src", "DREG", "DREG", 183u},
    {"dst", "EA", "EA", 182u},
    {"src", "EA", "EA", 185u},
    {"dst", "DREG", "DREG", 186u},
    {"src", "DREG", "DREG", 189u},
    {"dst", "EA", "EA", 188u},
    {"src", "EA", "EA", 191u},
    {"dst", "DREG", "DREG", 192u},
    {"lhs", "DREG", "DREG", 195u},
    {"rhs", "EA", "EA", 194u},
    {"lhs", "EA", "EA", 197u},
    {"rhs", "DREG", "DREG", 198u},
    {"src", "DREG", "DREG", 201u},
    {"dst", "EA", "EA", 200u},
    {"src", "EA", "EA", 203u},
    {"dst", "DREG", "DREG", 204u},
    {"src", "DREG", "DREG", 207u},
    {"dst", "EA", "EA", 206u},
    {"src", "EA", "EA", 209u},
    {"dst", "DREG", "DREG", 210u},
    {"src", "DREG", "DREG", 213u},
    {"dst", "EA", "EA", 212u},
    {"src", "EA", "EA", 215u},
    {"dst", "DREG", "DREG", 216u},
    {"src", "DREG", "DREG", 219u},
    {"dst", "EA", "EA", 218u},
    {"imm", "imm6", "IMM6", 223u},
    {"dst", "EA", "EA", 221u},
    {"imm", "imm6", "IMM6", 226u},
    {"dst", "EA", "EA", 224u},
    {"imm", "imm6", "IMM6", 229u},
    {"dst", "EA", "EA", 227u},
    {"imm", "imm6", "IMM6", 232u},
    {"dst", "EA", "EA", 230u},
    {"imm", "imm6", "IMM6", 235u},
    {"dst", "EA", "EA", 233u},
    {"imm", "imm6", "IMM6", 238u},
    {"dst", "EA", "EA", 236u},
    {"imm", "imm6", "IMM6", 241u},
    {"rhs", "EA", "EA", 239u},
    {"imm", "imm6", "IMM6", 244u},
    {"dst", "EA", "EA", 242u},
    {"lhs", "EA", "EA", 245u},
    {"rhs", "EA", "EA", 246u},
    {"imm", "imm6", "IMM6", 250u},
    {"rhs", "EA", "EA", 248u},
    {"src", "EA", "EA", 251u},
    {"dst", "EA", "EA", 252u},
    {"src", "EA", "EA", 254u},
    {"dst", "EA", "EA", 255u},
    {"src", "EA", "EA", 256u},
    {"dst", "EA", "EA", 257u},
    {"src", "EA", "EA", 258u},
    {"dst", "EA", "EA", 259u},
    {"src", "EA", "EA", 261u},
    {"dst", "EA", "EA", 262u},
    {"src", "EA", "EA", 264u},
    {"dst", "EA", "EA", 265u},
    {"lo", "DREG", "DREG", 268u},
    {"value", "EA", "EA", 267u},
    {"hi", "DREG", "DREG", 269u},
    {"lo", "DREG", "DREG", 272u},
    {"value", "EA", "EA", 271u},
    {"hi", "DREG", "DREG", 273u},
    {"lo", "DREG", "DREG", 276u},
    {"value", "EA", "EA", 275u},
    {"hi", "DREG", "DREG", 277u},
    {"lo", "DREG", "DREG", 280u},
    {"value", "EA", "EA", 279u},
    {"hi", "DREG", "DREG", 281u},
    {"lo", "DREG", "DREG", 284u},
    {"value", "EA", "EA", 283u},
    {"hi", "DREG", "DREG", 285u},
    {"lo", "DREG", "DREG", 288u},
    {"value", "EA", "EA", 287u},
    {"hi", "DREG", "DREG", 289u},
    {"lo", "DREG", "DREG", 292u},
    {"value", "EA", "EA", 291u},
    {"hi", "DREG", "DREG", 293u},
    {"lo", "DREG", "DREG", 296u},
    {"value", "EA", "EA", 295u},
    {"hi", "DREG", "DREG", 297u},
    {"src", "DREG", "DREG", 300u},
    {"dst", "EA", "EA", 299u},
    {"src", "EA", "EA", 302u},
    {"dst", "DREG", "DREG", 303u},
    {"src", "DREG", "DREG", 306u},
    {"dst", "EA", "EA", 305u},
    {"src", "EA", "EA", 308u},
    {"dst", "DREG", "DREG", 309u},
    {"src", "EA", "EA", 311u},
    {"quotient", "DREG", "DREG", 312u},
    {"remainder", "DREG", "DREG", 313u},
    {"src", "DREG", "DREG", 316u},
    {"dst", "EA", "EA", 315u},
    {"src", "EA", "EA", 318u},
    {"dst", "DREG", "DREG", 319u},
    {"src", "DREG", "DREG", 322u},
    {"dst", "EA", "EA", 321u},
    {"src", "EA", "EA", 324u},
    {"quotient", "DREG", "DREG", 325u},
    {"remainder", "DREG", "DREG", 326u},
    {"src", "EA", "EA", 328u},
    {"dst", "DREG", "DREG", 329u},
    {"src", "DREG", "DREG", 332u},
    {"dst", "EA", "EA", 331u},
    {"src", "EA", "EA", 334u},
    {"dst", "DREG", "DREG", 335u},
    {"src", "DREG", "DREG", 338u},
    {"dst", "EA", "EA", 337u},
    {"src", "EA", "EA", 340u},
    {"dst", "DREG", "DREG", 341u},
    {"src", "DREG", "DREG", 344u},
    {"dst", "EA", "EA", 343u},
    {"src", "EA", "EA", 346u},
    {"dst", "DREG", "DREG", 347u},
    {"src", "DREG", "DREG", 350u},
    {"dst", "EA", "EA", 349u},
    {"src", "EA", "EA", 352u},
    {"dst", "DREG", "DREG", 353u},
    {"src", "DREG", "DREG", 356u},
    {"dst", "EA", "EA", 355u},
    {"src", "EA", "EA", 358u},
    {"dst", "DREG", "DREG", 359u},
    {"src", "DREG", "DREG", 362u},
    {"dst", "EA", "EA", 361u},
    {"src", "EA", "EA", 364u},
    {"dst", "DREG", "DREG", 365u},
    {"src", "DREG", "DREG", 368u},
    {"dst", "EA", "EA", 367u},
    {"src", "EA", "EA", 370u},
    {"dst", "DREG", "DREG", 371u},
    {"src", "EA", "EA", 373u},
    {"multiplier", "DREG", "DREG", 374u},
    {"acc", "DREG", "DREG", 375u},
    {"src", "EA", "EA", 377u},
    {"multiplier", "DREG", "DREG", 378u},
    {"acc", "DREG", "DREG", 379u},
    {"bit_index", "DREG", "DREG", 381u},
    {"dst", "DREG", "DREG", 381u},
    {"bit_index", "DREG", "DREG", 384u},
    {"dst", "DREG", "DREG", 384u},
    {"bit_index", "DREG", "DREG", 387u},
    {"dst", "DREG", "DREG", 387u},
    {"bit_index", "DREG", "DREG", 390u},
    {"dst", "DREG", "DREG", 390u},
    {"src", "EA", "EA", 393u},
    {"count", "DREG", "DREG", 395u},
    {"dst", "DREG", "DREG", 395u},
    {"count", "DREG", "DREG", 398u},
    {"dst", "DREG", "DREG", 398u},
    {"src", "DREG", "DREG", 401u},
    {"dst", "DREG", "DREG", 402u},
    {"bit_index", "DREG", "DREG", 405u},
    {"dst", "EA", "EA", 404u},
    {"bit_index", "DREG", "DREG", 408u},
    {"dst", "EA", "EA", 407u},
    {"bit_index", "DREG", "DREG", 411u},
    {"dst", "EA", "EA", 410u},
    {"bit_index", "DREG", "DREG", 414u},
    {"dst", "EA", "EA", 413u},
    {"src", "EA", "EA", 416u},
    {"dst", "DREG", "DREG", 417u},
    {"src", "EA", "EA", 419u},
    {"dst", "DREG", "DREG", 420u},
    {"src", "EA", "EA", 422u},
    {"dst", "DREG", "DREG", 423u},
    {"src", "EA", "EA", 425u},
    {"dst", "DREG", "DREG", 426u},
    {"src", "EA", "EA", 428u},
    {"dst", "DREG", "DREG", 429u},
    {"count", "DREG", "DREG", 432u},
    {"dst", "EA", "EA", 431u},
    {"count", "DREG", "DREG", 435u},
    {"dst", "EA", "EA", 434u},
    {"src", "DREG", "DREG", 438u},
    {"dst", "EA", "EA", 437u},
    {"src", "EA", "EA", 440u},
    {"dst", "DREG", "DREG", 441u},
    {"count", "DREG", "DREG", 443u},
    {"dst", "DREG", "DREG", 443u},
    {"count", "DREG", "DREG", 446u},
    {"dst", "DREG", "DREG", 446u},
    {"count", "DREG", "DREG", 449u},
    {"dst", "DREG", "DREG", 449u},
    {"count", "DREG", "DREG", 452u},
    {"dst", "DREG", "DREG", 452u},
    {"count", "DREG", "DREG", 455u},
    {"dst", "DREG", "DREG", 455u},
    {"count", "DREG", "DREG", 459u},
    {"dst", "EA", "EA", 458u},
    {"count", "DREG", "DREG", 462u},
    {"dst", "EA", "EA", 461u},
    {"count", "DREG", "DREG", 465u},
    {"dst", "EA", "EA", 464u},
    {"count", "DREG", "DREG", 468u},
    {"dst", "EA", "EA", 467u},
    {"count", "DREG", "DREG", 471u},
    {"dst", "EA", "EA", 470u},
    {"bit_index", "selector_imm6", "selector6", 474u},
    {"dst", "EA", "EA", 473u},
    {"bit_index", "selector_imm6", "selector6", 477u},
    {"dst", "EA", "EA", 476u},
    {"bit_index", "selector_imm6", "selector6", 480u},
    {"dst", "EA", "EA", 479u},
    {"bit_index", "selector_imm6", "selector6", 483u},
    {"dst", "EA", "EA", 482u},
    {"count", "selector_imm6", "selector6", 486u},
    {"dst", "EA", "EA", 485u},
    {"count", "selector_imm6", "selector6", 489u},
    {"dst", "EA", "EA", 488u},
    {"count", "selector_imm6", "selector6", 492u},
    {"dst", "EA", "EA", 491u},
    {"count", "selector_imm6", "selector6", 495u},
    {"dst", "EA", "EA", 494u},
    {"count", "selector_imm6", "selector6", 498u},
    {"dst", "EA", "EA", 497u},
    {"count", "selector_imm6", "selector6", 501u},
    {"dst", "EA", "EA", 500u},
    {"count", "selector_imm6", "selector6", 504u},
    {"dst", "EA", "EA", 503u},
    {"src", "DREG", "DREG", 507u},
    {"dst", "EA", "EA", 506u},
    {"src", "EA", "EA", 509u},
    {"dst", "DREG", "DREG", 510u},
    {"lhs", "DREG", "DREG", 513u},
    {"rhs", "EA", "EA", 512u},
    {"lhs", "EA", "EA", 515u},
    {"rhs", "DREG", "DREG", 516u},
    {"src", "EA", "EA", 518u},
    {"dst", "EA", "EA", 519u},
    {"dst", "DREG", "DREG", 521u},
    {"selector", "DREG", "DREG", 522u},
    {"src_bank", "DBANK", "DBANK", 523u},
    {"regs", "bitmap16", "bitmap16", 524u},
    {"dst_bank", "DBANK", "DBANK", 525u},
    {"regs", "bitmap16", "bitmap16", 526u},
    {"selector", "DBANK", "DBANK", 527u},
    {"bank", "DBANK", "DBANK", 528u},
    {"regs", "bitmap16", "bitmap16", 529u},
    {"bank", "DBANK", "DBANK", 530u},
    {"regs", "bitmap16", "bitmap16", 531u},
    {"dst_bank", "DBANK", "DBANK", 532u},
    {"src_bank", "DBANK", "DBANK", 533u},
    {"regs", "bitmap16", "bitmap16", 534u},
    {"bank_a", "DBANK", "DBANK", 535u},
    {"bank_b", "DBANK", "DBANK", 536u},
    {"regs", "bitmap16", "bitmap16", 537u},
    {"src", "EA", "EA", 538u},
    {"dst", "AREG", "AREG", 539u},
    {"src", "EA", "EA", 540u},
    {"dst", "AREG", "AREG", 541u},
    {"src", "EA", "EA", 542u},
    {"target", "EA", "EA", 543u},
    {"new_cs", "DREG", "DREG", 545u},
    {"target", "EA", "EA", 544u},
    {"new_cs", "DREG", "DREG", 547u},
    {"target", "EA", "EA", 546u},
    {"counter", "DREG", "DREG", 550u},
    {"target", "EA", "EA", 549u},
    {"src", "FREG", "FREG", 553u},
    {"dst", "FREG", "FREG", 554u},
    {"target", "EA", "EA", 557u},
    {"target", "EA", "EA", 559u},
    {"dst", "EA", "EA", 562u},
    {"src", "AREG", "AREG", 566u},
    {"dst", "EA", "EA", 565u},
    {"src", "DREG", "DREG", 570u},
    {"dst", "EA", "EA", 569u},
    {"index", "DREG", "DREG", 574u},
    {"bound", "DREG", "DREG", 575u},
    {"target", "EA", "EA", 573u},
    {"src", "EA", "EA", 578u},
    {"dst", "AREG", "AREG", 579u},
    {"src", "EA", "EA", 582u},
    {"dst", "DREG", "DREG", 583u},
    {"src", "EA", "EA", 586u},
    {"dst", "FREG", "FREG", 587u},
    {"src", "FREG", "FREG", 591u},
    {"dst", "EA", "EA", 590u},
    {"expected", "DREG", "DREG", 596u},
    {"desired", "DREG", "DREG", 597u},
    {"memory", "EA", "EA", 595u},
    {"src", "DREG", "DREG", 600u},
    {"memory", "EA", "EA", 599u},
    {"src", "DREG", "DREG", 604u},
    {"memory", "EA", "EA", 603u},
    {"src", "DREG", "DREG", 608u},
    {"memory", "EA", "EA", 607u},
    {"src", "DREG", "DREG", 612u},
    {"memory", "EA", "EA", 611u},
    {"src", "DREG", "DREG", 616u},
    {"memory", "EA", "EA", 615u},
    {"src", "EA", "EA", 618u},
    {"asid", "imm16", "IMM16", 619u},
    {"new_ptcr", "DREG", "DREG", 620u},
    {"dst", "DREG", "DREG", 621u},
    {"page", "EA", "EA", 622u},
    {"new_ptcr", "DREG", "DREG", 623u},
    {"asid", "DREG", "DREG", 624u},
    {"target", "EA_or_range", "EA", 625u},
    {"target", "EA_or_range", "EA", 626u},
    {"target", "EA_or_range", "EA", 627u},
    {"target", "EA_or_range", "EA", 628u},
    {"target", "EA_or_range", "EA", 629u},
    {"src", "linear_or_EA", "EA", 630u},
    {"src", "linear_or_EA", "EA", 631u},
    {"src", "linear_or_EA", "EA", 632u},
    {"cr", "cr", "CR", 634u},
    {"dst", "DREG", "DREG", 633u},
    {"src", "DREG", "DREG", 635u},
    {"cr", "cr", "CR", 636u},
    {"dst", "DREG", "DREG", 637u},
    {"src", "DREG", "DREG", 638u},
    {"dst", "DREG", "DREG", 639u},
    {"src", "DREG", "DREG", 640u},
    {"reg", "DREG", "DREG", 641u},
    {"dst", "DREG", "DREG", 642u},
    {"seg", "SREG", "SREG", 643u},
    {"dst", "DREG", "DREG", 644u},
    {"src", "DREG", "DREG", 645u},
    {"seg", "SREG", "SREG", 646u},
    {"memory", "EA", "EA", 647u},
    {"memory", "EA", "EA", 648u},
    {"counter_id", "imm16", "IMM16", 650u},
    {"dst", "DREG", "DREG", 649u},
    {"src", "DREG", "DREG", 651u},
    {"dst", "EA", "EA", 652u},
    {"src", "FREG", "FREG", 653u},
    {"dst", "FREG", "FREG", 654u},
    {"src", "FREG", "FREG", 656u},
    {"constant_id", "imm16", "IMM16", 659u},
    {"dst", "FREG", "FREG", 658u},
    {"src", "DREG", "DREG", 660u},
    {"dst", "FREG", "FREG", 661u},
    {"src", "FREG", "FREG", 663u},
    {"dst", "DREG", "DREG", 662u},
    {"src", "FREG", "FREG", 665u},
    {"dst", "FREG", "FREG", 666u},
    {"src", "FREG", "FREG", 669u},
    {"dst", "DREG", "DREG", 668u},
    {"src", "DREG", "DREG", 670u},
    {"dst", "FREG", "FREG", 671u},
    {"src", "FREG", "FREG", 672u},
    {"dst", "FREG", "FREG", 673u},
    {"src", "EA", "EA", 674u},
    {"dst", "FREG", "FREG", 675u},
    {"src", "EA", "EA", 677u},
    {"src", "FREG", "FREG", 680u},
    {"dst", "DREG", "DREG", 679u},
    {"src", "FREG", "FREG", 681u},
    {"dst", "FREG", "FREG", 682u},
    {"src", "EA", "EA", 683u},
    {"dst", "FREG", "FREG", 684u},
    {"src", "FREG", "FREG", 687u},
    {"dst", "EA", "EA", 686u},
    {"src", "EA", "EA", 689u},
    {"dst", "FREG", "FREG", 690u},
    {"src", "FREG", "FREG", 693u},
    {"dst", "EA", "EA", 692u},
    {"src", "EA", "EA", 695u},
    {"dst", "FREG", "FREG", 696u},
    {"src", "FREG", "FREG", 698u},
    {"dst", "FREG", "FREG", 699u},
    {"src", "FREG", "FREG", 701u},
    {"dst", "FREG", "FREG", 702u},
    {"lo", "FREG", "FREG", 705u},
    {"value", "EA", "EA", 704u},
    {"hi", "FREG", "FREG", 706u},
    {"lo", "FREG", "FREG", 708u},
    {"value", "FREG", "FREG", 709u},
    {"hi", "FREG", "FREG", 710u},
    {"lo", "FREG", "FREG", 713u},
    {"value", "EA", "EA", 712u},
    {"hi", "FREG", "FREG", 714u},
    {"lo", "FREG", "FREG", 716u},
    {"value", "FREG", "FREG", 717u},
    {"hi", "FREG", "FREG", 718u},
    {"lo", "FREG", "FREG", 721u},
    {"value", "EA", "EA", 720u},
    {"hi", "FREG", "FREG", 722u},
    {"lo", "FREG", "FREG", 724u},
    {"value", "FREG", "FREG", 725u},
    {"hi", "FREG", "FREG", 726u},
    {"lo", "FREG", "FREG", 729u},
    {"value", "EA", "EA", 728u},
    {"hi", "FREG", "FREG", 730u},
    {"lo", "FREG", "FREG", 732u},
    {"value", "FREG", "FREG", 733u},
    {"hi", "FREG", "FREG", 734u},
    {"sign_src", "FREG", "FREG", 736u},
    {"magnitude_src", "FREG", "FREG", 737u},
    {"dst", "FREG", "FREG", 738u},
    {"lhs", "EA", "EA", 740u},
    {"rhs", "FREG", "FREG", 741u},
    {"dst", "FREG", "FREG", 742u},
    {"lhs", "FREG", "FREG", 745u},
    {"rhs", "EA", "EA", 744u},
    {"dst", "FREG", "FREG", 746u},
    {"lhs", "FREG", "FREG", 748u},
    {"rhs", "FREG", "FREG", 749u},
    {"dst", "FREG", "FREG", 750u},
    {"lhs", "EA", "EA", 752u},
    {"rhs", "FREG", "FREG", 753u},
    {"dst", "FREG", "FREG", 754u},
    {"lhs", "FREG", "FREG", 757u},
    {"rhs", "EA", "EA", 756u},
    {"dst", "FREG", "FREG", 758u},
    {"lhs", "FREG", "FREG", 760u},
    {"rhs", "FREG", "FREG", 761u},
    {"dst", "FREG", "FREG", 762u},
    {"lhs", "EA", "EA", 764u},
    {"rhs", "FREG", "FREG", 765u},
    {"dst", "FREG", "FREG", 766u},
    {"dst", "FREG", "FREG", 768u},
    {"lhs", "FREG", "FREG", 770u},
    {"rhs", "EA", "EA", 769u},
    {"dst", "FREG", "FREG", 771u},
    {"lhs", "FREG", "FREG", 773u},
    {"rhs", "FREG", "FREG", 774u},
    {"dst", "FREG", "FREG", 775u},
    {"lhs", "EA", "EA", 777u},
    {"rhs", "FREG", "FREG", 778u},
    {"dst", "FREG", "FREG", 779u},
    {"lhs", "FREG", "FREG", 782u},
    {"rhs", "EA", "EA", 781u},
    {"dst", "FREG", "FREG", 783u},
    {"lhs", "FREG", "FREG", 785u},
    {"rhs", "FREG", "FREG", 786u},
    {"dst", "FREG", "FREG", 787u},
    {"regs", "fbitmap16", "fbitmap16", 789u},
    {"regs", "fbitmap16", "fbitmap16", 790u},
    {"dst", "EA", "EA", 791u},
    {"lhs", "FREG", "FREG", 792u},
    {"rhs", "FREG", "FREG", 793u},
    {"src", "FREG", "FREG", 794u},
    {"dst", "FREG", "FREG", 795u},
    {"src", "EA", "EA", 797u},
    {"dst", "FREG", "FREG", 798u},
    {"src", "FREG", "FREG", 801u},
    {"dst", "EA", "EA", 800u},
    {"src", "EA", "EA", 803u},
    {"dst", "FREG", "FREG", 804u},
    {"src", "FREG", "FREG", 806u},
    {"dst", "FREG", "FREG", 807u},
    {"src", "FREG", "FREG", 809u},
    {"dst", "FREG", "FREG", 810u},
    {"src", "FREG", "FREG", 812u},
    {"dst", "FREG", "FREG", 813u},
    {"src", "FREG", "FREG", 815u},
    {"dst", "FREG", "FREG", 816u},
    {"src", "EA", "EA", 818u},
    {"dst", "FREG", "FREG", 819u},
    {"src", "FREG", "FREG", 822u},
    {"dst", "EA", "EA", 821u},
    {"src", "EA", "EA", 824u},
    {"dst", "FREG", "FREG", 825u},
    {"src", "EA", "EA", 827u},
    {"dst", "FREG", "FREG", 828u},
    {"src", "EA", "EA", 830u},
    {"dst", "FREG", "FREG", 831u},
    {"src", "FREG", "FREG", 834u},
    {"dst", "EA", "EA", 833u},
    {"src", "FREG", "FREG", 836u},
    {"dst", "FREG", "FREG", 837u},
    {"src", "FREG", "FREG", 839u},
    {"dst", "FREG", "FREG", 840u},
    {"src", "FREG", "FREG", 842u},
    {"dst", "FREG", "FREG", 843u},
    {"src", "FREG", "FREG", 845u},
    {"dst", "FREG", "FREG", 846u},
    {"src", "EA", "EA", 848u},
    {"dst", "FREG", "FREG", 849u},
    {"src", "FREG", "FREG", 852u},
    {"dst", "EA", "EA", 851u},
    {"src", "EA", "EA", 854u},
    {"dst", "FREG", "FREG", 855u},
    {"src", "EA", "EA", 857u},
    {"dst", "FREG", "FREG", 858u},
    {"src", "EA", "EA", 860u},
    {"dst", "FREG", "FREG", 861u},
    {"src", "FREG", "FREG", 863u},
    {"dst", "FREG", "FREG", 864u},
    {"src", "FREG", "FREG", 866u},
    {"dst", "FREG", "FREG", 867u},
    {"src", "FREG", "FREG", 869u},
    {"dst", "FREG", "FREG", 870u},
    {"src", "FREG", "FREG", 872u},
    {"dst", "FREG", "FREG", 873u},
    {"src", "EA", "EA", 875u},
    {"dst", "FREG", "FREG", 876u},
    {"src", "EA", "EA", 878u},
    {"dst", "FREG", "FREG", 879u},
    {"src", "FREG", "FREG", 882u},
    {"dst", "EA", "EA", 881u},
    {"src", "EA", "EA", 884u},
    {"dst", "FREG", "FREG", 885u},
    {"src", "EA", "EA", 887u},
    {"dst", "FREG", "FREG", 888u},
    {"src", "FREG", "FREG", 891u},
    {"dst", "EA", "EA", 890u},
    {"src", "FREG", "FREG", 893u},
    {"dst", "FREG", "FREG", 894u},
    {"src", "FREG", "FREG", 896u},
    {"dst", "FREG", "FREG", 897u},
    {"src", "FREG", "FREG", 899u},
    {"dst", "FREG", "FREG", 900u},
    {"src", "FREG", "FREG", 902u},
    {"dst", "FREG", "FREG", 903u},
    {"src", "EA", "EA", 905u},
    {"dst", "FREG", "FREG", 906u},
    {"src", "EA", "EA", 908u},
    {"dst", "FREG", "FREG", 909u},
    {"src", "FREG", "FREG", 912u},
    {"dst", "EA", "EA", 911u},
    {"src", "EA", "EA", 914u},
    {"dst", "FREG", "FREG", 915u},
    {"src", "EA", "EA", 917u},
    {"dst", "FREG", "FREG", 918u},
    {"src", "FREG", "FREG", 921u},
    {"dst", "EA", "EA", 920u},
    {"src", "FREG", "FREG", 923u},
    {"dst", "FREG", "FREG", 924u},
    {"src", "FREG", "FREG", 926u},
    {"dst", "FREG", "FREG", 927u},
    {"src", "FREG", "FREG", 929u},
    {"dst", "FREG", "FREG", 930u},
    {"src", "FREG", "FREG", 932u},
    {"dst", "FREG", "FREG", 933u},
    {"src", "FREG", "FREG", 935u},
    {"dst", "FREG", "FREG", 936u},
    {"src", "FREG", "FREG", 938u},
    {"dst", "FREG", "FREG", 939u},
    {"src", "FREG", "FREG", 941u},
    {"dst", "FREG", "FREG", 942u},
    {"src", "FREG", "FREG", 944u},
    {"dst", "FREG", "FREG", 945u},
    {"src", "FREG", "FREG", 947u},
    {"dst", "FREG", "FREG", 948u},
    {"src", "FREG", "FREG", 950u},
    {"dst", "FREG", "FREG", 951u},
    {"src", "FREG", "FREG", 953u},
    {"dst", "FREG", "FREG", 954u},
    {"src", "FREG", "FREG", 956u},
    {"dst", "FREG", "FREG", 957u},
    {"src", "FREG", "FREG", 959u},
    {"dst", "FREG", "FREG", 960u},
    {"src", "FREG", "FREG", 962u},
    {"dst", "FREG", "FREG", 963u},
    {"src", "FREG", "FREG", 965u},
    {"dst", "FREG", "FREG", 966u},
    {"src", "FREG", "FREG", 968u},
    {"dst", "FREG", "FREG", 969u},
    {"src", "FREG", "FREG", 971u},
    {"dst", "FREG", "FREG", 972u},
    {"src", "FREG", "FREG", 974u},
    {"dst", "FREG", "FREG", 975u},
    {"src", "FREG", "FREG", 977u},
    {"dst", "FREG", "FREG", 978u},
    {"src", "FREG", "FREG", 980u},
    {"dst", "FREG", "FREG", 981u},
    {"counter", "DREG", "DREG", 983u},
    {"body_bytes", "imm16", "imm16", 65535u},
};

const uint16_t bedrock_primary_values[] = {
    0x100u,
    0x101u,
    0x102u,
    0x103u,
    0x104u,
    0x105u,
    0x106u,
    0x107u,
    0x108u,
    0x109u,
    0x10au,
    0x10bu,
    0x10cu,
    0x10du,
    0x10eu,
    0x10fu,
    0x110u,
    0x111u,
    0x112u,
    0x113u,
    0x114u,
    0x115u,
    0x116u,
    0x117u,
    0x118u,
    0x119u,
    0x11au,
    0x11bu,
    0x11cu,
    0x11du,
    0x11eu,
    0x11fu,
    0x120u,
    0x121u,
    0x122u,
    0x123u,
    0x124u,
    0x125u,
    0x126u,
    0x127u,
    0x128u,
    0x129u,
    0x12au,
    0x12bu,
    0x12cu,
    0x12du,
    0x12eu,
    0x12fu,
    0x130u,
    0x131u,
    0x132u,
    0x133u,
    0x134u,
    0x135u,
    0x136u,
    0x137u,
    0x138u,
    0x139u,
    0x13au,
    0x13bu,
    0x13cu,
    0x13du,
    0x13eu,
    0x13fu,
    0x140u,
    0x141u,
    0x142u,
    0x143u,
    0x144u,
    0x145u,
    0x146u,
    0x147u,
    0x148u,
    0x149u,
    0x14au,
    0x14bu,
    0x14cu,
    0x14du,
    0x14eu,
    0x14fu,
    0x150u,
    0x151u,
    0x152u,
    0x153u,
    0x154u,
    0x155u,
    0x156u,
    0x157u,
    0x158u,
    0x159u,
    0x15au,
    0x15bu,
    0x15cu,
    0x15du,
    0x15eu,
    0x15fu,
    0x160u,
    0x161u,
    0x162u,
    0x163u,
    0x164u,
    0x165u,
    0x166u,
    0x167u,
    0x168u,
    0x169u,
    0x16au,
    0x16bu,
    0x16cu,
    0x16du,
    0x16eu,
    0x16fu,
    0x170u,
    0x171u,
    0x172u,
    0x173u,
    0x174u,
    0x175u,
    0x176u,
    0x177u,
    0x178u,
    0x179u,
    0x17au,
    0x17bu,
    0x17cu,
    0x17du,
    0x17eu,
    0x17fu,
    0x180u,
    0x181u,
    0x182u,
    0x183u,
    0x184u,
    0x185u,
    0x186u,
    0x187u,
    0x188u,
    0x189u,
    0x18au,
    0x18bu,
    0x18cu,
    0x18du,
    0x18eu,
    0x18fu,
    0x190u,
    0x191u,
    0x192u,
    0x193u,
    0x194u,
    0x195u,
    0x196u,
    0x197u,
    0x198u,
    0x199u,
    0x19au,
    0x19bu,
    0x19cu,
    0x19du,
    0x19eu,
    0x19fu,
    0x1a0u,
    0x1a1u,
    0x1a2u,
    0x1a3u,
    0x1a4u,
    0x1a5u,
    0x1a6u,
    0x1a7u,
    0x1a8u,
    0x1a9u,
    0x1aau,
    0x1abu,
    0x1acu,
    0x1adu,
    0x1aeu,
    0x1afu,
    0x1b0u,
    0x1b1u,
    0x1b2u,
    0x1b3u,
    0x1b4u,
    0x1b5u,
    0x1b6u,
    0x1b7u,
    0x1b8u,
    0x1b9u,
    0x1bau,
    0x1bbu,
    0x1bcu,
    0x1bdu,
    0x1beu,
    0x1bfu,
    0x200u,
    0x201u,
    0x202u,
    0x203u,
    0x204u,
    0x205u,
    0x206u,
    0x207u,
    0x208u,
    0x209u,
    0x20au,
    0x20bu,
    0x20cu,
    0x20du,
    0x20eu,
    0x20fu,
    0x210u,
    0x211u,
    0x212u,
    0x213u,
    0x214u,
    0x215u,
    0x216u,
    0x217u,
    0x218u,
    0x219u,
    0x21au,
    0x21bu,
    0x21cu,
    0x21du,
    0x21eu,
    0x21fu,
    0x220u,
    0x221u,
    0x222u,
    0x223u,
    0x224u,
    0x225u,
    0x226u,
    0x227u,
    0x228u,
    0x229u,
    0x22au,
    0x22bu,
    0x22cu,
    0x22du,
    0x22eu,
    0x22fu,
    0x230u,
    0x231u,
    0x232u,
    0x233u,
    0x234u,
    0x235u,
    0x236u,
    0x237u,
    0x238u,
    0x239u,
    0x23au,
    0x23bu,
    0x23cu,
    0x23du,
    0x23eu,
    0x23fu,
    0x240u,
    0x241u,
    0x242u,
    0x243u,
    0x244u,
    0x245u,
    0x246u,
    0x247u,
    0x248u,
    0x249u,
    0x24au,
    0x24bu,
    0x24cu,
    0x24du,
    0x24eu,
    0x24fu,
    0x250u,
    0x251u,
    0x252u,
    0x253u,
    0x254u,
    0x255u,
    0x256u,
    0x257u,
    0x258u,
    0x259u,
    0x25au,
    0x25bu,
    0x25cu,
    0x25du,
    0x25eu,
    0x25fu,
    0x260u,
    0x261u,
    0x262u,
    0x263u,
    0x264u,
    0x265u,
    0x266u,
    0x267u,
    0x268u,
    0x269u,
    0x26au,
    0x26bu,
    0x26cu,
    0x26du,
    0x26eu,
    0x26fu,
    0x270u,
    0x271u,
    0x272u,
    0x273u,
    0x274u,
    0x275u,
    0x276u,
    0x277u,
    0x278u,
    0x279u,
    0x27au,
    0x27bu,
    0x27cu,
    0x27du,
    0x27eu,
    0x27fu,
    0x280u,
    0x281u,
    0x282u,
    0x283u,
    0x284u,
    0x285u,
    0x286u,
    0x287u,
    0x288u,
    0x289u,
    0x28au,
    0x28bu,
    0x28cu,
    0x28du,
    0x28eu,
    0x28fu,
    0x290u,
    0x291u,
    0x292u,
    0x293u,
    0x294u,
    0x295u,
    0x296u,
    0x297u,
    0x298u,
    0x299u,
    0x29au,
    0x29bu,
    0x29cu,
    0x29du,
    0x29eu,
    0x29fu,
    0x2a0u,
    0x2a1u,
    0x2a2u,
    0x2a3u,
    0x2a4u,
    0x2a5u,
    0x2a6u,
    0x2a7u,
    0x2a8u,
    0x2a9u,
    0x2aau,
    0x2abu,
    0x2acu,
    0x2adu,
    0x2aeu,
    0x2afu,
    0x2b0u,
    0x2b1u,
    0x2b2u,
    0x2b3u,
    0x2b4u,
    0x2b5u,
    0x2b6u,
    0x2b7u,
    0x2b8u,
    0x2b9u,
    0x2bau,
    0x2bbu,
    0x2bcu,
    0x2bdu,
    0x2beu,
    0x2bfu,
    0x400u,
    0x440u,
    0x480u,
    0x4c0u,
    0x500u,
    0x540u,
    0x580u,
    0x5c0u,
    0x600u,
    0x640u,
    0x680u,
    0x6c0u,
    0x700u,
    0x740u,
    0x780u,
    0x7c0u,
    0x401u,
    0x441u,
    0x481u,
    0x4c1u,
    0x501u,
    0x541u,
    0x581u,
    0x5c1u,
    0x601u,
    0x641u,
    0x681u,
    0x6c1u,
    0x701u,
    0x741u,
    0x781u,
    0x7c1u,
    0x402u,
    0x442u,
    0x482u,
    0x4c2u,
    0x502u,
    0x542u,
    0x582u,
    0x5c2u,
    0x602u,
    0x642u,
    0x682u,
    0x6c2u,
    0x702u,
    0x742u,
    0x782u,
    0x7c2u,
    0x403u,
    0x443u,
    0x483u,
    0x4c3u,
    0x503u,
    0x543u,
    0x583u,
    0x5c3u,
    0x603u,
    0x643u,
    0x683u,
    0x6c3u,
    0x703u,
    0x743u,
    0x783u,
    0x7c3u,
    0x408u,
    0x409u,
    0x40au,
    0x40bu,
    0x40cu,
    0x40du,
    0x40eu,
    0x40fu,
    0x410u,
    0x411u,
    0x412u,
    0x413u,
    0x414u,
    0x415u,
    0x416u,
    0x417u,
    0x418u,
    0x419u,
    0x41au,
    0x41bu,
    0x41cu,
    0x41du,
    0x41eu,
    0x41fu,
    0x420u,
    0x421u,
    0x422u,
    0x423u,
    0x424u,
    0x425u,
    0x426u,
    0x427u,
    0x428u,
    0x429u,
    0x42au,
    0x42bu,
    0x42cu,
    0x42du,
    0x42eu,
    0x42fu,
    0x430u,
    0x431u,
    0x432u,
    0x433u,
    0x434u,
    0x435u,
    0x436u,
    0x437u,
    0x438u,
    0x439u,
    0x43au,
    0x43bu,
    0x43cu,
    0x43du,
    0x43eu,
    0x43fu,
    0x448u,
    0x449u,
    0x44au,
    0x44bu,
    0x44cu,
    0x44du,
    0x44eu,
    0x44fu,
    0x450u,
    0x451u,
    0x452u,
    0x453u,
    0x454u,
    0x455u,
    0x456u,
    0x457u,
    0x458u,
    0x459u,
    0x45au,
    0x45bu,
    0x45cu,
    0x45du,
    0x45eu,
    0x45fu,
    0x460u,
    0x461u,
    0x462u,
    0x463u,
    0x464u,
    0x465u,
    0x466u,
    0x467u,
    0x468u,
    0x469u,
    0x46au,
    0x46bu,
    0x46cu,
    0x46du,
    0x46eu,
    0x46fu,
    0x470u,
    0x471u,
    0x472u,
    0x473u,
    0x474u,
    0x475u,
    0x476u,
    0x477u,
    0x478u,
    0x479u,
    0x47au,
    0x47bu,
    0x47cu,
    0x47du,
    0x47eu,
    0x47fu,
    0x488u,
    0x489u,
    0x48au,
    0x48bu,
    0x48cu,
    0x48du,
    0x48eu,
    0x48fu,
    0x490u,
    0x491u,
    0x492u,
    0x493u,
    0x494u,
    0x495u,
    0x496u,
    0x497u,
    0x498u,
    0x499u,
    0x49au,
    0x49bu,
    0x49cu,
    0x49du,
    0x49eu,
    0x49fu,
    0x4a0u,
    0x4a1u,
    0x4a2u,
    0x4a3u,
    0x4a4u,
    0x4a5u,
    0x4a6u,
    0x4a7u,
    0x4a8u,
    0x4a9u,
    0x4aau,
    0x4abu,
    0x4acu,
    0x4adu,
    0x4aeu,
    0x4afu,
    0x4b0u,
    0x4b1u,
    0x4b2u,
    0x4b3u,
    0x4b4u,
    0x4b5u,
    0x4b6u,
    0x4b7u,
    0x4b8u,
    0x4b9u,
    0x4bau,
    0x4bbu,
    0x4bcu,
    0x4bdu,
    0x4beu,
    0x4bfu,
    0x4c8u,
    0x4c9u,
    0x4cau,
    0x4cbu,
    0x4ccu,
    0x4cdu,
    0x4ceu,
    0x4cfu,
    0x4d0u,
    0x4d1u,
    0x4d2u,
    0x4d3u,
    0x4d4u,
    0x4d5u,
    0x4d6u,
    0x4d7u,
    0x4d8u,
    0x4d9u,
    0x4dau,
    0x4dbu,
    0x4dcu,
    0x4ddu,
    0x4deu,
    0x4dfu,
    0x4e0u,
    0x4e1u,
    0x4e2u,
    0x4e3u,
    0x4e4u,
    0x4e5u,
    0x4e6u,
    0x4e7u,
    0x4e8u,
    0x4e9u,
    0x4eau,
    0x4ebu,
    0x4ecu,
    0x4edu,
    0x4eeu,
    0x4efu,
    0x4f0u,
    0x4f1u,
    0x4f2u,
    0x4f3u,
    0x4f4u,
    0x4f5u,
    0x4f6u,
    0x4f7u,
    0x4f8u,
    0x4f9u,
    0x4fau,
    0x4fbu,
    0x4fcu,
    0x4fdu,
    0x4feu,
    0x4ffu,
    0x508u,
    0x509u,
    0x50au,
    0x50bu,
    0x50cu,
    0x50du,
    0x50eu,
    0x50fu,
    0x510u,
    0x511u,
    0x512u,
    0x513u,
    0x514u,
    0x515u,
    0x516u,
    0x517u,
    0x518u,
    0x519u,
    0x51au,
    0x51bu,
    0x51cu,
    0x51du,
    0x51eu,
    0x51fu,
    0x520u,
    0x521u,
    0x522u,
    0x523u,
    0x524u,
    0x525u,
    0x526u,
    0x527u,
    0x528u,
    0x529u,
    0x52au,
    0x52bu,
    0x52cu,
    0x52du,
    0x52eu,
    0x52fu,
    0x530u,
    0x531u,
    0x532u,
    0x533u,
    0x534u,
    0x535u,
    0x536u,
    0x537u,
    0x538u,
    0x539u,
    0x53au,
    0x53bu,
    0x53cu,
    0x53du,
    0x53eu,
    0x53fu,
    0x548u,
    0x549u,
    0x54au,
    0x54bu,
    0x54cu,
    0x54du,
    0x54eu,
    0x54fu,
    0x550u,
    0x551u,
    0x552u,
    0x553u,
    0x554u,
    0x555u,
    0x556u,
    0x557u,
    0x558u,
    0x559u,
    0x55au,
    0x55bu,
    0x55cu,
    0x55du,
    0x55eu,
    0x55fu,
    0x560u,
    0x561u,
    0x562u,
    0x563u,
    0x564u,
    0x565u,
    0x566u,
    0x567u,
    0x568u,
    0x569u,
    0x56au,
    0x56bu,
    0x56cu,
    0x56du,
    0x56eu,
    0x56fu,
    0x570u,
    0x571u,
    0x572u,
    0x573u,
    0x574u,
    0x575u,
    0x576u,
    0x577u,
    0x578u,
    0x579u,
    0x57au,
    0x57bu,
    0x57cu,
    0x57du,
    0x57eu,
    0x57fu,
    0x588u,
    0x589u,
    0x58au,
    0x58bu,
    0x58cu,
    0x58du,
    0x58eu,
    0x58fu,
    0x590u,
    0x591u,
    0x592u,
    0x593u,
    0x594u,
    0x595u,
    0x596u,
    0x597u,
    0x598u,
    0x599u,
    0x59au,
    0x59bu,
    0x59cu,
    0x59du,
    0x59eu,
    0x59fu,
    0x5a0u,
    0x5a1u,
    0x5a2u,
    0x5a3u,
    0x5a4u,
    0x5a5u,
    0x5a6u,
    0x5a7u,
    0x5a8u,
    0x5a9u,
    0x5aau,
    0x5abu,
    0x5acu,
    0x5adu,
    0x5aeu,
    0x5afu,
    0x5b0u,
    0x5b1u,
    0x5b2u,
    0x5b3u,
    0x5b4u,
    0x5b5u,
    0x5b6u,
    0x5b7u,
    0x5b8u,
    0x5b9u,
    0x5bau,
    0x5bbu,
    0x5bcu,
    0x5bdu,
    0x5beu,
    0x5bfu,
    0x5c8u,
    0x5c9u,
    0x5cau,
    0x5cbu,
    0x5ccu,
    0x5cdu,
    0x5ceu,
    0x5cfu,
    0x5d0u,
    0x5d1u,
    0x5d2u,
    0x5d3u,
    0x5d4u,
    0x5d5u,
    0x5d6u,
    0x5d7u,
    0x5d8u,
    0x5d9u,
    0x5dau,
    0x5dbu,
    0x5dcu,
    0x5ddu,
    0x5deu,
    0x5dfu,
    0x5e0u,
    0x5e1u,
    0x5e2u,
    0x5e3u,
    0x5e4u,
    0x5e5u,
    0x5e6u,
    0x5e7u,
    0x5e8u,
    0x5e9u,
    0x5eau,
    0x5ebu,
    0x5ecu,
    0x5edu,
    0x5eeu,
    0x5efu,
    0x5f0u,
    0x5f1u,
    0x5f2u,
    0x5f3u,
    0x5f4u,
    0x5f5u,
    0x5f6u,
    0x5f7u,
    0x5f8u,
    0x5f9u,
    0x5fau,
    0x5fbu,
    0x5fcu,
    0x5fdu,
    0x5feu,
    0x5ffu,
    0x608u,
    0x609u,
    0x60au,
    0x60bu,
    0x60cu,
    0x60du,
    0x60eu,
    0x60fu,
    0x610u,
    0x611u,
    0x612u,
    0x613u,
    0x614u,
    0x615u,
    0x616u,
    0x617u,
    0x618u,
    0x619u,
    0x61au,
    0x61bu,
    0x61cu,
    0x61du,
    0x61eu,
    0x61fu,
    0x620u,
    0x621u,
    0x622u,
    0x623u,
    0x624u,
    0x625u,
    0x626u,
    0x627u,
    0x628u,
    0x629u,
    0x62au,
    0x62bu,
    0x62cu,
    0x62du,
    0x62eu,
    0x62fu,
    0x630u,
    0x631u,
    0x632u,
    0x633u,
    0x634u,
    0x635u,
    0x636u,
    0x637u,
    0x638u,
    0x639u,
    0x63au,
    0x63bu,
    0x63cu,
    0x63du,
    0x63eu,
    0x63fu,
    0x648u,
    0x649u,
    0x64au,
    0x64bu,
    0x64cu,
    0x64du,
    0x64eu,
    0x64fu,
    0x650u,
    0x651u,
    0x652u,
    0x653u,
    0x654u,
    0x655u,
    0x656u,
    0x657u,
    0x658u,
    0x659u,
    0x65au,
    0x65bu,
    0x65cu,
    0x65du,
    0x65eu,
    0x65fu,
    0x660u,
    0x661u,
    0x662u,
    0x663u,
    0x664u,
    0x665u,
    0x666u,
    0x667u,
    0x668u,
    0x669u,
    0x66au,
    0x66bu,
    0x66cu,
    0x66du,
    0x66eu,
    0x66fu,
    0x670u,
    0x671u,
    0x672u,
    0x673u,
    0x674u,
    0x675u,
    0x676u,
    0x677u,
    0x678u,
    0x679u,
    0x67au,
    0x67bu,
    0x67cu,
    0x67du,
    0x67eu,
    0x67fu,
    0x688u,
    0x689u,
    0x68au,
    0x68bu,
    0x68cu,
    0x68du,
    0x68eu,
    0x68fu,
    0x690u,
    0x691u,
    0x692u,
    0x693u,
    0x694u,
    0x695u,
    0x696u,
    0x697u,
    0x698u,
    0x699u,
    0x69au,
    0x69bu,
    0x69cu,
    0x69du,
    0x69eu,
    0x69fu,
    0x6a0u,
    0x6a1u,
    0x6a2u,
    0x6a3u,
    0x6a4u,
    0x6a5u,
    0x6a6u,
    0x6a7u,
    0x6a8u,
    0x6a9u,
    0x6aau,
    0x6abu,
    0x6acu,
    0x6adu,
    0x6aeu,
    0x6afu,
    0x6b0u,
    0x6b1u,
    0x6b2u,
    0x6b3u,
    0x6b4u,
    0x6b5u,
    0x6b6u,
    0x6b7u,
    0x6b8u,
    0x6b9u,
    0x6bau,
    0x6bbu,
    0x6bcu,
    0x6bdu,
    0x6beu,
    0x6bfu,
    0x6c8u,
    0x6c9u,
    0x6cau,
    0x6cbu,
    0x6ccu,
    0x6cdu,
    0x6ceu,
    0x6cfu,
    0x6d0u,
    0x6d1u,
    0x6d2u,
    0x6d3u,
    0x6d4u,
    0x6d5u,
    0x6d6u,
    0x6d7u,
    0x6d8u,
    0x6d9u,
    0x6dau,
    0x6dbu,
    0x6dcu,
    0x6ddu,
    0x6deu,
    0x6dfu,
    0x6e0u,
    0x6e1u,
    0x6e2u,
    0x6e3u,
    0x6e4u,
    0x6e5u,
    0x6e6u,
    0x6e7u,
    0x6e8u,
    0x6e9u,
    0x6eau,
    0x6ebu,
    0x6ecu,
    0x6edu,
    0x6eeu,
    0x6efu,
    0x6f0u,
    0x6f1u,
    0x6f2u,
    0x6f3u,
    0x6f4u,
    0x6f5u,
    0x6f6u,
    0x6f7u,
    0x6f8u,
    0x6f9u,
    0x6fau,
    0x6fbu,
    0x6fcu,
    0x6fdu,
    0x6feu,
    0x6ffu,
    0x708u,
    0x709u,
    0x70au,
    0x70bu,
    0x70cu,
    0x70du,
    0x70eu,
    0x70fu,
    0x710u,
    0x711u,
    0x712u,
    0x713u,
    0x714u,
    0x715u,
    0x716u,
    0x717u,
    0x718u,
    0x719u,
    0x71au,
    0x71bu,
    0x71cu,
    0x71du,
    0x71eu,
    0x71fu,
    0x720u,
    0x721u,
    0x722u,
    0x723u,
    0x724u,
    0x725u,
    0x726u,
    0x727u,
    0x728u,
    0x729u,
    0x72au,
    0x72bu,
    0x72cu,
    0x72du,
    0x72eu,
    0x72fu,
    0x730u,
    0x731u,
    0x732u,
    0x733u,
    0x734u,
    0x735u,
    0x736u,
    0x737u,
    0x738u,
    0x739u,
    0x73au,
    0x73bu,
    0x73cu,
    0x73du,
    0x73eu,
    0x73fu,
    0x748u,
    0x749u,
    0x74au,
    0x74bu,
    0x74cu,
    0x74du,
    0x74eu,
    0x74fu,
    0x750u,
    0x751u,
    0x752u,
    0x753u,
    0x754u,
    0x755u,
    0x756u,
    0x757u,
    0x758u,
    0x759u,
    0x75au,
    0x75bu,
    0x75cu,
    0x75du,
    0x75eu,
    0x75fu,
    0x760u,
    0x761u,
    0x762u,
    0x763u,
    0x764u,
    0x765u,
    0x766u,
    0x767u,
    0x768u,
    0x769u,
    0x76au,
    0x76bu,
    0x76cu,
    0x76du,
    0x76eu,
    0x76fu,
    0x770u,
    0x771u,
    0x772u,
    0x773u,
    0x774u,
    0x775u,
    0x776u,
    0x777u,
    0x778u,
    0x779u,
    0x77au,
    0x77bu,
    0x77cu,
    0x77du,
    0x77eu,
    0x77fu,
    0x788u,
    0x789u,
    0x78au,
    0x78bu,
    0x78cu,
    0x78du,
    0x78eu,
    0x78fu,
    0x790u,
    0x791u,
    0x792u,
    0x793u,
    0x794u,
    0x795u,
    0x796u,
    0x797u,
    0x798u,
    0x799u,
    0x79au,
    0x79bu,
    0x79cu,
    0x79du,
    0x79eu,
    0x79fu,
    0x7a0u,
    0x7a1u,
    0x7a2u,
    0x7a3u,
    0x7a4u,
    0x7a5u,
    0x7a6u,
    0x7a7u,
    0x7a8u,
    0x7a9u,
    0x7aau,
    0x7abu,
    0x7acu,
    0x7adu,
    0x7aeu,
    0x7afu,
    0x7b0u,
    0x7b1u,
    0x7b2u,
    0x7b3u,
    0x7b4u,
    0x7b5u,
    0x7b6u,
    0x7b7u,
    0x7b8u,
    0x7b9u,
    0x7bau,
    0x7bbu,
    0x7bcu,
    0x7bdu,
    0x7beu,
    0x7bfu,
    0x7c8u,
    0x7c9u,
    0x7cau,
    0x7cbu,
    0x7ccu,
    0x7cdu,
    0x7ceu,
    0x7cfu,
    0x7d0u,
    0x7d1u,
    0x7d2u,
    0x7d3u,
    0x7d4u,
    0x7d5u,
    0x7d6u,
    0x7d7u,
    0x7d8u,
    0x7d9u,
    0x7dau,
    0x7dbu,
    0x7dcu,
    0x7ddu,
    0x7deu,
    0x7dfu,
    0x7e0u,
    0x7e1u,
    0x7e2u,
    0x7e3u,
    0x7e4u,
    0x7e5u,
    0x7e6u,
    0x7e7u,
    0x7e8u,
    0x7e9u,
    0x7eau,
    0x7ebu,
    0x7ecu,
    0x7edu,
    0x7eeu,
    0x7efu,
    0x7f0u,
    0x7f1u,
    0x7f2u,
    0x7f3u,
    0x7f4u,
    0x7f5u,
    0x7f6u,
    0x7f7u,
    0x7f8u,
    0x7f9u,
    0x7fau,
    0x7fbu,
    0x7fcu,
    0x7fdu,
    0x7feu,
    0x7ffu,
    0xec0u,
    0xed0u,
    0xec0u,
    0xec2u,
    0xec3u,
    0xec4u,
    0xec5u,
    0xec6u,
    0xec7u,
    0xec8u,
    0xec9u,
    0xecau,
    0xecbu,
    0xeccu,
    0xecdu,
    0xeceu,
    0xecfu,
    0xed0u,
    0xed2u,
    0xed3u,
    0xed4u,
    0xed5u,
    0xed6u,
    0xed7u,
    0xed8u,
    0xed9u,
    0xedau,
    0xedbu,
    0xedcu,
    0xeddu,
    0xedeu,
    0xedfu,
    0xf50u,
    0xf50u,
};

const bedrock_named_value bedrock_condition_names[] = {
    {"T", 0u},
    {"F", 1u},
    {"EQ", 2u},
    {"Z", 2u},
    {"NE", 3u},
    {"NZ", 3u},
    {"ULT", 4u},
    {"C", 4u},
    {"UGE", 5u},
    {"NC", 5u},
    {"MI", 6u},
    {"N", 6u},
    {"PL", 7u},
    {"NN", 7u},
    {"VS", 8u},
    {"V", 8u},
    {"VC", 9u},
    {"NV", 9u},
    {"ULE", 10u},
    {"UGT", 11u},
    {"LT", 12u},
    {"GE", 13u},
    {"LE", 14u},
    {"GT", 15u},
};

const bedrock_named_value bedrock_sreg_names[] = {
    {"CS", 0u},
    {"DS", 1u},
    {"SS", 2u},
    {"GS0", 3u},
    {"GS1", 4u},
    {"GS2", 5u},
    {"GS3", 6u},
    {"GS4", 7u},
};

const bedrock_named_value bedrock_cr_names[] = {
    {"PTCR", 0u},
    {"ASCR", 1u},
    {"ICR", 2u},
    {"SPC", 256u},
    {"SCS", 257u},
    {"SDS", 258u},
    {"SSS0", 512u},
    {"SSP0", 513u},
    {"SSS1", 528u},
    {"SSP1", 529u},
    {"SSS2", 544u},
    {"SSP2", 545u},
    {"SSS3", 560u},
    {"SSP3", 561u},
    {"BOOTPC", 4096u},
    {"BOOTCFG", 4097u},
    {"PTC", 4352u},
    {"PMC", 4353u},
};

const bedrock_named_value bedrock_ea_segment_names[] = {
    {"CS", 0u},
    {"DS", 1u},
    {"GS0", 3u},
    {"GS1", 4u},
    {"GS2", 5u},
    {"GS3", 6u},
    {"GS4", 7u},
    {"SS", 2u},
};

const bedrock_named_value bedrock_memory_order_names[] = {
    {"RELAXED", 0u},
    {"ACQUIRE", 1u},
    {"RELEASE", 2u},
    {"ACQREL", 3u},
    {"SEQCST", 4u},
};

const bedrock_form_desc bedrock_forms[] = {
    {"HALT", "HALT", "HALT", BEDROCK_FORM_COMPACT, "system", "CORE_MISC.HALT", "supervisor", 0x000u, 0x000u, 0x0000u, 0x0000u, 1u, 8u, 1u, 0u, 0u, 0u, 0u, 0u, 0u, "", ""},
    {"CALL.IMM32", "CALL", "CALL imm32", BEDROCK_FORM_COMPACT, "control_flow", "CALL", "unprivileged", 0x001u, 0x001u, 0x0000u, 0x0000u, 3u, 8u, 3u, 0u, 0u, 0u, 1u, 0u, 0u, "", ""},
    {"CALL.IMM64", "CALL", "CALL imm64", BEDROCK_FORM_COMPACT, "control_flow", "CALL", "unprivileged", 0x002u, 0x002u, 0x0000u, 0x0000u, 5u, 8u, 5u, 0u, 0u, 1u, 1u, 0u, 0u, "", ""},
    {"CALL.IMM16", "CALL", "CALL imm16", BEDROCK_FORM_COMPACT, "control_flow", "CALL", "unprivileged", 0x003u, 0x003u, 0x0000u, 0x0000u, 2u, 8u, 2u, 0u, 0u, 2u, 1u, 0u, 0u, "", ""},
    {"BKPT", "BKPT", "BKPT", BEDROCK_FORM_COMPACT, "system", "CORE_MISC.BKPT", "any", 0x004u, 0x004u, 0x0000u, 0x0000u, 1u, 8u, 1u, 0u, 0u, 3u, 0u, 0u, 0u, "", ""},
    {"AFENCE", "AFENCE", "AFENCE", BEDROCK_FORM_COMPACT, "system", "CORE_MISC.AFENCE", "any", 0x005u, 0x005u, 0x0000u, 0x0000u, 1u, 8u, 1u, 0u, 0u, 3u, 0u, 0u, 0u, "", ""},
    {"WFENCE", "WFENCE", "WFENCE", BEDROCK_FORM_COMPACT, "system", "CORE_MISC.WFENCE", "any", 0x006u, 0x006u, 0x0000u, 0x0000u, 1u, 8u, 1u, 0u, 0u, 3u, 0u, 0u, 0u, "", ""},
    {"RFENCE", "RFENCE", "RFENCE", BEDROCK_FORM_COMPACT, "system", "CORE_MISC.RFENCE", "any", 0x007u, 0x007u, 0x0000u, 0x0000u, 1u, 8u, 1u, 0u, 0u, 3u, 0u, 0u, 0u, "", ""},
    {"PUSH.D", "PUSH", "PUSH.D Dn(d)", BEDROCK_FORM_COMPACT, "data_movement", "PUSH_POP.PUSH", "unprivileged", 0x008u, 0x00fu, 0x0000u, 0x0000u, 1u, 8u, 1u, 0u, 1u, 3u, 1u, 0u, 0u, "", ""},
    {"AND.IMM_TO_D", "AND", "AND.X(z:W/L) imm, Dn(d)", BEDROCK_FORM_COMPACT, "integer", "AND_OR.AND", "unprivileged", 0x010u, 0x01fu, 0x0000u, 0x0000u, 2u, 8u, 2u, 1u, 2u, 4u, 2u, 0u, 0u, "", ""},
    {"DEC.D", "DEC", "DEC.X(s:B/W/L/Q) Dn(d)", BEDROCK_FORM_COMPACT, "integer", "INC_DEC.DEC", "unprivileged", 0x020u, 0x03fu, 0x0000u, 0x0000u, 1u, 8u, 1u, 3u, 2u, 6u, 1u, 0u, 0u, "", ""},
    {"EXTSW.D_TO_D", "EXTSW", "EXTSW Dn(d), Dn(D)", BEDROCK_FORM_COMPACT, "integer", "EXTEND_TO_W_SIGNED.EXTSW", "unprivileged", 0x040u, 0x07fu, 0x0000u, 0x0000u, 1u, 8u, 1u, 5u, 2u, 7u, 2u, 0u, 0u, "", ""},
    {"ADD.D_TO_D", "ADD", "ADD.X(z:L/Q) Dn(d), Dn(D)", BEDROCK_FORM_COMPACT, "integer", "ADD_SUB.ADD", "unprivileged", 0x080u, 0x0ffu, 0x0000u, 0x0000u, 1u, 8u, 1u, 7u, 3u, 9u, 2u, 0u, 0u, "", ""},
    {"EXTSQ.D_TO_D", "EXTSQ", "EXTSQ.X(s:B/W/L/invalid) Dn(d), Dn(D)", BEDROCK_FORM_COMPACT, "integer", "EXTEND_TO_Q.EXTSQ", "unprivileged", 0x100u, 0x1bfu, 0x0000u, 0x0000u, 1u, 8u, 1u, 10u, 3u, 11u, 2u, 0u, 192u, "", ""},
    {"INC.D", "INC", "INC.X(s:B/W/L/Q) Dn(d)", BEDROCK_FORM_COMPACT, "integer", "INC_DEC.INC", "unprivileged", 0x1c0u, 0x1dfu, 0x0000u, 0x0000u, 1u, 8u, 1u, 13u, 2u, 13u, 1u, 192u, 0u, "", ""},
    {"ABS.D", "ABS", "ABS.X(s:B/W/L/Q) Dn(d)", BEDROCK_FORM_COMPACT, "integer", "NEG_ABS.ABS", "unprivileged", 0x1e0u, 0x1ffu, 0x0000u, 0x0000u, 1u, 8u, 1u, 15u, 2u, 14u, 1u, 192u, 0u, "", ""},
    {"EXTZQ.D_TO_D", "EXTZQ", "EXTZQ.X(s:B/W/L/invalid) Dn(d), Dn(D)", BEDROCK_FORM_COMPACT, "integer", "EXTEND_TO_Q.EXTZQ", "unprivileged", 0x200u, 0x2bfu, 0x0000u, 0x0000u, 1u, 8u, 1u, 17u, 3u, 15u, 2u, 192u, 192u, "", ""},
    {"DECN.D", "DECN", "DECN.X(s:B/W/L/Q) Dn(d)", BEDROCK_FORM_COMPACT, "integer", "INCN_DECN.DECN", "unprivileged", 0x2c0u, 0x2dfu, 0x0000u, 0x0000u, 1u, 8u, 1u, 20u, 2u, 17u, 1u, 384u, 0u, "", ""},
    {"INCN.D", "INCN", "INCN.X(s:B/W/L/Q) Dn(d)", BEDROCK_FORM_COMPACT, "integer", "INCN_DECN.INCN", "unprivileged", 0x2e0u, 0x2ffu, 0x0000u, 0x0000u, 1u, 8u, 1u, 22u, 2u, 18u, 1u, 384u, 0u, "", ""},
    {"AND.D_TO_D", "AND", "AND.X(z:L/Q) Dn(d), Dn(D)", BEDROCK_FORM_COMPACT, "integer", "AND_OR.AND", "unprivileged", 0x300u, 0x37fu, 0x0000u, 0x0000u, 1u, 8u, 1u, 24u, 3u, 19u, 2u, 384u, 0u, "", ""},
    {"CMP.D_TO_D", "CMP", "CMP.X(z:L/Q) Dn(d), Dn(D)", BEDROCK_FORM_COMPACT, "integer", "CMP", "unprivileged", 0x380u, 0x3ffu, 0x0000u, 0x0000u, 1u, 8u, 1u, 27u, 3u, 21u, 2u, 384u, 0u, "", ""},
    {"ADD.IMM_TO_D", "ADD", "ADD.X(z:W/L) imm, Dn(d)", BEDROCK_FORM_COMPACT, "integer", "ADD_SUB.ADD", "unprivileged", 0x400u, 0x7c0u, 0x0000u, 0x0000u, 2u, 8u, 2u, 30u, 2u, 23u, 2u, 384u, 16u, "", ""},
    {"CMP.IMM_TO_D", "CMP", "CMP.X(z:W/L) imm, Dn(r)", BEDROCK_FORM_COMPACT, "integer", "CMP", "unprivileged", 0x401u, 0x7c1u, 0x0000u, 0x0000u, 2u, 8u, 2u, 32u, 2u, 25u, 2u, 400u, 16u, "", ""},
    {"SUB.IMM_TO_D", "SUB", "SUB.X(z:W/L) imm, Dn(d)", BEDROCK_FORM_COMPACT, "integer", "ADD_SUB.SUB", "unprivileged", 0x402u, 0x7c2u, 0x0000u, 0x0000u, 2u, 8u, 2u, 34u, 2u, 27u, 2u, 416u, 16u, "", ""},
    {"TEST.IMM_TO_D", "TEST", "TEST.X(z:W/L) imm, Dn(r)", BEDROCK_FORM_COMPACT, "integer", "TEST", "unprivileged", 0x403u, 0x7c3u, 0x0000u, 0x0000u, 2u, 8u, 2u, 36u, 2u, 29u, 2u, 432u, 16u, "", ""},
    {"MOV.D_TO_EA", "MOV", "MOV.X(z:L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_COMPACT, "data_movement", "MOV", "unprivileged", 0x408u, 0x7ffu, 0x0000u, 0x0000u, 1u, 8u, 1u, 38u, 3u, 31u, 2u, 448u, 896u, "", ""},
    {"MOV.EA_TO_D", "MOV", "MOV.X(z:L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_COMPACT, "data_movement", "MOV", "unprivileged", 0x800u, 0xbffu, 0x0000u, 0x0000u, 1u, 8u, 1u, 41u, 3u, 33u, 2u, 1344u, 0u, "", ""},
    {"OR.D_TO_D", "OR", "OR.X(z:L/Q) Dn(d), Dn(D)", BEDROCK_FORM_COMPACT, "integer", "AND_OR.OR", "unprivileged", 0xc00u, 0xc7fu, 0x0000u, 0x0000u, 1u, 8u, 1u, 44u, 3u, 35u, 2u, 1344u, 0u, "", ""},
    {"SUB.D_TO_D", "SUB", "SUB.X(z:L/Q) Dn(d), Dn(D)", BEDROCK_FORM_COMPACT, "integer", "ADD_SUB.SUB", "unprivileged", 0xc80u, 0xcffu, 0x0000u, 0x0000u, 1u, 8u, 1u, 47u, 3u, 37u, 2u, 1344u, 0u, "", ""},
    {"TEST.D_TO_D", "TEST", "TEST.X(z:L/Q) Dn(d), Dn(D)", BEDROCK_FORM_COMPACT, "integer", "TEST", "unprivileged", 0xd00u, 0xd7fu, 0x0000u, 0x0000u, 1u, 8u, 1u, 50u, 3u, 39u, 2u, 1344u, 0u, "", ""},
    {"XOR.D_TO_D", "XOR", "XOR.X(z:L/Q) Dn(d), Dn(D)", BEDROCK_FORM_COMPACT, "integer", "XOR", "unprivileged", 0xd80u, 0xdffu, 0x0000u, 0x0000u, 1u, 8u, 1u, 53u, 3u, 41u, 2u, 1344u, 0u, "", ""},
    {"EXTZL.D_TO_D", "EXTZL", "EXTZL.X(s:B/W) Dn(d), Dn(D)", BEDROCK_FORM_COMPACT, "integer", "EXTEND_TO_L.EXTZL", "unprivileged", 0xe00u, 0xe7fu, 0x0000u, 0x0000u, 1u, 8u, 1u, 56u, 3u, 43u, 2u, 1344u, 0u, "", ""},
    {"NEG.D", "NEG", "NEG.X(s:B/W/L/Q) Dn(d)", BEDROCK_FORM_COMPACT, "integer", "NEG_ABS.NEG", "unprivileged", 0xe80u, 0xe9fu, 0x0000u, 0x0000u, 1u, 8u, 1u, 59u, 2u, 45u, 1u, 1344u, 0u, "", ""},
    {"NOT.D", "NOT", "NOT.X(s:B/W/L/Q) Dn(d)", BEDROCK_FORM_COMPACT, "integer", "NOT", "unprivileged", 0xea0u, 0xebfu, 0x0000u, 0x0000u, 1u, 8u, 1u, 61u, 2u, 46u, 1u, 1344u, 0u, "", ""},
    {"JMP.IMM", "JMP", "JMP.X(z:W/L) imm", BEDROCK_FORM_COMPACT_ALIAS, "control_flow", "Jcc", "unprivileged", 0xec0u, 0xed0u, 0x0000u, 0x0000u, 2u, 8u, 2u, 63u, 1u, 47u, 1u, 1344u, 2u, "Jcc.IMM", "T"},
    {"Jcc.IMM", "Jcc", "Jcc.X(z:W/L) imm", BEDROCK_FORM_COMPACT, "control_flow", "Jcc", "unprivileged", 0xec0u, 0xedfu, 0x0000u, 0x0000u, 2u, 8u, 2u, 64u, 2u, 48u, 1u, 1346u, 30u, "", ""},
    {"SYSCALL", "SYSCALL", "SYSCALL", BEDROCK_FORM_COMPACT, "system", "CORE_MISC.SYSCALL", "any", 0xec1u, 0xec1u, 0x0000u, 0x0000u, 1u, 8u, 1u, 66u, 0u, 49u, 0u, 1376u, 0u, "", ""},
    {"WAIT", "WAIT", "WAIT", BEDROCK_FORM_COMPACT, "system", "CORE_MISC.WAIT", "policy_controlled", 0xed1u, 0xed1u, 0x0000u, 0x0000u, 1u, 8u, 1u, 66u, 0u, 49u, 0u, 1376u, 0u, "", ""},
    {"OR.IMM_TO_D", "OR", "OR.X(z:W/L) imm, Dn(d)", BEDROCK_FORM_COMPACT, "integer", "AND_OR.OR", "unprivileged", 0xee0u, 0xeefu, 0x0000u, 0x0000u, 2u, 8u, 2u, 66u, 2u, 49u, 2u, 1376u, 0u, "", ""},
    {"XOR.IMM_TO_D", "XOR", "XOR.X(z:W/L) imm, Dn(d)", BEDROCK_FORM_COMPACT, "integer", "XOR", "unprivileged", 0xef0u, 0xeffu, 0x0000u, 0x0000u, 2u, 8u, 2u, 68u, 2u, 51u, 2u, 1376u, 0u, "", ""},
    {"PUSH.A", "PUSH", "PUSH An(a)", BEDROCK_FORM_COMPACT, "data_movement", "PUSH_POP.PUSH", "unprivileged", 0xf00u, 0xf07u, 0x0000u, 0x0000u, 1u, 8u, 1u, 70u, 1u, 53u, 1u, 1376u, 0u, "", ""},
    {"POP.D", "POP", "POP.D Dn(d)", BEDROCK_FORM_COMPACT, "data_movement", "PUSH_POP.POP", "unprivileged", 0xf08u, 0xf0fu, 0x0000u, 0x0000u, 1u, 8u, 1u, 71u, 1u, 54u, 1u, 1376u, 0u, "", ""},
    {"POP.A", "POP", "POP An(a)", BEDROCK_FORM_COMPACT, "data_movement", "PUSH_POP.POP", "unprivileged", 0xf10u, 0xf17u, 0x0000u, 0x0000u, 1u, 8u, 1u, 72u, 1u, 55u, 1u, 1376u, 0u, "", ""},
    {"CLR.A", "CLR", "CLR An(a)", BEDROCK_FORM_COMPACT, "integer", "CLR", "unprivileged", 0xf18u, 0xf1fu, 0x0000u, 0x0000u, 1u, 8u, 1u, 73u, 1u, 56u, 1u, 1376u, 0u, "", ""},
    {"CLR.D", "CLR", "CLR.D Dn(d)", BEDROCK_FORM_COMPACT, "integer", "CLR", "unprivileged", 0xf20u, 0xf27u, 0x0000u, 0x0000u, 1u, 8u, 1u, 74u, 1u, 57u, 1u, 1376u, 0u, "", ""},
    {"MOV.IMM_TO_A", "MOV", "MOV imm64, An(a)", BEDROCK_FORM_COMPACT, "data_movement", "MOV", "unprivileged", 0xf28u, 0xf2fu, 0x0000u, 0x0000u, 5u, 8u, 5u, 75u, 1u, 58u, 2u, 1376u, 0u, "", ""},
    {"RET", "RET", "RET", BEDROCK_FORM_COMPACT, "control_flow", "RET", "unprivileged", 0xf30u, 0xf30u, 0x0000u, 0x0000u, 1u, 8u, 1u, 76u, 0u, 60u, 0u, 1376u, 0u, "", ""},
    {"YIELD", "YIELD", "YIELD", BEDROCK_FORM_COMPACT, "system", "CORE_MISC.YIELD", "any", 0xf31u, 0xf31u, 0x0000u, 0x0000u, 1u, 8u, 1u, 76u, 0u, 60u, 0u, 1376u, 0u, "", ""},
    {"PUSHM.BITMAP", "PUSHM", "PUSHM <bitmap>", BEDROCK_FORM_COMPACT, "data_movement", "PUSHM_POPM.PUSHM", "unprivileged", 0xf32u, 0xf32u, 0x0000u, 0x0000u, 2u, 8u, 2u, 76u, 0u, 60u, 1u, 1376u, 0u, "", ""},
    {"POPM.BITMAP", "POPM", "POPM <bitmap>", BEDROCK_FORM_COMPACT, "data_movement", "PUSHM_POPM.POPM", "unprivileged", 0xf33u, 0xf33u, 0x0000u, 0x0000u, 2u, 8u, 2u, 76u, 0u, 61u, 1u, 1376u, 0u, "", ""},
    {"MOVSETAD.BITMAP", "MOVSETAD", "MOVSETAD <bitmap>", BEDROCK_FORM_COMPACT, "data_movement", "MOVSETAD", "unprivileged", 0xf34u, 0xf34u, 0x0000u, 0x0000u, 2u, 8u, 2u, 76u, 0u, 62u, 1u, 1376u, 0u, "", ""},
    {"MOVSETDA.BITMAP", "MOVSETDA", "MOVSETDA <bitmap>", BEDROCK_FORM_COMPACT, "data_movement", "MOVSETDA", "unprivileged", 0xf35u, 0xf35u, 0x0000u, 0x0000u, 2u, 8u, 2u, 76u, 0u, 63u, 1u, 1376u, 0u, "", ""},
    {"XCHGSETAD.BITMAP", "XCHGSETAD", "XCHGSETAD <bitmap>", BEDROCK_FORM_COMPACT, "data_movement", "XCHGSETAD", "unprivileged", 0xf36u, 0xf36u, 0x0000u, 0x0000u, 2u, 8u, 2u, 76u, 0u, 64u, 1u, 1376u, 0u, "", ""},
    {"XCHGSETDA.BITMAP", "XCHGSETDA", "XCHGSETDA <bitmap>", BEDROCK_FORM_COMPACT, "data_movement", "XCHGSETDA", "unprivileged", 0xf37u, 0xf37u, 0x0000u, 0x0000u, 2u, 8u, 2u, 76u, 0u, 65u, 1u, 1376u, 0u, "", ""},
    {"RESET", "RESET", "RESET", BEDROCK_FORM_COMPACT, "system", "RESET", "supervisor", 0xf38u, 0xf38u, 0x0000u, 0x0000u, 1u, 8u, 1u, 76u, 0u, 66u, 0u, 1376u, 0u, "", ""},
    {"SYSRET", "SYSRET", "SYSRET", BEDROCK_FORM_COMPACT, "system", "SYSRET", "supervisor", 0xf39u, 0xf39u, 0x0000u, 0x0000u, 1u, 8u, 1u, 76u, 0u, 66u, 0u, 1376u, 0u, "", ""},
    {"IRET", "IRET", "IRET", BEDROCK_FORM_COMPACT, "system", "IRET", "supervisor", 0xf3au, 0xf3au, 0x0000u, 0x0000u, 1u, 8u, 1u, 76u, 0u, 66u, 0u, 1376u, 0u, "", ""},
    {"TRACE.IMM", "TRACE", "TRACE imm16", BEDROCK_FORM_COMPACT, "control_flow", "TRACE", "unprivileged", 0xf3bu, 0xf3bu, 0x0000u, 0x0000u, 2u, 8u, 2u, 76u, 0u, 66u, 1u, 1376u, 0u, "", ""},
    {"ABS.EA", "ABS", "ABS.X(s:B/W/L/Q) <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "NEG_ABS.ABS.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x0000u, 0x00ffu, 2u, 8u, 2u, 76u, 2u, 67u, 1u, 1376u, 0u, "", ""},
    {"CLR.EA", "CLR", "CLR <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "CLR.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x0100u, 0x013fu, 2u, 8u, 2u, 78u, 1u, 68u, 1u, 1376u, 0u, "", ""},
    {"SUM.BITMAP_TO_A", "SUM", "SUM.X(s:B/W/L/Q) <bitmap>, An(a)", BEDROCK_FORM_EXTENDED, "integer", "SUM", "unprivileged", 0xf3cu, 0xf3cu, 0x0140u, 0x015fu, 3u, 8u, 3u, 79u, 3u, 69u, 2u, 1376u, 0u, "", ""},
    {"SUM.BITMAP_TO_D", "SUM", "SUM.X(s:B/W/L/Q) <bitmap>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "SUM", "unprivileged", 0xf3cu, 0xf3cu, 0x0160u, 0x017fu, 3u, 8u, 3u, 82u, 3u, 71u, 2u, 1376u, 0u, "", ""},
    {"EXTSL.D_TO_D", "EXTSL", "EXTSL.X(s:B/W) Dn(d), Dn(D)", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_L.EXTSL", "unprivileged", 0xf3cu, 0xf3cu, 0x0180u, 0x01ffu, 2u, 8u, 2u, 85u, 3u, 73u, 2u, 1376u, 0u, "", ""},
    {"ADD.EA_TO_A", "ADD", "ADD <ea(e)>, An(a)", BEDROCK_FORM_EXTENDED, "integer", "ADD_SUB.ADD.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x0200u, 0x03ffu, 2u, 8u, 2u, 88u, 2u, 75u, 2u, 1376u, 0u, "", ""},
    {"CMP.EA_TO_A", "CMP", "CMP <ea(e)>, An(r)", BEDROCK_FORM_EXTENDED, "integer", "CMP.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x0400u, 0x05ffu, 2u, 8u, 2u, 90u, 2u, 77u, 2u, 1376u, 0u, "", ""},
    {"DEC.EA", "DEC", "DEC.X(s:B/W/L/Q) <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "INC_DEC.DEC.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x0600u, 0x06ffu, 2u, 8u, 2u, 92u, 2u, 79u, 1u, 1376u, 0u, "", ""},
    {"DECN.EA", "DECN", "DECN.X(s:B/W/L/Q) <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "INCN_DECN.DECN.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x0700u, 0x07ffu, 2u, 8u, 2u, 94u, 2u, 80u, 1u, 1376u, 0u, "", ""},
    {"AND.EA_TO_D", "AND", "AND.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "AND_OR.AND.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x0800u, 0x0fffu, 2u, 8u, 2u, 96u, 3u, 81u, 2u, 1376u, 0u, "", ""},
    {"CMP.D_TO_EA", "CMP", "CMP.X(s:B/W/L/Q) Dn(l), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "CMP.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x1000u, 0x17ffu, 2u, 8u, 2u, 99u, 3u, 83u, 2u, 1376u, 0u, "", ""},
    {"CMP.EA_TO_D", "CMP", "CMP.X(s:B/W/L/Q) <ea(e)>, Dn(r)", BEDROCK_FORM_EXTENDED, "integer", "CMP.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x1800u, 0x1fffu, 2u, 8u, 2u, 102u, 3u, 85u, 2u, 1376u, 0u, "", ""},
    {"EXTSL.D_TO_EA", "EXTSL", "EXTSL.X(s:B/W) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_L.EXTSL.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x2000u, 0x23ffu, 2u, 8u, 2u, 105u, 3u, 87u, 2u, 1376u, 0u, "", ""},
    {"EXTSL.EA_TO_D", "EXTSL", "EXTSL.X(s:B/W) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_L.EXTSL.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x2400u, 0x27ffu, 2u, 8u, 2u, 108u, 3u, 89u, 2u, 1376u, 0u, "", ""},
    {"EXTSQ.D_TO_EA", "EXTSQ", "EXTSQ.X(s:B/W/L/invalid) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_Q.EXTSQ.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x2800u, 0x2fffu, 2u, 8u, 2u, 111u, 3u, 91u, 2u, 1376u, 0u, "", ""},
    {"EXTSQ.EA_TO_D", "EXTSQ", "EXTSQ.X(s:B/W/L/invalid) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_Q.EXTSQ.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x3000u, 0x37ffu, 2u, 8u, 2u, 114u, 3u, 93u, 2u, 1376u, 0u, "", ""},
    {"EXTSW.D_TO_EA", "EXTSW", "EXTSW Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_W_SIGNED.EXTSW.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x3800u, 0x39ffu, 2u, 8u, 2u, 117u, 2u, 95u, 2u, 1376u, 0u, "", ""},
    {"EXTSW.EA_TO_D", "EXTSW", "EXTSW <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_W_SIGNED.EXTSW.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x3a00u, 0x3bffu, 2u, 8u, 2u, 119u, 2u, 97u, 2u, 1376u, 0u, "", ""},
    {"EXTZL.D_TO_EA", "EXTZL", "EXTZL.X(s:B/W) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_L.EXTZL.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x3c00u, 0x3fffu, 2u, 8u, 2u, 121u, 3u, 99u, 2u, 1376u, 0u, "", ""},
    {"EXTZL.EA_TO_D", "EXTZL", "EXTZL.X(s:B/W) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_L.EXTZL.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x4000u, 0x43ffu, 2u, 8u, 2u, 124u, 3u, 101u, 2u, 1376u, 0u, "", ""},
    {"INC.EA", "INC", "INC.X(s:B/W/L/Q) <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "INC_DEC.INC.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x4400u, 0x44ffu, 2u, 8u, 2u, 127u, 2u, 103u, 1u, 1376u, 0u, "", ""},
    {"INCN.EA", "INCN", "INCN.X(s:B/W/L/Q) <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "INCN_DECN.INCN.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x4500u, 0x45ffu, 2u, 8u, 2u, 129u, 2u, 104u, 1u, 1376u, 0u, "", ""},
    {"NEG.EA", "NEG", "NEG.X(s:B/W/L/Q) <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "NEG_ABS.NEG.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x4600u, 0x46ffu, 2u, 8u, 2u, 131u, 2u, 105u, 1u, 1376u, 0u, "", ""},
    {"NOT.EA", "NOT", "NOT.X(s:B/W/L/Q) <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "NOT.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x4700u, 0x47ffu, 2u, 8u, 2u, 133u, 2u, 106u, 1u, 1376u, 0u, "", ""},
    {"EXTZQ.D_TO_EA", "EXTZQ", "EXTZQ.X(s:B/W/L/invalid) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_Q.EXTZQ.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x4800u, 0x4fffu, 2u, 8u, 2u, 135u, 3u, 107u, 2u, 1376u, 0u, "", ""},
    {"EXTZQ.EA_TO_D", "EXTZQ", "EXTZQ.X(s:B/W/L/invalid) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_Q.EXTZQ.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x5000u, 0x57ffu, 2u, 8u, 2u, 138u, 3u, 109u, 2u, 1376u, 0u, "", ""},
    {"MAXS.D_TO_EA", "MAXS", "MAXS.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "MIN_MAX.MAXS", "unprivileged", 0xf3cu, 0xf3cu, 0x5800u, 0x5fffu, 2u, 8u, 2u, 141u, 3u, 111u, 2u, 1376u, 0u, "", ""},
    {"MAXS.EA_TO_D", "MAXS", "MAXS.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "MIN_MAX.MAXS", "unprivileged", 0xf3cu, 0xf3cu, 0x6000u, 0x67ffu, 2u, 8u, 2u, 144u, 3u, 113u, 2u, 1376u, 0u, "", ""},
    {"MAXU.D_TO_EA", "MAXU", "MAXU.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "MIN_MAX.MAXU", "unprivileged", 0xf3cu, 0xf3cu, 0x6800u, 0x6fffu, 2u, 8u, 2u, 147u, 3u, 115u, 2u, 1376u, 0u, "", ""},
    {"MAXU.EA_TO_D", "MAXU", "MAXU.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "MIN_MAX.MAXU", "unprivileged", 0xf3cu, 0xf3cu, 0x7000u, 0x77ffu, 2u, 8u, 2u, 150u, 3u, 117u, 2u, 1376u, 0u, "", ""},
    {"MINS.D_TO_EA", "MINS", "MINS.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "MIN_MAX.MINS", "unprivileged", 0xf3cu, 0xf3cu, 0x7800u, 0x7fffu, 2u, 8u, 2u, 153u, 3u, 119u, 2u, 1376u, 0u, "", ""},
    {"MINS.EA_TO_D", "MINS", "MINS.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "MIN_MAX.MINS", "unprivileged", 0xf3cu, 0xf3cu, 0x8000u, 0x87ffu, 2u, 8u, 2u, 156u, 3u, 121u, 2u, 1376u, 0u, "", ""},
    {"MINU.D_TO_EA", "MINU", "MINU.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "MIN_MAX.MINU", "unprivileged", 0xf3cu, 0xf3cu, 0x8800u, 0x8fffu, 2u, 8u, 2u, 159u, 3u, 123u, 2u, 1376u, 0u, "", ""},
    {"MINU.EA_TO_D", "MINU", "MINU.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "MIN_MAX.MINU", "unprivileged", 0xf3cu, 0xf3cu, 0x9000u, 0x97ffu, 2u, 8u, 2u, 162u, 3u, 125u, 2u, 1376u, 0u, "", ""},
    {"OR.D_TO_EA", "OR", "OR.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "AND_OR.OR.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0x9800u, 0x9fffu, 2u, 8u, 2u, 165u, 3u, 127u, 2u, 1376u, 0u, "", ""},
    {"OR.EA_TO_D", "OR", "OR.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "AND_OR.OR.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0xa000u, 0xa7ffu, 2u, 8u, 2u, 168u, 3u, 129u, 2u, 1376u, 0u, "", ""},
    {"REVBYTE.D_TO_D", "REVBYTE", "REVBYTE.X(s:B/W/L/Q) Dn(d), Dn(D)", BEDROCK_FORM_EXTENDED, "integer", "REV.REVBYTE", "unprivileged", 0xf3cu, 0xf3cu, 0xa800u, 0xa8ffu, 2u, 8u, 2u, 171u, 3u, 131u, 2u, 1376u, 0u, "", ""},
    {"SUB.EA_TO_A", "SUB", "SUB <ea(e)>, An(a)", BEDROCK_FORM_EXTENDED, "integer", "ADD_SUB.SUB.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0xaa00u, 0xabffu, 2u, 8u, 2u, 174u, 2u, 133u, 2u, 1376u, 0u, "", ""},
    {"REVBYTE.D_TO_EA", "REVBYTE", "REVBYTE.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "REV.REVBYTE", "unprivileged", 0xf3cu, 0xf3cu, 0xb000u, 0xb7ffu, 2u, 8u, 2u, 176u, 3u, 135u, 2u, 1376u, 0u, "", ""},
    {"REVBYTE.EA_TO_D", "REVBYTE", "REVBYTE.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "REV.REVBYTE", "unprivileged", 0xf3cu, 0xf3cu, 0xb800u, 0xbfffu, 2u, 8u, 2u, 179u, 3u, 137u, 2u, 1376u, 0u, "", ""},
    {"SBB.D_TO_EA", "SBB", "SBB.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ADC_SBB.SBB", "unprivileged", 0xf3cu, 0xf3cu, 0xc000u, 0xc7ffu, 2u, 8u, 2u, 182u, 3u, 139u, 2u, 1376u, 0u, "", ""},
    {"SBB.EA_TO_D", "SBB", "SBB.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "ADC_SBB.SBB", "unprivileged", 0xf3cu, 0xf3cu, 0xc800u, 0xcfffu, 2u, 8u, 2u, 185u, 3u, 141u, 2u, 1376u, 0u, "", ""},
    {"SUB.D_TO_EA", "SUB", "SUB.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ADD_SUB.SUB.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0xd000u, 0xd7ffu, 2u, 8u, 2u, 188u, 3u, 143u, 2u, 1376u, 0u, "", ""},
    {"SUB.EA_TO_D", "SUB", "SUB.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "ADD_SUB.SUB.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0xd800u, 0xdfffu, 2u, 8u, 2u, 191u, 3u, 145u, 2u, 1376u, 0u, "", ""},
    {"TEST.D_TO_EA", "TEST", "TEST.X(s:B/W/L/Q) Dn(l), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "TEST.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0xe000u, 0xe7ffu, 2u, 8u, 2u, 194u, 3u, 147u, 2u, 1376u, 0u, "", ""},
    {"TEST.EA_TO_D", "TEST", "TEST.X(s:B/W/L/Q) <ea(e)>, Dn(r)", BEDROCK_FORM_EXTENDED, "integer", "TEST.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0xe800u, 0xefffu, 2u, 8u, 2u, 197u, 3u, 149u, 2u, 1376u, 0u, "", ""},
    {"XOR.D_TO_EA", "XOR", "XOR.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "XOR.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0xf000u, 0xf7ffu, 2u, 8u, 2u, 200u, 3u, 151u, 2u, 1376u, 0u, "", ""},
    {"XOR.EA_TO_D", "XOR", "XOR.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "XOR.extended_forms", "unprivileged", 0xf3cu, 0xf3cu, 0xf800u, 0xffffu, 2u, 8u, 2u, 203u, 3u, 153u, 2u, 1376u, 0u, "", ""},
    {"ADC.D_TO_EA", "ADC", "ADC.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ADC_SBB.ADC", "unprivileged", 0xf3du, 0xf3du, 0x0000u, 0x07ffu, 2u, 8u, 2u, 206u, 3u, 155u, 2u, 1376u, 0u, "", ""},
    {"ADC.EA_TO_D", "ADC", "ADC.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "ADC_SBB.ADC", "unprivileged", 0xf3du, 0xf3du, 0x0800u, 0x0fffu, 2u, 8u, 2u, 209u, 3u, 157u, 2u, 1376u, 0u, "", ""},
    {"ADD.D_TO_EA", "ADD", "ADD.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ADD_SUB.ADD.extended_forms", "unprivileged", 0xf3du, 0xf3du, 0x1000u, 0x17ffu, 2u, 8u, 2u, 212u, 3u, 159u, 2u, 1376u, 0u, "", ""},
    {"ADD.EA_TO_D", "ADD", "ADD.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "ADD_SUB.ADD.extended_forms", "unprivileged", 0xf3du, 0xf3du, 0x1800u, 0x1fffu, 2u, 8u, 2u, 215u, 3u, 161u, 2u, 1376u, 0u, "", ""},
    {"AND.D_TO_EA", "AND", "AND.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "AND_OR.AND.extended_forms", "unprivileged", 0xf3du, 0xf3du, 0x2000u, 0x27ffu, 2u, 8u, 2u, 218u, 3u, 163u, 2u, 1376u, 0u, "", ""},
    {"ADC.IMM_TO_EA", "ADC", "ADC.X(s:B/W/L/Q) <imm(i)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ADC_SBB.ADC", "unprivileged", 0xf3eu, 0xf3eu, 0x0000u, 0x3fffu, 2u, 8u, 2u, 221u, 3u, 165u, 2u, 1376u, 0u, "", ""},
    {"ADD.IMM_TO_EA", "ADD", "ADD.X(s:B/W/L/Q) <imm(i)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ADD_SUB.ADD.extended_forms", "unprivileged", 0xf3eu, 0xf3eu, 0x4000u, 0x7fffu, 2u, 8u, 2u, 224u, 3u, 167u, 2u, 1376u, 0u, "", ""},
    {"SBB.IMM_TO_EA", "SBB", "SBB.X(s:B/W/L/Q) <imm(i)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ADC_SBB.SBB", "unprivileged", 0xf3eu, 0xf3eu, 0x8000u, 0xbfffu, 2u, 8u, 2u, 227u, 3u, 169u, 2u, 1376u, 0u, "", ""},
    {"SUB.IMM_TO_EA", "SUB", "SUB.X(s:B/W/L/Q) <imm(i)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ADD_SUB.SUB.extended_forms", "unprivileged", 0xf3eu, 0xf3eu, 0xc000u, 0xffffu, 2u, 8u, 2u, 230u, 3u, 171u, 2u, 1376u, 0u, "", ""},
    {"AND.IMM_TO_EA", "AND", "AND.X(s:B/W/L/Q) <imm(i)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "AND_OR.AND.extended_forms", "unprivileged", 0xf3fu, 0xf3fu, 0x0000u, 0x3fffu, 2u, 8u, 2u, 233u, 3u, 173u, 2u, 1376u, 0u, "", ""},
    {"OR.IMM_TO_EA", "OR", "OR.X(s:B/W/L/Q) <imm(i)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "AND_OR.OR.extended_forms", "unprivileged", 0xf3fu, 0xf3fu, 0x4000u, 0x7fffu, 2u, 8u, 2u, 236u, 3u, 175u, 2u, 1376u, 0u, "", ""},
    {"TEST.IMM_TO_EA", "TEST", "TEST.X(s:B/W/L/Q) <imm(i)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "TEST.extended_forms", "unprivileged", 0xf3fu, 0xf3fu, 0x8000u, 0xbfffu, 2u, 8u, 2u, 239u, 3u, 177u, 2u, 1376u, 0u, "", ""},
    {"XOR.IMM_TO_EA", "XOR", "XOR.X(s:B/W/L/Q) <imm(i)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "XOR.extended_forms", "unprivileged", 0xf3fu, 0xf3fu, 0xc000u, 0xffffu, 2u, 8u, 2u, 242u, 3u, 179u, 2u, 1376u, 0u, "", ""},
    {"CMP.EA_TO_EA", "CMP", "CMP.X(s:B/W/L/Q) <ea(e)>, <ea(E)>", BEDROCK_FORM_EXTENDED, "integer", "CMP.extended_forms", "unprivileged", 0xf40u, 0xf40u, 0x0000u, 0x3fffu, 2u, 8u, 2u, 245u, 3u, 181u, 2u, 1376u, 0u, "", ""},
    {"CMP.IMM_TO_EA", "CMP", "CMP.X(s:B/W/L/Q) <imm(i)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "CMP.extended_forms", "unprivileged", 0xf40u, 0xf40u, 0x4000u, 0x7fffu, 2u, 8u, 2u, 248u, 3u, 183u, 2u, 1376u, 0u, "", ""},
    {"EXTSL.EA_TO_EA", "EXTSL", "EXTSL.X(s:B/W) <ea(e)>, <ea(E)>", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_L.EXTSL.extended_forms", "unprivileged", 0xf41u, 0xf41u, 0x0000u, 0x1fffu, 2u, 8u, 2u, 251u, 3u, 185u, 2u, 1376u, 0u, "", ""},
    {"EXTSW.EA_TO_EA", "EXTSW", "EXTSW <ea(e)>, <ea(E)>", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_W_SIGNED.EXTSW.extended_forms", "unprivileged", 0xf41u, 0xf41u, 0x2000u, 0x2fffu, 2u, 8u, 2u, 254u, 2u, 187u, 2u, 1376u, 0u, "", ""},
    {"EXTZW.EA_TO_EA", "EXTZW", "EXTZW <ea(e)>, <ea(E)>", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_W_ZERO.EXTZW", "unprivileged", 0xf41u, 0xf41u, 0x3000u, 0x3fffu, 2u, 8u, 2u, 256u, 2u, 189u, 2u, 1376u, 0u, "", ""},
    {"EXTSQ.EA_TO_EA", "EXTSQ", "EXTSQ.X(s:B/W/L/invalid) <ea(e)>, <ea(E)>", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_Q.EXTSQ.extended_forms", "unprivileged", 0xf41u, 0xf41u, 0x4000u, 0x7fffu, 2u, 8u, 2u, 258u, 3u, 191u, 2u, 1376u, 0u, "", ""},
    {"EXTZL.EA_TO_EA", "EXTZL", "EXTZL.X(s:B/W) <ea(e)>, <ea(E)>", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_L.EXTZL.extended_forms", "unprivileged", 0xf41u, 0xf41u, 0x8000u, 0x9fffu, 2u, 8u, 2u, 261u, 3u, 193u, 2u, 1376u, 0u, "", ""},
    {"EXTZQ.EA_TO_EA", "EXTZQ", "EXTZQ.X(s:B/W/L/invalid) <ea(e)>, <ea(E)>", BEDROCK_FORM_EXTENDED, "integer", "EXTEND_TO_Q.EXTZQ.extended_forms", "unprivileged", 0xf41u, 0xf41u, 0xc000u, 0xffffu, 2u, 8u, 2u, 264u, 3u, 195u, 2u, 1376u, 0u, "", ""},
    {"BNDSII.D_TO_EA_TO_D", "BNDSII", "BNDSII.X(s:B/W/L/Q) Dn(l), <ea(e)>, Dn(h)", BEDROCK_FORM_EXTENDED, "integer", "BOUNDS_SIGNED.BNDSII", "unprivileged", 0xf42u, 0xf42u, 0x0000u, 0x3fffu, 2u, 8u, 2u, 267u, 4u, 197u, 3u, 1376u, 0u, "", ""},
    {"BNDSIX.D_TO_EA_TO_D", "BNDSIX", "BNDSIX.X(s:B/W/L/Q) Dn(l), <ea(e)>, Dn(h)", BEDROCK_FORM_EXTENDED, "integer", "BOUNDS_SIGNED.BNDSIX", "unprivileged", 0xf42u, 0xf42u, 0x4000u, 0x7fffu, 2u, 8u, 2u, 271u, 4u, 200u, 3u, 1376u, 0u, "", ""},
    {"BNDSXI.D_TO_EA_TO_D", "BNDSXI", "BNDSXI.X(s:B/W/L/Q) Dn(l), <ea(e)>, Dn(h)", BEDROCK_FORM_EXTENDED, "integer", "BOUNDS_SIGNED.BNDSXI", "unprivileged", 0xf42u, 0xf42u, 0x8000u, 0xbfffu, 2u, 8u, 2u, 275u, 4u, 203u, 3u, 1376u, 0u, "", ""},
    {"BNDSXX.D_TO_EA_TO_D", "BNDSXX", "BNDSXX.X(s:B/W/L/Q) Dn(l), <ea(e)>, Dn(h)", BEDROCK_FORM_EXTENDED, "integer", "BOUNDS_SIGNED.BNDSXX", "unprivileged", 0xf42u, 0xf42u, 0xc000u, 0xffffu, 2u, 8u, 2u, 279u, 4u, 206u, 3u, 1376u, 0u, "", ""},
    {"BNDUII.D_TO_EA_TO_D", "BNDUII", "BNDUII.X(s:B/W/L/Q) Dn(l), <ea(e)>, Dn(h)", BEDROCK_FORM_EXTENDED, "integer", "BOUNDS_UNSIGNED.BNDUII", "unprivileged", 0xf43u, 0xf43u, 0x0000u, 0x3fffu, 2u, 8u, 2u, 283u, 4u, 209u, 3u, 1376u, 0u, "", ""},
    {"BNDUIX.D_TO_EA_TO_D", "BNDUIX", "BNDUIX.X(s:B/W/L/Q) Dn(l), <ea(e)>, Dn(h)", BEDROCK_FORM_EXTENDED, "integer", "BOUNDS_UNSIGNED.BNDUIX", "unprivileged", 0xf43u, 0xf43u, 0x4000u, 0x7fffu, 2u, 8u, 2u, 287u, 4u, 212u, 3u, 1376u, 0u, "", ""},
    {"BNDUXI.D_TO_EA_TO_D", "BNDUXI", "BNDUXI.X(s:B/W/L/Q) Dn(l), <ea(e)>, Dn(h)", BEDROCK_FORM_EXTENDED, "integer", "BOUNDS_UNSIGNED.BNDUXI", "unprivileged", 0xf43u, 0xf43u, 0x8000u, 0xbfffu, 2u, 8u, 2u, 291u, 4u, 215u, 3u, 1376u, 0u, "", ""},
    {"BNDUXX.D_TO_EA_TO_D", "BNDUXX", "BNDUXX.X(s:B/W/L/Q) Dn(l), <ea(e)>, Dn(h)", BEDROCK_FORM_EXTENDED, "integer", "BOUNDS_UNSIGNED.BNDUXX", "unprivileged", 0xf43u, 0xf43u, 0xc000u, 0xffffu, 2u, 8u, 2u, 295u, 4u, 218u, 3u, 1376u, 0u, "", ""},
    {"CLMUL.D_TO_EA", "CLMUL", "CLMUL.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "CARRYLESS_MULTIPLY.CLMUL", "unprivileged", 0xf44u, 0xf44u, 0x0000u, 0x07ffu, 2u, 8u, 2u, 299u, 3u, 221u, 2u, 1376u, 0u, "", ""},
    {"CLMUL.EA_TO_D", "CLMUL", "CLMUL.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "CARRYLESS_MULTIPLY.CLMUL", "unprivileged", 0xf44u, 0xf44u, 0x0800u, 0x0fffu, 2u, 8u, 2u, 302u, 3u, 223u, 2u, 1376u, 0u, "", ""},
    {"CLMULH.D_TO_EA", "CLMULH", "CLMULH.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "CARRYLESS_MULTIPLY.CLMULH", "unprivileged", 0xf44u, 0xf44u, 0x1000u, 0x17ffu, 2u, 8u, 2u, 305u, 3u, 225u, 2u, 1376u, 0u, "", ""},
    {"CLMULH.EA_TO_D", "CLMULH", "CLMULH.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "CARRYLESS_MULTIPLY.CLMULH", "unprivileged", 0xf44u, 0xf44u, 0x1800u, 0x1fffu, 2u, 8u, 2u, 308u, 3u, 227u, 2u, 1376u, 0u, "", ""},
    {"DIVMODS.EA_TO_D_TO_D", "DIVMODS", "DIVMODS.X(s:B/W/L/Q) <ea(e)>, Dn(q), Dn(r)", BEDROCK_FORM_EXTENDED, "integer", "DIVMOD.DIVMODS", "unprivileged", 0xf44u, 0xf44u, 0x2000u, 0x2000u, 3u, 8u, 3u, 311u, 4u, 229u, 3u, 1376u, 0u, "", ""},
    {"DIVS.D_TO_EA", "DIVS", "DIVS.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "DIVIDE_MOD.DIVS", "unprivileged", 0xf44u, 0xf44u, 0x2800u, 0x2fffu, 2u, 8u, 2u, 315u, 3u, 232u, 2u, 1376u, 0u, "", ""},
    {"DIVS.EA_TO_D", "DIVS", "DIVS.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "DIVIDE_MOD.DIVS", "unprivileged", 0xf44u, 0xf44u, 0x3000u, 0x37ffu, 2u, 8u, 2u, 318u, 3u, 234u, 2u, 1376u, 0u, "", ""},
    {"DIVU.D_TO_EA", "DIVU", "DIVU.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "DIVIDE_MOD.DIVU", "unprivileged", 0xf44u, 0xf44u, 0x3800u, 0x3fffu, 2u, 8u, 2u, 321u, 3u, 236u, 2u, 1376u, 0u, "", ""},
    {"DIVMODU.EA_TO_D_TO_D", "DIVMODU", "DIVMODU.X(s:B/W/L/Q) <ea(e)>, Dn(q), Dn(r)", BEDROCK_FORM_EXTENDED, "integer", "DIVMOD.DIVMODU", "unprivileged", 0xf44u, 0xf44u, 0x4000u, 0x7fffu, 2u, 8u, 2u, 324u, 4u, 238u, 3u, 1376u, 0u, "", ""},
    {"DIVU.EA_TO_D", "DIVU", "DIVU.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "DIVIDE_MOD.DIVU", "unprivileged", 0xf44u, 0xf44u, 0x8000u, 0x87ffu, 2u, 8u, 2u, 328u, 3u, 241u, 2u, 1376u, 0u, "", ""},
    {"MODS.D_TO_EA", "MODS", "MODS.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "DIVIDE_MOD.MODS", "unprivileged", 0xf44u, 0xf44u, 0x8800u, 0x8fffu, 2u, 8u, 2u, 331u, 3u, 243u, 2u, 1376u, 0u, "", ""},
    {"MODS.EA_TO_D", "MODS", "MODS.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "DIVIDE_MOD.MODS", "unprivileged", 0xf44u, 0xf44u, 0x9000u, 0x97ffu, 2u, 8u, 2u, 334u, 3u, 245u, 2u, 1376u, 0u, "", ""},
    {"MODU.D_TO_EA", "MODU", "MODU.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "DIVIDE_MOD.MODU", "unprivileged", 0xf44u, 0xf44u, 0x9800u, 0x9fffu, 2u, 8u, 2u, 337u, 3u, 247u, 2u, 1376u, 0u, "", ""},
    {"MODU.EA_TO_D", "MODU", "MODU.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "DIVIDE_MOD.MODU", "unprivileged", 0xf44u, 0xf44u, 0xa000u, 0xa7ffu, 2u, 8u, 2u, 340u, 3u, 249u, 2u, 1376u, 0u, "", ""},
    {"MULHS.D_TO_EA", "MULHS", "MULHS.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "MULTIPLY_HIGH.MULHS", "unprivileged", 0xf44u, 0xf44u, 0xa800u, 0xafffu, 2u, 8u, 2u, 343u, 3u, 251u, 2u, 1376u, 0u, "", ""},
    {"MULHS.EA_TO_D", "MULHS", "MULHS.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "MULTIPLY_HIGH.MULHS", "unprivileged", 0xf44u, 0xf44u, 0xb000u, 0xb7ffu, 2u, 8u, 2u, 346u, 3u, 253u, 2u, 1376u, 0u, "", ""},
    {"MULHSU.D_TO_EA", "MULHSU", "MULHSU.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "MULTIPLY_HIGH.MULHSU", "unprivileged", 0xf44u, 0xf44u, 0xb800u, 0xbfffu, 2u, 8u, 2u, 349u, 3u, 255u, 2u, 1376u, 0u, "", ""},
    {"MULHSU.EA_TO_D", "MULHSU", "MULHSU.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "MULTIPLY_HIGH.MULHSU", "unprivileged", 0xf44u, 0xf44u, 0xc000u, 0xc7ffu, 2u, 8u, 2u, 352u, 3u, 257u, 2u, 1376u, 0u, "", ""},
    {"MULHU.D_TO_EA", "MULHU", "MULHU.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "MULTIPLY_HIGH.MULHU", "unprivileged", 0xf44u, 0xf44u, 0xc800u, 0xcfffu, 2u, 8u, 2u, 355u, 3u, 259u, 2u, 1376u, 0u, "", ""},
    {"MULHU.EA_TO_D", "MULHU", "MULHU.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "MULTIPLY_HIGH.MULHU", "unprivileged", 0xf44u, 0xf44u, 0xd000u, 0xd7ffu, 2u, 8u, 2u, 358u, 3u, 261u, 2u, 1376u, 0u, "", ""},
    {"MULS.D_TO_EA", "MULS", "MULS.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "MULTIPLY.MULS", "unprivileged", 0xf44u, 0xf44u, 0xd800u, 0xdfffu, 2u, 8u, 2u, 361u, 3u, 263u, 2u, 1376u, 0u, "", ""},
    {"MULS.EA_TO_D", "MULS", "MULS.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "MULTIPLY.MULS", "unprivileged", 0xf44u, 0xf44u, 0xe000u, 0xe7ffu, 2u, 8u, 2u, 364u, 3u, 265u, 2u, 1376u, 0u, "", ""},
    {"MULU.D_TO_EA", "MULU", "MULU.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "MULTIPLY.MULU", "unprivileged", 0xf44u, 0xf44u, 0xe800u, 0xefffu, 2u, 8u, 2u, 367u, 3u, 267u, 2u, 1376u, 0u, "", ""},
    {"MULU.EA_TO_D", "MULU", "MULU.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "MULTIPLY.MULU", "unprivileged", 0xf44u, 0xf44u, 0xf000u, 0xf7ffu, 2u, 8u, 2u, 370u, 3u, 269u, 2u, 1376u, 0u, "", ""},
    {"MADD.EA_TO_D_TO_D", "MADD", "MADD.X(s:B/W/L/Q) <ea(e)>, Dn(d), Dn(D)", BEDROCK_FORM_EXTENDED, "integer", "MULTIPLY_ACCUMULATE.MADD", "unprivileged", 0xf45u, 0xf45u, 0x0000u, 0x3fffu, 2u, 8u, 2u, 373u, 4u, 271u, 3u, 1376u, 0u, "", ""},
    {"MSUB.EA_TO_D_TO_D", "MSUB", "MSUB.X(s:B/W/L/Q) <ea(e)>, Dn(d), Dn(D)", BEDROCK_FORM_EXTENDED, "integer", "MULTIPLY_ACCUMULATE.MSUB", "unprivileged", 0xf45u, 0xf45u, 0x4000u, 0x7fffu, 2u, 8u, 2u, 377u, 4u, 274u, 3u, 1376u, 0u, "", ""},
    {"BCHG.D_TO_D", "BCHG", "BCHG.X(s:B/W/L/Q) Dn(b), Dn(b)", BEDROCK_FORM_EXTENDED, "integer", "BIT_OPS.BCHG", "unprivileged", 0xf46u, 0xf46u, 0x0000u, 0x00ffu, 2u, 8u, 2u, 381u, 3u, 277u, 2u, 1376u, 0u, "", ""},
    {"BCLR.D_TO_D", "BCLR", "BCLR.X(s:B/W/L/Q) Dn(b), Dn(b)", BEDROCK_FORM_EXTENDED, "integer", "BIT_OPS.BCLR", "unprivileged", 0xf46u, 0xf46u, 0x0100u, 0x01ffu, 2u, 8u, 2u, 384u, 3u, 279u, 2u, 1376u, 0u, "", ""},
    {"BSET.D_TO_D", "BSET", "BSET.X(s:B/W/L/Q) Dn(b), Dn(b)", BEDROCK_FORM_EXTENDED, "integer", "BIT_OPS.BSET", "unprivileged", 0xf46u, 0xf46u, 0x0200u, 0x02ffu, 2u, 8u, 2u, 387u, 3u, 281u, 2u, 1376u, 0u, "", ""},
    {"BTEST.D_TO_D", "BTEST", "BTEST.X(s:B/W/L/Q) Dn(b), Dn(b)", BEDROCK_FORM_EXTENDED, "integer", "BIT_OPS.BTEST", "unprivileged", 0xf46u, 0xf46u, 0x0300u, 0x03ffu, 2u, 8u, 2u, 390u, 3u, 283u, 2u, 1376u, 0u, "", ""},
    {"PARITY.EA", "PARITY", "PARITY.X(s:B/W/L/Q) <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "PARITY", "unprivileged", 0xf46u, 0xf46u, 0x0400u, 0x04ffu, 2u, 8u, 2u, 393u, 2u, 285u, 1u, 1376u, 0u, "", ""},
    {"RCL.D_TO_D", "RCL", "RCL.X(s:B/W/L/Q) Dn(n), Dn(n)", BEDROCK_FORM_EXTENDED, "integer", "ROTATES.RCL", "unprivileged", 0xf46u, 0xf46u, 0x0500u, 0x05ffu, 2u, 8u, 2u, 395u, 3u, 286u, 2u, 1376u, 0u, "", ""},
    {"RCR.D_TO_D", "RCR", "RCR.X(s:B/W/L/Q) Dn(n), Dn(n)", BEDROCK_FORM_EXTENDED, "integer", "ROTATES.RCR", "unprivileged", 0xf46u, 0xf46u, 0x0600u, 0x06ffu, 2u, 8u, 2u, 398u, 3u, 288u, 2u, 1376u, 0u, "", ""},
    {"REVBIT.D_TO_D", "REVBIT", "REVBIT.X(s:B/W/L/Q) Dn(d), Dn(D)", BEDROCK_FORM_EXTENDED, "integer", "REV.REVBIT", "unprivileged", 0xf46u, 0xf46u, 0x0700u, 0x07ffu, 2u, 8u, 2u, 401u, 3u, 290u, 2u, 1376u, 0u, "", ""},
    {"BCHG.D_TO_EA", "BCHG", "BCHG.X(s:B/W/L/Q) Dn(b), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "BIT_OPS.BCHG", "unprivileged", 0xf46u, 0xf46u, 0x0800u, 0x0fffu, 2u, 8u, 2u, 404u, 3u, 292u, 2u, 1376u, 0u, "", ""},
    {"BCLR.D_TO_EA", "BCLR", "BCLR.X(s:B/W/L/Q) Dn(b), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "BIT_OPS.BCLR", "unprivileged", 0xf46u, 0xf46u, 0x1000u, 0x17ffu, 2u, 8u, 2u, 407u, 3u, 294u, 2u, 1376u, 0u, "", ""},
    {"BSET.D_TO_EA", "BSET", "BSET.X(s:B/W/L/Q) Dn(b), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "BIT_OPS.BSET", "unprivileged", 0xf46u, 0xf46u, 0x1800u, 0x1fffu, 2u, 8u, 2u, 410u, 3u, 296u, 2u, 1376u, 0u, "", ""},
    {"BTEST.D_TO_EA", "BTEST", "BTEST.X(s:B/W/L/Q) Dn(b), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "BIT_OPS.BTEST", "unprivileged", 0xf46u, 0xf46u, 0x2000u, 0x27ffu, 2u, 8u, 2u, 413u, 3u, 298u, 2u, 1376u, 0u, "", ""},
    {"CLS.EA_TO_D", "CLS", "CLS.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "BIT_COUNTS.CLS", "unprivileged", 0xf46u, 0xf46u, 0x2800u, 0x2fffu, 2u, 8u, 2u, 416u, 3u, 300u, 2u, 1376u, 0u, "", ""},
    {"CLZ.EA_TO_D", "CLZ", "CLZ.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "BIT_COUNTS.CLZ", "unprivileged", 0xf46u, 0xf46u, 0x3000u, 0x37ffu, 2u, 8u, 2u, 419u, 3u, 302u, 2u, 1376u, 0u, "", ""},
    {"CTS.EA_TO_D", "CTS", "CTS.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "BIT_COUNTS.CTS", "unprivileged", 0xf46u, 0xf46u, 0x3800u, 0x3fffu, 2u, 8u, 2u, 422u, 3u, 304u, 2u, 1376u, 0u, "", ""},
    {"CTZ.EA_TO_D", "CTZ", "CTZ.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "BIT_COUNTS.CTZ", "unprivileged", 0xf46u, 0xf46u, 0x4000u, 0x47ffu, 2u, 8u, 2u, 425u, 3u, 306u, 2u, 1376u, 0u, "", ""},
    {"POPCNT.EA_TO_D", "POPCNT", "POPCNT.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "BIT_COUNTS.POPCNT", "unprivileged", 0xf46u, 0xf46u, 0x4800u, 0x4fffu, 2u, 8u, 2u, 428u, 3u, 308u, 2u, 1376u, 0u, "", ""},
    {"RCL.D_TO_EA", "RCL", "RCL.X(s:B/W/L/Q) Dn(n), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ROTATES.RCL", "unprivileged", 0xf46u, 0xf46u, 0x5000u, 0x57ffu, 2u, 8u, 2u, 431u, 3u, 310u, 2u, 1376u, 0u, "", ""},
    {"RCR.D_TO_EA", "RCR", "RCR.X(s:B/W/L/Q) Dn(n), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ROTATES.RCR", "unprivileged", 0xf46u, 0xf46u, 0x5800u, 0x5fffu, 2u, 8u, 2u, 434u, 3u, 312u, 2u, 1376u, 0u, "", ""},
    {"REVBIT.D_TO_EA", "REVBIT", "REVBIT.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "REV.REVBIT", "unprivileged", 0xf46u, 0xf46u, 0x6000u, 0x67ffu, 2u, 8u, 2u, 437u, 3u, 314u, 2u, 1376u, 0u, "", ""},
    {"REVBIT.EA_TO_D", "REVBIT", "REVBIT.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "integer", "REV.REVBIT", "unprivileged", 0xf46u, 0xf46u, 0x6800u, 0x6fffu, 2u, 8u, 2u, 440u, 3u, 316u, 2u, 1376u, 0u, "", ""},
    {"ROL.D_TO_D", "ROL", "ROL.X(s:B/W/L/Q) Dn(n), Dn(n)", BEDROCK_FORM_EXTENDED, "integer", "ROTATES.ROL", "unprivileged", 0xf46u, 0xf46u, 0x7000u, 0x70ffu, 2u, 8u, 2u, 443u, 3u, 318u, 2u, 1376u, 0u, "", ""},
    {"ROR.D_TO_D", "ROR", "ROR.X(s:B/W/L/Q) Dn(n), Dn(n)", BEDROCK_FORM_EXTENDED, "integer", "ROTATES.ROR", "unprivileged", 0xf46u, 0xf46u, 0x7100u, 0x71ffu, 2u, 8u, 2u, 446u, 3u, 320u, 2u, 1376u, 0u, "", ""},
    {"SAR.D_TO_D", "SAR", "SAR.X(s:B/W/L/Q) Dn(n), Dn(n)", BEDROCK_FORM_EXTENDED, "integer", "SHIFTS.SAR", "unprivileged", 0xf46u, 0xf46u, 0x7200u, 0x72ffu, 2u, 8u, 2u, 449u, 3u, 322u, 2u, 1376u, 0u, "", ""},
    {"SHL.D_TO_D", "SHL", "SHL.X(s:B/W/L/Q) Dn(n), Dn(n)", BEDROCK_FORM_EXTENDED, "integer", "SHIFTS.SHL", "unprivileged", 0xf46u, 0xf46u, 0x7300u, 0x73ffu, 2u, 8u, 2u, 452u, 3u, 324u, 2u, 1376u, 0u, "", ""},
    {"SHR.D_TO_D", "SHR", "SHR.X(s:B/W/L/Q) Dn(n), Dn(n)", BEDROCK_FORM_EXTENDED, "integer", "SHIFTS.SHR", "unprivileged", 0xf46u, 0xf46u, 0x7400u, 0x74ffu, 2u, 8u, 2u, 455u, 3u, 326u, 2u, 1376u, 0u, "", ""},
    {"ROL.D_TO_EA", "ROL", "ROL.X(s:B/W/L/Q) Dn(n), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ROTATES.ROL", "unprivileged", 0xf46u, 0xf46u, 0x7800u, 0x7fffu, 2u, 8u, 2u, 458u, 3u, 328u, 2u, 1376u, 0u, "", ""},
    {"ROR.D_TO_EA", "ROR", "ROR.X(s:B/W/L/Q) Dn(n), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ROTATES.ROR", "unprivileged", 0xf46u, 0xf46u, 0x8000u, 0x87ffu, 2u, 8u, 2u, 461u, 3u, 330u, 2u, 1376u, 0u, "", ""},
    {"SAR.D_TO_EA", "SAR", "SAR.X(s:B/W/L/Q) Dn(n), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "SHIFTS.SAR", "unprivileged", 0xf46u, 0xf46u, 0x8800u, 0x8fffu, 2u, 8u, 2u, 464u, 3u, 332u, 2u, 1376u, 0u, "", ""},
    {"SHL.D_TO_EA", "SHL", "SHL.X(s:B/W/L/Q) Dn(n), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "SHIFTS.SHL", "unprivileged", 0xf46u, 0xf46u, 0x9000u, 0x97ffu, 2u, 8u, 2u, 467u, 3u, 334u, 2u, 1376u, 0u, "", ""},
    {"SHR.D_TO_EA", "SHR", "SHR.X(s:B/W/L/Q) Dn(n), <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "SHIFTS.SHR", "unprivileged", 0xf46u, 0xf46u, 0x9800u, 0x9fffu, 2u, 8u, 2u, 470u, 3u, 336u, 2u, 1376u, 0u, "", ""},
    {"BCHG.I6_TO_EA", "BCHG", "BCHG.X(s:B/W/L/Q) <bit_index(b)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "BIT_OPS.BCHG", "unprivileged", 0xf47u, 0xf47u, 0x0000u, 0x3fffu, 2u, 8u, 2u, 473u, 3u, 338u, 2u, 1376u, 0u, "", ""},
    {"BCLR.I6_TO_EA", "BCLR", "BCLR.X(s:B/W/L/Q) <bit_index(b)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "BIT_OPS.BCLR", "unprivileged", 0xf47u, 0xf47u, 0x4000u, 0x7fffu, 2u, 8u, 2u, 476u, 3u, 340u, 2u, 1376u, 0u, "", ""},
    {"BSET.I6_TO_EA", "BSET", "BSET.X(s:B/W/L/Q) <bit_index(b)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "BIT_OPS.BSET", "unprivileged", 0xf47u, 0xf47u, 0x8000u, 0xbfffu, 2u, 8u, 2u, 479u, 3u, 342u, 2u, 1376u, 0u, "", ""},
    {"BTEST.I6_TO_EA", "BTEST", "BTEST.X(s:B/W/L/Q) <bit_index(b)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "BIT_OPS.BTEST", "unprivileged", 0xf47u, 0xf47u, 0xc000u, 0xffffu, 2u, 8u, 2u, 482u, 3u, 344u, 2u, 1376u, 0u, "", ""},
    {"RCL.I6_TO_EA", "RCL", "RCL.X(s:B/W/L/Q) <count(n)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ROTATES.RCL", "unprivileged", 0xf48u, 0xf48u, 0x0000u, 0x3fffu, 2u, 8u, 2u, 485u, 3u, 346u, 2u, 1376u, 0u, "", ""},
    {"RCR.I6_TO_EA", "RCR", "RCR.X(s:B/W/L/Q) <count(n)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ROTATES.RCR", "unprivileged", 0xf48u, 0xf48u, 0x4000u, 0x7fffu, 2u, 8u, 2u, 488u, 3u, 348u, 2u, 1376u, 0u, "", ""},
    {"ROL.I6_TO_EA", "ROL", "ROL.X(s:B/W/L/Q) <count(n)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ROTATES.ROL", "unprivileged", 0xf48u, 0xf48u, 0x8000u, 0xbfffu, 2u, 8u, 2u, 491u, 3u, 350u, 2u, 1376u, 0u, "", ""},
    {"ROR.I6_TO_EA", "ROR", "ROR.X(s:B/W/L/Q) <count(n)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "ROTATES.ROR", "unprivileged", 0xf48u, 0xf48u, 0xc000u, 0xffffu, 2u, 8u, 2u, 494u, 3u, 352u, 2u, 1376u, 0u, "", ""},
    {"SHL.I6_TO_EA", "SHL", "SHL.X(s:B/W/L/Q) <count(n)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "SHIFTS.SHL", "unprivileged", 0xf49u, 0xf49u, 0x0000u, 0x3fffu, 2u, 8u, 2u, 497u, 3u, 354u, 2u, 1376u, 0u, "", ""},
    {"SHR.I6_TO_EA", "SHR", "SHR.X(s:B/W/L/Q) <count(n)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "SHIFTS.SHR", "unprivileged", 0xf49u, 0xf49u, 0x4000u, 0x7fffu, 2u, 8u, 2u, 500u, 3u, 356u, 2u, 1376u, 0u, "", ""},
    {"SAR.I6_TO_EA", "SAR", "SAR.X(s:B/W/L/Q) <count(n)>, <ea(e)>", BEDROCK_FORM_EXTENDED, "integer", "SHIFTS.SAR", "unprivileged", 0xf49u, 0xf49u, 0x8000u, 0xbfffu, 2u, 8u, 2u, 503u, 3u, 358u, 2u, 1376u, 0u, "", ""},
    {"MOV.D_TO_EA_WIDE", "MOV", "MOV.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "data_movement", "MOV.extended_forms", "unprivileged", 0xf4au, 0xf4au, 0x0000u, 0x07ffu, 2u, 8u, 2u, 506u, 3u, 360u, 2u, 1376u, 0u, "", ""},
    {"MOV.EA_TO_D_WIDE", "MOV", "MOV.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "data_movement", "MOV.extended_forms", "unprivileged", 0xf4au, 0xf4au, 0x0800u, 0x0fffu, 2u, 8u, 2u, 509u, 3u, 362u, 2u, 1376u, 0u, "", ""},
    {"XCHG.D_TO_EA", "XCHG", "XCHG.X(s:B/W/L/Q) Dn(l), <ea(e)>", BEDROCK_FORM_EXTENDED, "data_movement", "XCHG", "unprivileged", 0xf4au, 0xf4au, 0x1000u, 0x17ffu, 2u, 8u, 2u, 512u, 3u, 364u, 2u, 1376u, 0u, "", ""},
    {"XCHG.EA_TO_D", "XCHG", "XCHG.X(s:B/W/L/Q) <ea(e)>, Dn(r)", BEDROCK_FORM_EXTENDED, "data_movement", "XCHG", "unprivileged", 0xf4au, 0xf4au, 0x1800u, 0x1fffu, 2u, 8u, 2u, 515u, 3u, 366u, 2u, 1376u, 0u, "", ""},
    {"MOV.EA_TO_EA", "MOV", "MOV.X(s:B/W/L/Q) <ea(e)>, <ea(E)>", BEDROCK_FORM_EXTENDED, "data_movement", "MOV.extended_forms", "unprivileged", 0xf4au, 0xf4au, 0x4000u, 0x7fffu, 2u, 8u, 2u, 518u, 3u, 368u, 2u, 1376u, 0u, "", ""},
    {"GETDB.D", "GETDB", "GETDB.D Dn(d)", BEDROCK_FORM_EXTENDED, "data_movement", "DATA_BANK_READ.GETDB", "user allowed", 0xf4bu, 0xf4bu, 0x0000u, 0x0007u, 2u, 8u, 2u, 521u, 1u, 370u, 1u, 1376u, 0u, "", ""},
    {"SELDB.D", "SELDB", "SELDB.D Dn(d)", BEDROCK_FORM_EXTENDED, "data_movement", "DATA_BANK_SELECT.SELDB", "user allowed", 0xf4bu, 0xf4bu, 0x0008u, 0x000fu, 2u, 8u, 2u, 522u, 1u, 371u, 1u, 1376u, 0u, "", ""},
    {"MOVSETAD.DB_TO_BITMAP", "MOVSETAD", "MOVSETAD DBn(k), <bitmap>", BEDROCK_FORM_EXTENDED, "data_movement", "MOVSETAD.extended_forms", "unprivileged", 0xf4bu, 0xf4bu, 0x0010u, 0x001fu, 3u, 8u, 3u, 523u, 2u, 372u, 2u, 1376u, 0u, "", ""},
    {"MOVSETDA.DB_TO_BITMAP", "MOVSETDA", "MOVSETDA DBn(k), <bitmap>", BEDROCK_FORM_EXTENDED, "data_movement", "MOVSETDA.extended_forms", "unprivileged", 0xf4bu, 0xf4bu, 0x0020u, 0x002fu, 3u, 8u, 3u, 525u, 2u, 374u, 2u, 1376u, 0u, "", ""},
    {"SELDB.DB", "SELDB", "SELDB DBn(k)", BEDROCK_FORM_EXTENDED, "data_movement", "DATA_BANK_SELECT.SELDB", "user allowed", 0xf4bu, 0xf4bu, 0x0030u, 0x003fu, 2u, 8u, 2u, 527u, 1u, 376u, 1u, 1376u, 0u, "", ""},
    {"XCHGSETAD.DB_TO_BITMAP", "XCHGSETAD", "XCHGSETAD DBn(k), <bitmap>", BEDROCK_FORM_EXTENDED, "data_movement", "XCHGSETAD.extended_forms", "unprivileged", 0xf4bu, 0xf4bu, 0x0040u, 0x004fu, 3u, 8u, 3u, 528u, 2u, 377u, 2u, 1376u, 0u, "", ""},
    {"XCHGSETDA.DB_TO_BITMAP", "XCHGSETDA", "XCHGSETDA DBn(k), <bitmap>", BEDROCK_FORM_EXTENDED, "data_movement", "XCHGSETDA.extended_forms", "unprivileged", 0xf4bu, 0xf4bu, 0x0050u, 0x005fu, 3u, 8u, 3u, 530u, 2u, 379u, 2u, 1376u, 0u, "", ""},
    {"MOVSETDD.DB_TO_DB_TO_BITMAP", "MOVSETDD", "MOVSETDD DBn(k), DBn(K), <bitmap>", BEDROCK_FORM_EXTENDED, "data_movement", "DATA_BANK_SET_COPY.MOVSETDD", "unprivileged", 0xf4bu, 0xf4bu, 0x0100u, 0x01ffu, 3u, 8u, 3u, 532u, 3u, 381u, 3u, 1376u, 0u, "", ""},
    {"XCHGSETDD.DB_TO_DB_TO_BITMAP", "XCHGSETDD", "XCHGSETDD DBn(k), DBn(K), <bitmap>", BEDROCK_FORM_EXTENDED, "data_movement", "DATA_BANK_SET_EXCHANGE.XCHGSETDD", "unprivileged", 0xf4bu, 0xf4bu, 0x0200u, 0x02ffu, 3u, 8u, 3u, 535u, 3u, 384u, 3u, 1376u, 0u, "", ""},
    {"LEA.EA_TO_A", "LEA", "LEA <ea(e)>, An(a)", BEDROCK_FORM_EXTENDED, "data_movement", "LEA", "unprivileged", 0xf4cu, 0xf4cu, 0x0000u, 0x01ffu, 2u, 8u, 2u, 538u, 2u, 387u, 2u, 1376u, 0u, "", ""},
    {"SEGLEA.EA_TO_A", "SEGLEA", "SEGLEA <ea(e)>, An(a)", BEDROCK_FORM_EXTENDED, "data_movement", "SEGLEA", "unprivileged", 0xf4cu, 0xf4cu, 0x0200u, 0x03ffu, 2u, 8u, 2u, 540u, 2u, 389u, 2u, 1376u, 0u, "", ""},
    {"TESTCANON.EA", "TESTCANON", "TESTCANON <ea(e)>", BEDROCK_FORM_EXTENDED, "data_movement", "TESTCANON", "unprivileged", 0xf4cu, 0xf4cu, 0x0400u, 0x043fu, 2u, 8u, 2u, 542u, 1u, 391u, 1u, 1376u, 0u, "", ""},
    {"CALL.EA", "CALL", "CALL <ea(e)>", BEDROCK_FORM_EXTENDED, "control_flow", "CALL.extended_forms", "unprivileged", 0xf4du, 0xf4du, 0x0000u, 0x003fu, 2u, 8u, 2u, 543u, 1u, 392u, 1u, 1376u, 0u, "", ""},
    {"LRET", "LRET", "LRET", BEDROCK_FORM_EXTENDED, "control_flow", "LRET", "unprivileged", 0xf4du, 0xf4du, 0x0040u, 0x0040u, 2u, 8u, 2u, 544u, 0u, 393u, 0u, 1376u, 0u, "", ""},
    {"LCALL.D_TO_EA", "LCALL", "LCALL Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "control_flow", "LCALL", "unprivileged", 0xf4du, 0xf4du, 0x0200u, 0x03ffu, 2u, 8u, 2u, 544u, 2u, 393u, 2u, 1376u, 0u, "", ""},
    {"LJMP.D_TO_EA", "LJMP", "LJMP Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "control_flow", "LJMP", "unprivileged", 0xf4du, 0xf4du, 0x0400u, 0x05ffu, 2u, 8u, 2u, 546u, 2u, 395u, 2u, 1376u, 0u, "", ""},
    {"NOP", "NOP", "NOP", BEDROCK_FORM_COMPACT, "system", "CORE_MISC.NOP", "any", 0xf4fu, 0xf4fu, 0x0000u, 0x0000u, 1u, 8u, 1u, 548u, 0u, 397u, 0u, 1376u, 0u, "", ""},
    {"DJcc.D_TO_EA", "DJcc", "DJcc.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "control_flow", "DJcc", "unprivileged", 0xf50u, 0xf5fu, 0x0000u, 0x07ffu, 2u, 8u, 2u, 548u, 4u, 397u, 2u, 1376u, 0u, "", ""},
    {"FMOVcc.F_TO_F", "FMOVcc", "FMOVcc Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FMOVcc.extended_forms", "unprivileged", 0xf50u, 0xf5fu, 0x0800u, 0x08ffu, 2u, 8u, 2u, 552u, 3u, 399u, 2u, 1376u, 0u, "", ""},
    {"TRAP", "TRAP", "TRAP", BEDROCK_FORM_EXTENDED_ALIAS, "control_flow", "TRAPcc", "unprivileged", 0xf50u, 0xf50u, 0x0900u, 0x0900u, 2u, 8u, 2u, 555u, 0u, 401u, 0u, 1376u, 1u, "TRAPcc", "T"},
    {"TRAPcc", "TRAPcc", "TRAPcc", BEDROCK_FORM_EXTENDED, "control_flow", "TRAPcc", "unprivileged", 0xf50u, 0xf5fu, 0x0900u, 0x0900u, 2u, 8u, 2u, 555u, 1u, 401u, 0u, 1377u, 0u, "", ""},
    {"JMP.EA", "JMP", "JMP.X(z:W/L) <ea(e)>", BEDROCK_FORM_EXTENDED_ALIAS, "control_flow", "Jcc.extended_forms", "unprivileged", 0xf50u, 0xf50u, 0x0980u, 0x09ffu, 2u, 8u, 2u, 556u, 2u, 401u, 1u, 1377u, 1u, "Jcc.EA", "T"},
    {"Jcc.EA", "Jcc", "Jcc.X(z:W/L) <ea(e)>", BEDROCK_FORM_EXTENDED, "control_flow", "Jcc.extended_forms", "unprivileged", 0xf50u, 0xf5fu, 0x0980u, 0x09ffu, 2u, 8u, 2u, 558u, 3u, 402u, 1u, 1378u, 0u, "", ""},
    {"SETcc.EA", "SETcc", "SETcc.X(s:B/W/L/Q) <ea(e)>", BEDROCK_FORM_EXTENDED, "control_flow", "SETcc", "unprivileged", 0xf50u, 0xf5fu, 0x0a00u, 0x0affu, 2u, 8u, 2u, 561u, 3u, 403u, 1u, 1378u, 0u, "", ""},
    {"MOVcc.A_TO_EA", "MOVcc", "MOVcc.X(s:B/W/L/Q) An(a), <ea(e)>", BEDROCK_FORM_EXTENDED, "control_flow", "MOVcc", "unprivileged", 0xf50u, 0xf5fu, 0x1000u, 0x17ffu, 2u, 8u, 2u, 564u, 4u, 404u, 2u, 1378u, 0u, "", ""},
    {"MOVcc.D_TO_EA", "MOVcc", "MOVcc.X(s:B/W/L/Q) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "control_flow", "MOVcc", "unprivileged", 0xf50u, 0xf5fu, 0x1800u, 0x1fffu, 2u, 8u, 2u, 568u, 4u, 406u, 2u, 1378u, 0u, "", ""},
    {"IJcc.D_TO_D_TO_EA", "IJcc", "IJcc.X(z:L/Q) Dn(d), Dn(D), <ea(e)>", BEDROCK_FORM_EXTENDED, "control_flow", "IJcc", "unprivileged", 0xf50u, 0xf5fu, 0x2000u, 0x3fffu, 2u, 8u, 2u, 572u, 5u, 408u, 3u, 1378u, 0u, "", ""},
    {"MOVcc.EA_TO_A", "MOVcc", "MOVcc.X(s:B/W/L/Q) <ea(e)>, An(a)", BEDROCK_FORM_EXTENDED, "control_flow", "MOVcc", "unprivileged", 0xf50u, 0xf5fu, 0x4000u, 0x47ffu, 2u, 8u, 2u, 577u, 4u, 411u, 2u, 1378u, 0u, "", ""},
    {"MOVcc.EA_TO_D", "MOVcc", "MOVcc.X(s:B/W/L/Q) <ea(e)>, Dn(d)", BEDROCK_FORM_EXTENDED, "control_flow", "MOVcc", "unprivileged", 0xf50u, 0xf5fu, 0x4800u, 0x4fffu, 2u, 8u, 2u, 581u, 4u, 413u, 2u, 1378u, 0u, "", ""},
    {"FMOVcc.EA_TO_F", "FMOVcc", "FMOVcc.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FMOVcc.extended_forms", "unprivileged", 0xf50u, 0xf5fu, 0x5000u, 0x57ffu, 2u, 8u, 2u, 585u, 4u, 415u, 2u, 1378u, 0u, "", ""},
    {"FMOVcc.F_TO_EA", "FMOVcc", "FMOVcc.X(z:S/D) Fn(f), <ea(e)>", BEDROCK_FORM_EXTENDED, "fpu", "FMOVcc.extended_forms", "unprivileged", 0xf50u, 0xf5fu, 0x5800u, 0x5fffu, 2u, 8u, 2u, 589u, 4u, 417u, 2u, 1378u, 0u, "", ""},
    {"CMPXCHG.D_TO_D_TO_EA", "CMPXCHG", "CMPXCHG.X(s:B/W/L/Q)/ORDER(o) Dn(x), Dn(y), <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "CMPXCHG", "unprivileged", 0xf60u, 0xf60u, 0x0000u, 0x0003u, 3u, 8u, 3u, 593u, 5u, 419u, 3u, 1378u, 0u, "", ""},
    {"FETCHADD.D_TO_EA", "FETCHADD", "FETCHADD.X(s:B/W/L/Q)/ORDER(o) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "FETCH_OPS.FETCHADD", "unprivileged", 0xf60u, 0xf60u, 0x0004u, 0x0004u, 3u, 8u, 3u, 598u, 4u, 422u, 2u, 1378u, 0u, "", ""},
    {"FETCHAND.D_TO_EA", "FETCHAND", "FETCHAND.X(s:B/W/L/Q)/ORDER(o) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "FETCH_OPS.FETCHAND", "unprivileged", 0xf60u, 0xf60u, 0x0005u, 0x0005u, 3u, 8u, 3u, 602u, 4u, 424u, 2u, 1378u, 0u, "", ""},
    {"FETCHOR.D_TO_EA", "FETCHOR", "FETCHOR.X(s:B/W/L/Q)/ORDER(o) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "FETCH_OPS.FETCHOR", "unprivileged", 0xf60u, 0xf60u, 0x0006u, 0x0006u, 3u, 8u, 3u, 606u, 4u, 426u, 2u, 1378u, 0u, "", ""},
    {"FETCHSUB.D_TO_EA", "FETCHSUB", "FETCHSUB.X(s:B/W/L/Q)/ORDER(o) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "FETCH_OPS.FETCHSUB", "unprivileged", 0xf60u, 0xf60u, 0x0007u, 0x0007u, 3u, 8u, 3u, 610u, 4u, 428u, 2u, 1378u, 0u, "", ""},
    {"FETCHXOR.D_TO_EA", "FETCHXOR", "FETCHXOR.X(s:B/W/L/Q)/ORDER(o) Dn(d), <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "FETCH_OPS.FETCHXOR", "unprivileged", 0xf60u, 0xf60u, 0x0008u, 0x0008u, 3u, 8u, 3u, 614u, 4u, 430u, 2u, 1378u, 0u, "", ""},
    {"PREFETCH.EA", "PREFETCH", "PREFETCH <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "PREFETCH", "user allowed", 0xf61u, 0xf61u, 0x0000u, 0x003fu, 2u, 8u, 2u, 618u, 1u, 432u, 1u, 1378u, 0u, "", ""},
    {"INVTLB", "INVTLB", "INVTLB", BEDROCK_FORM_EXTENDED, "system", "TLB_INVALIDATE.INVTLB", "supervisor", 0xf62u, 0xf62u, 0x0000u, 0x0000u, 2u, 8u, 2u, 619u, 0u, 433u, 0u, 1378u, 0u, "", ""},
    {"INVASID.IMM", "INVASID", "INVASID imm16", BEDROCK_FORM_EXTENDED, "system", "TLB_INVALIDATE.INVASID", "supervisor", 0xf62u, 0xf62u, 0x0001u, 0x0001u, 3u, 8u, 3u, 619u, 1u, 433u, 1u, 1378u, 0u, "", ""},
    {"SWPT.D", "SWPT", "SWPT.D Dn(d)", BEDROCK_FORM_EXTENDED, "system", "SWPT", "supervisor", 0xf62u, 0xf62u, 0x0008u, 0x000fu, 2u, 8u, 2u, 620u, 1u, 434u, 1u, 1378u, 0u, "", ""},
    {"RDPTC.D", "RDPTC", "RDPTC.D Dn(d)", BEDROCK_FORM_EXTENDED, "system", "RDPTC", "configurable", 0xf62u, 0xf62u, 0x0010u, 0x0017u, 2u, 8u, 2u, 621u, 1u, 435u, 1u, 1378u, 0u, "", ""},
    {"INVPAGE.EA", "INVPAGE", "INVPAGE <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "TLB_INVALIDATE.INVPAGE", "supervisor", 0xf62u, 0xf62u, 0x0040u, 0x007fu, 2u, 8u, 2u, 622u, 1u, 436u, 1u, 1378u, 0u, "", ""},
    {"SWPTA.D_TO_D", "SWPTA", "SWPTA Dn(d), Dn(D)", BEDROCK_FORM_EXTENDED, "system", "SWPTA", "supervisor", 0xf62u, 0xf62u, 0x0080u, 0x00bfu, 2u, 8u, 2u, 623u, 2u, 437u, 2u, 1378u, 0u, "", ""},
    {"INVDCACHE.EA", "INVDCACHE", "INVDCACHE <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "CACHE_OPS.INVDCACHE", "supervisor_or_policy_controlled", 0xf62u, 0xf62u, 0x00c0u, 0x00ffu, 2u, 8u, 2u, 625u, 1u, 439u, 1u, 1378u, 0u, "", ""},
    {"WRBKDCACHE.EA", "WRBKDCACHE", "WRBKDCACHE <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "CACHE_OPS.WRBKDCACHE", "supervisor_or_policy_controlled", 0xf62u, 0xf62u, 0x0100u, 0x013fu, 2u, 8u, 2u, 626u, 1u, 440u, 1u, 1378u, 0u, "", ""},
    {"FLSHDCACHE.EA", "FLSHDCACHE", "FLSHDCACHE <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "CACHE_OPS.FLSHDCACHE", "supervisor_or_policy_controlled", 0xf62u, 0xf62u, 0x0140u, 0x017fu, 2u, 8u, 2u, 627u, 1u, 441u, 1u, 1378u, 0u, "", ""},
    {"INVICACHE.EA", "INVICACHE", "INVICACHE <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "CACHE_OPS.INVICACHE", "supervisor_or_policy_controlled", 0xf62u, 0xf62u, 0x0180u, 0x01bfu, 2u, 8u, 2u, 628u, 1u, 442u, 1u, 1378u, 0u, "", ""},
    {"SYNCCACHE.EA", "SYNCCACHE", "SYNCCACHE <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "CACHE_OPS.SYNCCACHE", "supervisor_or_policy_controlled", 0xf62u, 0xf62u, 0x01c0u, 0x01ffu, 2u, 8u, 2u, 629u, 1u, 443u, 1u, 1378u, 0u, "", ""},
    {"PTATTR.EA", "PTATTR", "PTATTR <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "PAGE_QUERY.PTATTR", "supervisor", 0xf62u, 0xf62u, 0x0200u, 0x023fu, 2u, 8u, 2u, 630u, 1u, 444u, 1u, 1378u, 0u, "", ""},
    {"PTQUERY.EA", "PTQUERY", "PTQUERY <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "PAGE_QUERY.PTQUERY", "supervisor", 0xf62u, 0xf62u, 0x0240u, 0x027fu, 2u, 8u, 2u, 631u, 1u, 445u, 1u, 1378u, 0u, "", ""},
    {"VTOP.EA", "VTOP", "VTOP <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "PAGE_QUERY.VTOP", "supervisor", 0xf62u, 0xf62u, 0x0280u, 0x02bfu, 2u, 8u, 2u, 632u, 1u, 446u, 1u, 1378u, 0u, "", ""},
    {"RDCR.D", "RDCR", "RDCR.D <cr(i)>, Dn(d)", BEDROCK_FORM_EXTENDED, "system", "CONTROL_REGISTER_ACCESS.RDCR", "supervisor", 0xf63u, 0xf63u, 0x0000u, 0x0007u, 3u, 8u, 3u, 633u, 2u, 447u, 2u, 1378u, 0u, "", ""},
    {"WRCR.D", "WRCR", "WRCR.D Dn(d), <cr(i)>", BEDROCK_FORM_EXTENDED, "system", "CONTROL_REGISTER_ACCESS.WRCR", "supervisor", 0xf63u, 0xf63u, 0x0008u, 0x000fu, 3u, 8u, 3u, 635u, 2u, 449u, 2u, 1378u, 0u, "", ""},
    {"RDFLAGS.D", "RDFLAGS", "RDFLAGS.D Dn(d)", BEDROCK_FORM_EXTENDED, "system", "FLAGS_ACCESS.RDFLAGS", "unprivileged", 0xf63u, 0xf63u, 0x0010u, 0x0017u, 2u, 8u, 2u, 637u, 1u, 451u, 1u, 1378u, 0u, "", ""},
    {"WRFLAGS.D", "WRFLAGS", "WRFLAGS.D Dn(d)", BEDROCK_FORM_EXTENDED, "system", "FLAGS_ACCESS.WRFLAGS", "unprivileged", 0xf63u, 0xf63u, 0x0018u, 0x001fu, 2u, 8u, 2u, 638u, 1u, 452u, 1u, 1378u, 0u, "", ""},
    {"RDSTATUS.D", "RDSTATUS", "RDSTATUS.D Dn(d)", BEDROCK_FORM_EXTENDED, "system", "STATUS_ACCESS.RDSTATUS", "unprivileged", 0xf63u, 0xf63u, 0x0020u, 0x0027u, 2u, 8u, 2u, 639u, 1u, 453u, 1u, 1378u, 0u, "", ""},
    {"WRSTATUS.D", "WRSTATUS", "WRSTATUS.D Dn(d)", BEDROCK_FORM_EXTENDED, "system", "STATUS_ACCESS.WRSTATUS", "supervisor", 0xf63u, 0xf63u, 0x0028u, 0x002fu, 2u, 8u, 2u, 640u, 1u, 454u, 1u, 1378u, 0u, "", ""},
    {"CPUID.D", "CPUID", "CPUID.D Dn(d)", BEDROCK_FORM_EXTENDED, "system", "CPUID", "user allowed", 0xf63u, 0xf63u, 0x0030u, 0x0037u, 2u, 8u, 2u, 641u, 1u, 455u, 1u, 1378u, 0u, "", ""},
    {"RDFSTATUS.D", "RDFSTATUS", "RDFSTATUS.D Dn(d)", BEDROCK_FORM_EXTENDED, "system", "FSTATUS_ACCESS.RDFSTATUS", "unprivileged", 0xf63u, 0xf63u, 0x0038u, 0x003fu, 2u, 8u, 2u, 642u, 1u, 456u, 1u, 1378u, 0u, "", ""},
    {"RDSEG.S_TO_D", "RDSEG", "RDSEG Sreg(g), Dn(d)", BEDROCK_FORM_EXTENDED, "system", "SEGMENT_REGISTER_ACCESS.RDSEG", "policy controlled", 0xf63u, 0xf63u, 0x0040u, 0x007fu, 2u, 8u, 2u, 643u, 2u, 457u, 2u, 1378u, 0u, "", ""},
    {"WRSEG.D_TO_S", "WRSEG", "WRSEG Dn(d), Sreg(g)", BEDROCK_FORM_EXTENDED, "system", "SEGMENT_REGISTER_ACCESS.WRSEG", "policy controlled", 0xf63u, 0xf63u, 0x0080u, 0x00bfu, 2u, 8u, 2u, 645u, 2u, 459u, 2u, 1378u, 0u, "", ""},
    {"SAVE.EA", "SAVE", "SAVE <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "PROCESSOR_STATE_SAVE_RESTORE.SAVE", "unprivileged", 0xf63u, 0xf63u, 0x00c0u, 0x00ffu, 2u, 8u, 2u, 647u, 1u, 461u, 1u, 1378u, 0u, "", ""},
    {"RESTORE.EA", "RESTORE", "RESTORE <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "PROCESSOR_STATE_SAVE_RESTORE.RESTORE", "unprivileged", 0xf63u, 0xf63u, 0x0100u, 0x013fu, 2u, 8u, 2u, 648u, 1u, 462u, 1u, 1378u, 0u, "", ""},
    {"RDPMC.IMM_TO_D", "RDPMC", "RDPMC imm16, Dn(d)", BEDROCK_FORM_EXTENDED, "system", "RDPMC", "configurable", 0xf63u, 0xf63u, 0x0140u, 0x0147u, 3u, 8u, 3u, 649u, 2u, 463u, 2u, 1378u, 0u, "", ""},
    {"WRFSTATUS.D", "WRFSTATUS", "WRFSTATUS.D Dn(d)", BEDROCK_FORM_EXTENDED, "system", "FSTATUS_ACCESS.WRFSTATUS", "unprivileged", 0xf63u, 0xf63u, 0x0148u, 0x014fu, 2u, 8u, 2u, 651u, 1u, 465u, 1u, 1378u, 0u, "", ""},
    {"ENCINST.EA", "ENCINST", "ENCINST <ea(e)>", BEDROCK_FORM_EXTENDED, "system", "ENCINST", "user allowed when ENCINST is present", 0xf64u, 0xf64u, 0x0000u, 0x003fu, 2u, 8u, 2u, 652u, 1u, 466u, 1u, 1378u, 0u, "", ""},
    {"FCMP.F_TO_F", "FCMP", "FCMP.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_COMPARE.FCMP", "unprivileged", 0xf65u, 0xf65u, 0x0000u, 0x01ffu, 2u, 8u, 2u, 653u, 3u, 467u, 2u, 1378u, 0u, "", ""},
    {"FTEST.F", "FTEST", "FTEST.X(z:S/D) Fn(f)", BEDROCK_FORM_EXTENDED, "fpu", "FP_COMPARE.FTEST", "unprivileged", 0xf65u, 0xf65u, 0x0200u, 0x021fu, 2u, 8u, 2u, 656u, 2u, 469u, 1u, 1378u, 0u, "", ""},
    {"FMOVCR.IMM_TO_F", "FMOVCR", "FMOVCR imm16, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FMOVCR", "unprivileged", 0xf65u, 0xf65u, 0x0220u, 0x022fu, 3u, 8u, 3u, 658u, 2u, 470u, 2u, 1378u, 0u, "", ""},
    {"FCVT.D_TO_F", "FCVT", "FCVT Dn(d), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FCVT_FCVTU.FCVT", "unprivileged", 0xf65u, 0xf65u, 0x0280u, 0x02ffu, 2u, 8u, 2u, 660u, 2u, 472u, 2u, 1378u, 0u, "", ""},
    {"FCLASS.F_TO_D", "FCLASS", "FCLASS.X(z:S/D) Fn(f), Dn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FCLASS", "unprivileged", 0xf65u, 0xf65u, 0x0300u, 0x03ffu, 2u, 8u, 2u, 662u, 3u, 474u, 2u, 1378u, 0u, "", ""},
    {"FMOV.F_TO_F", "FMOV", "FMOV.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FMOV", "unprivileged", 0xf65u, 0xf65u, 0x0400u, 0x05ffu, 2u, 8u, 2u, 665u, 3u, 476u, 2u, 1378u, 0u, "", ""},
    {"FCVT.F_TO_D", "FCVT", "FCVT Fn(f), Dn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FCVT_FCVTU.FCVT", "unprivileged", 0xf65u, 0xf65u, 0x0600u, 0x067fu, 2u, 8u, 2u, 668u, 2u, 478u, 2u, 1378u, 0u, "", ""},
    {"FCVTU.D_TO_F", "FCVTU", "FCVTU Dn(d), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FCVT_FCVTU.FCVTU", "unprivileged", 0xf65u, 0xf65u, 0x0680u, 0x06ffu, 2u, 8u, 2u, 670u, 2u, 480u, 2u, 1378u, 0u, "", ""},
    {"FCVT.F_TO_F", "FCVT", "FCVT Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FCVT_FCVTU.FCVT", "unprivileged", 0xf65u, 0xf65u, 0x0700u, 0x07ffu, 2u, 8u, 2u, 672u, 2u, 482u, 2u, 1378u, 0u, "", ""},
    {"FCMP.EA_TO_F", "FCMP", "FCMP.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_COMPARE.FCMP", "unprivileged", 0xf65u, 0xf65u, 0x0800u, 0x0fffu, 2u, 8u, 2u, 674u, 3u, 484u, 2u, 1378u, 0u, "", ""},
    {"FTEST.EA", "FTEST", "FTEST.X(z:S/D) <ea(e)>", BEDROCK_FORM_EXTENDED, "fpu", "FP_COMPARE.FTEST", "unprivileged", 0xf65u, 0xf65u, 0x1000u, 0x107fu, 2u, 8u, 2u, 677u, 2u, 486u, 1u, 1378u, 0u, "", ""},
    {"FCVTU.F_TO_D", "FCVTU", "FCVTU Fn(f), Dn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FCVT_FCVTU.FCVTU", "unprivileged", 0xf65u, 0xf65u, 0x1080u, 0x10ffu, 2u, 8u, 2u, 679u, 2u, 487u, 2u, 1378u, 0u, "", ""},
    {"FCVTU.F_TO_F", "FCVTU", "FCVTU Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FCVT_FCVTU.FCVTU", "unprivileged", 0xf65u, 0xf65u, 0x1100u, 0x11ffu, 2u, 8u, 2u, 681u, 2u, 489u, 2u, 1378u, 0u, "", ""},
    {"FMOV.EA_TO_F", "FMOV", "FMOV.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FMOV", "unprivileged", 0xf65u, 0xf65u, 0x1800u, 0x1fffu, 2u, 8u, 2u, 683u, 3u, 491u, 2u, 1378u, 0u, "", ""},
    {"FMOV.F_TO_EA", "FMOV", "FMOV.X(z:S/D) Fn(f), <ea(e)>", BEDROCK_FORM_EXTENDED, "fpu", "FMOV", "unprivileged", 0xf65u, 0xf65u, 0x2000u, 0x27ffu, 2u, 8u, 2u, 686u, 3u, 493u, 2u, 1378u, 0u, "", ""},
    {"FABS.EA_TO_F", "FABS", "FABS.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_UNARY.FABS", "unprivileged", 0xf66u, 0xf66u, 0x0000u, 0x07ffu, 2u, 8u, 2u, 689u, 3u, 495u, 2u, 1378u, 0u, "", ""},
    {"FABS.F_TO_EA", "FABS", "FABS.X(z:S/D) Fn(f), <ea(e)>", BEDROCK_FORM_EXTENDED, "fpu", "FP_UNARY.FABS", "unprivileged", 0xf66u, 0xf66u, 0x0800u, 0x0fffu, 2u, 8u, 2u, 692u, 3u, 497u, 2u, 1378u, 0u, "", ""},
    {"FADD.EA_TO_F", "FADD", "FADD.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_ARITH.FADD", "unprivileged", 0xf66u, 0xf66u, 0x1000u, 0x17ffu, 2u, 8u, 2u, 695u, 3u, 499u, 2u, 1378u, 0u, "", ""},
    {"FABS.F_TO_F", "FABS", "FABS.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_UNARY.FABS", "unprivileged", 0xf67u, 0xf67u, 0x0000u, 0x01ffu, 2u, 8u, 2u, 698u, 3u, 501u, 2u, 1378u, 0u, "", ""},
    {"FADD.F_TO_F", "FADD", "FADD.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_ARITH.FADD", "unprivileged", 0xf67u, 0xf67u, 0x0200u, 0x03ffu, 2u, 8u, 2u, 701u, 3u, 503u, 2u, 1378u, 0u, "", ""},
    {"FBNDII.F_TO_EA_TO_F", "FBNDII", "FBNDII.X(z:S/D) Fn(l), <ea(e)>, Fn(h)", BEDROCK_FORM_EXTENDED, "fpu", "FP_BOUNDS.FBNDII", "unprivileged", 0xf67u, 0xf67u, 0x0400u, 0x0400u, 3u, 8u, 3u, 704u, 4u, 505u, 3u, 1378u, 0u, "", ""},
    {"FBNDII.F_TO_F_TO_F", "FBNDII", "FBNDII.X(z:S/D) Fn(l), Fn(x), Fn(h)", BEDROCK_FORM_EXTENDED, "fpu", "FP_BOUNDS.FBNDII", "unprivileged", 0xf67u, 0xf67u, 0x0401u, 0x0401u, 3u, 8u, 3u, 708u, 4u, 508u, 3u, 1378u, 0u, "", ""},
    {"FBNDIX.F_TO_EA_TO_F", "FBNDIX", "FBNDIX.X(z:S/D) Fn(l), <ea(e)>, Fn(h)", BEDROCK_FORM_EXTENDED, "fpu", "FP_BOUNDS.FBNDIX", "unprivileged", 0xf67u, 0xf67u, 0x0402u, 0x0402u, 3u, 8u, 3u, 712u, 4u, 511u, 3u, 1378u, 0u, "", ""},
    {"FBNDIX.F_TO_F_TO_F", "FBNDIX", "FBNDIX.X(z:S/D) Fn(l), Fn(x), Fn(h)", BEDROCK_FORM_EXTENDED, "fpu", "FP_BOUNDS.FBNDIX", "unprivileged", 0xf67u, 0xf67u, 0x0403u, 0x0403u, 3u, 8u, 3u, 716u, 4u, 514u, 3u, 1378u, 0u, "", ""},
    {"FBNDXI.F_TO_EA_TO_F", "FBNDXI", "FBNDXI.X(z:S/D) Fn(l), <ea(e)>, Fn(h)", BEDROCK_FORM_EXTENDED, "fpu", "FP_BOUNDS.FBNDXI", "unprivileged", 0xf67u, 0xf67u, 0x0404u, 0x0404u, 3u, 8u, 3u, 720u, 4u, 517u, 3u, 1378u, 0u, "", ""},
    {"FBNDXI.F_TO_F_TO_F", "FBNDXI", "FBNDXI.X(z:S/D) Fn(l), Fn(x), Fn(h)", BEDROCK_FORM_EXTENDED, "fpu", "FP_BOUNDS.FBNDXI", "unprivileged", 0xf67u, 0xf67u, 0x0405u, 0x0405u, 3u, 8u, 3u, 724u, 4u, 520u, 3u, 1378u, 0u, "", ""},
    {"FBNDXX.F_TO_EA_TO_F", "FBNDXX", "FBNDXX.X(z:S/D) Fn(l), <ea(e)>, Fn(h)", BEDROCK_FORM_EXTENDED, "fpu", "FP_BOUNDS.FBNDXX", "unprivileged", 0xf67u, 0xf67u, 0x0406u, 0x0406u, 3u, 8u, 3u, 728u, 4u, 523u, 3u, 1378u, 0u, "", ""},
    {"FBNDXX.F_TO_F_TO_F", "FBNDXX", "FBNDXX.X(z:S/D) Fn(l), Fn(x), Fn(h)", BEDROCK_FORM_EXTENDED, "fpu", "FP_BOUNDS.FBNDXX", "unprivileged", 0xf67u, 0xf67u, 0x0407u, 0x0407u, 3u, 8u, 3u, 732u, 4u, 526u, 3u, 1378u, 0u, "", ""},
    {"FCOPYSIGN.F_TO_F_TO_F", "FCOPYSIGN", "FCOPYSIGN.X(z:S/D) Fn(f), Fn(F), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FCOPYSIGN", "unprivileged", 0xf67u, 0xf67u, 0x0408u, 0x0408u, 3u, 8u, 3u, 736u, 4u, 529u, 3u, 1378u, 0u, "", ""},
    {"FMADD.EA_TO_F_TO_F", "FMADD", "FMADD.X(z:S/D) <ea(e)>, Fn(r), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_FMA.FMADD", "unprivileged", 0xf67u, 0xf67u, 0x0409u, 0x0409u, 3u, 8u, 3u, 740u, 4u, 532u, 3u, 1378u, 0u, "", ""},
    {"FMADD.F_TO_EA_TO_F", "FMADD", "FMADD.X(z:S/D) Fn(l), <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_FMA.FMADD", "unprivileged", 0xf67u, 0xf67u, 0x040au, 0x040au, 3u, 8u, 3u, 744u, 4u, 535u, 3u, 1378u, 0u, "", ""},
    {"FMADD.F_TO_F_TO_F", "FMADD", "FMADD.X(z:S/D) Fn(l), Fn(r), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_FMA.FMADD", "unprivileged", 0xf67u, 0xf67u, 0x040bu, 0x040bu, 3u, 8u, 3u, 748u, 4u, 538u, 3u, 1378u, 0u, "", ""},
    {"FMSUB.EA_TO_F_TO_F", "FMSUB", "FMSUB.X(z:S/D) <ea(e)>, Fn(r), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_FMA.FMSUB", "unprivileged", 0xf67u, 0xf67u, 0x040cu, 0x040cu, 3u, 8u, 3u, 752u, 4u, 541u, 3u, 1378u, 0u, "", ""},
    {"FMSUB.F_TO_EA_TO_F", "FMSUB", "FMSUB.X(z:S/D) Fn(l), <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_FMA.FMSUB", "unprivileged", 0xf67u, 0xf67u, 0x040du, 0x040du, 3u, 8u, 3u, 756u, 4u, 544u, 3u, 1378u, 0u, "", ""},
    {"FMSUB.F_TO_F_TO_F", "FMSUB", "FMSUB.X(z:S/D) Fn(l), Fn(r), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_FMA.FMSUB", "unprivileged", 0xf67u, 0xf67u, 0x040eu, 0x040eu, 3u, 8u, 3u, 760u, 4u, 547u, 3u, 1378u, 0u, "", ""},
    {"FNMADD.EA_TO_F_TO_F", "FNMADD", "FNMADD.X(z:S/D) <ea(e)>, Fn(r), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_FMA.FNMADD", "unprivileged", 0xf67u, 0xf67u, 0x040fu, 0x040fu, 3u, 8u, 3u, 764u, 4u, 550u, 3u, 1378u, 0u, "", ""},
    {"FCLR.F", "FCLR", "FCLR Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FCLR", "unprivileged", 0xf67u, 0xf67u, 0x0410u, 0x041fu, 2u, 8u, 2u, 768u, 1u, 553u, 1u, 1378u, 0u, "", ""},
    {"FNMADD.F_TO_EA_TO_F", "FNMADD", "FNMADD.X(z:S/D) Fn(l), <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_FMA.FNMADD", "unprivileged", 0xf67u, 0xf67u, 0x0420u, 0x0420u, 3u, 8u, 3u, 769u, 4u, 554u, 3u, 1378u, 0u, "", ""},
    {"FNMADD.F_TO_F_TO_F", "FNMADD", "FNMADD.X(z:S/D) Fn(l), Fn(r), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_FMA.FNMADD", "unprivileged", 0xf67u, 0xf67u, 0x0421u, 0x0421u, 3u, 8u, 3u, 773u, 4u, 557u, 3u, 1378u, 0u, "", ""},
    {"FNMSUB.EA_TO_F_TO_F", "FNMSUB", "FNMSUB.X(z:S/D) <ea(e)>, Fn(r), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_FMA.FNMSUB", "unprivileged", 0xf67u, 0xf67u, 0x0422u, 0x0422u, 3u, 8u, 3u, 777u, 4u, 560u, 3u, 1378u, 0u, "", ""},
    {"FNMSUB.F_TO_EA_TO_F", "FNMSUB", "FNMSUB.X(z:S/D) Fn(l), <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_FMA.FNMSUB", "unprivileged", 0xf67u, 0xf67u, 0x0423u, 0x0423u, 3u, 8u, 3u, 781u, 4u, 563u, 3u, 1378u, 0u, "", ""},
    {"FNMSUB.F_TO_F_TO_F", "FNMSUB", "FNMSUB.X(z:S/D) Fn(l), Fn(r), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_FMA.FNMSUB", "unprivileged", 0xf67u, 0xf67u, 0x0424u, 0x0424u, 3u, 8u, 3u, 785u, 4u, 566u, 3u, 1378u, 0u, "", ""},
    {"FPOPM.BITMAP", "FPOPM", "FPOPM <bitmap>", BEDROCK_FORM_EXTENDED, "fpu", "FPUSHM_FPOPM.FPOPM", "unprivileged", 0xf67u, 0xf67u, 0x0425u, 0x0425u, 3u, 8u, 3u, 789u, 1u, 569u, 1u, 1378u, 0u, "", ""},
    {"FPUSHM.BITMAP", "FPUSHM", "FPUSHM <bitmap>", BEDROCK_FORM_EXTENDED, "fpu", "FPUSHM_FPOPM.FPUSHM", "unprivileged", 0xf67u, 0xf67u, 0x0426u, 0x0426u, 3u, 8u, 3u, 790u, 1u, 570u, 1u, 1378u, 0u, "", ""},
    {"FCLR.EA", "FCLR", "FCLR <ea(e)>", BEDROCK_FORM_EXTENDED, "fpu", "FCLR", "unprivileged", 0xf67u, 0xf67u, 0x0440u, 0x047fu, 2u, 8u, 2u, 791u, 1u, 571u, 1u, 1378u, 0u, "", ""},
    {"FXCHG.F_TO_F", "FXCHG", "FXCHG Fn(l), Fn(r)", BEDROCK_FORM_EXTENDED, "fpu", "FXCHG", "unprivileged", 0xf67u, 0xf67u, 0x0500u, 0x05ffu, 2u, 8u, 2u, 792u, 2u, 572u, 2u, 1378u, 0u, "", ""},
    {"FCEIL.F_TO_F", "FCEIL", "FCEIL.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FCEIL", "unprivileged", 0xf67u, 0xf67u, 0x0600u, 0x07ffu, 2u, 8u, 2u, 794u, 3u, 574u, 2u, 1378u, 0u, "", ""},
    {"FCEIL.EA_TO_F", "FCEIL", "FCEIL.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FCEIL", "unprivileged", 0xf67u, 0xf67u, 0x0800u, 0x0fffu, 2u, 8u, 2u, 797u, 3u, 576u, 2u, 1378u, 0u, "", ""},
    {"FCEIL.F_TO_EA", "FCEIL", "FCEIL.X(z:S/D) Fn(f), <ea(e)>", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FCEIL", "unprivileged", 0xf67u, 0xf67u, 0x1000u, 0x17ffu, 2u, 8u, 2u, 800u, 3u, 578u, 2u, 1378u, 0u, "", ""},
    {"FDIV.EA_TO_F", "FDIV", "FDIV.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_ARITH.FDIV", "unprivileged", 0xf67u, 0xf67u, 0x1800u, 0x1fffu, 2u, 8u, 2u, 803u, 3u, 580u, 2u, 1378u, 0u, "", ""},
    {"FDIV.F_TO_F", "FDIV", "FDIV.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_ARITH.FDIV", "unprivileged", 0xf67u, 0xf67u, 0x2000u, 0x21ffu, 2u, 8u, 2u, 806u, 3u, 582u, 2u, 1378u, 0u, "", ""},
    {"FFLOOR.F_TO_F", "FFLOOR", "FFLOOR.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FFLOOR", "unprivileged", 0xf67u, 0xf67u, 0x2200u, 0x23ffu, 2u, 8u, 2u, 809u, 3u, 584u, 2u, 1378u, 0u, "", ""},
    {"FGETEXP.F_TO_F", "FGETEXP", "FGETEXP.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_EXP_MAN_SCALE.FGETEXP", "unprivileged", 0xf67u, 0xf67u, 0x2400u, 0x25ffu, 2u, 8u, 2u, 812u, 3u, 586u, 2u, 1378u, 0u, "", ""},
    {"FGETMAN.F_TO_F", "FGETMAN", "FGETMAN.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_EXP_MAN_SCALE.FGETMAN", "unprivileged", 0xf67u, 0xf67u, 0x2600u, 0x27ffu, 2u, 8u, 2u, 815u, 3u, 588u, 2u, 1378u, 0u, "", ""},
    {"FFLOOR.EA_TO_F", "FFLOOR", "FFLOOR.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FFLOOR", "unprivileged", 0xf67u, 0xf67u, 0x2800u, 0x2fffu, 2u, 8u, 2u, 818u, 3u, 590u, 2u, 1378u, 0u, "", ""},
    {"FFLOOR.F_TO_EA", "FFLOOR", "FFLOOR.X(z:S/D) Fn(f), <ea(e)>", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FFLOOR", "unprivileged", 0xf67u, 0xf67u, 0x3000u, 0x37ffu, 2u, 8u, 2u, 821u, 3u, 592u, 2u, 1378u, 0u, "", ""},
    {"FGETEXP.EA_TO_F", "FGETEXP", "FGETEXP.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_EXP_MAN_SCALE.FGETEXP", "unprivileged", 0xf67u, 0xf67u, 0x3800u, 0x3fffu, 2u, 8u, 2u, 824u, 3u, 594u, 2u, 1378u, 0u, "", ""},
    {"FGETMAN.EA_TO_F", "FGETMAN", "FGETMAN.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_EXP_MAN_SCALE.FGETMAN", "unprivileged", 0xf67u, 0xf67u, 0x4000u, 0x47ffu, 2u, 8u, 2u, 827u, 3u, 596u, 2u, 1378u, 0u, "", ""},
    {"FINT.EA_TO_F", "FINT", "FINT.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FINT", "unprivileged", 0xf67u, 0xf67u, 0x4800u, 0x4fffu, 2u, 8u, 2u, 830u, 3u, 598u, 2u, 1378u, 0u, "", ""},
    {"FINT.F_TO_EA", "FINT", "FINT.X(z:S/D) Fn(f), <ea(e)>", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FINT", "unprivileged", 0xf67u, 0xf67u, 0x5000u, 0x57ffu, 2u, 8u, 2u, 833u, 3u, 600u, 2u, 1378u, 0u, "", ""},
    {"FINT.F_TO_F", "FINT", "FINT.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FINT", "unprivileged", 0xf67u, 0xf67u, 0x5800u, 0x59ffu, 2u, 8u, 2u, 836u, 3u, 602u, 2u, 1378u, 0u, "", ""},
    {"FINTRZ.F_TO_F", "FINTRZ", "FINTRZ.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FINTRZ", "unprivileged", 0xf67u, 0xf67u, 0x5a00u, 0x5bffu, 2u, 8u, 2u, 839u, 3u, 604u, 2u, 1378u, 0u, "", ""},
    {"FMAX.F_TO_F", "FMAX", "FMAX.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FMIN_FMAX.FMAX", "unprivileged", 0xf67u, 0xf67u, 0x5c00u, 0x5dffu, 2u, 8u, 2u, 842u, 3u, 606u, 2u, 1378u, 0u, "", ""},
    {"FMIN.F_TO_F", "FMIN", "FMIN.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FMIN_FMAX.FMIN", "unprivileged", 0xf67u, 0xf67u, 0x5e00u, 0x5fffu, 2u, 8u, 2u, 845u, 3u, 608u, 2u, 1378u, 0u, "", ""},
    {"FINTRZ.EA_TO_F", "FINTRZ", "FINTRZ.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FINTRZ", "unprivileged", 0xf67u, 0xf67u, 0x6000u, 0x67ffu, 2u, 8u, 2u, 848u, 3u, 610u, 2u, 1378u, 0u, "", ""},
    {"FINTRZ.F_TO_EA", "FINTRZ", "FINTRZ.X(z:S/D) Fn(f), <ea(e)>", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FINTRZ", "unprivileged", 0xf67u, 0xf67u, 0x6800u, 0x6fffu, 2u, 8u, 2u, 851u, 3u, 612u, 2u, 1378u, 0u, "", ""},
    {"FMAX.EA_TO_F", "FMAX", "FMAX.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FMIN_FMAX.FMAX", "unprivileged", 0xf67u, 0xf67u, 0x7000u, 0x77ffu, 2u, 8u, 2u, 854u, 3u, 614u, 2u, 1378u, 0u, "", ""},
    {"FMIN.EA_TO_F", "FMIN", "FMIN.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FMIN_FMAX.FMIN", "unprivileged", 0xf67u, 0xf67u, 0x7800u, 0x7fffu, 2u, 8u, 2u, 857u, 3u, 616u, 2u, 1378u, 0u, "", ""},
    {"FMOD.EA_TO_F", "FMOD", "FMOD.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_ARITH.FMOD", "unprivileged", 0xf67u, 0xf67u, 0x8000u, 0x87ffu, 2u, 8u, 2u, 860u, 3u, 618u, 2u, 1378u, 0u, "", ""},
    {"FMOD.F_TO_F", "FMOD", "FMOD.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_ARITH.FMOD", "unprivileged", 0xf67u, 0xf67u, 0x8800u, 0x89ffu, 2u, 8u, 2u, 863u, 3u, 620u, 2u, 1378u, 0u, "", ""},
    {"FMUL.F_TO_F", "FMUL", "FMUL.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_ARITH.FMUL", "unprivileged", 0xf67u, 0xf67u, 0x8a00u, 0x8bffu, 2u, 8u, 2u, 866u, 3u, 622u, 2u, 1378u, 0u, "", ""},
    {"FNEG.F_TO_F", "FNEG", "FNEG.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_UNARY.FNEG", "unprivileged", 0xf67u, 0xf67u, 0x8c00u, 0x8dffu, 2u, 8u, 2u, 869u, 3u, 624u, 2u, 1378u, 0u, "", ""},
    {"FREM.F_TO_F", "FREM", "FREM.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_ARITH.FREM", "unprivileged", 0xf67u, 0xf67u, 0x8e00u, 0x8fffu, 2u, 8u, 2u, 872u, 3u, 626u, 2u, 1378u, 0u, "", ""},
    {"FMUL.EA_TO_F", "FMUL", "FMUL.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_ARITH.FMUL", "unprivileged", 0xf67u, 0xf67u, 0x9000u, 0x97ffu, 2u, 8u, 2u, 875u, 3u, 628u, 2u, 1378u, 0u, "", ""},
    {"FNEG.EA_TO_F", "FNEG", "FNEG.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_UNARY.FNEG", "unprivileged", 0xf67u, 0xf67u, 0x9800u, 0x9fffu, 2u, 8u, 2u, 878u, 3u, 630u, 2u, 1378u, 0u, "", ""},
    {"FNEG.F_TO_EA", "FNEG", "FNEG.X(z:S/D) Fn(f), <ea(e)>", BEDROCK_FORM_EXTENDED, "fpu", "FP_UNARY.FNEG", "unprivileged", 0xf67u, 0xf67u, 0xa000u, 0xa7ffu, 2u, 8u, 2u, 881u, 3u, 632u, 2u, 1378u, 0u, "", ""},
    {"FREM.EA_TO_F", "FREM", "FREM.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_ARITH.FREM", "unprivileged", 0xf67u, 0xf67u, 0xa800u, 0xafffu, 2u, 8u, 2u, 884u, 3u, 634u, 2u, 1378u, 0u, "", ""},
    {"FROUND.EA_TO_F", "FROUND", "FROUND.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FROUND", "unprivileged", 0xf67u, 0xf67u, 0xb000u, 0xb7ffu, 2u, 8u, 2u, 887u, 3u, 636u, 2u, 1378u, 0u, "", ""},
    {"FROUND.F_TO_EA", "FROUND", "FROUND.X(z:S/D) Fn(f), <ea(e)>", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FROUND", "unprivileged", 0xf67u, 0xf67u, 0xb800u, 0xbfffu, 2u, 8u, 2u, 890u, 3u, 638u, 2u, 1378u, 0u, "", ""},
    {"FROUND.F_TO_F", "FROUND", "FROUND.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FROUND", "unprivileged", 0xf67u, 0xf67u, 0xc000u, 0xc1ffu, 2u, 8u, 2u, 893u, 3u, 640u, 2u, 1378u, 0u, "", ""},
    {"FSCALE.F_TO_F", "FSCALE", "FSCALE.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_EXP_MAN_SCALE.FSCALE", "unprivileged", 0xf67u, 0xf67u, 0xc200u, 0xc3ffu, 2u, 8u, 2u, 896u, 3u, 642u, 2u, 1378u, 0u, "", ""},
    {"FSQRT.F_TO_F", "FSQRT", "FSQRT.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_UNARY.FSQRT", "unprivileged", 0xf67u, 0xf67u, 0xc400u, 0xc5ffu, 2u, 8u, 2u, 899u, 3u, 644u, 2u, 1378u, 0u, "", ""},
    {"FSUB.F_TO_F", "FSUB", "FSUB.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_ARITH.FSUB", "unprivileged", 0xf67u, 0xf67u, 0xc600u, 0xc7ffu, 2u, 8u, 2u, 902u, 3u, 646u, 2u, 1378u, 0u, "", ""},
    {"FSCALE.EA_TO_F", "FSCALE", "FSCALE.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_EXP_MAN_SCALE.FSCALE", "unprivileged", 0xf67u, 0xf67u, 0xc800u, 0xcfffu, 2u, 8u, 2u, 905u, 3u, 648u, 2u, 1378u, 0u, "", ""},
    {"FSQRT.EA_TO_F", "FSQRT", "FSQRT.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_UNARY.FSQRT", "unprivileged", 0xf67u, 0xf67u, 0xd000u, 0xd7ffu, 2u, 8u, 2u, 908u, 3u, 650u, 2u, 1378u, 0u, "", ""},
    {"FSQRT.F_TO_EA", "FSQRT", "FSQRT.X(z:S/D) Fn(f), <ea(e)>", BEDROCK_FORM_EXTENDED, "fpu", "FP_UNARY.FSQRT", "unprivileged", 0xf67u, 0xf67u, 0xd800u, 0xdfffu, 2u, 8u, 2u, 911u, 3u, 652u, 2u, 1378u, 0u, "", ""},
    {"FSUB.EA_TO_F", "FSUB", "FSUB.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_ARITH.FSUB", "unprivileged", 0xf67u, 0xf67u, 0xe000u, 0xe7ffu, 2u, 8u, 2u, 914u, 3u, 654u, 2u, 1378u, 0u, "", ""},
    {"FTRUNC.EA_TO_F", "FTRUNC", "FTRUNC.X(z:S/D) <ea(e)>, Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FTRUNC", "unprivileged", 0xf67u, 0xf67u, 0xe800u, 0xefffu, 2u, 8u, 2u, 917u, 3u, 656u, 2u, 1378u, 0u, "", ""},
    {"FTRUNC.F_TO_EA", "FTRUNC", "FTRUNC.X(z:S/D) Fn(f), <ea(e)>", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FTRUNC", "unprivileged", 0xf67u, 0xf67u, 0xf000u, 0xf7ffu, 2u, 8u, 2u, 920u, 3u, 658u, 2u, 1378u, 0u, "", ""},
    {"FTRUNC.F_TO_F", "FTRUNC", "FTRUNC.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INTEGRAL_ROUND.FTRUNC", "unprivileged", 0xf67u, 0xf67u, 0xf800u, 0xf9ffu, 2u, 8u, 2u, 923u, 3u, 660u, 2u, 1378u, 0u, "", ""},
    {"FACOS.F_TO_F", "FACOS", "FACOS.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INV_TRIG.FACOS", "unprivileged", 0xf68u, 0xf68u, 0x0000u, 0x01ffu, 2u, 8u, 2u, 926u, 3u, 662u, 2u, 1378u, 0u, "", ""},
    {"FASIN.F_TO_F", "FASIN", "FASIN.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INV_TRIG.FASIN", "unprivileged", 0xf68u, 0xf68u, 0x0200u, 0x03ffu, 2u, 8u, 2u, 929u, 3u, 664u, 2u, 1378u, 0u, "", ""},
    {"FATAN.F_TO_F", "FATAN", "FATAN.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_INV_TRIG.FATAN", "unprivileged", 0xf68u, 0xf68u, 0x0400u, 0x05ffu, 2u, 8u, 2u, 932u, 3u, 666u, 2u, 1378u, 0u, "", ""},
    {"FATANH.F_TO_F", "FATANH", "FATANH.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_HYPERBOLIC.FATANH", "unprivileged", 0xf68u, 0xf68u, 0x0600u, 0x07ffu, 2u, 8u, 2u, 935u, 3u, 668u, 2u, 1378u, 0u, "", ""},
    {"FCOS.F_TO_F", "FCOS", "FCOS.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_TRIG.FCOS", "unprivileged", 0xf68u, 0xf68u, 0x0800u, 0x09ffu, 2u, 8u, 2u, 938u, 3u, 670u, 2u, 1378u, 0u, "", ""},
    {"FCOSH.F_TO_F", "FCOSH", "FCOSH.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_HYPERBOLIC.FCOSH", "unprivileged", 0xf68u, 0xf68u, 0x0a00u, 0x0bffu, 2u, 8u, 2u, 941u, 3u, 672u, 2u, 1378u, 0u, "", ""},
    {"FETOX.F_TO_F", "FETOX", "FETOX.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_EXP.FETOX", "unprivileged", 0xf68u, 0xf68u, 0x0c00u, 0x0dffu, 2u, 8u, 2u, 944u, 3u, 674u, 2u, 1378u, 0u, "", ""},
    {"FETOXM1.F_TO_F", "FETOXM1", "FETOXM1.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_EXP.FETOXM1", "unprivileged", 0xf68u, 0xf68u, 0x0e00u, 0x0fffu, 2u, 8u, 2u, 947u, 3u, 676u, 2u, 1378u, 0u, "", ""},
    {"FLOG10.F_TO_F", "FLOG10", "FLOG10.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_LOG.FLOG10", "unprivileged", 0xf68u, 0xf68u, 0x1000u, 0x11ffu, 2u, 8u, 2u, 950u, 3u, 678u, 2u, 1378u, 0u, "", ""},
    {"FLOG2.F_TO_F", "FLOG2", "FLOG2.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_LOG.FLOG2", "unprivileged", 0xf68u, 0xf68u, 0x1200u, 0x13ffu, 2u, 8u, 2u, 953u, 3u, 680u, 2u, 1378u, 0u, "", ""},
    {"FLOGN.F_TO_F", "FLOGN", "FLOGN.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_LOG.FLOGN", "unprivileged", 0xf68u, 0xf68u, 0x1400u, 0x15ffu, 2u, 8u, 2u, 956u, 3u, 682u, 2u, 1378u, 0u, "", ""},
    {"FLOGNP1.F_TO_F", "FLOGNP1", "FLOGNP1.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_LOG.FLOGNP1", "unprivileged", 0xf68u, 0xf68u, 0x1600u, 0x17ffu, 2u, 8u, 2u, 959u, 3u, 684u, 2u, 1378u, 0u, "", ""},
    {"FSIN.F_TO_F", "FSIN", "FSIN.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_TRIG.FSIN", "unprivileged", 0xf68u, 0xf68u, 0x1800u, 0x19ffu, 2u, 8u, 2u, 962u, 3u, 686u, 2u, 1378u, 0u, "", ""},
    {"FSINCOS.F_TO_F", "FSINCOS", "FSINCOS.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_TRIG.FSINCOS", "unprivileged", 0xf68u, 0xf68u, 0x1a00u, 0x1bffu, 2u, 8u, 2u, 965u, 3u, 688u, 2u, 1378u, 0u, "", ""},
    {"FSINH.F_TO_F", "FSINH", "FSINH.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_HYPERBOLIC.FSINH", "unprivileged", 0xf68u, 0xf68u, 0x1c00u, 0x1dffu, 2u, 8u, 2u, 968u, 3u, 690u, 2u, 1378u, 0u, "", ""},
    {"FTAN.F_TO_F", "FTAN", "FTAN.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_TRIG.FTAN", "unprivileged", 0xf68u, 0xf68u, 0x1e00u, 0x1fffu, 2u, 8u, 2u, 971u, 3u, 692u, 2u, 1378u, 0u, "", ""},
    {"FTANH.F_TO_F", "FTANH", "FTANH.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_HYPERBOLIC.FTANH", "unprivileged", 0xf68u, 0xf68u, 0x2000u, 0x21ffu, 2u, 8u, 2u, 974u, 3u, 694u, 2u, 1378u, 0u, "", ""},
    {"FTENTOX.F_TO_F", "FTENTOX", "FTENTOX.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_EXP.FTENTOX", "unprivileged", 0xf68u, 0xf68u, 0x2200u, 0x23ffu, 2u, 8u, 2u, 977u, 3u, 696u, 2u, 1378u, 0u, "", ""},
    {"FTWOTOX.F_TO_F", "FTWOTOX", "FTWOTOX.X(z:S/D) Fn(f), Fn(d)", BEDROCK_FORM_EXTENDED, "fpu", "FP_EXP.FTWOTOX", "unprivileged", 0xf68u, 0xf68u, 0x2400u, 0x25ffu, 2u, 8u, 2u, 980u, 3u, 698u, 2u, 1378u, 0u, "", ""},
    {"REPG.D_TO_IMM", "REPG", "REPG Dn(d), imm16", BEDROCK_FORM_COMPACT, "control_flow", "REPG", "unprivileged", 0xf70u, 0xf77u, 0x0000u, 0x0000u, 2u, 2u, 2u, 983u, 1u, 700u, 2u, 1378u, 0u, "", ""},
    {"ILLEGAL", "ILLEGAL", "ILLEGAL", BEDROCK_FORM_COMPACT, "system", "CORE_MISC.ILLEGAL", "any", 0xfffu, 0xfffu, 0x0000u, 0x0000u, 1u, 8u, 1u, 984u, 0u, 702u, 0u, 1378u, 0u, "", ""},
};

const size_t bedrock_forms_count = sizeof(bedrock_forms) / sizeof(bedrock_forms[0]);
const size_t bedrock_fields_count = sizeof(bedrock_fields) / sizeof(bedrock_fields[0]);
const size_t bedrock_operands_count = sizeof(bedrock_operands) / sizeof(bedrock_operands[0]);
const size_t bedrock_primary_values_count = sizeof(bedrock_primary_values) / sizeof(bedrock_primary_values[0]);
const size_t bedrock_condition_names_count = sizeof(bedrock_condition_names) / sizeof(bedrock_condition_names[0]);
const size_t bedrock_sreg_names_count = sizeof(bedrock_sreg_names) / sizeof(bedrock_sreg_names[0]);
const size_t bedrock_cr_names_count = sizeof(bedrock_cr_names) / sizeof(bedrock_cr_names[0]);
const size_t bedrock_ea_segment_names_count = sizeof(bedrock_ea_segment_names) / sizeof(bedrock_ea_segment_names[0]);
const size_t bedrock_memory_order_names_count = sizeof(bedrock_memory_order_names) / sizeof(bedrock_memory_order_names[0]);
const size_t bedrock_size_codes_count = sizeof(bedrock_size_codes) / sizeof(bedrock_size_codes[0]);
const size_t bedrock_size_kind_values_count = sizeof(bedrock_size_kind_values) / sizeof(bedrock_size_kind_values[0]);
const size_t bedrock_bitmap_ranges_count = sizeof(bedrock_bitmap_ranges) / sizeof(bedrock_bitmap_ranges[0]);

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
