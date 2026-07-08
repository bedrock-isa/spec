#NO_APP
	.file	"multi_scan.c"
	.text
	.align	2
	.globl	ms_find_zero
	.type	ms_find_zero, @function
ms_find_zero:
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
	.size	ms_find_zero, .-ms_find_zero
	.align	2
	.globl	ms_count_ge
	.type	ms_count_ge, @function
ms_count_ge:
	move.l 12(%sp),%d1
	move.l 4(%sp),%a0
	clr.l %d0
.L7:
	cmp.l 8(%sp),%d0
	jge .L6
	addq.l #1,%d0
	cmp.l (%a0)+,%d1
	jgt .L7
.L6:
	rts
	.size	ms_count_ge, .-ms_count_ge
	.align	2
	.globl	ms_copy_prefix
	.type	ms_copy_prefix, @function
ms_copy_prefix:
	move.l %a2,-(%sp)
	move.l 8(%sp),%a1
	clr.l %d1
	clr.l %d0
.L11:
	cmp.l 16(%sp),%d0
	jlt .L13
.L10:
	move.l (%sp)+,%a2
	rts
.L13:
	move.l 12(%sp),%a2
	move.l (%a2,%d1.l),%a0
	move.l %a0,(%a1,%d1.l)
	jeq .L10
	addq.l #4,%d1
	addq.l #1,%d0
	jra .L11
	.size	ms_copy_prefix, .-ms_copy_prefix
	.align	2
	.globl	ms_pipeline
	.type	ms_pipeline, @function
ms_pipeline:
	subq.l #8,%sp
	move.l 20(%sp),-(%sp)
	move.l 20(%sp),-(%sp)
	jsr ms_find_zero
	addq.l #8,%sp
	move.l %d0,(%sp)
	move.l 24(%sp),-(%sp)
	move.l 24(%sp),-(%sp)
	move.l 24(%sp),-(%sp)
	jsr ms_count_ge
	lea (12,%sp),%sp
	move.l %d0,4(%sp)
	move.l 20(%sp),-(%sp)
	move.l 20(%sp),-(%sp)
	move.l 20(%sp),-(%sp)
	jsr ms_copy_prefix
	move.l 12(%sp),%d1
	add.l 16(%sp),%d1
	add.l %d1,%d0
	lea (20,%sp),%sp
	rts
	.size	ms_pipeline, .-ms_pipeline
	.ident	"GCC: (GNU) 16.1.0"
