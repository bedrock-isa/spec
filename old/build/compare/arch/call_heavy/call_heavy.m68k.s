#NO_APP
	.file	"call_heavy.c"
	.text
	.align	2
	.globl	call_heavy
	.type	call_heavy, @function
call_heavy:
	movem.l #62,-(%sp)
	move.l 24(%sp),%a3
	clr.l %d0
	sub.l %a2,%a2
	lea ext_mix,%a6
.L2:
	cmp.l 28(%sp),%a2
	jlt .L3
	movem.l (%sp)+,#31744
	rts
.L3:
	move.l (%a3)+,%a4
	move.l %a4,-(%sp)
	move.l %d0,-(%sp)
	jsr ext_add
	move.l %a2,-(%sp)
	move.l %d0,-(%sp)
	jsr (%a6)
	pea (%a2,%a4.l)
	move.l %d0,-(%sp)
	jsr ext_fold
	addq.l #1,%a2
	lea (24,%sp),%sp
	jra .L2
	.size	call_heavy, .-call_heavy
	.ident	"GCC: (GNU) 16.1.0"
