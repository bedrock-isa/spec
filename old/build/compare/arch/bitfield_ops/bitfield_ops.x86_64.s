	.file	"bitfield_ops.c"
	.text
	.globl	bitfield_ops                    # -- Begin function bitfield_ops
	.type	bitfield_ops,@function
bitfield_ops:                           # @bitfield_ops
# %bb.0:
	movl	%edi, %eax
	andl	$-993, %esi                     # imm = 0xFC1F
	andl	$999, %eax                      # imm = 0x3E7
	orl	%esi, %eax
	retq
.Lfunc_end0:
	.size	bitfield_ops, .Lfunc_end0-bitfield_ops
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
