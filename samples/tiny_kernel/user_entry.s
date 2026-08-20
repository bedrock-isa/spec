.text
.globl syscall_call
syscall_call:
  mov.q r0, r1
  syscall
  ret
