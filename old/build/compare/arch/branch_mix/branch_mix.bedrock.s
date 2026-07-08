.text
.globl branch_mix
branch_mix:
	CLR D1
	TEST.L D0, D0
	JLE.W .Lrepzero1@WORD_PCREL16
	REPG D0, {
		MOV.L [A0++], D3
		ABS.L D3
		ADD.L D3, D1
	}
.Lrepzero1:
	MOV.L D1, D0
	RET
/* end function branch_mix */

