	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"block_copy_long.c"
	.text
	.globl	block_copy_long                 # -- Begin function block_copy_long
	.p2align	1
	.type	block_copy_long,@function
block_copy_long:                        # @block_copy_long
# %bb.0:
	sgtz	a3, a2
	neg	a3, a3
	and	a2, a2, a3
	mv	a3, a2
	beqz	a2, .LBB0_2
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	ld	a4, 0(a1)
	addi	a1, a1, 8
	sd	a4, 0(a0)
	addi	a0, a0, 8
	addi	a3, a3, -1
	bnez	a3, .LBB0_1
.LBB0_2:
	sext.w	a0, a2
	ret
.Lfunc_end0:
	.size	block_copy_long, .Lfunc_end0-block_copy_long
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
