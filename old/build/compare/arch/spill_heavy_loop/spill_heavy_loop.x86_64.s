	.file	"spill_heavy_loop.c"
	.text
	.globl	spill_heavy_loop                # -- Begin function spill_heavy_loop
	.type	spill_heavy_loop,@function
spill_heavy_loop:                       # @spill_heavy_loop
# %bb.0:
	pushq	%rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
                                        # kill: def $r8d killed $r8d def $r8
	xorl	%r14d, %r14d
	testl	%r8d, %r8d
	cmovlel	%r14d, %r8d
	movl	$8, %r9d
	movl	$7, %r10d
	movl	$6, %ebx
	movl	$5, %eax
	movl	$4, %r15d
	movl	$3, %r11d
	movl	$2, %ebp
	movl	$1, %r12d
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmpl	%r14d, %r8d
	je	.LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	addl	(%rdi,%r14,4), %r12d
	addl	(%rsi,%r14,4), %ebp
	addl	%r12d, %ebp
	addl	(%rdx,%r14,4), %r11d
	addl	%ebp, %r11d
	addl	(%rcx,%r14,4), %r15d
	addl	%r11d, %r15d
	addl	%r12d, %eax
	addl	%r15d, %eax
	addl	%ebp, %ebx
	addl	%eax, %ebx
	addl	%r11d, %r10d
	addl	%ebx, %r10d
	addl	%r15d, %r9d
	addl	%r10d, %r9d
	incq	%r14
	jmp	.LBB0_1
.LBB0_3:
	addl	%r12d, %ebp
	addl	%r15d, %r11d
	addl	%ebp, %r11d
	addl	%ebx, %eax
	addl	%r10d, %eax
	addl	%r11d, %eax
	addl	%r9d, %eax
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	retq
.Lfunc_end0:
	.size	spill_heavy_loop, .Lfunc_end0-spill_heavy_loop
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
