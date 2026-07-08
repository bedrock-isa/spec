	.file	"call_heavy.c"
	.text
	.globl	call_heavy                      // -- Begin function call_heavy
	.p2align	2
	.type	call_heavy,@function
call_heavy:                             // @call_heavy
// %bb.0:
	stp	x29, x30, [sp, #-48]!           // 16-byte Folded Spill
	stp	x22, x21, [sp, #16]             // 16-byte Folded Spill
	bic	w22, w1, w1, asr #31
	mov	x29, sp
	stp	x20, x19, [sp, #32]             // 16-byte Folded Spill
	mov	x19, x0
	mov	x20, xzr
	mov	w0, wzr
.LBB0_1:                                // =>This Inner Loop Header: Depth=1
	cmp	x22, x20
	b.eq	.LBB0_3
// %bb.2:                               //   in Loop: Header=BB0_1 Depth=1
	ldr	w21, [x19, x20, lsl #2]
	mov	w1, w21
	bl	ext_add
	mov	w1, w20
	bl	ext_mix
	add	w1, w20, w21
	bl	ext_fold
	add	x20, x20, #1
	b	.LBB0_1
.LBB0_3:
	ldp	x20, x19, [sp, #32]             // 16-byte Folded Reload
	ldp	x22, x21, [sp, #16]             // 16-byte Folded Reload
	ldp	x29, x30, [sp], #48             // 16-byte Folded Reload
	ret
.Lfunc_end0:
	.size	call_heavy, .Lfunc_end0-call_heavy
                                        // -- End function
	.ident	"Homebrew clang version 22.1.0"
	.section	".note.GNU-stack","",@progbits
	.addrsig
