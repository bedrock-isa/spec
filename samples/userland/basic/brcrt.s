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
  mov.q 32, r2
  shl.q r2, r1
  add.q r1, r0
  mov.q r0, r1
  syscall
  ret
