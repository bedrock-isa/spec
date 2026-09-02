// Keyboard-to-framebuffer echo sample for the Bedrock emulator.
typedef unsigned long long u64;
typedef unsigned int u32;
typedef unsigned char u8;

#include <bedrockmmuintrin.h>

#include "../common/font8x8.h"

#define PAGE_PRESENT (1ULL << 0)
#define PAGE_TABLE (1ULL << 1)
#define PAGE_AM_RW (3ULL << 2)
#define PAGE_AM_RX (4ULL << 2)
#define PAGE_AM_MMIO_RW (7ULL << 2)
#define PAGE_TABLE_R (1ULL << 2)
#define PAGE_TABLE_W (1ULL << 3)
#define PAGE_TABLE_X (1ULL << 4)
#define PAGE_USER (1ULL << 5)

#define HI_BASE 0x00000fff00000000ULL
#define FB ((volatile u8 *)(HI_BASE + 0x0000000000f00000ULL))
#define KBD_STATUS (*(volatile u32 *)(HI_BASE + 0x0000000000f20000ULL))
#define KBD_DATA (*(volatile u32 *)(HI_BASE + 0x0000000000f20004ULL))

static u64 l3_table[2048] __attribute__((aligned(16384)));
static u64 l2_table[2048] __attribute__((aligned(16384)));
static u64 l1_table[512] __attribute__((aligned(4096)));

static void map16k(u64 va, u64 pa, u64 flags) {
  u64 l3i = (va >> 34) & 2047ULL;
  u64 l2i = (va >> 23) & 2047ULL;
  u64 l1i = (va >> 14) & 511ULL;

  u64 table = PAGE_PRESENT | PAGE_TABLE | PAGE_TABLE_R | PAGE_TABLE_W |
              PAGE_TABLE_X | PAGE_USER;
  l3_table[l3i] = (u64)l2_table | table;
  l2_table[l2i] = (u64)l1_table | table;
  l1_table[l1i] = (pa & ~0x3fffULL) | flags;
}

static void draw_char(u32 cx, u32 cy, u8 ch) {
  if (ch < 0x20 || ch > 0x7e) {
    ch = '?';
  }

  u32 index = (u32)(ch - 0x20);
  const u8 *glyph = BEDROCK_FONT8X8[index];
  for (u32 row = 0; row < 8; row++) {
    u8 bits = glyph[row];
    volatile u8 *p = FB + (cy + row) * 320 + cx;
    for (u32 col = 0; col < 8; col++) {
      p[col] = (bits & (0x80u >> col)) ? 0xff : 0x00;
    }
  }
}

void _start(void) {
  map16k(0x0000000000000000ULL, 0x0000000000000000ULL,
        PAGE_PRESENT | PAGE_AM_RX);
  map16k((u64)l3_table, (u64)l3_table, PAGE_PRESENT | PAGE_AM_RW);
  map16k((u64)l2_table, (u64)l2_table, PAGE_PRESENT | PAGE_AM_RW);
  map16k((u64)l1_table, (u64)l1_table, PAGE_PRESENT | PAGE_AM_RW);

  for (u32 page = 0; page < 4; page++) {
    map16k(HI_BASE + 0x00f00000ULL + page * 16384ULL,
          0x00f00000ULL + page * 16384ULL,
          PAGE_PRESENT | PAGE_AM_MMIO_RW);
  }

  map16k(HI_BASE + 0x00f20000ULL, 0x00f20000ULL,
        PAGE_PRESENT | PAGE_AM_MMIO_RW);

  __bedrock_switch_page_table((u64)l3_table | 5u);

  u32 x = 0;
  u32 y = 0;
  for (;;) {
    while ((KBD_STATUS & 1u) == 0u) {
    }

    u32 ev = KBD_DATA;
    if ((ev & 0x00010000u) == 0u) {
      continue;
    }

    u32 code = ev & 0xffffu;
    if (code == '\r' || code == '\n') {
      x = 0;
      y += 10;
    } else if (code < 0x20u || code > 0x7eu) {
      continue;
    } else {
      draw_char(x, y, (u8)code);
      x += 8;
      if (x >= 320) {
        x = 0;
        y += 10;
      }
    }

    if (y >= 200) {
      y = 0;
    }
  }
}
