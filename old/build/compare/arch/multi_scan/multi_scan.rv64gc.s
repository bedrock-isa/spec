	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"multi_scan.c"
	.text
	.globl	ms_find_zero                    # -- Begin function ms_find_zero
	.p2align	1
	.type	ms_find_zero,@function
ms_find_zero:                           # @ms_find_zero
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
	.size	ms_find_zero, .Lfunc_end0-ms_find_zero
                                        # -- End function
	.globl	ms_count_ge                     # -- Begin function ms_count_ge
	.p2align	1
	.type	ms_count_ge,@function
ms_count_ge:                            # @ms_count_ge
# %bb.0:
	li	a3, 0
	sgtz	a4, a1
	neg	a4, a4
	and	a1, a1, a4
	mv	a4, a1
.LBB1_1:                                # =>This Inner Loop Header: Depth=1
	beqz	a4, .LBB1_3
# %bb.2:                                #   in Loop: Header=BB1_1 Depth=1
	lw	a5, 0(a0)
	addi	a3, a3, 1
	addi	a0, a0, 4
	addi	a4, a4, -1
	blt	a5, a2, .LBB1_1
	j	.LBB1_4
.LBB1_3:
	mv	a3, a1
.LBB1_4:
	sext.w	a0, a3
	ret
.Lfunc_end1:
	.size	ms_count_ge, .Lfunc_end1-ms_count_ge
                                        # -- End function
	.globl	ms_copy_prefix                  # -- Begin function ms_copy_prefix
	.p2align	1
	.type	ms_copy_prefix,@function
ms_copy_prefix:                         # @ms_copy_prefix
# %bb.0:
	li	a3, 0
	sgtz	a4, a2
	neg	a4, a4
	and	a2, a2, a4
	mv	a4, a2
	beqz	a2, .LBB2_4
.LBB2_1:                                # =>This Inner Loop Header: Depth=1
	lw	a5, 0(a1)
	sw	a5, 0(a0)
	beqz	a5, .LBB2_3
# %bb.2:                                #   in Loop: Header=BB2_1 Depth=1
	addi	a3, a3, 1
	addi	a1, a1, 4
	addi	a0, a0, 4
	addi	a4, a4, -1
	beqz	a4, .LBB2_4
	j	.LBB2_1
.LBB2_3:
	mv	a2, a3
.LBB2_4:
	sext.w	a0, a2
	ret
.Lfunc_end2:
	.size	ms_copy_prefix, .Lfunc_end2-ms_copy_prefix
                                        # -- End function
	.globl	ms_pipeline                     # -- Begin function ms_pipeline
	.p2align	1
	.type	ms_pipeline,@function
ms_pipeline:                            # @ms_pipeline
# %bb.0:
	addi	sp, sp, -48
	sd	ra, 40(sp)                      # 8-byte Folded Spill
	sd	s0, 32(sp)                      # 8-byte Folded Spill
	sd	s1, 24(sp)                      # 8-byte Folded Spill
	sd	s2, 16(sp)                      # 8-byte Folded Spill
	sd	s3, 8(sp)                       # 8-byte Folded Spill
	sd	s4, 0(sp)                       # 8-byte Folded Spill
	mv	s2, a3
	mv	s1, a2
	mv	s0, a1
	mv	s3, a0
	mv	a0, a1
	mv	a1, a2
	call	ms_find_zero
	mv	s4, a0
	mv	a0, s0
	mv	a1, s1
	mv	a2, s2
	call	ms_count_ge
	mv	s2, a0
	mv	a0, s3
	mv	a1, s0
	mv	a2, s1
	call	ms_copy_prefix
	add	s2, s2, s4
	addw	a0, s2, a0
	ld	ra, 40(sp)                      # 8-byte Folded Reload
	ld	s0, 32(sp)                      # 8-byte Folded Reload
	ld	s1, 24(sp)                      # 8-byte Folded Reload
	ld	s2, 16(sp)                      # 8-byte Folded Reload
	ld	s3, 8(sp)                       # 8-byte Folded Reload
	ld	s4, 0(sp)                       # 8-byte Folded Reload
	addi	sp, sp, 48
	ret
.Lfunc_end3:
	.size	ms_pipeline, .Lfunc_end3-ms_pipeline
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
