.text
.globl dot_product
dot_product:
	CLR D1
	TEST.L D0, D0
	JLE.W .Lrepzero1@WORD_PCREL16
	REPG D0, {
		MOV.L [A1++], D4
		MADD.L [A0++], D4, D1
	}
.Lrepzero1:
	MOV.L D1, D0
	RET
/* end function dot_product */

