	.file	"scale_store.c"
	.text
	.globl	scale_store                     // -- Begin function scale_store
	.p2align	2
	.type	scale_store,@function
scale_store:                            // @scale_store
// %bb.0:
	mov	x8, x0
	bic	w0, w2, w2, asr #31
	mov	w9, #1                          // =0x1
	mov	x10, x0
	cbz	x10, .LBB0_2
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	ldr	w11, [x1], #4
	sub	x10, x10, #1
	orr	w11, w9, w11, lsl #2
	str	w11, [x8], #4
	cbnz	x10, .LBB0_1
.LBB0_2:
                                        // kill: def $w0 killed $w0 killed $x0
	ret
.Lfunc_end0:
	.size	scale_store, .Lfunc_end0-scale_store
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
