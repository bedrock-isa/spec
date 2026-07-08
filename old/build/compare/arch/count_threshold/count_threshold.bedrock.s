.text
.globl count_threshold
count_threshold:
	TEST.L D0, D0
	JLE.W .Lrepzero1@WORD_PCREL16
	MOV.L D0, D2
	REPGT D2, CMP.L [A0++], D1
	SUB.L D2, D0
	RET
.Lrepzero1:
	CLR D0
	RET
/* end function count_threshold */

