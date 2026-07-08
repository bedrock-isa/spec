	.file	"block_copy_long.c"
	.text
	.globl	block_copy_long                 # -- Begin function block_copy_long
	.type	block_copy_long,@function
block_copy_long:                        # @block_copy_long
# %bb.0:
	movl	%edx, %eax
	xorl	%ecx, %ecx
	testl	%edx, %edx
	cmovlel	%ecx, %eax
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rcx, %rax
	je	.LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	movq	(%rsi,%rcx,8), %rdx
	movq	%rdx, (%rdi,%rcx,8)
	incq	%rcx
	jmp	.LBB0_1
.LBB0_3:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end0:
	.size	block_copy_long, .Lfunc_end0-block_copy_long
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
