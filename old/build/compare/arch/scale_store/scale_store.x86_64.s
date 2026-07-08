	.file	"scale_store.c"
	.text
	.globl	scale_store                     # -- Begin function scale_store
	.type	scale_store,@function
scale_store:                            # @scale_store
# %bb.0:
	movl	%edx, %eax
	xorl	%ecx, %ecx
	testl	%edx, %edx
	cmovlel	%ecx, %eax
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rcx, %rax
	je	.LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	movl	(%rsi,%rcx,4), %edx
	leal	1(,%rdx,4), %edx
	movl	%edx, (%rdi,%rcx,4)
	incq	%rcx
	jmp	.LBB0_1
.LBB0_3:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end0:
	.size	scale_store, .Lfunc_end0-scale_store
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
