#ifndef __BEDROCKSYSREGINTRIN_H
#define __BEDROCKSYSREGINTRIN_H

#include <stdint.h>

typedef enum __bedrock_segment_register {
  __BEDROCK_SEG_CS = 0,
  __BEDROCK_SEG_DS = 1,
  __BEDROCK_SEG_SS = 2,
  __BEDROCK_SEG_GS0 = 3,
  __BEDROCK_SEG_GS1 = 4,
  __BEDROCK_SEG_GS2 = 5,
  __BEDROCK_SEG_GS3 = 6,
  __BEDROCK_SEG_GS4 = 7
} __bedrock_segment_register_t;

typedef enum __bedrock_control_register {
  __BEDROCK_CR_PTCR = 0x0000,
  __BEDROCK_CR_ASCR = 0x0001,
  __BEDROCK_CR_ICR = 0x0002,
  __BEDROCK_CR_SPC = 0x0100,
  __BEDROCK_CR_SCS = 0x0101,
  __BEDROCK_CR_SDS = 0x0102,
  __BEDROCK_CR_SSS0 = 0x0200,
  __BEDROCK_CR_SSP0 = 0x0201,
  __BEDROCK_CR_SSS1 = 0x0210,
  __BEDROCK_CR_SSP1 = 0x0211,
  __BEDROCK_CR_SSS2 = 0x0220,
  __BEDROCK_CR_SSP2 = 0x0221,
  __BEDROCK_CR_SSS3 = 0x0230,
  __BEDROCK_CR_SSP3 = 0x0231,
  __BEDROCK_CR_BOOTPC = 0x1000,
  __BEDROCK_CR_BOOTCFG = 0x1001,
  __BEDROCK_CR_PMC = 0x1100
} __bedrock_control_register_t;

static __inline__ void
__bedrock_write_status(uint16_t value)
{
  __builtin_bedrock_write_status(value);
}

#define __bedrock_read_control_register(selector) \
  __builtin_bedrock_read_control_register(selector)
#define __bedrock_write_control_register(selector, value) \
  __builtin_bedrock_write_control_register(selector, value)
#define __bedrock_read_segment_register(selector) \
  __builtin_bedrock_read_segment_register(selector)
#define __bedrock_write_segment_register(selector, image) \
  __builtin_bedrock_write_segment_register(selector, image)

#endif
