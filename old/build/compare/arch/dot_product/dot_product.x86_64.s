	.file	"dot_product.c"
	.text
	.globl	dot_product                     # -- Begin function dot_product
	.type	dot_product,@function
dot_product:                            # @dot_product
# %bb.0:
                                        # kill: def $edx killed $edx def $rdx
	xorl	%eax, %eax
	testl	%edx, %edx
	cmovlel	%eax, %edx
	xorl	%ecx, %ecx
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rcx, %rdx
	je	.LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	movl	(%rsi,%rcx,4), %r8d
	imull	(%rdi,%rcx,4), %r8d
	addl	%r8d, %eax
	incq	%rcx
	jmp	.LBB0_1
.LBB0_3:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end0:
	.size	dot_product, .Lfunc_end0-dot_product
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
