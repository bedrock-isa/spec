	.file	"copy_words.c"
	.text
	.globl	copy_words                      // -- Begin function copy_words
	.p2align	2
	.type	copy_words,@function
copy_words:                             // @copy_words
// %bb.0:
	mov	x8, x0
	bic	w0, w2, w2, asr #31
	mov	x9, x0
	cbz	x9, .LBB0_2
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	ldr	w10, [x1], #4
	sub	x9, x9, #1
	str	w10, [x8], #4
	cbnz	x9, .LBB0_1
.LBB0_2:
                                        // kill: def $w0 killed $w0 killed $x0
	ret
.Lfunc_end0:
	.size	copy_words, .Lfunc_end0-copy_words
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
