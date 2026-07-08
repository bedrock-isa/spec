	.file	"switch_jump_table.c"
	.text
	.globl	switch_jump_table               // -- Begin function switch_jump_table
	.p2align	2
	.type	switch_jump_table,@function
switch_jump_table:                      // @switch_jump_table
// %bb.0:
	and	w8, w0, #0x7
	adrp	x9, .Lswitch.table.switch_jump_table
	add	x9, x9, :lo12:.Lswitch.table.switch_jump_table
	ldr	w8, [x9, w8, uxtw #2]
	add	w0, w1, w8
	ret
.Lfunc_end0:
	.size	switch_jump_table, .Lfunc_end0-switch_jump_table
                                        // -- End function
	.type	.Lswitch.table.switch_jump_table,@object // @switch.table.switch_jump_table
	.section	.rodata.cst32,"aM",@progbits,32
	.p2align	2, 0x0
.Lswitch.table.switch_jump_table:
	.word	3                               // 0x3
	.word	5                               // 0x5
	.word	7                               // 0x7
	.word	11                              // 0xb
	.word	13                              // 0xd
	.word	17                              // 0x11
	.word	19                              // 0x13
	.word	23                              // 0x17
	.size	.Lswitch.table.switch_jump_table, 32

	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
