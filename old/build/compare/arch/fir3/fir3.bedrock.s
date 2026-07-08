.text
.globl fir_three
fir_three:
	TEST.L D0, D0
	JLE.W .Lrepzero1@WORD_PCREL16
	MOV.L D0, D4
	REPG D4, {
		CLR D5
		MADD.L [A1++], D1, D5
		MADD.L [A1], D2, D5
		MADD.L [A1 + 4], D3, D5
		MOV.L D5, [A0++]
	}
	RET
.Lrepzero1:
	CLR D0
	RET
/* end function fir_three */

