#NO_APP
	.file	"register_pressure.c"
	.text
	.align	2
	.globl	register_pressure
	.type	register_pressure, @function
register_pressure:
	movem.l #15904,-(%sp)
	moveq #8,%d5
	move.w #7,%a0
	move.w #6,%a1
	moveq #5,%d2
	moveq #4,%d3
	moveq #3,%d4
	moveq #2,%d0
	moveq #1,%d1
	clr.l %d6
.L2:
	cmp.l 32(%sp),%d6
	jlt .L3
	add.l %d1,%d0
	add.l %d4,%d0
	add.l %d3,%d0
	add.l %d2,%d0
	add.l %a1,%d0
	add.l %a0,%d0
	add.l %d5,%d0
	movem.l (%sp)+,#1148
	rts
.L3:
	move.l 28(%sp),%a2
	addq.l #4,28(%sp)
	add.l (%a2)+,%d1
	add.l %d1,%d0
	add.l %d0,%d4
	add.l %d4,%d3
	add.l %d3,%d2
	add.l %d2,%a1
	add.l %a1,%a0
	add.l %a0,%d5
	addq.l #1,%d6
	jra .L2
	.size	register_pressure, .-register_pressure
	.ident	"GCC: (GNU) 16.1.0"
