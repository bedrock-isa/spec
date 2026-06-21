#include "all.h"

int bedrock_rsave[] = {
	D0, D1, D2, D3, D4, D5,
	A0, A1, A2, A3, A4, A5,
	F0, F1, F2, F3, F4, F5, F6, F7,
	-1
};

int bedrock_rclob[] = {
	D6, D7, A6, -1
};

int bedrock_cmodel = BEDROCK_CMODEL_LARGE;

int
bedrock_set_cmodel(char *name)
{
	if (strcmp(name, "large") == 0) {
		bedrock_cmodel = BEDROCK_CMODEL_LARGE;
		return 1;
	}
	if (strcmp(name, "low") == 0) {
		bedrock_cmodel = BEDROCK_CMODEL_LOW;
		return 1;
	}
	if (strcmp(name, "high") == 0) {
		bedrock_cmodel = BEDROCK_CMODEL_HIGH;
		return 1;
	}
	if (strcmp(name, "small") == 0) {
		bedrock_cmodel = BEDROCK_CMODEL_SMALL;
		return 1;
	}
	return 0;
}

static int
bedrock_memargs(int op)
{
	(void)op;
	return 0;
}

Target T_bedrock = {
	.gpr0 = D0,
	.ngpr = NGPR,
	.fpr0 = F0,
	.nfpr = NFPR,
	.rglob = BIT(A7),
	.nrglob = 1,
	.rsave = bedrock_rsave,
	.nrsave = {NGPS, NFPS},
	.retregs = bedrock_retregs,
	.argregs = bedrock_argregs,
	.memargs = bedrock_memargs,
	.abi = bedrock_abi,
	.isel = bedrock_isel,
	.emitfn = bedrock_emitfn,
};

MAKESURE(arrays_size_ok,
	sizeof bedrock_rsave == (NGPS+NFPS+1) * sizeof(int) &&
	sizeof bedrock_rclob == (NCLR+1) * sizeof(int)
);
