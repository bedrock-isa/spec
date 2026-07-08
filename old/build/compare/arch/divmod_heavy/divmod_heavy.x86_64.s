	.file	"divmod_heavy.c"
	.text
	.globl	divmod_heavy                    # -- Begin function divmod_heavy
	.type	divmod_heavy,@function
divmod_heavy:                           # @divmod_heavy
# %bb.0:
	movl	%edx, %ecx
                                        # kill: def $esi killed $esi def $rsi
	xorl	%r8d, %r8d
	testl	%esi, %esi
	cmovlel	%r8d, %esi
	xorl	%r9d, %r9d
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmpq	%r9, %rsi
	je	.LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	movl	(%rdi,%r9,4), %eax
	addl	%r9d, %eax
	cltd
	idivl	%ecx
                                        # kill: def $edx killed $edx def $rdx
                                        # kill: def $eax killed $eax def $rax
	leal	(%rax,%rax,2), %eax
	leal	(%rdx,%rdx,4), %edx
	addl	%edx, %r8d
	addl	%eax, %r8d
	incq	%r9
	jmp	.LBB0_1
.LBB0_3:
	movl	%r8d, %eax
	retq
.Lfunc_end0:
	.size	divmod_heavy, .Lfunc_end0-divmod_heavy
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
