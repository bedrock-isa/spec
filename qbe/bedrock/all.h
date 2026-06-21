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
	F8,
	F9,
	F10,
	F11,
	F12,
	F13,
	F14,
	F15,
	F16,
	F17,
	F18,
	F19,
	F20,
	F21,
	F22,
	F23,
	F24,
	F25,
	F26,
	F27,
	F28,
	F29,
	F30,
	F31,

	NGPR = A7 - D0 + 1,
	NFPR = F30 - F0 + 1,
	NGPS = (D5 - D0 + 1) + (A5 - A0 + 1),
	NFPS = F7 - F0 + 1,
	NCLR = 3,
};
MAKESURE(reg_not_tmp, F31 < (int)Tmp0);

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
