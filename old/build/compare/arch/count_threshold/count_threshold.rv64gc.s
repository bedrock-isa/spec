	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"count_threshold.c"
	.text
	.globl	count_threshold                 # -- Begin function count_threshold
	.p2align	1
	.type	count_threshold,@function
count_threshold:                        # @count_threshold
# %bb.0:
	li	a3, 0
	sgtz	a4, a1
	neg	a4, a4
	and	a1, a1, a4
	mv	a4, a1
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	beqz	a4, .LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	lw	a5, 0(a0)
	addi	a3, a3, 1
	addi	a0, a0, 4
	addi	a4, a4, -1
	blt	a5, a2, .LBB0_1
	j	.LBB0_4
.LBB0_3:
	mv	a3, a1
.LBB0_4:
	sext.w	a0, a3
	ret
.Lfunc_end0:
	.size	count_threshold, .Lfunc_end0-count_threshold
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
