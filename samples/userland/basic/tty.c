#include "basic.h"

void tty_reset(void) {
  br_syscall(SYSCALL_PACK(SYSCALL_TTY_CLEAR, 0));
}

void tty_put_char(u8 ch) {
  br_syscall(SYSCALL_PACK(SYSCALL_TTY_PUT_CHAR, ch));
}

void tty_puts(const char *text) {
  br_syscall(SYSCALL_PACK(SYSCALL_TTY_PUTS, (u32)(u64)text));
}

static void tty_put_dec_place32(u32 *value, u32 place, u32 *started) {
  u32 digit = 0;
  while (*value >= place) {
    *value -= place;
    digit++;
  }
  if (digit != 0u || *started != 0u || place == 1u) {
    tty_put_char((u8)('0' + digit));
    *started = 1;
  }
}

static void tty_put_dec_place64(u64 *value, u64 place, u32 *started) {
  u32 digit = 0;
  while (*value >= place) {
    *value -= place;
    digit++;
  }
  if (digit != 0u || *started != 0u || place == 1ULL) {
    tty_put_char((u8)('0' + digit));
    *started = 1;
  }
}

static u64 g_tty_u64_value;
static u32 g_tty_u64_started;

void tty_put_u32_dec(u32 value) {
  u32 started = 0;
  tty_put_dec_place32(&value, 1000000000u, &started);
  tty_put_dec_place32(&value, 100000000u, &started);
  tty_put_dec_place32(&value, 10000000u, &started);
  tty_put_dec_place32(&value, 1000000u, &started);
  tty_put_dec_place32(&value, 100000u, &started);
  tty_put_dec_place32(&value, 10000u, &started);
  tty_put_dec_place32(&value, 1000u, &started);
  tty_put_dec_place32(&value, 100u, &started);
  tty_put_dec_place32(&value, 10u, &started);
  tty_put_dec_place32(&value, 1u, &started);
}

void tty_put_u64_dec(u64 value) {
  g_tty_u64_value = value;
  g_tty_u64_started = 0;
#define PUT_U64_PLACE(place)                                                   \
  tty_put_dec_place64(&g_tty_u64_value, (place), &g_tty_u64_started)
  PUT_U64_PLACE(10000000000000000000ULL);
  PUT_U64_PLACE(1000000000000000000ULL);
  PUT_U64_PLACE(100000000000000000ULL);
  PUT_U64_PLACE(10000000000000000ULL);
  PUT_U64_PLACE(1000000000000000ULL);
  PUT_U64_PLACE(100000000000000ULL);
  PUT_U64_PLACE(10000000000000ULL);
  PUT_U64_PLACE(1000000000000ULL);
  PUT_U64_PLACE(100000000000ULL);
  PUT_U64_PLACE(10000000000ULL);
  PUT_U64_PLACE(1000000000ULL);
  PUT_U64_PLACE(100000000ULL);
  PUT_U64_PLACE(10000000ULL);
  PUT_U64_PLACE(1000000ULL);
  PUT_U64_PLACE(100000ULL);
  PUT_U64_PLACE(10000ULL);
  PUT_U64_PLACE(1000ULL);
  PUT_U64_PLACE(100ULL);
  PUT_U64_PLACE(10ULL);
  PUT_U64_PLACE(1ULL);
#undef PUT_U64_PLACE
}

static u32 basic_poll_char(void) {
  u32 event = br_syscall(SYSCALL_PACK(SYSCALL_KBD_READ, 0));
  if (event == 0u) {
    return 0;
  }
  if ((event & KBD_EVENT_PRESSED) == 0u) {
    return 0;
  }
  if ((event & (KBD_EVENT_CTRL | KBD_EVENT_ALT | KBD_EVENT_COMMAND)) != 0u) {
    return 0;
  }

  u32 code = event & KBD_EVENT_CODE_MASK;
  if (code > 0xffu) {
    return 0;
  }
  return code;
}

u32 basic_read_line(char *buffer, u32 capacity) {
  u32 len = 0;
  if (capacity == 0u) {
    return 0;
  }
  buffer[0] = 0;

  for (;;) {
    u32 code = basic_poll_char();
    if (code == 0u) {
      br_syscall(SYSCALL_PACK(SYSCALL_YIELD, 0));
      continue;
    }

    u8 ch = (u8)code;
    if (ch == '\r' || ch == '\n') {
      tty_put_char('\n');
      buffer[len] = 0;
      return len;
    }

    if (ch == 8u || ch == 127u) {
      if (len != 0u) {
        len--;
        buffer[len] = 0;
        tty_put_char(8u);
      }
      continue;
    }

    if (ch < 0x20u || ch > 0x7eu || len + 1u >= capacity) {
      continue;
    }

    buffer[len] = (char)ch;
    len++;
    buffer[len] = 0;
    tty_put_char(ch);
  }
}
