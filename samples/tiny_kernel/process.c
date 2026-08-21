#include "tiny_kernel.h"

#define PROCESS_STATE_BOOT 1u
#define PROCESS_STATE_USER 2u
#define PROCESS_STATE_FAULTED 3u
#define PROCESS_STATE_HALTED 4u

struct Process g_user_process;
struct Process g_basic_process;
struct Process g_demo_process;
struct Process g_math_process;
struct Process g_sort_process;
struct Process g_mem_process;
struct Process g_fault_process;
struct Process g_halt_process;
struct Process g_far_process;
struct Process g_pfault_process;
struct Process g_sfault_process;

static struct Process *g_current_process;
static struct UserContext g_shell_context;
u64 g_active_user_registers[16];

struct AppDescriptor {
  u32 id;
  u32 pid;
  struct Process *process;
  const u8 *image;
  const u64 *len;
};

static struct Process *current_process(void) {
  if (g_current_process == 0) {
    return &g_user_process;
  }
  return g_current_process;
}

static void publish_process_markers(void) {
  display_write_marker(0x56, (u8)g_user_process.payload_count);
  display_write_marker(0x57, (u8)g_user_process.yield_count);
  display_write_marker(0x58, (u8)g_kernel_stats.page_count);
  display_write_marker(0x59, (u8)g_user_process.state);
  display_write_marker(0x5b, (u8)g_user_process.page_checksum);
  display_write_marker(0x5c, (u8)(g_user_process.page_checksum >> 8));
  display_write_marker(0x5d, (u8)g_user_process.last_yield);
}

static void reset_process(struct Process *process, u32 pid) {
  process->pid = pid;
  process->state = 0;
  process->syscall_count = 0;
  process->payload_count = 0;
  process->yield_count = 0;
  process->fault_count = 0;
  process->kernel_page = 0;
  process->page_checksum = 0;
  process->last_yield = 0;
  process->code_start = 0;
  process->code_end = 0;
  process->data_start = 0;
  process->data_end = 0;
  process->stack_start = 0;
  process->stack_end = 0;
  process->cs = 0;
  process->ds = 0;
  process->ss = 0;
  process->gs0 = 0;
  process->entry = 0;
  process->ptcr = 0;
  process->asid = pid;
}

static const struct AppDescriptor *app_descriptor(u32 app_id) {
  static const struct AppDescriptor apps[] = {
      {APP_ID_BASIC, 2u, &g_basic_process, g_basic_app_elf,
       &g_basic_app_elf_len},
      {APP_ID_DEMO, 3u, &g_demo_process, g_demo_app_elf, &g_demo_app_elf_len},
      {APP_ID_MATH, 4u, &g_math_process, g_math_app_elf, &g_math_app_elf_len},
      {APP_ID_SORT, 5u, &g_sort_process, g_sort_app_elf, &g_sort_app_elf_len},
      {APP_ID_MEM, 6u, &g_mem_process, g_mem_app_elf, &g_mem_app_elf_len},
      {APP_ID_FAULT, 7u, &g_fault_process, g_fault_app_elf,
       &g_fault_app_elf_len},
      {APP_ID_HALT, 8u, &g_halt_process, g_halt_app_elf, &g_halt_app_elf_len},
      {APP_ID_FAR, 9u, &g_far_process, g_far_app_elf, &g_far_app_elf_len},
      {APP_ID_PFAULT, 10u, &g_pfault_process, g_pfault_app_elf,
       &g_pfault_app_elf_len},
      {APP_ID_SFAULT, 11u, &g_sfault_process, g_sfault_app_elf,
       &g_sfault_app_elf_len},
  };

  for (u32 i = 0; i < sizeof(apps) / sizeof(apps[0]); i++) {
    if (apps[i].id == app_id) {
      return &apps[i];
    }
  }
  return 0;
}

static void save_context(struct UserContext *context,
                         struct UserReturnContext *return_context,
                         const struct Process *process) {
  context->uctl = return_context->uctl;
  context->pc = return_context->pc;
  context->sp = return_context->sp;
  context->cs = return_context->cs;
  context->ds = return_context->ds;
  context->ss = return_context->ss;
  context->gs0 = process->gs0;
  for (u32 i = 0; i < 16u; i++) {
    context->r[i] = g_active_user_registers[i];
  }
}

static void load_user_return_context(struct UserReturnContext *return_context,
                                     const struct UserContext *context) {
  return_context->uctl = context->uctl;
  return_context->pc = context->pc;
  return_context->sp = context->sp;
  return_context->cs = context->cs;
  return_context->ds = context->ds;
  return_context->ss = context->ss;
  write_gs0(context->gs0);
  for (u32 i = 0; i < 16u; i++) {
    g_active_user_registers[i] = context->r[i];
  }
}

static void load_event_context(struct ExceptionFrame *frame,
                               const struct UserContext *context) {
  frame->frame_control =
      (frame->frame_control & 0xffffffffULL) |
      ((context->uctl & 0xffffffffULL) << 32);
  frame->saved_pc = context->pc;
  frame->saved_sp = context->sp;
  frame->saved_cs = context->cs;
  frame->saved_ds = context->ds;
  frame->saved_ss = context->ss;
  write_gs0(context->gs0);
  for (u32 i = 0; i < 16u; i++) {
    g_active_user_registers[i] = context->r[i];
  }
}

void process_init(void) {
  g_user_process.pid = 1;
  g_user_process.state = PROCESS_STATE_BOOT;
  g_user_process.syscall_count = 0;
  g_user_process.payload_count = 0;
  g_user_process.yield_count = 0;
  g_user_process.fault_count = 0;
  g_user_process.last_yield = 0;
  g_user_process.code_start = (u64)__user_text_start;
  g_user_process.code_end = (u64)__user_text_end;
  g_user_process.data_start = (u64)__user_rodata_start;
  g_user_process.data_end = (u64)__tls_end;
  g_user_process.stack_start = (u64)__user_stack_start;
  g_user_process.stack_end = (u64)__user_stack_end;
  g_user_process.cs = segment_window_for_range(g_user_process.code_start,
                                               g_user_process.code_end, 1);
  g_user_process.ds = segment_window_for_range(g_user_process.data_start,
                                               g_user_process.data_end, 1);
  g_user_process.ss = segment_window_for_range(g_user_process.stack_start,
                                               g_user_process.stack_end, 1);
  g_user_process.gs0 =
      segment_window_for_range((u64)__tls_start, (u64)__tls_end, 0);
  g_user_process.entry = (u64)user_main;
  g_user_process.asid = 1u;
  g_user_process.ptcr = memory_create_address_space(1u, 1u);
  g_user_process.kernel_page = memory_alloc_page();
  g_current_process = &g_user_process;
  reset_process(&g_basic_process, 2u);
  reset_process(&g_demo_process, 3u);
  reset_process(&g_math_process, 4u);
  reset_process(&g_sort_process, 5u);
  reset_process(&g_mem_process, 6u);
  reset_process(&g_fault_process, 7u);
  reset_process(&g_halt_process, 8u);
  reset_process(&g_far_process, 9u);
  reset_process(&g_pfault_process, 10u);
  reset_process(&g_sfault_process, 11u);

  if (g_user_process.kernel_page != 0) {
    memory_fill_page(g_user_process.kernel_page, 0x4bu);
    g_user_process.page_checksum =
        memory_page_checksum(g_user_process.kernel_page, KERNEL_PAGE_SIZE);
  } else {
    g_user_process.page_checksum = 0;
  }

  publish_process_markers();
  display_render_process(&g_user_process);
}

void process_enter_user(void (*entry)(void)) {
  g_user_process.state = PROCESS_STATE_USER;
  g_current_process = &g_user_process;
  enter_user_process((u64)entry, g_user_process.stack_end - 16, g_user_process.cs,
                     g_user_process.ds, g_user_process.ss, g_user_process.gs0);
}

void process_mark_user_entry(void) {
  g_current_process = &g_user_process;
  g_user_process.state = PROCESS_STATE_USER;
  publish_process_markers();
  display_render_process(&g_user_process);
}

u32 process_exec_app(struct UserReturnContext *context, u32 app_id) {
  const struct AppDescriptor *app = app_descriptor(app_id);
  if (context == 0 || app == 0 || current_process() != &g_user_process) {
    display_write_marker(0x75, 0xfe);
    return 0xfeu;
  }

  u32 load_error = app_load(app->process, app->image, *app->len, app->pid);
  if (load_error != 0u) {
    display_write_marker(0x75, (u8)load_error);
    return 0x80u | load_error;
  }

  save_context(&g_shell_context, context, &g_user_process);
  for (u32 i = 0; i < 16u; i++) {
    g_active_user_registers[i] = 0;
  }
  app->process->state = PROCESS_STATE_USER;
  g_current_process = app->process;
  context->pc = app->process->entry;
  context->sp = app->process->stack_end - 16;
  context->cs = app->process->cs;
  context->ds = app->process->ds;
  context->ss = app->process->ss;
  write_gs0(app->process->gs0);
  memory_switch_address_space(app->process->ptcr, (u32)app->process->asid);
  display_write_marker(0x70, (u8)app_id);
  display_write_marker(0x75, 0x01);
  display_write_marker(0x76, (u8)app->process->cs);
  display_write_marker(0x77, (u8)app->process->ds);
  return 0;
}

u32 process_exec_basic(struct UserReturnContext *context) {
  return process_exec_app(context, APP_ID_BASIC);
}

u32 process_exit_current(struct UserReturnContext *context, u32 code) {
  struct Process *process = current_process();
  if (context == 0 || process == &g_user_process) {
    return code;
  }

  process->state = PROCESS_STATE_HALTED;
  g_current_process = &g_user_process;
  g_user_process.state = PROCESS_STATE_USER;
  memory_switch_address_space(g_user_process.ptcr, (u32)g_user_process.asid);
  load_user_return_context(context, &g_shell_context);
  display_write_marker(0x78, (u8)code);
  publish_process_markers();
  return code;
}

void process_record_payload(u32 value) {
  (void)value;
  struct Process *process = current_process();
  process->syscall_count++;
  process->payload_count++;
  if (process == &g_user_process) {
    publish_process_markers();
  }
}

void process_record_yield(u32 ticket) {
  struct Process *process = current_process();
  process->syscall_count++;
  process->yield_count++;
  process->last_yield = ticket;
  if (process == &g_user_process) {
    publish_process_markers();
  }
  display_render_yield(process->yield_count, ticket);
}

void process_record_user_sum(u32 value) {
  current_process()->syscall_count++;
  g_kernel_stats.user_mirror = value & 0xffu;
  display_write_marker(0x32, (u8)g_kernel_stats.user_mirror);
  display_write_marker(0x5a, (u8)g_kernel_stats.user_mirror);
  if (current_process() == &g_user_process) {
    publish_process_markers();
  }
}

void process_record_user_result(u32 slot, u32 value) {
  current_process()->syscall_count++;
  display_write_marker(0x68u + (slot & 0x0fu), value & 0xffu);
  if (current_process() == &g_user_process) {
    publish_process_markers();
  }
}

void process_record_fault(void) {
  struct Process *process = current_process();
  process->state = PROCESS_STATE_FAULTED;
  process->fault_count++;
  if (process == &g_user_process) {
    publish_process_markers();
  }
}

u32 process_fault_is_recoverable(const struct ExceptionFrame *frame) {
  if (frame == 0 || current_process() == &g_user_process) {
    return 0;
  }
  return ((frame->frame_control >> 52) & 1u) == 0u;
}

u32 process_user_range_readable(u64 address, u64 len) {
  struct Process *process = current_process();
  u64 end = address + len;
  if (end < address)
    return 0;
  if (address >= process->code_start && end <= process->code_end)
    return 1;
  if (address >= process->data_start && end <= process->data_end)
    return 1;
  if (address >= process->stack_start && end <= process->stack_end)
    return 1;
  return 0;
}

u64 process_recover_page_fault(struct ExceptionFrame *frame, u32 reason) {
  struct Process *process = current_process();
  if (frame == 0 || process == &g_user_process) {
    return 0xffu;
  }

  process->state = PROCESS_STATE_FAULTED;
  process->fault_count++;
  g_current_process = &g_user_process;
  g_user_process.state = PROCESS_STATE_USER;
  memory_switch_address_space(g_user_process.ptcr, (u32)g_user_process.asid);
  load_event_context(frame, &g_shell_context);
  publish_process_markers();
  return 0x80u | (reason & 0x7fu);
}

void process_mark_halted(void) {
  struct Process *process = current_process();
  process->state = PROCESS_STATE_HALTED;
  if (process == &g_user_process) {
    publish_process_markers();
  }
}
