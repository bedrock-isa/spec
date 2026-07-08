	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"pointer_integer_mix.c"
	.text
	.globl	pointer_integer_mix             # -- Begin function pointer_integer_mix
	.p2align	1
	.type	pointer_integer_mix,@function
pointer_integer_mix:                    # @pointer_integer_mix
# %bb.0:
	mv	a6, a0
	li	a5, 0
	li	a0, 0
	li	a4, 4
	div	a4, a3, a4
	sgtz	a3, a2
	neg	a3, a3
	and	t0, a3, a2
	slli	a2, a2, 2
	sub	a7, a1, a6
	add	t1, a6, a2
	slli	a4, a4, 2
	add	a4, a4, a6
	srai	a6, a7, 2
	beqz	t0, .LBB0_2
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	lw	a3, 0(t1)
	lw	a2, 0(a4)
	addi	t1, t1, 4
	addi	a4, a4, 4
	slt	a1, a6, a5
	add	a0, a0, a1
	add	a0, a0, a3
	addw	a0, a0, a2
	addi	a5, a5, 1
	bne	t0, a5, .LBB0_1
.LBB0_2:
	ret
.Lfunc_end0:
	.size	pointer_integer_mix, .Lfunc_end0-pointer_integer_mix
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
