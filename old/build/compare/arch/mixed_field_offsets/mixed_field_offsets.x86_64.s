	.file	"mixed_field_offsets.c"
	.text
	.globl	mixed_field_offsets             # -- Begin function mixed_field_offsets
	.type	mixed_field_offsets,@function
mixed_field_offsets:                    # @mixed_field_offsets
# %bb.0:
	movslq	4(%rdi), %rcx
	movl	%ecx, %r8d
	movslq	%edx, %rax
	addq	%rax, %rcx
	addq	16(%rsi), %rcx
	addl	%r8d, %eax
	addl	28(%rdi), %eax
	addq	%rcx, 40(%rsi)
	movl	%eax, 28(%rdi)
	addl	(%rdi), %eax
                                        # kill: def $eax killed $eax killed $rax
	retq
.Lfunc_end0:
	.size	mixed_field_offsets, .Lfunc_end0-mixed_field_offsets
                                        # -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
