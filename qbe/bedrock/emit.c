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
	bits reg;
	bits replacement_reg;
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
static int ins_touches_regs(Fn *fn, Ins *i, bits regs);
static unsigned fence_pushm_bitmap(bits live);
static int ref_dead_after(Fn *fn, Ref r, Ins *start, Ins *end);

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
	} else if (F0 <= r && r <= F15) {
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
	return rtype(r) == RTmp && isreg(r) && F0 <= (int)r.val && (int)r.val <= F15;
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
scratchreg(int k, bits avoid)
{
	int r;

	if (KBASE(k) == 1) {
		for (r=F15; r>=F0; r--)
			if (!(avoid & BIT(r)))
				return r;
	} else {
		for (r=D7; r>=D0; r--)
			if (!(avoid & BIT(r)))
				return r;
	}
	die("no scratch register available");
}

static void
savescratch(int r, int k, E *e)
{
	if (KBASE(k) == 1)
		fprintf(e->f, "\tFPUSHM 0x%04x\n", 1u << (r - F0));
	else
		fprintf(e->f, "\tPUSH %s\n", rname(r, Kl));
}

static void
restorescratch(int r, int k, E *e)
{
	if (KBASE(k) == 1)
		fprintf(e->f, "\tFPOPM 0x%04x\n", 1u << (r - F0));
	else
		fprintf(e->f, "\tPOP %s\n", rname(r, Kl));
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
		bits avoid = 0;
		if (isreg(i->to))
			avoid |= BIT(i->to.val);
		if (isreg(i->arg[0]))
			avoid |= BIT(i->arg[0].val);
		scratch = TMP(scratchreg(i->cls, avoid));
		savescratch(scratch.val, i->cls, e);
		copyref(scratch, i->arg[1], i->cls, e);
		copyref(i->to, i->arg[0], i->cls, e);
		emitop2ref(op, i->cls, scratch, i->to, e);
		restorescratch(scratch.val, i->cls, e);
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
	if (i + 2 < end
	&& i[2].op == Ocopy && i[2].cls == i[0].cls
	&& req(i[2].to, i[0].to) && !req(i[2].arg[0], i[0].to)) {
		*pi = i + 2;
		return 1;
	}
	copyref(i[0].to, i[0].arg[0], i[0].cls, e);
	*pi = i + 2;
	return 1;
}

static int
emitcopythrough(Ins **pi, Ins *end, E *e)
{
	Ins *i, *use, *kill;
	Ref tmp, src, dst;
	bits watched;

	i = *pi;
	if (end - i < 3 || i[0].op != Ocopy)
		return 0;
	if (!isreg(i[0].to) || !isreg(i[0].arg[0]))
		return 0;
	tmp = i[0].to;
	src = i[0].arg[0];
	if (req(src, tmp))
		return 0;
	for (use=i+1; use!=end; use++) {
		if (use->op != Onop && use->op != Ocopy)
			return 0;
		if (use->op == Ocopy && use->cls == i[0].cls
		&& isreg(use->to) && isreg(use->arg[0]) && req(use->arg[0], tmp)) {
			dst = use->to;
			if (req(dst, tmp) || req(dst, src))
				return 0;
			watched = BIT(tmp.val) | BIT(dst.val);
			break;
		}
		if (ins_touches_regs(e->fn, use, BIT(tmp.val)))
			return 0;
	}
	if (use == end)
		return 0;
	for (kill=use+1; kill!=end; kill++) {
		if (kill->op != Onop && kill->op != Ocopy)
			return 0;
		if (kill->op == Ocopy && kill->cls == i[0].cls
		&& isreg(kill->to) && req(kill->to, tmp) && !req(kill->arg[0], tmp)) {
			copyref(dst, src, i[0].cls, e);
			use->op = Onop;
			*pi = i + 1;
			return 1;
		}
		if (ins_touches_regs(e->fn, kill, watched))
			return 0;
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
	if (i->op == Onop)
		return 0;
	return req(i->arg[0], r) || req(i->arg[1], r)
		|| (ref_reg_bits(fn, i->arg[0]) & ref_reg_bits(fn, r))
		|| (ref_reg_bits(fn, i->arg[1]) & ref_reg_bits(fn, r));
}

static int
ins_defines_ref(Ins *i, Ref r)
{
	if (i->op == Onop)
		return 0;
	return rtype(i->to) == RTmp && req(i->to, r);
}

static int
ins_touches_regs(Fn *fn, Ins *i, bits regs)
{
	if (i->op == Onop)
		return 0;
	if (rtype(i->to) == RTmp && isreg(i->to) && (regs & BIT(i->to.val)))
		return 1;
	return (ref_reg_bits(fn, i->arg[0]) & regs)
		|| (ref_reg_bits(fn, i->arg[1]) & regs);
}

static bits
fence_bitmap_reg_bits(unsigned bm)
{
	bits regs;
	int bit, reg;

	regs = 0;
	for (bit=0; bit<16; bit++) {
		if (!(bm & (1u << bit)))
			continue;
		reg = bit < 8 ? D0 + bit : A0 + bit - 8;
		regs |= BIT(reg);
	}
	return regs;
}

static int
overwritten_copy(Ins *i, Ins *end)
{
	if (end - i < 2 || i[0].op != Ocopy || i[1].op != Ocopy)
		return 0;
	if (rtype(i[0].to) != RTmp || !isreg(i[0].to) || !req(i[0].to, i[1].to))
		return 0;
	return !req(i[1].arg[0], i[0].to);
}

static int
copyback_with_overwrite(Ins *i, Ins *end)
{
	if (end - i < 3)
		return 0;
	if (i[0].op != Ocopy || i[1].op != Ocopy || i[2].op != Ocopy)
		return 0;
	if (i[0].cls != i[1].cls || i[0].cls != i[2].cls)
		return 0;
	if (!isreg(i[0].to) || !isreg(i[0].arg[0])
	|| !isreg(i[1].to) || !isreg(i[1].arg[0]))
		return 0;
	if (!req(i[0].to, i[1].arg[0]) || !req(i[0].arg[0], i[1].to))
		return 0;
	return req(i[2].to, i[0].to) && !req(i[2].arg[0], i[0].to);
}

static int
call_fence_group_scan_used(Fn *fn, Ins *i, Ins *end, bits regs, int *used)
{
	if (i->op == Onop)
		goto One;
	if (overwritten_copy(i, end))
		goto One;
	if (copyback_with_overwrite(i, end)) {
		*used = 2;
		return 1;
	}
	if (i->op != Ocopy || ins_touches_regs(fn, i, regs))
		return 0;
	if (rtype(i->arg[0]) == RMem || rtype(i->arg[0]) == RSlot
	|| rtype(i->arg[1]) == RMem || rtype(i->arg[1]) == RSlot)
		return 0;
One:
	*used = 1;
	return 1;
}

static int
emitcallfencegroup(Ins **pi, Ins *end, E *e, unsigned *fences, Ins *base)
{
	Ins *i, *scan;
	bits regs;
	unsigned bm;
	int calls, used;

	i = *pi;
	if (fences == 0 || i == end || i->op != Ocall)
		return 0;
	bm = fences[i - base];
	if (bm == 0)
		return 0;
	regs = fence_bitmap_reg_bits(bm);
	calls = 0;
	for (scan=i; scan!=end;) {
		if (scan->op == Ocall) {
			if (fences[scan - base] != bm)
				break;
			calls++;
			scan++;
			continue;
		}
		if (!call_fence_group_scan_used(e->fn, scan, end, regs, &used))
			break;
		scan += used;
	}
	if (calls < 2)
		return 0;
	fprintf(e->f, "\tPUSHM 0x%04x\n", bm);
	while (i != scan) {
		if (i->op == Ocall) {
			e->ins_call_fence_bitmap = 0;
			emitins(i++, e);
			continue;
		}
		if (overwritten_copy(i, scan)) {
			i++;
			continue;
		}
		if (!emitcopyback(&i, scan, e))
			emitins(i++, e);
	}
	fprintf(e->f, "\tPOPM 0x%04x\n", bm);
	*pi = scan;
	return 1;
}

static int
fenced_pair_other(Ref r)
{
	if (!isreg(r))
		return -1;
	if (r.val == A4)
		return A5;
	if (r.val == A5)
		return A4;
	return -1;
}

static int
copyback_pair_for(Ins *i, Ins *end, Ref reg, int cls)
{
	Ref tmp;

	if (end - i < 2 || i[0].op != Ocopy || i[1].op != Ocopy)
		return 0;
	if (i[0].cls != cls || i[1].cls != cls)
		return 0;
	if (!isreg(i[0].to) || !isreg(i[0].arg[0]) || !isreg(i[1].to) || !isreg(i[1].arg[0]))
		return 0;
	if (!req(i[0].arg[0], reg) || !req(i[1].to, reg))
		return 0;
	tmp = i[0].to;
	return req(i[1].arg[0], tmp);
}

static int
emitstackcallspill(Ins **pi, Ins *end, E *e, unsigned *fences, Ins *base)
{
	Ins *i, *scan, *restore;
	Ref spill, src, dst;
	int other, sawcall, cls;

	i = *pi;
	if (end - i < 4 || i->op != Ocopy || KBASE(i->cls) != 0)
		return 0;
	if (!isreg(i->to) || !isreg(i->arg[0]))
		return 0;
	spill = i->to;
	src = i->arg[0];
	other = fenced_pair_other(spill);
	if (other < 0 || !isdreg(src))
		return 0;
	if (!ref_dead_after(e->fn, TMP(other), i + 1, end))
		return 0;
	cls = i->cls;
	sawcall = 0;
	restore = 0;
	for (scan=i+1; scan!=end;) {
		if (copyback_pair_for(scan, end, spill, cls)) {
			scan += 2;
			continue;
		}
		if (scan->op == Ocall) {
			sawcall = 1;
			scan++;
			continue;
		}
		if (scan->op == Ocopy && scan->cls == cls
		&& isreg(scan->to) && isreg(scan->arg[0]) && req(scan->arg[0], spill)) {
			restore = scan;
			dst = scan->to;
			break;
		}
		if (ins_touches_regs(e->fn, scan, BIT(spill.val)))
			return 0;
		scan++;
	}
	if (!sawcall || restore == 0 || !isdreg(dst))
		return 0;
	fprintf(e->f, "\tPUSH %s\n", rname(src.val, cls));
	for (scan=i+1; scan!=restore;) {
		if (copyback_pair_for(scan, restore, spill, cls)) {
			scan += 2;
			continue;
		}
		if (scan->op == Ocall && fences != 0)
			e->ins_call_fence_bitmap = fences[scan - base] & ~fence_pushm_bitmap(BIT(spill.val) | BIT(other));
		emitins(scan++, e);
	}
	fprintf(e->f, "\tMOV.%c [SP + 0], %s\n", siz(cls), rname(dst.val, cls));
	fprintf(e->f, "\tPOP %s\n", rname(spill.val, cls));
	*pi = restore + 1;
	return 1;
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
		if (inc == i+1 && inc+1 != end && !isdreg(i->to)) {
			Ins *op;
			Ref acc;
			char *name;

			op = inc + 1;
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
bitmap_bit_for_intreg(Ref r, unsigned *bit)
{
	int v;

	if (rtype(r) != RTmp || !isreg(r))
		return 0;
	v = (int)r.val;
	if (D0 <= v && v <= D7) {
		*bit = (unsigned)(v - D0);
		return 1;
	}
	if (A0 <= v && v <= A7) {
		*bit = (unsigned)(8 + v - A0);
		return 1;
	}
	return 0;
}

static int
bitmap_add_intreg(unsigned *bitmap, Ref r)
{
	unsigned bit, mask;

	if (!bitmap_bit_for_intreg(r, &bit))
		return 0;
	mask = 1u << bit;
	if (*bitmap & mask)
		return 0;
	*bitmap |= mask;
	return 1;
}

static int
bitmap_operand_count(unsigned bitmap)
{
	int count;

	count = 0;
	bitmap &= 0xffffu;
	while (bitmap) {
		count += bitmap & 1u;
		bitmap >>= 1;
	}
	return count;
}

static int
add_source_for_acc(Ins *i, Ref acc, Ref *src)
{
	if (i->op != Oadd || !req(i->to, acc))
		return 0;
	if (req(i->arg[0], acc) && isintreg(i->arg[1])) {
		*src = i->arg[1];
		return 1;
	}
	if (req(i->arg[1], acc) && isintreg(i->arg[0])) {
		*src = i->arg[0];
		return 1;
	}
	return 0;
}

static int
emitsumfold(Ins **pi, Ins *end, E *e)
{
	Ins *i, *scan;
	Ref dst, src;
	unsigned bitmap;
	int cls, old_words, first_extra_word;

	i = *pi;
	if (i == end || KBASE(i->cls) != 0 || (i->cls != Kw && i->cls != Kl))
		return 0;
	bitmap = 0;
	cls = i->cls;
	first_extra_word = 0;
	if (i->op == Ocopy && isintreg(i->to) && isintreg(i->arg[0])) {
		dst = i->to;
		if (!bitmap_add_intreg(&bitmap, i->arg[0]))
			return 0;
		scan = i + 1;
	} else if (i->op == Oadd && isintreg(i->to) && isintreg(i->arg[0]) && isintreg(i->arg[1])) {
		dst = i->to;
		if (!bitmap_add_intreg(&bitmap, i->arg[0]) || !bitmap_add_intreg(&bitmap, i->arg[1]))
			return 0;
		if (!req(i->to, i->arg[0]) && !req(i->to, i->arg[1]))
			first_extra_word = 1;
		scan = i + 1;
	} else if (isintreg(i->to) && add_source_for_acc(i, i->to, &src)) {
		dst = i->to;
		if (!bitmap_add_intreg(&bitmap, dst) || !bitmap_add_intreg(&bitmap, src))
			return 0;
		scan = i + 1;
	} else {
		return 0;
	}
	while (scan != end && scan->cls == cls && add_source_for_acc(scan, dst, &src)) {
		if (!bitmap_add_intreg(&bitmap, src))
			break;
		scan++;
	}
	if (bitmap_operand_count(bitmap) < 3)
		return 0;
	old_words = (int)(scan - i) + first_extra_word;
	if (old_words <= 3)
		return 0;
	fprintf(e->f, "\tSUM.%c 0x%04x, %s\n", siz(cls), bitmap & 0xffffu, rname(dst.val, cls));
	*pi = scan;
	return 1;
}

static int
is_areg_ref(Ref r)
{
	return rtype(r) == RTmp && isreg(r) && A0 <= (int)r.val && (int)r.val <= A7;
}

static int
is_self_shl2(Ins *i, Ref reg, E *e)
{
	if (i->op != Oshl || i->cls != Kl || !req(i->to, reg) || !req(i->arg[0], reg))
		return 0;
	return isconval(i->arg[1], e, 2);
}

static int
is_copy_areg(Ins *i, Ref *base, Ref *dst)
{
	if (i->op != Ocopy || i->cls != Kl || !is_areg_ref(i->arg[0]) || !is_areg_ref(i->to))
		return 0;
	*base = i->arg[0];
	*dst = i->to;
	return 1;
}

static int
is_ptr_add_index(Ins *i, Ref dst, Ref index)
{
	if (i->op != Oadd || i->cls != Kl || !req(i->to, dst))
		return 0;
	return (req(i->arg[0], dst) && req(i->arg[1], index))
		|| (req(i->arg[1], dst) && req(i->arg[0], index));
}

static int
is_ptr_add_base_index(Ins *i, Ref *base, Ref index, Ref *dst)
{
	if (i->op != Oadd || i->cls != Kl || !is_areg_ref(i->to))
		return 0;
	if (is_areg_ref(i->arg[0]) && req(i->arg[1], index)) {
		*base = i->arg[0];
		*dst = i->to;
		return 1;
	}
	if (is_areg_ref(i->arg[1]) && req(i->arg[0], index)) {
		*base = i->arg[1];
		*dst = i->to;
		return 1;
	}
	return 0;
}

typedef struct {
	Ref base;
	Ref dst;
	Ref index;
	Ref tmp;
	const char *suffix;
	int nins;
} LeaFold;

static int
matchleafold(Ins *i, Ins *end, E *e, LeaFold *fold)
{
	if (end - i >= 3
	&& i[0].op == Oextsw && i[0].cls == Kl && isdreg(i[0].to) && isdreg(i[0].arg[0])
	&& is_self_shl2(&i[1], i[0].to, e)
	&& is_ptr_add_base_index(&i[2], &fold->base, i[0].to, &fold->dst)
	&& ref_dead_after(e->fn, i[0].to, i + 3, end)) {
		fold->index = i[0].arg[0];
		fold->tmp = i[0].to;
		fold->suffix = ".L";
		fold->nins = 3;
		return 1;
	}
	if (end - i >= 2
	&& isdreg(i[0].to) && is_self_shl2(&i[0], i[0].to, e)
	&& is_ptr_add_base_index(&i[1], &fold->base, i[0].to, &fold->dst)
	&& ref_dead_after(e->fn, i[0].to, i + 2, end)) {
		fold->index = i[0].to;
		fold->tmp = i[0].to;
		fold->suffix = "";
		fold->nins = 2;
		return 1;
	}
	if (end - i >= 4
	&& i[0].op == Oextsw && i[0].cls == Kl && isdreg(i[0].to) && isdreg(i[0].arg[0])
	&& is_self_shl2(&i[1], i[0].to, e)
	&& is_copy_areg(&i[2], &fold->base, &fold->dst)
	&& is_ptr_add_index(&i[3], fold->dst, i[0].to)
	&& ref_dead_after(e->fn, i[0].to, i + 4, end)) {
		fold->index = i[0].arg[0];
		fold->tmp = i[0].to;
		fold->suffix = ".L";
		fold->nins = 4;
		return 1;
	}
	if (end - i >= 3
	&& isdreg(i[0].to) && is_self_shl2(&i[0], i[0].to, e)
	&& is_copy_areg(&i[1], &fold->base, &fold->dst)
	&& is_ptr_add_index(&i[2], fold->dst, i[0].to)
	&& ref_dead_after(e->fn, i[0].to, i + 3, end)) {
		fold->index = i[0].to;
		fold->tmp = i[0].to;
		fold->suffix = "";
		fold->nins = 3;
		return 1;
	}
	return 0;
}

static void
emitleafoldplan(LeaFold *fold, Ref base, E *e)
{
	fprintf(e->f, "\tLEA [%s + %s%s * 4], %s\n",
		rname(base.val, Kl), rname(fold->index.val, Kl),
		fold->suffix, rname(fold->dst.val, Kl));
}

static int
emitleafold(Ins **pi, Ins *end, E *e)
{
	LeaFold fold;

	if (!matchleafold(*pi, end, e, &fold))
		return 0;
	emitleafoldplan(&fold, fold.base, e);
	*pi += fold.nins;
	return 1;
}

static int
lea_reorder_middle_safe(Fn *fn, Ins *i, bits forbidden)
{
	if (i->op == Onop)
		return 1;
	if (isload(i->op) || isstore(i->op) || i->op == Ocall)
		return 0;
	if (KBASE(i->cls) == 1)
		return 0;
	if (ref_is_memlike(i->to) || ref_is_memlike(i->arg[0]) || ref_is_memlike(i->arg[1]))
		return 0;
	return !ins_touches_regs(fn, i, forbidden);
}

static int
emitleareorder(Ins **pi, Ins *end, E *e)
{
	Ins *i, *first, *scan, *mid;
	LeaFold before, after;
	Ref base, save;
	bits forbidden;

	i = *pi;
	if (end - i < 6 || !is_copy_areg(i, &base, &save) || req(base, save))
		return 0;
	first = i + 1;
	if (!matchleafold(first, end, e, &before))
		return 0;
	if (!req(before.base, save) || !req(before.dst, base))
		return 0;
	forbidden = BIT(base.val) | BIT(save.val) | BIT(before.index.val) | BIT(before.tmp.val);
	for (scan=first+before.nins; scan!=end; scan++) {
		if (matchleafold(scan, end, e, &after)) {
			if (!req(after.base, save) || req(after.dst, base) || req(after.dst, save))
				return 0;
			if (!ref_dead_after(e->fn, save, scan + after.nins, end))
				return 0;
			for (mid=first+before.nins; mid!=scan; mid++) {
				if (!lea_reorder_middle_safe(e->fn, mid, forbidden))
					return 0;
			}
			for (mid=first+before.nins; mid!=scan;)
				emitins(mid++, e);
			emitleafoldplan(&after, base, e);
			emitleafoldplan(&before, base, e);
			*pi = scan + after.nins;
			return 1;
		}
		if (!lea_reorder_middle_safe(e->fn, scan, forbidden))
			return 0;
	}
	return 0;
}

static int
leafold_consumes_tmp(Ins *i, Ins *end, E *e, Ref tmp, int *used)
{
	Ref base, dst;

	if (end - i >= 3
	&& i[0].op == Oextsw && i[0].cls == Kl && req(i[0].to, tmp) && isdreg(i[0].arg[0])
	&& is_self_shl2(&i[1], tmp, e)
	&& is_ptr_add_base_index(&i[2], &base, tmp, &dst)) {
		*used = 3;
		return 1;
	}
	if (end - i >= 2
	&& req(i[0].to, tmp) && is_self_shl2(&i[0], tmp, e)
	&& is_ptr_add_base_index(&i[1], &base, tmp, &dst)) {
		*used = 2;
		return 1;
	}
	if (end - i >= 4
	&& i[0].op == Oextsw && i[0].cls == Kl && req(i[0].to, tmp) && isdreg(i[0].arg[0])
	&& is_self_shl2(&i[1], tmp, e)
	&& is_copy_areg(&i[2], &base, &dst)
	&& is_ptr_add_index(&i[3], dst, tmp)) {
		*used = 4;
		return 1;
	}
	if (end - i >= 3
	&& req(i[0].to, tmp) && is_self_shl2(&i[0], tmp, e)
	&& is_copy_areg(&i[1], &base, &dst)
	&& is_ptr_add_index(&i[2], dst, tmp)) {
		*used = 3;
		return 1;
	}
	return 0;
}

static int
emitsavedsubshift(Ins **pi, Ins *end, E *e)
{
	Ins *i, *scan, *chain, *sub, *shift;
	Ref hi, base, savehi, savebase, tmp, dst;
	int used;

	i = *pi;
	if (end - i < 6)
		return 0;
	if (i[0].op != Ocopy || i[1].op != Ocopy || i[0].cls != Kl || i[1].cls != Kl)
		return 0;
	if (!isreg(i[0].arg[0]) || !isreg(i[0].to)
	|| !isreg(i[1].arg[0]) || !isreg(i[1].to))
		return 0;
	hi = i[0].arg[0];
	savehi = i[0].to;
	base = i[1].arg[0];
	savebase = i[1].to;
	if (req(hi, savehi) || req(base, savebase) || req(savehi, savebase))
		return 0;
	chain = 0;
	for (scan=i+2; scan+1<end; scan++) {
		if (scan[0].op == Osub && scan[0].cls == Kl
		&& isdreg(scan[0].to) && req(scan[0].arg[0], savehi) && req(scan[0].arg[1], savebase)
		&& scan[1].op == Osar && scan[1].cls == Kl
		&& isdreg(scan[1].to) && req(scan[1].arg[0], scan[0].to)) {
			tmp = scan[0].to;
			dst = scan[1].to;
			shift = scan + 1;
			if (!ref_dead_after(e->fn, savehi, scan + 2, end)
			|| !ref_dead_after(e->fn, tmp, scan + 2, end))
				return 0;
			chain = scan;
			break;
		}
		if (scan+3 >= end)
			continue;
		if (scan[0].op == Ocopy && scan[0].cls == Kl
		&& req(scan[0].arg[0], savehi) && isdreg(scan[0].to)) {
			tmp = scan[0].to;
			sub = scan + 1;
			if (sub->op != Osub || sub->cls != Kl || !req(sub->to, tmp)
			|| !req(sub->arg[0], tmp) || !req(sub->arg[1], savebase))
				continue;
			if (scan[2].op != Ocopy || scan[2].cls != Kl
			|| !req(scan[2].arg[0], tmp) || !isdreg(scan[2].to))
				continue;
			dst = scan[2].to;
			shift = scan + 3;
			if (shift->op != Osar || shift->cls != Kl
			|| !req(shift->to, dst) || !req(shift->arg[0], dst))
				continue;
			if (!ref_dead_after(e->fn, savehi, scan + 4, end)
			|| !ref_dead_after(e->fn, tmp, scan + 4, end))
				return 0;
			chain = scan;
			break;
		}
	}
	if (chain == 0)
		return 0;
	for (scan=i+2; scan!=chain; ) {
		if (ins_touches_regs(e->fn, scan, BIT(savehi.val)))
			return 0;
		if (ins_touches_regs(e->fn, scan, BIT(dst.val))) {
			if (!leafold_consumes_tmp(scan, end, e, dst, &used) || scan + used > chain)
				return 0;
			scan += used;
			continue;
		}
		scan++;
	}
	copyref(dst, hi, Kl, e);
	emitop2ref("SUB", Kl, base, dst, e);
	emitop2ref("SAR", Kl, shift->arg[1], dst, e);
	if (shift == chain + 1) {
		chain[0].op = Onop;
		chain[1].op = Onop;
	} else {
		chain[0].op = Onop;
		chain[1].op = Onop;
		chain[2].op = Onop;
		chain[3].op = Onop;
	}
	*pi = i + 1;
	return 1;
}

static int
mul_uses_pair(Ins *i, Ref lhs, Ref rhs)
{
	if (i->op != Omul || i->cls != Kw)
		return 0;
	return (req(i->arg[0], lhs) && req(i->arg[1], rhs))
		|| (req(i->arg[0], rhs) && req(i->arg[1], lhs));
}

static int
add_accumulates_product(Ins *i, Ref product, Ref *acc)
{
	if (i->op != Oadd || i->cls != Kw || !isdreg(i->to))
		return 0;
	if (req(i->arg[0], i->to) && req(i->arg[1], product)) {
		*acc = i->to;
		return 1;
	}
	if (req(i->arg[1], i->to) && req(i->arg[0], product)) {
		*acc = i->to;
		return 1;
	}
	return 0;
}

static int
emitloadmaddfold(Ins **pi, Ins *end, E *e)
{
	Ins *load0, *load1, *mul, *add;
	Ref product, acc;
	char src[128];

	load0 = *pi;
	if (end - load0 < 4 || load0[0].op != Oload || load0[1].op != Oload)
		return 0;
	load1 = load0 + 1;
	mul = load0 + 2;
	add = load0 + 3;
	if (load0->cls != Kw || load1->cls != Kw || !isdreg(load0->to) || !isdreg(load1->to))
		return 0;
	if (!mul_uses_pair(mul, load0->to, load1->to))
		return 0;
	product = mul->to;
	if (!req(product, load0->to) && !req(product, load1->to))
		return 0;
	if (!add_accumulates_product(add, product, &acc))
		return 0;
	if (!ref_dead_after(e->fn, load0->to, add + 1, end)
	|| !ref_dead_after(e->fn, load1->to, add + 1, end))
		return 0;
	emitins(load0, e);
	snprintf(src, sizeof(src), "%s", memrefread(load1->arg[0], e));
	fprintf(e->f, "\tMADD.L %s, %s, %s\n",
		src, rname(load0->to.val, Kw), rname(acc.val, Kw));
	*pi = add + 1;
	return 1;
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
record_emitted_fn(Fn *fn, bits regs)
{
	uint i;

	for (i=0; i<nemitted_fns; i++)
		if (strcmp(emitted_fns[i].name, fn->name) == 0) {
			emitted_fns[i].regs = regs;
			return;
		}
	if (nemitted_fns == sizeof emitted_fns / sizeof emitted_fns[0])
		return;
	strncpy(emitted_fns[nemitted_fns].name, fn->name, NString-1);
	emitted_fns[nemitted_fns].name[NString-1] = '\0';
	emitted_fns[nemitted_fns].regs = regs;
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

static bits
call_fenced_regs(E *e)
{
	bits *fence_in, *fence_out, live, regs;
	Blk *b;
	Ins *i;
	uint nfence, idx;

	compute_fence_liveness(e->fn, &fence_in, &fence_out, &nfence);
	regs = 0;
	for (b=e->fn->start; b; b=b->link) {
		live = (b->id < nfence ? fence_out[b->id] : 0) | fence_ref_regs(e->fn, b->jmp.arg);
		for (idx=b->nins; idx-- > 0;) {
			i = &b->ins[idx];
			if (i->op == Ocall && call_fence_bitmap(e, i, live))
				regs |= live & (BIT(A4) | BIT(A5));
			live = fence_ins_uses(e->fn, i) | (live & ~fence_ins_defs(i));
		}
	}
	free(fence_in);
	free(fence_out);
	return regs;
}

static int
call_uses_arg_reg(Ins *i, int reg)
{
	return i->op == Ocall && (bedrock_argregs(i->arg[1], 0) & BIT(reg));
}

static int
entry_uses_reg_before_def(Fn *fn, int reg)
{
	Blk *b;
	Ins *i;
	Ref r;

	b = fn->start;
	if (b == 0)
		return 0;
	r = TMP(reg);
	for (i=b->ins; i!=&b->ins[b->nins]; i++) {
		if (ins_uses_ref(fn, i, r))
			return 1;
		if (ins_defines_ref(i, r))
			return 0;
	}
	return 0;
}

static int
fixed_abi_reg_use(Fn *fn, int reg)
{
	Blk *b;
	Ins *i;

	if (entry_uses_reg_before_def(fn, reg))
		return 1;
	for (b=fn->start; b; b=b->link)
		for (i=b->ins; i!=&b->ins[b->nins]; i++)
			if (call_uses_arg_reg(i, reg))
				return 1;
	return 0;
}

static bits
all_emitted_regs(Fn *fn)
{
	Blk *b;
	Ins *i;
	bits regs;

	regs = 0;
	for (b=fn->start; b; b=b->link) {
		for (i=b->ins; i!=&b->ins[b->nins]; i++) {
			if (i->op == Onop)
				continue;
			if (rtype(i->to) == RTmp && isreg(i->to))
				regs |= BIT(i->to.val);
			regs |= ref_reg_bits(fn, i->arg[0]);
			regs |= ref_reg_bits(fn, i->arg[1]);
		}
		regs |= ref_reg_bits(fn, b->jmp.arg);
	}
	return regs;
}

static void
replace_ref_reg(Fn *fn, Ref *r, int from, int to)
{
	Mem *m;

	switch (rtype(*r)) {
	case RTmp:
		if (isreg(*r) && r->val == (uint)from)
			*r = TMP(to);
		break;
	case RMem:
		m = &fn->mem[r->val];
		replace_ref_reg(fn, &m->base, from, to);
		replace_ref_reg(fn, &m->index, from, to);
		break;
	default:
		break;
	}
}

static void
replace_fn_reg(Fn *fn, int from, int to)
{
	Blk *b;
	Ins *i;

	for (b=fn->start; b; b=b->link) {
		for (i=b->ins; i!=&b->ins[b->nins]; i++) {
			replace_ref_reg(fn, &i->to, from, to);
			replace_ref_reg(fn, &i->arg[0], from, to);
			replace_ref_reg(fn, &i->arg[1], from, to);
		}
		replace_ref_reg(fn, &b->jmp.arg, from, to);
	}
}

static void
promote_call_fenced_regs(E *e)
{
	bits fenced, used;

	fenced = call_fenced_regs(e);
	if (!(fenced & (BIT(A4) | BIT(A5))))
		return;
	used = all_emitted_regs(e->fn);
	if (used & BIT(A6))
		return;
	if ((fenced & BIT(A4)) && !fixed_abi_reg_use(e->fn, A4)) {
		replace_fn_reg(e->fn, A4, A6);
		return;
	}
	if ((fenced & BIT(A5)) && !fixed_abi_reg_use(e->fn, A5))
		replace_fn_reg(e->fn, A5, A6);
}

static bits
ins_reg_defs(Ins *i)
{
	if (i->op == Onop)
		return 0;
	if (rtype(i->to) == RTmp && isreg(i->to))
		return BIT(i->to.val);
	return 0;
}

static void
compute_reg_liveness(Fn *fn, bits **pin, bits **pout, uint *pn)
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
			uses = ref_reg_bits(fn, i->arg[0]) | ref_reg_bits(fn, i->arg[1]);
			defs = ins_reg_defs(i);
			gen[b->id] |= uses & ~kill[b->id];
			kill[b->id] |= defs;
		}
		gen[b->id] |= ref_reg_bits(fn, b->jmp.arg) & ~kill[b->id];
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

static int
regcopyrefs(Ins *i, Ref *dst, Ref *src)
{
	if (i->op != Ocopy || !isreg(i->to) || !isreg(i->arg[0]))
		return 0;
	*dst = i->to;
	*src = i->arg[0];
	return 1;
}

static void
elide_edge_copybacks(Fn *fn)
{
	bits *live_in, *live_out, pair;
	Blk *b, *s;
	Ins *first, *scan, *last;
	Ref dst, src, rdst, rsrc;
	uint nlive;

	compute_reg_liveness(fn, &live_in, &live_out, &nlive);
	for (b=fn->start; b; b=b->link) {
		if (b->jmp.type != Jjmp || b->s1 == 0)
			continue;
		s = b->s1;
		if (s->npred != 1 || s->nins != 1 || s->jmp.type != Jjmp)
			continue;
		first = &s->ins[0];
		if (!regcopyrefs(first, &rdst, &rsrc))
			continue;
		if (s->id < nlive && (live_out[s->id] & BIT(rsrc.val)))
			continue;
		pair = BIT(rdst.val) | BIT(rsrc.val);
		if (ref_reg_bits(fn, b->jmp.arg) & pair)
			continue;
		last = &b->ins[b->nins];
		for (scan=last; scan-- != b->ins;) {
			if (regcopyrefs(scan, &dst, &src)
			&& scan->cls == first->cls && req(dst, rsrc) && req(src, rdst)) {
				scan->op = Onop;
				first->op = Onop;
				break;
			}
			if (ins_touches_regs(fn, scan, pair))
				break;
		}
	}
	free(live_in);
	free(live_out);
}

static void
appendins(Blk *b, Ins ins)
{
	Ins *newins;

	newins = alloc((b->nins + 1) * sizeof newins[0]);
	if (b->nins)
		memcpy(newins, b->ins, b->nins * sizeof newins[0]);
	newins[b->nins++] = ins;
	b->ins = newins;
}

static int
block_reaches_rec(Blk *b, Blk *target, unsigned char *seen, uint nseen)
{
	if (b == 0)
		return 0;
	if (b == target)
		return 1;
	if (b->id >= nseen || seen[b->id])
		return 0;
	seen[b->id] = 1;
	return block_reaches_rec(b->s1, target, seen, nseen)
		|| block_reaches_rec(b->s2, target, seen, nseen);
}

static int
block_reaches(Blk *from, Blk *to, uint nblk)
{
	unsigned char *seen;
	int reaches;

	seen = calloc(nblk, 1);
	if (!seen)
		die("out of memory");
	reaches = block_reaches_rec(from, to, seen, nblk);
	free(seen);
	return reaches;
}

static Blk *
loop_preheader(Fn *fn, Blk *header, uint nblk)
{
	Blk *b, *pre;

	pre = 0;
	for (b=fn->start; b; b=b->link) {
		if (b->s1 != header && b->s2 != header)
			continue;
		if (block_reaches(header, b, nblk))
			continue;
		if (pre != 0)
			return 0;
		pre = b;
	}
	return pre;
}

static int
copy_phys_reg(Ins *i, Ref to, Ref from)
{
	return i->op == Ocopy && i->cls == Kw
		&& isreg(i->to) && isreg(i->arg[0])
		&& req(i->to, to) && req(i->arg[0], from);
}

static int
copy_from_to(Ins *i, Ref to, Ref from, int cls)
{
	return i->op == Ocopy && i->cls == cls
		&& isreg(i->to) && isreg(i->arg[0])
		&& req(i->to, to) && req(i->arg[0], from);
}

static int
loop_saved_reg_pair(Fn *fn, Blk *body, Ref orig, Ref *save)
{
	Ins *i, *end, *saved, *restore, *scan;
	int sawcall;

	if (body == 0)
		return 0;
	end = &body->ins[body->nins];
	for (i=body->ins; i!=end; i++) {
		if (i->op != Ocopy || i->cls != Kw
		|| !isreg(i->to) || !isreg(i->arg[0]) || !req(i->arg[0], orig))
			continue;
		*save = i->to;
		if (req(*save, orig))
			continue;
		saved = i;
		sawcall = 0;
		restore = 0;
		for (scan=saved+1; scan!=end; scan++) {
			if (scan->op == Ocall)
				sawcall = 1;
			if (ins_defines_ref(scan, *save))
				break;
			if (copy_phys_reg(scan, orig, *save)) {
				restore = scan;
				break;
			}
		}
		if (!sawcall || restore == 0)
			continue;
		for (scan=saved+1; scan!=restore; scan++)
			if (ins_uses_ref(fn, scan, *save))
				return 0;
		saved->op = Onop;
		restore->op = Onop;
		return 1;
	}
	return 0;
}

static void
promote_loop_saved_regs(Fn *fn)
{
	Blk *h, *body, *pre;
	Ins *cmp, copy;
	Ref orig, save;
	uint nblk;

	nblk = maxblkid(fn) + 1;
	for (h=fn->start; h; h=h->link) {
		if (h->nins != 1 || h->s1 == 0 || h->s2 == 0)
			continue;
		cmp = &h->ins[0];
		if (cmp->op != Oacmp || cmp->cls != Kw)
			continue;
		body = block_reaches(h->s1, h, nblk) ? h->s1 : 0;
		if (body == 0 && block_reaches(h->s2, h, nblk))
			body = h->s2;
		if (body == 0)
			continue;
		pre = loop_preheader(fn, h, nblk);
		if (pre == 0 || pre->jmp.type != Jjmp)
			continue;
		if (isreg(cmp->arg[0]) && loop_saved_reg_pair(fn, body, cmp->arg[0], &save)) {
			orig = cmp->arg[0];
			cmp->arg[0] = save;
		} else if (isreg(cmp->arg[1]) && loop_saved_reg_pair(fn, body, cmp->arg[1], &save)) {
			orig = cmp->arg[1];
			cmp->arg[1] = save;
		} else {
			continue;
		}
		memset(&copy, 0, sizeof copy);
		copy.op = Ocopy;
		copy.cls = Kw;
		copy.to = save;
		copy.arg[0] = orig;
		copy.arg[1] = R;
		appendins(pre, copy);
	}
}

static void
elide_saved_copybacks(Fn *fn)
{
	Blk *b;
	Ins *i, *scan, *restore, *end;
	Ref save0, save1, src, other;
	bits watched;

	for (b=fn->start; b; b=b->link) {
		end = &b->ins[b->nins];
		for (i=b->ins; i!=end; i++) {
			if (i->op != Ocopy || !isreg(i->to) || !isreg(i->arg[0]))
				continue;
			save0 = i->to;
			src = i->arg[0];
			if (req(save0, src) || i + 3 >= end)
				continue;
			scan = i + 1;
			if (scan->op != Ocopy || scan->cls != i->cls
			|| !isreg(scan->to) || !isreg(scan->arg[0]) || !req(scan->to, src))
				continue;
			other = scan->arg[0];
			if (req(other, src) || req(other, save0))
				continue;
			watched = BIT(src.val) | BIT(save0.val) | BIT(other.val);
			for (restore=scan+1; restore!=end; restore++) {
				if (restore->op == Ocopy && restore->cls == i->cls
				&& isreg(restore->to) && isreg(restore->arg[0])
				&& req(restore->arg[0], src) && !req(restore->to, src)) {
					save1 = restore->to;
					if (req(save1, save0) || req(save1, other))
						break;
					if (restore + 1 == end
					|| !copy_from_to(restore + 1, src, save0, i->cls))
						break;
					scan->op = Onop;
					restore->arg[0] = other;
					restore[1].op = Onop;
					break;
				}
				if (restore->op == Onop)
					continue;
				if (restore->op != Ocopy || ins_touches_regs(fn, restore, watched))
					break;
			}
		}
	}
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
		if (e->reg & BIT(r))
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
		if (e->reg & BIT(bedrock_rclob[i])) {
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

static unsigned
saved_gpr_bitmap(E *e)
{
	unsigned bm;
	int i, r;

	bm = 0;
	for (i=0; bedrock_rclob[i]>=0; i++) {
		r = bedrock_rclob[i];
		if (!(e->reg & BIT(r)))
			continue;
		if (D0 <= r && r <= D7)
			bm |= 1u << (r - D0);
		else if (A0 <= r && r <= A7)
			bm |= 1u << (8 + r - A0);
		else if (!(F0 <= r && r <= F15))
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

static unsigned
saved_freg_bitmap(E *e)
{
	unsigned bm;
	int i, r;

	bm = 0;
	for (i=0; bedrock_rclob[i]>=0; i++) {
		r = bedrock_rclob[i];
		if ((e->reg & BIT(r)) && F0 <= r && r <= F15)
			bm |= 1u << (r - F0);
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
	unsigned gpr_bm, fpr_bm;

	gpr_bm = saved_gpr_bitmap(e);
	fpr_bm = saved_freg_bitmap(e);
	if (popcount16(gpr_bm) > 1) {
		fprintf(e->f, "\tPUSHM 0x%04x\n", gpr_bm);
	} else {
		for (i=0; bedrock_rclob[i]>=0; i++)
			if ((e->reg & BIT(bedrock_rclob[i]))
			&& D0 <= bedrock_rclob[i] && bedrock_rclob[i] <= A7)
				fprintf(e->f, "\tPUSH %s\n", rname(bedrock_rclob[i], Kl));
		if (e->uses_ascratch)
			fprintf(e->f, "\tPUSH A7\n");
		if (e->save_pad_reg >= 0)
			fprintf(e->f, "\tPUSH %s\n", rname(e->save_pad_reg, Kl));
	}
	if (fpr_bm)
		fprintf(e->f, "\tFPUSHM 0x%04x\n", fpr_bm);
}

static void
emitcallee_restores(E *e)
{
	int i;
	unsigned gpr_bm, fpr_bm;

	gpr_bm = saved_gpr_bitmap(e);
	fpr_bm = saved_freg_bitmap(e);
	if (fpr_bm)
		fprintf(e->f, "\tFPOPM 0x%04x\n", fpr_bm);
	if (popcount16(gpr_bm) > 1) {
		fprintf(e->f, "\tPOPM 0x%04x\n", gpr_bm);
	} else {
		if (e->uses_ascratch)
			fprintf(e->f, "\tPOP A7\n");
		if (e->save_pad_reg >= 0)
			fprintf(e->f, "\tPOP %s\n", rname(e->save_pad_reg, Kl));
		for (i=0; bedrock_rclob[i]>=0; i++)
			;
		while (i-- > 0)
			if ((e->reg & BIT(bedrock_rclob[i]))
			&& D0 <= bedrock_rclob[i] && bedrock_rclob[i] <= A7)
				fprintf(e->f, "\tPOP %s\n", rname(bedrock_rclob[i], Kl));
	}
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

typedef struct CountLoop CountLoop;
typedef struct RepeatMem RepeatMem;
typedef struct RepeatArg RepeatArg;
typedef struct RepeatOp RepeatOp;
typedef struct RepeatPlan RepeatPlan;
typedef struct RepeatStream RepeatStream;
typedef struct RepeatDecode RepeatDecode;

struct CountLoop {
	Blk *header;
	Blk *body;
	Blk *exit;
	Ref counter;
	Ref limit;
};

struct RepeatMem {
	Ref base;
	int64_t disp;
	int postinc;
};

enum {
	RpPlain,
	RpGroup,
	RpNE,
	RpGT,
};

enum {
	RpFinishAcc,
	RpFinishLimit,
	RpFinishDelta,
};

enum {
	RpaRef,
	RpaMem,
	RpaImm,
};

struct RepeatArg {
	int kind;
	Ref ref;
	RepeatMem mem;
	int64_t imm;
};

struct RepeatOp {
	const char *name;
	int cls;
	int sized;
	RepeatArg *arg;
	int nargs;
};

struct RepeatPlan {
	int mode;
	int finish;
	int copy_guard_to_count;
	int has_preclear;
	Ref guard;
	Ref count;
	Ref preclear;
	Ref ret;
	RepeatOp *op;
	int nops;
};

struct RepeatStream {
	Ref base;
	int size;
	int advanced;
	int postinc;
};

struct RepeatDecode {
	RepeatStream *stream;
	int nstream;
};

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
isaccsub(Ins *i, Ref acc, Ref src)
{
	if (i->op != Osub || i->cls != Kw || !req(i->to, acc))
		return 0;
	return req(i->arg[0], acc) && req(i->arg[1], src);
}

static int
indexedmem(Ref r, Ref counter, int scale, E *e, Ref *base, int64_t *disp)
{
	Mem *m;

	if (rtype(r) != RMem)
		return 0;
	m = &e->fn->mem[r.val];
	if (!req(m->index, counter) || m->scale != scale)
		return 0;
	if (rtype(m->base) != RTmp || !isreg(m->base) || !(A0 <= (int)m->base.val && (int)m->base.val <= A7))
		return 0;
	*base = m->base;
	*disp = conoffset(&m->offset);
	return 1;
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
isretcopyblock(Blk *b, Ref value, Blk **retb)
{
	Ins *copy;

	*retb = 0;
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
	*retb = b->s1;
	if (*retb == 0 || (*retb)->jmp.type != Jret0)
		return 0;
	return (*retb)->nins == 0
		|| ((*retb)->nins == 1 && (*retb)->ins[0].op == Ocopy
			&& (*retb)->ins[0].cls == Kw
			&& req((*retb)->ins[0].to, TMP(D0))
			&& req((*retb)->ins[0].arg[0], TMP(D0)));
}

static int
blockin(Blk **blocks, int n, Blk *b)
{
	int i;

	for (i=0; i<n; i++)
		if (blocks[i] == b)
			return 1;
	return 0;
}

static void
addblock(Blk **blocks, int *n, Blk *b)
{
	if (b != 0 && !blockin(blocks, *n, b))
		blocks[(*n)++] = b;
}

static int
privateblocks(Blk **blocks, int n, Blk *entry)
{
	Blk *b;
	uint i, j;

	for (i=0; i<(uint)n; i++) {
		b = blocks[i];
		if (b == entry)
			continue;
		for (j=0; j<b->npred; j++)
			if (!blockin(blocks, n, b->pred[j]))
				return 0;
	}
	return 1;
}

static void
markblocks(unsigned char *skip, Blk **blocks, int n, Blk *entry)
{
	int i;

	for (i=0; i<n; i++)
		if (blocks[i] != entry)
			skip[blocks[i]->id] = 1;
}

static void
emitoptlabel(E *e, Blk *b, int idbase, int need_label)
{
	if (need_label)
		fprintf(e->f, ".Lbb%d:\n", idbase + b->id);
}

static void
emitret(E *e)
{
	emitframe(e, 1);
	fprintf(e->f, "\tRET\n");
}

static void
notereplref(E *e, Ref r)
{
	if (rtype(r) == RTmp && isreg(r))
		e->replacement_reg |= BIT(r.val);
}

static RepeatMem
repmem(Ref base, int64_t disp, int postinc)
{
	RepeatMem m;

	m.base = base;
	m.disp = disp;
	m.postinc = postinc;
	return m;
}

static void
repinit(RepeatPlan *p, int mode, int finish, Ref guard, Ref count)
{
	memset(p, 0, sizeof *p);
	p->mode = mode;
	p->finish = finish;
	p->guard = guard;
	p->count = count;
	p->op = vnew(0, sizeof p->op[0], Pfn);
}

static void
repeatdecodeinit(RepeatDecode *d)
{
	memset(d, 0, sizeof *d);
	d->stream = vnew(0, sizeof d->stream[0], Pfn);
}

static RepeatDecode
repeatdecodesnapshot(RepeatDecode *d)
{
	RepeatDecode save;

	save.nstream = d->nstream;
	save.stream = vnew((ulong)d->nstream, sizeof save.stream[0], Pfn);
	if (d->nstream)
		memcpy(save.stream, d->stream, d->nstream * sizeof save.stream[0]);
	return save;
}

static void
reppreclear(RepeatPlan *p, Ref r)
{
	p->has_preclear = 1;
	p->preclear = r;
}

static RepeatOp *
repop(RepeatPlan *p, const char *name, int cls, int sized)
{
	RepeatOp *op;

	vgrow(&p->op, (ulong)p->nops + 1);
	op = &p->op[p->nops++];
	memset(op, 0, sizeof *op);
	op->name = name;
	op->cls = cls;
	op->sized = sized;
	op->arg = vnew(0, sizeof op->arg[0], Pfn);
	return op;
}

static void
reparg(RepeatOp *op, int kind)
{
	vgrow(&op->arg, (ulong)op->nargs + 1);
	memset(&op->arg[op->nargs], 0, sizeof op->arg[op->nargs]);
	op->arg[op->nargs].kind = kind;
	op->nargs++;
}

static void
repargref(RepeatOp *op, Ref ref)
{
	reparg(op, RpaRef);
	op->arg[op->nargs-1].ref = ref;
}

static void
repargmem(RepeatOp *op, RepeatMem mem)
{
	reparg(op, RpaMem);
	op->arg[op->nargs-1].mem = mem;
}

static void
repargimm(RepeatOp *op, int64_t imm)
{
	reparg(op, RpaImm);
	op->arg[op->nargs-1].imm = imm;
}

static void
noterepmem(E *e, RepeatMem m)
{
	notereplref(e, m.base);
}

static void
notereparg(E *e, RepeatArg *arg)
{
	switch (arg->kind) {
	case RpaRef:
		notereplref(e, arg->ref);
		break;
	case RpaMem:
		noterepmem(e, arg->mem);
		break;
	case RpaImm:
		break;
	default:
		die("unknown repeat operand");
	}
}

static void
noterepop(E *e, RepeatOp *op)
{
	int i;

	for (i=0; i<op->nargs; i++)
		notereparg(e, &op->arg[i]);
}

static void
noterepplan(E *e, RepeatPlan *p)
{
	int i;

	notereplref(e, p->guard);
	notereplref(e, p->count);
	if (p->finish == RpFinishAcc)
		notereplref(e, p->ret);
	if (p->has_preclear)
		notereplref(e, p->preclear);
	for (i=0; i<p->nops; i++)
		noterepop(e, &p->op[i]);
}

static void
emitrepmem(FILE *f, RepeatMem m)
{
	fprintf(f, "[%s", rname(m.base.val, Kl));
	if (m.postinc) {
		fprintf(f, "++]");
		return;
	}
	if (m.disp)
		fprintf(f, " + %"PRId64, m.disp);
	fprintf(f, "]");
}

static void
emitreparg(E *e, RepeatOp *op, RepeatArg *arg)
{
	switch (arg->kind) {
	default:
		die("unknown repeat operand");
	case RpaRef:
		fprintf(e->f, "%s", rname(arg->ref.val, op->cls));
		break;
	case RpaMem:
		emitrepmem(e->f, arg->mem);
		break;
	case RpaImm:
		fprintf(e->f, "%"PRId64, arg->imm);
		break;
	}
}

static void
emitrepop(E *e, RepeatOp *op)
{
	int i;

	if (op->name == 0)
		die("unnamed repeat operation");
	fprintf(e->f, "%s", op->name);
	if (op->sized)
		fprintf(e->f, ".%c", siz(op->cls));
	if (op->nargs)
		fprintf(e->f, " ");
	for (i=0; i<op->nargs; i++) {
		if (i)
			fprintf(e->f, ", ");
		emitreparg(e, op, &op->arg[i]);
	}
	fprintf(e->f, "\n");
}

static char *
repopname(int mode)
{
	switch (mode) {
	default:
		die("unknown repeat mode");
	case RpPlain:
		return "REP";
	case RpNE:
		return "REPNE";
	case RpGT:
		return "REPGT";
	}
}

static void
emitrepops(E *e, RepeatPlan *p)
{
	int i;

	if (p->mode == RpGroup) {
		fprintf(e->f, "\tREPG %s, {\n", rname(p->count.val, Kw));
		for (i=0; i<p->nops; i++) {
			fprintf(e->f, "\t\t");
			emitrepop(e, &p->op[i]);
		}
		fprintf(e->f, "\t}\n");
		return;
	}
	if (p->nops != 1)
		die("non-group repeat must have exactly one operation");
	fprintf(e->f, "\t%s %s, ", repopname(p->mode), rname(p->count.val, Kw));
	emitrepop(e, &p->op[0]);
}

static int
emitrepplan(E *e, Blk *entry, int idbase, unsigned char *skip,
	int need_label, Blk **blocks, int n, RepeatPlan *p)
{
	int tag;

	if (!privateblocks(blocks, n, entry))
		return 0;
	tag = idbase + entry->id;
	noterepplan(e, p);
	emitoptlabel(e, entry, idbase, need_label);
	if (p->has_preclear)
		fprintf(e->f, "\tCLR %s\n", rname(p->preclear.val, Kw));
	fprintf(e->f, "\tTEST.L %s, %s\n", rname(p->guard.val, Kw), rname(p->guard.val, Kw));
	fprintf(e->f, "\tJLE.W .Lrepzero%d@WORD_PCREL16\n", tag);
	if (p->copy_guard_to_count)
		fprintf(e->f, "\tMOV.L %s, %s\n", rname(p->guard.val, Kw), rname(p->count.val, Kw));
	emitrepops(e, p);
	switch (p->finish) {
	case RpFinishAcc:
		fprintf(e->f, ".Lrepzero%d:\n", tag);
		if (!req(p->ret, TMP(D0)))
			fprintf(e->f, "\tMOV.L %s, D0\n", rname(p->ret.val, Kw));
		emitret(e);
		break;
	case RpFinishLimit:
		if (!req(p->guard, TMP(D0)))
			fprintf(e->f, "\tMOV.L %s, D0\n", rname(p->guard.val, Kw));
		emitret(e);
		fprintf(e->f, ".Lrepzero%d:\n", tag);
		fprintf(e->f, "\tCLR D0\n");
		emitret(e);
		break;
	case RpFinishDelta:
		if (!req(p->guard, TMP(D0)))
			fprintf(e->f, "\tMOV.L %s, D0\n", rname(p->guard.val, Kw));
		fprintf(e->f, "\tSUB.L %s, D0\n", rname(p->count.val, Kw));
		emitret(e);
		fprintf(e->f, ".Lrepzero%d:\n", tag);
		fprintf(e->f, "\tCLR D0\n");
		emitret(e);
		break;
	default:
		die("unknown repeat finish");
	}
	markblocks(skip, blocks, n, entry);
	return 1;
}

static int
repeatclsbytes(int cls)
{
	switch (cls) {
	default:
		return 0;
	case Kw:
	case Ks:
		return 4;
	case Kl:
	case Kd:
		return 8;
	}
}

static int
repeatstorecls(int op, int *cls)
{
	switch (op) {
	default:
		return 0;
	case Ostorew:
		*cls = Kw;
		return 1;
	case Ostorel:
		*cls = Kl;
		return 1;
	}
}

static RepeatStream *
repeatstream(RepeatDecode *d, Ref base, int size)
{
	RepeatStream *s;
	int i;

	for (i=0; i<d->nstream; i++) {
		s = &d->stream[i];
		if (req(s->base, base) && s->size == size)
			return s;
	}
	vgrow(&d->stream, (ulong)d->nstream + 1);
	s = &d->stream[d->nstream++];
	memset(s, 0, sizeof *s);
	s->base = base;
	s->size = size;
	return s;
}

static int
repeatmemfor(RepeatDecode *d, Ref mem, Ref counter, int cls, E *e, RepeatMem *out)
{
	RepeatStream *s;
	Ref base;
	int size;
	int64_t disp, adj;

	size = repeatclsbytes(cls);
	if (size == 0 || !indexedmem(mem, counter, size, e, &base, &disp))
		return 0;
	s = repeatstream(d, base, size);
	if (s == 0)
		return 0;
	adj = disp - s->advanced;
	if (!s->postinc && adj == 0) {
		*out = repmem(base, 0, 1);
		s->postinc = 1;
		s->advanced += size;
		return 1;
	}
	if (adj < 0)
		return 0;
	*out = repmem(base, adj, 0);
	return 1;
}

static int
repeatstreamscomplete(RepeatDecode *d)
{
	int i;

	for (i=0; i<d->nstream; i++)
		if (!d->stream[i].postinc)
			return 0;
	return 1;
}

static int
repeataddreg(Ins *i, Ref *src, Ref *dst)
{
	if (i->op != Oadd || KBASE(i->cls) != 0 || !isdreg(i->to))
		return 0;
	if (req(i->arg[0], i->to) && isdreg(i->arg[1])) {
		*src = i->arg[1];
		*dst = i->to;
		return 1;
	}
	if (req(i->arg[1], i->to) && isdreg(i->arg[0])) {
		*src = i->arg[0];
		*dst = i->to;
		return 1;
	}
	return 0;
}

static int
repeatmulreg(Ins *i, Ref *src, Ref *dst)
{
	if (i->op != Omul || KBASE(i->cls) != 0 || !isdreg(i->to))
		return 0;
	if (req(i->arg[0], i->to) && isdreg(i->arg[1])) {
		*src = i->arg[1];
		*dst = i->to;
		return 1;
	}
	if (req(i->arg[1], i->to) && isdreg(i->arg[0])) {
		*src = i->arg[0];
		*dst = i->to;
		return 1;
	}
	return 0;
}

static int
appendrepeatloadstore(RepeatDecode *d, RepeatPlan *p, Ins *i, Ins *end,
	Ref counter, E *e, int *used)
{
	RepeatDecode save;
	RepeatOp *op;
	RepeatMem src, dst;
	Ins *load, *store;
	int cls, nops;

	if (end - i < 2)
		return 0;
	load = i;
	store = i + 1;
	if (load->op != Oload || KBASE(load->cls) != 0)
		return 0;
	cls = load->cls;
	if (store->op != store_op_for_cls(cls) || !req(store->arg[0], load->to))
		return 0;
	save = repeatdecodesnapshot(d);
	nops = p->nops;
	if (!repeatmemfor(d, load->arg[0], counter, cls, e, &src)
	|| !repeatmemfor(d, store->arg[1], counter, cls, e, &dst)) {
		*d = save;
		p->nops = nops;
		return 0;
	}
	op = repop(p, "MOV", cls, 1);
	repargmem(op, src);
	repargmem(op, dst);
	*used = 2;
	return 1;
}

static int
appendrepeatloadadd(RepeatDecode *d, RepeatPlan *p, Ins *i, Ins *end,
	Ref counter, E *e, int *used)
{
	RepeatOp *op;
	RepeatMem mem;
	Ins *load, *add;
	Ref acc;

	if (end - i < 2)
		return 0;
	load = i;
	add = i + 1;
	if (load->op != Oload || KBASE(load->cls) != 0 || add->op != Oadd || add->cls != load->cls)
		return 0;
	if (!op_allows_memfold(add->op, add->to, add->arg[0], add->arg[1], load->to, &acc)
	|| !isdreg(acc) || !ref_dead_after(e->fn, load->to, add+1, end))
		return 0;
	if (!repeatmemfor(d, load->arg[0], counter, load->cls, e, &mem))
		return 0;
	op = repop(p, "ADD", load->cls, 1);
	repargmem(op, mem);
	repargref(op, acc);
	*used = 2;
	return 1;
}

static int
appendrepeatdot(RepeatDecode *d, RepeatPlan *p, Ins *i, Ins *end,
	Ref counter, E *e, int *used)
{
	RepeatDecode save;
	RepeatOp *op;
	RepeatMem mem0, mem1;
	Ins *load0, *load1, *mul, *add;
	Ref acc, tmp;
	int nops;

	if (end - i < 4)
		return 0;
	load0 = i;
	load1 = i + 1;
	mul = i + 2;
	add = i + 3;
	if (load0->op != Oload || load0->cls != Kw
	|| load1->op != Oload || load1->cls != Kw
	|| !isdreg(load0->to) || !isdreg(load1->to)
	|| !ismul2(mul, load0->to, load1->to)
	|| !isaccadd(add, add->to, mul->to)
	|| !isdreg(add->to))
		return 0;
	acc = add->to;
	if (!req(add->to, add->arg[0]) && !req(add->to, add->arg[1]))
		return 0;
	save = repeatdecodesnapshot(d);
	nops = p->nops;
	if (!repeatmemfor(d, load1->arg[0], counter, Kw, e, &mem1)
	|| !repeatmemfor(d, load0->arg[0], counter, Kw, e, &mem0)) {
		*d = save;
		p->nops = nops;
		return 0;
	}
	tmp = load1->to;
	op = repop(p, "MOV", Kw, 1);
	repargmem(op, mem1);
	repargref(op, tmp);
	op = repop(p, "MADD", Kw, 1);
	repargmem(op, mem0);
	repargref(op, tmp);
	repargref(op, acc);
	*used = 4;
	return 1;
}

static int
appendrepeatmaddchain(RepeatDecode *d, RepeatPlan *p, Ins *i, Ins *end,
	Ref counter, E *e, int *used)
{
	RepeatDecode save;
	RepeatMem *mem, dst;
	RepeatOp *op;
	Ref *val, coeff, acc;
	Ins *scan;
	int nload, nops, k, storecls;

	save = repeatdecodesnapshot(d);
	nops = p->nops;
	mem = vnew(0, sizeof mem[0], Pfn);
	val = vnew(0, sizeof val[0], Pfn);
	nload = 0;
	scan = i;
	while (scan != end && scan->op == Oload && scan->cls == Kw && isdreg(scan->to)) {
		vgrow(&mem, (ulong)nload + 1);
		vgrow(&val, (ulong)nload + 1);
		if (!repeatmemfor(d, scan->arg[0], counter, Kw, e, &mem[nload]))
			goto Fail;
		val[nload++] = scan->to;
		scan++;
	}
	if (nload < 2 || scan == end || !ismulacc(scan, val[0], &coeff))
		goto Fail;
	acc = val[0];
	op = repop(p, "CLR", Kw, 0);
	repargref(op, acc);
	op = repop(p, "MADD", Kw, 1);
	repargmem(op, mem[0]);
	repargref(op, coeff);
	repargref(op, acc);
	scan++;
	for (k=1; k<nload; k++) {
		if (scan == end || !ismulacc(scan, val[k], &coeff))
			goto Fail;
		scan++;
		if (scan == end || !isaccadd(scan, acc, val[k]))
			goto Fail;
		op = repop(p, "MADD", Kw, 1);
		repargmem(op, mem[k]);
		repargref(op, coeff);
		repargref(op, acc);
		scan++;
	}
	if (scan == end || !repeatstorecls(scan->op, &storecls) || storecls != Kw
	|| !req(scan->arg[0], acc)
	|| !repeatmemfor(d, scan->arg[1], counter, Kw, e, &dst))
		goto Fail;
	op = repop(p, "MOV", Kw, 1);
	repargref(op, acc);
	repargmem(op, dst);
	*used = (int)(scan - i) + 1;
	return 1;

Fail:
	*d = save;
	p->nops = nops;
	return 0;
}

static int
appendrepeatins(RepeatDecode *d, RepeatPlan *p, Ins *i, Ins *end,
	Ref counter, E *e, int *used)
{
	RepeatOp *op;
	RepeatMem mem;
	Ref src, dst;
	int64_t imm;
	int cls;

	*used = 1;
	if (appendrepeatmaddchain(d, p, i, end, counter, e, used)
	|| appendrepeatdot(d, p, i, end, counter, e, used)
	|| appendrepeatloadstore(d, p, i, end, counter, e, used)
	|| appendrepeatloadadd(d, p, i, end, counter, e, used))
		return 1;
	switch (i->op) {
	default:
		return 0;
	case Onop:
		return 1;
	case Oload:
		if (KBASE(i->cls) != 0 || !isdreg(i->to)
		|| !repeatmemfor(d, i->arg[0], counter, i->cls, e, &mem))
			return 0;
		op = repop(p, "MOV", i->cls, 1);
		repargmem(op, mem);
		repargref(op, i->to);
		return 1;
	case Ocopy:
		if (!isdreg(i->to))
			return 0;
		if (isconval(i->arg[0], e, 0)) {
			op = repop(p, "CLR", i->cls, 0);
			repargref(op, i->to);
			return 1;
		}
		if (!isdreg(i->arg[0]))
			return 0;
		op = repop(p, "MOV", i->cls, 1);
		repargref(op, i->arg[0]);
		repargref(op, i->to);
		return 1;
	case Oadd:
		if (isincreg(i, i->to, e)) {
			op = repop(p, "INC", i->cls, 1);
			repargref(op, i->to);
			return 1;
		}
		if (!repeataddreg(i, &src, &dst))
			return 0;
		op = repop(p, "ADD", i->cls, 1);
		repargref(op, src);
		repargref(op, dst);
		return 1;
	case Omul:
		if (!repeatmulreg(i, &src, &dst))
			return 0;
		op = repop(p, "MULU", i->cls, 1);
		repargref(op, src);
		repargref(op, dst);
		return 1;
	case Oshl:
		if (!isdreg(i->to) || !req(i->arg[0], i->to) || !isbits(i->arg[1], e, &imm))
			return 0;
		op = repop(p, "SHL", i->cls, 1);
		repargimm(op, imm);
		repargref(op, i->to);
		return 1;
	case Ostorew:
	case Ostorel:
		if (!repeatstorecls(i->op, &cls) || !isdreg(i->arg[0])
		|| !repeatmemfor(d, i->arg[1], counter, cls, e, &mem))
			return 0;
		op = repop(p, "MOV", cls, 1);
		repargref(op, i->arg[0]);
		repargmem(op, mem);
		return 1;
	}
}

static int
decoderepeatbody(RepeatPlan *p, Ins *start, Ins *end, Ref counter, E *e)
{
	RepeatDecode d;
	Ins *i;
	int used;

	repeatdecodeinit(&d);
	for (i=start; i!=end; i+=used) {
		if (!appendrepeatins(&d, p, i, end, counter, e, &used))
			return 0;
		if (used <= 0 || i + used > end)
			return 0;
	}
	return repeatstreamscomplete(&d);
}

static bits
normalemittedregs(Fn *fn, unsigned char *skip)
{
	Blk *b;
	Ins *i;
	bits regs;

	regs = 0;
	for (b=fn->start; b; b=b->link) {
		if (skip[b->id])
			continue;
		for (i=b->ins; i!=&b->ins[b->nins]; i++) {
			if (i->op == Onop)
				continue;
			if (rtype(i->to) == RTmp && isreg(i->to))
				regs |= BIT(i->to.val);
			regs |= ref_reg_bits(fn, i->arg[0]);
			regs |= ref_reg_bits(fn, i->arg[1]);
		}
		regs |= ref_reg_bits(fn, b->jmp.arg);
	}
	return regs;
}

static int
folded_load_tmp(Ins *load, Ins *end, E *e, int *skipidx)
{
	Ins *inc, *op;
	Ref acc;
	char *name;
	int reg, size;

	if (load->op != Oload || KBASE(load->cls) != 0 || !isintreg(load->to) || isdreg(load->to))
		return 0;
	size = postinc_size(load);
	if (size == 0 || !direct_areg_ref(load->arg[0], &reg) || req(load->to, TMP(reg)))
		return 0;
	inc = findpostincadd(load, end, reg, size, e);
	if (inc == 0)
		return 0;
	if (inc == load+1) {
		if (inc+1 == end)
			return 0;
		op = inc + 1;
	} else {
		op = load + 1;
		if (op == end || op == inc)
			return 0;
	}
	name = alu_op_name(op->op);
	if (name == 0 || op->cls != load->cls)
		return 0;
	if (!op_allows_memfold(op->op, op->to, op->arg[0], op->arg[1], load->to, &acc))
		return 0;
	if (!isdreg(acc) || !ref_dead_after(e->fn, load->to, op+1, end))
		return 0;
	*skipidx = (int)(op - load);
	return 1;
}

static int
reg_only_folded_load_tmp(E *e, unsigned char *skip, int reg)
{
	Blk *b;
	Ins *i, *end;
	int idx, skip_use;

	for (b=e->fn->start; b; b=b->link) {
		if (skip[b->id])
			continue;
		end = &b->ins[b->nins];
		skip_use = -1;
		for (i=b->ins, idx=0; i!=end; i++, idx++) {
			if (idx == skip_use) {
				if (ins_touches_regs(e->fn, i, BIT(reg)))
					continue;
				skip_use = -1;
			}
			if (!ins_touches_regs(e->fn, i, BIT(reg)))
				continue;
			if (i->op == Oload && req(i->to, TMP(reg))
			&& folded_load_tmp(i, end, e, &skip_use)) {
				skip_use += idx;
				continue;
			}
			return 0;
		}
	}
	return 1;
}

static bits
foldedtmpregs(E *e, unsigned char *skip)
{
	bits regs;
	int i, r;

	regs = 0;
	for (i=0; bedrock_rclob[i]>=0; i++) {
		r = bedrock_rclob[i];
		if ((e->fn->reg & BIT(r)) && reg_only_folded_load_tmp(e, skip, r))
			regs |= BIT(r);
	}
	return regs;
}

static int
matchcountloop(Blk *init, CountLoop *loop)
{
	Blk *header;
	Ins *cmp;
	int cond;

	if (init == 0 || init->jmp.type != Jjmp || init->s1 == 0)
		return 0;
	header = init->s1;
	if (header->nins != 1 || header->s1 == 0 || header->s2 == 0)
		return 0;
	cmp = &header->ins[0];
	cond = header->jmp.type - Jjf;
	if (cmp->op != Oacmp || cmp->cls != Kw || (cond != Cislt && cond != Cisge))
		return 0;
	loop->header = header;
	loop->counter = cmp->arg[0];
	loop->limit = cmp->arg[1];
	if (cond == Cislt) {
		loop->body = header->s1;
		loop->exit = header->s2;
	} else {
		loop->body = header->s2;
		loop->exit = header->s1;
	}
	return loop->body != 0 && loop->exit != 0;
}

static int
zeroinits(Blk *entry, Ref **zero, int *nzero, E *e)
{
	uint i;

	*nzero = 0;
	*zero = 0;
	if (entry->nins == 0)
		return 0;
	*zero = vnew(entry->nins, sizeof (*zero)[0], Pfn);
	for (i=0; i<entry->nins; i++)
		if (!isregcopyzero(&entry->ins[i], &(*zero)[i], e))
			return 0;
	*nzero = entry->nins;
	return 1;
}

static int
findzero(Ref *zero, int nzero, Ref r)
{
	int i;

	for (i=0; i<nzero; i++)
		if (req(zero[i], r))
			return i;
	return -1;
}

static int
repeatretvalue(Blk *exit, Ref *zero, int nzero, Ref counter, Ref *ret, Blk **retb)
{
	int i;

	if (isretcopyblock(exit, counter, retb)) {
		*ret = counter;
		return RpFinishLimit;
	}
	for (i=0; i<nzero; i++) {
		if (req(zero[i], counter))
			continue;
		if (isretcopyblock(exit, zero[i], retb)) {
			*ret = zero[i];
			return RpFinishAcc;
		}
	}
	return -1;
}

static int
emit_repeat_straight_loop(E *e, Blk *entry, int idbase, unsigned char *skip, int need_label)
{
	CountLoop l;
	Blk *blocks[8], *retb;
	Ins *inc;
	Ref *zero, ret;
	RepeatPlan p;
	int finish, n, nzero;

	if (!zeroinits(entry, &zero, &nzero, e) || !matchcountloop(entry, &l))
		return 0;
	if (findzero(zero, nzero, l.counter) < 0 || !isdreg(l.counter) || !isdreg(l.limit))
		return 0;
	if (l.body->nins < 2 || l.body->jmp.type != Jjmp || l.body->s1 != l.header)
		return 0;
	inc = &l.body->ins[l.body->nins - 1];
	if (!iscountinc(inc, l.counter, e))
		return 0;
	finish = repeatretvalue(l.exit, zero, nzero, l.counter, &ret, &retb);
	if (finish < 0)
		return 0;
	repinit(&p, RpGroup, finish, l.limit, finish == RpFinishAcc ? l.limit : l.counter);
	if (finish == RpFinishAcc) {
		reppreclear(&p, ret);
		p.ret = ret;
	} else {
		p.copy_guard_to_count = 1;
	}
	if (!decoderepeatbody(&p, l.body->ins, inc, l.counter, e))
		return 0;
	if (p.nops == 0)
		return 0;
	if (p.nops == 1)
		p.mode = RpPlain;
	n = 0;
	addblock(blocks, &n, entry);
	addblock(blocks, &n, l.header);
	addblock(blocks, &n, l.body);
	addblock(blocks, &n, l.exit);
	addblock(blocks, &n, retb);
	return emitrepplan(e, entry, idbase, skip, need_label, blocks, n, &p);
}

static int
emit_repeat_zero_break_loop(E *e, Blk *entry, int idbase, unsigned char *skip, int need_label)
{
	CountLoop l;
	Blk *blocks[12], *retb0, *retb1, *found, *incb, *raw_found, *raw_incb;
	Ins *test, *inc;
	Ref *zero, counter, tmp;
	RepeatPlan p;
	int n, nzero, testcond;

	if (!zeroinits(entry, &zero, &nzero, e) || nzero != 1 || !matchcountloop(entry, &l))
		return 0;
	counter = zero[0];
	if (!req(l.counter, counter) || !isdreg(counter) || !isdreg(l.limit))
		return 0;
	if (l.body->nins < 2 || l.body->s1 == 0 || l.body->s2 == 0)
		return 0;
	test = &l.body->ins[l.body->nins - 1];
	testcond = l.body->jmp.type - Jjf;
	if (test->op != Oacmp || test->cls != Kw || !isdreg(test->arg[0])
	|| !isconval(test->arg[1], e, 0) || (testcond != Cieq && testcond != Cine))
		return 0;
	tmp = test->arg[0];
	if (testcond == Cieq) {
		raw_found = l.body->s1;
		raw_incb = l.body->s2;
	} else {
		raw_found = l.body->s2;
		raw_incb = l.body->s1;
	}
	found = skipbarejump(raw_found);
	incb = skipbarejump(raw_incb);
	if (!isretcopyblock(found, counter, &retb0))
		return 0;
	if (incb == 0 || incb->nins != 1 || incb->jmp.type != Jjmp || incb->s1 != l.header)
		return 0;
	inc = &incb->ins[0];
	if (!iscountinc(inc, counter, e) || !isretcopyblock(l.exit, counter, &retb1))
		return 0;
	repinit(&p, RpNE, RpFinishDelta, l.limit, counter);
	p.copy_guard_to_count = 1;
	if (!decoderepeatbody(&p, l.body->ins, test, counter, e) || p.nops != 1)
		return 0;
	if (strcmp(p.op[0].name, "MOV") == 0
	&& p.op[0].nargs == 2
	&& p.op[0].arg[0].kind == RpaMem
	&& p.op[0].arg[1].kind == RpaRef
	&& !req(p.op[0].arg[1].ref, tmp))
		return 0;
	n = 0;
	addblock(blocks, &n, entry);
	addblock(blocks, &n, l.header);
	addblock(blocks, &n, l.body);
	addblock(blocks, &n, raw_found);
	addblock(blocks, &n, raw_incb);
	addblock(blocks, &n, found);
	addblock(blocks, &n, incb);
	addblock(blocks, &n, l.exit);
	addblock(blocks, &n, retb0);
	addblock(blocks, &n, retb1);
	return emitrepplan(e, entry, idbase, skip, need_label, blocks, n, &p);
}

static int
emit_repeat_threshold_break_loop(E *e, Blk *entry, int idbase, unsigned char *skip, int need_label)
{
	CountLoop l;
	Blk *blocks[10], *retb, *taken, *fall, *raw_taken, *raw_fall;
	Ins *load, *inc, *test;
	Ref *zero, counter, threshold, tmp;
	RepeatDecode d;
	RepeatMem mem;
	RepeatPlan p;
	RepeatOp *op;
	int n, nzero, testcond;

	if (!zeroinits(entry, &zero, &nzero, e) || nzero != 1 || !matchcountloop(entry, &l))
		return 0;
	counter = zero[0];
	if (!req(l.counter, counter) || !isdreg(counter) || !isdreg(l.limit))
		return 0;
	if (l.body->nins != 3 || l.body->s1 == 0 || l.body->s2 == 0)
		return 0;
	load = &l.body->ins[0];
	inc = &l.body->ins[1];
	test = &l.body->ins[2];
	testcond = l.body->jmp.type - Jjf;
	if (load->op != Oload || load->cls != Kw || !isdreg(load->to)
	|| !iscountinc(inc, counter, e)
	|| test->op != Oacmp || test->cls != Kw || testcond != Cisle)
		return 0;
	tmp = load->to;
	threshold = test->arg[0];
	if (!isdreg(threshold) || !req(test->arg[1], tmp)
	|| req(threshold, counter) || req(threshold, l.limit) || req(threshold, tmp))
		return 0;
	raw_taken = l.body->s1;
	raw_fall = l.body->s2;
	taken = skipbarejump(raw_taken);
	fall = skipbarejump(raw_fall);
	if (taken != l.exit || fall != l.header || !isretcopyblock(l.exit, counter, &retb))
		return 0;
	repeatdecodeinit(&d);
	if (!repeatmemfor(&d, load->arg[0], counter, Kw, e, &mem)
	|| !repeatstreamscomplete(&d))
		return 0;
	repinit(&p, RpGT, RpFinishDelta, l.limit, counter);
	p.copy_guard_to_count = 1;
	op = repop(&p, "CMP", Kw, 1);
	repargmem(op, mem);
	repargref(op, threshold);
	n = 0;
	addblock(blocks, &n, entry);
	addblock(blocks, &n, l.header);
	addblock(blocks, &n, l.body);
	addblock(blocks, &n, raw_taken);
	addblock(blocks, &n, raw_fall);
	addblock(blocks, &n, l.exit);
	addblock(blocks, &n, retb);
	return emitrepplan(e, entry, idbase, skip, need_label, blocks, n, &p);
}

static int
emit_repeat_break_loop(E *e, Blk *entry, int idbase, unsigned char *skip, int need_label)
{
	return emit_repeat_zero_break_loop(e, entry, idbase, skip, need_label)
		|| emit_repeat_threshold_break_loop(e, entry, idbase, skip, need_label);
}

static int
emit_repeat_abs_diamond_loop(E *e, Blk *entry, int idbase, unsigned char *skip, int need_label)
{
	CountLoop l;
	Blk *blocks[12], *retb, *posb, *negb, *join0, *join1, *join;
	Ins *load, *test, *add, *sub, *inc;
	Ref zero0, zero1, counter, acc, tmp;
	RepeatDecode d;
	RepeatMem mem;
	RepeatPlan p;
	RepeatOp *op;
	int n, testcond;

	if (entry->nins != 2 || !matchcountloop(entry, &l))
		return 0;
	if (!isregcopyzero(&entry->ins[0], &zero0, e) || !isregcopyzero(&entry->ins[1], &zero1, e))
		return 0;
	if (!req(l.counter, zero0) && !req(l.counter, zero1))
		return 0;
	counter = l.counter;
	acc = req(counter, zero0) ? zero1 : zero0;
	if (!isdreg(counter) || !isdreg(acc) || !isdreg(l.limit)
	|| req(l.limit, counter) || req(l.limit, acc))
		return 0;
	if (l.body->nins != 2 || l.body->s1 == 0 || l.body->s2 == 0)
		return 0;
	load = &l.body->ins[0];
	test = &l.body->ins[1];
	if (load->op != Oload || load->cls != Kw)
		return 0;
	tmp = load->to;
	testcond = l.body->jmp.type - Jjf;
	if (!isdreg(tmp) || req(tmp, counter) || req(tmp, acc) || req(tmp, l.limit)
	|| test->op != Oacmp || test->cls != Kw || !req(test->arg[0], tmp)
	|| !isconval(test->arg[1], e, 0) || (testcond != Cisgt && testcond != Cisle))
		return 0;
	if (testcond == Cisgt) {
		posb = l.body->s1;
		negb = l.body->s2;
	} else {
		posb = l.body->s2;
		negb = l.body->s1;
	}
	if (posb == 0 || negb == 0 || posb->nins != 1 || negb->nins != 1
	|| posb->jmp.type != Jjmp || negb->jmp.type != Jjmp)
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
	if (join->nins != 1 || join->jmp.type != Jjmp || join->s1 != l.header)
		return 0;
	inc = &join->ins[0];
	if (!iscountinc(inc, counter, e) || !isretcopyblock(l.exit, acc, &retb))
		return 0;
	n = 0;
	addblock(blocks, &n, entry);
	addblock(blocks, &n, l.header);
	addblock(blocks, &n, l.body);
	addblock(blocks, &n, posb);
	addblock(blocks, &n, negb);
	addblock(blocks, &n, posb->s1);
	addblock(blocks, &n, negb->s1);
	addblock(blocks, &n, join);
	addblock(blocks, &n, l.exit);
	addblock(blocks, &n, retb);
	repeatdecodeinit(&d);
	if (!repeatmemfor(&d, load->arg[0], counter, Kw, e, &mem)
	|| !repeatstreamscomplete(&d))
		return 0;
	repinit(&p, RpGroup, RpFinishAcc, l.limit, l.limit);
	reppreclear(&p, acc);
	p.ret = acc;
	op = repop(&p, "MOV", Kw, 1);
	repargmem(op, mem);
	repargref(op, tmp);
	op = repop(&p, "ABS", Kw, 1);
	repargref(op, tmp);
	op = repop(&p, "ADD", Kw, 1);
	repargref(op, tmp);
	repargref(op, acc);
	return emitrepplan(e, entry, idbase, skip, need_label, blocks, n, &p);
}

static int
emit_repeat_clamp_diamond_loop(E *e, Blk *entry, int idbase, unsigned char *skip, int need_label)
{
	CountLoop l;
	Blk *blocks[14], *retb, *init, *lowcopy, *highb, *highcopy, *storeb;
	Ins *load, *lowcmp, *highcmp, *store, *inc;
	Ref counter, tmp, low, high, sw0, sw1;
	RepeatDecode d;
	RepeatMem srcmem, dstmem;
	RepeatPlan p;
	RepeatOp *op;
	int n, has_swap, lowcond, highcond;

	has_swap = 0;
	init = entry;
	if (entry->nins == 1 && entry->ins[0].op == Oswap && entry->ins[0].cls == Kw) {
		if (!isdreg(entry->ins[0].arg[0]) || !isdreg(entry->ins[0].arg[1])
		|| entry->jmp.type != Jjmp || entry->s1 == 0)
			return 0;
		has_swap = 1;
		sw0 = entry->ins[0].arg[0];
		sw1 = entry->ins[0].arg[1];
		init = entry->s1;
	}
	if (init->nins != 1 || !matchcountloop(init, &l))
		return 0;
	if (!isregcopyzero(&init->ins[0], &counter, e) || !isdreg(counter) || !req(l.counter, counter) || !isdreg(l.limit))
		return 0;
	if (l.body->nins != 2 || l.body->s1 == 0 || l.body->s2 == 0)
		return 0;
	load = &l.body->ins[0];
	lowcmp = &l.body->ins[1];
	if (load->op != Oload || load->cls != Kw)
		return 0;
	tmp = load->to;
	lowcond = l.body->jmp.type - Jjf;
	if (!isdreg(tmp) || req(tmp, counter) || req(tmp, l.limit)
	|| lowcmp->op != Oacmp || lowcmp->cls != Kw || lowcond != Cislt
	|| !req(lowcmp->arg[0], tmp) || !isdreg(lowcmp->arg[1]))
		return 0;
	low = lowcmp->arg[1];
	lowcopy = l.body->s1;
	highb = l.body->s2;
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
	if (!iscopyjumpblock(lowcopy, tmp, low, highb)
	|| !iscopyjumpblock(highcopy, tmp, high, storeb)
	|| storeb == 0 || storeb->nins != 2 || storeb->jmp.type != Jjmp || storeb->s1 != l.header)
		return 0;
	store = &storeb->ins[0];
	inc = &storeb->ins[1];
	if (store->op != Ostorew || !req(store->arg[0], tmp)
	|| !iscountinc(inc, counter, e)
	|| !isretcopyblock(l.exit, counter, &retb))
		return 0;
	low = unswapref(low, has_swap, sw0, sw1);
	high = unswapref(high, has_swap, sw0, sw1);
	if (!isdreg(low) || !isdreg(high) || req(low, high))
		return 0;
	n = 0;
	addblock(blocks, &n, entry);
	addblock(blocks, &n, init);
	addblock(blocks, &n, l.header);
	addblock(blocks, &n, l.body);
	addblock(blocks, &n, lowcopy);
	addblock(blocks, &n, highb);
	addblock(blocks, &n, highcopy);
	addblock(blocks, &n, storeb);
	addblock(blocks, &n, l.exit);
	addblock(blocks, &n, retb);
	repeatdecodeinit(&d);
	if (!repeatmemfor(&d, load->arg[0], counter, Kw, e, &srcmem)
	|| !repeatmemfor(&d, store->arg[1], counter, Kw, e, &dstmem)
	|| !repeatstreamscomplete(&d))
		return 0;
	repinit(&p, RpGroup, RpFinishLimit, l.limit, counter);
	p.copy_guard_to_count = 1;
	op = repop(&p, "MOV", Kw, 1);
	repargmem(op, srcmem);
	repargref(op, tmp);
	op = repop(&p, "MAXS", Kw, 1);
	repargref(op, low);
	repargref(op, tmp);
	op = repop(&p, "MINS", Kw, 1);
	repargref(op, high);
	repargref(op, tmp);
	op = repop(&p, "MOV", Kw, 1);
	repargref(op, tmp);
	repargmem(op, dstmem);
	return emitrepplan(e, entry, idbase, skip, need_label, blocks, n, &p);
}

static int
emit_repeat_ifconverted_loop(E *e, Blk *entry, int idbase, unsigned char *skip, int need_label)
{
	return emit_repeat_clamp_diamond_loop(e, entry, idbase, skip, need_label)
		|| emit_repeat_abs_diamond_loop(e, entry, idbase, skip, need_label);
}

static int
emit_counted_loop(E *e, Blk *b, int idbase, unsigned char *skip, int need_label)
{
	return emit_repeat_straight_loop(e, b, idbase, skip, need_label)
		|| emit_repeat_break_loop(e, b, idbase, skip, need_label)
		|| emit_repeat_ifconverted_loop(e, b, idbase, skip, need_label)
		;
}

static void
mark_counted_loops(E *e, int idbase, unsigned char *skip)
{
	FILE *out, *null;
	Blk *b;

	null = fopen("/dev/null", "w");
	if (null == 0)
		return;
	out = e->f;
	e->f = null;
	for (b=e->fn->start; b; b=b->link) {
		if (skip[b->id])
			continue;
		(void)emit_counted_loop(e, b, idbase, skip, 0);
	}
	e->f = out;
	fclose(null);
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
	unsigned char *skip_blocks;
	int c, lbl;
	E ebuf, *e;

	e = &ebuf;
	e->f = out;
	e->fn = fn;
	e->reg = fn->reg;
	e->replacement_reg = 0;
	promote_call_fenced_regs(e);
	elide_edge_copybacks(e->fn);
	promote_loop_saved_regs(e->fn);
	elide_saved_copybacks(e->fn);
	skip_blocks = calloc(maxblkid(e->fn) + 1, 1);
	framelayout(e);
	mark_counted_loops(e, id0, skip_blocks);
	e->reg = (normalemittedregs(e->fn, skip_blocks) & ~foldedtmpregs(e, skip_blocks))
		| e->replacement_reg;
	framelayout(e);
	record_emitted_fn(fn, e->reg);

	fprintf(e->f, ".text\n");
	if (e->fn->export)
		fprintf(e->f, ".globl %s%s\n", gassym, e->fn->name);
	fprintf(e->f, "%s%s:\n", gassym, e->fn->name);
	compute_fence_liveness(e->fn, &fence_in, &fence_out, &nfence);
	emitframe(e, 0);

	for (lbl=0, b=e->fn->start; b; b=b->link) {
		int nins;
		if (skip_blocks[b->id]) {
			lbl = 1;
			continue;
		}
		if (emit_counted_loop(e, b, id0, skip_blocks, lbl || b->npred > 1)) {
			lbl = 1;
			continue;
		}
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
			if (!emitcallfencegroup(&i, iend, e, call_fences, b->ins)
			&& !skipoverwrittencopy(&i, iend)
			&& !emitstackcallspill(&i, iend, e, call_fences, b->ins)
			&& !emitsavedsubshift(&i, iend, e)
			&& !emitcopythrough(&i, iend, e)
			&& !emitleareorder(&i, iend, e)
			&& !emitleafold(&i, iend, e)
			&& !emitsumfold(&i, iend, e)
			&& !emitbitfieldreplace(&i, iend, e)
			&& !emitdivmodpair(&i, iend, e)
			&& !emitrmwaddstore(&i, iend, e)
			&& !emitmemcopyfold(&i, iend, e)
			&& !emitloadmaddfold(&i, iend, e)
			&& !emitloadopfold(&i, iend, e)
			&& !emitpostinc(&i, iend, e)
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
	free(skip_blocks);
	free(fence_in);
	free(fence_out);
	id0 += e->fn->nblk;
}
