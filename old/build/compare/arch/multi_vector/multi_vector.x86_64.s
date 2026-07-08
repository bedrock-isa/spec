	.file	"multi_vector.c"
	.text
	.globl	mv_sum                          # -- Begin function mv_sum
	.type	mv_sum,@function
mv_sum:                                 # @mv_sum
# %bb.0:
                                        # kill: def $esi killed $esi def $rsi
	xorl	%eax, %eax
	testl	%esi, %esi
	cmovlel	%eax, %esi
	xorl	%ecx, %ecx
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rcx, %rsi
	je	.LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	addl	(%rdi,%rcx,4), %eax
	incq	%rcx
	jmp	.LBB0_1
.LBB0_3:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end0:
	.size	mv_sum, .Lfunc_end0-mv_sum
                                        # -- End function
	.globl	mv_dot                          # -- Begin function mv_dot
	.type	mv_dot,@function
mv_dot:                                 # @mv_dot
# %bb.0:
                                        # kill: def $edx killed $edx def $rdx
	xorl	%eax, %eax
	testl	%edx, %edx
	cmovlel	%eax, %edx
	xorl	%ecx, %ecx
.LBB1_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rcx, %rdx
	je	.LBB1_3
# %bb.2:                                #   in Loop: Header=BB1_1 Depth=1
	movl	(%rsi,%rcx,4), %r8d
	imull	(%rdi,%rcx,4), %r8d
	addl	%r8d, %eax
	incq	%rcx
	jmp	.LBB1_1
.LBB1_3:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end1:
	.size	mv_dot, .Lfunc_end1-mv_dot
                                        # -- End function
	.globl	mv_clamp_store                  # -- Begin function mv_clamp_store
	.type	mv_clamp_store,@function
mv_clamp_store:                         # @mv_clamp_store
# %bb.0:
	movl	%edx, %eax
	xorl	%edx, %edx
	testl	%eax, %eax
	cmovlel	%edx, %eax
.LBB2_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rdx, %rax
	je	.LBB2_3
# %bb.2:                                #   in Loop: Header=BB2_1 Depth=1
	movl	(%rsi,%rdx,4), %r9d
	cmpl	%ecx, %r9d
	cmovlel	%ecx, %r9d
	cmpl	%r8d, %r9d
	cmovgel	%r8d, %r9d
	movl	%r9d, (%rdi,%rdx,4)
	incq	%rdx
	jmp	.LBB2_1
.LBB2_3:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end2:
	.size	mv_clamp_store, .Lfunc_end2-mv_clamp_store
                                        # -- End function
	.globl	mv_pipeline                     # -- Begin function mv_pipeline
	.type	mv_pipeline,@function
mv_pipeline:                            # @mv_pipeline
# %bb.0:
	pushq	%rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	movl	%ecx, %ebx
	movq	%rdx, %r14
	movq	%rsi, %r15
	movq	%rdi, %r12
	movl	%ecx, %edx
	movl	%r8d, %ecx
	movl	%r9d, %r8d
	callq	mv_clamp_store
	movq	%r12, %rdi
	movl	%ebx, %esi
	callq	mv_sum
	movl	%eax, %ebp
	movq	%r15, %rdi
	movq	%r14, %rsi
	movl	%ebx, %edx
	callq	mv_dot
	addl	%ebp, %eax
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	retq
.Lfunc_end3:
	.size	mv_pipeline, .Lfunc_end3-mv_pipeline
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
