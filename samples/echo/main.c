// Keyboard-to-framebuffer echo sample for the Bedrock emulator.
typedef unsigned long long u64;
typedef unsigned int u32;
typedef unsigned char u8;

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

#define L4 ((volatile u64 *)0x0000000000008000ULL)
#define L3 ((volatile u64 *)0x0000000000009000ULL)
#define L2 ((volatile u64 *)0x000000000000a000ULL)
#define L1 ((volatile u64 *)0x000000000000b000ULL)

#define HI_BASE 0x00007fff00000000ULL
#define FB ((volatile u8 *)(HI_BASE + 0x0000000000f00000ULL))
#define KBD_STATUS (*(volatile u32 *)(HI_BASE + 0x0000000000f20000ULL))
#define KBD_DATA (*(volatile u32 *)(HI_BASE + 0x0000000000f20004ULL))

static void map4k(u64 va, u64 pa, u64 flags) {
  u64 l4i = (va >> 39) & 511ULL;
  u64 l3i = (va >> 30) & 511ULL;
  u64 l2i = (va >> 21) & 511ULL;
  u64 l1i = (va >> 12) & 511ULL;

  u64 table = PAGE_PRESENT | PAGE_TABLE | PAGE_TABLE_R | PAGE_TABLE_W |
              PAGE_TABLE_X | PAGE_USER;
  L4[l4i] = 0x9000ULL | table;
  L3[l3i] = 0xa000ULL | table;
  L2[l2i] = 0xb000ULL | table;
  L1[l1i] = (pa & ~0xfffULL) | flags;
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
  map4k(0x0000000000001000ULL, 0x0000000000001000ULL,
        PAGE_PRESENT | PAGE_AM_RX);
  map4k(0x0000000000002000ULL, 0x0000000000002000ULL,
        PAGE_PRESENT | PAGE_AM_RX);
  map4k(0x0000000000003000ULL, 0x0000000000003000ULL,
        PAGE_PRESENT | PAGE_AM_RX);
  map4k(0x0000000000008000ULL, 0x0000000000008000ULL,
        PAGE_PRESENT | PAGE_AM_RW);
  map4k(0x0000000000009000ULL, 0x0000000000009000ULL,
        PAGE_PRESENT | PAGE_AM_RW);
  map4k(0x000000000000a000ULL, 0x000000000000a000ULL,
        PAGE_PRESENT | PAGE_AM_RW);
  map4k(0x000000000000b000ULL, 0x000000000000b000ULL,
        PAGE_PRESENT | PAGE_AM_RW);

  for (u32 page = 0; page < 16; page++) {
    map4k(HI_BASE + 0x00f00000ULL + page * 4096ULL,
          0x00f00000ULL + page * 4096ULL,
          PAGE_PRESENT | PAGE_AM_MMIO_RW);
  }

  map4k(HI_BASE + 0x00f20000ULL, 0x00f20000ULL,
        PAGE_PRESENT | PAGE_AM_MMIO_RW);

  __asm__ volatile(
      "MOV.Q 32769, R0\n"
      "SWPT R0"
      :
      :
      : "r0", "memory");

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
