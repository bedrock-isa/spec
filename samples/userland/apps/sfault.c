#include "app.h"

static volatile u8 fault_anchor;

u32 app_main(void) {
  fault_anchor++;
  volatile u8 *outside_ds = (volatile u8 *)0x1000u;
  return *outside_ds;
}
