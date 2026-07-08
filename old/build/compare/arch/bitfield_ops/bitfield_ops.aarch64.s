	.file	"bitfield_ops.c"
	.text
	.globl	bitfield_ops                    // -- Begin function bitfield_ops
	.p2align	2
	.type	bitfield_ops,@function
bitfield_ops:                           // @bitfield_ops
// %bb.0:
	mov	w8, #999                        // =0x3e7
	and	w9, w1, #0xfffffc1f
	and	w8, w0, w8
	orr	w0, w9, w8
	ret
.Lfunc_end0:
	.size	bitfield_ops, .Lfunc_end0-bitfield_ops
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
