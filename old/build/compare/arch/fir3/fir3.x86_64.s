	.file	"fir3.c"
	.text
	.globl	fir_three                       # -- Begin function fir_three
	.type	fir_three,@function
fir_three:                              # @fir_three
# %bb.0:
	movl	%edx, %eax
	xorl	%edx, %edx
	testl	%eax, %eax
	cmovlel	%edx, %eax
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rdx, %rax
	je	.LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	movl	(%rsi,%rdx,4), %r10d
	imull	%ecx, %r10d
	movl	4(%rsi,%rdx,4), %r11d
	imull	%r8d, %r11d
	addl	%r10d, %r11d
	movl	8(%rsi,%rdx,4), %r10d
	imull	%r9d, %r10d
	addl	%r11d, %r10d
	movl	%r10d, (%rdi,%rdx,4)
	incq	%rdx
	jmp	.LBB0_1
.LBB0_3:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end0:
	.size	fir_three, .Lfunc_end0-fir_three
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
