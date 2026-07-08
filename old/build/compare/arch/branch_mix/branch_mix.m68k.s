#NO_APP
	.file	"branch_mix.c"
	.text
	.align	2
	.globl	branch_mix
	.type	branch_mix, @function
branch_mix:
	move.l 4(%sp),%a1
	clr.l %d0
	clr.l %d1
.L2:
	cmp.l 8(%sp),%d1
	jlt .L5
	rts
.L5:
	move.l (%a1)+,%a0
	tst.l %a0
	jle .L3
	add.l %a0,%d0
.L4:
	addq.l #1,%d1
	jra .L2
.L3:
	sub.l %a0,%d0
	jra .L4
	.size	branch_mix, .-branch_mix
	.ident	"GCC: (GNU) 16.1.0"
