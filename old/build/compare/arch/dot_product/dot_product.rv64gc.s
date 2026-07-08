	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"dot_product.c"
	.text
	.globl	dot_product                     # -- Begin function dot_product
	.p2align	1
	.type	dot_product,@function
dot_product:                            # @dot_product
# %bb.0:
	mv	a3, a0
	li	a0, 0
	sgtz	a4, a2
	neg	a4, a4
	and	a2, a2, a4
	beqz	a2, .LBB0_2
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	lw	a4, 0(a3)
	lw	a5, 0(a1)
	addi	a3, a3, 4
	addi	a1, a1, 4
	mul	a4, a5, a4
	addw	a0, a0, a4
	addi	a2, a2, -1
	bnez	a2, .LBB0_1
.LBB0_2:
	ret
.Lfunc_end0:
	.size	dot_product, .Lfunc_end0-dot_product
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
