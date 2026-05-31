#include "all.h"

static int gpreg[] = {D0, D1, D2, D3, D4, D5};
static int apreg[] = {A0, A1, A2, A3, A4, A5};
static int fpreg[] = {F0, F1, F2, F3, F4, F5, F6};

bits
bedrock_retregs(Ref r, int p[2])
{
	bits b;
	int ngp, nap, nfp;

	assert(rtype(r) == RCall);
	ngp = r.val & 1;
	nap = (r.val >> 1) & 1;
	nfp = (r.val >> 2) & 1;
	if (p) {
		p[0] = ngp + nap;
		p[1] = nfp;
	}
	b = 0;
	if (ngp)
		b |= BIT(D0);
	if (nap)
		b |= BIT(A0);
	if (nfp)
		b |= BIT(F0);
	return b;
}

bits
bedrock_argregs(Ref r, int p[2])
{
	bits b;
	int ngp, nap, nfp;

	assert(rtype(r) == RCall);
	ngp = (r.val >> 5) & 15;
	nfp = (r.val >> 9) & 15;
	nap = (r.val >> 13) & 15;
	if (p) {
		p[0] = ngp + nap;
		p[1] = nfp;
	}
	b = 0;
	while (ngp--)
		b |= BIT(D0+ngp);
	while (nap--)
		b |= BIT(A0+nap);
	while (nfp--)
		b |= BIT(F0+nfp);
	return b;
}

static void
selret(Blk *b, Fn *fn)
{
	int j, k, cty;
	Ref r;

	j = b->jmp.type;
	if (!isret(j) || j == Jret0)
		return;

	r = b->jmp.arg;
	b->jmp.type = Jret0;
	k = j - Jretw;
	if (KBASE(k) == 0) {
		if (fn->retptr) {
			emit(Ocopy, k, TMP(A0), r, R);
			curi->ptr = 1;
			cty = 2;
		} else {
			emit(Ocopy, k, TMP(D0), r, R);
			cty = 1;
		}
	} else {
		emit(Ocopy, k, TMP(F0), r, R);
		cty = 1 << 2;
	}
	b->jmp.arg = CALL(cty);
}

static void
selcall(Ins *i0, Ins *i1)
{
	Ins *i;
	int ngp, nap, nfp, cty, k;

	ngp = 0;
	nap = 0;
	nfp = 0;
	for (i=i0; i<i1; i++) {
		if (i->op == Oargc)
			die("bedrock abi: aggregate call arguments are not lowered yet");
		if (i->op == Oarge)
			die("bedrock abi: environment calls are not lowered yet");
		if (i->ptr) {
			if (nap == (int)(sizeof apreg / sizeof apreg[0]))
				die("bedrock abi: stack pointer call arguments are not lowered yet");
			nap++;
		} else if (KBASE(i->cls) == 0) {
			if (ngp == (int)(sizeof gpreg / sizeof gpreg[0]))
				die("bedrock abi: stack call arguments are not lowered yet");
			ngp++;
		} else {
			if (nfp == (int)(sizeof fpreg / sizeof fpreg[0]))
				die("bedrock abi: stack floating-point call arguments are not lowered yet");
			nfp++;
		}
	}

	cty = (ngp << 5) | (nfp << 9) | (nap << 13);
	if (!req(i1->arg[1], R))
		die("bedrock abi: aggregate return values are not lowered yet");
	if (!req(i1->to, R)) {
		k = i1->cls;
		if (i1->ptr) {
			emit(Ocopy, k, i1->to, TMP(A0), R);
			curi->ptr = 1;
			cty |= 2;
		} else if (KBASE(k) == 0) {
			emit(Ocopy, k, i1->to, TMP(D0), R);
			cty |= 1;
		} else {
			emit(Ocopy, k, i1->to, TMP(F0), R);
			cty |= 1 << 2;
		}
	}

	emit(Ocall, 0, R, i1->arg[0], CALL(cty));

	ngp = 0;
	nap = 0;
	nfp = 0;
	for (i=i0; i<i1; i++) {
		if (i->ptr) {
			emit(Ocopy, i->cls, TMP(apreg[nap++]), i->arg[0], R);
			curi->ptr = 1;
		} else if (KBASE(i->cls) == 0)
			emit(Ocopy, i->cls, TMP(gpreg[ngp++]), i->arg[0], R);
		else
			emit(Ocopy, i->cls, TMP(fpreg[nfp++]), i->arg[0], R);
	}
}

static void
selpar(Fn *fn, Ins *i0, Ins *i1)
{
	Ins *i;
	int ngp, nap, nfp;

	ngp = 0;
	nap = 0;
	nfp = 0;
	curi = &insb[NIns];
	for (i=i0; i<i1; i++) {
		if (i->op == Oparc)
			die("bedrock abi: aggregate parameters are not lowered yet");
		if (i->op == Opare)
			die("bedrock abi: environment parameters are not lowered yet");
		if (i->ptr) {
			if (nap == (int)(sizeof apreg / sizeof apreg[0]))
				die("bedrock abi: stack pointer parameters are not lowered yet");
			emit(Ocopy, i->cls, i->to, TMP(apreg[nap++]), R);
			curi->ptr = 1;
		} else if (KBASE(i->cls) == 0) {
			if (ngp == (int)(sizeof gpreg / sizeof gpreg[0]))
				die("bedrock abi: stack parameters are not lowered yet");
			emit(Ocopy, i->cls, i->to, TMP(gpreg[ngp++]), R);
		} else {
			if (nfp == (int)(sizeof fpreg / sizeof fpreg[0]))
				die("bedrock abi: stack floating-point parameters are not lowered yet");
			emit(Ocopy, i->cls, i->to, TMP(fpreg[nfp++]), R);
		}
	}
	(void)fn;
}

void
bedrock_abi(Fn *fn)
{
	Blk *b;
	Ins *i, *i0, *ip;
	uint n;

	for (b=fn->start, i=b->ins; i-b->ins<b->nins; i++)
		if (!ispar(i->op))
			break;
	selpar(fn, b->ins, i);
	n = b->nins - (i - b->ins) + (&insb[NIns] - curi);
	i0 = alloc(n * sizeof(Ins));
	ip = icpy(ip = i0, curi, &insb[NIns] - curi);
	ip = icpy(ip, i, &b->ins[b->nins] - i);
	b->nins = n;
	b->ins = i0;

	for (b=fn->start; b; b=b->link)
		b->visit = 0;

	b = fn->start;
	do {
		if (!(b = b->link))
			b = fn->start;
		if (b->visit)
			continue;
		b->visit = 1;
		curi = &insb[NIns];
		selret(b, fn);
		for (i=&b->ins[b->nins]; i!=b->ins;)
			switch ((--i)->op) {
			default:
				emiti(*i);
				break;
			case Ocall:
			case Ovacall:
				if (i->op == Ovacall)
					die("bedrock abi: variadic calls are not lowered yet");
				for (i0=i; i0>b->ins; i0--)
					if (!isarg((i0-1)->op))
						break;
				selcall(i0, i);
				i = i0;
				break;
			case Ovastart:
			case Ovaarg:
				die("bedrock abi: variadic functions are not lowered yet");
			case Oarg:
			case Oargc:
			case Oarge:
				die("unreachable");
			}
		b->nins = &insb[NIns] - curi;
		idup(&b->ins, curi, b->nins);
	} while (b != fn->start);

	for (b=fn->start; b; b=b->link)
		b->visit = 0;

	if (debug['A']) {
		fprintf(stderr, "\n> After ABI lowering:\n");
		printfn(fn, stderr);
	}
}
