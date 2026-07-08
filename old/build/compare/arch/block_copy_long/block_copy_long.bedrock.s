.text
.globl block_copy_long
block_copy_long:
	TEST.L D0, D0
	JLE.W .Lrepzero1@WORD_PCREL16
	MOV.L D0, D1
	REP D1, MOV.Q [A1++], [A0++]
	RET
.Lrepzero1:
	CLR D0
	RET
/* end function block_copy_long */

