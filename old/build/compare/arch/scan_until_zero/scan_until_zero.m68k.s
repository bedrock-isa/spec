#NO_APP
	.file	"scan_until_zero.c"
	.text
	.align	2
	.globl	scan_until_zero
	.type	scan_until_zero, @function
scan_until_zero:
	move.l 4(%sp),%a0
	clr.l %d0
.L2:
	cmp.l 8(%sp),%d0
	jlt .L4
.L1:
	rts
.L4:
	tst.l (%a0)
	jeq .L1
	addq.l #4,%a0
	addq.l #1,%d0
	jra .L2
	.size	scan_until_zero, .-scan_until_zero
	.ident	"GCC: (GNU) 16.1.0"
