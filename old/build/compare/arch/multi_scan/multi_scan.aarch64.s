	.file	"multi_scan.c"
	.text
	.globl	ms_find_zero                    // -- Begin function ms_find_zero
	.p2align	2
	.type	ms_find_zero,@function
ms_find_zero:                           // @ms_find_zero
// %bb.0:
	mov	x8, x0
	bic	w0, w1, w1, asr #31
	mov	x9, xzr
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	cmp	x0, x9
	b.eq	.LBB0_5
// %bb.2:                               //   in Loop: Header=BB0_1 Depth=1
	ldr	w10, [x8, x9, lsl #2]
	cbz	w10, .LBB0_4
// %bb.3:                               //   in Loop: Header=BB0_1 Depth=1
	add	x9, x9, #1
	b	.LBB0_1
.LBB0_4:
	mov	w0, w9
.LBB0_5:
                                        // kill: def $w0 killed $w0 killed $x0
	ret
.Lfunc_end0:
	.size	ms_find_zero, .Lfunc_end0-ms_find_zero
                                        // -- End function
	.globl	ms_count_ge                     // -- Begin function ms_count_ge
	.p2align	2
	.type	ms_count_ge,@function
ms_count_ge:                            // @ms_count_ge
// %bb.0:
	mov	x8, x0
	bic	w0, w1, w1, asr #31
	mov	x9, xzr
.LBB1_1:                                // =>This Inner Loop Header: Depth=1
	cmp	x0, x9
	b.eq	.LBB1_4
// %bb.2:                               //   in Loop: Header=BB1_1 Depth=1
	ldr	w10, [x8, x9, lsl #2]
	add	x9, x9, #1
	cmp	w10, w2
	b.lt	.LBB1_1
// %bb.3:
	mov	w0, w9
.LBB1_4:
                                        // kill: def $w0 killed $w0 killed $x0
	ret
.Lfunc_end1:
	.size	ms_count_ge, .Lfunc_end1-ms_count_ge
                                        // -- End function
	.globl	ms_copy_prefix                  // -- Begin function ms_copy_prefix
	.p2align	2
	.type	ms_copy_prefix,@function
ms_copy_prefix:                         // @ms_copy_prefix
// %bb.0:
	mov	x8, x0
	bic	w0, w2, w2, asr #31
	mov	x9, xzr
.LBB2_1:                                // =>This Inner Loop Header: Depth=1
	cmp	x0, x9
	b.eq	.LBB2_5
// %bb.2:                               //   in Loop: Header=BB2_1 Depth=1
	ldr	w10, [x1, x9, lsl #2]
	str	w10, [x8, x9, lsl #2]
	cbz	w10, .LBB2_4
// %bb.3:                               //   in Loop: Header=BB2_1 Depth=1
	add	x9, x9, #1
	b	.LBB2_1
.LBB2_4:
	mov	w0, w9
.LBB2_5:
                                        // kill: def $w0 killed $w0 killed $x0
	ret
.Lfunc_end2:
	.size	ms_copy_prefix, .Lfunc_end2-ms_copy_prefix
                                        // -- End function
	.globl	ms_pipeline                     // -- Begin function ms_pipeline
	.p2align	2
	.type	ms_pipeline,@function
ms_pipeline:                            // @ms_pipeline
// %bb.0:
	stp	x29, x30, [sp, #-64]!           // 16-byte Folded Spill
	stp	x22, x21, [sp, #32]             // 16-byte Folded Spill
	mov	x21, x1
	mov	x22, x0
	mov	x0, x1
	mov	w1, w2
	str	x23, [sp, #16]                  // 8-byte Spill
	stp	x20, x19, [sp, #48]             // 16-byte Folded Spill
	mov	x29, sp
	mov	w19, w3
	mov	w20, w2
	bl	ms_find_zero
	mov	w23, w0
	mov	x0, x21
	mov	w1, w20
	mov	w2, w19
	bl	ms_count_ge
	mov	w19, w0
	mov	x0, x22
	mov	x1, x21
	mov	w2, w20
	bl	ms_copy_prefix
	add	w8, w19, w23
	ldp	x20, x19, [sp, #48]             // 16-byte Folded Reload
	ldp	x22, x21, [sp, #32]             // 16-byte Folded Reload
	add	w0, w8, w0
	ldr	x23, [sp, #16]                  // 8-byte Reload
	ldp	x29, x30, [sp], #64             // 16-byte Folded Reload
	ret
.Lfunc_end3:
	.size	ms_pipeline, .Lfunc_end3-ms_pipeline
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
