#include "app.h"

#include <bedrocksysregintrin.h>

static volatile u8 fault_anchor;

u32 app_main(void) {
  fault_anchor++;
  return app_segment_read_u8(__BEDROCK_SEGMENT_DISABLED, 0x1000u);
}
