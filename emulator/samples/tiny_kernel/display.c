#include "tiny_kernel.h"
#include "../common/font8x8.h"

volatile u8 g_test_markers[128];
static u32 g_tty_col;
static u32 g_tty_row;

static void put_pixel(u32 x, u32 y, u32 color) {
  if (x < SCREEN_WIDTH && y < SCREEN_HEIGHT) {
    fb_write_u8(y * SCREEN_WIDTH + x, color);
  }
}

u8 hex_digit(u64 value) {
  u32 nibble = (u32)value & 0x0fu;
  return (u8)(nibble < 10u ? ('0' + nibble) : ('A' + nibble - 10u));
}

void display_clear(u32 color) {
  for (u32 y = 0; y < SCREEN_HEIGHT; y++) {
    for (u32 x = 0; x < SCREEN_WIDTH; x++) {
      fb_write_u8(y * SCREEN_WIDTH + x, color);
    }
  }
}

void display_fill_rect(u32 x, u32 y, u32 w, u32 h, u32 color) {
  for (u32 row = 0; row < h; row++) {
    for (u32 col = 0; col < w; col++) {
      put_pixel(x + col, y + row, color);
    }
  }
}

void display_scroll_up(u32 text_rows) {
  u32 pixels = text_rows * TTY_CELL_H;
  if (pixels == 0u) {
    return;
  }
  if (pixels >= SCREEN_HEIGHT) {
    display_clear(COLOR_BLACK);
    return;
  }

  volatile u64 *fb_words = (volatile u64 *)FB_BASE;
  u32 words_per_row = SCREEN_WIDTH / sizeof(u64);
  u32 copy_height = SCREEN_HEIGHT - pixels;
  for (u32 y = 0; y < copy_height; y++) {
    for (u32 word = 0; word < words_per_row; word++) {
      u32 dst = y * words_per_row + word;
      u32 src = (y + pixels) * words_per_row + word;
      fb_words[dst] = fb_words[src];
    }
  }

  for (u32 y = copy_height; y < SCREEN_HEIGHT; y++) {
    for (u32 word = 0; word < words_per_row; word++) {
      fb_words[y * words_per_row + word] = 0;
    }
  }
}

static void tty_clear_cell(u32 col, u32 row) {
  display_fill_rect(col * TTY_CELL_W, row * TTY_CELL_H, TTY_CELL_W, TTY_CELL_H,
                    COLOR_BLACK);
}

static void draw_char(u32 x, u32 y, u32 ch, u32 color) {
  if (ch < 0x20u || ch > 0x7eu) {
    ch = '?';
  }

  const u8 *glyph = BEDROCK_FONT8X8[ch - 0x20u];
  for (u32 row = 0; row < 8; row++) {
    u8 bits = glyph[row];
    for (u32 col = 0; col < 8; col++) {
      u8 pixel = (bits & (0x80u >> col)) != 0 ? (u8)color : (u8)COLOR_BLACK;
      fb_write_u8((y + row) * SCREEN_WIDTH + x + col, pixel);
    }
  }
}

void display_draw_char(u32 x, u32 y, u32 ch, u32 color) {
  draw_char(x, y, ch, color);
}

static void tty_newline(void) {
  g_tty_col = 0;
  g_tty_row++;
  if (g_tty_row >= TTY_ROWS) {
    display_scroll_up(1u);
    g_test_markers[0x6b] = 1u;
    g_test_markers[0x6c] = 0x5cu;
    g_tty_row = TTY_ROWS - 1u;
  }
}

void display_tty_clear(void) {
  display_clear(COLOR_BLACK);
  g_tty_col = 0;
  g_tty_row = 0;
}

void display_tty_put_char(u32 ch) {
  if (ch == '\r') {
    g_tty_col = 0;
    return;
  }
  if (ch == '\n') {
    tty_newline();
    return;
  }
  if (ch == 8u || ch == 127u) {
    display_tty_backspace();
    return;
  }

  tty_clear_cell(g_tty_col, g_tty_row);
  draw_char(g_tty_col * TTY_CELL_W, g_tty_row * TTY_CELL_H, ch, COLOR_WHITE);

  g_tty_col++;
  if (g_tty_col >= TTY_COLS) {
    tty_newline();
  }
}

void display_tty_backspace(void) {
  if (g_tty_col == 0) {
    return;
  }

  g_tty_col--;
  tty_clear_cell(g_tty_col, g_tty_row);
}

void display_draw_text(u32 x, u32 y, const char *text, u32 color) {
  u32 cursor = x;
  for (u32 i = 0; text[i] != 0; i++) {
    draw_char(cursor, y, (u32)(u8)text[i], color);
    cursor += 8;
  }
}

void display_draw_hex8(u32 x, u32 y, u32 value, u32 color) {
  u32 hi = (value >> 4) & 0x0f;
  u32 lo = value & 0x0f;
  draw_char(x, y, hex_digit(hi), color);
  draw_char(x + 8, y, hex_digit(lo), color);
}

void display_write_marker(u32 offset, u32 value) {
  if (offset < sizeof(g_test_markers)) {
    g_test_markers[offset] = (u8)value;
  }
}

void display_render_boot(void) {
  display_tty_clear();
}

void display_render_syscall(u32 index, u32 value, u64 checksum) {
  display_write_marker(index, value);
  display_write_marker(0x31, (u8)(index + 1u));
  display_write_marker(0x54, (u8)checksum);
  display_write_marker(0x55, (u8)(checksum >> 8));
}

void display_render_process(const struct Process *process) {
  (void)process;
}

void display_render_yield(u64 yield_count, u32 ticket) {
  (void)yield_count;
  (void)ticket;
}

void display_render_fault(u64 error_code, u64 count) {
  display_write_marker(0x40, 0x1c);
  display_write_marker(0x41, (u8)count);
  display_write_marker(0x42, (u8)error_code);
}

void display_render_event_return(u64 syscall_count) {
  display_write_marker(0x43, 0x03);
  display_write_marker(0x44, (u8)syscall_count);
}

void display_render_halt(const struct KernelStats *stats) {
  display_write_marker(0x50, 0xff);
  display_write_marker(0x51, (u8)stats->syscall_count);
  display_write_marker(0x52, (u8)stats->privilege_fault_count);
  display_write_marker(0x53, (u8)stats->breakpoint_count);
  display_write_marker(0x54, (u8)stats->checksum);
  display_write_marker(0x55, (u8)(stats->checksum >> 8));
  display_write_marker(0x56, (u8)stats->payload_count);
  display_write_marker(0x57, (u8)stats->yield_count);
  display_write_marker(0x58, (u8)stats->page_count);
  display_write_marker(0x59, 4);
  display_write_marker(0x5a, (u8)stats->user_mirror);
  display_write_marker(0x5d, (u8)stats->last_yield);
  display_write_marker(0x5e, (u8)stats->bad_syscall_count);
}
