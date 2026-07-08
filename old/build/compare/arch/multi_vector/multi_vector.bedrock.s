.text
.globl mv_sum
mv_sum:
	CLR D1
	TEST.L D0, D0
	JLE.W .Lrepzero1@WORD_PCREL16
	REP D0, ADD.L [A0++], D1
.Lrepzero1:
	MOV.L D1, D0
	RET
/* end function mv_sum */

.text
.globl mv_dot
mv_dot:
	CLR D1
	TEST.L D0, D0
	JLE.W .Lrepzero7@WORD_PCREL16
	REPG D0, {
		MOV.L [A1++], D4
		MADD.L [A0++], D4, D1
	}
.Lrepzero7:
	MOV.L D1, D0
	RET
/* end function mv_dot */

.text
.globl mv_clamp_store
mv_clamp_store:
	TEST.L D0, D0
	JLE.W .Lrepzero12@WORD_PCREL16
	MOV.L D0, D3
	REPG D3, {
		MOV.L [A1++], D4
		MAXS.L D1, D4
		MINS.L D2, D4
		MOV.L D4, [A0++]
	}
	RET
.Lrepzero12:
	CLR D0
	RET
/* end function mv_clamp_store */

.text
.globl mv_pipeline
mv_pipeline:
	PUSHM 0x40c0
	SUB.Q 16, SP
	MOV.Q A2, [SP + 0]
	MOV.Q A1, A6
	MOV.L D0, D6
	MOV.Q A6, A1
	MOV.Q A0, D7
	CALL mv_clamp_store@PCREL32
	MOV.Q D7, A0
	MOV.L D6, D0
	MOV.Q [SP + 0], D7
	MOV.L D0, D6
	CALL mv_sum@PCREL32
	MOV.Q D7, A1
	MOV.Q A6, A0
	XCHG.L D0, D6
	CALL mv_dot@PCREL32
	ADD.L D6, D0
	ADD.Q 16, SP
	POPM 0x40c0
	RET
/* end function mv_pipeline */

