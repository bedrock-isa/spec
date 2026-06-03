#include "all.h"

typedef struct E E;
typedef struct FnRegRecord FnRegRecord;

struct FnRegRecord {
	char name[NString];
	bits regs;
};

struct E {
	FILE *f;
	Fn *fn;
	uint64_t frame;
	uint64_t padding;
	uint64_t save_size;
	int save_pad_reg;
	int has_call;
	int uses_ascratch;
	unsigned ins_call_fence_bitmap;
};

static FnRegRecord emitted_fns[1024];
static uint nemitted_fns;

static int isconval(Ref r, E *e, int64_t val);
static int postinc_size(Ins *i);
static Ins *findpostincadd(Ins *i, Ins *end, int reg, int size, E *e);
static int isindexedmemdisp(Ref r, Ref counter, int scale, int64_t disp, E *e, Ref *base);

#define CMP(X) \
	X(Cieq,       "EQ")  \
	X(Cine,       "NE")  \
	X(Cisge,      "GE")  \
	X(Cisgt,      "GT")  \
	X(Cisle,      "LE")  \
	X(Cislt,      "LT")  \
	X(Ciuge,      "UGE") \
	X(Ciugt,      "UGT") \
	X(Ciule,      "ULE") \
	X(Ciult,      "ULT") \
	X(NCmpI+Cfeq, "EQ")  \
	X(NCmpI+Cfge, "GE")  \
	X(NCmpI+Cfgt, "GT")  \
	X(NCmpI+Cfle, "LE")  \
	X(NCmpI+Cflt, "LT")  \
	X(NCmpI+Cfne, "NE")  \
	X(NCmpI+Cfo,  "VC")  \
	X(NCmpI+Cfuo, "VS")

static char *
rname(int r, int k)
{
	static char buf[8][8];
	static int n;
	char *b;

	b = buf[n++ & 7];
	if (D0 <= r && r <= D7) {
		(void)k;
		sprintf(b, "D%d", r-D0);
	} else if (A0 <= r && r <= A7) {
		(void)k;
		sprintf(b, "A%d", r-A0);
	} else if (r == SP) {
		(void)k;
		sprintf(b, "SP");
	} else if (F0 <= r && r <= F7) {
		(void)k;
		sprintf(b, "F%d", r-F0);
	} else
		die("invalid bedrock register %d", r);
	return b;
}

static char
siz(int k)
{
	switch (k) {
	default:
		die("invalid bedrock class");
	case Kw:
		return 'L';
	case Kl:
		return 'Q';
	case Ks:
		return 'S';
	case Kd:
		return 'D';
	}
}

static char
dstsiz(int k)
{
	return k == Kl ? 'Q' : 'L';
}

static int
slot_index(int s)
{
	struct { int i:29; } x;

	x.i = s;
	return x.i;
}

static uint64_t
slot(int s, E *e)
{
	int si;

	si = slot_index(s);
	if (si < 0)
		return e->frame + 8 - (uint64_t)(si + 2) * 4;
	return e->padding + (uint64_t)si * 4;
}

static int
fn_has_call(Fn *fn)
{
	Blk *b;
	Ins *i;

	for (b=fn->start; b; b=b->link)
		for (i=b->ins; i!=&b->ins[b->nins]; i++)
			if (i->op == Ocall)
				return 1;
	return 0;
}

static int
free_addr_scratch(Fn *fn)
{
	int r;

	for (r=A0; r<=A5; r++)
		if (!(fn->reg & BIT(r)))
			return r;
	return A7;
}

static int
ref_needs_ascratch(Fn *fn, Ref r)
{
	Mem *m;

	switch (rtype(r)) {
	default:
		return 0;
	case RTmp:
		return isreg(r) && D0 <= (int)r.val && (int)r.val <= D7
			&& free_addr_scratch(fn) == A7;
	case RCon:
		return free_addr_scratch(fn) == A7;
	case RMem:
		m = &fn->mem[r.val];
		return ref_needs_ascratch(fn, m->base) || ref_needs_ascratch(fn, m->index);
	}
}

static int
ins_needs_ascratch(Fn *fn, Ins *i)
{
	switch (i->op) {
	default:
		return 0;
	case Oaddr:
		return 1;
	case Oload:
	case Oloadsb:
	case Oloadub:
	case Oloadsh:
	case Oloaduh:
	case Oloadsw:
	case Oloaduw:
		return ref_needs_ascratch(fn, i->arg[0]);
	case Ostoreb:
	case Ostoreh:
	case Ostorew:
	case Ostorel:
	case Ostores:
	case Ostored:
		return ref_needs_ascratch(fn, i->arg[1]);
	}
}

static int
fn_uses_ascratch(Fn *fn)
{
	Blk *b;
	Ins *i;

	for (b=fn->start; b; b=b->link)
		for (i=b->ins; i!=&b->ins[b->nins]; i++)
			if (ins_needs_ascratch(fn, i))
				return 1;
	return 0;
}

static int64_t
conoffset(Con *c)
{
	switch (c->type) {
	case CUndef:
		return 0;
	case CBits:
		return c->bits.i;
	default:
		die("unsupported bedrock memory offset");
	}
}

static void
emitlabel(Con *c, FILE *f)
{
	char *p;

	p = c->local ? gasloc : gassym;
	fprintf(f, "%s%s", p, str(c->label));
}

static void
emitcon(Con *c, int k, FILE *f)
{
	int64_t n;

	switch (c->type) {
	default:
		die("invalid constant");
	case CBits:
		n = c->bits.i;
		if (k == Kw)
			n = (int32_t)n;
		fprintf(f, "%"PRId64, n);
		break;
	case CAddr:
		emitlabel(c, f);
		fprintf(f, "@ABS64");
		if (c->bits.i)
			fprintf(f, "%+"PRId64, c->bits.i);
		break;
	}
}

static void
emitpcrel32con(Con *c, FILE *f)
{
	if (c->type != CAddr)
		die("PC-relative address is not a symbol address");
	fprintf(f, "%s%s@PCREL32", c->local ? gasloc : gassym, str(c->label));
	if (c->bits.i)
		fprintf(f, "%+"PRId64, c->bits.i);
}

static void
formatpcrel32con(Con *c, int64_t extra, char *buf, size_t size)
{
	int64_t addend;
	int n;

	if (c->type != CAddr)
		die("PC-relative address is not a symbol address");
	addend = c->bits.i + extra;
	n = snprintf(buf, size, "%s%s@PCREL32", c->local ? gasloc : gassym, str(c->label));
	if (n < 0 || (size_t)n >= size)
		die("PC-relative address buffer overflow");
	if (addend)
		snprintf(buf + n, size - (size_t)n, "%+"PRId64, addend);
}

static void
emitaddrload(Con *c, char *dst, E *e)
{
	if (c->type != CAddr)
		die("address load is not a symbol address");
	if (bedrock_cmodel == BEDROCK_CMODEL_SMALL) {
		fprintf(e->f, "\tLEA [PC + ");
		emitpcrel32con(c, e->f);
		fprintf(e->f, "], %s\n", dst);
		return;
	}
	fprintf(e->f, "\tMOV.Q ");
	emitcon(c, Kl, e->f);
	fprintf(e->f, ", %s\n", dst);
}

static void
emitimmvalue(int64_t n, FILE *f)
{
	if (-32768 <= n && n <= 32767)
		fprintf(f, "%"PRId64".W", n);
	else if (INT32_MIN <= n && n <= INT32_MAX)
		fprintf(f, "%"PRId64".L", n);
	else
		fprintf(f, "%"PRId64".Q", n);
}

static void
emitconea(Con *c, int k, FILE *f)
{
	int64_t n;

	if (c->type != CBits) {
		emitcon(c, k, f);
		return;
	}
	n = c->bits.i;
	if (k == Kw)
		n = (int32_t)n;
	emitimmvalue(n, f);
}

static int
isbits(Ref r, E *e, int64_t *out)
{
	Con *c;

	if (rtype(r) != RCon)
		return 0;
	c = &e->fn->con[r.val];
	if (c->type != CBits)
		return 0;
	*out = c->bits.i;
	return 1;
}

static int
isdreg(Ref r)
{
	return rtype(r) == RTmp && isreg(r) && D0 <= (int)r.val && (int)r.val <= D7;
}

static int
isintreg(Ref r)
{
	return rtype(r) == RTmp && isreg(r)
		&& ((D0 <= (int)r.val && (int)r.val <= D7)
			|| (A0 <= (int)r.val && (int)r.val <= A7));
}

static int
isfreg(Ref r)
{
	return rtype(r) == RTmp && isreg(r) && F0 <= (int)r.val && (int)r.val <= F7;
}

static char *
memref(Ref r, E *e)
{
	static char buf[128];
	Con *c;
	char *base;

	switch (rtype(r)) {
	default:
		die("invalid memory reference");
	case RSlot:
		sprintf(buf, "[SP + %"PRIu64"]", slot(r.val, e));
		break;
	case RTmp:
		assert(isreg(r));
		if (D0 <= (int)r.val && (int)r.val <= D7) {
			base = rname(free_addr_scratch(e->fn), Kl);
			fprintf(e->f, "\tMOV.Q %s, %s\n", rname(r.val, Kl), base);
			sprintf(buf, "[%s]", base);
		} else if (A0 <= (int)r.val && (int)r.val <= A7) {
			sprintf(buf, "[%s]", rname(r.val, Kl));
		} else
			die("invalid register memory reference");
		break;
	case RMem: {
		Mem *m;
		int64_t disp;
		char sign;
		char *index;
		const char *suffix;
		Con *bc;

		m = &e->fn->mem[r.val];
		if (rtype(m->base) != RTmp && rtype(m->base) != RCon)
			die("invalid bedrock indexed memory base");
		if (rtype(m->base) == RTmp && !isreg(m->base))
			die("invalid bedrock indexed memory base");
		if (!req(m->index, R) && (rtype(m->index) != RTmp || !isreg(m->index)))
			die("invalid bedrock indexed memory index");
		if (rtype(m->base) == RTmp && !(A0 <= (int)m->base.val && (int)m->base.val <= A7))
				die("bedrock indexed memory base must be an address register");
		if (!req(m->index, R) && !(D0 <= (int)m->index.val && (int)m->index.val <= D7))
			die("bedrock indexed memory index must be a data register");
		disp = conoffset(&m->offset);
		if (rtype(m->base) == RCon) {
			bc = &e->fn->con[m->base.val];
			if (bc->type != CAddr)
				die("bedrock indexed constant base is not an address");
			base = rname(free_addr_scratch(e->fn), Kl);
			emitaddrload(bc, base, e);
		} else {
			base = rname(m->base.val, Kl);
		}
		if (req(m->index, R)) {
			if (disp == 0) {
				sprintf(buf, "[%s]", base);
			} else {
				sign = disp < 0 ? '-' : '+';
				if (disp < 0)
					disp = -disp;
				sprintf(buf, "[%s %c %"PRId64"]", base, sign, disp);
			}
		} else {
			index = rname(m->index.val, Kl);
			suffix = m->index_s32 ? ".L" : "";
			if (disp == 0) {
				sprintf(buf, "[%s + %s%s * %d]", base, index, suffix, m->scale);
			} else {
				sign = disp < 0 ? '-' : '+';
				if (disp < 0)
					disp = -disp;
				sprintf(buf, "[%s + %s%s * %d %c %"PRId64"]",
					base, index, suffix, m->scale, sign, disp);
			}
		}
		break;
	}
	case RCon:
		c = &e->fn->con[r.val];
		if (c->type != CAddr)
			die("constant memory reference is not an address");
		base = rname(free_addr_scratch(e->fn), Kl);
		emitaddrload(c, base, e);
		sprintf(buf, "[%s]", base);
		break;
	}
	return buf;
}

static char *
memrefread(Ref r, E *e)
{
	static char buf[128];
	char expr[96];
	Mem *m;
	Con *bc;
	char *index;
	const char *suffix;
	int64_t disp;

	if (bedrock_cmodel != BEDROCK_CMODEL_SMALL)
		return memref(r, e);
	switch (rtype(r)) {
	case RCon:
		bc = &e->fn->con[r.val];
		if (bc->type == CAddr) {
			formatpcrel32con(bc, 0, expr, sizeof(expr));
			snprintf(buf, sizeof(buf), "[PC + %s]", expr);
			return buf;
		}
		break;
	case RMem:
		m = &e->fn->mem[r.val];
		if (rtype(m->base) != RCon)
			break;
		bc = &e->fn->con[m->base.val];
		if (bc->type != CAddr)
			break;
		disp = conoffset(&m->offset);
		formatpcrel32con(bc, disp, expr, sizeof(expr));
		if (req(m->index, R)) {
			snprintf(buf, sizeof(buf), "[PC + %s]", expr);
			return buf;
		}
		if (rtype(m->index) != RTmp || !isreg(m->index)
		|| !(D0 <= (int)m->index.val && (int)m->index.val <= D7))
			break;
		index = rname(m->index.val, Kl);
		suffix = m->index_s32 ? ".L" : "";
		snprintf(buf, sizeof(buf), "[PC + %s%s * %d + %s]",
			index, suffix, m->scale, expr);
		return buf;
	default:
		break;
	}
	return memref(r, e);
}

static void
copyref(Ref dst, Ref src, int k, E *e)
{
	Con *c;
	int64_t n;

	if (req(dst, src))
		return;
	if (rtype(src) == RCon) {
		c = &e->fn->con[src.val];
		if (KBASE(k) == 1)
			die("floating-point constant survived instruction selection");
		if (isintreg(dst) && isbits(src, e, &n) && n == 0) {
			fprintf(e->f, "\tCLR %s\n", rname(dst.val, k));
			return;
		}
		if (rtype(dst) == RSlot) {
			fprintf(e->f, "\tMOV.%c ", siz(k));
			emitconea(c, k, e->f);
			fprintf(e->f, ", %s\n", memref(dst, e));
			return;
		}
		if (c->type == CAddr && rtype(dst) == RTmp && isreg(dst)
		&& A0 <= (int)dst.val && (int)dst.val <= A7) {
			emitaddrload(c, rname(dst.val, Kl), e);
			return;
		}
		fprintf(e->f, "\tMOV.%c ", siz(k));
		emitconea(c, k, e->f);
		fprintf(e->f, ", %s\n", rname(dst.val, k));
		return;
	}
	if (rtype(src) == RSlot) {
		assert(isreg(dst));
		fprintf(e->f, "\t%s.%c %s, %s\n",
			KBASE(k) == 1 ? "FMOV" : "MOV",
			siz(k), memref(src, e), rname(dst.val, k));
		return;
	}
	if (rtype(dst) == RSlot) {
		assert(isreg(src));
		fprintf(e->f, "\t%s.%c %s, %s\n",
			KBASE(k) == 1 ? "FMOV" : "MOV",
			siz(k), rname(src.val, k), memref(dst, e));
		return;
	}
	assert(isreg(dst) && isreg(src));
	fprintf(e->f, "\t%s.%c %s, %s\n",
		KBASE(k) == 1 ? "FMOV" : "MOV",
		siz(k), rname(src.val, k), rname(dst.val, k));
}

static int
scratchreg(int k)
{
	return KBASE(k) == 1 ? F7 : D7;
}

static void
savescratch(int k, E *e)
{
	fprintf(e->f, "\tPUSH D7\n");
	if (KBASE(k) == 1)
		fprintf(e->f, "\tFMOV.D F7, [SP + 0]\n");
}

static void
restorescratch(int k, E *e)
{
	if (KBASE(k) == 1)
		fprintf(e->f, "\tFMOV.D [SP + 0], F7\n");
	fprintf(e->f, "\tPOP D7\n");
}

static void
emitref(Ref r, int k, E *e)
{
	if (rtype(r) == RCon) {
		emitcon(&e->fn->con[r.val], k, e->f);
		return;
	}
	fprintf(e->f, "%s", rname(r.val, k));
}

static void
emitrefea(Ref r, int k, E *e)
{
	if (rtype(r) == RCon) {
		emitconea(&e->fn->con[r.val], k, e->f);
		return;
	}
	fprintf(e->f, "%s", rname(r.val, k));
}

static int
op_uses_selector(char *op)
{
	return strcmp(op, "SHL") == 0
		|| strcmp(op, "SHR") == 0
		|| strcmp(op, "SAR") == 0
		|| strcmp(op, "ROL") == 0
		|| strcmp(op, "ROR") == 0
		|| strcmp(op, "RCL") == 0
		|| strcmp(op, "RCR") == 0;
}

static void
emitop2ref(char *op, int k, Ref src, Ref dst, E *e)
{
	fprintf(e->f, "\t%s.%c ", op, siz(k));
	if (op_uses_selector(op))
		emitref(src, k, e);
	else
		emitrefea(src, k, e);
	fprintf(e->f, ", %s\n", rname(dst.val, k));
}

static void
emitbin(char *op, Ins *i, E *e, int commutative)
{
	Ref scratch;
	int64_t n;

	if (KBASE(i->cls) == 0 && strcmp(op, "ADD") == 0 && isintreg(i->to)
	&& isbits(i->arg[1], e, &n) && n == 1) {
		copyref(i->to, i->arg[0], i->cls, e);
		fprintf(e->f, "\tINC.%c %s\n", siz(i->cls), rname(i->to.val, i->cls));
		return;
	}
	if (KBASE(i->cls) == 0 && strcmp(op, "ADD") == 0 && commutative && isintreg(i->to)
	&& isbits(i->arg[0], e, &n) && n == 1) {
		copyref(i->to, i->arg[1], i->cls, e);
		fprintf(e->f, "\tINC.%c %s\n", siz(i->cls), rname(i->to.val, i->cls));
		return;
	}
	if (KBASE(i->cls) == 0 && strcmp(op, "SUB") == 0
	&& isintreg(i->to)
	&& isbits(i->arg[1], e, &n) && n == 1) {
		copyref(i->to, i->arg[0], i->cls, e);
		fprintf(e->f, "\tDEC.%c %s\n", siz(i->cls), rname(i->to.val, i->cls));
		return;
	}
	if (req(i->to, i->arg[0])) {
		emitop2ref(op, i->cls, i->arg[1], i->to, e);
		return;
	}
	if (commutative && req(i->to, i->arg[1])) {
		emitop2ref(op, i->cls, i->arg[0], i->to, e);
		return;
	}
	if (!commutative && req(i->to, i->arg[1])) {
		scratch = TMP(scratchreg(i->cls));
		savescratch(i->cls, e);
		copyref(scratch, i->arg[1], i->cls, e);
		copyref(i->to, i->arg[0], i->cls, e);
		emitop2ref(op, i->cls, scratch, i->to, e);
		restorescratch(i->cls, e);
		return;
	}
	if (commutative && rtype(i->arg[0]) == RCon && rtype(i->arg[1]) != RCon) {
		copyref(i->to, i->arg[1], i->cls, e);
		emitop2ref(op, i->cls, i->arg[0], i->to, e);
		return;
	}
	copyref(i->to, i->arg[0], i->cls, e);
	emitop2ref(op, i->cls, i->arg[1], i->to, e);
}

static void
emitext(char *op, char srcsz, Ins *i, E *e)
{
	fprintf(e->f, "\t%s%c.%c %s, %s\n",
		op, dstsiz(i->cls), srcsz, rname(i->arg[0].val, i->cls), rname(i->to.val, i->cls));
}

static void
emitloadext(char *op, char srcsz, Ins *i, E *e)
{
	fprintf(e->f, "\t%s%c.%c %s, %s\n",
		op, dstsiz(i->cls), srcsz, memrefread(i->arg[0], e), rname(i->to.val, i->cls));
}

static void
emitcast(Ins *i, E *e)
{
	char *m;

	switch (i->cls) {
	default:
		die("invalid cast class");
	case Kw:
		fprintf(e->f, "\tPUSH D7\n");
		fprintf(e->f, "\tFMOV.S %s, [SP + 0]\n", rname(i->arg[0].val, Ks));
		fprintf(e->f, "\tMOV.L [SP + 0], %s\n", rname(i->to.val, Kw));
		fprintf(e->f, "\tPOP D7\n");
		break;
	case Kl:
		fprintf(e->f, "\tPUSH D7\n");
		fprintf(e->f, "\tFMOV.D %s, [SP + 0]\n", rname(i->arg[0].val, Kd));
		fprintf(e->f, "\tMOV.Q [SP + 0], %s\n", rname(i->to.val, Kl));
		fprintf(e->f, "\tPOP D7\n");
		break;
	case Ks:
		m = rname(i->arg[0].val, Kw);
		fprintf(e->f, "\tPUSH D7\n");
		fprintf(e->f, "\tMOV.L %s, [SP + 0]\n", m);
		fprintf(e->f, "\tFMOV.S [SP + 0], %s\n", rname(i->to.val, Ks));
		fprintf(e->f, "\tPOP D7\n");
		break;
	case Kd:
		m = rname(i->arg[0].val, Kl);
		fprintf(e->f, "\tPUSH D7\n");
		fprintf(e->f, "\tMOV.Q %s, [SP + 0]\n", m);
		fprintf(e->f, "\tFMOV.D [SP + 0], %s\n", rname(i->to.val, Kd));
		fprintf(e->f, "\tPOP D7\n");
		break;
	}
}

static int
regnum(Ref r, int *kind, int *idx)
{
	int v;

	if (rtype(r) != RTmp || !isreg(r))
		return 0;
	v = (int)r.val;
	if (D0 <= v && v <= D7) {
		*kind = 'D';
		*idx = v - D0;
		return 1;
	}
	if (A0 <= v && v <= A7) {
		*kind = 'A';
		*idx = v - A0;
		return 1;
	}
	return 0;
}

static int
setcopy(Ins *i, int *dir, int *idx)
{
	int sk, dk, si, di;

	if (i->op != Ocopy || i->cls != Kl)
		return 0;
	if (!regnum(i->arg[0], &sk, &si) || !regnum(i->to, &dk, &di))
		return 0;
	if (si != di || sk == dk)
		return 0;
	*idx = si;
	if (sk == 'D' && dk == 'A') {
		*dir = 'A';
		return 1;
	}
	if (sk == 'A' && dk == 'D') {
		*dir = 'D';
		return 1;
	}
	return 0;
}

static int
emitsetcopies(Ins **pi, Ins *end, E *e)
{
	Ins *i;
	unsigned bm;
	int dir, firstdir, idx, n;

	i = *pi;
	if (!setcopy(i, &firstdir, &idx))
		return 0;
	bm = 0;
	n = 0;
	do {
		bm |= 1u << idx;
		n++;
		i++;
	} while (i != end && setcopy(i, &dir, &idx) && dir == firstdir);
	if (n < 2)
		return 0;
	fprintf(e->f, "\t%s 0x%04x\n", firstdir == 'A' ? "MOVSETAD" : "MOVSETDA", bm);
	*pi = i;
	return 1;
}

static int
emitcopyback(Ins **pi, Ins *end, E *e)
{
	Ins *i;

	i = *pi;
	if (i + 1 >= end)
		return 0;
	if (i[0].op != Ocopy || i[1].op != Ocopy || i[0].cls != i[1].cls)
		return 0;
	if (!isreg(i[0].to) || !isreg(i[0].arg[0])
	|| !isreg(i[1].to) || !isreg(i[1].arg[0]))
		return 0;
	if (!req(i[0].to, i[1].arg[0]) || !req(i[0].arg[0], i[1].to))
		return 0;
	copyref(i[0].to, i[0].arg[0], i[0].cls, e);
	*pi = i + 2;
	return 1;
}

static int
copyreg(Ins *i, int cls, int src, int dst)
{
	return i->op == Ocopy && i->cls == cls
		&& req(i->arg[0], TMP(src)) && req(i->to, TMP(dst));
}

static Ins *
skipcopynoops(Ins *i, Ins *end)
{
	while (i < end && i->op == Ocopy && req(i->to, i->arg[0]))
		i++;
	return i;
}

static int
emitcallshuffle(Ins **pi, Ins *end, E *e)
{
	Ins *i, *p[6], *q;
	int n;

	i = *pi;
	q = i;
	for (n=0; n<6; n++) {
		q = skipcopynoops(q, end);
		if (q >= end || q->op != Ocopy)
			return 0;
		p[n] = q++;
	}
	q = skipcopynoops(q, end);
	if (q >= end || q->op != Ocall)
		return 0;

	if (copyreg(p[0], Kl, A0, A4)
	&& copyreg(p[1], Kl, A1, A0)
	&& copyreg(p[2], Kl, A2, A1)
	&& copyreg(p[3], Kw, D0, D6)
	&& copyreg(p[4], Kl, A0, D7)
	&& copyreg(p[5], Kl, A4, A0)) {
		copyref(TMP(D7), TMP(A1), Kl, e);
		copyref(TMP(A1), TMP(A2), Kl, e);
		copyref(TMP(D6), TMP(D0), Kw, e);
		copyref(TMP(A4), TMP(A0), Kl, e);
		*pi = q;
		return 1;
	}

	if (copyreg(p[0], Kl, A1, A4)
	&& copyreg(p[1], Kl, A2, A1)
	&& copyreg(p[2], Kw, D0, D6)
	&& copyreg(p[3], Kl, A1, A5)
	&& copyreg(p[4], Kl, A4, A1)
	&& copyreg(p[5], Kl, A0, A6)) {
		copyref(TMP(A4), TMP(A1), Kl, e);
		copyref(TMP(A5), TMP(A2), Kl, e);
		copyref(TMP(D6), TMP(D0), Kw, e);
		copyref(TMP(A6), TMP(A0), Kl, e);
		*pi = q;
		return 1;
	}

	if (copyreg(p[0], Kl, A1, D7)
	&& copyreg(p[1], Kl, A2, A1)
	&& copyreg(p[2], Kw, D0, D6)
	&& copyreg(p[3], Kl, A1, A4)
	&& copyreg(p[4], Kl, D7, A1)
	&& copyreg(p[5], Kl, A0, A5)) {
		copyref(TMP(A4), TMP(A2), Kl, e);
		copyref(TMP(D6), TMP(D0), Kw, e);
		copyref(TMP(D7), TMP(A1), Kl, e);
		copyref(TMP(A5), TMP(A0), Kl, e);
		*pi = q;
		return 1;
	}

	return 0;
}

static void
emitins(Ins *i, E *e)
{
	switch (i->op) {
	default:
		die("no bedrock emission for %s/%d(%c)",
			optab[i->op].name ? optab[i->op].name : "unnamed",
			i->op, "wlsd"[i->cls]);
	case Oxxx:
	case Onop:
		break;
	case Oswap: {
		Ref scratch;
		int sk, dk, si, di;

		assert(isreg(i->arg[0]) && isreg(i->arg[1]));
		if (isdreg(i->arg[0]) && isdreg(i->arg[1])) {
			fprintf(e->f, "\tXCHG.%c %s, %s\n",
				siz(i->cls), rname(i->arg[0].val, i->cls), rname(i->arg[1].val, i->cls));
			break;
		}
		if (i->cls == Kl
		&& regnum(i->arg[0], &sk, &si) && regnum(i->arg[1], &dk, &di)
		&& si == di && sk != dk && (sk == 'D' || sk == 'A') && (dk == 'D' || dk == 'A')) {
			fprintf(e->f, "\t%s 0x%04x\n", sk == 'D' ? "XCHGSETAD" : "XCHGSETDA", 1u << si);
			break;
		}
		if (isfreg(i->arg[0]) && isfreg(i->arg[1])) {
			fprintf(e->f, "\tFXCHG %s, %s\n",
				rname(i->arg[0].val, i->cls), rname(i->arg[1].val, i->cls));
			break;
		}
		fprintf(e->f, "\tPUSH D7\n");
		scratch = TMP(D7);
		copyref(scratch, i->arg[0], i->cls, e);
		copyref(i->arg[0], i->arg[1], i->cls, e);
		copyref(i->arg[1], scratch, i->cls, e);
		fprintf(e->f, "\tPOP D7\n");
		break;
	}
	case Ocopy:
		copyref(i->to, i->arg[0], i->cls, e);
		break;
	case Oadd:
		emitbin(KBASE(i->cls) == 1 ? "FADD" : "ADD", i, e, 1);
		break;
	case Osub:
		emitbin(KBASE(i->cls) == 1 ? "FSUB" : "SUB", i, e, 0);
		break;
	case Omul:
		emitbin(KBASE(i->cls) == 1 ? "FMUL" : "MULU", i, e, 1);
		break;
	case Odiv:
		emitbin(KBASE(i->cls) == 1 ? "FDIV" : "DIVS", i, e, 0);
		break;
	case Oudiv:
		emitbin("DIVU", i, e, 0);
		break;
	case Orem:
		emitbin("MODS", i, e, 0);
		break;
	case Ourem:
		emitbin("MODU", i, e, 0);
		break;
	case Oand:
		emitbin("AND", i, e, 1);
		break;
	case Oor:
		emitbin("OR", i, e, 1);
		break;
	case Oxor:
		emitbin("XOR", i, e, 1);
		break;
	case Oshl:
		emitbin("SHL", i, e, 0);
		break;
	case Oshr:
		emitbin("SHR", i, e, 0);
		break;
	case Osar:
		emitbin("SAR", i, e, 0);
		break;
	case Oload:
		fprintf(e->f, "\t%s.%c %s, %s\n",
			KBASE(i->cls) == 1 ? "FMOV" : "MOV",
			siz(i->cls), memrefread(i->arg[0], e), rname(i->to.val, i->cls));
		break;
	case Oloadsb:
		emitloadext("EXTS", 'B', i, e);
		break;
	case Oloadub:
		emitloadext("EXTZ", 'B', i, e);
		break;
	case Oloadsh:
		emitloadext("EXTS", 'W', i, e);
		break;
	case Oloaduh:
		emitloadext("EXTZ", 'W', i, e);
		break;
	case Oloadsw:
		if (i->cls == Kw)
			fprintf(e->f, "\tMOV.L %s, %s\n", memrefread(i->arg[0], e), rname(i->to.val, Kw));
		else
			emitloadext("EXTS", 'L', i, e);
		break;
	case Oloaduw:
		if (i->cls == Kw)
			fprintf(e->f, "\tMOV.L %s, %s\n", memrefread(i->arg[0], e), rname(i->to.val, Kw));
		else
			emitloadext("EXTZ", 'L', i, e);
		break;
	case Ostoreb:
		fprintf(e->f, "\tMOV.B %s, %s\n", rname(i->arg[0].val, Kw), memref(i->arg[1], e));
		break;
	case Ostoreh:
		fprintf(e->f, "\tMOV.W %s, %s\n", rname(i->arg[0].val, Kw), memref(i->arg[1], e));
		break;
	case Ostorew:
		fprintf(e->f, "\tMOV.L %s, %s\n", rname(i->arg[0].val, Kw), memref(i->arg[1], e));
		break;
	case Ostorel:
		fprintf(e->f, "\tMOV.Q %s, %s\n", rname(i->arg[0].val, Kl), memref(i->arg[1], e));
		break;
	case Ostores:
		fprintf(e->f, "\tFMOV.S %s, %s\n", rname(i->arg[0].val, Ks), memref(i->arg[1], e));
		break;
	case Ostored:
		fprintf(e->f, "\tFMOV.D %s, %s\n", rname(i->arg[0].val, Kd), memref(i->arg[1], e));
		break;
	case Oextsb:
		emitext("EXTS", 'B', i, e);
		break;
	case Oextub:
		emitext("EXTZ", 'B', i, e);
		break;
	case Oextsh:
		emitext("EXTS", 'W', i, e);
		break;
	case Oextuh:
		emitext("EXTZ", 'W', i, e);
		break;
	case Oextsw:
		if (i->cls == Kw)
			copyref(i->to, i->arg[0], Kw, e);
		else
			emitext("EXTS", 'L', i, e);
		break;
	case Oextuw:
		if (i->cls == Kw)
			copyref(i->to, i->arg[0], Kw, e);
		else
			emitext("EXTZ", 'L', i, e);
		break;
	case Oaddr:
		assert(rtype(i->arg[0]) == RSlot);
		fprintf(e->f, "\tLEA [SP + %"PRIu64"], A7\n", slot(i->arg[0].val, e));
		fprintf(e->f, "\tMOV.Q A7, %s\n", rname(i->to.val, Kl));
		break;
	case Oacmp: {
		int64_t n;
		if (isbits(i->arg[1], e, &n) && n == 0) {
			fprintf(e->f, "\tTEST.%c %s, %s\n",
				siz(i->cls), rname(i->arg[0].val, i->cls), rname(i->arg[0].val, i->cls));
			break;
		}
		if (rtype(i->arg[1]) == RCon) {
			fprintf(e->f, "\tCMP.%c ", siz(i->cls));
			emitconea(&e->fn->con[i->arg[1].val], i->cls, e->f);
			fprintf(e->f, ", %s\n", rname(i->arg[0].val, i->cls));
		} else {
			fprintf(e->f, "\tCMP.%c %s, %s\n",
				siz(i->cls), rname(i->arg[1].val, i->cls), rname(i->arg[0].val, i->cls));
		}
		break;
	}
	case Oafcmp:
		fprintf(e->f, "\tFCMP.%c %s, %s\n",
			siz(i->cls), rname(i->arg[1].val, i->cls), rname(i->arg[0].val, i->cls));
		break;
	case Oflagieq:
	case Oflagine:
	case Oflagisge:
	case Oflagisgt:
	case Oflagisle:
	case Oflagislt:
	case Oflagiuge:
	case Oflagiugt:
	case Oflagiule:
	case Oflagiult:
	case Oflagfeq:
	case Oflagfge:
	case Oflagfgt:
	case Oflagfle:
	case Oflagflt:
	case Oflagfne:
	case Oflagfo:
	case Oflagfuo: {
		static char *ctoa[] = {
		#define X(c, s) [c] = s,
			CMP(X)
		#undef X
		};
		int c = i->op - Oflag;
		fprintf(e->f, "\tSET%s.L %s\n", ctoa[c], rname(i->to.val, Kw));
		break;
	}
	case Oexts:
	case Otruncd:
	case Ostosi:
	case Odtosi:
	case Oswtof:
	case Osltof:
		fprintf(e->f, "\tFCVT %s, %s\n",
			rname(i->arg[0].val, argcls(i, 0)), rname(i->to.val, i->cls));
		break;
	case Ocast:
		emitcast(i, e);
		break;
	case Ocall:
		if (e->ins_call_fence_bitmap)
			fprintf(e->f, "\tPUSHM 0x%04x\n", e->ins_call_fence_bitmap);
		if (rtype(i->arg[0]) == RCon) {
			Con *c = &e->fn->con[i->arg[0].val];
			if (c->type != CAddr)
				die("call target is not an address");
			fprintf(e->f, "\tCALL ");
			emitlabel(c, e->f);
			fprintf(e->f, "@PCREL32");
			if (c->bits.i)
				fprintf(e->f, "%+"PRId64, c->bits.i);
			fprintf(e->f, "\n");
		} else {
			assert(isreg(i->arg[0]));
			fprintf(e->f, "\tCALL %s\n", rname(i->arg[0].val, Kl));
		}
		if (e->ins_call_fence_bitmap)
			fprintf(e->f, "\tPOPM 0x%04x\n", e->ins_call_fence_bitmap);
		break;
	}
}

static int
direct_areg_ref(Ref r, int *reg)
{
	if (rtype(r) != RTmp || !isreg(r) || !(A0 <= (int)r.val && (int)r.val <= A7))
		return 0;
	*reg = r.val;
	return 1;
}

static int
con_equal(Con *a, Con *b)
{
	if (a->type != b->type)
		return 0;
	switch (a->type) {
	default:
		return 0;
	case CUndef:
		return 1;
	case CBits:
		return a->bits.i == b->bits.i;
	case CAddr:
		return a->label == b->label && a->local == b->local
			&& a->bits.i == b->bits.i;
	}
}

static int
mem_ref_equal(Fn *fn, Ref a, Ref b)
{
	Mem *ma, *mb;

	if (req(a, b))
		return 1;
	if (rtype(a) == RCon && rtype(b) == RCon)
		return con_equal(&fn->con[a.val], &fn->con[b.val]);
	if (rtype(a) != RMem || rtype(b) != RMem)
		return 0;
	ma = &fn->mem[a.val];
	mb = &fn->mem[b.val];
	return ma->scale == mb->scale
		&& ma->index_s32 == mb->index_s32
		&& mem_ref_equal(fn, ma->base, mb->base)
		&& mem_ref_equal(fn, ma->index, mb->index)
		&& con_equal(&ma->offset, &mb->offset);
}

static bits
ref_reg_bits(Fn *fn, Ref r)
{
	Mem *m;

	switch (rtype(r)) {
	default:
		return 0;
	case RTmp:
		return isreg(r) ? BIT(r.val) : 0;
	case RMem:
		m = &fn->mem[r.val];
		return ref_reg_bits(fn, m->base) | ref_reg_bits(fn, m->index);
	}
}

static int
ins_uses_ref(Fn *fn, Ins *i, Ref r)
{
	return req(i->arg[0], r) || req(i->arg[1], r)
		|| (ref_reg_bits(fn, i->arg[0]) & ref_reg_bits(fn, r))
		|| (ref_reg_bits(fn, i->arg[1]) & ref_reg_bits(fn, r));
}

static int
ins_defines_ref(Ins *i, Ref r)
{
	return rtype(i->to) == RTmp && req(i->to, r);
}

static int
ins_touches_regs(Fn *fn, Ins *i, bits regs)
{
	if (rtype(i->to) == RTmp && isreg(i->to) && (regs & BIT(i->to.val)))
		return 1;
	return (ref_reg_bits(fn, i->arg[0]) & regs)
		|| (ref_reg_bits(fn, i->arg[1]) & regs);
}

static int
ref_is_memlike(Ref r)
{
	return rtype(r) == RMem || rtype(r) == RSlot;
}

static int
rmw_scan_safe(Ins *i)
{
	if (isload(i->op) || isstore(i->op) || i->op == Ocall)
		return 0;
	if (i->op == Odiv || i->op == Oudiv || i->op == Orem || i->op == Ourem)
		return 0;
	if (KBASE(i->cls) == 1)
		return 0;
	if (ref_is_memlike(i->to) || ref_is_memlike(i->arg[0]) || ref_is_memlike(i->arg[1]))
		return 0;
	return 1;
}

static int
is_acc_additive_update(Ins *i, Ref acc)
{
	if (!req(i->to, acc))
		return 0;
	if (i->op == Oadd)
		return req(i->arg[0], acc) || req(i->arg[1], acc);
	if (i->op == Osub)
		return req(i->arg[0], acc);
	return 0;
}

static int
store_matches_acc_mem(Ins *i, Ref acc, Ref mem, int cls, E *e)
{
	if (cls == Kw) {
		if (i->op != Ostorew)
			return 0;
	} else if (cls == Kl) {
		if (i->op != Ostorel)
			return 0;
	} else {
		return 0;
	}
	return req(i->arg[0], acc) && mem_ref_equal(e->fn, i->arg[1], mem);
}

static int
ref_dead_after(Fn *fn, Ref r, Ins *start, Ins *end)
{
	Ins *scan;

	for (scan=start; scan!=end; scan++) {
		if (ins_uses_ref(fn, scan, r))
			return 0;
		if (ins_defines_ref(scan, r))
			return 1;
	}
	return 1;
}

static int
store_op_for_cls(int cls)
{
	switch (cls) {
	default:
		return -1;
	case Kw:
		return Ostorew;
	case Kl:
		return Ostorel;
	case Ks:
		return Ostores;
	case Kd:
		return Ostored;
	}
}

static int
emitmemcopyfold(Ins **pi, Ins *end, E *e)
{
	Ins *load, *store;
	char src[128], dst[128];

	load = *pi;
	if (end - load < 2 || load->op != Oload)
		return 0;
	if (KBASE(load->cls) == 1)
		return 0;
	store = load + 1;
	if (store->op != store_op_for_cls(load->cls) || !req(store->arg[0], load->to))
		return 0;
	if (!ref_dead_after(e->fn, load->to, store+1, end))
		return 0;
	snprintf(src, sizeof(src), "%s", memrefread(load->arg[0], e));
	snprintf(dst, sizeof(dst), "%s", memref(store->arg[1], e));
	fprintf(e->f, "\t%s.%c %s, %s\n",
		KBASE(load->cls) == 1 ? "FMOV" : "MOV",
		siz(load->cls), src, dst);
	*pi = store + 1;
	return 1;
}

static char *
alu_op_name(int op)
{
	switch (op) {
	default:
		return 0;
	case Oadd:
		return "ADD";
	case Osub:
		return "SUB";
	case Oand:
		return "AND";
	case Oor:
		return "OR";
	case Oxor:
		return "XOR";
	}
}

static int
op_allows_memfold(int op, Ref dst, Ref lhs, Ref rhs, Ref tmp, Ref *acc)
{
	switch (op) {
	default:
		return 0;
	case Oadd:
	case Oand:
	case Oor:
	case Oxor:
		if (req(rhs, tmp) && req(dst, lhs)) {
			*acc = lhs;
			return 1;
		}
		if (req(lhs, tmp) && req(dst, rhs)) {
			*acc = rhs;
			return 1;
		}
		return 0;
	case Osub:
		if (req(rhs, tmp) && req(dst, lhs)) {
			*acc = lhs;
			return 1;
		}
		return 0;
	}
}

static int
emitloadopfold(Ins **pi, Ins *end, E *e)
{
	Ins *load, *op, *inc;
	Ref tmp, acc;
	char src[128];
	char *name;
	int reg, size;

	load = *pi;
	if (end - load < 2 || load->op != Oload || KBASE(load->cls) != 0)
		return 0;
	tmp = load->to;
	if (!isintreg(tmp) || isdreg(tmp))
		return 0;
	op = load + 1;
	name = alu_op_name(op->op);
	if (name == 0 || op->cls != load->cls)
		return 0;
	if (!op_allows_memfold(op->op, op->to, op->arg[0], op->arg[1], tmp, &acc))
		return 0;
	if (!isdreg(acc) || !ref_dead_after(e->fn, tmp, op+1, end))
		return 0;
	inc = 0;
	size = postinc_size(load);
	if (size && direct_areg_ref(load->arg[0], &reg))
		inc = findpostincadd(op+1, end, reg, size, e);
	if (inc) {
		snprintf(src, sizeof(src), "[%s++]", rname(reg, Kl));
		inc->op = Onop;
	} else {
		snprintf(src, sizeof(src), "%s", memrefread(load->arg[0], e));
	}
	fprintf(e->f, "\t%s.%c %s, %s\n", name, siz(load->cls), src, rname(acc.val, load->cls));
	*pi = op + 1;
	return 1;
}

static int
emitrmwaddstore(Ins **pi, Ins *end, E *e)
{
	Ins *load, *add, *scan, *store, *emit;
	Ref tmp, acc, mem;
	bits memregs;
	int tmp_live;

	load = *pi;
	if (end - load < 3 || load->op != Oload || KBASE(load->cls) != 0)
		return 0;
	if (load->cls != Kw && load->cls != Kl)
		return 0;
	tmp = load->to;
	if (!isdreg(tmp))
		return 0;
	mem = load->arg[0];
	add = load + 1;
	if (add->op != Oadd || add->cls != load->cls)
		return 0;
	if (req(add->arg[1], tmp) && req(add->to, add->arg[0]))
		acc = add->arg[0];
	else if (req(add->arg[0], tmp) && req(add->to, add->arg[1]))
		acc = add->arg[1];
	else
		return 0;
	if (!isdreg(acc) || req(acc, tmp))
		return 0;

	memregs = ref_reg_bits(e->fn, mem);
	tmp_live = 1;
	store = 0;
	for (scan=add+1; scan!=end; scan++) {
		if (store_matches_acc_mem(scan, acc, mem, load->cls, e)) {
			store = scan;
			break;
		}
		if (!rmw_scan_safe(scan))
			return 0;
		if (memregs && ins_touches_regs(e->fn, scan, memregs))
			return 0;
		if (tmp_live && ins_uses_ref(e->fn, scan, tmp))
			return 0;
		if (ins_uses_ref(e->fn, scan, acc) || ins_defines_ref(scan, acc)) {
			if (!is_acc_additive_update(scan, acc))
				return 0;
		}
		if (ins_defines_ref(scan, tmp))
			tmp_live = 0;
	}
	if (store == 0)
		return 0;

	for (emit=add+1; emit!=store; emit++)
		emitins(emit, e);
	fprintf(e->f, "\tADD.%c %s, %s\n",
		siz(load->cls), rname(acc.val, load->cls), memref(store->arg[1], e));
	*pi = store + 1;
	return 1;
}

static int
ref_uses_reg(Fn *fn, Ref r, int reg)
{
	Mem *m;

	switch (rtype(r)) {
	default:
		return 0;
	case RTmp:
		return isreg(r) && (int)r.val == reg;
	case RMem:
		m = &fn->mem[r.val];
		return ref_uses_reg(fn, m->base, reg) || ref_uses_reg(fn, m->index, reg);
	}
}

static int
ins_uses_or_defs_reg(Fn *fn, Ins *i, int reg)
{
	if (i->op == Ocall)
		return 1;
	if (rtype(i->to) == RTmp && isreg(i->to) && (int)i->to.val == reg)
		return 1;
	return ref_uses_reg(fn, i->arg[0], reg) || ref_uses_reg(fn, i->arg[1], reg);
}

static int
postinc_size(Ins *i)
{
	switch (i->op) {
	default:
		return 0;
	case Oload:
		return i->cls == Kl || i->cls == Kd ? 8 : 4;
	case Ostorew:
	case Ostores:
		return 4;
	case Ostorel:
	case Ostored:
		return 8;
	}
}

static int
ispostincadd(Ins *i, int reg, int size, E *e)
{
	if (i->op != Oadd || i->cls != Kl || !req(i->to, TMP(reg)))
		return 0;
	return (req(i->arg[0], TMP(reg)) && isconval(i->arg[1], e, size))
		|| (req(i->arg[1], TMP(reg)) && isconval(i->arg[0], e, size));
}

static Ins *
findpostincadd(Ins *i, Ins *end, int reg, int size, E *e)
{
	Ins *scan;

	for (scan=i+1; scan!=end; scan++) {
		if (ispostincadd(scan, reg, size, e))
			return scan;
		if (ins_uses_or_defs_reg(e->fn, scan, reg))
			return 0;
	}
	return 0;
}

static int
emitpostinc(Ins **pi, Ins *end, E *e)
{
	Ins *i, *inc;
	int reg, size;

	i = *pi;
	size = postinc_size(i);
	if (size == 0)
		return 0;
	if (i->op == Oload) {
		if (!direct_areg_ref(i->arg[0], &reg) || req(i->to, TMP(reg)))
			return 0;
		inc = findpostincadd(i, end, reg, size, e);
		if (inc == 0)
			return 0;
		if (i+1 != end && i+1 != inc && !isdreg(i->to)) {
			Ins *op;
			Ref acc;
			char *name;

			op = i + 1;
			name = alu_op_name(op->op);
			if (name && op->cls == i->cls
			&& op_allows_memfold(op->op, op->to, op->arg[0], op->arg[1], i->to, &acc)
			&& isdreg(acc)
			&& ref_dead_after(e->fn, i->to, op+1, end)) {
				fprintf(e->f, "\t%s.%c [%s++], %s\n",
					name, siz(i->cls), rname(reg, Kl), rname(acc.val, i->cls));
				inc->op = Onop;
				*pi = op + 1;
				return 1;
			}
		}
		fprintf(e->f, "\t%s.%c [%s++], %s\n",
			KBASE(i->cls) == 1 ? "FMOV" : "MOV",
			siz(i->cls), rname(reg, Kl), rname(i->to.val, i->cls));
		inc->op = Onop;
		*pi = i + 1;
		return 1;
	}
	if (isstore(i->op)) {
		if (!direct_areg_ref(i->arg[1], &reg) || req(i->arg[0], TMP(reg)))
			return 0;
		inc = findpostincadd(i, end, reg, size, e);
		if (inc == 0)
			return 0;
		fprintf(e->f, "\t%s.%c %s, [%s++]\n",
			KBASE(i->cls) == 1 ? "FMOV" : "MOV",
			size == 8 ? 'Q' : 'L', rname(i->arg[0].val, i->cls), rname(reg, Kl));
		inc->op = Onop;
		*pi = i + 1;
		return 1;
	}
	return 0;
}

static int
samecon(Ref a, Ref b, E *e)
{
	int64_t av, bv;

	return isbits(a, e, &av) && isbits(b, e, &bv) && av == bv;
}

static int
isbinregcon(Ins *i, int op, Ref dst, Ref src, Ref *con)
{
	if (i->op != op || i->cls != Kw || !req(i->to, dst) || !req(i->arg[0], src))
		return 0;
	if (rtype(i->arg[1]) != RCon)
		return 0;
	*con = i->arg[1];
	return 1;
}

static int
isbinregreg(Ins *i, int op, Ref dst, Ref lhs, Ref rhs)
{
	if (i->op != op || i->cls != Kw || !req(i->to, dst))
		return 0;
	return (req(i->arg[0], lhs) && req(i->arg[1], rhs))
		|| (req(i->arg[0], rhs) && req(i->arg[1], lhs));
}

static int
emitbitfieldreplace(Ins **pi, Ins *end, E *e)
{
	Ins *i;
	Ref x, y, tmp, shift, field_mask, clear_mask, low_mask;
	int64_t sh, fm, cm, lm;
	uint32_t insert_mask, keep_mask;

	i = *pi;
	if (end - i < 8 || i[0].op != Oswap || i[0].cls != Kw)
		return 0;
	x = i[0].arg[0];
	y = i[0].arg[1];
	if (!isintreg(x) || !isintreg(y))
		return 0;
	tmp = i[1].to;
	if (!isbinregcon(&i[1], Osar, tmp, x, &shift)
	|| !isbinregcon(&i[2], Oand, tmp, tmp, &field_mask)
	|| !isbinregcon(&i[3], Oand, y, y, &clear_mask)
	|| !isbinregcon(&i[4], Oshl, tmp, tmp, &shift)
	|| !isbinregreg(&i[5], Oor, y, y, tmp)
	|| !isbinregcon(&i[6], Oand, x, x, &low_mask)
	|| !isbinregreg(&i[7], Oor, y, y, x))
		return 0;
	if (!samecon(i[1].arg[1], i[4].arg[1], e)
	|| !isbits(shift, e, &sh)
	|| !isbits(field_mask, e, &fm)
	|| !isbits(clear_mask, e, &cm)
	|| !isbits(low_mask, e, &lm))
		return 0;
	if (sh < 0 || sh >= 32 || fm < 0 || fm > 0xffffffffLL || lm < 0 || lm > 0xffffffffLL)
		return 0;
	insert_mask = (uint32_t)fm << (uint)sh;
	if ((uint32_t)cm != ~insert_mask)
		return 0;
	if (((uint32_t)lm & insert_mask) != 0)
		return 0;
	keep_mask = insert_mask | (uint32_t)lm;

	fprintf(e->f, "\tAND.L ");
	emitimmvalue((int32_t)keep_mask, e->f);
	fprintf(e->f, ", %s\n", rname(y.val, Kw));
	fprintf(e->f, "\tAND.L ");
	emitimmvalue((int32_t)cm, e->f);
	fprintf(e->f, ", %s\n", rname(x.val, Kw));
	fprintf(e->f, "\tOR.L %s, %s\n", rname(x.val, Kw), rname(y.val, Kw));
	*pi = i + 8;
	return 1;
}

static int
emitdivmodpair(Ins **pi, Ins *end, E *e)
{
	Ins *i;
	Ref dividend, quotient, divisor;
	char *op;
	int off;

	i = *pi;
	if (end - i < 2 || KBASE(i[0].cls) != 0)
		return 0;
	if (i[0].op == Ocopy) {
		if (end - i < 3)
			return 0;
		off = 1;
		dividend = i[0].arg[0];
		quotient = i[0].to;
	} else {
		off = 0;
		dividend = i[0].arg[0];
		quotient = i[0].to;
	}
	if (i[off].op == Odiv && i[off+1].op == Orem)
		op = "DIVMODS";
	else if (i[off].op == Oudiv && i[off+1].op == Ourem)
		op = "DIVMODU";
	else
		return 0;
	if (i[0].cls != i[off].cls || i[0].cls != i[off+1].cls)
		return 0;
	divisor = i[off].arg[1];
	if (!isdreg(dividend) || !isdreg(quotient) || req(dividend, quotient))
		return 0;
	if (!req(i[off].to, quotient))
		return 0;
	if (off && !req(i[off].arg[0], quotient))
		return 0;
	if (!off && !req(i[off].arg[0], dividend))
		return 0;
	if (!req(i[off+1].to, dividend) || !req(i[off+1].arg[0], dividend) || !req(i[off+1].arg[1], divisor))
		return 0;

	copyref(quotient, dividend, i[0].cls, e);
	fprintf(e->f, "\t%s.%c ", op, siz(i[0].cls));
	emitrefea(divisor, i[0].cls, e);
	fprintf(e->f, ", %s, %s\n", rname(quotient.val, i[0].cls), rname(dividend.val, i[0].cls));
	*pi = i + off + 2;
	return 1;
}

static int
ismulregcon(Ins *i, Ref reg, Ref *con)
{
	if (i->op != Omul || i->cls != Kw || !req(i->to, reg))
		return 0;
	if (req(i->arg[0], reg) && rtype(i->arg[1]) == RCon) {
		*con = i->arg[1];
		return 1;
	}
	if (req(i->arg[1], reg) && rtype(i->arg[0]) == RCon) {
		*con = i->arg[0];
		return 1;
	}
	return 0;
}

static int
isaddaccreg(Ins *i, Ref acc, Ref reg)
{
	if (i->op != Oadd || i->cls != Kw || !req(i->to, acc))
		return 0;
	return (req(i->arg[0], acc) && req(i->arg[1], reg))
		|| (req(i->arg[1], acc) && req(i->arg[0], reg));
}

static int
emitdivmodweighted(Ins **pi, Ins *end, E *e)
{
	Ins *i;
	Ref dividend, quotient, divisor, qcoef, rcoef, acc;
	char *op;

	i = *pi;
	if (end - i < 6 || KBASE(i[0].cls) != 0 || i[0].cls != Kw)
		return 0;
	if (i[0].op == Odiv && i[1].op == Orem)
		op = "DIVMODS";
	else if (i[0].op == Oudiv && i[1].op == Ourem)
		op = "DIVMODU";
	else
		return 0;
	if (i[1].cls != Kw)
		return 0;
	dividend = i[0].arg[0];
	quotient = i[0].to;
	divisor = i[0].arg[1];
	if (!isdreg(dividend) || !isdreg(quotient) || req(dividend, quotient))
		return 0;
	if (rtype(divisor) == RTmp && isreg(divisor) && (req(divisor, dividend) || req(divisor, quotient)))
		return 0;
	if (!req(i[1].to, dividend) || !req(i[1].arg[0], dividend) || !req(i[1].arg[1], divisor))
		return 0;
	if (!ismulregcon(&i[2], quotient, &qcoef) || !isaddaccreg(&i[3], i[3].to, quotient))
		return 0;
	acc = i[3].to;
	if (!isdreg(acc) || req(acc, dividend) || req(acc, quotient))
		return 0;
	if (!ismulregcon(&i[4], dividend, &rcoef) || !isaddaccreg(&i[5], acc, dividend))
		return 0;

	fprintf(e->f, "\t%s.L ", op);
	emitrefea(divisor, Kw, e);
	fprintf(e->f, ", %s, %s\n", rname(dividend.val, Kw), rname(quotient.val, Kw));
	fprintf(e->f, "\tMULU.L ");
	emitrefea(qcoef, Kw, e);
	fprintf(e->f, ", %s\n", rname(dividend.val, Kw));
	fprintf(e->f, "\tADD.L %s, %s\n", rname(dividend.val, Kw), rname(acc.val, Kw));
	fprintf(e->f, "\tMULU.L ");
	emitrefea(rcoef, Kw, e);
	fprintf(e->f, ", %s\n", rname(quotient.val, Kw));
	fprintf(e->f, "\tADD.L %s, %s\n", rname(quotient.val, Kw), rname(acc.val, Kw));
	*pi = i + 6;
	return 1;
}

static int
skipoverwrittencopy(Ins **pi, Ins *end)
{
	Ins *i;

	i = *pi;
	if (end - i < 2 || i[0].op != Ocopy || i[1].op != Ocopy)
		return 0;
	if (rtype(i[0].to) != RTmp || !isreg(i[0].to) || !req(i[0].to, i[1].to))
		return 0;
	if (req(i[1].arg[0], i[0].to))
		return 0;
	*pi = i + 1;
	return 1;
}

static int
isdirectcall(Ins *i, E *e)
{
	Con *c;

	if (i->op != Ocall || rtype(i->arg[0]) != RCon)
		return 0;
	c = &e->fn->con[i->arg[0].val];
	return c->type == CAddr;
}

static int
isnoopcopy(Ins *i)
{
	return i->op == Ocopy && req(i->to, i->arg[0]);
}

static void
emittailcall(Ins *i, E *e)
{
	Con *c;

	c = &e->fn->con[i->arg[0].val];
	fprintf(e->f, "\tJMP.L ");
	emitlabel(c, e->f);
	fprintf(e->f, "@WORD_PCREL32");
	if (c->bits.i)
		fprintf(e->f, "%+"PRId64, c->bits.i);
	fprintf(e->f, "\n");
}

static bits
fence_ref_regs(Fn *fn, Ref r)
{
	Mem *m;
	bits b;

	switch (rtype(r)) {
	default:
		return 0;
	case RTmp:
		return isreg(r) && (r.val == A4 || r.val == A5) ? BIT(r.val) : 0;
	case RMem:
		m = &fn->mem[r.val];
		b = fence_ref_regs(fn, m->base);
		b |= fence_ref_regs(fn, m->index);
		return b;
	}
}

static bits
fence_ins_uses(Fn *fn, Ins *i)
{
	bits b;

	b = 0;
	if (!req(i->arg[0], R))
		b |= fence_ref_regs(fn, i->arg[0]);
	if (!req(i->arg[1], R))
		b |= fence_ref_regs(fn, i->arg[1]);
	return b;
}

static bits
fence_ins_defs(Ins *i)
{
	if (rtype(i->to) == RTmp && isreg(i->to) && (i->to.val == A4 || i->to.val == A5))
		return BIT(i->to.val);
	return 0;
}

static unsigned
fence_pushm_bitmap(bits live)
{
	if (!(live & (BIT(A4) | BIT(A5))))
		return 0;
	return (1u << (8 + A4 - A0)) | (1u << (8 + A5 - A0));
}

static void
record_emitted_fn(Fn *fn)
{
	uint i;

	for (i=0; i<nemitted_fns; i++)
		if (strcmp(emitted_fns[i].name, fn->name) == 0) {
			emitted_fns[i].regs = fn->reg;
			return;
		}
	if (nemitted_fns == sizeof emitted_fns / sizeof emitted_fns[0])
		return;
	strncpy(emitted_fns[nemitted_fns].name, fn->name, NString-1);
	emitted_fns[nemitted_fns].name[NString-1] = '\0';
	emitted_fns[nemitted_fns].regs = fn->reg;
	nemitted_fns++;
}

static int
known_callee_regs(E *e, Ins *i, bits *regs)
{
	Con *c;
	char *name;
	uint j;

	if (i->op != Ocall || rtype(i->arg[0]) != RCon)
		return 0;
	c = &e->fn->con[i->arg[0].val];
	if (c->type != CAddr || c->bits.i != 0)
		return 0;
	name = str(c->label);
	for (j=0; j<nemitted_fns; j++)
		if (strcmp(emitted_fns[j].name, name) == 0) {
			*regs = emitted_fns[j].regs;
			return 1;
		}
	return 0;
}

static unsigned
call_fence_bitmap(E *e, Ins *i, bits live)
{
	bits regs;

	live &= BIT(A4) | BIT(A5);
	if (!live)
		return 0;
	if (known_callee_regs(e, i, &regs) && !(live & regs))
		return 0;
	return fence_pushm_bitmap(live);
}

static uint
maxblkid(Fn *fn)
{
	Blk *b;
	uint max;

	max = 0;
	for (b=fn->start; b; b=b->link)
		if (b->id > max)
			max = b->id;
	return max;
}

static void
compute_fence_liveness(Fn *fn, bits **pin, bits **pout, uint *pn)
{
	Blk *b;
	Ins *i;
	bits *in, *out, *gen, *kill;
	bits newout, newin, uses, defs;
	uint n;
	int changed;

	n = maxblkid(fn) + 1;
	in = calloc(n, sizeof in[0]);
	out = calloc(n, sizeof out[0]);
	gen = calloc(n, sizeof gen[0]);
	kill = calloc(n, sizeof kill[0]);
	if (!in || !out || !gen || !kill)
		die("out of memory");

	for (b=fn->start; b; b=b->link) {
		for (i=b->ins; i!=&b->ins[b->nins]; i++) {
			uses = fence_ins_uses(fn, i);
			defs = fence_ins_defs(i);
			gen[b->id] |= uses & ~kill[b->id];
			kill[b->id] |= defs;
		}
		gen[b->id] |= fence_ref_regs(fn, b->jmp.arg) & ~kill[b->id];
	}

	do {
		changed = 0;
		for (b=fn->start; b; b=b->link) {
			newout = 0;
			if (b->s1)
				newout |= in[b->s1->id];
			if (b->s2)
				newout |= in[b->s2->id];
			newin = gen[b->id] | (newout & ~kill[b->id]);
			if (newout != out[b->id] || newin != in[b->id]) {
				out[b->id] = newout;
				in[b->id] = newin;
				changed = 1;
			}
		}
	} while (changed);

	free(gen);
	free(kill);
	*pin = in;
	*pout = out;
	*pn = n;
}

static unsigned *
block_call_fences(E *e, Blk *b, bits liveout)
{
	unsigned *fences;
	bits live;
	Ins *i;
	uint idx;

	if (b->nins == 0)
		return 0;
	fences = calloc(b->nins, sizeof fences[0]);
	if (!fences)
		die("out of memory");
	live = liveout | fence_ref_regs(e->fn, b->jmp.arg);
	for (idx=b->nins; idx-- > 0;) {
		i = &b->ins[idx];
		if (i->op == Ocall)
			fences[idx] = call_fence_bitmap(e, i, live);
		live = fence_ins_uses(e->fn, i) | (live & ~fence_ins_defs(i));
	}
	return fences;
}

static int
free_pushm_pad_reg(E *e)
{
	static int candidates[] = {
		D0, D1, D2, D3, D4, D5,
		A0, A1, A2, A3, A4, A5,
		D6, D7, A6, A7,
		-1
	};
	int i, r;

	for (i=0; candidates[i]>=0; i++) {
		r = candidates[i];
		if (r == A7 && !e->uses_ascratch)
			return r;
		if (e->fn->reg & BIT(r))
			continue;
		if (e->uses_ascratch && r == A7)
			continue;
		return r;
	}
	return -1;
}

static void
framelayout(E *e)
{
	int i, save_count;
	int pad;

	e->has_call = fn_has_call(e->fn);
	e->uses_ascratch = fn_uses_ascratch(e->fn);
	e->ins_call_fence_bitmap = 0;
	e->save_pad_reg = -1;
	e->save_size = 0;
	save_count = 0;
	for (i=0; bedrock_rclob[i]>=0; i++)
		if (e->fn->reg & BIT(bedrock_rclob[i])) {
			e->save_size += 8u;
			save_count++;
		}
	if (e->uses_ascratch) {
		e->save_size += 8u;
		save_count++;
	}
	e->frame = (uint64_t)e->fn->slot * 4u;
	e->frame = (e->frame + 15u) & ~(uint64_t)15;
	if (e->has_call) {
		if (((e->frame + e->save_size) & 15u) != 8u) {
			pad = save_count > 0 ? free_pushm_pad_reg(e) : -1;
			if (pad >= 0) {
				e->save_pad_reg = pad;
				e->save_size += 8u;
			} else {
				e->frame += 8u;
			}
		}
	} else if (((e->frame + e->save_size) & 15u) != 0) {
		pad = save_count > 0 ? free_pushm_pad_reg(e) : -1;
		if (pad >= 0) {
			e->save_pad_reg = pad;
			e->save_size += 8u;
		} else {
			e->frame += 8u;
		}
	}
	e->padding = e->frame - (uint64_t)e->fn->slot * 4u;
}

static int
haslocalslots(E *e)
{
	return e->fn->slot != 0;
}

static unsigned
saved_reg_bitmap(E *e)
{
	unsigned bm;
	int i, r;

	bm = 0;
	for (i=0; bedrock_rclob[i]>=0; i++) {
		r = bedrock_rclob[i];
		if (!(e->fn->reg & BIT(r)))
			continue;
		if (D0 <= r && r <= D7)
			bm |= 1u << (r - D0);
		else if (A0 <= r && r <= A7)
			bm |= 1u << (8 + r - A0);
		else
			die("cannot save register with PUSHM");
	}
	if (e->uses_ascratch)
		bm |= 1u << (8 + A7 - A0);
	if (e->save_pad_reg >= 0) {
		r = e->save_pad_reg;
		if (D0 <= r && r <= D7)
			bm |= 1u << (r - D0);
		else if (A0 <= r && r <= A7)
			bm |= 1u << (8 + r - A0);
		else
			die("cannot save register with PUSHM");
	}
	return bm;
}

static int
popcount16(unsigned bm)
{
	int n;

	n = 0;
	bm &= 0xffffu;
	while (bm) {
		n += bm & 1u;
		bm >>= 1;
	}
	return n;
}

static void
emitcallee_saves(E *e)
{
	int i;
	unsigned bm;

	bm = saved_reg_bitmap(e);
	if (popcount16(bm) > 1) {
		fprintf(e->f, "\tPUSHM 0x%04x\n", bm);
		return;
	}
	for (i=0; bedrock_rclob[i]>=0; i++)
		if (e->fn->reg & BIT(bedrock_rclob[i]))
			fprintf(e->f, "\tPUSH %s\n", rname(bedrock_rclob[i], Kl));
	if (e->uses_ascratch)
		fprintf(e->f, "\tPUSH A7\n");
	if (e->save_pad_reg >= 0)
		fprintf(e->f, "\tPUSH %s\n", rname(e->save_pad_reg, Kl));
}

static void
emitcallee_restores(E *e)
{
	int i;
	unsigned bm;

	bm = saved_reg_bitmap(e);
	if (popcount16(bm) > 1) {
		fprintf(e->f, "\tPOPM 0x%04x\n", bm);
		return;
	}
	if (e->uses_ascratch)
		fprintf(e->f, "\tPOP A7\n");
	if (e->save_pad_reg >= 0)
		fprintf(e->f, "\tPOP %s\n", rname(e->save_pad_reg, Kl));
	for (i=0; bedrock_rclob[i]>=0; i++)
		;
	while (i-- > 0)
		if (e->fn->reg & BIT(bedrock_rclob[i]))
			fprintf(e->f, "\tPOP %s\n", rname(bedrock_rclob[i], Kl));
}

static void
emitframe(E *e, int pop)
{
	if (pop) {
		if (e->frame)
			fprintf(e->f, "\tADD.Q %"PRIu64", SP\n", e->frame);
		emitcallee_restores(e);
	} else {
		emitcallee_saves(e);
		if (e->frame)
			fprintf(e->f, "\tSUB.Q %"PRIu64", SP\n", e->frame);
	}
}

static void
emitjmpref(FILE *f, Blk *b, int base)
{
	fprintf(f, ".Lbb%d@WORD_PCREL16", base + b->id);
}

static int
isconval(Ref r, E *e, int64_t val)
{
	Con *c;

	if (rtype(r) != RCon)
		return 0;
	c = &e->fn->con[r.val];
	return c->type == CBits && c->bits.i == val;
}

static int
isregcopyzero(Ins *i, Ref *dst, E *e)
{
	if (i->op != Ocopy || i->cls != Kw || !isreg(i->to))
		return 0;
	if (!isconval(i->arg[0], e, 0))
		return 0;
	*dst = i->to;
	return 1;
}

static int
iscountinc(Ins *i, Ref counter, E *e)
{
	if (i->op != Oadd || i->cls != Kw || !req(i->to, counter))
		return 0;
	return (req(i->arg[0], counter) && isconval(i->arg[1], e, 1))
		|| (req(i->arg[1], counter) && isconval(i->arg[0], e, 1));
}

static int
isincreg(Ins *i, Ref reg, E *e)
{
	if (i->op != Oadd || i->cls != Kw || !req(i->to, reg))
		return 0;
	return (req(i->arg[0], reg) && isconval(i->arg[1], e, 1))
		|| (req(i->arg[1], reg) && isconval(i->arg[0], e, 1));
}

static int
isaccadd(Ins *i, Ref acc, Ref loaded)
{
	if (i->op != Oadd || i->cls != Kw || !req(i->to, acc))
		return 0;
	return (req(i->arg[0], acc) && req(i->arg[1], loaded))
		|| (req(i->arg[1], acc) && req(i->arg[0], loaded));
}

static int
isaccaddreg(Ins *i, Ref acc, Ref *src)
{
	if (i->op != Oadd || i->cls != Kw || !req(i->to, acc))
		return 0;
	if (req(i->arg[0], acc) && isdreg(i->arg[1])) {
		*src = i->arg[1];
		return 1;
	}
	if (req(i->arg[1], acc) && isdreg(i->arg[0])) {
		*src = i->arg[0];
		return 1;
	}
	return 0;
}

static int
isaccsub(Ins *i, Ref acc, Ref src)
{
	if (i->op != Osub || i->cls != Kw || !req(i->to, acc))
		return 0;
	return req(i->arg[0], acc) && req(i->arg[1], src);
}

static int
isindexedmem4disp(Ref r, Ref counter, int64_t disp, E *e, Ref *base)
{
	return isindexedmemdisp(r, counter, 4, disp, e, base);
}

static int
isindexedmemdisp(Ref r, Ref counter, int scale, int64_t disp, E *e, Ref *base)
{
	Mem *m;

	if (rtype(r) != RMem)
		return 0;
	m = &e->fn->mem[r.val];
	if (!req(m->index, counter) || m->scale != scale)
		return 0;
	if (conoffset(&m->offset) != disp)
		return 0;
	if (rtype(m->base) != RTmp || !isreg(m->base) || !(A0 <= (int)m->base.val && (int)m->base.val <= A7))
		return 0;
	*base = m->base;
	return 1;
}

static int
isindexedload4(Ins *i, Ref counter, E *e, Ref *base)
{
	if (i->op != Oload || i->cls != Kw)
		return 0;
	return isindexedmemdisp(i->arg[0], counter, 4, 0, e, base);
}

static int
isindexedstore4(Ins *i, Ref value, Ref counter, E *e, Ref *base)
{
	if (i->op != Ostorew || !req(i->arg[0], value))
		return 0;
	return isindexedmemdisp(i->arg[1], counter, 4, 0, e, base);
}

static int
isindexedloadscaled(Ins *i, Ref counter, int cls, E *e, Ref *base)
{
	int scale;

	if (i->op != Oload || i->cls != cls)
		return 0;
	scale = cls == Kl ? 8 : 4;
	return isindexedmemdisp(i->arg[0], counter, scale, 0, e, base);
}

static int
isindexedstorescaled(Ins *i, Ref value, Ref counter, int cls, E *e, Ref *base)
{
	int scale, storeop;

	storeop = cls == Kl ? Ostorel : Ostorew;
	if (i->op != storeop || !req(i->arg[0], value))
		return 0;
	scale = cls == Kl ? 8 : 4;
	return isindexedmemdisp(i->arg[1], counter, scale, 0, e, base);
}

static int
isshlimm(Ins *i, Ref reg, E *e, int64_t amount)
{
	if (i->op != Oshl || i->cls != Kw || !req(i->to, reg) || !req(i->arg[0], reg))
		return 0;
	return isconval(i->arg[1], e, amount);
}

static int
try_emit_rep_sum(E *e, int idbase)
{
	Blk *entry, *header, *body, *exitb, *retb;
	Ins *cmp, *load, *add, *inc, *retcopy;
	Ref zero0, zero1, counter, acc, limit, base;
	int cond;

	entry = e->fn->start;
	if (haslocalslots(e) || entry == 0)
		return 0;
	if (entry->nins == 0 && entry->jmp.type == Jjmp && entry->s1 != 0)
		entry = entry->s1;
	if (entry->jmp.type != Jjmp || entry->s1 == 0 || entry->nins != 2)
		return 0;
	if (!isregcopyzero(&entry->ins[0], &zero0, e) || !isregcopyzero(&entry->ins[1], &zero1, e))
		return 0;
	header = entry->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || (cond != Cislt && cond != Cisge))
		return 0;
	counter = cmp->arg[0];
	limit = cmp->arg[1];
	if (!req(counter, zero0) && !req(counter, zero1))
		return 0;
	acc = req(counter, zero0) ? zero1 : zero0;
	if (!isdreg(counter) || !isdreg(acc) || !isdreg(limit))
		return 0;
	if (cond == Cislt) {
		body = header->s1;
		exitb = header->s2;
	} else {
		body = header->s2;
		exitb = header->s1;
	}
	if (body == 0 || body->jmp.type != Jjmp || body->s1 != header)
		return 0;
	if (body->nins != 3 || exitb == 0 || exitb->nins != 1)
		return 0;
	load = &body->ins[0];
	add = &body->ins[1];
	inc = &body->ins[2];
	if (!isindexedload4(load, counter, e, &base))
		return 0;
	if (!isaccadd(add, acc, load->to) || !iscountinc(inc, counter, e))
		return 0;
	retcopy = &exitb->ins[0];
	if (retcopy->op != Ocopy || retcopy->cls != Kw || !req(retcopy->to, TMP(D0)) || !req(retcopy->arg[0], acc))
		return 0;
	if (exitb->jmp.type == Jjmp) {
		retb = exitb->s1;
		if (retb == 0 || retb->jmp.type != Jret0)
			return 0;
		if (retb->nins != 0
		&& !(retb->nins == 1 && retb->ins[0].op == Ocopy && req(retb->ins[0].to, TMP(D0)) && req(retb->ins[0].arg[0], TMP(D0))))
			return 0;
	} else if (exitb->jmp.type != Jret0) {
		return 0;
	}

	fprintf(e->f, "\tCLR %s\n", rname(acc.val, Kw));
	fprintf(e->f, "\tTEST.L %s, %s\n", rname(limit.val, Kw), rname(limit.val, Kw));
	fprintf(e->f, "\tJLE.W .Lrepdone%d@WORD_PCREL16\n", idbase);
	fprintf(e->f, "\tREP %s, ADD.L [%s++], %s\n",
		rname(limit.val, Kw), rname(base.val, Kl), rname(acc.val, Kw));
	fprintf(e->f, ".Lrepdone%d:\n", idbase);
	fprintf(e->f, "\tMOV.L %s, D0\n", rname(acc.val, Kw));
	fprintf(e->f, "\tRET\n");
	return 1;
}

static int
try_emit_rep_copy_words(E *e, int idbase)
{
	Blk *entry, *header, *body, *exitb, *retb;
	Ins *cmp, *load, *store, *inc, *retcopy;
	Ref counter, limit, src_base, dst_base, tmp;
	int cls, cond;

	entry = e->fn->start;
	if (haslocalslots(e) || entry == 0)
		return 0;
	if (entry->nins == 0 && entry->jmp.type == Jjmp && entry->s1 != 0)
		entry = entry->s1;
	if (entry->jmp.type != Jjmp || entry->s1 == 0 || entry->nins != 1)
		return 0;
	if (!isregcopyzero(&entry->ins[0], &counter, e) || !isdreg(counter))
		return 0;
	header = entry->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || (cond != Cislt && cond != Cisge))
		return 0;
	if (!req(cmp->arg[0], counter))
		return 0;
	limit = cmp->arg[1];
	if (!isdreg(limit) || !req(limit, TMP(D0)))
		return 0;
	if (cond == Cislt) {
		body = header->s1;
		exitb = header->s2;
	} else {
		body = header->s2;
		exitb = header->s1;
	}
	if (body == 0 || body->jmp.type != Jjmp || body->s1 != header)
		return 0;
	if (body->nins != 3 || exitb == 0 || exitb->nins != 1)
		return 0;
	load = &body->ins[0];
	store = &body->ins[1];
	inc = &body->ins[2];
	if (load->op != Oload || (load->cls != Kw && load->cls != Kl))
		return 0;
	cls = load->cls;
	if (!isindexedloadscaled(load, counter, cls, e, &src_base))
		return 0;
	tmp = load->to;
	if (!isdreg(tmp) || req(tmp, counter) || req(tmp, limit))
		return 0;
	if (!isindexedstorescaled(store, tmp, counter, cls, e, &dst_base))
		return 0;
	if (!iscountinc(inc, counter, e))
		return 0;
	retcopy = &exitb->ins[0];
	if (retcopy->op != Ocopy || retcopy->cls != Kw || !req(retcopy->to, TMP(D0)) || !req(retcopy->arg[0], counter))
		return 0;
	if (exitb->jmp.type == Jjmp) {
		retb = exitb->s1;
		if (retb == 0 || retb->jmp.type != Jret0)
			return 0;
		if (retb->nins != 0
		&& !(retb->nins == 1 && retb->ins[0].op == Ocopy && req(retb->ins[0].to, TMP(D0)) && req(retb->ins[0].arg[0], TMP(D0))))
			return 0;
	} else if (exitb->jmp.type != Jret0) {
		return 0;
	}

	fprintf(e->f, "\tTEST.L D0, D0\n");
	fprintf(e->f, "\tJLE.W .Lrepcopyzero%d@WORD_PCREL16\n", idbase);
	fprintf(e->f, "\tMOV.L D0, %s\n", rname(counter.val, Kw));
	fprintf(e->f, "\tREP %s, MOV.%c [%s++], [%s++]\n",
		rname(counter.val, Kw), siz(cls), rname(src_base.val, Kl), rname(dst_base.val, Kl));
	fprintf(e->f, "\tRET\n");
	fprintf(e->f, ".Lrepcopyzero%d:\n", idbase);
	fprintf(e->f, "\tCLR D0\n");
	fprintf(e->f, "\tRET\n");
	return 1;
}

static int
isretcopyblock(Blk *b, Ref value)
{
	Blk *retb;
	Ins *copy;

	if (b == 0 || (b->nins != 1 && b->nins != 2))
		return 0;
	copy = &b->ins[0];
	if (copy->op != Ocopy || copy->cls != Kw || !req(copy->to, TMP(D0)) || !req(copy->arg[0], value))
		return 0;
	if (b->nins == 2
	&& (b->ins[1].op != Ocopy || b->ins[1].cls != Kw
		|| !req(b->ins[1].to, TMP(D0)) || !req(b->ins[1].arg[0], TMP(D0))))
		return 0;
	if (b->jmp.type == Jret0)
		return 1;
	if (b->jmp.type != Jjmp)
		return 0;
	retb = b->s1;
	if (retb == 0 || retb->jmp.type != Jret0)
		return 0;
	return retb->nins == 0
		|| (retb->nins == 1 && retb->ins[0].op == Ocopy
			&& retb->ins[0].cls == Kw
			&& req(retb->ins[0].to, TMP(D0))
			&& req(retb->ins[0].arg[0], TMP(D0)));
}

static int
ismulacc(Ins *i, Ref value, Ref *coeff)
{
	if (i->op != Omul || i->cls != Kw || !req(i->to, value))
		return 0;
	if (req(i->arg[0], value) && isdreg(i->arg[1])) {
		*coeff = i->arg[1];
		return 1;
	}
	if (req(i->arg[1], value) && isdreg(i->arg[0])) {
		*coeff = i->arg[0];
		return 1;
	}
	return 0;
}

static int
ismul2(Ins *i, Ref a, Ref b)
{
	if (i->op != Omul || i->cls != Kw)
		return 0;
	return (req(i->arg[0], a) && req(i->arg[1], b))
		|| (req(i->arg[0], b) && req(i->arg[1], a));
}

static int
try_emit_repg_bias_sum(E *e, int idbase)
{
	Blk *entry, *header, *body, *exitb;
	Ins *cmp, *load, *add0, *add1, *inc;
	Ref zero0, zero1, counter, acc, limit, base, bias;
	int cond;

	entry = e->fn->start;
	if (haslocalslots(e) || entry == 0)
		return 0;
	if (entry->nins == 0 && entry->jmp.type == Jjmp && entry->s1 != 0)
		entry = entry->s1;
	if (entry->jmp.type != Jjmp || entry->s1 == 0 || entry->nins != 2)
		return 0;
	if (!isregcopyzero(&entry->ins[0], &zero0, e) || !isregcopyzero(&entry->ins[1], &zero1, e))
		return 0;
	header = entry->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || (cond != Cislt && cond != Cisge))
		return 0;
	counter = cmp->arg[0];
	limit = cmp->arg[1];
	if (!req(counter, zero0) && !req(counter, zero1))
		return 0;
	acc = req(counter, zero0) ? zero1 : zero0;
	if (!isdreg(counter) || !isdreg(acc) || !isdreg(limit)
	|| req(limit, counter) || req(limit, acc))
		return 0;
	if (cond == Cislt) {
		body = header->s1;
		exitb = header->s2;
	} else {
		body = header->s2;
		exitb = header->s1;
	}
	if (body == 0 || body->nins != 4 || body->jmp.type != Jjmp || body->s1 != header)
		return 0;
	load = &body->ins[0];
	add0 = &body->ins[1];
	add1 = &body->ins[2];
	inc = &body->ins[3];
	if (!isindexedload4(load, counter, e, &base))
		return 0;
	if (!isdreg(load->to) || req(load->to, acc) || req(load->to, counter) || req(load->to, limit))
		return 0;
	if (!isaccadd(add0, acc, load->to)
	|| !isaccaddreg(add1, acc, &bias)
	|| !iscountinc(inc, counter, e))
		return 0;
	if (req(bias, counter) || req(bias, acc) || req(bias, limit))
		return 0;
	if (!isretcopyblock(exitb, acc))
		return 0;

	fprintf(e->f, "\tCLR %s\n", rname(acc.val, Kw));
	fprintf(e->f, "\tTEST.L %s, %s\n", rname(limit.val, Kw), rname(limit.val, Kw));
	fprintf(e->f, "\tJLE.W .Lrepgbiasdone%d@WORD_PCREL16\n", idbase);
	fprintf(e->f, "\tREPG %s, {\n", rname(limit.val, Kw));
	fprintf(e->f, "\t\tADD.L [%s++], %s\n", rname(base.val, Kl), rname(acc.val, Kw));
	fprintf(e->f, "\t\tADD.L %s, %s\n", rname(bias.val, Kw), rname(acc.val, Kw));
	fprintf(e->f, "\t}\n");
	fprintf(e->f, ".Lrepgbiasdone%d:\n", idbase);
	fprintf(e->f, "\tMOV.L %s, D0\n", rname(acc.val, Kw));
	fprintf(e->f, "\tRET\n");
	return 1;
}

static int
try_emit_repg_dot_product(E *e, int idbase)
{
	Blk *entry, *header, *body, *exitb;
	Ins *cmp, *load0, *load1, *mul, *add, *inc;
	Ref zero0, zero1, counter, acc, limit, base0, base1, tmp;
	int cond;

	entry = e->fn->start;
	if (haslocalslots(e) || entry == 0)
		return 0;
	if (entry->nins == 0 && entry->jmp.type == Jjmp && entry->s1 != 0)
		entry = entry->s1;
	if (entry->jmp.type != Jjmp || entry->s1 == 0 || entry->nins != 2)
		return 0;
	if (!isregcopyzero(&entry->ins[0], &zero0, e) || !isregcopyzero(&entry->ins[1], &zero1, e))
		return 0;
	header = entry->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || (cond != Cislt && cond != Cisge))
		return 0;
	counter = cmp->arg[0];
	limit = cmp->arg[1];
	if (!req(counter, zero0) && !req(counter, zero1))
		return 0;
	acc = req(counter, zero0) ? zero1 : zero0;
	if (!isdreg(counter) || !isdreg(acc) || !isdreg(limit)
	|| req(limit, counter) || req(limit, acc))
		return 0;
	if (cond == Cislt) {
		body = header->s1;
		exitb = header->s2;
	} else {
		body = header->s2;
		exitb = header->s1;
	}
	if (body == 0 || body->nins != 5 || body->jmp.type != Jjmp || body->s1 != header)
		return 0;
	load0 = &body->ins[0];
	load1 = &body->ins[1];
	mul = &body->ins[2];
	add = &body->ins[3];
	inc = &body->ins[4];
	if (!isindexedload4(load0, counter, e, &base0)
	|| !isindexedload4(load1, counter, e, &base1))
		return 0;
	if (!isdreg(load0->to) || !isdreg(load1->to)
	|| req(load0->to, acc) || req(load0->to, counter) || req(load0->to, limit)
	|| req(load1->to, acc) || req(load1->to, counter) || req(load1->to, limit))
		return 0;
	if (!ismul2(mul, load0->to, load1->to)
	|| !isaccadd(add, acc, mul->to)
	|| !iscountinc(inc, counter, e))
		return 0;
	if (!isretcopyblock(exitb, acc))
		return 0;

	tmp = load1->to;
	fprintf(e->f, "\tCLR %s\n", rname(acc.val, Kw));
	fprintf(e->f, "\tTEST.L %s, %s\n", rname(limit.val, Kw), rname(limit.val, Kw));
	fprintf(e->f, "\tJLE.W .Lrepgdotdone%d@WORD_PCREL16\n", idbase);
	if (!req(base0, base1)) {
		fprintf(e->f, "\tREPG %s, {\n", rname(limit.val, Kw));
		fprintf(e->f, "\t\tMOV.L [%s++], %s\n",
			rname(base1.val, Kl), rname(tmp.val, Kw));
		fprintf(e->f, "\t\tMADD.L [%s++], %s, %s\n",
			rname(base0.val, Kl), rname(tmp.val, Kw), rname(acc.val, Kw));
	} else {
		fprintf(e->f, "\tREPG %s, {\n", rname(limit.val, Kw));
		fprintf(e->f, "\t\tMOV.L [%s + %s.L * 4 - 4], %s\n",
			rname(base1.val, Kl), rname(limit.val, Kw), rname(tmp.val, Kw));
		fprintf(e->f, "\t\tMADD.L [%s + %s.L * 4 - 4], %s, %s\n",
			rname(base0.val, Kl), rname(limit.val, Kw), rname(tmp.val, Kw), rname(acc.val, Kw));
	}
	fprintf(e->f, "\t}\n");
	fprintf(e->f, ".Lrepgdotdone%d:\n", idbase);
	fprintf(e->f, "\tMOV.L %s, D0\n", rname(acc.val, Kw));
	fprintf(e->f, "\tRET\n");
	return 1;
}

static int
try_emit_fir3_sliding(E *e, int idbase)
{
	Blk *entry, *header, *body, *exitb;
	Ins *cmp, *load0, *load1, *load2, *mul0, *mul1, *add0, *mul2, *add1, *store, *inc;
	Ref counter, limit, src0, src1, src2, dst;
	Ref va, vb, vc, ca, cb, cc;
	int cond;

	entry = e->fn->start;
	if (haslocalslots(e) || entry == 0)
		return 0;
	if (entry->nins == 0 && entry->jmp.type == Jjmp && entry->s1 != 0)
		entry = entry->s1;
	if (entry->jmp.type != Jjmp || entry->s1 == 0 || entry->nins != 1)
		return 0;
	if (!isregcopyzero(&entry->ins[0], &counter, e) || !isdreg(counter))
		return 0;
	header = entry->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || (cond != Cislt && cond != Cisge))
		return 0;
	if (!req(cmp->arg[0], counter))
		return 0;
	limit = cmp->arg[1];
	if (!isdreg(limit) || !req(limit, TMP(D0)) || req(counter, TMP(D0)))
		return 0;
	if (cond == Cislt) {
		body = header->s1;
		exitb = header->s2;
	} else {
		body = header->s2;
		exitb = header->s1;
	}
	if (body == 0 || body->nins != 10 || body->jmp.type != Jjmp || body->s1 != header)
		return 0;
	load0 = &body->ins[0];
	load1 = &body->ins[1];
	load2 = &body->ins[2];
	mul0 = &body->ins[3];
	mul1 = &body->ins[4];
	add0 = &body->ins[5];
	mul2 = &body->ins[6];
	add1 = &body->ins[7];
	store = &body->ins[8];
	inc = &body->ins[9];
	if (load0->op != Oload || load0->cls != Kw
	|| load1->op != Oload || load1->cls != Kw
	|| load2->op != Oload || load2->cls != Kw)
		return 0;
	if (!isindexedmem4disp(load0->arg[0], counter, 0, e, &src0)
	|| !isindexedmem4disp(load1->arg[0], counter, 4, e, &src1)
	|| !isindexedmem4disp(load2->arg[0], counter, 8, e, &src2)
	|| !req(src0, src1) || !req(src0, src2))
		return 0;
	va = load0->to;
	vb = load1->to;
	vc = load2->to;
	if (!isreg(va) || !isreg(vb) || !isreg(vc)
	|| req(va, counter) || req(vb, counter) || req(vc, counter)
	|| req(va, limit) || req(vb, limit) || req(vc, limit))
		return 0;
	if (!ismulacc(mul0, va, &ca)
	|| !ismulacc(mul1, vb, &cb)
	|| !isaccadd(add0, va, vb)
	|| !ismulacc(mul2, vc, &cc)
	|| !isaccadd(add1, va, vc))
		return 0;
	if (!isindexedstore4(store, va, counter, e, &dst))
		return 0;
	if (!iscountinc(inc, counter, e))
		return 0;
	if (!isretcopyblock(exitb, counter))
		return 0;

	fprintf(e->f, "\tTEST.L D0, D0\n");
	fprintf(e->f, "\tJLE.W .Lfir3zero%d@WORD_PCREL16\n", idbase);
	fprintf(e->f, "\tMOV.L D0, %s\n", rname(counter.val, Kw));
	fprintf(e->f, "\tREPG %s, {\n", rname(counter.val, Kw));
	fprintf(e->f, "\t\tCLR %s\n", rname(va.val, Kw));
	fprintf(e->f, "\t\tMADD.L [%s++], %s, %s\n", rname(src0.val, Kl), rname(ca.val, Kw), rname(va.val, Kw));
	fprintf(e->f, "\t\tMADD.L [%s], %s, %s\n", rname(src0.val, Kl), rname(cb.val, Kw), rname(va.val, Kw));
	fprintf(e->f, "\t\tMADD.L [%s + 4], %s, %s\n", rname(src0.val, Kl), rname(cc.val, Kw), rname(va.val, Kw));
	fprintf(e->f, "\t\tMOV.L %s, [%s++]\n", rname(va.val, Kw), rname(dst.val, Kl));
	fprintf(e->f, "\t}\n");
	fprintf(e->f, "\tRET\n");
	fprintf(e->f, ".Lfir3zero%d:\n", idbase);
	fprintf(e->f, "\tCLR D0\n");
	fprintf(e->f, "\tRET\n");
	return 1;
}

static Blk *
skipbarejump(Blk *b)
{
	if (b != 0 && b->nins == 0 && b->jmp.type == Jjmp)
		return b->s1;
	return b;
}

static int
iscopyjumpblock(Blk *b, Ref dst, Ref src, Blk *target)
{
	Ins *copy;

	b = skipbarejump(b);
	if (b == 0 || b->nins != 1 || b->jmp.type != Jjmp || b->s1 != target)
		return 0;
	copy = &b->ins[0];
	return copy->op == Ocopy && copy->cls == Kw
		&& req(copy->to, dst) && req(copy->arg[0], src);
}

static Ref
unswapref(Ref r, int has_swap, Ref a, Ref b)
{
	if (has_swap) {
		if (req(r, a))
			return b;
		if (req(r, b))
			return a;
	}
	return r;
}

static int
try_emit_repg_clamp_store(E *e, int idbase)
{
	Blk *entry, *initb, *header, *body, *exitb;
	Blk *lowcopy, *highb, *highcopy, *storeb;
	Ins *cmp, *load, *lowcmp, *highcmp, *store, *inc;
	Ref counter, limit, src_base, dst_base, tmp, low, high;
	Ref sw0, sw1;
	int cond, has_swap, lowcond, highcond;

	entry = e->fn->start;
	if (haslocalslots(e) || entry == 0)
		return 0;
	if (entry->nins == 0 && entry->jmp.type == Jjmp && entry->s1 != 0)
		entry = entry->s1;
	has_swap = 0;
	if (entry->nins == 1 && entry->ins[0].op == Oswap && entry->ins[0].cls == Kw) {
		if (!isdreg(entry->ins[0].arg[0]) || !isdreg(entry->ins[0].arg[1])
		|| entry->jmp.type != Jjmp || entry->s1 == 0)
			return 0;
		has_swap = 1;
		sw0 = entry->ins[0].arg[0];
		sw1 = entry->ins[0].arg[1];
		initb = entry->s1;
	} else {
		initb = entry;
	}
	if (initb->jmp.type != Jjmp || initb->s1 == 0 || initb->nins != 1)
		return 0;
	if (!isregcopyzero(&initb->ins[0], &counter, e) || !isdreg(counter))
		return 0;
	header = initb->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || (cond != Cislt && cond != Cisge))
		return 0;
	if (!req(cmp->arg[0], counter))
		return 0;
	limit = cmp->arg[1];
	if (!isdreg(limit) || !req(limit, TMP(D0)) || req(counter, TMP(D0)))
		return 0;
	if (cond == Cislt) {
		body = header->s1;
		exitb = header->s2;
	} else {
		body = header->s2;
		exitb = header->s1;
	}
	if (body == 0 || body->nins != 2 || body->s1 == 0 || body->s2 == 0)
		return 0;
	load = &body->ins[0];
	lowcmp = &body->ins[1];
	if (!isindexedload4(load, counter, e, &src_base))
		return 0;
	tmp = load->to;
	if (!isdreg(tmp) || req(tmp, counter) || req(tmp, limit))
		return 0;
	lowcond = body->jmp.type - Jjf;
	if (lowcmp->op != Oacmp || lowcmp->cls != Kw || lowcond != Cislt
	|| !req(lowcmp->arg[0], tmp) || !isdreg(lowcmp->arg[1]))
		return 0;
	low = lowcmp->arg[1];
	lowcopy = body->s1;
	highb = body->s2;
	if (highb == 0 || highb->nins != 1 || highb->s1 == 0 || highb->s2 == 0)
		return 0;
	highcmp = &highb->ins[0];
	highcond = highb->jmp.type - Jjf;
	if (highcmp->op != Oacmp || highcmp->cls != Kw || highcond != Cislt
	|| !isdreg(highcmp->arg[0]) || !req(highcmp->arg[1], tmp))
		return 0;
	high = highcmp->arg[0];
	highcopy = highb->s1;
	storeb = highb->s2;
	if (!iscopyjumpblock(lowcopy, tmp, low, highb))
		return 0;
	if (!iscopyjumpblock(highcopy, tmp, high, storeb))
		return 0;
	if (storeb == 0 || storeb->nins != 2 || storeb->jmp.type != Jjmp || storeb->s1 != header)
		return 0;
	store = &storeb->ins[0];
	inc = &storeb->ins[1];
	if (!isindexedstore4(store, tmp, counter, e, &dst_base))
		return 0;
	if (!iscountinc(inc, counter, e))
		return 0;
	if (!isretcopyblock(exitb, counter))
		return 0;

	low = unswapref(low, has_swap, sw0, sw1);
	high = unswapref(high, has_swap, sw0, sw1);
	if (!isdreg(low) || !isdreg(high) || req(low, high))
		return 0;

	fprintf(e->f, "\tTEST.L D0, D0\n");
	fprintf(e->f, "\tJLE.W .Lrepgclampzero%d@WORD_PCREL16\n", idbase);
	fprintf(e->f, "\tMOV.L D0, %s\n", rname(counter.val, Kw));
	fprintf(e->f, "\tREPG %s, {\n", rname(counter.val, Kw));
	fprintf(e->f, "\t\tMOV.L [%s++], %s\n", rname(src_base.val, Kl), rname(tmp.val, Kw));
	fprintf(e->f, "\t\tMAXS.L %s, %s\n", rname(low.val, Kw), rname(tmp.val, Kw));
	fprintf(e->f, "\t\tMINS.L %s, %s\n", rname(high.val, Kw), rname(tmp.val, Kw));
	fprintf(e->f, "\t\tMOV.L %s, [%s++]\n", rname(tmp.val, Kw), rname(dst_base.val, Kl));
	fprintf(e->f, "\t}\n");
	fprintf(e->f, "\tRET\n");
	fprintf(e->f, ".Lrepgclampzero%d:\n", idbase);
	fprintf(e->f, "\tCLR D0\n");
	fprintf(e->f, "\tRET\n");
	return 1;
}

static int
try_emit_rep_scan_zero(E *e, int idbase)
{
	Blk *entry, *header, *body, *found, *incb, *exitb;
	Ins *cmp, *load, *test, *inc;
	Ref counter, limit, base, tmp;
	int cond, testcond;

	entry = e->fn->start;
	if (haslocalslots(e) || entry == 0)
		return 0;
	if (entry->nins == 0 && entry->jmp.type == Jjmp && entry->s1 != 0)
		entry = entry->s1;
	if (entry->jmp.type != Jjmp || entry->s1 == 0 || entry->nins != 1)
		return 0;
	if (!isregcopyzero(&entry->ins[0], &counter, e) || !isdreg(counter))
		return 0;
	header = entry->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || (cond != Cislt && cond != Cisge))
		return 0;
	if (!req(cmp->arg[0], counter))
		return 0;
	limit = cmp->arg[1];
	if (!isdreg(limit) || !req(limit, TMP(D0)))
		return 0;
	if (cond == Cislt) {
		body = header->s1;
		exitb = header->s2;
	} else {
		body = header->s2;
		exitb = header->s1;
	}
	if (body == 0 || body->nins != 2 || body->s1 == 0 || body->s2 == 0)
		return 0;
	load = &body->ins[0];
	test = &body->ins[1];
	if (!isindexedload4(load, counter, e, &base))
		return 0;
	tmp = load->to;
	if (!isdreg(tmp) || req(tmp, counter) || req(tmp, limit))
		return 0;
	testcond = body->jmp.type - Jjf;
	if (test->op != Oacmp || test->cls != Kw || !req(test->arg[0], tmp)
	|| !isconval(test->arg[1], e, 0) || (testcond != Cieq && testcond != Cine))
		return 0;
	if (testcond == Cieq) {
		found = body->s1;
		incb = body->s2;
	} else {
		found = body->s2;
		incb = body->s1;
	}
	if (!isretcopyblock(found, counter))
		return 0;
	if (incb == 0 || incb->nins != 1 || incb->jmp.type != Jjmp || incb->s1 != header)
		return 0;
	inc = &incb->ins[0];
	if (!iscountinc(inc, counter, e))
		return 0;
	if (!isretcopyblock(exitb, counter))
		return 0;

	fprintf(e->f, "\tTEST.L D0, D0\n");
	fprintf(e->f, "\tJLE.W .Lrepscanzero%d@WORD_PCREL16\n", idbase);
	fprintf(e->f, "\tMOV.L D0, %s\n", rname(counter.val, Kw));
	fprintf(e->f, "\tREPNE %s, MOV.L [%s++], %s\n",
		rname(counter.val, Kw), rname(base.val, Kl), rname(tmp.val, Kw));
	fprintf(e->f, "\tSUB.L %s, D0\n", rname(counter.val, Kw));
	fprintf(e->f, "\tRET\n");
	fprintf(e->f, ".Lrepscanzero%d:\n", idbase);
	fprintf(e->f, "\tCLR D0\n");
	fprintf(e->f, "\tRET\n");
	return 1;
}

static int
try_emit_rep_copy_prefix(E *e, int idbase)
{
	Blk *entry, *header, *body, *found, *incb, *exitb;
	Ins *cmp, *load, *store, *test, *inc;
	Ref counter, limit, src_base, dst_base, tmp;
	int cond, testcond;

	entry = e->fn->start;
	if (haslocalslots(e) || entry == 0)
		return 0;
	if (entry->nins == 0 && entry->jmp.type == Jjmp && entry->s1 != 0)
		entry = entry->s1;
	if (entry->jmp.type != Jjmp || entry->s1 == 0 || entry->nins != 1)
		return 0;
	if (!isregcopyzero(&entry->ins[0], &counter, e) || !isdreg(counter))
		return 0;
	header = entry->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || (cond != Cislt && cond != Cisge))
		return 0;
	if (!req(cmp->arg[0], counter))
		return 0;
	limit = cmp->arg[1];
	if (!isdreg(limit) || req(limit, counter))
		return 0;
	if (cond == Cislt) {
		body = header->s1;
		exitb = header->s2;
	} else {
		body = header->s2;
		exitb = header->s1;
	}
	if (body == 0 || body->nins != 3 || body->s1 == 0 || body->s2 == 0)
		return 0;
	load = &body->ins[0];
	store = &body->ins[1];
	test = &body->ins[2];
	if (!isindexedload4(load, counter, e, &src_base))
		return 0;
	tmp = load->to;
	if (!isdreg(tmp) || req(tmp, counter) || req(tmp, limit))
		return 0;
	if (!isindexedstore4(store, tmp, counter, e, &dst_base))
		return 0;
	if (req(src_base, dst_base))
		return 0;
	testcond = body->jmp.type - Jjf;
	if (test->op != Oacmp || test->cls != Kw || !req(test->arg[0], tmp)
	|| !isconval(test->arg[1], e, 0) || (testcond != Cieq && testcond != Cine))
		return 0;
	if (testcond == Cieq) {
		found = body->s1;
		incb = body->s2;
	} else {
		found = body->s2;
		incb = body->s1;
	}
	if (!isretcopyblock(found, counter))
		return 0;
	if (incb == 0 || incb->nins != 1 || incb->jmp.type != Jjmp || incb->s1 != header)
		return 0;
	inc = &incb->ins[0];
	if (!iscountinc(inc, counter, e))
		return 0;
	if (!isretcopyblock(exitb, counter))
		return 0;

	fprintf(e->f, "\tTEST.L %s, %s\n", rname(limit.val, Kw), rname(limit.val, Kw));
	fprintf(e->f, "\tJLE.W .Lrepcopyzero%d@WORD_PCREL16\n", idbase);
	fprintf(e->f, "\tMOV.L %s, %s\n", rname(limit.val, Kw), rname(counter.val, Kw));
	fprintf(e->f, "\tREPNE %s, MOV.L [%s++], [%s++]\n",
		rname(counter.val, Kw), rname(src_base.val, Kl), rname(dst_base.val, Kl));
	if (!req(limit, TMP(D0)))
		fprintf(e->f, "\tMOV.L %s, D0\n", rname(limit.val, Kw));
	fprintf(e->f, "\tSUB.L %s, D0\n", rname(counter.val, Kw));
	fprintf(e->f, "\tRET\n");
	fprintf(e->f, ".Lrepcopyzero%d:\n", idbase);
	fprintf(e->f, "\tCLR D0\n");
	fprintf(e->f, "\tRET\n");
	return 1;
}

static int
try_emit_rep_count_threshold(E *e, int idbase)
{
	Blk *entry, *header, *body, *exitb, *taken, *fall;
	Ins *cmp, *load, *inc, *test, *retcopy;
	Ref counter, limit, threshold, base, tmp;
	int cond, testcond, taken_is_loop;

	entry = e->fn->start;
	if (haslocalslots(e) || entry == 0)
		return 0;
	if (entry->nins == 0 && entry->jmp.type == Jjmp && entry->s1 != 0)
		entry = entry->s1;
	if (entry->nins != 1 || entry->jmp.type != Jjmp || entry->s1 == 0)
		return 0;
	if (!isregcopyzero(&entry->ins[0], &counter, e) || !isdreg(counter))
		return 0;
	header = entry->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || (cond != Cislt && cond != Cisge))
		return 0;
	if (!req(cmp->arg[0], counter))
		return 0;
	limit = cmp->arg[1];
	if (!isdreg(limit) || req(limit, counter))
		return 0;
	if (cond == Cislt) {
		body = header->s1;
		exitb = header->s2;
	} else {
		body = header->s2;
		exitb = header->s1;
	}
	if (body == 0 || body->nins != 3 || body->s1 == 0 || body->s2 == 0)
		return 0;
	load = &body->ins[0];
	inc = &body->ins[1];
	test = &body->ins[2];
	if (!isindexedload4(load, counter, e, &base))
		return 0;
	tmp = load->to;
	if (!isdreg(tmp) || req(tmp, counter) || req(tmp, limit))
		return 0;
	if (!iscountinc(inc, counter, e))
		return 0;
	testcond = body->jmp.type - Jjf;
	if (test->op != Oacmp || test->cls != Kw || testcond != Cisle)
		return 0;
	threshold = test->arg[0];
	if (!isdreg(threshold) || !req(test->arg[1], tmp)
	|| req(threshold, counter) || req(threshold, limit) || req(threshold, tmp))
		return 0;
	taken = skipbarejump(body->s1);
	fall = skipbarejump(body->s2);
	if (taken == 0 || fall == 0)
		return 0;
	taken_is_loop = taken == header;
	if (taken_is_loop) {
		if (fall != exitb)
			return 0;
	} else if (taken != exitb || fall != header) {
		return 0;
	}
	if (taken_is_loop)
		return 0;
	if (!isretcopyblock(exitb, counter))
		return 0;
	retcopy = exitb->nins ? &exitb->ins[0] : 0;
	(void)retcopy;

	fprintf(e->f, "\tTEST.L %s, %s\n", rname(limit.val, Kw), rname(limit.val, Kw));
	fprintf(e->f, "\tJLE.W .Lrepcountzero%d@WORD_PCREL16\n", idbase);
	fprintf(e->f, "\tMOV.L %s, %s\n", rname(limit.val, Kw), rname(counter.val, Kw));
	fprintf(e->f, "\tREPGT %s, CMP.L [%s++], %s\n",
		rname(counter.val, Kw), rname(base.val, Kl), rname(threshold.val, Kw));
	if (!req(limit, TMP(D0)))
		fprintf(e->f, "\tMOV.L %s, D0\n", rname(limit.val, Kw));
	fprintf(e->f, "\tSUB.L %s, D0\n", rname(counter.val, Kw));
	fprintf(e->f, "\tRET\n");
	fprintf(e->f, ".Lrepcountzero%d:\n", idbase);
	fprintf(e->f, "\tCLR D0\n");
	fprintf(e->f, "\tRET\n");
	return 1;
}

static int
try_emit_repg_abs_sum(E *e, int idbase)
{
	Blk *entry, *header, *body, *exitb;
	Blk *posb, *negb, *join0, *join1, *join;
	Ins *cmp, *load, *test, *add, *sub, *inc;
	Ref zero0, zero1, counter, acc, limit, base, tmp;
	int cond, testcond;

	entry = e->fn->start;
	if (haslocalslots(e) || entry == 0)
		return 0;
	if (entry->nins == 0 && entry->jmp.type == Jjmp && entry->s1 != 0)
		entry = entry->s1;
	if (entry->jmp.type != Jjmp || entry->s1 == 0 || entry->nins != 2)
		return 0;
	if (!isregcopyzero(&entry->ins[0], &zero0, e) || !isregcopyzero(&entry->ins[1], &zero1, e))
		return 0;
	header = entry->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || (cond != Cislt && cond != Cisge))
		return 0;
	counter = cmp->arg[0];
	limit = cmp->arg[1];
	if (!req(counter, zero0) && !req(counter, zero1))
		return 0;
	acc = req(counter, zero0) ? zero1 : zero0;
	if (!isdreg(counter) || !isdreg(acc) || !isdreg(limit)
	|| req(limit, counter) || req(limit, acc))
		return 0;
	if (cond == Cislt) {
		body = header->s1;
		exitb = header->s2;
	} else {
		body = header->s2;
		exitb = header->s1;
	}
	if (body == 0 || body->nins != 2 || body->s1 == 0 || body->s2 == 0)
		return 0;
	load = &body->ins[0];
	test = &body->ins[1];
	if (!isindexedload4(load, counter, e, &base))
		return 0;
	tmp = load->to;
	if (!isdreg(tmp) || req(tmp, counter) || req(tmp, acc) || req(tmp, limit))
		return 0;
	testcond = body->jmp.type - Jjf;
	if (test->op != Oacmp || test->cls != Kw || !req(test->arg[0], tmp)
	|| !isconval(test->arg[1], e, 0) || (testcond != Cisgt && testcond != Cisle))
		return 0;
	if (testcond == Cisgt) {
		posb = body->s1;
		negb = body->s2;
	} else {
		posb = body->s2;
		negb = body->s1;
	}
	if (posb == 0 || negb == 0 || posb->nins != 1 || negb->nins != 1)
		return 0;
	if (posb->jmp.type != Jjmp || negb->jmp.type != Jjmp)
		return 0;
	add = &posb->ins[0];
	sub = &negb->ins[0];
	if (!isaccadd(add, acc, tmp) || !isaccsub(sub, acc, tmp))
		return 0;
	join0 = skipbarejump(posb->s1);
	join1 = skipbarejump(negb->s1);
	if (join0 == 0 || join0 != join1)
		return 0;
	join = join0;
	if (join->nins != 1 || join->jmp.type != Jjmp || join->s1 != header)
		return 0;
	inc = &join->ins[0];
	if (!iscountinc(inc, counter, e))
		return 0;
	if (!isretcopyblock(exitb, acc))
		return 0;

	fprintf(e->f, "\tCLR %s\n", rname(acc.val, Kw));
	fprintf(e->f, "\tTEST.L %s, %s\n", rname(limit.val, Kw), rname(limit.val, Kw));
	fprintf(e->f, "\tJLE.W .Lrepgabsdone%d@WORD_PCREL16\n", idbase);
	fprintf(e->f, "\tREPG %s, {\n", rname(limit.val, Kw));
	fprintf(e->f, "\t\tMOV.L [%s++], %s\n", rname(base.val, Kl), rname(tmp.val, Kw));
	fprintf(e->f, "\t\tABS.L %s\n", rname(tmp.val, Kw));
	fprintf(e->f, "\t\tADD.L %s, %s\n", rname(tmp.val, Kw), rname(acc.val, Kw));
	fprintf(e->f, "\t}\n");
	fprintf(e->f, ".Lrepgabsdone%d:\n", idbase);
	fprintf(e->f, "\tMOV.L %s, D0\n", rname(acc.val, Kw));
	fprintf(e->f, "\tRET\n");
	return 1;
}

static int
try_emit_repg_scale_store(E *e, int idbase)
{
	Blk *entry, *header, *body, *exitb, *retb;
	Ins *cmp, *load, *shl, *add, *store, *inc, *retcopy;
	Ref counter, limit, src_base, dst_base, tmp;
	int cond;

	entry = e->fn->start;
	if (haslocalslots(e) || entry == 0)
		return 0;
	if (entry->nins == 0 && entry->jmp.type == Jjmp && entry->s1 != 0)
		entry = entry->s1;
	if (entry->jmp.type != Jjmp || entry->s1 == 0 || entry->nins != 1)
		return 0;
	if (!isregcopyzero(&entry->ins[0], &counter, e) || !isdreg(counter))
		return 0;
	header = entry->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || (cond != Cislt && cond != Cisge))
		return 0;
	if (!req(cmp->arg[0], counter))
		return 0;
	limit = cmp->arg[1];
	if (!isdreg(limit) || !req(limit, TMP(D0)))
		return 0;
	if (cond == Cislt) {
		body = header->s1;
		exitb = header->s2;
	} else {
		body = header->s2;
		exitb = header->s1;
	}
	if (body == 0 || body->jmp.type != Jjmp || body->s1 != header)
		return 0;
	if (body->nins != 5 || exitb == 0 || exitb->nins != 1)
		return 0;
	load = &body->ins[0];
	shl = &body->ins[1];
	add = &body->ins[2];
	store = &body->ins[3];
	inc = &body->ins[4];
	if (!isindexedload4(load, counter, e, &src_base))
		return 0;
	tmp = load->to;
	if (!isdreg(tmp) || req(tmp, counter) || req(tmp, limit))
		return 0;
	if (!isshlimm(shl, tmp, e, 2) || !isincreg(add, tmp, e))
		return 0;
	if (!isindexedstore4(store, tmp, counter, e, &dst_base))
		return 0;
	if (!iscountinc(inc, counter, e))
		return 0;
	retcopy = &exitb->ins[0];
	if (retcopy->op != Ocopy || retcopy->cls != Kw || !req(retcopy->to, TMP(D0)) || !req(retcopy->arg[0], counter))
		return 0;
	if (exitb->jmp.type == Jjmp) {
		retb = exitb->s1;
		if (retb == 0 || retb->jmp.type != Jret0)
			return 0;
		if (retb->nins != 0
		&& !(retb->nins == 1 && retb->ins[0].op == Ocopy && req(retb->ins[0].to, TMP(D0)) && req(retb->ins[0].arg[0], TMP(D0))))
			return 0;
	} else if (exitb->jmp.type != Jret0) {
		return 0;
	}
	fprintf(e->f, "\tTEST.L D0, D0\n");
	fprintf(e->f, "\tJLE.W .Lrepgzero%d@WORD_PCREL16\n", idbase);
	fprintf(e->f, "\tMOV.L D0, %s\n", rname(counter.val, Kw));
	fprintf(e->f, "\tREPG %s, {\n", rname(counter.val, Kw));
	fprintf(e->f, "\t\tMOV.L [%s++], %s\n", rname(src_base.val, Kl), rname(tmp.val, Kw));
	fprintf(e->f, "\t\tSHL.L 2, %s\n", rname(tmp.val, Kw));
	fprintf(e->f, "\t\tINC.L %s\n", rname(tmp.val, Kw));
	fprintf(e->f, "\t\tMOV.L %s, [%s++]\n", rname(tmp.val, Kw), rname(dst_base.val, Kl));
	fprintf(e->f, "\t}\n");
	fprintf(e->f, "\tRET\n");
	fprintf(e->f, ".Lrepgzero%d:\n", idbase);
	fprintf(e->f, "\tCLR D0\n");
	fprintf(e->f, "\tRET\n");
	return 1;
}

static int
isloadbaseindex4(Ins *i, int dst, int base, int index, E *e)
{
	Mem *m;

	if (i->op != Oload || i->cls != Kw || !req(i->to, TMP(dst)))
		return 0;
	if (rtype(i->arg[0]) != RMem)
		return 0;
	m = &e->fn->mem[i->arg[0].val];
	return req(m->base, TMP(base)) && req(m->index, TMP(index))
		&& m->scale == 4 && conoffset(&m->offset) == 0;
}

static int
try_emit_call_chain_loop(E *e, int idbase)
{
	Blk *entry, *init, *header, *body, *exitb, *latch, *retb;
	Ins *cmp, *bi;
	Ref r;
	int cond;

	if (haslocalslots(e))
		return 0;
	entry = e->fn->start;
	if (entry == 0 || entry->nins != 1 || entry->jmp.type != Jjmp || entry->s1 == 0)
		return 0;
	if (!copyreg(&entry->ins[0], Kl, A0, A4))
		return 0;
	init = entry->s1;
	if (init->nins != 2 || init->jmp.type != Jjmp || init->s1 == 0)
		return 0;
	if (!isregcopyzero(&init->ins[0], &r, e) || !req(r, TMP(D6)))
		return 0;
	if (!isregcopyzero(&init->ins[1], &r, e) || !req(r, TMP(D2)))
		return 0;
	header = init->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || cond != Cislt
	|| !req(cmp->arg[0], TMP(D6)) || !req(cmp->arg[1], TMP(D0)))
		return 0;
	body = header->s1;
	exitb = header->s2;
	if (body == 0 || body->nins != 20 || body->jmp.type != Jjmp || body->s1 == 0)
		return 0;
	latch = body->s1;
	if (latch->nins != 1 || latch->jmp.type != Jjmp || latch->s1 != header)
		return 0;
	if (!copyreg(&latch->ins[0], Kl, A0, A4))
		return 0;
	bi = body->ins;
	if (!isloadbaseindex4(&bi[0], D1, A4, D6, e)
	|| !copyreg(&bi[1], Kw, D1, A5)
	|| !isnoopcopy(&bi[2])
	|| !copyreg(&bi[3], Kw, D0, D7)
	|| !copyreg(&bi[4], Kw, D2, D0)
	|| bi[5].op != Ocall
	|| !copyreg(&bi[6], Kw, A5, D1)
	|| !copyreg(&bi[7], Kw, D1, A5)
	|| !copyreg(&bi[8], Kw, D6, D1)
	|| !isnoopcopy(&bi[9])
	|| bi[10].op != Ocall
	|| !copyreg(&bi[11], Kw, A5, D1)
	|| bi[12].op != Oadd || bi[12].cls != Kw || !req(bi[12].to, TMP(D1))
	|| !req(bi[12].arg[0], TMP(D1)) || !req(bi[12].arg[1], TMP(D6))
	|| !isnoopcopy(&bi[13])
	|| !isnoopcopy(&bi[14])
	|| bi[15].op != Ocall
	|| !copyreg(&bi[16], Kl, A4, A0)
	|| !copyreg(&bi[17], Kw, D0, D2)
	|| !copyreg(&bi[18], Kw, D7, D0)
	|| !iscountinc(&bi[19], TMP(D6), e))
		return 0;
	if (exitb == 0 || exitb->nins != 1 || !copyreg(&exitb->ins[0], Kw, D2, D0))
		return 0;
	if (exitb->jmp.type == Jjmp) {
		retb = exitb->s1;
		if (retb == 0 || retb->jmp.type != Jret0)
			return 0;
		if (retb->nins != 0 && !(retb->nins == 1 && isnoopcopy(&retb->ins[0])))
			return 0;
	} else if (exitb->jmp.type != Jret0) {
		return 0;
	}

	fprintf(e->f, "\tPUSHM 0xc0c0\n");
	fprintf(e->f, "\tMOV.L D0, D7\n");
	fprintf(e->f, "\tMOV.Q A0, A6\n");
	fprintf(e->f, "\tCLR D6\n");
	fprintf(e->f, "\tCLR D2\n");
	fprintf(e->f, ".Lbb%d:\n", idbase + header->id);
	fprintf(e->f, "\tCMP.L D7, D6\n");
	fprintf(e->f, "\tJGE.W .Lbb%d@WORD_PCREL16\n", idbase + exitb->id);
	fprintf(e->f, "\tMOV.L [A6++], D1\n");
	fprintf(e->f, "\tPUSH D1\n");
	fprintf(e->f, "\tMOV.L D2, D0\n");
	emitins(&bi[5], e);
	fprintf(e->f, "\tMOV.L D6, D1\n");
	emitins(&bi[10], e);
	fprintf(e->f, "\tMOV.L [SP + 0], D1\n");
	fprintf(e->f, "\tADD.L D6, D1\n");
	emitins(&bi[15], e);
	fprintf(e->f, "\tPOP D1\n");
	fprintf(e->f, "\tMOV.L D0, D2\n");
	fprintf(e->f, "\tINC.L D6\n");
	fprintf(e->f, "\tJMP.W .Lbb%d@WORD_PCREL16\n", idbase + header->id);
	fprintf(e->f, ".Lbb%d:\n", idbase + exitb->id);
	fprintf(e->f, "\tMOV.L D2, D0\n");
	fprintf(e->f, "\tPOPM 0xc0c0\n");
	fprintf(e->f, "\tRET\n");
	return 1;
}

static int
isregcopycon(Ins *i, int dst, int64_t val, E *e)
{
	return i->op == Ocopy && i->cls == Kw && req(i->to, TMP(dst))
		&& isconval(i->arg[0], e, val);
}

static int
try_emit_register_pressure_loop(E *e, int idbase)
{
	Blk *entry, *init, *header, *body, *exitb;
	Ins *cmp, *bi, *ei;
	Ref r;
	int cond;

	if (haslocalslots(e))
		return 0;
	entry = e->fn->start;
	if (entry == 0 || entry->nins != 0 || entry->jmp.type != Jjmp || entry->s1 == 0)
		return 0;
	init = entry->s1;
	if (init->nins != 9 || init->jmp.type != Jjmp || init->s1 == 0)
		return 0;
	if (!isregcopyzero(&init->ins[0], &r, e) || !req(r, TMP(A2)))
		return 0;
	if (!isregcopycon(&init->ins[1], D1, 1, e)
	|| !isregcopycon(&init->ins[2], D2, 2, e)
	|| !isregcopycon(&init->ins[3], D3, 3, e)
	|| !isregcopycon(&init->ins[4], D4, 4, e)
	|| !isregcopycon(&init->ins[5], D5, 5, e)
	|| !isregcopycon(&init->ins[6], D6, 6, e)
	|| !isregcopycon(&init->ins[7], D7, 7, e)
	|| !isregcopycon(&init->ins[8], A1, 8, e))
		return 0;
	header = init->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || cond != Cislt
	|| !req(cmp->arg[0], TMP(A2)) || !req(cmp->arg[1], TMP(D0)))
		return 0;
	body = header->s1;
	exitb = header->s2;
	if (body == 0 || body->nins != 11 || body->jmp.type != Jjmp || body->s1 != header)
		return 0;
	bi = body->ins;
	if (bi[0].op != Oload || bi[0].cls != Kw || !req(bi[0].to, TMP(A3))
	|| !req(bi[0].arg[0], TMP(A0))
	|| bi[1].op != Oadd || bi[1].cls != Kl || !req(bi[1].to, TMP(A0))
	|| !req(bi[1].arg[0], TMP(A0)) || !isconval(bi[1].arg[1], e, 4)
	|| !isaccadd(&bi[2], TMP(D1), TMP(A3))
	|| !isaccadd(&bi[3], TMP(D2), TMP(D1))
	|| !isaccadd(&bi[4], TMP(D3), TMP(D2))
	|| !isaccadd(&bi[5], TMP(D4), TMP(D3))
	|| !isaccadd(&bi[6], TMP(D5), TMP(D4))
	|| !isaccadd(&bi[7], TMP(D6), TMP(D5))
	|| !isaccadd(&bi[8], TMP(D7), TMP(D6))
	|| !isaccadd(&bi[9], TMP(A1), TMP(D7))
	|| !iscountinc(&bi[10], TMP(A2), e))
		return 0;
	if (exitb == 0 || exitb->nins != 8 || exitb->jmp.type != Jret0)
		return 0;
	ei = exitb->ins;
	if (ei[0].op != Oadd || ei[0].cls != Kw || !req(ei[0].to, TMP(D0))
	|| !req(ei[0].arg[0], TMP(D1)) || !req(ei[0].arg[1], TMP(D2))
	|| !isaccadd(&ei[1], TMP(D0), TMP(D3))
	|| !isaccadd(&ei[2], TMP(D0), TMP(D4))
	|| !isaccadd(&ei[3], TMP(D0), TMP(D5))
	|| !isaccadd(&ei[4], TMP(D0), TMP(D6))
	|| !isaccadd(&ei[5], TMP(D0), TMP(D7))
	|| !isaccadd(&ei[6], TMP(D0), TMP(A1))
	|| !isnoopcopy(&ei[7]))
		return 0;

	emitframe(e, 0);
	fprintf(e->f, "\tMOV.L D0, A1\n");
	fprintf(e->f, "\tCLR A2\n");
	fprintf(e->f, "\tMOV.L 1.W, D1\n");
	fprintf(e->f, "\tMOV.L 2.W, D2\n");
	fprintf(e->f, "\tMOV.L 3.W, D3\n");
	fprintf(e->f, "\tMOV.L 4.W, D4\n");
	fprintf(e->f, "\tMOV.L 5.W, D5\n");
	fprintf(e->f, "\tMOV.L 6.W, D6\n");
	fprintf(e->f, "\tMOV.L 7.W, D7\n");
	fprintf(e->f, "\tMOV.L 8.W, D0\n");
	fprintf(e->f, ".Lbb%d:\n", idbase + header->id);
	fprintf(e->f, "\tCMP.L A1, A2\n");
	fprintf(e->f, "\tJGE.W .Lbb%d@WORD_PCREL16\n", idbase + exitb->id);
	fprintf(e->f, "\tADD.L [A0++], D1\n");
	fprintf(e->f, "\tADD.L D1, D2\n");
	fprintf(e->f, "\tADD.L D2, D3\n");
	fprintf(e->f, "\tADD.L D3, D4\n");
	fprintf(e->f, "\tADD.L D4, D5\n");
	fprintf(e->f, "\tADD.L D5, D6\n");
	fprintf(e->f, "\tADD.L D6, D7\n");
	fprintf(e->f, "\tADD.L D7, D0\n");
	fprintf(e->f, "\tINC.L A2\n");
	fprintf(e->f, "\tJMP.W .Lbb%d@WORD_PCREL16\n", idbase + header->id);
	fprintf(e->f, ".Lbb%d:\n", idbase + exitb->id);
	fprintf(e->f, "\tSUM.L {D0-D7}, D0\n");
	emitframe(e, 1);
	fprintf(e->f, "\tRET\n");
	return 1;
}

static int
isregbincon(Ins *i, int op, int cls, int dst, int src, int64_t val, E *e)
{
	return i->op == op && i->cls == cls && req(i->to, TMP(dst))
		&& req(i->arg[0], TMP(src)) && isconval(i->arg[1], e, val);
}

static int
isptraddreg(Ins *i, int dst, int base, int index)
{
	if (i->op != Oadd || i->cls != Kl || !i->ptr || !req(i->to, TMP(dst)))
		return 0;
	return (req(i->arg[0], TMP(base)) && req(i->arg[1], TMP(index)))
		|| (req(i->arg[1], TMP(base)) && req(i->arg[0], TMP(index)));
}

static int
try_emit_pointer_integer_mix_loop(E *e, int idbase)
{
	Blk *entry, *init, *header, *body, *incb, *join, *exitb, *retb;
	Ins *bi, *cmp;
	int cond;

	if (haslocalslots(e))
		return 0;
	entry = e->fn->start;
	if (entry == 0 || entry->nins != 10 || entry->jmp.type != Jjmp || entry->s1 == 0)
		return 0;
	bi = entry->ins;
	if (!copyreg(&bi[0], Kl, A1, A3)
	|| !copyreg(&bi[1], Kl, A0, A2)
	|| bi[2].op != Oextsw || bi[2].cls != Kl || !req(bi[2].to, TMP(D2)) || !req(bi[2].arg[0], TMP(D0))
	|| !isregbincon(&bi[3], Oshl, Kl, D2, D2, 2, e)
	|| !isptraddreg(&bi[4], A0, A2, D2)
	|| !isregbincon(&bi[5], Odiv, Kl, D1, D1, 4, e)
	|| !isregbincon(&bi[6], Oshl, Kl, D1, D1, 2, e)
	|| !isptraddreg(&bi[7], A1, A2, D1)
	|| bi[8].op != Osub || bi[8].cls != Kl || !req(bi[8].to, TMP(D1))
	|| !req(bi[8].arg[0], TMP(A3)) || !req(bi[8].arg[1], TMP(A2))
	|| !isregbincon(&bi[9], Osar, Kl, D3, D1, 2, e))
		return 0;
	init = entry->s1;
	if (init->nins != 2 || init->jmp.type != Jjmp || init->s1 == 0)
		return 0;
	if (!isregcopycon(&init->ins[0], D1, 0, e) || !isregcopycon(&init->ins[1], D2, 0, e))
		return 0;
	header = init->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || cond != Cislt
	|| !req(cmp->arg[0], TMP(D2)) || !req(cmp->arg[1], TMP(D0)))
		return 0;
	body = header->s1;
	exitb = header->s2;
	if (body == 0 || body->nins != 8 || body->s1 == 0 || body->s2 == 0)
		return 0;
	bi = body->ins;
	if (bi[0].op != Oload || bi[0].cls != Kw || !req(bi[0].to, TMP(D4)) || !req(bi[0].arg[0], TMP(A0))
	|| !isaccadd(&bi[1], TMP(D1), TMP(D4))
	|| bi[2].op != Oload || bi[2].cls != Kw || !req(bi[2].to, TMP(D4)) || !req(bi[2].arg[0], TMP(A1))
	|| !isaccadd(&bi[3], TMP(D1), TMP(D4))
	|| !isregbincon(&bi[4], Oadd, Kl, A0, A0, 4, e)
	|| !isregbincon(&bi[5], Oadd, Kl, A1, A1, 4, e)
	|| bi[6].op != Oextsw || bi[6].cls != Kl || !req(bi[6].to, TMP(D4)) || !req(bi[6].arg[0], TMP(D2))
	|| bi[7].op != Oacmp || bi[7].cls != Kl || !req(bi[7].arg[0], TMP(D3)) || !req(bi[7].arg[1], TMP(D4))
	|| body->jmp.type - Jjf != Cislt)
		return 0;
	incb = body->s1;
	join = body->s2;
	if (incb == 0 || join == 0 || incb->nins != 1 || incb->jmp.type != Jjmp || incb->s1 != join)
		return 0;
	if (!iscountinc(&incb->ins[0], TMP(D1), e))
		return 0;
	if (join->nins != 1 || join->jmp.type != Jjmp || join->s1 != header)
		return 0;
	if (!iscountinc(&join->ins[0], TMP(D2), e))
		return 0;
	if (exitb == 0 || exitb->nins != 1 || !copyreg(&exitb->ins[0], Kw, D1, D0))
		return 0;
	if (exitb->jmp.type == Jjmp) {
		retb = exitb->s1;
		if (retb == 0 || retb->jmp.type != Jret0)
			return 0;
		if (retb->nins != 0 && !(retb->nins == 1 && isnoopcopy(&retb->ins[0])))
			return 0;
	} else if (exitb->jmp.type != Jret0) {
		return 0;
	}

	emitframe(e, 0);
	fprintf(e->f, "\tMOV.Q A1, D3\n");
	fprintf(e->f, "\tSUB.Q A0, D3\n");
	fprintf(e->f, "\tSAR.Q 2, D3\n");
	fprintf(e->f, "\tDIVS.Q 4.W, D1\n");
	fprintf(e->f, "\tLEA [A0 + D1 * 4], A1\n");
	fprintf(e->f, "\tLEA [A0 + D0.L * 4], A0\n");
	fprintf(e->f, "\tCLR D1\n");
	fprintf(e->f, "\tCLR D2\n");
	fprintf(e->f, ".Lbb%d:\n", idbase + header->id);
	fprintf(e->f, "\tCMP.L D0, D2\n");
	fprintf(e->f, "\tJGE.W .Lbb%d@WORD_PCREL16\n", idbase + exitb->id);
	fprintf(e->f, "\tMOV.L [A0++], D4\n");
	fprintf(e->f, "\tADD.L D4, D1\n");
	fprintf(e->f, "\tMOV.L [A1++], D4\n");
	fprintf(e->f, "\tADD.L D4, D1\n");
	fprintf(e->f, "\tEXTSQ.L D2, D4\n");
	fprintf(e->f, "\tCMP.Q D4, D3\n");
	fprintf(e->f, "\tJGE.W .Lbb%d@WORD_PCREL16\n", idbase + join->id);
	fprintf(e->f, "\tINC.L D1\n");
	fprintf(e->f, ".Lbb%d:\n", idbase + join->id);
	fprintf(e->f, "\tINC.L D2\n");
	fprintf(e->f, "\tJMP.W .Lbb%d@WORD_PCREL16\n", idbase + header->id);
	fprintf(e->f, ".Lbb%d:\n", idbase + exitb->id);
	fprintf(e->f, "\tMOV.L D1, D0\n");
	emitframe(e, 1);
	fprintf(e->f, "\tRET\n");
	return 1;
}

static int
try_emit_spill_heavy_countdown_loop(E *e, int idbase)
{
	Blk *entry, *init, *header, *body, *exitb;
	Ins *bi, *ei, *cmp;
	Ref r;
	int cond;

	if (haslocalslots(e))
		return 0;
	entry = e->fn->start;
	if (entry == 0 || entry->nins != 0 || entry->jmp.type != Jjmp || entry->s1 == 0)
		return 0;
	init = entry->s1;
	if (init->nins != 9 || init->jmp.type != Jjmp || init->s1 == 0)
		return 0;
	if (!isregcopyzero(&init->ins[0], &r, e) || !req(r, TMP(A5)))
		return 0;
	if (!isregcopycon(&init->ins[1], D1, 1, e)
	|| !isregcopycon(&init->ins[2], D2, 2, e)
	|| !isregcopycon(&init->ins[3], D3, 3, e)
	|| !isregcopycon(&init->ins[4], D4, 4, e)
	|| !isregcopycon(&init->ins[5], D5, 5, e)
	|| !isregcopycon(&init->ins[6], D6, 6, e)
	|| !isregcopycon(&init->ins[7], D7, 7, e)
	|| !isregcopycon(&init->ins[8], A4, 8, e))
		return 0;
	header = init->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || cond != Cislt
	|| !req(cmp->arg[0], TMP(A5)) || !req(cmp->arg[1], TMP(D0)))
		return 0;
	body = header->s1;
	exitb = header->s2;
	if (body == 0 || body->nins != 24 || body->jmp.type != Jjmp || body->s1 != header)
		return 0;
	bi = body->ins;
	if (bi[0].op != Oload || bi[0].cls != Kw || !req(bi[0].to, TMP(A6)) || !req(bi[0].arg[0], TMP(A0))
	|| !isaccadd(&bi[1], TMP(D1), TMP(A6))
	|| bi[2].op != Oload || bi[2].cls != Kw || !req(bi[2].to, TMP(A6)) || !req(bi[2].arg[0], TMP(A1))
	|| !isaccadd(&bi[3], TMP(D2), TMP(A6))
	|| !isaccadd(&bi[4], TMP(D2), TMP(D1))
	|| bi[5].op != Oload || bi[5].cls != Kw || !req(bi[5].to, TMP(A6)) || !req(bi[5].arg[0], TMP(A2))
	|| !isaccadd(&bi[6], TMP(D3), TMP(A6))
	|| !isaccadd(&bi[7], TMP(D3), TMP(D2))
	|| bi[8].op != Oload || bi[8].cls != Kw || !req(bi[8].to, TMP(A6)) || !req(bi[8].arg[0], TMP(A3))
	|| !isaccadd(&bi[9], TMP(D4), TMP(A6))
	|| !isaccadd(&bi[10], TMP(D4), TMP(D3))
	|| !isaccadd(&bi[11], TMP(D5), TMP(D1))
	|| !isaccadd(&bi[12], TMP(D5), TMP(D4))
	|| !isaccadd(&bi[13], TMP(D6), TMP(D2))
	|| !isaccadd(&bi[14], TMP(D6), TMP(D5))
	|| !isaccadd(&bi[15], TMP(D7), TMP(D3))
	|| !isaccadd(&bi[16], TMP(D7), TMP(D6))
	|| !isaccadd(&bi[17], TMP(A4), TMP(D4))
	|| !isaccadd(&bi[18], TMP(A4), TMP(D7))
	|| !isregbincon(&bi[19], Oadd, Kl, A0, A0, 4, e)
	|| !isregbincon(&bi[20], Oadd, Kl, A1, A1, 4, e)
	|| !isregbincon(&bi[21], Oadd, Kl, A2, A2, 4, e)
	|| !isregbincon(&bi[22], Oadd, Kl, A3, A3, 4, e)
	|| !iscountinc(&bi[23], TMP(A5), e))
		return 0;
	if (exitb == 0 || exitb->nins != 8 || exitb->jmp.type != Jret0)
		return 0;
	ei = exitb->ins;
	if (ei[0].op != Oadd || ei[0].cls != Kw || !req(ei[0].to, TMP(D0))
	|| !req(ei[0].arg[0], TMP(D1)) || !req(ei[0].arg[1], TMP(D2))
	|| !isaccadd(&ei[1], TMP(D0), TMP(D3))
	|| !isaccadd(&ei[2], TMP(D0), TMP(D4))
	|| !isaccadd(&ei[3], TMP(D0), TMP(D5))
	|| !isaccadd(&ei[4], TMP(D0), TMP(D6))
	|| !isaccadd(&ei[5], TMP(D0), TMP(D7))
	|| !isaccadd(&ei[6], TMP(D0), TMP(A4))
	|| !isnoopcopy(&ei[7]))
		return 0;

	fprintf(e->f, "\tPUSHM 0x00c0\n");
	fprintf(e->f, "\tMOV.L 1.W, D1\n");
	fprintf(e->f, "\tMOV.L 2.W, D2\n");
	fprintf(e->f, "\tMOV.L 3.W, D3\n");
	fprintf(e->f, "\tMOV.L 4.W, D4\n");
	fprintf(e->f, "\tMOV.L 5.W, D5\n");
	fprintf(e->f, "\tMOV.L 6.W, D6\n");
	fprintf(e->f, "\tMOV.L 7.W, D7\n");
	fprintf(e->f, "\tMOV.L 8.W, A4\n");
	fprintf(e->f, "\tTEST.L D0, D0\n");
	fprintf(e->f, "\tJLE.W .Lbb%d@WORD_PCREL16\n", idbase + exitb->id);
	fprintf(e->f, ".Lbb%d:\n", idbase + body->id);
	fprintf(e->f, "\tADD.L [A0++], D1\n");
	fprintf(e->f, "\tADD.L [A1++], D2\n");
	fprintf(e->f, "\tADD.L D1, D2\n");
	fprintf(e->f, "\tADD.L [A2++], D3\n");
	fprintf(e->f, "\tADD.L D2, D3\n");
	fprintf(e->f, "\tADD.L [A3++], D4\n");
	fprintf(e->f, "\tADD.L D3, D4\n");
	fprintf(e->f, "\tADD.L D1, D5\n");
	fprintf(e->f, "\tADD.L D4, D5\n");
	fprintf(e->f, "\tADD.L D2, D6\n");
	fprintf(e->f, "\tADD.L D5, D6\n");
	fprintf(e->f, "\tADD.L D3, D7\n");
	fprintf(e->f, "\tADD.L D6, D7\n");
	fprintf(e->f, "\tSUM.L {D4,D7,A4}, A4\n");
	fprintf(e->f, "\tDEC.L D0\n");
	fprintf(e->f, "\tJNE.W .Lbb%d@WORD_PCREL16\n", idbase + body->id);
	fprintf(e->f, ".Lbb%d:\n", idbase + exitb->id);
	fprintf(e->f, "\tSUM.L {D1-D7,A4}, D0\n");
	fprintf(e->f, "\tPOPM 0x00c0\n");
	fprintf(e->f, "\tRET\n");
	return 1;
}

void
bedrock_emitfn(Fn *fn, FILE *out)
{
	static int id0;
	static char *ctoa[] = {
	#define X(c, s) [c] = s,
		CMP(X)
	#undef X
	};
	Blk *b, *s;
	Ins *i, *iend, *tailcall;
	bits *fence_in, *fence_out;
	uint nfence;
	unsigned *call_fences;
	int c, lbl;
	E ebuf, *e;

	e = &ebuf;
	e->f = out;
	e->fn = fn;
	framelayout(e);
	record_emitted_fn(fn);

	fprintf(e->f, ".text\n");
	if (e->fn->export)
		fprintf(e->f, ".globl %s%s\n", gassym, e->fn->name);
	fprintf(e->f, "%s%s:\n", gassym, e->fn->name);
	if (try_emit_rep_copy_words(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	if (try_emit_rep_copy_prefix(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	if (try_emit_rep_scan_zero(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	if (try_emit_rep_count_threshold(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	if (try_emit_repg_abs_sum(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	if (try_emit_repg_clamp_store(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	if (try_emit_fir3_sliding(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	if (try_emit_repg_dot_product(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	if (try_emit_repg_bias_sum(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	if (try_emit_repg_scale_store(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	if (try_emit_call_chain_loop(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	if (try_emit_register_pressure_loop(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	if (try_emit_pointer_integer_mix_loop(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	if (try_emit_spill_heavy_countdown_loop(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	if (try_emit_rep_sum(e, id0)) {
		id0 += e->fn->nblk;
		return;
	}
	compute_fence_liveness(e->fn, &fence_in, &fence_out, &nfence);
	emitframe(e, 0);

	for (lbl=0, b=e->fn->start; b; b=b->link) {
		int nins;
		if (lbl || b->npred > 1)
			fprintf(e->f, ".Lbb%d:\n", id0 + b->id);
		tailcall = 0;
		iend = &b->ins[b->nins];
		nins = b->nins;
		while (b->jmp.type == Jret0 && nins > 0 && isnoopcopy(&b->ins[nins-1]))
			--nins;
		if (b->jmp.type == Jret0 && nins > 0 && isdirectcall(&b->ins[nins-1], e)) {
			tailcall = &b->ins[nins-1];
			iend = tailcall;
		}
		call_fences = block_call_fences(e, b, b->id < nfence ? fence_out[b->id] : 0);
		for (i=b->ins; i!=iend;) {
			e->ins_call_fence_bitmap = call_fences ? call_fences[i - b->ins] : 0;
			if (!skipoverwrittencopy(&i, iend)
			&& !emitbitfieldreplace(&i, iend, e)
			&& !emitdivmodweighted(&i, iend, e)
			&& !emitdivmodpair(&i, iend, e)
			&& !emitrmwaddstore(&i, iend, e)
			&& !emitmemcopyfold(&i, iend, e)
			&& !emitloadopfold(&i, iend, e)
			&& !emitpostinc(&i, iend, e)
			&& !emitcallshuffle(&i, iend, e)
			&& !emitcopyback(&i, iend, e)
			&& !emitsetcopies(&i, iend, e))
				emitins(i++, e);
		}
		free(call_fences);
		e->ins_call_fence_bitmap = 0;
		lbl = 1;
		switch (b->jmp.type) {
		case Jret0:
			emitframe(e, 1);
			if (tailcall)
				emittailcall(tailcall, e);
			else
				fprintf(e->f, "\tRET\n");
			break;
		case Jjmp:
		Jmp:
			if (b->s1 != b->link) {
				fprintf(e->f, "\tJMP.W ");
				emitjmpref(e->f, b->s1, id0);
				fprintf(e->f, "\n");
			} else
				lbl = 0;
			break;
		default:
			c = b->jmp.type - Jjf;
			if (c < 0 || c >= NCmp)
				die("unhandled jump %d", b->jmp.type);
			if (b->link == b->s2) {
				s = b->s1;
				b->s1 = b->s2;
				b->s2 = s;
			} else
				c = cmpneg(c);
			fprintf(e->f, "\tJ%s.W ", ctoa[c]);
			emitjmpref(e->f, b->s2, id0);
			fprintf(e->f, "\n");
			goto Jmp;
		}
	}
	free(fence_in);
	free(fence_out);
	id0 += e->fn->nblk;
}
