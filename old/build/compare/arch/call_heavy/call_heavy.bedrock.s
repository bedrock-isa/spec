.text
.globl call_heavy
call_heavy:
	PUSHM 0xc0c8
	SUB.Q 16, SP
	MOV.L D0, D7
	MOV.Q A0, A6
	MOV.L D7, [SP + 0]
	CLR D6
	CLR D2
.Lbb2:
	CMP.L D7, D6
	JGE.W .Lbb5@WORD_PCREL16
	MOV.L [A6 + D6.L * 4], D1
	MOV.L D1, D7
	MOV.L D2, D0
	CALL ext_add@PCREL32
	MOV.L D6, D1
	CALL ext_mix@PCREL32
	MOV.L D7, D1
	MOV.L [SP + 0], D7
	ADD.L D6, D1
	CALL ext_fold@PCREL32
	MOV.Q A6, A0
	MOV.L D0, D2
	MOV.L D7, D0
	INC.L D6
	MOV.L D0, D7
	MOV.Q A0, A6
	JMP.W .Lbb2@WORD_PCREL16
.Lbb5:
	MOV.L D2, D0
	ADD.Q 16, SP
	POPM 0xc0c8
	RET
/* end function call_heavy */

