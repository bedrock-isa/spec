#ifndef BEDROCK_TINY_KERNEL_H
#define BEDROCK_TINY_KERNEL_H

typedef unsigned long long u64;
typedef unsigned int u32;
typedef unsigned short u16;
typedef unsigned char u8;

#include "../common/bedrock_syscalls.h"

#define SCREEN_WIDTH 320u
#define SCREEN_HEIGHT 200u
#define FB_BASE 0x00f00000ULL
#define FB_SIZE (SCREEN_WIDTH * SCREEN_HEIGHT)
#define KBD_BASE 0x00f20000ULL
#define KBD_STATUS_OFFSET 0x00u
#define KBD_DATA_OFFSET 0x04u
#define KBD_REG_SIZE 0x100u

#define EVENT_BREAKPOINT 0x00000002u
#define EVENT_PRIVILEGE_FAULT 0x00000008u
#define EVENT_PAGE_FAULT 0x00000009u
#define REQUEST_COUNT 16u
#define PAGE_SIZE 4096u
#define KERNEL_PAGE_SIZE 256u
#define USER_APP_BASE 0x00080000ULL
#define USER_APP_LIMIT 0x00090000ULL
#define SHELL_INPUT_CAP 39u
#define TTY_COLS 40u
#define TTY_ROWS 25u
#define TTY_CELL_W 8u
#define TTY_CELL_H 8u

#define KBD_EVENT_CODE_MASK 0x0000ffffu
#define KBD_EVENT_PRESSED 0x00010000u
#define KBD_EVENT_SHIFT 0x00020000u
#define KBD_EVENT_CTRL 0x00040000u
#define KBD_EVENT_ALT 0x00080000u
#define KBD_EVENT_COMMAND 0x00100000u

#define APP_ID_BASIC 1u
#define APP_ID_DEMO 2u
#define APP_ID_MATH 3u
#define APP_ID_SORT 4u
#define APP_ID_MEM 5u
#define APP_ID_FAULT 6u
#define APP_ID_HALT 7u
#define APP_ID_FAR 8u
#define APP_ID_PFAULT 9u
#define APP_ID_SFAULT 10u

#define PAGE_PRESENT (1ULL << 0)
#define PAGE_WRITE (1ULL << 1)
#define PAGE_EXEC (1ULL << 2)
#define PAGE_USER (1ULL << 3)
#define PAGE_ACCESSED (1ULL << 5)
#define PAGE_DIRTY (1ULL << 6)
#define PAGE_TABLE (1ULL << 11)

#define SEGMENT_WINDOW(base_page, exponent, mantissa, bounds_only)             \
  ((((u64)(base_page)) << 12) | (((u64)(exponent) & 0x1fULL) << 7) |           \
   (((u64)(mantissa) & 0x3fULL) << 1) | ((bounds_only) ? 1ULL : 0ULL))
#define SEGMENT_WINDOW_FOR_BASE(base, exponent, mantissa, bounds_only)         \
  SEGMENT_WINDOW(((u64)(base)) >> 12, exponent, mantissa, bounds_only)
#define KERNEL_SEGMENT_WINDOW SEGMENT_WINDOW(0, 6, 61, 1)

#define TTY_PACK_CELL(col, row)                                                \
  ((((u32)(row) & 0xffu) << 8) | ((u32)(col) & 0xffu))
#define TTY_PACK_CHAR(col, row, ch)                                            \
  (TTY_PACK_CELL((col), (row)) | (((u32)(ch) & 0xffu) << 16))

#define COLOR_BLACK 0x00u
#define COLOR_WHITE 0xffu
#define COLOR_CYAN 0x1fu
#define COLOR_GREEN 0x1cu
#define COLOR_YELLOW 0xfcu
#define COLOR_RED 0xe0u
#define COLOR_BLUE 0x03u
#define COLOR_MAGENTA 0xe3u
#define COLOR_PANEL 0x49u
#define COLOR_PANEL_DARK 0x24u

struct ExceptionFrame {
  u64 frame_control;
  u64 event_info;
  u64 frame_ext1;
  u64 saved_pc;
  u64 saved_sp;
  u64 saved_cs;
  u64 saved_ds;
  u64 saved_ss;
  u64 error_code;
  u64 fault_ea;
  u64 fault_linear;
  u64 fault_aux;
};

struct UserReturnContext {
  u64 urctl;
  u64 pc;
  u64 sp;
  u64 cs;
  u64 ds;
  u64 ss;
};

struct KernelStats {
  u64 boot_magic;
  u64 syscall_count;
  u64 privilege_fault_count;
  u64 breakpoint_count;
  u64 checksum;
  u64 last_error;
  u64 payload_count;
  u64 yield_count;
  u64 page_count;
  u64 bad_syscall_count;
  u64 user_mirror;
  u64 last_yield;
  u64 page_fault_count;
  u64 last_fault_address;
  u64 last_fault_reason;
};

struct Process {
  u64 pid;
  u64 state;
  u64 syscall_count;
  u64 payload_count;
  u64 yield_count;
  u64 fault_count;
  u64 kernel_page;
  u64 page_checksum;
  u64 last_yield;
  u64 code_start;
  u64 code_end;
  u64 data_start;
  u64 data_end;
  u64 stack_start;
  u64 stack_end;
  u64 cs;
  u64 ds;
  u64 ss;
  u64 gs0;
  u64 entry;
  u64 ptcr;
  u64 asid;
};

struct UserContext {
  u64 urctl;
  u64 pc;
  u64 sp;
  u64 cs;
  u64 ds;
  u64 ss;
  u64 gs0;
  u64 r[16];
};

struct UserTls {
  u8 input[SHELL_INPUT_CAP];
  u32 input_len;
  u32 command_count;
  u32 last_key_event;
};

extern struct KernelStats g_kernel_stats;
extern struct Process g_user_process;
extern struct Process g_basic_process;
extern struct Process g_demo_process;
extern struct Process g_math_process;
extern struct Process g_sort_process;
extern struct Process g_mem_process;
extern struct Process g_fault_process;
extern struct Process g_halt_process;
extern struct Process g_far_process;
extern struct Process g_pfault_process;
extern struct Process g_sfault_process;
extern _Thread_local struct UserTls g_user_tls;
extern u32 g_syscall_cursor;
extern u64 g_active_user_registers[16];
extern const u8 g_basic_app_elf[];
extern const u64 g_basic_app_elf_len;
extern const u8 g_demo_app_elf[];
extern const u64 g_demo_app_elf_len;
extern const u8 g_math_app_elf[];
extern const u64 g_math_app_elf_len;
extern const u8 g_sort_app_elf[];
extern const u64 g_sort_app_elf_len;
extern const u8 g_mem_app_elf[];
extern const u64 g_mem_app_elf_len;
extern const u8 g_fault_app_elf[];
extern const u64 g_fault_app_elf_len;
extern const u8 g_halt_app_elf[];
extern const u64 g_halt_app_elf_len;
extern const u8 g_far_app_elf[];
extern const u64 g_far_app_elf_len;
extern const u8 g_pfault_app_elf[];
extern const u64 g_pfault_app_elf_len;
extern const u8 g_sfault_app_elf[];
extern const u64 g_sfault_app_elf_len;
extern u8 __kernel_text_start[];
extern u8 __kernel_text_end[];
extern u8 __user_text_start[];
extern u8 __user_text_end[];
extern u8 __kernel_rodata_start[];
extern u8 __kernel_rodata_end[];
extern u8 __user_rodata_start[];
extern u8 __user_rodata_end[];
extern u8 __kernel_data_start[];
extern u8 __kernel_data_end[];
extern u8 __tls_start[];
extern u8 __tls_end[];
extern u8 __kernel_stack_start[];
extern u8 __kernel_stack_end[];
extern u8 __user_stack_start[];
extern u8 __user_stack_end[];
extern u8 __page_pool_start[];
extern u8 __page_pool_end[];
extern u8 kernel_stack_top[];
extern u8 interrupt_stack_top[];
extern u8 fault_stack_top[];
extern u8 double_fault_stack_top[];
extern u8 user_stack[];
extern u8 user_stack_top[];

void kernel_main(void);
u64 kernel_syscall_dispatch(u64 code);
u64 kernel_syscall_dispatch_frame(u64 code,
                                  struct UserReturnContext *context);
u64 kernel_event_dispatch(struct ExceptionFrame *frame);
void kernel_privilege_fault_dispatch(struct ExceptionFrame *frame);
u64 kernel_page_fault_dispatch(struct ExceptionFrame *frame);
void kernel_breakpoint_dispatch(struct ExceptionFrame *frame);

void user_main(void);

void syscall_entry(void);
void event_entry(void);
u32 syscall_call(u64 value);
void syscall_put(u64 value);
void syscall_user_sum(u64 value);
u32 syscall_user_result(u64 slot, u64 value);
u8 hex_digit(u64 value);
void trigger_privileged_read(void);
void write_spc(u64 value);
void write_scs(u64 value);
void write_sds(u64 value);
void write_sss(u64 value);
void write_ssp(u64 value);
void write_epc(u64 value);
void write_ecs(u64 value);
void write_eds(u64 value);
void write_iss(u64 value);
void write_isp(u64 value);
void write_fss(u64 value);
void write_fsp(u64 value);
void write_dss(u64 value);
void write_dsp(u64 value);
void write_ecr(u64 value);
void write_gs0(u64 value);
void halt_cpu(void);
u32 read_user_u8(u64 address);
static inline void fb_write_u8(u64 offset, u32 value) {
  *(volatile u8 *)(FB_BASE + offset) = (u8)value;
}

static inline u32 kbd_read_u32(u64 offset) {
  return *(volatile u32 *)(KBD_BASE + offset);
}

void memory_init(void);
u64 memory_alloc_page(void);
void memory_fill_page(u64 addr, u32 seed);
u64 memory_page_checksum(u64 addr, u32 len);
u64 segment_window_for_range(u64 start, u64 end, u32 bounds_only);
u64 memory_create_address_space(u32 asid, u32 include_shell);
void memory_switch_address_space(u64 ptcr, u32 asid);
u32 memory_map_page(u64 ptcr, u64 virtual_address, u64 physical_address,
                    u64 flags);
void memory_clear_user_arena(void);
u64 memory_user_physical(u64 virtual_address);
u32 memory_map_user_page(u64 ptcr, u64 virtual_address, u64 flags);

u32 app_load(struct Process *process, const u8 *image, u64 len, u32 pid);

void process_init(void);
void process_enter_user(void (*entry)(void));
void enter_user_process(u64 entry, u64 sp, u64 cs, u64 ds, u64 ss, u64 gs0);
void process_mark_user_entry(void);
u32 process_exec_app(struct UserReturnContext *context, u32 app_id);
u32 process_exec_basic(struct UserReturnContext *context);
u32 process_exit_current(struct UserReturnContext *context, u32 code);
void process_record_payload(u32 value);
void process_record_yield(u32 ticket);
void process_record_user_sum(u32 value);
void process_record_user_result(u32 slot, u32 value);
void process_record_fault(void);
u64 process_recover_page_fault(struct ExceptionFrame *frame, u32 reason);
u32 process_fault_is_recoverable(const struct ExceptionFrame *frame);
u32 process_user_range_readable(u64 address, u64 len);
void process_mark_halted(void);

void display_clear(u32 color);
void display_fill_rect(u32 x, u32 y, u32 w, u32 h, u32 color);
void display_scroll_up(u32 text_rows);
void display_tty_clear(void);
void display_tty_put_char(u32 ch);
void display_tty_backspace(void);
void display_draw_char(u32 x, u32 y, u32 ch, u32 color);
void display_draw_text(u32 x, u32 y, const char *text, u32 color);
void display_draw_hex8(u32 x, u32 y, u32 value, u32 color);
void display_write_marker(u32 offset, u32 value);
void display_render_boot(void);
void display_render_syscall(u32 index, u32 value, u64 checksum);
void display_render_process(const struct Process *process);
void display_render_yield(u64 yield_count, u32 ticket);
void display_render_fault(u64 error_code, u64 count);
void display_render_event_return(u64 syscall_count);
void display_render_halt(const struct KernelStats *stats);

#endif
