	.file	"mixed_field_offsets.c"
	.text
	.globl	mixed_field_offsets             // -- Begin function mixed_field_offsets
	.p2align	2
	.type	mixed_field_offsets,@function
mixed_field_offsets:                    // @mixed_field_offsets
// %bb.0:
	ldp	w13, w9, [x0]
                                        // kill: def $w9 killed $w9 def $x9
	ldr	x10, [x1, #16]
	ldr	x11, [x1, #40]
	mov	x8, x0
	sxtw	x9, w9
	ldr	w12, [x0, #28]
	add	x10, x10, x11
	add	x14, x9, w2, sxtw
	add	w9, w9, w2
	add	w9, w9, w12
	add	x10, x14, x10
	add	w0, w13, w9
	str	w9, [x8, #28]
	str	x10, [x1, #40]
	ret
.Lfunc_end0:
	.size	mixed_field_offsets, .Lfunc_end0-mixed_field_offsets
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
