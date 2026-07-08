	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"multi_fir.c"
	.text
	.globl	mf_fir_three                    # -- Begin function mf_fir_three
	.p2align	1
	.type	mf_fir_three,@function
mf_fir_three:                           # @mf_fir_three
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
	.size	mf_fir_three, .Lfunc_end0-mf_fir_three
                                        # -- End function
	.globl	mf_scale_store                  # -- Begin function mf_scale_store
	.p2align	1
	.type	mf_scale_store,@function
mf_scale_store:                         # @mf_scale_store
# %bb.0:
	sgtz	a3, a2
	neg	a3, a3
	and	a2, a2, a3
	mv	a3, a2
	beqz	a2, .LBB1_2
.LBB1_1:                                # =>This Inner Loop Header: Depth=1
	lw	a4, 0(a1)
	addi	a1, a1, 4
	slli	a4, a4, 2
	addi	a4, a4, 1
	sw	a4, 0(a0)
	addi	a0, a0, 4
	addi	a3, a3, -1
	bnez	a3, .LBB1_1
.LBB1_2:
	sext.w	a0, a2
	ret
.Lfunc_end1:
	.size	mf_scale_store, .Lfunc_end1-mf_scale_store
                                        # -- End function
	.globl	mf_bias_sum                     # -- Begin function mf_bias_sum
	.p2align	1
	.type	mf_bias_sum,@function
mf_bias_sum:                            # @mf_bias_sum
# %bb.0:
	li	a3, 0
	sgtz	a4, a1
	neg	a4, a4
	and	a1, a1, a4
	beqz	a1, .LBB2_2
.LBB2_1:                                # =>This Inner Loop Header: Depth=1
	lw	a4, 0(a0)
	add	a3, a3, a2
	addi	a0, a0, 4
	addw	a3, a3, a4
	addi	a1, a1, -1
	bnez	a1, .LBB2_1
.LBB2_2:
	mv	a0, a3
	ret
.Lfunc_end2:
	.size	mf_bias_sum, .Lfunc_end2-mf_bias_sum
                                        # -- End function
	.globl	mf_pipeline                     # -- Begin function mf_pipeline
	.p2align	1
	.type	mf_pipeline,@function
mf_pipeline:                            # @mf_pipeline
# %bb.0:
	addi	sp, sp, -48
	sd	ra, 40(sp)                      # 8-byte Folded Spill
	sd	s0, 32(sp)                      # 8-byte Folded Spill
	sd	s1, 24(sp)                      # 8-byte Folded Spill
	sd	s2, 16(sp)                      # 8-byte Folded Spill
	sd	s3, 8(sp)                       # 8-byte Folded Spill
	mv	s0, a3
	mv	s2, a1
	mv	s1, a0
	mv	a1, a2
	mv	a2, a3
	mv	a3, a4
	mv	a4, a5
	mv	a5, a6
	call	mf_fir_three
	mv	s3, a0
	mv	a0, s2
	mv	a1, s1
	mv	a2, s0
	call	mf_scale_store
	addw	a2, a0, s3
	mv	a0, s2
	mv	a1, s0
	ld	ra, 40(sp)                      # 8-byte Folded Reload
	ld	s0, 32(sp)                      # 8-byte Folded Reload
	ld	s1, 24(sp)                      # 8-byte Folded Reload
	ld	s2, 16(sp)                      # 8-byte Folded Reload
	ld	s3, 8(sp)                       # 8-byte Folded Reload
	addi	sp, sp, 48
	tail	mf_bias_sum
.Lfunc_end3:
	.size	mf_pipeline, .Lfunc_end3-mf_pipeline
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
