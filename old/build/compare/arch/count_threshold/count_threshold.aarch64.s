	.file	"count_threshold.c"
	.text
	.globl	count_threshold                 // -- Begin function count_threshold
	.p2align	2
	.type	count_threshold,@function
count_threshold:                        // @count_threshold
// %bb.0:
	mov	x8, x0
	bic	w0, w1, w1, asr #31
	mov	x9, xzr
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	cmp	x0, x9
	b.eq	.LBB0_4
// %bb.2:                               //   in Loop: Header=BB0_1 Depth=1
	ldr	w10, [x8, x9, lsl #2]
	add	x9, x9, #1
	cmp	w10, w2
	b.lt	.LBB0_1
// %bb.3:
	mov	w0, w9
.LBB0_4:
                                        // kill: def $w0 killed $w0 killed $x0
	ret
.Lfunc_end0:
	.size	count_threshold, .Lfunc_end0-count_threshold
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
