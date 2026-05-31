#include "all.h"

static Ins *
defins(Fn *fn, Ref r, Ins **defs)
{
	if (rtype(r) != RTmp || r.val >= (uint)fn->ntmp)
		return 0;
	return defs[r.val];
}

static int
bitscon(Fn *fn, Ref r, int64_t *out)
{
	if (rtype(r) != RCon || fn->con[r.val].type != CBits)
		return 0;
	*out = fn->con[r.val].bits.i;
	return 1;
}

static int
addrcon(Fn *fn, Ref r)
{
	return rtype(r) == RCon && fn->con[r.val].type == CAddr;
}

static int
ptrref(Fn *fn, Ref r)
{
	return (rtype(r) == RTmp && fn->tmp[r.val].isptr) || addrcon(fn, r);
}

static int
scaleval(int64_t n)
{
	return n == 1 || n == 2 || n == 4 || n == 8;
}

static int
matchindexbase(Fn *fn, Ref r, Ins **defs, Ref *index, int64_t *offset)
{
	Ins *i;
	int64_t n;

	i = defins(fn, r, defs);
	if (i && i->op == Oadd && KBASE(i->cls) == 0) {
		if (bitscon(fn, i->arg[0], &n)
		&& rtype(i->arg[1]) == RTmp && !fn->tmp[i->arg[1].val].isptr) {
			*index = i->arg[1];
			*offset = n;
			return 1;
		}
		if (bitscon(fn, i->arg[1], &n)
		&& rtype(i->arg[0]) == RTmp && !fn->tmp[i->arg[0].val].isptr) {
			*index = i->arg[0];
			*offset = n;
			return 1;
		}
	}
	if (rtype(r) == RTmp && !fn->tmp[r.val].isptr) {
		*index = r;
		*offset = 0;
		return 1;
	}
	return 0;
}

static int
matchindexref(Fn *fn, Ref r, Ins **defs, Ref *index, int *index_s32, int64_t *offset)
{
	Ins *i;

	i = defins(fn, r, defs);
	if (i && i->op == Oextsw && i->cls == Kl
	&& matchindexbase(fn, i->arg[0], defs, index, offset)) {
		*index_s32 = 1;
		return 1;
	}
	if (matchindexbase(fn, r, defs, index, offset)) {
		*index_s32 = 0;
		return 1;
	}
	return 0;
}

static int
matchindex(Fn *fn, Ref r, Ins **defs, Ref *index, int *scale, int *index_s32, int64_t *offset)
{
	Ins *i;
	int64_t n;
	int64_t addend;

	i = defins(fn, r, defs);
	if (i && i->op == Omul && KBASE(i->cls) == 0) {
		if (bitscon(fn, i->arg[0], &n) && scaleval(n)
		&& matchindexref(fn, i->arg[1], defs, index, index_s32, &addend)) {
			*scale = (int)n;
			*offset = addend * n;
			return 1;
		}
		if (bitscon(fn, i->arg[1], &n) && scaleval(n)
		&& matchindexref(fn, i->arg[0], defs, index, index_s32, &addend)) {
			*scale = (int)n;
			*offset = addend * n;
			return 1;
		}
	}
	if (i && i->op == Oshl && KBASE(i->cls) == 0
	&& bitscon(fn, i->arg[1], &n) && 0 <= n && n <= 3
	&& matchindexref(fn, i->arg[0], defs, index, index_s32, &addend)) {
		*scale = 1 << (int)n;
		*offset = addend << (int)n;
		return 1;
	}
	if (matchindexref(fn, r, defs, index, index_s32, &addend)) {
		*scale = 1;
		*offset = addend;
		return 1;
	}
	return 0;
}

static int
matchaddr(Fn *fn, Ref r, Ins **defs, Addr *addr)
{
	Ins *i;
	Ref lhs, rhs, base, index;
	int64_t offset;
	int scale;
	int index_s32;
	int lhs_ptr, rhs_ptr;

	if (rtype(r) != RTmp || !fn->tmp[r.val].isptr)
		return 0;
	i = defins(fn, r, defs);
	if (!i || i->op != Oadd || !i->ptr)
		return 0;
	lhs = i->arg[0];
	rhs = i->arg[1];
	lhs_ptr = ptrref(fn, lhs);
	rhs_ptr = ptrref(fn, rhs);
	if (lhs_ptr == rhs_ptr)
		return 0;
	base = lhs_ptr ? lhs : rhs;
	if (bitscon(fn, lhs_ptr ? rhs : lhs, &offset)) {
		index = R;
		scale = 0;
		index_s32 = 0;
	} else if (!matchindex(fn, lhs_ptr ? rhs : lhs, defs, &index, &scale, &index_s32, &offset)) {
		return 0;
	}
	memset(addr, 0, sizeof *addr);
	addr->offset.type = CBits;
	addr->offset.bits.i = offset;
	addr->base = base;
	addr->index = index;
	addr->scale = scale;
	addr->index_s32 = index_s32;
	return 1;
}

static void
seladdr(Ref *pr, Fn *fn, Ins **defs)
{
	Addr addr;
	Ref r;

	r = *pr;
	if (!matchaddr(fn, r, defs, &addr))
		return;
	chuse(r, -1, fn);
	chuse(addr.base, +1, fn);
	chuse(addr.index, +1, fn);
	vgrow(&fn->mem, ++fn->nmem);
	fn->mem[fn->nmem-1] = addr;
	*pr = MEM(fn->nmem-1);
}

static int
pow2shift(int64_t n)
{
	int shift;

	if (n <= 0 || (n & (n - 1)) != 0)
		return -1;
	for (shift=0; n > 1; shift++)
		n >>= 1;
	return shift;
}

static void
foldpow2mul(Ins *i, Fn *fn)
{
	int64_t n;
	int shift;
	Ref value;

	if (i->op != Omul || KBASE(i->cls) != 0)
		return;
	if (bitscon(fn, i->arg[0], &n))
		value = i->arg[1];
	else if (bitscon(fn, i->arg[1], &n))
		value = i->arg[0];
	else
		return;
	shift = pow2shift(n);
	if (shift < 0)
		return;
	if (shift == 0) {
		i->op = Ocopy;
		i->arg[0] = value;
		i->arg[1] = R;
		return;
	}
	i->op = Oshl;
	i->arg[0] = value;
	i->arg[1] = getcon(shift, fn);
}

static int
exactptrdiff(Fn *fn, Ref r, Ins **defs)
{
	Ins *i;

	i = defins(fn, r, defs);
	return i && i->op == Osub && ptrref(fn, i->arg[0]) && ptrref(fn, i->arg[1]);
}

static void
foldexactpow2div(Ins *i, Fn *fn, Ins **defs)
{
	int64_t n;
	int shift;

	if ((i->op != Odiv && i->op != Oudiv) || KBASE(i->cls) != 0)
		return;
	if (!bitscon(fn, i->arg[1], &n))
		return;
	shift = pow2shift(n);
	if (shift < 0 || !exactptrdiff(fn, i->arg[0], defs))
		return;
	if (shift == 0) {
		i->op = Ocopy;
		i->arg[1] = R;
		return;
	}
	i->op = i->op == Oudiv ? Oshr : Osar;
	i->arg[1] = getcon(shift, fn);
}

static int
keepiconst(Ins *i, int arg)
{
	if (KBASE(i->cls) != 0 || rtype(i->arg[arg]) != RCon)
		return 0;
	switch (i->op) {
	case Oadd:
	case Osub:
	case Oand:
	case Oor:
	case Oxor:
	case Omul:
	case Odiv:
	case Orem:
	case Oudiv:
	case Ourem:
	case Oshl:
	case Oshr:
	case Osar:
		return 1;
	default:
		return 0;
	}
}

static void
fixarg(Ref *pr, int k, int phi, Fn *fn)
{
	char buf[32];
	Ref r0, r1, r2;
	Con *c;
	int s, n;

	r0 = *pr;
	switch (rtype(r0)) {
	case RCon:
		if (KBASE(k) == 0 && phi)
			return;
		r1 = newtmp("isel", k, fn);
		if (KBASE(k) == 0) {
			emit(Ocopy, k, r1, r0, R);
		} else {
			c = &fn->con[r0.val];
			n = gasstash(&c->bits, KWIDE(k) ? 8 : 4);
			vgrow(&fn->con, ++fn->ncon);
			c = &fn->con[fn->ncon-1];
			sprintf(buf, "fp%d", n);
			*c = (Con){.type = CAddr, .local = 1};
			c->label = intern(buf);
			r2 = newtmp("isel", Kl, fn);
			fn->tmp[r2.val].isptr = 1;
			emit(Oload, k, r1, r2, R);
			emit(Ocopy, Kl, r2, CON(c-fn->con), R);
			curi->ptr = 1;
		}
		*pr = r1;
		break;
	case RTmp:
		s = fn->tmp[r0.val].slot;
		if (s == -1)
			break;
		r1 = newtmp("isel", Kl, fn);
		fn->tmp[r1.val].isptr = 1;
		emit(Oaddr, Kl, r1, SLOT(s), R);
		curi->ptr = 1;
		*pr = r1;
		break;
	}
}

static void
setregprefs(Fn *fn)
{
	int t, r;
	bits dregs, aregs;
	Tmp *tmp;

	dregs = 0;
	aregs = 0;
	for (r=D0; r<=D7; r++)
		dregs |= BIT(r);
	for (r=A0; r<=A6; r++)
		aregs |= BIT(r);
	for (t=Tmp0; t<fn->ntmp; t++) {
		tmp = &fn->tmp[t];
		if (KBASE(tmp->cls) == 0)
			tmp->hint.m |= tmp->isptr ? dregs : aregs;
	}
}

static int
markptr(Fn *fn, Ref r)
{
	if (rtype(r) != RTmp || r.val >= (uint)fn->ntmp || fn->tmp[r.val].isptr)
		return 0;
	fn->tmp[r.val].isptr = 1;
	return 1;
}

static void
inferptrprefs(Fn *fn)
{
	Blk *b;
	Ins *i;
	Phi *p;
	int changed;
	uint n;

	do {
		changed = 0;
		for (b=fn->start; b; b=b->link) {
			for (p=b->phi; p; p=p->link) {
				if (rtype(p->to) == RTmp && fn->tmp[p->to.val].isptr) {
					p->ptr = 1;
					for (n=0; n<p->narg; n++)
						changed |= markptr(fn, p->arg[n]);
				}
				for (n=0; n<p->narg; n++)
					if (rtype(p->arg[n]) == RTmp && fn->tmp[p->arg[n].val].isptr) {
						p->ptr = 1;
						changed |= markptr(fn, p->to);
					}
			}
			for (i=b->ins; i!=&b->ins[b->nins]; i++) {
				if (isload(i->op))
					changed |= markptr(fn, i->arg[0]);
				if (isstore(i->op))
					changed |= markptr(fn, i->arg[1]);
				if (i->op == Ocopy) {
					if (rtype(i->arg[0]) == RTmp && fn->tmp[i->arg[0].val].isptr) {
						i->ptr = 1;
						changed |= markptr(fn, i->to);
					}
					if (rtype(i->to) == RTmp && fn->tmp[i->to.val].isptr)
						changed |= markptr(fn, i->arg[0]);
				}
				if (i->op == Oaddr) {
					i->ptr = 1;
					changed |= markptr(fn, i->to);
				}
				if (i->op == Oadd && i->cls == Kl) {
					if (i->ptr)
						changed |= markptr(fn, i->to);
					if (rtype(i->to) == RTmp && fn->tmp[i->to.val].isptr) {
						i->ptr = 1;
						if (rtype(i->arg[0]) == RTmp && rtype(i->arg[1]) == RCon
						&& fn->con[i->arg[1].val].type == CBits)
							changed |= markptr(fn, i->arg[0]);
						if (rtype(i->arg[1]) == RTmp && rtype(i->arg[0]) == RCon
						&& fn->con[i->arg[0].val].type == CBits)
							changed |= markptr(fn, i->arg[1]);
					}
				}
			}
		}
	} while (changed);
}

static int
selcmp(Ref arg[2], int k, Fn *fn)
{
	Ref r, *iarg;
	int64_t val;
	int swap;

	if (KBASE(k) == 1) {
		emit(Oafcmp, k, R, arg[0], arg[1]);
		iarg = curi->arg;
		fixarg(&iarg[0], k, 0, fn);
		fixarg(&iarg[1], k, 0, fn);
		return 0;
	}

	swap = rtype(arg[0]) == RCon;
	if (swap) {
		r = arg[1];
		arg[1] = arg[0];
		arg[0] = r;
	}
	emit(Oacmp, k, R, arg[0], arg[1]);
	iarg = curi->arg;
	fixarg(&iarg[0], k, 0, fn);
	if (!bitscon(fn, iarg[1], &val) || val != 0)
		fixarg(&iarg[1], k, 0, fn);
	return swap;
}

static void
sel(Ins i, Fn *fn, Ins **defs)
{
	Ref *iarg;
	Ins *i0;
	int ck, cc;

	if (rtype(i.to) == RTmp)
	if (!isreg(i.to) && !isreg(i.arg[0]) && !isreg(i.arg[1]))
	if (fn->tmp[i.to.val].nuse == 0) {
		chuse(i.arg[0], -1, fn);
		chuse(i.arg[1], -1, fn);
		return;
	}

	if (iscmp(i.op, &ck, &cc)) {
		emit(Oflag, i.cls, i.to, R, R);
		i0 = curi;
		if (selcmp(i.arg, ck, fn))
			i0->op += cmpop(cc);
		else
			i0->op += cc;
	} else if (i.op != Onop) {
		if (isload(i.op))
			seladdr(&i.arg[0], fn, defs);
		else if (isstore(i.op))
			seladdr(&i.arg[1], fn, defs);
		foldpow2mul(&i, fn);
		foldexactpow2div(&i, fn, defs);
		emiti(i);
		iarg = curi->arg;
		if (i.op != Ocall && !keepiconst(&i, 0))
			fixarg(&iarg[0], argcls(&i, 0), 0, fn);
		if (!keepiconst(&i, 1))
			fixarg(&iarg[1], argcls(&i, 1), 0, fn);
	}
}

static void
seljmp(Blk *b, Fn *fn)
{
	Ref r;
	Ins *i, *ir;
	int ck, cc, use;

	switch (b->jmp.type) {
	default:
		assert(0 && "TODO jump");
		break;
	case Jret0:
	case Jjmp:
		return;
	case Jjnz:
		break;
	}

	r = b->jmp.arg;
	use = -1;
	b->jmp.arg = R;
	ir = 0;
	i = &b->ins[b->nins];
	while (i > b->ins)
		if (req((--i)->to, r)) {
			use = fn->tmp[r.val].nuse;
			ir = i;
			break;
		}
	if (ir && use == 1
	&& iscmp(ir->op, &ck, &cc)) {
		if (selcmp(ir->arg, ck, fn))
			cc = cmpop(cc);
		b->jmp.type = Jjf + cc;
		*ir = (Ins){.op = Onop};
	}
	else {
		selcmp((Ref[]){r, CON_Z}, Kw, fn);
		b->jmp.type = Jjfine;
	}
}

void
bedrock_isel(Fn *fn)
{
	Blk *b, **sb;
	Ins *i;
	Ins **defs;
	Phi *p;
	uint n, al;
	int64_t sz;

	b = fn->start;
	for (al=Oalloc, n=4; al<=Oalloc1; al++, n*=2)
		for (i=b->ins; i-b->ins < b->nins; i++)
			if (i->op == al) {
				if (rtype(i->arg[0]) != RCon)
					break;
				sz = fn->con[i->arg[0].val].bits.i;
				if (sz < 0 || sz >= INT_MAX-15)
					err("invalid alloc size %"PRId64, sz);
				sz = (sz + n-1) & -n;
				sz /= 4;
				fn->tmp[i->to.val].slot = fn->slot;
				fn->slot += sz;
				*i = (Ins){.op = Onop};
			}

	defs = emalloc(fn->ntmp * sizeof defs[0]);
	for (b=fn->start; b; b=b->link) {
		curi = &insb[NIns];
		for (sb=(Blk*[3]){b->s1, b->s2, 0}; *sb; sb++)
			for (p=(*sb)->phi; p; p=p->link) {
				for (n=0; p->blk[n] != b; n++)
					assert(n+1 < p->narg);
				fixarg(&p->arg[n], p->cls, 1, fn);
			}
		memset(defs, 0, fn->ntmp * sizeof defs[0]);
		for (i=b->ins; i-b->ins < b->nins; i++)
			if (rtype(i->to) == RTmp)
				defs[i->to.val] = i;
		seljmp(b, fn);
		for (i=&b->ins[b->nins]; i!=b->ins;)
			sel(*--i, fn, defs);
		b->nins = &insb[NIns] - curi;
		idup(&b->ins, curi, b->nins);
	}
	free(defs);

	inferptrprefs(fn);
	setregprefs(fn);

	if (debug['I']) {
		fprintf(stderr, "\n> After instruction selection:\n");
		printfn(fn, stderr);
	}
}
