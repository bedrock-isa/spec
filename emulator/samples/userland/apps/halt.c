#include "app.h"

u32 app_main(void) {
  app_puts("RUN HALT\n");
  __asm__ volatile("BKPT" ::: "memory");
  for (;;) {
  }
  return 0;
}
