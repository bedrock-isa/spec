.text
.globl register_pressure
register_pressure:
	PUSHM 0x00c0
	CLR A2
	MOV.L 1.W, D1
	MOV.L 2.W, D2
	MOV.L 3.W, D3
	MOV.L 4.W, D4
	MOV.L 5.W, D5
	MOV.L 6.W, D6
	MOV.L 7.W, D7
	MOV.L 8.W, A1
.Lbb2:
	CMP.L D0, A2
	JGE.W .Lbb4@WORD_PCREL16
	ADD.L [A0++], D1
	ADD.L D1, D2
	ADD.L D2, D3
	ADD.L D3, D4
	ADD.L D4, D5
	ADD.L D5, D6
	ADD.L D6, D7
	ADD.L D7, A1
	INC.L A2
	JMP.W .Lbb2@WORD_PCREL16
.Lbb4:
	SUM.L 0x02fe, D0
	POPM 0x00c0
	RET
/* end function register_pressure */

