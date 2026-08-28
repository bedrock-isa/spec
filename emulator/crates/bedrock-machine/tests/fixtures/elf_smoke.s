.text
.globl _start
.type _start, @function
_start:
  mov.q 42, r0
  halt
.size _start, .-_start
