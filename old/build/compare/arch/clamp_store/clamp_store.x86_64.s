	.file	"clamp_store.c"
	.text
	.globl	clamp_store                     # -- Begin function clamp_store
	.type	clamp_store,@function
clamp_store:                            # @clamp_store
# %bb.0:
	movl	%edx, %eax
	xorl	%edx, %edx
	testl	%eax, %eax
	cmovlel	%edx, %eax
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rdx, %rax
	je	.LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	movl	(%rsi,%rdx,4), %r9d
	cmpl	%ecx, %r9d
	cmovlel	%ecx, %r9d
	cmpl	%r8d, %r9d
	cmovgel	%r8d, %r9d
	movl	%r9d, (%rdi,%rdx,4)
	incq	%rdx
	jmp	.LBB0_1
.LBB0_3:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end0:
	.size	clamp_store, .Lfunc_end0-clamp_store
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
