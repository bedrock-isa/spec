#ifndef BEDROCK_USERLAND_BASIC_H
#define BEDROCK_USERLAND_BASIC_H

typedef unsigned long long u64;
typedef unsigned int u32;
typedef unsigned char u8;

#include "../../common/bedrock_syscalls.h"

#define BASIC_TTY_COLS 40u
#define BASIC_TTY_ROWS 25u
#define BASIC_TTY_CELL_W 8u
#define BASIC_TTY_CELL_H 8u

#define TTY_PACK_CELL(col, row)                                                \
  ((((u32)(row) & 0xffu) << 8) | ((u32)(col) & 0xffu))
#define TTY_PACK_CHAR(col, row, ch)                                            \
  (TTY_PACK_CELL((col), (row)) | (((u32)(ch) & 0xffu) << 16))

u32 br_syscall(u64 code);
void br_exit(u32 code);
void tty_reset(void);
void tty_put_char(u8 ch);
void tty_puts(const char *text);
void tty_put_u32_dec(u32 value);
void tty_put_u64_dec(u64 value);
u32 basic_read_line(char *buffer, u32 capacity);

#define BASIC_INPUT_CAP 64u
#define BASIC_LINE_TEXT_CAP 56u
#define BASIC_MAX_LINES 16u
#define BASIC_COMPILED_CAP 64u

#define BASIC_EDIT_NOT_LINE 0u
#define BASIC_EDIT_OK 1u
#define BASIC_EDIT_ERROR 2u

#define KBD_EVENT_CODE_MASK 0x0000ffffu
#define KBD_EVENT_PRESSED 0x00010000u
#define KBD_EVENT_CTRL 0x00040000u
#define KBD_EVENT_ALT 0x00080000u
#define KBD_EVENT_COMMAND 0x00100000u

enum BasicOpcode {
  BASIC_OP_SET = 1,
  BASIC_OP_ADD = 2,
  BASIC_OP_MUL = 3,
  BASIC_OP_XOR = 4,
  BASIC_OP_FSET = 5,
  BASIC_OP_FADD = 6,
  BASIC_OP_FMUL = 7,
  BASIC_OP_FDIV = 8,
  BASIC_OP_FSERIES = 9,
  BASIC_OP_PRINT = 10,
  BASIC_OP_FPRINT = 11,
  BASIC_OP_END = 255,
};

struct BasicInstruction {
  u8 opcode;
  u8 dst;
  u8 src;
  u8 rounds;
  u32 imm;
  double fimm;
};

extern u32 g_basic_line_numbers[BASIC_MAX_LINES];
extern char g_basic_line_text[BASIC_MAX_LINES][BASIC_LINE_TEXT_CAP];
extern u32 g_basic_line_count;
extern struct BasicInstruction g_basic_program[BASIC_COMPILED_CAP];
extern u32 g_basic_program_len;

u32 basic_main(void) __attribute__((noinline));
u32 basic_run_demo(void) __attribute__((noinline));
u32 basic_vm_run(void) __attribute__((noinline));
void basic_program_reset(void) __attribute__((noinline));
void basic_program_list(void) __attribute__((noinline));
u32 basic_program_edit_line(const char *line) __attribute__((noinline));
u32 basic_program_compile(void) __attribute__((noinline));
double basic_fp_series(double x, double y, u32 rounds)
    __attribute__((noinline));
u32 basic_fp_checksum(double value) __attribute__((noinline));
u64 basic_fp_bits(double value) __attribute__((noinline));

#endif
