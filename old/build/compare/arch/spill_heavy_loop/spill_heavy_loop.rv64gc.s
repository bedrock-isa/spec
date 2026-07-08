	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"spill_heavy_loop.c"
	.text
	.globl	spill_heavy_loop                # -- Begin function spill_heavy_loop
	.p2align	1
	.type	spill_heavy_loop,@function
spill_heavy_loop:                       # @spill_heavy_loop
# %bb.0:
	addi	sp, sp, -16
	sd	s0, 8(sp)                       # 8-byte Folded Spill
	sgtz	t2, a4
	li	a6, 8
	li	a7, 7
	li	t0, 6
	li	t1, 5
	li	t3, 4
	li	t4, 3
	li	t5, 2
	negw	a5, t2
	and	t2, a5, a4
	li	t6, 1
	beqz	t2, .LBB0_2
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	lw	a5, 0(a0)
	lw	a4, 0(a1)
	lw	s0, 0(a2)
	add	t6, t6, a5
	add	a4, a4, t5
	add	t4, t4, s0
	lw	a5, 0(a3)
	addi	a0, a0, 4
	addi	a1, a1, 4
	addi	a2, a2, 4
	addi	a3, a3, 4
	add	a5, a5, t3
	add	t5, a4, t6
	add	t1, t1, t6
	add	t4, t4, t5
	add	t0, t0, t5
	add	t3, a5, t4
	add	a7, a7, t4
	add	t1, t1, t3
	add	a6, a6, t3
	add	t0, t0, t1
	add	a7, a7, t0
	add	a6, a6, a7
	addiw	t2, t2, -1
	bnez	t2, .LBB0_1
.LBB0_2:
	add	t5, t5, t6
	add	t3, t3, t4
	add	t0, t0, t1
	add	t3, t3, t5
	add	a7, a7, t0
	add	a7, a7, t3
	addw	a0, a7, a6
	ld	s0, 8(sp)                       # 8-byte Folded Reload
	addi	sp, sp, 16
	ret
.Lfunc_end0:
	.size	spill_heavy_loop, .Lfunc_end0-spill_heavy_loop
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
