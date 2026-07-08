#NO_APP
	.file	"multi_fir.c"
	.text
	.align	2
	.globl	mf_fir_three
	.type	mf_fir_three, @function
mf_fir_three:
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
	.size	mf_fir_three, .-mf_fir_three
	.align	2
	.globl	mf_scale_store
	.type	mf_scale_store, @function
mf_scale_store:
	subq.l #4,%sp
	move.l %a2,-(%sp)
	move.l %d2,-(%sp)
	move.l 24(%sp),%d0
	clr.l %d1
	sub.l %a0,%a0
.L6:
	cmp.l %a0,%d0
	jgt .L7
	tst.l %d0
	jge .L8
	clr.l %d0
.L8:
	move.l (%sp)+,%d2
	move.l (%sp)+,%a2
	addq.l #4,%sp
	rts
.L7:
	move.l 20(%sp),%a1
	move.l (%a1,%d1.l),%d2
	lsl.l #2,%d2
	move.l %d2,%a1
	addq.l #1,%a1
	move.l 16(%sp),%a2
	move.l %a1,(%a2,%d1.l)
	addq.l #1,%a0
	addq.l #4,%d1
	jra .L6
	.size	mf_scale_store, .-mf_scale_store
	.align	2
	.globl	mf_bias_sum
	.type	mf_bias_sum, @function
mf_bias_sum:
	move.l 4(%sp),%a0
	clr.l %d0
	clr.l %d1
.L10:
	cmp.l 8(%sp),%d1
	jlt .L11
	rts
.L11:
	add.l (%a0)+,%d0
	add.l 12(%sp),%d0
	addq.l #1,%d1
	jra .L10
	.size	mf_bias_sum, .-mf_bias_sum
	.align	2
	.globl	mf_pipeline
	.type	mf_pipeline, @function
mf_pipeline:
	subq.l #4,%sp
	movem.l #14336,-(%sp)
	move.l 20(%sp),%d4
	move.l 24(%sp),%d3
	move.l 32(%sp),%d2
	move.l 44(%sp),-(%sp)
	move.l 44(%sp),-(%sp)
	move.l 44(%sp),-(%sp)
	move.l %d2,-(%sp)
	move.l 44(%sp),-(%sp)
	move.l %d4,-(%sp)
	jsr mf_fir_three
	move.l %d0,36(%sp)
	move.l %d2,-(%sp)
	move.l %d4,-(%sp)
	move.l %d3,-(%sp)
	jsr mf_scale_store
	lea (36,%sp),%sp
	add.l 12(%sp),%d0
	move.l %d0,28(%sp)
	move.l %d2,24(%sp)
	move.l %d3,20(%sp)
	movem.l (%sp)+,#28
	addq.l #4,%sp
	jra mf_bias_sum
	.size	mf_pipeline, .-mf_pipeline
	.ident	"GCC: (GNU) 16.1.0"
