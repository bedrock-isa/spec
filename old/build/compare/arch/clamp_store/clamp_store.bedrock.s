.text
.globl clamp_store
clamp_store:
	TEST.L D0, D0
	JLE.W .Lrepzero0@WORD_PCREL16
	MOV.L D0, D3
	REPG D3, {
		MOV.L [A1++], D4
		MAXS.L D1, D4
		MINS.L D2, D4
		MOV.L D4, [A0++]
	}
	RET
.Lrepzero0:
	CLR D0
	RET
/* end function clamp_store */

