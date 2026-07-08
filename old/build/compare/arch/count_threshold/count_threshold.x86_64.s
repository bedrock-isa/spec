	.file	"count_threshold.c"
	.text
	.globl	count_threshold                 # -- Begin function count_threshold
	.type	count_threshold,@function
count_threshold:                        # @count_threshold
# %bb.0:
	movl	%esi, %eax
	xorl	%ecx, %ecx
	testl	%esi, %esi
	cmovlel	%ecx, %eax
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rcx, %rax
	je	.LBB0_4
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	leaq	1(%rcx), %rsi
	cmpl	%edx, (%rdi,%rcx,4)
	movq	%rsi, %rcx
	jl	.LBB0_1
# %bb.3:
	movl	%esi, %eax
.LBB0_4:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end0:
	.size	count_threshold, .Lfunc_end0-count_threshold
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
