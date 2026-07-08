	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"clamp_store.c"
	.text
	.globl	clamp_store                     # -- Begin function clamp_store
	.p2align	1
	.type	clamp_store,@function
clamp_store:                            # @clamp_store
# %bb.0:
	sgtz	a5, a2
	neg	a5, a5
	and	a6, a5, a2
	mv	a5, a6
	beqz	a6, .LBB0_6
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	lw	a2, 0(a1)
	blt	a3, a2, .LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	mv	a2, a3
.LBB0_3:                                #   in Loop: Header=BB0_1 Depth=1
	blt	a2, a4, .LBB0_5
# %bb.4:                                #   in Loop: Header=BB0_1 Depth=1
	mv	a2, a4
.LBB0_5:                                #   in Loop: Header=BB0_1 Depth=1
	sw	a2, 0(a0)
	addi	a1, a1, 4
	addi	a0, a0, 4
	addi	a5, a5, -1
	bnez	a5, .LBB0_1
.LBB0_6:
	sext.w	a0, a6
	ret
.Lfunc_end0:
	.size	clamp_store, .Lfunc_end0-clamp_store
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
