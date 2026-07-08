	.file	"divmod_heavy.c"
	.text
	.globl	divmod_heavy                    // -- Begin function divmod_heavy
	.p2align	2
	.type	divmod_heavy,@function
divmod_heavy:                           // @divmod_heavy
// %bb.0:
	bic	w10, w1, w1, asr #31
	mov	x9, xzr
	mov	w8, wzr
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	cmp	x10, x9
	b.eq	.LBB0_3
// %bb.2:                               //   in Loop: Header=BB0_1 Depth=1
	ldr	w11, [x0, x9, lsl #2]
	add	w11, w9, w11
	add	x9, x9, #1
	sdiv	w12, w11, w2
	msub	w11, w12, w2, w11
	add	w12, w12, w12, lsl #1
	add	w8, w12, w8
	add	w11, w11, w11, lsl #2
	add	w8, w8, w11
	b	.LBB0_1
.LBB0_3:
	mov	w0, w8
	ret
.Lfunc_end0:
	.size	divmod_heavy, .Lfunc_end0-divmod_heavy
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
