.text
.globl divmod_heavy
divmod_heavy:
	CLR D3
	CLR D2
.Lbb2:
	CMP.L D0, D3
	JGE.W .Lbb4@WORD_PCREL16
	MOV.L [A0 + D3.L * 4], D4
	ADD.L D3, D4
	MOV.L D4, D5
	DIVMODS.L D1, D5, D4
	MULU.L 3.W, D5
	ADD.L D5, D2
	MULU.L 5.W, D4
	ADD.L D4, D2
	INC.L D3
	JMP.W .Lbb2@WORD_PCREL16
.Lbb4:
	MOV.L D2, D0
	RET
/* end function divmod_heavy */

