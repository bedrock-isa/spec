	.file	"scan_until_zero.c"
	.text
	.globl	scan_until_zero                 # -- Begin function scan_until_zero
	.type	scan_until_zero,@function
scan_until_zero:                        # @scan_until_zero
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
	.size	scan_until_zero, .Lfunc_end0-scan_until_zero
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
