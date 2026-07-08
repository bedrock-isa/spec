	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"pointer_sum.c"
	.text
	.globl	sum                             # -- Begin function sum
	.p2align	1
	.type	sum,@function
sum:                                    # @sum
# %bb.0:
	mv	a2, a0
	li	a0, 0
	sgtz	a3, a1
	neg	a3, a3
	and	a1, a1, a3
	beqz	a1, .LBB0_2
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	lw	a3, 0(a2)
	addi	a2, a2, 4
	addw	a0, a0, a3
	addi	a1, a1, -1
	bnez	a1, .LBB0_1
.LBB0_2:
	ret
.Lfunc_end0:
	.size	sum, .Lfunc_end0-sum
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
