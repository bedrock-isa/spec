#NO_APP
	.file	"clamp_store.c"
	.text
	.align	2
	.globl	clamp_store
	.type	clamp_store, @function
clamp_store:
	move.l %a2,-(%sp)
	move.l 16(%sp),%d0
	sub.l %a0,%a0
	sub.l %a1,%a1
.L2:
	cmp.l %a1,%d0
	jgt .L5
	tst.l %d0
	jge .L6
	clr.l %d0
.L6:
	move.l (%sp)+,%a2
	rts
.L5:
	move.l 12(%sp),%a2
	move.l (%a2,%a0.l),%d1
	cmp.l 20(%sp),%d1
	jge .L3
	move.l 20(%sp),%d1
.L3:
	cmp.l 24(%sp),%d1
	jle .L4
	move.l 24(%sp),%d1
.L4:
	move.l 8(%sp),%a2
	move.l %d1,(%a2,%a0.l)
	addq.l #1,%a1
	addq.l #4,%a0
	jra .L2
	.size	clamp_store, .-clamp_store
	.ident	"GCC: (GNU) 16.1.0"
