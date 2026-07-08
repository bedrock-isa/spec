	.file	"register_pressure.c"
	.text
	.globl	register_pressure               # -- Begin function register_pressure
	.type	register_pressure,@function
register_pressure:                      # @register_pressure
# %bb.0:
	pushq	%rbp
	pushq	%rbx
                                        # kill: def $esi killed $esi def $rsi
	xorl	%r10d, %r10d
	testl	%esi, %esi
	cmovlel	%r10d, %esi
	movl	$8, %ecx
	movl	$7, %edx
	movl	$6, %r9d
	movl	$5, %eax
	movl	$4, %ebx
	movl	$3, %r8d
	movl	$2, %r11d
	movl	$1, %ebp
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmpl	%r10d, %esi
	je	.LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	addl	(%rdi,%r10,4), %ebp
	addl	%ebp, %r11d
	addl	%r11d, %r8d
	addl	%r8d, %ebx
	addl	%ebx, %eax
	addl	%eax, %r9d
	addl	%r9d, %edx
	addl	%edx, %ecx
	incq	%r10
	jmp	.LBB0_1
.LBB0_3:
	addl	%ebp, %r11d
	addl	%ebx, %r8d
	addl	%r11d, %r8d
	addl	%r9d, %eax
	addl	%edx, %eax
	addl	%r8d, %eax
	addl	%ecx, %eax
	popq	%rbx
	popq	%rbp
	retq
.Lfunc_end0:
	.size	register_pressure, .Lfunc_end0-register_pressure
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
