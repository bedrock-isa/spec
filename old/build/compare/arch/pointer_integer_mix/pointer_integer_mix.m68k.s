#NO_APP
	.file	"pointer_integer_mix.c"
	.text
	.align	2
	.globl	pointer_integer_mix
	.type	pointer_integer_mix, @function
pointer_integer_mix:
	move.l %a2,-(%sp)
	move.l %d2,-(%sp)
	move.l 12(%sp),%d1
	move.l 20(%sp),%d0
	lsl.l #2,%d0
	move.l %d1,%a2
	add.l %d0,%a2
	move.l 24(%sp),%d0
	jpl .L2
	addq.l #3,%d0
.L2:
	and.w #65532,%d0
	move.l %d1,%a0
	add.l %d0,%a0
	move.l 16(%sp),%d2
	sub.l %d1,%d2
	asr.l #2,%d2
	sub.l %a1,%a1
	clr.l %d1
	clr.l %d0
.L3:
	cmp.l 20(%sp),%d1
	jlt .L5
	move.l (%sp)+,%d2
	move.l (%sp)+,%a2
	rts
.L5:
	add.l (%a2,%a1.l),%d0
	add.l (%a0,%a1.l),%d0
	cmp.l %d1,%d2
	jge .L4
	addq.l #1,%d0
.L4:
	addq.l #1,%d1
	addq.l #4,%a1
	jra .L3
	.size	pointer_integer_mix, .-pointer_integer_mix
	.ident	"GCC: (GNU) 16.1.0"
