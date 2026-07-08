#NO_APP
	.file	"block_copy_long.c"
	.text
	.align	2
	.globl	block_copy_long
	.type	block_copy_long, @function
block_copy_long:
	move.l %a2,-(%sp)
	move.l 8(%sp),%a1
	move.l 16(%sp),%d0
	clr.l %d1
	sub.l %a0,%a0
.L2:
	cmp.l %a0,%d0
	jgt .L3
	tst.l %d0
	jge .L4
	clr.l %d0
.L4:
	move.l (%sp)+,%a2
	rts
.L3:
	move.l 12(%sp),%a2
	move.l (%a2,%d1.l),(%a1,%d1.l)
	addq.l #1,%a0
	addq.l #4,%d1
	jra .L2
	.size	block_copy_long, .-block_copy_long
	.ident	"GCC: (GNU) 16.1.0"
