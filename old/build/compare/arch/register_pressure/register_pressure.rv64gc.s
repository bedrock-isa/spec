	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"register_pressure.c"
	.text
	.globl	register_pressure               # -- Begin function register_pressure
	.p2align	1
	.type	register_pressure,@function
register_pressure:                      # @register_pressure
# %bb.0:
	sgtz	a2, a1
	li	a6, 8
	li	a7, 7
	li	t0, 6
	li	t1, 5
	li	t2, 4
	li	a3, 3
	li	a4, 2
	negw	a2, a2
	and	a2, a2, a1
	li	a5, 1
	beqz	a2, .LBB0_2
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	lw	a1, 0(a0)
	addi	a0, a0, 4
	add	a5, a5, a1
	add	a4, a4, a5
	add	a3, a3, a4
	add	t2, t2, a3
	add	t1, t1, t2
	add	t0, t0, t1
	add	a7, a7, t0
	add	a6, a6, a7
	addiw	a2, a2, -1
	bnez	a2, .LBB0_1
.LBB0_2:
	add	a4, a4, a5
	add	a3, a3, t2
	add	t0, t0, t1
	add	a3, a3, a4
	add	a7, a7, t0
	add	a3, a3, a7
	addw	a0, a3, a6
	ret
.Lfunc_end0:
	.size	register_pressure, .Lfunc_end0-register_pressure
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
