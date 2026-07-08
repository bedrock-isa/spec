.text
.globl mf_fir_three
mf_fir_three:
	TEST.L D0, D0
	JLE.W .Lrepzero1@WORD_PCREL16
	MOV.L D0, D4
	REPG D4, {
		CLR D5
		MADD.L [A1++], D1, D5
		MADD.L [A1], D2, D5
		MADD.L [A1 + 4], D3, D5
		MOV.L D5, [A0++]
	}
	RET
.Lrepzero1:
	CLR D0
	RET
/* end function mf_fir_three */

.text
.globl mf_scale_store
mf_scale_store:
	TEST.L D0, D0
	JLE.W .Lrepzero7@WORD_PCREL16
	MOV.L D0, D1
	REPG D1, {
		MOV.L [A1++], D2
		SHL.L 2, D2
		INC.L D2
		MOV.L D2, [A0++]
	}
	RET
.Lrepzero7:
	CLR D0
	RET
/* end function mf_scale_store */

.text
.globl mf_bias_sum
mf_bias_sum:
	CLR D2
	TEST.L D0, D0
	JLE.W .Lrepzero13@WORD_PCREL16
	REPG D0, {
		ADD.L [A0++], D2
		ADD.L D1, D2
	}
.Lrepzero13:
	MOV.L D2, D0
	RET
/* end function mf_bias_sum */

.text
.globl mf_pipeline
mf_pipeline:
	PUSHM 0x40c0
	MOV.Q A0, D7
	MOV.Q A1, A6
	MOV.Q A2, A1
	MOV.L D0, D6
	MOV.Q D7, A0
	CALL mf_fir_three@PCREL32
	MOV.Q D7, A1
	MOV.Q A6, A0
	XCHG.L D0, D6
	MOV.L D0, D7
	MOV.Q A0, A6
	CALL mf_scale_store@PCREL32
	MOV.Q A6, A0
	MOV.L D0, D1
	MOV.L D7, D0
	ADD.L D6, D1
	POPM 0x40c0
	JMP.L mf_bias_sum@WORD_PCREL32
/* end function mf_pipeline */

