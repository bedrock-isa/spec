	.file	"spill_heavy_loop.c"
	.text
	.globl	spill_heavy_loop                // -- Begin function spill_heavy_loop
	.p2align	2
	.type	spill_heavy_loop,@function
spill_heavy_loop:                       // @spill_heavy_loop
// %bb.0:
	bic	w10, w4, w4, asr #31
	mov	w8, #8                          // =0x8
	mov	w9, #7                          // =0x7
	mov	w11, #6                         // =0x6
	mov	w12, #5                         // =0x5
	mov	w13, #4                         // =0x4
	mov	w14, #3                         // =0x3
	mov	w16, #2                         // =0x2
	mov	w15, #1                         // =0x1
	cbz	w10, .LBB0_2
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	ldr	w17, [x0], #4
	sub	w10, w10, #1
	ldr	w18, [x1], #4
	add	w15, w17, w15
	ldr	w17, [x2], #4
	add	w16, w18, w16
	ldr	w18, [x3], #4
	add	w14, w17, w14
	add	w16, w16, w15
	add	w12, w15, w12
	add	w14, w14, w16
	add	w13, w18, w13
	add	w11, w16, w11
	add	w13, w13, w14
	add	w9, w14, w9
	add	w12, w12, w13
	add	w8, w13, w8
	add	w11, w11, w12
	add	w9, w9, w11
	add	w8, w8, w9
	cbnz	w10, .LBB0_1
.LBB0_2:
	add	w10, w16, w15
	add	w13, w14, w13
	add	w11, w12, w11
	add	w10, w10, w13
	add	w9, w11, w9
	add	w9, w10, w9
	add	w0, w9, w8
	ret
.Lfunc_end0:
	.size	spill_heavy_loop, .Lfunc_end0-spill_heavy_loop
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
