	.file	"dot_product.c"
	.text
	.globl	dot_product                     // -- Begin function dot_product
	.p2align	2
	.type	dot_product,@function
dot_product:                            // @dot_product
// %bb.0:
	bic	w9, w2, w2, asr #31
	mov	w8, wzr
	cbz	x9, .LBB0_2
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	ldr	w10, [x0], #4
	sub	x9, x9, #1
	ldr	w11, [x1], #4
	madd	w8, w11, w10, w8
	cbnz	x9, .LBB0_1
.LBB0_2:
	mov	w0, w8
	ret
.Lfunc_end0:
	.size	dot_product, .Lfunc_end0-dot_product
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
