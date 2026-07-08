	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"divmod_heavy.c"
	.text
	.globl	divmod_heavy                    # -- Begin function divmod_heavy
	.p2align	1
	.type	divmod_heavy,@function
divmod_heavy:                           # @divmod_heavy
# %bb.0:
	li	a7, 0
	li	a6, 0
	sgtz	a5, a1
	neg	a5, a5
	and	a1, a1, a5
	beqz	a1, .LBB0_2
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	lw	a5, 0(a0)
	addi	a0, a0, 4
	add	a5, a5, a7
	divw	a3, a5, a2
	addi	a7, a7, 1
	mul	a4, a3, a2
	add	a6, a6, a3
	slli	a3, a3, 1
	sub	a5, a5, a4
	add	a3, a3, a6
	slli	a4, a5, 2
	add	a4, a4, a5
	addw	a6, a3, a4
	addi	a1, a1, -1
	bnez	a1, .LBB0_1
.LBB0_2:
	mv	a0, a6
	ret
.Lfunc_end0:
	.size	divmod_heavy, .Lfunc_end0-divmod_heavy
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
