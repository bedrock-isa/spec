.text
.globl bitfield_ops
bitfield_ops:
	AND.L 999.W, D0
	AND.L -993.W, D1
	OR.L D1, D0
	RET
/* end function bitfield_ops */

