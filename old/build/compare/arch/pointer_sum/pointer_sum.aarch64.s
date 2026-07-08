	.file	"pointer_sum.c"
	.text
	.globl	sum                             // -- Begin function sum
	.p2align	2
	.type	sum,@function
sum:                                    // @sum
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
	.size	sum, .Lfunc_end0-sum
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
