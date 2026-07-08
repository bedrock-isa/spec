#NO_APP
	.file	"dot_product.c"
	.text
	.align	2
	.globl	dot_product
	.type	dot_product, @function
dot_product:
	move.l %a2,-(%sp)
	move.l %d2,-(%sp)
	move.l 12(%sp),%a1
	clr.l %d1
	clr.l %d0
	sub.l %a0,%a0
.L2:
	cmp.l 20(%sp),%a0
	jlt .L3
	move.l (%sp)+,%d2
	move.l (%sp)+,%a2
	rts
.L3:
	move.l (%a1,%d1.l),%d2
	move.l 16(%sp),%a2
	muls.l (%a2,%d1.l),%d2
	add.l %d2,%d0
	addq.l #1,%a0
	addq.l #4,%d1
	jra .L2
	.size	dot_product, .-dot_product
	.ident	"GCC: (GNU) 16.1.0"
