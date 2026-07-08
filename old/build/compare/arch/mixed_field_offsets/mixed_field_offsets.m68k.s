#NO_APP
	.file	"mixed_field_offsets.c"
	.text
	.align	2
	.globl	mixed_field_offsets
	.type	mixed_field_offsets, @function
mixed_field_offsets:
	subq.l #4,%sp
	move.l 8(%sp),%a0
	move.l 12(%sp),%a1
	move.l 4(%a0),%d0
	move.l 28(%a0),(%sp)
	move.l 8(%a1),%d1
	add.l 20(%a1),%d1
	add.l %d0,%d1
	add.l 16(%sp),%d1
	move.l %d1,20(%a1)
	add.l (%sp),%d0
	add.l 16(%sp),%d0
	move.l %d0,28(%a0)
	add.l (%a0),%d0
	addq.l #4,%sp
	rts
	.size	mixed_field_offsets, .-mixed_field_offsets
	.ident	"GCC: (GNU) 16.1.0"
