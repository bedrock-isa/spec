#NO_APP
	.file	"spill_heavy_loop.c"
	.text
	.align	2
	.globl	spill_heavy_loop
	.type	spill_heavy_loop, @function
spill_heavy_loop:
	movem.l #16160,-(%sp)
	clr.l %d6
	moveq #8,%d2
	moveq #7,%d3
	moveq #6,%d4
	moveq #5,%d5
	move.w #4,%a0
	move.w #3,%a1
	moveq #2,%d0
	moveq #1,%d1
	clr.l %d7
.L2:
	cmp.l 48(%sp),%d7
	jlt .L3
	add.l %d1,%d0
	add.l %a1,%d0
	add.l %a0,%d0
	add.l %d5,%d0
	add.l %d4,%d0
	add.l %d3,%d0
	add.l %d2,%d0
	movem.l (%sp)+,#1276
	rts
.L3:
	move.l 32(%sp),%a2
	add.l (%a2,%d6.l),%d1
	move.l 36(%sp),%a2
	add.l (%a2,%d6.l),%d0
	add.l %d1,%d0
	move.l 40(%sp),%a2
	add.l (%a2,%d6.l),%a1
	add.l %d0,%a1
	move.l 44(%sp),%a2
	add.l (%a2,%d6.l),%a0
	add.l %a1,%a0
	add.l %d1,%d5
	add.l %a0,%d5
	add.l %d0,%d4
	add.l %d5,%d4
	add.l %a1,%d3
	add.l %d4,%d3
	add.l %a0,%d2
	add.l %d3,%d2
	addq.l #1,%d7
	addq.l #4,%d6
	jra .L2
	.size	spill_heavy_loop, .-spill_heavy_loop
	.ident	"GCC: (GNU) 16.1.0"
