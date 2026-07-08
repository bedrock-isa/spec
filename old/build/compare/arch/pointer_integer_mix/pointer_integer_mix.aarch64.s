	.file	"pointer_integer_mix.c"
	.text
	.globl	pointer_integer_mix             // -- Begin function pointer_integer_mix
	.p2align	2
	.type	pointer_integer_mix,@function
pointer_integer_mix:                    // @pointer_integer_mix
// %bb.0:
	mov	w9, #4                          // =0x4
	sub	x11, x1, x0
	bic	w12, w2, w2, asr #31
	sdiv	x10, x3, x9
	add	x9, x0, w2, sxtw #2
	asr	x11, x11, #2
	mov	x8, xzr
	add	x10, x0, x10, lsl #2
	mov	w0, wzr
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	cmp	x12, x8
	b.eq	.LBB0_3
// %bb.2:                               //   in Loop: Header=BB0_1 Depth=1
	ldr	w13, [x9, x8, lsl #2]
	cmp	x11, x8
	ldr	w14, [x10, x8, lsl #2]
	cinc	w15, w0, lt
	add	x8, x8, #1
	add	w13, w15, w13
	add	w0, w13, w14
	b	.LBB0_1
.LBB0_3:
	ret
.Lfunc_end0:
	.size	pointer_integer_mix, .Lfunc_end0-pointer_integer_mix
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
