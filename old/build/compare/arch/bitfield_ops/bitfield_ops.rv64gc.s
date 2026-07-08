	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"bitfield_ops.c"
	.text
	.globl	bitfield_ops                    # -- Begin function bitfield_ops
	.p2align	1
	.type	bitfield_ops,@function
bitfield_ops:                           # @bitfield_ops
# %bb.0:
	andi	a1, a1, -993
	andi	a0, a0, 999
	or	a0, a0, a1
	ret
.Lfunc_end0:
	.size	bitfield_ops, .Lfunc_end0-bitfield_ops
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
