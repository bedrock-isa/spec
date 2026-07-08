	.file	"multi_vector.c"
	.text
	.globl	mv_sum                          // -- Begin function mv_sum
	.p2align	2
	.type	mv_sum,@function
mv_sum:                                 // @mv_sum
// %bb.0:
	bic	w9, w1, w1, asr #31
	mov	w8, wzr
	cbz	x9, .LBB0_2
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	ldr	w10, [x0], #4
	sub	x9, x9, #1
	add	w8, w10, w8
	cbnz	x9, .LBB0_1
.LBB0_2:
	mov	w0, w8
	ret
.Lfunc_end0:
	.size	mv_sum, .Lfunc_end0-mv_sum
                                        // -- End function
	.globl	mv_dot                          // -- Begin function mv_dot
	.p2align	2
	.type	mv_dot,@function
mv_dot:                                 // @mv_dot
// %bb.0:
	bic	w9, w2, w2, asr #31
	mov	w8, wzr
	cbz	x9, .LBB1_2
.LBB1_1:                                // =>This Inner Loop Header: Depth=1
	ldr	w10, [x0], #4
	sub	x9, x9, #1
	ldr	w11, [x1], #4
	madd	w8, w11, w10, w8
	cbnz	x9, .LBB1_1
.LBB1_2:
	mov	w0, w8
	ret
.Lfunc_end1:
	.size	mv_dot, .Lfunc_end1-mv_dot
                                        // -- End function
	.globl	mv_clamp_store                  // -- Begin function mv_clamp_store
	.p2align	2
	.type	mv_clamp_store,@function
mv_clamp_store:                         // @mv_clamp_store
// %bb.0:
	mov	x8, x0
	bic	w0, w2, w2, asr #31
	mov	x9, x0
	cbz	x9, .LBB2_2
.LBB2_1:                                // =>This Inner Loop Header: Depth=1
	ldr	w10, [x1], #4
	sub	x9, x9, #1
	cmp	w10, w3
	csel	w10, w10, w3, gt
	cmp	w10, w4
	csel	w10, w10, w4, lt
	str	w10, [x8], #4
	cbnz	x9, .LBB2_1
.LBB2_2:
                                        // kill: def $w0 killed $w0 killed $x0
	ret
.Lfunc_end2:
	.size	mv_clamp_store, .Lfunc_end2-mv_clamp_store
                                        // -- End function
	.globl	mv_pipeline                     // -- Begin function mv_pipeline
	.p2align	2
	.type	mv_pipeline,@function
mv_pipeline:                            // @mv_pipeline
// %bb.0:
	stp	x29, x30, [sp, #-48]!           // 16-byte Folded Spill
	stp	x20, x19, [sp, #32]             // 16-byte Folded Spill
	mov	w19, w3
	mov	x20, x2
	mov	w2, w3
	mov	w3, w4
	mov	w4, w5
	stp	x22, x21, [sp, #16]             // 16-byte Folded Spill
	mov	x29, sp
	mov	x21, x1
	mov	x22, x0
	bl	mv_clamp_store
	mov	x0, x22
	mov	w1, w19
	bl	mv_sum
	mov	w22, w0
	mov	x0, x21
	mov	x1, x20
	mov	w2, w19
	bl	mv_dot
	add	w0, w0, w22
	ldp	x20, x19, [sp, #32]             // 16-byte Folded Reload
	ldp	x22, x21, [sp, #16]             // 16-byte Folded Reload
	ldp	x29, x30, [sp], #48             // 16-byte Folded Reload
	ret
.Lfunc_end3:
	.size	mv_pipeline, .Lfunc_end3-mv_pipeline
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
