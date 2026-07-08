#NO_APP
	.file	"pointer_sum.c"
	.text
	.align	2
	.globl	sum
	.type	sum, @function
sum:
	move.l 4(%sp),%a0
	clr.l %d0
	clr.l %d1
.L2:
	cmp.l 8(%sp),%d1
	jlt .L3
	rts
.L3:
	add.l (%a0)+,%d0
	addq.l #1,%d1
	jra .L2
	.size	sum, .-sum
	.ident	"GCC: (GNU) 16.1.0"
