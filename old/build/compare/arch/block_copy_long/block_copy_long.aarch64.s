	.file	"block_copy_long.c"
	.text
	.globl	block_copy_long                 // -- Begin function block_copy_long
	.p2align	2
	.type	block_copy_long,@function
block_copy_long:                        // @block_copy_long
// %bb.0:
	mov	x8, x0
	bic	w0, w2, w2, asr #31
	mov	x9, x0
	cbz	x9, .LBB0_2
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	ldr	x10, [x1], #8
	sub	x9, x9, #1
	str	x10, [x8], #8
	cbnz	x9, .LBB0_1
.LBB0_2:
                                        // kill: def $w0 killed $w0 killed $x0
	ret
.Lfunc_end0:
	.size	block_copy_long, .Lfunc_end0-block_copy_long
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
