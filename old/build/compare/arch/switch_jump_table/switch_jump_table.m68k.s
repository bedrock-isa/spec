#NO_APP
	.file	"switch_jump_table.c"
	.text
	.align	2
	.globl	switch_jump_table
	.type	switch_jump_table, @function
switch_jump_table:
	move.l 8(%sp),%a0
	moveq #7,%d0
	and.l 4(%sp),%d0
	moveq #6,%d1
	cmp.l %d0,%d1
	jcs .L2
	move.w .L4(%pc,%d0.l*2),%d0
	jmp %pc@(2,%d0:w)
	.balignw 2,0x284c
	.swbeg	&7
.L4:
	.word .L10-.L4
	.word .L9-.L4
	.word .L8-.L4
	.word .L7-.L4
	.word .L6-.L4
	.word .L5-.L4
	.word .L3-.L4
.L10:
	addq.l #3,%a0
.L1:
	move.l %a0,%d0
	rts
.L9:
	addq.l #5,%a0
	jra .L1
.L8:
	addq.l #7,%a0
	jra .L1
.L7:
	lea (11,%a0),%a0
	jra .L1
.L6:
	lea (13,%a0),%a0
	jra .L1
.L5:
	lea (17,%a0),%a0
	jra .L1
.L3:
	lea (19,%a0),%a0
	jra .L1
.L2:
	lea (23,%a0),%a0
	jra .L1
	.size	switch_jump_table, .-switch_jump_table
	.ident	"GCC: (GNU) 16.1.0"
