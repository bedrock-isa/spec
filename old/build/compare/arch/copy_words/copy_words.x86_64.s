	.file	"copy_words.c"
	.text
	.globl	copy_words                      # -- Begin function copy_words
	.type	copy_words,@function
copy_words:                             # @copy_words
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
	movl	%edx, (%rdi,%rcx,4)
	incq	%rcx
	jmp	.LBB0_1
.LBB0_3:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end0:
	.size	copy_words, .Lfunc_end0-copy_words
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
