#include "app.h"

static u8 hex_digit(u32 value) {
  value &= 0x0fu;
  return (u8)(value < 10u ? ('0' + value) : ('A' + value - 10u));
}

void _start(void) {
  u32 code = app_main();
  br_exit(code);
  for (;;) {
  }
}

void app_put_char(u8 ch) {
  br_syscall(SYSCALL_PACK(SYSCALL_TTY_PUT_CHAR, ch));
}

void app_puts(const char *text) {
  br_syscall(SYSCALL_PACK(SYSCALL_TTY_PUTS, (u32)(u64)text));
}

void app_put_hex8(u32 value) {
  app_put_char(hex_digit(value >> 4));
  app_put_char(hex_digit(value));
}

void app_payload(u32 value) {
  br_syscall(SYSCALL_PACK(SYSCALL_PUT, value & 0xffu));
}

void app_yield(u32 ticket) {
  br_syscall(SYSCALL_PACK(SYSCALL_YIELD, ticket));
}

void app_user_sum(u32 value) {
  br_syscall(SYSCALL_PACK(SYSCALL_USER_SUM, value & 0xffu));
}

u32 app_user_result(u32 slot, u32 value) {
  return br_syscall(
      SYSCALL_PACK(SYSCALL_USER_RESULT, SYSCALL_PACK_RESULT(slot, value)));
}

u32 app_rotl8(u32 value, u32 amount) {
  amount &= 7u;
  value &= 0xffu;
  switch (amount) {
  case 0u:
    return value;
  case 1u:
    return ((value << 1u) | (value >> 7u)) & 0xffu;
  case 2u:
    return ((value << 2u) | (value >> 6u)) & 0xffu;
  case 3u:
    return ((value << 3u) | (value >> 5u)) & 0xffu;
  case 4u:
    return ((value << 4u) | (value >> 4u)) & 0xffu;
  case 5u:
    return ((value << 5u) | (value >> 3u)) & 0xffu;
  case 6u:
    return ((value << 6u) | (value >> 2u)) & 0xffu;
  default:
    return ((value << 7u) | (value >> 1u)) & 0xffu;
  }
}
