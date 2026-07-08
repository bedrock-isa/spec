	.file	"pointer_integer_mix.c"
	.text
	.globl	pointer_integer_mix             # -- Begin function pointer_integer_mix
	.type	pointer_integer_mix,@function
pointer_integer_mix:                    # @pointer_integer_mix
# %bb.0:
	movq	%rcx, %rax
	movslq	%edx, %rcx
	leaq	(%rdi,%rcx,4), %r8
	pushq	$4
	popq	%r9
	cqto
	idivq	%r9
	leaq	(%rdi,%rax,4), %rdx
	subq	%rdi, %rsi
	sarq	$2, %rsi
	xorl	%eax, %eax
	testl	%ecx, %ecx
	cmovlel	%eax, %ecx
	xorl	%edi, %edi
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%rdi, %rcx
	je	.LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	xorl	%r9d, %r9d
	cmpq	%rdi, %rsi
	setl	%r9b
	addl	%r9d, %eax
	addl	(%r8,%rdi,4), %eax
	addl	(%rdx,%rdi,4), %eax
	incq	%rdi
	jmp	.LBB0_1
.LBB0_3:
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end0:
	.size	pointer_integer_mix, .Lfunc_end0-pointer_integer_mix
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
