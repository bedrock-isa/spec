#include "basic.h"

void _start(void) {
  u32 code = basic_main();
  br_exit(code);
  for (;;) {
  }
}

u32 basic_main(void) {
  tty_reset();
  basic_program_reset();
  tty_puts("BEDROCK BASIC\n");
  tty_puts("READY\n");
  return basic_run_demo();
}
