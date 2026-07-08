#NO_APP
	.file	"fir3.c"
	.text
	.align	2
	.globl	fir_three
	.type	fir_three, @function
fir_three:
	movem.l #12320,-(%sp)
	move.l 24(%sp),%d0
	move.l 20(%sp),%a0
	move.l 16(%sp),%a2
	clr.l %d1
.L2:
	cmp.l %d1,%d0
	jgt .L3
	tst.l %d0
	jge .L4
	clr.l %d0
.L4:
	movem.l (%sp)+,#1036
	rts
.L3:
	move.l 28(%sp),%d2
	muls.l (%a0)+,%d2
	move.l 32(%sp),%d3
	muls.l (%a0),%d3
	move.l %d3,%a1
	add.l %d2,%a1
	move.l 36(%sp),%d2
	muls.l 4(%a0),%d2
	add.l %a1,%d2
	move.l %d2,(%a2)+
	addq.l #1,%d1
	jra .L2
	.size	fir_three, .-fir_three
	.ident	"GCC: (GNU) 16.1.0"
