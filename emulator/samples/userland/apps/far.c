#include "app.h"

#include <bedrocksysregintrin.h>

#define FAR_BANK_SIZE 4096u
#define FAR_INPUT_SIZE 64u
#define FAR_OUTPUT_OFFSET 128u
#define FAR_EXPECTED_CHECKSUM 0xaau

static volatile u8 far_bank[FAR_BANK_SIZE] __attribute__((aligned(4096)));

u32 app_main(void) {
  u64 base = (u64)&far_bank[0];
  u64 translated = __BEDROCK_SEGMENT_IMAGE_FOR_BASE(base, 0, 1, 0);
  u32 valid = app_segment_image_round_trip(translated) == translated;

  for (u32 i = 0; i < FAR_INPUT_SIZE; i++) {
    app_segment_write_u8(translated, i, (i * 37u + 11u) & 0xffu);
  }

  u32 checksum = 0x6du;
  for (u32 i = 0; i < FAR_INPUT_SIZE; i++) {
    u32 source = app_segment_read_u8(translated, FAR_INPUT_SIZE - 1u - i);
    u32 mask = app_rotl8(i * 13u + 7u, i & 7u);
    u32 transformed = (source ^ mask) & 0xffu;
    app_segment_write_u8(translated, FAR_OUTPUT_OFFSET + i, transformed);
    checksum = app_rotl8(checksum + transformed + i * 3u, 3u) ^
               app_segment_read_u8(translated, i);
  }
  checksum &= 0xffu;

  u32 first = app_segment_read_u8(translated, 0);
  u32 last = app_segment_read_u8(translated, FAR_INPUT_SIZE - 1u);
  u32 output_first = app_segment_read_u8(translated, FAR_OUTPUT_OFFSET);
  u32 output_last = app_segment_read_u8(
      translated, FAR_OUTPUT_OFFSET + FAR_INPUT_SIZE - 1u);
  valid = valid && first == 0x0bu && last == 0x26u &&
          output_first == 0x21u && output_last == 0x16u &&
          checksum == FAR_EXPECTED_CHECKSUM;

  app_user_result(7u, checksum);
  app_user_sum(checksum);
  app_puts("FAR IN ");
  app_put_hex8(first);
  app_put_char('/');
  app_put_hex8(last);
  app_puts(" OUT ");
  app_put_hex8(output_first);
  app_put_char('/');
  app_put_hex8(output_last);
  app_puts(" CHK ");
  app_put_hex8(checksum);
  app_put_char(' ');
  app_puts(valid ? "PASS\n" : "FAIL\n");
  return valid ? checksum : 0xffu;
}
