	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"branch_mix.c"
	.text
	.globl	branch_mix                      # -- Begin function branch_mix
	.p2align	1
	.type	branch_mix,@function
branch_mix:                             # @branch_mix
# %bb.0:
	li	a2, 0
	sgtz	a3, a1
	neg	a3, a3
	and	a1, a1, a3
	beqz	a1, .LBB0_2
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	lw	a3, 0(a0)
	addi	a0, a0, 4
	sraiw	a4, a3, 31
	xor	a3, a3, a4
	sub	a4, a4, a2
	subw	a2, a3, a4
	addi	a1, a1, -1
	bnez	a1, .LBB0_1
.LBB0_2:
	mv	a0, a2
	ret
.Lfunc_end0:
	.size	branch_mix, .Lfunc_end0-branch_mix
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
