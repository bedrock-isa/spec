	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"multi_vector.c"
	.text
	.globl	mv_sum                          # -- Begin function mv_sum
	.p2align	1
	.type	mv_sum,@function
mv_sum:                                 # @mv_sum
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
	.size	mv_sum, .Lfunc_end0-mv_sum
                                        # -- End function
	.globl	mv_dot                          # -- Begin function mv_dot
	.p2align	1
	.type	mv_dot,@function
mv_dot:                                 # @mv_dot
# %bb.0:
	mv	a3, a0
	li	a0, 0
	sgtz	a4, a2
	neg	a4, a4
	and	a2, a2, a4
	beqz	a2, .LBB1_2
.LBB1_1:                                # =>This Inner Loop Header: Depth=1
	lw	a4, 0(a3)
	lw	a5, 0(a1)
	addi	a3, a3, 4
	addi	a1, a1, 4
	mul	a4, a5, a4
	addw	a0, a0, a4
	addi	a2, a2, -1
	bnez	a2, .LBB1_1
.LBB1_2:
	ret
.Lfunc_end1:
	.size	mv_dot, .Lfunc_end1-mv_dot
                                        # -- End function
	.globl	mv_clamp_store                  # -- Begin function mv_clamp_store
	.p2align	1
	.type	mv_clamp_store,@function
mv_clamp_store:                         # @mv_clamp_store
# %bb.0:
	sgtz	a5, a2
	neg	a5, a5
	and	a6, a5, a2
	mv	a5, a6
	beqz	a6, .LBB2_6
.LBB2_1:                                # =>This Inner Loop Header: Depth=1
	lw	a2, 0(a1)
	blt	a3, a2, .LBB2_3
# %bb.2:                                #   in Loop: Header=BB2_1 Depth=1
	mv	a2, a3
.LBB2_3:                                #   in Loop: Header=BB2_1 Depth=1
	blt	a2, a4, .LBB2_5
# %bb.4:                                #   in Loop: Header=BB2_1 Depth=1
	mv	a2, a4
.LBB2_5:                                #   in Loop: Header=BB2_1 Depth=1
	sw	a2, 0(a0)
	addi	a1, a1, 4
	addi	a0, a0, 4
	addi	a5, a5, -1
	bnez	a5, .LBB2_1
.LBB2_6:
	sext.w	a0, a6
	ret
.Lfunc_end2:
	.size	mv_clamp_store, .Lfunc_end2-mv_clamp_store
                                        # -- End function
	.globl	mv_pipeline                     # -- Begin function mv_pipeline
	.p2align	1
	.type	mv_pipeline,@function
mv_pipeline:                            # @mv_pipeline
# %bb.0:
	addi	sp, sp, -48
	sd	ra, 40(sp)                      # 8-byte Folded Spill
	sd	s0, 32(sp)                      # 8-byte Folded Spill
	sd	s1, 24(sp)                      # 8-byte Folded Spill
	sd	s2, 16(sp)                      # 8-byte Folded Spill
	sd	s3, 8(sp)                       # 8-byte Folded Spill
	mv	s0, a3
	mv	s2, a2
	mv	s3, a1
	mv	s1, a0
	mv	a2, a3
	mv	a3, a4
	mv	a4, a5
	call	mv_clamp_store
	mv	a0, s1
	mv	a1, s0
	call	mv_sum
	mv	s1, a0
	mv	a0, s3
	mv	a1, s2
	mv	a2, s0
	call	mv_dot
	addw	a0, a0, s1
	ld	ra, 40(sp)                      # 8-byte Folded Reload
	ld	s0, 32(sp)                      # 8-byte Folded Reload
	ld	s1, 24(sp)                      # 8-byte Folded Reload
	ld	s2, 16(sp)                      # 8-byte Folded Reload
	ld	s3, 8(sp)                       # 8-byte Folded Reload
	addi	sp, sp, 48
	ret
.Lfunc_end3:
	.size	mv_pipeline, .Lfunc_end3-mv_pipeline
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
