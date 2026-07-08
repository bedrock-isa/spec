.text
.globl spill_heavy_loop
spill_heavy_loop:
	PUSHM 0x00c0
	CLR A5
	MOV.L 1.W, D1
	MOV.L 2.W, D2
	MOV.L 3.W, D3
	MOV.L 4.W, D4
	MOV.L 5.W, D5
	MOV.L 6.W, D6
	MOV.L 7.W, D7
	MOV.L 8.W, A4
.Lbb2:
	CMP.L D0, A5
	JGE.W .Lbb4@WORD_PCREL16
	ADD.L [A0++], D1
	ADD.L [A1++], D2
	ADD.L D1, D2
	ADD.L [A2++], D3
	ADD.L D2, D3
	ADD.L [A3++], D4
	ADD.L D3, D4
	ADD.L D1, D5
	ADD.L D4, D5
	ADD.L D2, D6
	ADD.L D5, D6
	ADD.L D3, D7
	ADD.L D6, D7
	ADD.L D4, A4
	ADD.L D7, A4
	INC.L A5
	JMP.W .Lbb2@WORD_PCREL16
.Lbb4:
	SUM.L 0x10fe, D0
	POPM 0x00c0
	RET
/* end function spill_heavy_loop */

