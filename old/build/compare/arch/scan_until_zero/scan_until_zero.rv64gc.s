	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"scan_until_zero.c"
	.text
	.globl	scan_until_zero                 # -- Begin function scan_until_zero
	.p2align	1
	.type	scan_until_zero,@function
scan_until_zero:                        # @scan_until_zero
# %bb.0:
	li	a2, 0
	sgtz	a3, a1
	neg	a3, a3
	and	a1, a1, a3
	mv	a3, a1
	beqz	a1, .LBB0_4
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	lw	a4, 0(a0)
	beqz	a4, .LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	addi	a2, a2, 1
	addi	a0, a0, 4
	addi	a3, a3, -1
	beqz	a3, .LBB0_4
	j	.LBB0_1
.LBB0_3:
	mv	a1, a2
.LBB0_4:
	sext.w	a0, a1
	ret
.Lfunc_end0:
	.size	scan_until_zero, .Lfunc_end0-scan_until_zero
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
