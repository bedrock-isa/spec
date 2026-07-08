.text
.globl mixed_field_offsets
mixed_field_offsets:
	MOV.L [A0 + 4], D1
	MOV.L [A0 + 28], D2
	MOV.Q [A1 + 16], D3
	EXTSQ.L D1, D4
	ADD.Q D4, D3
	EXTSQ.L D0, D4
	ADD.Q D4, D3
	ADD.Q D3, [A1 + 40]
	ADD.L D2, D1
	ADD.L D0, D1
	MOV.L D1, [A0 + 28]
	MOV.L [A0], D0
	ADD.L D1, D0
	RET
/* end function mixed_field_offsets */

