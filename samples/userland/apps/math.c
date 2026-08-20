#include "app.h"

u32 app_main(void) {
  u32 a = 1u;
  u32 b = 1u;
  u32 checksum = 0x42u;

  for (u32 i = 0; i < 24u; i++) {
    u32 next = a + b;
    u32 mixed = (next * 17u) ^ (a * 5u) ^ (b * 3u) ^ (i * 29u);
    a = b;
    b = next;
    checksum = app_rotl8(checksum ^ mixed ^ (next >> 1), (i & 3u) + 1u);
  }

  u32 result = (checksum ^ a ^ b) & 0xffu;
  app_user_result(0u, result);
  app_user_sum(result);
  app_puts("MATH FIB ");
  app_put_hex8(b);
  app_puts(" MIX ");
  app_put_hex8(checksum);
  app_puts(" RES ");
  app_put_hex8(result);
  app_put_char('\n');
  return result;
}
