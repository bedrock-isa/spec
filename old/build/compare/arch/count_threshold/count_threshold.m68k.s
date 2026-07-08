#NO_APP
	.file	"count_threshold.c"
	.text
	.align	2
	.globl	count_threshold
	.type	count_threshold, @function
count_threshold:
	move.l 12(%sp),%d1
	move.l 4(%sp),%a0
	clr.l %d0
.L2:
	cmp.l 8(%sp),%d0
	jge .L1
	addq.l #1,%d0
	cmp.l (%a0)+,%d1
	jgt .L2
.L1:
	rts
	.size	count_threshold, .-count_threshold
	.ident	"GCC: (GNU) 16.1.0"
