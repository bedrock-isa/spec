.text
.globl copy_words
copy_words:
	TEST.L D0, D0
	JLE.W .Lrepzero1@WORD_PCREL16
	MOV.L D0, D1
	REP D1, MOV.L [A1++], [A0++]
	RET
.Lrepzero1:
	CLR D0
	RET
/* end function copy_words */

