#include "tiny_kernel.h"

#define PRIVILEGED_READ_PROBE_BYTES 6u
#define ECR_VALID 1u
#define ECR_MAX_EDEPTH(value) ((u64)(value) << 8)

struct KernelStats g_kernel_stats;
u32 g_syscall_cursor;

void kernel_main(void) {
  g_kernel_stats.boot_magic = 0xbed000000001ULL;
  g_kernel_stats.syscall_count = 0;
  g_kernel_stats.privilege_fault_count = 0;
  g_kernel_stats.breakpoint_count = 0;
  g_kernel_stats.checksum = 0xbed0ULL;
  g_kernel_stats.last_error = 0;
  g_kernel_stats.payload_count = 0;
  g_kernel_stats.yield_count = 0;
  g_kernel_stats.page_count = 0;
  g_kernel_stats.bad_syscall_count = 0;
  g_kernel_stats.user_mirror = 0;
  g_kernel_stats.last_yield = 0;
  g_kernel_stats.page_fault_count = 0;
  g_kernel_stats.last_fault_address = 0;
  g_kernel_stats.last_fault_reason = 0;
  g_syscall_cursor = 0;

  display_render_boot();
  display_write_marker(0x30, 0x4b);
  memory_init();
  process_init();

  u64 supervisor_segment = KERNEL_SEGMENT_WINDOW;
  write_sss(supervisor_segment);
  write_ssp((u64)kernel_stack_top);
  write_epc((u64)event_entry);
  write_ecs(supervisor_segment);
  write_eds(0);
  write_iss(supervisor_segment);
  write_isp((u64)interrupt_stack_top);
  write_fss(supervisor_segment);
  write_fsp((u64)fault_stack_top);
  write_dss(supervisor_segment);
  write_dsp((u64)double_fault_stack_top);
  write_ecr(ECR_VALID | ECR_MAX_EDEPTH(15));
  display_write_marker(0x64, (u8)supervisor_segment);
  display_write_marker(0x65, (u8)(supervisor_segment >> 8));
  display_write_marker(0x66, (u8)g_user_process.gs0);
  display_write_marker(0x67, (u8)(g_user_process.gs0 >> 8));
  if (g_user_process.ptcr == 0) {
    display_write_marker(0x79, (u8)g_kernel_stats.last_error);
    halt_cpu();
  }
  memory_switch_address_space(g_user_process.ptcr, (u32)g_user_process.asid);
}

void kernel_privilege_fault_dispatch(struct ExceptionFrame *frame,
                                     struct UserReturnContext *context) {
  u64 event_code = frame->event_info;

  if (context != 0)
    context->pc += PRIVILEGED_READ_PROBE_BYTES;
  else
    frame->saved_pc += PRIVILEGED_READ_PROBE_BYTES;
  g_kernel_stats.privilege_fault_count++;
  g_kernel_stats.last_error = event_code;
  process_record_fault();
  display_render_fault(event_code, g_kernel_stats.privilege_fault_count);
  display_render_event_return(g_kernel_stats.syscall_count);
  display_write_marker(0x63, 0x1d);
}

u64 kernel_page_fault_dispatch(struct ExceptionFrame *frame,
                               struct UserReturnContext *context) {
  u32 reason = (u32)(frame->error_code & 0xffu);
  g_kernel_stats.page_fault_count++;
  if ((frame->error_code & (1u << 25)) != 0u)
    g_kernel_stats.last_fault_address = frame->fault_linear;
  else if ((frame->error_code & (1u << 24)) != 0u)
    g_kernel_stats.last_fault_address = frame->fault_ea;
  else
    g_kernel_stats.last_fault_address = 0;
  g_kernel_stats.last_fault_reason = reason;
  display_write_marker(0x79, reason);
  display_write_marker(0x7a, (u8)g_kernel_stats.page_fault_count);

  if (process_fault_is_recoverable(context)) {
    return process_recover_page_fault(context, reason);
  }

  process_mark_halted();
  display_render_fault(frame->error_code, g_kernel_stats.page_fault_count);
  halt_cpu();
  return 0xffu;
}

void kernel_breakpoint_dispatch(struct ExceptionFrame *frame) {
  (void)frame;
  g_kernel_stats.breakpoint_count++;
  process_mark_halted();
  display_render_halt(&g_kernel_stats);
}

u64 kernel_event_dispatch(struct ExceptionFrame *frame,
                          struct UserReturnContext *context) {
  u32 event_code = (u32)frame->event_info;
  if (event_code == EVENT_PRIVILEGE_FAULT) {
    kernel_privilege_fault_dispatch(frame, context);
    return g_active_user_registers[0];
  }
  if (event_code == EVENT_PAGE_FAULT)
    return kernel_page_fault_dispatch(frame, context);
  if (event_code == EVENT_BREAKPOINT) {
    kernel_breakpoint_dispatch(frame);
    return g_active_user_registers[0];
  }

  g_kernel_stats.last_error = event_code;
  process_mark_halted();
  display_render_fault(event_code, 1);
  halt_cpu();
  return 0xffu;
}
