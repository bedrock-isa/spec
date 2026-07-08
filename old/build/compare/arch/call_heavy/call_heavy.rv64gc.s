	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"call_heavy.c"
	.text
	.globl	call_heavy                      # -- Begin function call_heavy
	.p2align	1
	.type	call_heavy,@function
call_heavy:                             # @call_heavy
# %bb.0:
	addi	sp, sp, -48
	sd	ra, 40(sp)                      # 8-byte Folded Spill
	sd	s0, 32(sp)                      # 8-byte Folded Spill
	sd	s1, 24(sp)                      # 8-byte Folded Spill
	sd	s2, 16(sp)                      # 8-byte Folded Spill
	sd	s3, 8(sp)                       # 8-byte Folded Spill
	mv	s2, a0
	li	s1, 0
	li	a0, 0
	sgtz	a2, a1
	neg	a2, a2
	and	s3, a2, a1
	beqz	s3, .LBB0_2
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	lw	s0, 0(s2)
	mv	a1, s0
	call	ext_add
	mv	a1, s1
	call	ext_mix
	addw	a1, s1, s0
	call	ext_fold
	addi	s2, s2, 4
	addiw	s1, s1, 1
	addi	s3, s3, -1
	bnez	s3, .LBB0_1
.LBB0_2:
	ld	ra, 40(sp)                      # 8-byte Folded Reload
	ld	s0, 32(sp)                      # 8-byte Folded Reload
	ld	s1, 24(sp)                      # 8-byte Folded Reload
	ld	s2, 16(sp)                      # 8-byte Folded Reload
	ld	s3, 8(sp)                       # 8-byte Folded Reload
	addi	sp, sp, 48
	ret
.Lfunc_end0:
	.size	call_heavy, .Lfunc_end0-call_heavy
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
