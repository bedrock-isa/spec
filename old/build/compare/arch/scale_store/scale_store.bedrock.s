.text
.globl scale_store
scale_store:
	TEST.L D0, D0
	JLE.W .Lrepzero1@WORD_PCREL16
	MOV.L D0, D1
	REPG D1, {
		MOV.L [A1++], D2
		SHL.L 2, D2
		INC.L D2
		MOV.L D2, [A0++]
	}
	RET
.Lrepzero1:
	CLR D0
	RET
/* end function scale_store */

