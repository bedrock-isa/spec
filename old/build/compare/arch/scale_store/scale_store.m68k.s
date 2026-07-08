#NO_APP
	.file	"scale_store.c"
	.text
	.align	2
	.globl	scale_store
	.type	scale_store, @function
scale_store:
	subq.l #4,%sp
	move.l %a2,-(%sp)
	move.l %d2,-(%sp)
	move.l 24(%sp),%d0
	clr.l %d1
	sub.l %a0,%a0
.L2:
	cmp.l %a0,%d0
	jgt .L3
	tst.l %d0
	jge .L4
	clr.l %d0
.L4:
	move.l (%sp)+,%d2
	move.l (%sp)+,%a2
	addq.l #4,%sp
	rts
.L3:
	move.l 20(%sp),%a1
	move.l (%a1,%d1.l),%d2
	lsl.l #2,%d2
	move.l %d2,%a1
	addq.l #1,%a1
	move.l 16(%sp),%a2
	move.l %a1,(%a2,%d1.l)
	addq.l #1,%a0
	addq.l #4,%d1
	jra .L2
	.size	scale_store, .-scale_store
	.ident	"GCC: (GNU) 16.1.0"
