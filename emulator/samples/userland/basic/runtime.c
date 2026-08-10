#include "basic.h"

static void list_program(void) __attribute__((noinline));
static u32 run_program(void) __attribute__((noinline));

static u32 g_demo_result;
static char g_command_line[BASIC_INPUT_CAP];

static u8 ascii_upper(u8 ch) {
  if (ch >= 'a' && ch <= 'z') {
    return (u8)(ch - 32u);
  }
  return ch;
}

static u32 is_space(u8 ch) { return ch == ' ' || ch == '\t'; }

static u32 command_is(const char *line, const char *name) {
  u32 line_index = 0;
  u32 name_index = 0;

  while (is_space((u8)line[line_index])) {
    line_index++;
  }

  for (;;) {
    u8 want = (u8)name[name_index];
    u8 got = (u8)line[line_index];
    if (want == 0u) {
      while (is_space(got)) {
        line_index++;
        got = (u8)line[line_index];
      }
      return got == 0u;
    }
    if (ascii_upper(got) != want) {
      return 0;
    }
    line_index++;
    name_index++;
  }
}

static u32 command_is_empty(const char *line) {
  u32 index = 0;
  while (is_space((u8)line[index])) {
    index++;
  }
  return line[index] == 0;
}

static void list_program(void) { basic_program_list(); }

static u32 run_program(void) {
  if (!basic_program_compile()) {
    tty_puts("COMPILE ERROR\n");
    return 0;
  }

  tty_puts("RUN USER PROGRAM\n");

  g_demo_result = basic_vm_run();
  br_syscall(SYSCALL_PACK(SYSCALL_YIELD, 0));
  tty_puts("RESULT ");
  tty_put_u32_dec(g_demo_result);
  tty_put_char('\n');
  return g_demo_result;
}

static void print_result(void) {
  tty_puts("RESULT ");
  tty_put_u32_dec(g_demo_result);
  tty_put_char('\n');
}

u32 basic_run_demo(void) {
  for (;;) {
    tty_put_char('>');
    basic_read_line(g_command_line, BASIC_INPUT_CAP);

    if (command_is_empty(g_command_line)) {
      continue;
    }

    u32 edit_result = basic_program_edit_line(g_command_line);
    if (edit_result != BASIC_EDIT_NOT_LINE) {
      if (edit_result == BASIC_EDIT_OK) {
        tty_puts("OK\n");
      } else {
        tty_puts("?\n");
      }
      continue;
    }

    if (command_is(g_command_line, "LIST")) {
      list_program();
      continue;
    }
    if (command_is(g_command_line, "RUN")) {
      run_program();
      continue;
    }
    if (command_is(g_command_line, "PRINT")) {
      print_result();
      continue;
    }
    if (command_is(g_command_line, "HELP")) {
      tty_puts("LIST RUN PRINT EXIT\n");
      continue;
    }
    if (command_is(g_command_line, "EXIT") ||
        command_is(g_command_line, "QUIT")) {
      return g_demo_result;
    }

    tty_puts("?\n");
  }
}
