.text
.globl pointer_integer_mix
pointer_integer_mix:
	MOV.Q A1, D3
	SUB.Q A0, D3
	SAR.Q 2, D3
	DIVS.Q 4.W, D1
	LEA [A0 + D1 * 4], A1
	LEA [A0 + D0.L * 4], A0
	CLR D1
	CLR D2
.Lbb2:
	CMP.L D0, D2
	JGE.W .Lbb6@WORD_PCREL16
	MOV.L [A0++], D4
	ADD.L D4, D1
	MOV.L [A1++], D4
	ADD.L D4, D1
	EXTSQ.L D2, D4
	CMP.Q D4, D3
	JGE.W .Lbb5@WORD_PCREL16
	INC.L D1
.Lbb5:
	INC.L D2
	JMP.W .Lbb2@WORD_PCREL16
.Lbb6:
	MOV.L D1, D0
	RET
/* end function pointer_integer_mix */

