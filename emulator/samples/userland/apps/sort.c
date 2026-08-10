#include "app.h"

static const u8 SORT_INPUT[12] = {0x39, 0x02, 0xa7, 0x14, 0x88, 0x55,
                                  0x01, 0xfe, 0x73, 0x20, 0xcd, 0x46};

u32 app_main(void) {
  u8 values[12];
  for (u32 i = 0u; i < 12u; i++) {
    values[i] = SORT_INPUT[i];
  }

  for (u32 i = 1u; i < 12u; i++) {
    u8 key = values[i];
    u32 j = i;
    while (j != 0u && values[j - 1u] > key) {
      values[j] = values[j - 1u];
      j--;
    }
    values[j] = key;
  }

  u32 checksum = 0x95u;
  for (u32 i = 0u; i < 12u; i++) {
    checksum = app_rotl8(checksum ^ values[i] ^ (i * 19u), 2u);
  }

  u32 result = checksum & 0xffu;
  app_user_result(1u, result);
  app_user_sum(result);
  app_puts("SORT MIN ");
  app_put_hex8(values[0]);
  app_puts(" MAX ");
  app_put_hex8(values[11]);
  app_puts(" CHK ");
  app_put_hex8(result);
  app_put_char('\n');
  return result;
}
