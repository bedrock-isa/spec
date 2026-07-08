	.file	"switch_jump_table.c"
	.text
	.globl	switch_jump_table               # -- Begin function switch_jump_table
	.type	switch_jump_table,@function
switch_jump_table:                      # @switch_jump_table
# %bb.0:
	movl	%esi, %eax
                                        # kill: def $edi killed $edi def $rdi
	andl	$7, %edi
	leaq	.Lswitch.table.switch_jump_table(%rip), %rcx
	addl	(%rcx,%rdi,4), %eax
	retq
.Lfunc_end0:
	.size	switch_jump_table, .Lfunc_end0-switch_jump_table
                                        # -- End function
	.type	.Lswitch.table.switch_jump_table,@object # @switch.table.switch_jump_table
	.section	.rodata.cst32,"aM",@progbits,32
	.p2align	2, 0x0
.Lswitch.table.switch_jump_table:
	.long	3                               # 0x3
	.long	5                               # 0x5
	.long	7                               # 0x7
	.long	11                              # 0xb
	.long	13                              # 0xd
	.long	17                              # 0x11
	.long	19                              # 0x13
	.long	23                              # 0x17
	.size	.Lswitch.table.switch_jump_table, 32

	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
