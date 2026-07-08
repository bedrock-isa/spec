	.file	"multi_scan.c"
	.text
	.globl	ms_find_zero                    # -- Begin function ms_find_zero
	.type	ms_find_zero,@function
ms_find_zero:                           # @ms_find_zero
# %bb.0:
	movl	%esi, %eax
	xorl	%ecx, %ecx
	testl	%esi, %esi
	cmovlel	%ecx, %eax
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rcx, %rax
	je	.LBB0_5
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	cmpl	$0, (%rdi,%rcx,4)
	je	.LBB0_4
# %bb.3:                                #   in Loop: Header=BB0_1 Depth=1
	incq	%rcx
	jmp	.LBB0_1
.LBB0_4:
	movl	%ecx, %eax
.LBB0_5:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end0:
	.size	ms_find_zero, .Lfunc_end0-ms_find_zero
                                        # -- End function
	.globl	ms_count_ge                     # -- Begin function ms_count_ge
	.type	ms_count_ge,@function
ms_count_ge:                            # @ms_count_ge
# %bb.0:
	movl	%esi, %eax
	xorl	%ecx, %ecx
	testl	%esi, %esi
	cmovlel	%ecx, %eax
.LBB1_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rcx, %rax
	je	.LBB1_4
# %bb.2:                                #   in Loop: Header=BB1_1 Depth=1
	leaq	1(%rcx), %rsi
	cmpl	%edx, (%rdi,%rcx,4)
	movq	%rsi, %rcx
	jl	.LBB1_1
# %bb.3:
	movl	%esi, %eax
.LBB1_4:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end1:
	.size	ms_count_ge, .Lfunc_end1-ms_count_ge
                                        # -- End function
	.globl	ms_copy_prefix                  # -- Begin function ms_copy_prefix
	.type	ms_copy_prefix,@function
ms_copy_prefix:                         # @ms_copy_prefix
# %bb.0:
	movl	%edx, %eax
	xorl	%ecx, %ecx
	testl	%edx, %edx
	cmovlel	%ecx, %eax
.LBB2_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rcx, %rax
	je	.LBB2_5
# %bb.2:                                #   in Loop: Header=BB2_1 Depth=1
	movl	(%rsi,%rcx,4), %edx
	movl	%edx, (%rdi,%rcx,4)
	testl	%edx, %edx
	je	.LBB2_4
# %bb.3:                                #   in Loop: Header=BB2_1 Depth=1
	incq	%rcx
	jmp	.LBB2_1
.LBB2_4:
	movl	%ecx, %eax
.LBB2_5:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end2:
	.size	ms_copy_prefix, .Lfunc_end2-ms_copy_prefix
                                        # -- End function
	.globl	ms_pipeline                     # -- Begin function ms_pipeline
	.type	ms_pipeline,@function
ms_pipeline:                            # @ms_pipeline
# %bb.0:
	pushq	%rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	movl	%ecx, %ebx
	movl	%edx, %ebp
	movq	%rsi, %r14
	movq	%rdi, %r15
	movq	%rsi, %rdi
	movl	%edx, %esi
	callq	ms_find_zero
	movl	%eax, %r12d
	movq	%r14, %rdi
	movl	%ebp, %esi
	movl	%ebx, %edx
	callq	ms_count_ge
	movl	%eax, %ebx
	movq	%r15, %rdi
	movq	%r14, %rsi
	movl	%ebp, %edx
	callq	ms_copy_prefix
	addl	%r12d, %ebx
	addl	%ebx, %eax
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	retq
.Lfunc_end3:
	.size	ms_pipeline, .Lfunc_end3-ms_pipeline
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
