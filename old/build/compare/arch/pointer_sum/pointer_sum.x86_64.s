	.file	"pointer_sum.c"
	.text
	.globl	sum                             # -- Begin function sum
	.type	sum,@function
sum:                                    # @sum
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
	.size	sum, .Lfunc_end0-sum
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
