	.file	"call_heavy.c"
	.text
	.globl	call_heavy                      # -- Begin function call_heavy
	.type	call_heavy,@function
call_heavy:                             # @call_heavy
# %bb.0:
	pushq	%rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	pushq	%rax
	movl	%esi, %ebx
	movq	%rdi, %r14
	xorl	%eax, %eax
	testl	%esi, %esi
	cmovlel	%eax, %ebx
	xorl	%r15d, %r15d
	xorl	%eax, %eax
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%r15, %rbx
	je	.LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	movl	(%r14,%r15,4), %ebp
	movl	%eax, %edi
	movl	%ebp, %esi
	xorl	%eax, %eax
	callq	ext_add@PLT
	movl	%eax, %edi
	movl	%r15d, %esi
	xorl	%eax, %eax
	callq	ext_mix@PLT
	addl	%r15d, %ebp
	movl	%eax, %edi
	movl	%ebp, %esi
	xorl	%eax, %eax
	callq	ext_fold@PLT
	incq	%r15
	jmp	.LBB0_1
.LBB0_3:
	addq	$8, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	retq
.Lfunc_end0:
	.size	call_heavy, .Lfunc_end0-call_heavy
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
