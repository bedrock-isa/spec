#include "tiny_kernel.h"

#include <bedrockmmuintrin.h>

#define PAGE_POOL_COUNT 72u
#define USER_FRAME_COUNT 16u

static u8 page_pool[PAGE_POOL_COUNT][PAGE_SIZE]
    __attribute__((aligned(PAGE_SIZE), section(".page_pool")));
static u64 user_frames[USER_FRAME_COUNT];
static u32 next_page;

static void zero_page(u64 address) {
  volatile u64 *words = (volatile u64 *)address;
  for (u32 i = 0; i < PAGE_SIZE / sizeof(u64); i++) {
    words[i] = 0;
  }
}

static u64 align_down(u64 value) { return value & ~(PAGE_SIZE - 1u); }

static u64 align_up(u64 value) {
  return (value + PAGE_SIZE - 1u) & ~(PAGE_SIZE - 1u);
}

void memory_init(void) {
  next_page = 0;
  for (u32 i = 0; i < USER_FRAME_COUNT; i++) {
    user_frames[i] = memory_alloc_page();
  }
}

u64 memory_alloc_page(void) {
  if (next_page >= PAGE_POOL_COUNT) {
    return 0;
  }

  u64 page = (u64)&page_pool[next_page][0];
  next_page++;
  zero_page(page);
  g_kernel_stats.page_count = next_page;
  return page;
}

void memory_fill_page(u64 addr, u32 seed) {
  volatile u8 *page = (volatile u8 *)addr;
  for (u32 i = 0; i < KERNEL_PAGE_SIZE; i++) {
    page[i] = (u8)((seed + i * 17u + (i >> 1)) & 0xffu);
  }
}

u64 memory_page_checksum(u64 addr, u32 len) {
  volatile u8 *page = (volatile u8 *)addr;
  u64 checksum = 0x1234u;
  for (u32 i = 0; i < len; i++) {
    checksum = (checksum * 33u) ^ (u64)page[i] ^ (u64)i;
  }
  return checksum;
}

u64 segment_window_for_range(u64 start, u64 end, u32 bounds_only) {
  if (end <= start) {
    return 0;
  }

  u64 base = align_down(start);
  u64 rounded_end = align_up(end);
  if (rounded_end < end || rounded_end <= base) {
    return 0;
  }

  u64 pages = (rounded_end - base) / PAGE_SIZE;
  u64 exponent = 0;
  u64 mantissa = pages;
  while (mantissa > 63u && exponent < 31u) {
    exponent++;
    mantissa = (pages + ((1ULL << exponent) - 1u)) >> exponent;
  }
  if (mantissa == 0 || mantissa > 63u) {
    return 0;
  }

  return SEGMENT_WINDOW_FOR_BASE(base, exponent, mantissa, bounds_only);
}

u32 memory_map_page(u64 ptcr, u64 virtual_address, u64 physical_address,
                    u64 flags) {
  static const u32 shifts[3] = {39u, 30u, 21u};
  u64 *table = (u64 *)(ptcr & ~(PAGE_SIZE - 1u));
  const u64 table_flags =
      PAGE_PRESENT | PAGE_WRITE | PAGE_EXEC | PAGE_USER | PAGE_TABLE;

  if ((virtual_address & (PAGE_SIZE - 1u)) != 0u ||
      (physical_address & (PAGE_SIZE - 1u)) != 0u) {
    return 0;
  }

  for (u32 level = 0; level < 3u; level++) {
    u32 index = (u32)((virtual_address >> shifts[level]) & 0x1ffu);
    volatile u64 *slot = (volatile u64 *)((u64)table + ((u64)index << 3));
    u64 entry = *slot;
    if ((entry & PAGE_PRESENT) == 0u) {
      u64 child = memory_alloc_page();
      if (child == 0) {
        return 0;
      }
      entry = child | table_flags;
      *slot = entry;
    } else if ((entry & PAGE_TABLE) == 0u) {
      return 0;
    }
    table = (u64 *)(entry & ~(PAGE_SIZE - 1u));
  }

  u64 leaf_index = (virtual_address >> 12) & 0x1ffu;
  *(volatile u64 *)((u64)table + (leaf_index << 3)) =
      physical_address | PAGE_PRESENT | flags;
  return 1;
}

static u32 map_identity_range(u64 ptcr, u64 start, u64 end, u64 flags) {
  if (end <= start) {
    return 1;
  }
  start = align_down(start);
  end = align_up(end);
  for (u64 address = start; address < end; address += PAGE_SIZE) {
    if (!memory_map_page(ptcr, address, address, flags)) {
      return 0;
    }
  }
  return 1;
}

u64 memory_create_address_space(u32 asid, u32 include_shell) {
  (void)asid;
  u64 root = memory_alloc_page();
  if (root == 0) {
    return 0;
  }
  u64 ptcr = root | 1u;

  if (!map_identity_range(ptcr, (u64)__kernel_text_start,
                          (u64)__kernel_text_end, PAGE_EXEC)) {
    g_kernel_stats.last_error = 1;
    return 0;
  }
  if (!map_identity_range(ptcr, (u64)__kernel_rodata_start,
                          (u64)__kernel_rodata_end, 0)) {
    g_kernel_stats.last_error = 2;
    return 0;
  }
  if (!map_identity_range(ptcr, (u64)__kernel_data_start,
                          (u64)__kernel_data_end, PAGE_WRITE)) {
    g_kernel_stats.last_error = 3;
    return 0;
  }
  if (!map_identity_range(ptcr, (u64)__kernel_stack_start,
                          (u64)__kernel_stack_end, PAGE_WRITE)) {
    g_kernel_stats.last_error = 4;
    return 0;
  }
  if (!map_identity_range(ptcr, 0x000ff000ULL, 0x00100000ULL, PAGE_WRITE)) {
    g_kernel_stats.last_error = 5;
    return 0;
  }
  if (!map_identity_range(ptcr, (u64)__page_pool_start, (u64)__page_pool_end,
                          PAGE_WRITE)) {
    g_kernel_stats.last_error = 6;
    return 0;
  }
  if (!map_identity_range(ptcr, FB_BASE, FB_BASE + FB_SIZE, PAGE_WRITE)) {
    g_kernel_stats.last_error = 7;
    return 0;
  }
  if (!map_identity_range(ptcr, KBD_BASE, KBD_BASE + KBD_REG_SIZE,
                          PAGE_WRITE)) {
    g_kernel_stats.last_error = 8;
    return 0;
  }

  if (include_shell != 0u &&
      (!map_identity_range(ptcr, (u64)__user_text_start, (u64)__user_text_end,
                           PAGE_EXEC | PAGE_USER) ||
       !map_identity_range(ptcr, (u64)__user_rodata_start,
                           (u64)__user_rodata_end, PAGE_USER) ||
       !map_identity_range(ptcr, (u64)__tls_start, (u64)__tls_end,
                           PAGE_WRITE | PAGE_USER) ||
       !map_identity_range(ptcr, (u64)__user_stack_start, (u64)__user_stack_end,
                           PAGE_WRITE | PAGE_USER))) {
    g_kernel_stats.last_error = 9;
    return 0;
  }

  return ptcr;
}

void memory_switch_address_space(u64 ptcr, u32 asid) {
  __bedrock_switch_page_table_asid(ptcr, (u16)asid);
}

void memory_clear_user_arena(void) {
  for (u32 i = 0; i < USER_FRAME_COUNT; i++) {
    zero_page(user_frames[i]);
  }
}

u64 memory_user_physical(u64 virtual_address) {
  if (virtual_address < USER_APP_BASE ||
      virtual_address >= USER_APP_BASE + USER_FRAME_COUNT * PAGE_SIZE) {
    return 0;
  }
  u32 index = (u32)((virtual_address - USER_APP_BASE) / PAGE_SIZE);
  return user_frames[index] + (virtual_address & (PAGE_SIZE - 1u));
}

u32 memory_map_user_page(u64 ptcr, u64 virtual_address, u64 flags) {
  u64 physical = memory_user_physical(align_down(virtual_address));
  if (physical == 0) {
    return 0;
  }
  return memory_map_page(ptcr, align_down(virtual_address), physical, flags);
}
