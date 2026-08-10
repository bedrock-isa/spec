#include "tiny_kernel.h"

#define EI_CLASS 4u
#define EI_DATA 5u
#define EI_VERSION 6u
#define ELFCLASS64 2u
#define ELFDATA2LSB 1u
#define EV_CURRENT 1u
#define ET_EXEC 2u
#define EM_BEDROCK 0xffb0u
#define PT_LOAD 1u
#define PF_X 1u
#define PF_W 2u
#define PF_R 4u
#define USER_APP_STACK_SIZE 8192u

static u16 read16(const u8 *p) { return (u16)p[0] | ((u16)p[1] << 8); }

static u32 read32(const u8 *p) {
  return (u32)p[0] | ((u32)p[1] << 8) | ((u32)p[2] << 16) | ((u32)p[3] << 24);
}

static u64 read64(const u8 *p) {
  u64 lo = read32(p);
  u64 hi = read32(p + 4);
  return lo | (hi << 32);
}

static u64 align_down(u64 value) { return value & ~(PAGE_SIZE - 1u); }

static u64 align_up(u64 value) {
  return (value + PAGE_SIZE - 1u) & ~(PAGE_SIZE - 1u);
}

static u64 min_nonzero(u64 current, u64 candidate) {
  if (candidate == 0)
    return current;
  if (current == 0 || candidate < current)
    return candidate;
  return current;
}

static u64 max_u64(u64 current, u64 candidate) {
  return candidate > current ? candidate : current;
}

static u32 copy_to_user_frames(u64 destination, const u8 *source, u64 len) {
  for (u64 index = 0; index < len; index++) {
    u64 physical = memory_user_physical(destination + index);
    if (physical == 0)
      return 0;
    *(volatile u8 *)physical = source[index];
  }
  return 1;
}

static u32 map_user_range(u64 ptcr, u64 start, u64 end, u64 flags) {
  for (u64 page = align_down(start); page < align_up(end); page += PAGE_SIZE) {
    if (!memory_map_user_page(ptcr, page, flags))
      return 0;
  }
  return 1;
}

u32 app_load(struct Process *process, const u8 *image, u64 len, u32 pid) {
  if (len < 64u)
    return 1u;
  if (image[0] != 0x7fu || image[1] != 'E' || image[2] != 'L' ||
      image[3] != 'F')
    return 2u;
  if (image[EI_CLASS] != ELFCLASS64 || image[EI_DATA] != ELFDATA2LSB ||
      image[EI_VERSION] != EV_CURRENT)
    return 3u;
  if (read16(image + 16) != ET_EXEC || read16(image + 18) != EM_BEDROCK)
    return 4u;

  u64 entry = read64(image + 24);
  u64 phoff = read64(image + 32);
  u16 phentsize = read16(image + 54);
  u16 phnum = read16(image + 56);
  if (phentsize != 56u)
    return 5u;
  u64 table_size = (u64)phentsize * phnum;
  if (phoff > len || table_size > len - phoff)
    return 6u;

  u64 code_start = 0;
  u64 code_end = 0;
  u64 data_start = 0;
  u64 data_end = 0;
  const u8 *ph = image + phoff;

  for (u32 index = 0; index < phnum; index++, ph += phentsize) {
    u32 type = read32(ph);
    u32 flags = read32(ph + 4);
    if (type != PT_LOAD)
      continue;
    if (flags != (PF_R | PF_X) && flags != (PF_R | PF_W))
      return 7u;

    u64 offset = read64(ph + 8);
    u64 vaddr = read64(ph + 16);
    u64 filesz = read64(ph + 32);
    u64 memsz = read64(ph + 40);
    if (filesz > memsz || offset > len || filesz > len - offset)
      return 8u;
    u64 segment_end = vaddr + memsz;
    if (memsz == 0 || vaddr < USER_APP_BASE || segment_end < vaddr ||
        segment_end > USER_APP_LIMIT)
      return 10u;
    if (flags == (PF_R | PF_X)) {
      code_start = min_nonzero(code_start, vaddr);
      code_end = max_u64(code_end, vaddr + memsz);
    } else {
      data_start = min_nonzero(data_start, vaddr);
      data_end = max_u64(data_end, vaddr + memsz);
    }
  }

  if (code_start == 0 || code_end <= code_start || data_start == 0 ||
      data_end <= data_start || entry < code_start || entry >= code_end)
    return 9u;

  u64 stack_start = align_up(data_end);
  u64 stack_end = stack_start + USER_APP_STACK_SIZE;
  if (stack_end < stack_start || stack_end > USER_APP_LIMIT)
    return 12u;

  if (process->ptcr == 0) {
    process->ptcr = memory_create_address_space(pid, 0);
    if (process->ptcr == 0)
      return 13u;
  }
  memory_clear_user_arena();

  ph = image + phoff;
  for (u32 index = 0; index < phnum; index++, ph += phentsize) {
    u32 type = read32(ph);
    u32 flags = read32(ph + 4);
    if (type != PT_LOAD)
      continue;
    u64 offset = read64(ph + 8);
    u64 vaddr = read64(ph + 16);
    u64 filesz = read64(ph + 32);
    u64 memsz = read64(ph + 40);
    u64 page_flags =
        PAGE_USER | (flags == (PF_R | PF_X) ? PAGE_EXEC : PAGE_WRITE);
    if (!map_user_range(process->ptcr, vaddr, vaddr + memsz, page_flags) ||
        !copy_to_user_frames(vaddr, image + offset, filesz))
      return 14u;
  }
  if (!map_user_range(process->ptcr, stack_start, stack_end,
                      PAGE_USER | PAGE_WRITE))
    return 14u;

  process->pid = pid;
  process->asid = pid;
  process->state = 1u;
  process->syscall_count = 0;
  process->payload_count = 0;
  process->yield_count = 0;
  process->fault_count = 0;
  process->kernel_page = 0;
  process->page_checksum = 0;
  process->last_yield = 0;
  process->code_start = code_start;
  process->code_end = code_end;
  process->data_start = data_start;
  process->data_end = data_end;
  process->stack_start = stack_start;
  process->stack_end = stack_end;
  process->cs = segment_window_for_range(code_start, code_end, 1u);
  process->ds = segment_window_for_range(data_start, stack_end, 1u);
  process->ss = segment_window_for_range(stack_start, stack_end, 1u);
  process->gs0 = 0;
  process->entry = entry;

  display_write_marker(0x70, (u8)entry);
  display_write_marker(0x71, (u8)(entry >> 8));
  return 0u;
}
