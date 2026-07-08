	.file	"clamp_store.c"
	.text
	.globl	clamp_store                     // -- Begin function clamp_store
	.p2align	2
	.type	clamp_store,@function
clamp_store:                            // @clamp_store
// %bb.0:
	mov	x8, x0
	bic	w0, w2, w2, asr #31
	mov	x9, x0
	cbz	x9, .LBB0_2
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	ldr	w10, [x1], #4
	sub	x9, x9, #1
	cmp	w10, w3
	csel	w10, w10, w3, gt
	cmp	w10, w4
	csel	w10, w10, w4, lt
	str	w10, [x8], #4
	cbnz	x9, .LBB0_1
.LBB0_2:
                                        // kill: def $w0 killed $w0 killed $x0
	ret
.Lfunc_end0:
	.size	clamp_store, .Lfunc_end0-clamp_store
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
