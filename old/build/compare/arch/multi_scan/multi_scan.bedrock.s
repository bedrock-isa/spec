.text
.globl ms_find_zero
ms_find_zero:
	TEST.L D0, D0
	JLE.W .Lrepzero1@WORD_PCREL16
	MOV.L D0, D1
	REPNE D1, MOV.L [A0++], D2
	SUB.L D1, D0
	RET
.Lrepzero1:
	CLR D0
	RET
/* end function ms_find_zero */

.text
.globl ms_count_ge
ms_count_ge:
	TEST.L D0, D0
	JLE.W .Lrepzero10@WORD_PCREL16
	MOV.L D0, D2
	REPGT D2, CMP.L [A0++], D1
	SUB.L D2, D0
	RET
.Lrepzero10:
	CLR D0
	RET
/* end function ms_count_ge */

.text
.globl ms_copy_prefix
ms_copy_prefix:
	TEST.L D0, D0
	JLE.W .Lrepzero15@WORD_PCREL16
	MOV.L D0, D1
	REPNE D1, MOV.L [A1++], [A0++]
	SUB.L D1, D0
	RET
.Lrepzero15:
	CLR D0
	RET
/* end function ms_copy_prefix */

.text
.globl ms_pipeline
ms_pipeline:
	PUSHM 0x40c0
	SUB.Q 16, SP
	MOV.L D1, [SP + 4]
	MOV.Q A1, D7
	MOV.L D0, D6
	MOV.Q A0, A6
	MOV.Q D7, A0
	CALL ms_find_zero@PCREL32
	MOV.Q A6, A0
	MOV.L D0, [SP + 0]
	MOV.L D6, D0
	MOV.L [SP + 4], D1
	MOV.L D0, D6
	MOV.Q A0, A6
	MOV.Q D7, A0
	CALL ms_count_ge@PCREL32
	MOV.Q D7, A1
	MOV.Q A6, A0
	MOV.L D0, D7
	MOV.L D6, D0
	MOV.L [SP + 0], D6
	CALL ms_copy_prefix@PCREL32
	MOV.L D0, D1
	MOV.L D6, D0
	ADD.L D7, D0
	ADD.L D1, D0
	ADD.Q 16, SP
	POPM 0x40c0
	RET
/* end function ms_pipeline */

