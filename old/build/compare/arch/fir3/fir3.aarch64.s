	.file	"fir3.c"
	.text
	.globl	fir_three                       // -- Begin function fir_three
	.p2align	2
	.type	fir_three,@function
fir_three:                              // @fir_three
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
	.size	fir_three, .Lfunc_end0-fir_three
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
