#include <stdio.h>
#include <string.h>

#include "bedrock_asm_disasm.h"

static int check_line_words(const char *input, const char *expected_form, size_t expected_words)
{
    uint16_t words[BEDROCK_MAX_INSTRUCTION_WORDS];
    size_t written_words = 0;
    char disassembled[160];
    const bedrock_form_desc *assembled_form = 0;
    const bedrock_form_desc *decoded_form = 0;
    int status = bedrock_assemble_line(input, words, BEDROCK_MAX_INSTRUCTION_WORDS, &written_words, &assembled_form);
    if (status != BEDROCK_OK) {
        fprintf(stderr, "assemble failed (%d): %s\n", status, input);
        return 1;
    }
    if (assembled_form == 0 || strcmp(assembled_form->id, expected_form) != 0) {
        fprintf(
            stderr,
            "unexpected form for %s: got %s, expected %s\n",
            input,
            assembled_form ? assembled_form->id : "<none>",
            expected_form
        );
        return 1;
    }
    if (expected_words != 0u && written_words != expected_words) {
        fprintf(
            stderr,
            "unexpected word count for %s: got %zu, expected %zu\n",
            input,
            written_words,
            expected_words
        );
        return 1;
    }
    status = bedrock_disassemble_line(words, written_words, disassembled, sizeof(disassembled), &decoded_form);
    if (status != BEDROCK_OK) {
        fprintf(stderr, "disassemble failed (%d): %s\n", status, input);
        return 1;
    }
    if (decoded_form == 0) {
        fprintf(stderr, "decoder returned no form: %s\n", input);
        return 1;
    }
    printf("%-24s -> %-22s -> %s\n", input, assembled_form->id, disassembled);
    return 0;
}

static int check_line(const char *input, const char *expected_form)
{
    return check_line_words(input, expected_form, 0);
}

static int check_prefixed_line(const char *input, const char *expected_form)
{
    uint16_t words[BEDROCK_MAX_INSTRUCTION_WORDS];
    size_t written_words = 0;
    const bedrock_form_desc *assembled_form = 0;
    int status = bedrock_assemble_line(input, words, BEDROCK_MAX_INSTRUCTION_WORDS, &written_words, &assembled_form);
    if (status != BEDROCK_OK) {
        fprintf(stderr, "assemble failed (%d): %s\n", status, input);
        return 1;
    }
    if ((words[0] & BEDROCK_WORD0_PREFIX_BIT) == 0u || written_words < 2u) {
        fprintf(stderr, "missing prefix encoding for %s\n", input);
        return 1;
    }
    if (assembled_form == 0 || strcmp(assembled_form->id, expected_form) != 0) {
        fprintf(
            stderr,
            "unexpected form for %s: got %s, expected %s\n",
            input,
            assembled_form ? assembled_form->id : "<none>",
            expected_form
        );
        return 1;
    }
    printf("%-24s -> %-22s -> prefix word 0x%04x\n", input, assembled_form->id, words[1]);
    return 0;
}

static int check_rejected_line(const char *input)
{
    uint16_t words[BEDROCK_MAX_INSTRUCTION_WORDS];
    size_t written_words = 0;
    const bedrock_form_desc *assembled_form = 0;
    int status = bedrock_assemble_line(input, words, BEDROCK_MAX_INSTRUCTION_WORDS, &written_words, &assembled_form);
    if (status == BEDROCK_OK) {
        fprintf(stderr, "unexpectedly accepted invalid assembly: %s\n", input);
        return 1;
    }
    printf("%-24s -> rejected as expected\n", input);
    return 0;
}

int main(void)
{
    int failed = 0;
    failed |= check_line("ADD.L D1, D2", "ADD.D_TO_D");
    failed |= check_line("MOV.L D0, D1", "MOV.EA_TO_D");
    failed |= check_line("MOV.L D0, [A1]", "MOV.D_TO_EA");
    failed |= check_line("MOV.L [A1], D0", "MOV.EA_TO_D");
    failed |= check_line("MOV.Q D0, SP", "MOV.D_TO_EA");
    failed |= check_line("MOV.Q SP, D0", "MOV.EA_TO_D");
    failed |= check_line("MOV.Q 16, SP", "MOV.EA_TO_EA");
    failed |= check_line("CMP.L [A0], [A1]", "CMP.EA_TO_EA");
    failed |= check_line("ADD.Q D0, A1", "ADD.EA_TO_A");
    failed |= check_line("ADD.Q D0, SP", "ADD.D_TO_EA");
    failed |= check_line_words("ADD.Q 16, SP", "ADD.IMM_TO_EA", 2);
    failed |= check_line("ADD.L 1.W, D0", "ADD.IMM_TO_D");
    failed |= check_rejected_line("ADD.Q 64, SP");
    failed |= check_rejected_line("ADD.Q 16.W, SP");
    failed |= check_line("SUB.Q D0, SP", "SUB.D_TO_EA");
    failed |= check_line_words("SUB.Q 8, SP", "SUB.IMM_TO_EA", 2);
    failed |= check_line("SUB.W 2.W, D1", "SUB.IMM_TO_D");
    failed |= check_line_words("AND.L 1, [A1]", "AND.IMM_TO_EA", 2);
    failed |= check_line("AND.L 999.W, D1", "AND.IMM_TO_D");
    failed |= check_line("AND.L -993.W, D0", "AND.IMM_TO_D");
    failed |= check_line("OR.L 1.W, D0", "OR.IMM_TO_D");
    failed |= check_line("XOR.L 1.W, D0", "XOR.IMM_TO_D");
    failed |= check_line("TEST.L 0xff.W, D2", "TEST.IMM_TO_D");
    failed |= check_line("CMP.L 9.W, D3", "CMP.IMM_TO_D");
    failed |= check_line_words("CMP.L 9, SP", "CMP.IMM_TO_EA", 2);
    failed |= check_line("MOV.L [A0 + D1.L * 4], D0", "MOV.EA_TO_D");
    failed |= check_line("MOV.L [GS4:A0 + D1.L * 4], D0", "MOV.EA_TO_D");
    failed |= check_line("ADC.Q D1, [A2]", "ADC.D_TO_EA");
    failed |= check_line("EXTSW.B D1, D2", "EXTSW.D_TO_D");
    failed |= check_line("EXTSQ.L D1, D2", "EXTSQ.D_TO_D");
    failed |= check_line("EXTZQ.L D1, D2", "EXTZQ.D_TO_D");
    failed |= check_rejected_line("EXTZQ.Q D1, D2");
    failed |= check_line("EXTZL.W [A0], D3", "EXTZL.EA_TO_D");
    failed |= check_line("EXTZW.B [A0], D3", "EXTZW.EA_TO_EA");
    failed |= check_line("CMPXCHG.Q/ACQREL D0, D1, [A2]", "CMPXCHG.D_TO_D_TO_EA");
    failed |= check_line("FETCHADD.L/RELEASE D2, [A3]", "FETCHADD.D_TO_EA");
    failed |= check_line("FADD.S [A0], F1", "FADD.EA_TO_F");
    failed |= check_line("FMOVEQ F1, F2", "FMOVcc.F_TO_F");
    failed |= check_line("FMOVEQ.S [A0], F1", "FMOVcc.EA_TO_F");
    failed |= check_line("FMOVNE.D F1, [A0]", "FMOVcc.F_TO_EA");
    failed |= check_line("FMADD.S [A0], F15, F2", "FMADD.EA_TO_F_TO_F");
    failed |= check_rejected_line("FMADD.S [A0], F16, F2");
    failed |= check_line("FPUSHM {F8-F15}", "FPUSHM.BITMAP");
    failed |= check_line("FPOPM {F8-F15}", "FPOPM.BITMAP");
    failed |= check_line("SHL.Q 63, D0", "SHL.I6_TO_EA");
    failed |= check_line("SHR.L D1, [A0]", "SHR.D_TO_EA");
    failed |= check_rejected_line("SHL.Q 64, D0");
    failed |= check_line("BTEST.Q 63, D0", "BTEST.I6_TO_EA");
    failed |= check_line("BSET.L D2, [A1]", "BSET.D_TO_EA");
    failed |= check_line("BNDUII.L D1, [A0], D2", "BNDUII.D_TO_EA_TO_D");
    failed |= check_line("PARITY.L [A0]", "PARITY.EA");
    failed |= check_line("CLR A2", "CLR.A");
    failed |= check_line("LEA [A2 + D2.L * 4 + 1], A3", "LEA.EA_TO_A");
    failed |= check_line("JEQ.W 16", "Jcc.IMM");
    failed |= check_line("JMP.W 16", "JMP.IMM");
    failed |= check_rejected_line("JF.W 16");
    failed |= check_line_words("CALL 0x1234", "CALL.IMM16", 2);
    failed |= check_line("CALL 0x10000", "CALL.IMM32");
    failed |= check_line("CALL 0x100000000", "CALL.IMM64");
    failed |= check_line("CALL [A0]", "CALL.EA");
    failed |= check_line("TRACE 0x1234", "TRACE.IMM");
    failed |= check_line_words("REPG D0, 8", "REPG.D_TO_IMM", 2);
    failed |= check_rejected_line("REPG D0, 0");
    failed |= check_rejected_line("REPG D0, 7");
    failed |= check_line("PUSHM {D0-D7}", "PUSHM.BITMAP");
    failed |= check_line("SUM.L {D1-D7,A4}, D0", "SUM.BITMAP_TO_D");
    failed |= check_line("SUM.L {D4,D7,A4}, A4", "SUM.BITMAP_TO_A");
    failed |= check_line("ENCINST [A0]", "ENCINST.EA");
    failed |= check_line("MOVSETAD {D0-D1}", "MOVSETAD.BITMAP");
    failed |= check_line("MOVSETAD DB2, {D0-D1}", "MOVSETAD.DB_TO_BITMAP");
    failed |= check_line("MOVSETDA 0x0003", "MOVSETDA.BITMAP");
    failed |= check_line("MOVSETDA DB3, {D0-D1}", "MOVSETDA.DB_TO_BITMAP");
    failed |= check_line("MOVSETDD DB1, DB2, {D0-D3}", "MOVSETDD.DB_TO_DB_TO_BITMAP");
    failed |= check_line("XCHGSETAD 0x0003", "XCHGSETAD.BITMAP");
    failed |= check_line("XCHGSETAD DB2, 0x0003", "XCHGSETAD.DB_TO_BITMAP");
    failed |= check_line("XCHGSETDD DB1, DB2, {D0-D3}", "XCHGSETDD.DB_TO_DB_TO_BITMAP");
    failed |= check_line("SELDB DB1", "SELDB.DB");
    failed |= check_line("SELDB D0", "SELDB.D");
    failed |= check_line("GETDB D0", "GETDB.D");
    failed |= check_line("WRFLAGS D1", "WRFLAGS.D");
    failed |= check_line("RDSEG DS, D0", "RDSEG.S_TO_D");
    failed |= check_line("RDSEG GS4, D0", "RDSEG.S_TO_D");
    failed |= check_line("WRSEG D1, GS4", "WRSEG.D_TO_S");
    failed |= check_line("RDCR PTCR, D0", "RDCR.D");
    failed |= check_line("WRCR D1, ICR", "WRCR.D");
    failed |= check_line("CPUID D0", "CPUID.D");
    failed |= check_prefixed_line("MOV.L [A1++], D2", "MOV.EA_TO_D");
    failed |= check_prefixed_line("MOV.L D2, [A0++]", "MOV.D_TO_EA");
    failed |= check_prefixed_line("REP D0, ADD.L [A0 + D0.L * 4 - 4], D1", "ADD.EA_TO_D");
    failed |= check_prefixed_line("REPEQ D2, CMP.L [A0 + D2.L * 4 - 4], D1", "CMP.EA_TO_D");
    failed |= check_rejected_line("MOV.L [A0 + D1.L], D0");
    return failed ? 1 : 0;
}
