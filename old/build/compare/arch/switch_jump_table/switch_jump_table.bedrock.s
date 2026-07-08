.text
.globl switch_jump_table
switch_jump_table:
	AND.L 7.W, D0
	MOV.L [PC + D0.L * 4 + glo1@PCREL32], D0
	ADD.L D1, D0
	RET
/* end function switch_jump_table */

.data
.align 8
glo1:
	.int 3
	.int 5
	.int 7
	.int 11
	.int 13
	.int 17
	.int 19
	.int 23
/* end data */

