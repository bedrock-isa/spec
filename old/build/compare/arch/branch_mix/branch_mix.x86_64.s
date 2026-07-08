	.file	"branch_mix.c"
	.text
	.globl	branch_mix                      # -- Begin function branch_mix
	.type	branch_mix,@function
branch_mix:                             # @branch_mix
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
	movl	(%rdi,%rcx,4), %edx
	movl	%edx, %r8d
	negl	%r8d
	cmovsl	%edx, %r8d
	addl	%r8d, %eax
	incq	%rcx
	jmp	.LBB0_1
.LBB0_3:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end0:
	.size	branch_mix, .Lfunc_end0-branch_mix
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
