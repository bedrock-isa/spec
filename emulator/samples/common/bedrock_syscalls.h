#ifndef BEDROCK_SAMPLE_SYSCALLS_H
#define BEDROCK_SAMPLE_SYSCALLS_H

#define SYSCALL_PUT 1ULL
#define SYSCALL_YIELD 2ULL
#define SYSCALL_USER_SUM 3ULL
#define SYSCALL_KBD_READ 4ULL
#define SYSCALL_TTY_CLEAR 5ULL
#define SYSCALL_TTY_CLEAR_CELL 6ULL
#define SYSCALL_TTY_DRAW_CHAR 7ULL
#define SYSCALL_USER_RESULT 8ULL
#define SYSCALL_TTY_SCROLL 9ULL
#define SYSCALL_EXEC_BASIC 10ULL
#define SYSCALL_EXIT 11ULL
#define SYSCALL_TTY_PUT_CHAR 12ULL
#define SYSCALL_TTY_BACKSPACE 13ULL
#define SYSCALL_TTY_PUTS 14ULL
#define SYSCALL_EXEC_APP 15ULL
#define SYSCALL_SHELL_MARKER 16ULL

#define SYSCALL_PACK(id, value)                                                 \
  ((((u64)(id)) << 32) | ((u64)(u32)(value)))
#define SYSCALL_PACK_RESULT(slot, value)                                        \
  ((((u32)(slot)&0xffu) << 8) | ((u32)(value)&0xffu))

#endif
