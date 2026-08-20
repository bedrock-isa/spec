#include "app.h"

u32 app_main(void) {
  app_puts("RUN FAULT\n");
  trigger_privileged_read();
  return 0;
}
