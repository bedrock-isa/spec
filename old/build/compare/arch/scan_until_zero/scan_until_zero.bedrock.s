.text
.globl scan_until_zero
scan_until_zero:
	TEST.L D0, D0
	JLE.W .Lrepzero1@WORD_PCREL16
	MOV.L D0, D1
	REPNE D1, MOV.L [A0++], D2
	SUB.L D1, D0
	RET
.Lrepzero1:
	CLR D0
	RET
/* end function scan_until_zero */

