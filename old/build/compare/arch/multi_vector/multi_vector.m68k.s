#NO_APP
	.file	"multi_vector.c"
	.text
	.align	2
	.globl	mv_sum
	.type	mv_sum, @function
mv_sum:
	move.l 4(%sp),%a0
	clr.l %d0
	clr.l %d1
.L2:
	cmp.l 8(%sp),%d1
	jlt .L3
	rts
.L3:
	add.l (%a0)+,%d0
	addq.l #1,%d1
	jra .L2
	.size	mv_sum, .-mv_sum
	.align	2
	.globl	mv_dot
	.type	mv_dot, @function
mv_dot:
	move.l %a2,-(%sp)
	move.l %d2,-(%sp)
	move.l 12(%sp),%a1
	clr.l %d1
	clr.l %d0
	sub.l %a0,%a0
.L5:
	cmp.l 20(%sp),%a0
	jlt .L6
	move.l (%sp)+,%d2
	move.l (%sp)+,%a2
	rts
.L6:
	move.l (%a1,%d1.l),%d2
	move.l 16(%sp),%a2
	muls.l (%a2,%d1.l),%d2
	add.l %d2,%d0
	addq.l #1,%a0
	addq.l #4,%d1
	jra .L5
	.size	mv_dot, .-mv_dot
	.align	2
	.globl	mv_clamp_store
	.type	mv_clamp_store, @function
mv_clamp_store:
	move.l %a2,-(%sp)
	move.l 16(%sp),%d0
	sub.l %a0,%a0
	sub.l %a1,%a1
.L8:
	cmp.l %a1,%d0
	jgt .L11
	tst.l %d0
	jge .L12
	clr.l %d0
.L12:
	move.l (%sp)+,%a2
	rts
.L11:
	move.l 12(%sp),%a2
	move.l (%a2,%a0.l),%d1
	cmp.l 20(%sp),%d1
	jge .L9
	move.l 20(%sp),%d1
.L9:
	cmp.l 24(%sp),%d1
	jle .L10
	move.l 24(%sp),%d1
.L10:
	move.l 8(%sp),%a2
	move.l %d1,(%a2,%a0.l)
	addq.l #1,%a1
	addq.l #4,%a0
	jra .L8
	.size	mv_clamp_store, .-mv_clamp_store
	.align	2
	.globl	mv_pipeline
	.type	mv_pipeline, @function
mv_pipeline:
	subq.l #4,%sp
	move.l 28(%sp),-(%sp)
	move.l 28(%sp),-(%sp)
	move.l 28(%sp),-(%sp)
	move.l 24(%sp),-(%sp)
	move.l 24(%sp),-(%sp)
	jsr mv_clamp_store
	move.l 40(%sp),-(%sp)
	move.l 32(%sp),-(%sp)
	jsr mv_sum
	addq.l #8,%sp
	move.l %d0,20(%sp)
	move.l 40(%sp),-(%sp)
	move.l 40(%sp),-(%sp)
	move.l 40(%sp),-(%sp)
	jsr mv_dot
	add.l 32(%sp),%d0
	lea (36,%sp),%sp
	rts
	.size	mv_pipeline, .-mv_pipeline
	.ident	"GCC: (GNU) 16.1.0"
