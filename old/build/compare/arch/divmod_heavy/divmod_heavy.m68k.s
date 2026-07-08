#NO_APP
	.file	"divmod_heavy.c"
	.text
	.align	2
	.globl	divmod_heavy
	.type	divmod_heavy, @function
divmod_heavy:
	movem.l #12320,-(%sp)
	move.l 16(%sp),%a2
	clr.l %d0
	sub.l %a0,%a0
.L2:
	cmp.l 20(%sp),%a0
	jlt .L3
	movem.l (%sp)+,#1036
	rts
.L3:
	move.l (%a2)+,%d1
	add.l %a0,%d1
	divsl.l 24(%sp),%d2:%d1
	move.l %d1,%d3
	add.l %d3,%d3
	add.l %d3,%d1
	add.l %d1,%d0
	move.l %d2,%d1
	lsl.l #2,%d1
	add.l %d2,%d1
	add.l %d1,%d0
	addq.l #1,%a0
	jra .L2
	.size	divmod_heavy, .-divmod_heavy
	.ident	"GCC: (GNU) 16.1.0"
