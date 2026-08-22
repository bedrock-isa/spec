.text
.globl _start
_start:
  call kernel_main@PCREL32
  mov.q user_main@ABS64, r0
  call process_enter_user@PCREL32
  mov.q 0xef, r0
  mov.q 0x00f0007f, r8
  mov.b r0, [r8]
  bkpt

.globl trigger_privileged_read
trigger_privileged_read:
  rdcr PTCR, r2
  ret

.globl write_sss
write_sss:
  wrcr r0, 0x0200
  ret

.globl write_ssp
write_ssp:
  wrcr r0, 0x0201
  ret

.globl write_epc
write_epc:
  wrcr r0, 0x0110
  ret

.globl write_ecs
write_ecs:
  wrcr r0, 0x0111
  ret

.globl write_eds
write_eds:
  wrcr r0, 0x0112
  ret

.globl write_iss
write_iss:
  wrcr r0, 0x0210
  ret

.globl write_isp
write_isp:
  wrcr r0, 0x0211
  ret

.globl write_fss
write_fss:
  wrcr r0, 0x0220
  ret

.globl write_fsp
write_fsp:
  wrcr r0, 0x0221
  ret

.globl write_dss
write_dss:
  wrcr r0, 0x0230
  ret

.globl write_dsp
write_dsp:
  wrcr r0, 0x0231
  ret

.globl write_ecr
write_ecr:
  wrcr r0, 0x0002
  ret

.globl write_gs0
write_gs0:
  wrseg r0, gs0
  ret

.globl enter_user_process
enter_user_process:
  wrseg r5, gs0
  wrcr r0, 0x0108
  wrcr r1, 0x0109
  wrcr r2, 0x010a
  wrcr r3, 0x010b
  wrcr r4, 0x010c
  mov.q 0x100000000, r8
  wrcr r8, 0x010d
  eret

.balign 16
.globl syscall_entry
syscall_entry:
  call save_user_registers@PCREL32

syscall_entry_saved:
  sub.q 64, sp
  rdcr 0x010d, r8
  mov.q r8, [sp]
  rdcr 0x010e, r8
  mov.q r8, [sp + 8]
  rdcr 0x0108, r8
  mov.q r8, [sp + 16]
  rdcr 0x0109, r8
  mov.q r8, [sp + 24]
  rdcr 0x010a, r8
  mov.q r8, [sp + 32]
  rdcr 0x010b, r8
  mov.q r8, [sp + 40]
  rdcr 0x010c, r8
  mov.q r8, [sp + 48]
  lea.q [sp], r8
  mov.q r1, r0
  mov.q r8, r1
  call kernel_syscall_dispatch_frame@PCREL32
  mov.q g_active_user_registers@ABS64, r8
  mov.q r0, [r8]
  lea.q [sp], r8
  call write_user_return_context@PCREL32
  add.q 64, sp
  call restore_user_registers@PCREL32
  eret

.balign 16
.globl event_entry
event_entry:
  call save_user_registers@PCREL32
  rdstatus r8
  and.q 0x7c0, r8
  cmp.q 0x440, r8
  jne stacked_event_entry
  rdcr 0x010e, r8
  cmp.q 0x20, r8
  jeq syscall_entry_saved

  # First-level user exceptions have only their optional payload on the
  # supervisor stack. Materialize the kernel's private C view of the frame and
  # a separate authoritative user return context from the U-bank.
  mov.q sp, r9
  sub.q 160, sp
  mov.q 8, [sp]
  mov.q r8, [sp + 8]
  rdcr 0x0108, r8
  mov.q r8, [sp + 16]
  mov.q r8, [sp + 112]
  rdcr 0x0109, r8
  mov.q r8, [sp + 24]
  mov.q r8, [sp + 120]
  rdcr 0x010a, r8
  mov.q r8, [sp + 32]
  mov.q r8, [sp + 128]
  rdcr 0x010b, r8
  mov.q r8, [sp + 40]
  mov.q r8, [sp + 136]
  rdcr 0x010c, r8
  mov.q r8, [sp + 48]
  mov.q r8, [sp + 144]
  rdcr 0x010d, r8
  mov.q r8, [sp + 96]
  rdcr 0x010e, r8
  mov.q r8, [sp + 104]
  mov.q 0, [sp + 56]
  mov.q 0, [sp + 64]
  mov.q 0, [sp + 72]
  mov.q 0, [sp + 80]
  mov.q 0, [sp + 88]
  rdcr 0x010e, r8
  cmp.q 9, r8
  jne dispatch_user_event
  mov.q [r9], r8
  mov.q r8, [sp + 64]
  mov.q [r9 + 8], r8
  mov.q r8, [sp + 72]
  mov.q [r9 + 16], r8
  mov.q r8, [sp + 80]
  mov.q [r9 + 24], r8
  mov.q r8, [sp + 88]

dispatch_user_event:
  lea.q [sp], r8
  mov.q r8, r0
  lea.q [sp + 96], r8
  mov.q r8, r1
  call kernel_event_dispatch@PCREL32
  mov.q g_active_user_registers@ABS64, r8
  mov.q r0, [r8]
  lea.q [sp + 96], r8
  call write_user_return_context@PCREL32
  add.q 160, sp
  call restore_user_registers@PCREL32
  eret

stacked_event_entry:
  lea.q [sp], r8
  mov.q r8, r0
  mov.q 0, r1
  call kernel_event_dispatch@PCREL32
  call restore_user_registers_with_result@PCREL32
  eret

# A return context can select an address space disjoint from the current
# U-bank. Stage the complete bank with paging and segment bounds disabled, then
# reinstate the already-selected address space so no WRCR observes mixed PC/CS
# or SP/SS pairs.
write_user_return_context:
  rdcr PTCR, r9
  rdcr ASCR, r10
  mov.q 16, r11
  shr.q r11, r10
  mov.q 0, r11
  swpt r11
  wrcr r11, 0x010a
  wrcr r11, 0x010c
  mov.q [r8 + 16], r12
  wrcr r12, 0x0108
  mov.q [r8 + 24], r12
  wrcr r12, 0x0109
  mov.q [r8 + 40], r12
  wrcr r12, 0x010b
  mov.q [r8 + 32], r12
  wrcr r12, 0x010a
  mov.q [r8 + 48], r12
  wrcr r12, 0x010c
  mov.q [r8 + 8], r12
  wrcr r12, 0x010e
  mov.q [r8], r12
  wrcr r12, 0x010d
  swpta r9, r10
  ret

.globl halt_cpu
halt_cpu:
  halt
  ret

.globl read_user_u8
read_user_u8:
  movuc.b [r0], r0
  mov.b r0, r0
  ret

save_user_registers:
  push r8
  mov.q g_active_user_registers@ABS64, r8
  mov.q r0, [r8]
  mov.q r1, [r8 + 8]
  mov.q r2, [r8 + 16]
  mov.q r3, [r8 + 24]
  mov.q r4, [r8 + 32]
  mov.q r5, [r8 + 40]
  mov.q r6, [r8 + 48]
  mov.q r7, [r8 + 56]
  mov.q r9, [r8 + 72]
  mov.q r10, [r8 + 80]
  mov.q r11, [r8 + 88]
  mov.q r12, [r8 + 96]
  mov.q r13, [r8 + 104]
  mov.q r14, [r8 + 112]
  mov.q r15, [r8 + 120]
  pop r9
  mov.q r9, [r8 + 64]
  mov.q [r8 + 72], r9
  mov.q [r8 + 64], r8
  ret

restore_user_registers_with_result:
  mov.q g_active_user_registers@ABS64, r8
  mov.q r0, [r8]
  jmp restore_user_registers_loaded

restore_user_registers:
  mov.q g_active_user_registers@ABS64, r8

restore_user_registers_loaded:
  mov.q [r8], r0
  mov.q [r8 + 8], r1
  mov.q [r8 + 16], r2
  mov.q [r8 + 24], r3
  mov.q [r8 + 32], r4
  mov.q [r8 + 40], r5
  mov.q [r8 + 48], r6
  mov.q [r8 + 56], r7
  mov.q [r8 + 72], r9
  mov.q [r8 + 80], r10
  mov.q [r8 + 88], r11
  mov.q [r8 + 96], r12
  mov.q [r8 + 104], r13
  mov.q [r8 + 112], r14
  mov.q [r8 + 120], r15
  mov.q [r8 + 64], r8
  ret

.section .kernel_stack,"aw",@nobits
.balign 64
kernel_stack:
  .space 4096
.globl kernel_stack_top
kernel_stack_top:

.balign 64
interrupt_stack:
  .space 4096
.globl interrupt_stack_top
interrupt_stack_top:

.balign 64
fault_stack:
  .space 4096
.globl fault_stack_top
fault_stack_top:

.balign 64
double_fault_stack:
  .space 4096
.globl double_fault_stack_top
double_fault_stack_top:

.section .user_stack,"aw",@nobits
.balign 16
.globl user_stack
user_stack:
  .space 4096
.globl user_stack_top
user_stack_top:
