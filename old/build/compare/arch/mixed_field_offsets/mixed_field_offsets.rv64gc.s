	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"mixed_field_offsets.c"
	.text
	.globl	mixed_field_offsets             # -- Begin function mixed_field_offsets
	.p2align	1
	.type	mixed_field_offsets,@function
mixed_field_offsets:                    # @mixed_field_offsets
# %bb.0:
	lw	a6, 4(a0)
	ld	a7, 16(a1)
	ld	a5, 40(a1)
	lw	a3, 0(a0)
	lw	a4, 28(a0)
	add	a2, a2, a6
	add	a5, a5, a7
	add	a5, a5, a2
	add	a2, a2, a4
	sd	a5, 40(a1)
	addw	a1, a3, a2
	sw	a2, 28(a0)
	mv	a0, a1
	ret
.Lfunc_end0:
	.size	mixed_field_offsets, .Lfunc_end0-mixed_field_offsets
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
