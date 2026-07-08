	.attribute	4, 16
	.attribute	5, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
	.file	"switch_jump_table.c"
	.text
	.globl	switch_jump_table               # -- Begin function switch_jump_table
	.p2align	1
	.type	switch_jump_table,@function
switch_jump_table:                      # @switch_jump_table
# %bb.0:
	andi	a0, a0, 7
	slli	a0, a0, 2
	lui	a2, %hi(.Lswitch.table.switch_jump_table)
	addi	a2, a2, %lo(.Lswitch.table.switch_jump_table)
	add	a0, a0, a2
	lw	a0, 0(a0)
	addw	a0, a0, a1
	ret
.Lfunc_end0:
	.size	switch_jump_table, .Lfunc_end0-switch_jump_table
                                        # -- End function
	.type	.Lswitch.table.switch_jump_table,@object # @switch.table.switch_jump_table
	.section	.rodata.cst32,"aM",@progbits,32
	.p2align	2, 0x0
.Lswitch.table.switch_jump_table:
	.word	3                               # 0x3
	.word	5                               # 0x5
	.word	7                               # 0x7
	.word	11                              # 0xb
	.word	13                              # 0xd
	.word	17                              # 0x11
	.word	19                              # 0x13
	.word	23                              # 0x17
	.size	.Lswitch.table.switch_jump_table, 32

	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
