#include "tiny_kernel.h"

struct SyscallContext {
  u32 id;
  u32 arg;
  u64 raw;
  u64 index;
  struct UserReturnContext *return_context;
};

static u64 update_checksum(u64 checksum, u64 value, u64 index) {
  checksum = (checksum * 131u) ^ ((value & 0xffu) + index * 17u);
  return checksum & 0xffffffffffffffffULL;
}

static u64 handle_put(struct SyscallContext *ctx) {
  u32 value = ctx->arg & 0xffu;
  u64 payload_index = g_kernel_stats.payload_count;

  g_kernel_stats.payload_count = payload_index + 1u;
  g_kernel_stats.checksum =
      update_checksum(g_kernel_stats.checksum, value, payload_index);
  process_record_payload(value);

  if (g_syscall_cursor < REQUEST_COUNT) {
    display_render_syscall(g_syscall_cursor, value, g_kernel_stats.checksum);
  }
  g_syscall_cursor++;
  return 0;
}

static u64 handle_yield(struct SyscallContext *ctx) {
  g_kernel_stats.yield_count++;
  g_kernel_stats.last_yield = ctx->arg;
  process_record_yield(ctx->arg);
  return 0;
}

static u64 handle_user_sum(struct SyscallContext *ctx) {
  process_record_user_sum(ctx->arg);
  return 0;
}

static u64 handle_kbd_read(struct SyscallContext *ctx) {
  (void)ctx;
  return kbd_read_u32(KBD_DATA_OFFSET);
}

static u64 handle_tty_clear(struct SyscallContext *ctx) {
  (void)ctx;
  display_tty_clear();
  return 0;
}

static u64 handle_tty_clear_cell(struct SyscallContext *ctx) {
  u32 col = ctx->arg & 0xffu;
  u32 row = (ctx->arg >> 8) & 0xffu;
  display_fill_rect(col * TTY_CELL_W, row * TTY_CELL_H, TTY_CELL_W, TTY_CELL_H,
                    COLOR_BLACK);
  return 0;
}

static u64 handle_tty_draw_char(struct SyscallContext *ctx) {
  u32 col = ctx->arg & 0xffu;
  u32 row = (ctx->arg >> 8) & 0xffu;
  u32 ch = (ctx->arg >> 16) & 0xffu;
  display_draw_char(col * TTY_CELL_W, row * TTY_CELL_H, ch, COLOR_WHITE);
  return 0;
}

static u64 handle_tty_scroll(struct SyscallContext *ctx) {
  u32 rows = ctx->arg & 0xffu;
  if (rows == 0u) {
    rows = 1u;
  }

  display_scroll_up(rows);
  display_write_marker(0x6b, (u8)rows);
  display_write_marker(0x6c, 0x5c);
  return 0;
}

static u64 handle_tty_put_char(struct SyscallContext *ctx) {
  display_tty_put_char(ctx->arg & 0xffu);
  return 0;
}

static u64 handle_tty_puts(struct SyscallContext *ctx) {
  u64 text = (u64)ctx->arg;
  for (u32 i = 0; i < 1024u; i++) {
    u64 address = text + i;
    if (address < text || !process_user_range_readable(address, 1u)) {
      return 0xfdu;
    }
    u32 ch = read_user_u8(address);
    if (ch == 0)
      return 0;
    display_tty_put_char((u8)ch);
  }
  return 0xfcu;
}

static u64 handle_tty_backspace(struct SyscallContext *ctx) {
  (void)ctx;
  display_tty_backspace();
  return 0;
}

static u64 handle_user_result(struct SyscallContext *ctx) {
  u32 slot = (ctx->arg >> 8) & 0xffu;
  u32 value = ctx->arg & 0xffu;
  process_record_user_result(slot, value);
  return value;
}

static u64 handle_shell_marker(struct SyscallContext *ctx) {
  u32 offset = (ctx->arg >> 8) & 0xffu;
  u32 value = ctx->arg & 0xffu;
  if (offset < 0x60u || offset > 0x62u) {
    return 0xfeu;
  }
  display_write_marker(offset, value);
  return 0;
}

static u64 handle_exec_basic(struct SyscallContext *ctx) {
  return process_exec_basic(ctx->return_context);
}

static u64 handle_exec_app(struct SyscallContext *ctx) {
  return process_exec_app(ctx->return_context, ctx->arg);
}

static u64 handle_exit(struct SyscallContext *ctx) {
  return process_exit_current(ctx->return_context, ctx->arg & 0xffu);
}

static u64 handle_bad_syscall(struct SyscallContext *ctx) {
  g_kernel_stats.bad_syscall_count++;
  g_kernel_stats.last_error = ctx->raw;
  display_write_marker(0x5e, (u8)g_kernel_stats.bad_syscall_count);
  return 0;
}

__attribute__((optnone)) u64
kernel_syscall_dispatch_frame(u64 code, struct UserReturnContext *context) {
  struct SyscallContext ctx;
  ctx.id = (u32)(code >> 32);
  ctx.arg = (u32)code;
  ctx.raw = code;
  ctx.index = g_kernel_stats.syscall_count;
  ctx.return_context = context;
  g_kernel_stats.syscall_count = ctx.index + 1u;

  if (ctx.id == SYSCALL_PUT)
    return handle_put(&ctx);
  if (ctx.id == SYSCALL_YIELD)
    return handle_yield(&ctx);
  if (ctx.id == SYSCALL_USER_SUM)
    return handle_user_sum(&ctx);
  if (ctx.id == SYSCALL_KBD_READ)
    return handle_kbd_read(&ctx);
  if (ctx.id == SYSCALL_TTY_CLEAR)
    return handle_tty_clear(&ctx);
  if (ctx.id == SYSCALL_TTY_CLEAR_CELL)
    return handle_tty_clear_cell(&ctx);
  if (ctx.id == SYSCALL_TTY_DRAW_CHAR)
    return handle_tty_draw_char(&ctx);
  if (ctx.id == SYSCALL_USER_RESULT)
    return handle_user_result(&ctx);
  if (ctx.id == SYSCALL_TTY_SCROLL)
    return handle_tty_scroll(&ctx);
  if (ctx.id == SYSCALL_EXEC_BASIC)
    return handle_exec_basic(&ctx);
  if (ctx.id == SYSCALL_EXIT)
    return handle_exit(&ctx);
  if (ctx.id == SYSCALL_TTY_PUT_CHAR)
    return handle_tty_put_char(&ctx);
  if (ctx.id == SYSCALL_TTY_BACKSPACE)
    return handle_tty_backspace(&ctx);
  if (ctx.id == SYSCALL_TTY_PUTS)
    return handle_tty_puts(&ctx);
  if (ctx.id == SYSCALL_EXEC_APP)
    return handle_exec_app(&ctx);
  if (ctx.id == SYSCALL_SHELL_MARKER)
    return handle_shell_marker(&ctx);

  return handle_bad_syscall(&ctx);
}

u64 kernel_syscall_dispatch(u64 code) {
  return kernel_syscall_dispatch_frame(code, 0);
}
