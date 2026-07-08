	.file	"multi_fir.c"
	.text
	.globl	mf_fir_three                    # -- Begin function mf_fir_three
	.type	mf_fir_three,@function
mf_fir_three:                           # @mf_fir_three
# %bb.0:
	movl	%edx, %eax
	xorl	%edx, %edx
	testl	%eax, %eax
	cmovlel	%edx, %eax
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rdx, %rax
	je	.LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	movl	(%rsi,%rdx,4), %r10d
	imull	%ecx, %r10d
	movl	4(%rsi,%rdx,4), %r11d
	imull	%r8d, %r11d
	addl	%r10d, %r11d
	movl	8(%rsi,%rdx,4), %r10d
	imull	%r9d, %r10d
	addl	%r11d, %r10d
	movl	%r10d, (%rdi,%rdx,4)
	incq	%rdx
	jmp	.LBB0_1
.LBB0_3:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end0:
	.size	mf_fir_three, .Lfunc_end0-mf_fir_three
                                        # -- End function
	.globl	mf_scale_store                  # -- Begin function mf_scale_store
	.type	mf_scale_store,@function
mf_scale_store:                         # @mf_scale_store
# %bb.0:
	movl	%edx, %eax
	xorl	%ecx, %ecx
	testl	%edx, %edx
	cmovlel	%ecx, %eax
.LBB1_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rcx, %rax
	je	.LBB1_3
# %bb.2:                                #   in Loop: Header=BB1_1 Depth=1
	movl	(%rsi,%rcx,4), %edx
	leal	1(,%rdx,4), %edx
	movl	%edx, (%rdi,%rcx,4)
	incq	%rcx
	jmp	.LBB1_1
.LBB1_3:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end1:
	.size	mf_scale_store, .Lfunc_end1-mf_scale_store
                                        # -- End function
	.globl	mf_bias_sum                     # -- Begin function mf_bias_sum
	.type	mf_bias_sum,@function
mf_bias_sum:                            # @mf_bias_sum
# %bb.0:
                                        # kill: def $esi killed $esi def $rsi
	xorl	%eax, %eax
	testl	%esi, %esi
	cmovlel	%eax, %esi
	xorl	%ecx, %ecx
.LBB2_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rcx, %rsi
	je	.LBB2_3
# %bb.2:                                #   in Loop: Header=BB2_1 Depth=1
	addl	%edx, %eax
	addl	(%rdi,%rcx,4), %eax
	incq	%rcx
	jmp	.LBB2_1
.LBB2_3:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end2:
	.size	mf_bias_sum, .Lfunc_end2-mf_bias_sum
                                        # -- End function
	.globl	mf_pipeline                     # -- Begin function mf_pipeline
	.type	mf_pipeline,@function
mf_pipeline:                            # @mf_pipeline
# %bb.0:
	pushq	%rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	pushq	%rax
	movl	%r9d, %eax
	movl	%ecx, %ebx
	movq	%rsi, %r14
	movq	%rdi, %r15
	movl	48(%rsp), %r9d
	movq	%rdx, %rsi
	movl	%ecx, %edx
	movl	%r8d, %ecx
	movl	%eax, %r8d
	callq	mf_fir_three
	movl	%eax, %ebp
	movq	%r14, %rdi
	movq	%r15, %rsi
	movl	%ebx, %edx
	callq	mf_scale_store
	addl	%eax, %ebp
	movq	%r14, %rdi
	movl	%ebx, %esi
	movl	%ebp, %edx
	addq	$8, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	jmp	mf_bias_sum                     # TAILCALL
.Lfunc_end3:
	.size	mf_pipeline, .Lfunc_end3-mf_pipeline
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
