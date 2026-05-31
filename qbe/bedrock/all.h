#include "../all.h"

enum BedrockReg {
	D0 = RXX + 1,
	D1,
	D2,
	D3,
	D4,
	D5,
	D6,
	D7,

	A0,
	A1,
	A2,
	A3,
	A4,
	A5,
	A6,
	A7,
	SP,

	F0,
	F1,
	F2,
	F3,
	F4,
	F5,
	F6,
	F7,

	NGPR = A7 - D0 + 1,
	NFPR = F6 - F0 + 1,
	NGPS = (D5 - D0 + 1) + (A3 - A0 + 1),
	NFPS = NFPR,
	NCLR = 3,
};
MAKESURE(reg_not_tmp, F7 < (int)Tmp0);

enum BedrockCodeModel {
	BEDROCK_CMODEL_LARGE,
	BEDROCK_CMODEL_LOW,
	BEDROCK_CMODEL_HIGH,
	BEDROCK_CMODEL_SMALL,
};

/* targ.c */
extern int bedrock_rsave[];
extern int bedrock_rclob[];
extern int bedrock_cmodel;
int bedrock_set_cmodel(char *);

/* abi.c */
bits bedrock_retregs(Ref, int[2]);
bits bedrock_argregs(Ref, int[2]);
void bedrock_abi(Fn *);

/* isel.c */
void bedrock_isel(Fn *);

/* emit.c */
void bedrock_emitfn(Fn *, FILE *);
