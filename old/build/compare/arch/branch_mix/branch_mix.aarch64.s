	.file	"branch_mix.c"
	.text
	.globl	branch_mix                      // -- Begin function branch_mix
	.p2align	2
	.type	branch_mix,@function
branch_mix:                             // @branch_mix
// %bb.0:
	bic	w9, w1, w1, asr #31
	mov	w8, wzr
	cbz	x9, .LBB0_2
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	ldr	w10, [x0], #4
	sub	x9, x9, #1
	cmp	w10, #0
	cneg	w10, w10, mi
	add	w8, w10, w8
	cbnz	x9, .LBB0_1
.LBB0_2:
	mov	w0, w8
	ret
.Lfunc_end0:
	.size	branch_mix, .Lfunc_end0-branch_mix
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
