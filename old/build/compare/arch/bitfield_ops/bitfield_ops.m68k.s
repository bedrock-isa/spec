#NO_APP
	.file	"bitfield_ops.c"
	.text
	.align	2
	.globl	bitfield_ops
	.type	bitfield_ops, @function
bitfield_ops:
	move.l 8(%sp),%d1
	and.w #64543,%d1
	move.l 4(%sp),%d0
	and.l #999,%d0
	or.l %d1,%d0
	rts
	.size	bitfield_ops, .-bitfield_ops
	.ident	"GCC: (GNU) 16.1.0"
