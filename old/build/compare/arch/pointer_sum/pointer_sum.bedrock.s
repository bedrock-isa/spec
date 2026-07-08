.text
.globl sum
sum:
	CLR D1
	TEST.L D0, D0
	JLE.W .Lrepzero1@WORD_PCREL16
	REP D0, ADD.L [A0++], D1
.Lrepzero1:
	MOV.L D1, D0
	RET
/* end function sum */

