.text

.globl br_syscall
br_syscall:
  mov.q r0, r1
  syscall
  ret

.globl br_exit
br_exit:
  extzq.l r0, r0
  mov.q 11, r1
  shl.q 32, r1
  add.q r1, r0
  mov.q r0, r1
  syscall
  ret

.globl trigger_privileged_read
trigger_privileged_read:
  rdcr PTCR, r2
  ret

.globl app_segment_read_u8
app_segment_read_u8:
  wrseg r0, gs1
  mov.b [gs1:0 + r1], r0
  extzq.b r0, r0
  ret

.globl app_segment_write_u8
app_segment_write_u8:
  wrseg r0, gs1
  mov.b r2, [gs1:0 + r1]
  ret

.globl app_segment_image_round_trip
app_segment_image_round_trip:
  wrseg r0, gs1
  rdseg gs1, r0
  ret
