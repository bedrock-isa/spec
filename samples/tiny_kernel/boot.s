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

.globl write_spc
write_spc:
  wrcr r0, 0x0100
  ret

.globl write_scs
write_scs:
  wrcr r0, 0x0101
  ret

.globl write_sds
write_sds:
  wrcr r0, 0x0102
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
  sysret

.balign 16
.globl syscall_entry
syscall_entry:
  call save_user_registers@PCREL32
  sub.q 48, sp
  rdcr 0x010d, r8
  mov.q r8, [sp]
  rdcr 0x0108, r8
  mov.q r8, [sp + 8]
  rdcr 0x0109, r8
  mov.q r8, [sp + 16]
  rdcr 0x010a, r8
  mov.q r8, [sp + 24]
  rdcr 0x010b, r8
  mov.q r8, [sp + 32]
  rdcr 0x010c, r8
  mov.q r8, [sp + 40]
  lea.q [sp], r8
  mov.q r1, r0
  mov.q r8, r1
  call kernel_syscall_dispatch_frame@PCREL32
  mov.q g_active_user_registers@ABS64, r8
  mov.q r0, [r8]
  mov.q [sp + 8], r8
  wrcr r8, 0x0108
  mov.q [sp + 16], r8
  wrcr r8, 0x0109
  mov.q [sp + 24], r8
  wrcr r8, 0x010a
  mov.q [sp + 32], r8
  wrcr r8, 0x010b
  mov.q [sp + 40], r8
  wrcr r8, 0x010c
  mov.q [sp], r8
  wrcr r8, 0x010d
  add.q 48, sp
  call restore_user_registers@PCREL32
  sysret

.balign 16
.globl event_entry
event_entry:
  call save_user_registers@PCREL32
  lea.q [sp], r8
  mov.q r8, r0
  call kernel_event_dispatch@PCREL32
  call restore_user_registers_with_result@PCREL32
  eret

.globl halt_cpu
halt_cpu:
  halt
  ret

.globl read_user_u8
read_user_u8:
  movuc.b [r0], r0
  extzq.b r0, r0
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
