	.file	"multi_fir.c"
	.text
	.globl	mf_fir_three                    // -- Begin function mf_fir_three
	.p2align	2
	.type	mf_fir_three,@function
mf_fir_three:                           // @mf_fir_three
// %bb.0:
	mov	x8, x0
	bic	w0, w2, w2, asr #31
	add	x9, x1, #8
	mov	x10, x0
	cbz	x10, .LBB0_2
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	ldp	w11, w12, [x9, #-8]
	ldr	w13, [x9], #4
	sub	x10, x10, #1
	mul	w11, w11, w3
	madd	w11, w12, w4, w11
	madd	w11, w13, w5, w11
	str	w11, [x8], #4
	cbnz	x10, .LBB0_1
.LBB0_2:
                                        // kill: def $w0 killed $w0 killed $x0
	ret
.Lfunc_end0:
	.size	mf_fir_three, .Lfunc_end0-mf_fir_three
                                        // -- End function
	.globl	mf_scale_store                  // -- Begin function mf_scale_store
	.p2align	2
	.type	mf_scale_store,@function
mf_scale_store:                         // @mf_scale_store
// %bb.0:
	mov	x8, x0
	bic	w0, w2, w2, asr #31
	mov	w9, #1                          // =0x1
	mov	x10, x0
	cbz	x10, .LBB1_2
.LBB1_1:                                // =>This Inner Loop Header: Depth=1
	ldr	w11, [x1], #4
	sub	x10, x10, #1
	orr	w11, w9, w11, lsl #2
	str	w11, [x8], #4
	cbnz	x10, .LBB1_1
.LBB1_2:
                                        // kill: def $w0 killed $w0 killed $x0
	ret
.Lfunc_end1:
	.size	mf_scale_store, .Lfunc_end1-mf_scale_store
                                        // -- End function
	.globl	mf_bias_sum                     // -- Begin function mf_bias_sum
	.p2align	2
	.type	mf_bias_sum,@function
mf_bias_sum:                            // @mf_bias_sum
// %bb.0:
	bic	w9, w1, w1, asr #31
	mov	w8, wzr
	cbz	x9, .LBB2_2
.LBB2_1:                                // =>This Inner Loop Header: Depth=1
	ldr	w10, [x0], #4
	add	w8, w8, w2
	sub	x9, x9, #1
	add	w8, w8, w10
	cbnz	x9, .LBB2_1
.LBB2_2:
	mov	w0, w8
	ret
.Lfunc_end2:
	.size	mf_bias_sum, .Lfunc_end2-mf_bias_sum
                                        // -- End function
	.globl	mf_pipeline                     // -- Begin function mf_pipeline
	.p2align	2
	.type	mf_pipeline,@function
mf_pipeline:                            // @mf_pipeline
// %bb.0:
	stp	x29, x30, [sp, #-48]!           // 16-byte Folded Spill
	stp	x20, x19, [sp, #32]             // 16-byte Folded Spill
	mov	w19, w3
	mov	x20, x1
	mov	x1, x2
	mov	w2, w3
	mov	w3, w4
	mov	w4, w5
	mov	w5, w6
	stp	x22, x21, [sp, #16]             // 16-byte Folded Spill
	mov	x29, sp
	mov	x21, x0
	bl	mf_fir_three
	mov	w22, w0
	mov	x0, x20
	mov	x1, x21
	mov	w2, w19
	bl	mf_scale_store
	mov	w8, w0
	mov	x0, x20
	mov	w1, w19
	add	w2, w8, w22
	ldp	x20, x19, [sp, #32]             // 16-byte Folded Reload
	ldp	x22, x21, [sp, #16]             // 16-byte Folded Reload
	ldp	x29, x30, [sp], #48             // 16-byte Folded Reload
	b	mf_bias_sum
.Lfunc_end3:
	.size	mf_pipeline, .Lfunc_end3-mf_pipeline
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
