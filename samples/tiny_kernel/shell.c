#include "tiny_kernel.h"

_Thread_local struct UserTls g_user_tls;

static u8 ascii_upper(u8 ch) {
  if (ch >= 'a' && ch <= 'z') {
    return (u8)(ch - 32u);
  }
  return ch;
}

static u8 to_input_char(u32 code) {
  if (code >= 'a' && code <= 'z') {
    return (u8)code;
  }
  if (code >= 0x20u && code <= 0x7eu) {
    return (u8)code;
  }
  return 0;
}

static int command_is(const char *name) {
  u32 i = 0;
  for (;;) {
    u8 ch = g_user_tls.input[i];
    if (ch == 0 || name[i] == 0) {
      return ch == 0 && name[i] == 0;
    }
    if (ascii_upper(ch) != (u8)name[i]) {
      return 0;
    }
    i++;
  }
}

static void shell_clear_input(void) {
  for (u32 i = 0; i < SHELL_INPUT_CAP; i++) {
    g_user_tls.input[i] = 0;
  }
  g_user_tls.input_len = 0;
}

static void tty_put_char(u8 ch) {
  syscall_call(SYSCALL_PACK(SYSCALL_TTY_PUT_CHAR, ch));
}

static void tty_put_dec_place(u32 *value, u32 place, u32 *started) {
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

static void tty_put_u32_dec(u32 value) {
  u32 started = 0;
  tty_put_dec_place(&value, 1000000000u, &started);
  tty_put_dec_place(&value, 100000000u, &started);
  tty_put_dec_place(&value, 10000000u, &started);
  tty_put_dec_place(&value, 1000000u, &started);
  tty_put_dec_place(&value, 100000u, &started);
  tty_put_dec_place(&value, 10000u, &started);
  tty_put_dec_place(&value, 1000u, &started);
  tty_put_dec_place(&value, 100u, &started);
  tty_put_dec_place(&value, 10u, &started);
  tty_put_dec_place(&value, 1u, &started);
}

static void tty_puts(const char *text) {
  syscall_call(SYSCALL_PACK(SYSCALL_TTY_PUTS, (u32)(u64)text));
}

static void tty_put_ok(void) {
  tty_put_char('\n');
  tty_puts("OK\n");
}

static void tty_put_app_ok(void) { tty_puts("OK\n"); }

static void tty_prompt(void) { tty_put_char('>'); }

static void tty_backspace(void) {
  syscall_call(SYSCALL_PACK(SYSCALL_TTY_BACKSPACE, 0));
}

static u32 shell_exec_app(u32 app_id) {
  return syscall_call(SYSCALL_PACK(SYSCALL_EXEC_APP, app_id));
}

static void shell_marker(u32 offset, u32 value) {
  syscall_call(SYSCALL_PACK(SYSCALL_SHELL_MARKER,
                            ((offset & 0xffu) << 8) | (value & 0xffu)));
}

static u32 shell_poll_char(void) {
  u32 event = syscall_call(SYSCALL_PACK(SYSCALL_KBD_READ, 0));
  if (event == 0u) {
    return 0;
  }
  g_user_tls.last_key_event = event;

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

static void shell_reset_screen(void) {
  syscall_call(SYSCALL_PACK(SYSCALL_TTY_CLEAR, 0));
  tty_prompt();
}

static void shell_run_command(void) {
  u32 command_count = g_user_tls.command_count + 1u;
  g_user_tls.command_count = command_count;
  shell_marker(0x60, 0x51);
  shell_marker(0x61, command_count);
  tty_put_char('\n');

  if (command_is("DEMO")) {
    shell_marker(0x62, 0x01);
    shell_exec_app(APP_ID_DEMO);
    tty_put_app_ok();
  } else if (command_is("MATH")) {
    shell_marker(0x62, 0x07);
    shell_exec_app(APP_ID_MATH);
    tty_put_app_ok();
  } else if (command_is("SORT")) {
    shell_marker(0x62, 0x08);
    shell_exec_app(APP_ID_SORT);
    tty_put_app_ok();
  } else if (command_is("MEM")) {
    shell_marker(0x62, 0x09);
    shell_exec_app(APP_ID_MEM);
    tty_put_app_ok();
  } else if (command_is("FAR")) {
    shell_marker(0x62, 0x0b);
    shell_exec_app(APP_ID_FAR);
    tty_put_app_ok();
  } else if (command_is("BASIC")) {
    u32 code;
    shell_marker(0x62, 0x0a);
    code = shell_exec_app(APP_ID_BASIC);
    tty_puts("BASIC EXIT ");
    tty_put_u32_dec(code);
    tty_put_ok();
  } else if (command_is("FAULT")) {
    shell_marker(0x62, 0x02);
    shell_exec_app(APP_ID_FAULT);
    tty_put_app_ok();
  } else if (command_is("PFAULT")) {
    shell_marker(0x62, 0x0c);
    shell_exec_app(APP_ID_PFAULT);
    tty_put_app_ok();
  } else if (command_is("SFAULT")) {
    shell_marker(0x62, 0x0d);
    shell_exec_app(APP_ID_SFAULT);
    tty_put_app_ok();
  } else if (command_is("HALT")) {
    shell_marker(0x62, 0x03);
    shell_exec_app(APP_ID_HALT);
  } else if (command_is("HELP")) {
    shell_marker(0x62, 0x04);
    tty_puts("MATH SORT MEM FAR DEMO\n");
    tty_puts("BASIC FAULT PFAULT SFAULT\n");
    tty_puts("HALT CLEAR STATS\n");
  } else if (command_is("CLEAR")) {
    shell_marker(0x62, 0x05);
    shell_reset_screen();
    return;
  } else if (command_is("STATS")) {
    shell_marker(0x62, 0x06);
    tty_puts("STATS MARKERS\n");
  } else if (g_user_tls.input_len != 0u) {
    shell_marker(0x62, 0xee);
    tty_puts("BAD CMD\n");
  }

  shell_clear_input();
  tty_prompt();
}

void user_main(void) {
  shell_clear_input();
  g_user_tls.command_count = 0;
  shell_reset_screen();

  for (;;) {
    u32 event_char = shell_poll_char();
    if (event_char == 0u) {
      continue;
    }

    u8 ch = (u8)event_char;
    if (ch == '\r' || ch == '\n') {
      shell_run_command();
      continue;
    }

    if (ch == 8u || ch == 127u) {
      u32 len = g_user_tls.input_len;
      if (len != 0u) {
        len--;
        g_user_tls.input_len = len;
        g_user_tls.input[len] = 0;
        tty_backspace();
      }
      continue;
    }

    u8 printable = to_input_char(ch);
    u32 len = g_user_tls.input_len;
    if (printable == 0u || len + 1u >= SHELL_INPUT_CAP) {
      continue;
    }

    g_user_tls.input[len] = printable;
    len++;
    g_user_tls.input_len = len;
    g_user_tls.input[len] = 0;
    tty_put_char(printable);
  }
}
