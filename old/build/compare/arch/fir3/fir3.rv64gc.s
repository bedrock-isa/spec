	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"fir3.c"
	.text
	.globl	fir_three                       # -- Begin function fir_three
	.p2align	1
	.type	fir_three,@function
fir_three:                              # @fir_three
# %bb.0:
	sgtz	a6, a2
	neg	a6, a6
	and	a6, a6, a2
	addi	a1, a1, 8
	mv	a7, a6
	beqz	a6, .LBB0_2
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	lw	a2, -8(a1)
	lw	t0, -4(a1)
	lw	t1, 0(a1)
	addi	a1, a1, 4
	mul	t2, a2, a3
	mul	a2, t0, a4
	mul	t0, t1, a5
	add	a2, a2, t2
	add	a2, a2, t0
	sw	a2, 0(a0)
	addi	a0, a0, 4
	addi	a7, a7, -1
	bnez	a7, .LBB0_1
.LBB0_2:
	sext.w	a0, a6
	ret
.Lfunc_end0:
	.size	fir_three, .Lfunc_end0-fir_three
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
