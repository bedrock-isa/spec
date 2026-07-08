	.file	"scan_until_zero.c"
	.text
	.globl	scan_until_zero                 // -- Begin function scan_until_zero
	.p2align	2
	.type	scan_until_zero,@function
scan_until_zero:                        // @scan_until_zero
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
	.size	scan_until_zero, .Lfunc_end0-scan_until_zero
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
