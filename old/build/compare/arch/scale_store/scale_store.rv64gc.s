	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"scale_store.c"
	.text
	.globl	scale_store                     # -- Begin function scale_store
	.p2align	1
	.type	scale_store,@function
scale_store:                            # @scale_store
# %bb.0:
	sgtz	a3, a2
	neg	a3, a3
	and	a2, a2, a3
	mv	a3, a2
	beqz	a2, .LBB0_2
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	lw	a4, 0(a1)
	addi	a1, a1, 4
	slli	a4, a4, 2
	addi	a4, a4, 1
	sw	a4, 0(a0)
	addi	a0, a0, 4
	addi	a3, a3, -1
	bnez	a3, .LBB0_1
.LBB0_2:
	sext.w	a0, a2
	ret
.Lfunc_end0:
	.size	scale_store, .Lfunc_end0-scale_store
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
