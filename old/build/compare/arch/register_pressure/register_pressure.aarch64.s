	.file	"register_pressure.c"
	.text
	.globl	register_pressure               // -- Begin function register_pressure
	.p2align	2
	.type	register_pressure,@function
register_pressure:                      // @register_pressure
// %bb.0:
	bic	w12, w1, w1, asr #31
	mov	w8, #8                          // =0x8
	mov	w9, #7                          // =0x7
	mov	w10, #6                         // =0x6
	mov	w11, #5                         // =0x5
	mov	w13, #4                         // =0x4
	mov	w14, #3                         // =0x3
	mov	w15, #2                         // =0x2
	mov	w16, #1                         // =0x1
	cbz	w12, .LBB0_2
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	ldr	w17, [x0], #4
	sub	w12, w12, #1
	add	w16, w17, w16
	add	w15, w16, w15
	add	w14, w15, w14
	add	w13, w14, w13
	add	w11, w13, w11
	add	w10, w11, w10
	add	w9, w10, w9
	add	w8, w9, w8
	cbnz	w12, .LBB0_1
.LBB0_2:
	add	w12, w15, w16
	add	w13, w14, w13
	add	w10, w11, w10
	add	w11, w12, w13
	add	w9, w10, w9
	add	w9, w11, w9
	add	w0, w9, w8
	ret
.Lfunc_end0:
	.size	register_pressure, .Lfunc_end0-register_pressure
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
