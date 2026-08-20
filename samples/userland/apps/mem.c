#include "app.h"

#define LOCAL_SIZE 16u

u32 app_main(void) {
  volatile u8 local[LOCAL_SIZE];
  u32 checksum = 0x5au;

  for (u32 i = 0u; i < LOCAL_SIZE; i++) {
    local[i] = (u8)((i * 17u + 3u) & 0xffu);
  }

  for (u32 i = 0u; i < LOCAL_SIZE; i++) {
    u32 value = local[LOCAL_SIZE - 1u - i];
    checksum = app_rotl8(checksum + (value ^ (i * 9u)) + i, 1u);
  }

  u32 result = checksum & 0xffu;
  app_user_result(2u, result);
  app_user_sum(result);
  app_puts("MEM FIRST ");
  app_put_hex8(local[0]);
  app_puts(" LAST ");
  app_put_hex8(local[LOCAL_SIZE - 1u]);
  app_puts(" CHK ");
  app_put_hex8(result);
  app_put_char('\n');
  return result;
}
