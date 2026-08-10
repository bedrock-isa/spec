#include "app.h"

static const u8 USER_PAYLOAD[APP_REQUEST_COUNT] = {
    0x24, 0xe0, 0x31, 0x5a, 0x83, 0xac, 0xd5, 0xfe,
    0x19, 0x42, 0x6b, 0x94, 0xbd, 0xe6, 0x0f, 0x38,
};

u32 app_main(void) {
  u32 mirror = 0x6du;
  for (u32 i = 0; i < APP_REQUEST_COUNT; i++) {
    u8 value = USER_PAYLOAD[i];
    mirror = ((mirror << 3) ^ value ^ (i * 29u)) & 0xffu;
    app_payload(value);
    if ((i & 3u) == 3u) {
      app_yield(i);
    }
  }

  app_user_sum(mirror);
  app_puts("DEMO SUM ");
  app_put_hex8(mirror);
  app_puts(" YIELD ");
  app_put_hex8(APP_REQUEST_COUNT / 4u);
  app_put_char('\n');
  return mirror & 0xffu;
}
