.text
.globl foo
.type foo, @function
foo:
    ADD.L D1, D2
    ABS.L D2
    ADD.Q D0, SP
    ADD.Q 16.W, SP
    SUB.Q D0, SP
    SUB.Q 8.W, SP
    AND.L 1.W, [A1]
    CMP.L 9.W, SP
    MOV.Q D0, SP
    MOV.Q SP, D0
    MOV.Q 16, SP
    MOV.L D0, [A1]
    SHL.L 2, D0
    PARITY.L [A0]
    CMP.L [A0], [A1]
    MOV.L [A0 + D1.L * 4], D0
    REP D0, ADD.L [A0 + D0.L * 4 - 4], D1
    REPLT D1, CMP.L D2, [A0++]
    REPGT D2, CMP.L [A0++], D1
    DJLT.L D1, done@WORD_PCREL16
    SETGE.L D3
    REPG D0, {
        ADD.L D1, D2
        SUB.L D3, D4
        INC.L D5
        DEC.L D6
    }
    REPG D4, {
        CLR D5
        MADD.L [A1++], D1, D5
        MADD.L [A1], D2, D5
        MADD.L [A1 + 4], D3, D5
        MOV.L D5, [A0++]
    }
    REPGF D0, {
        ADD.L [A0 + D0.L * 4 - 4], D1
        MOV.L D1, [A1 + D0.L * 4 - 4]
    }
    MOV.L [A1++], D2
    MOV.L D2, [A0++]
    MOVSETAD 0x0003
    MOVSETAD DB2, 0x0003
    MOVSETDA 0x0003
    MOVSETDA DB3, {D0-D1}
    MOVSETDD DB1, DB2, {D0-D3}
    XCHGSETAD 0x0003
    XCHGSETAD DB2, 0x0003
    XCHGSETDD DB1, DB2, {D0-D3}
    SELDB DB1
    SELDB D0
    GETDB D0
    SUM.L {D1-D7,A4}, D0
    SUM.L {D4,D7,A4}, A4
    ENCINST [A0]
    CPUID D0
    CLR A2
    LEA [A2 + D2.L * 4 + 1], A3
    .balign 64
repg_mem:
    REPG D0, {
        MOV.L [A1++], D2
        LEA [A2 + D2.L * 4 + 1], A3
        MOV.L A3, [A0++]
    }
    FADD.S [A0], F1
    FMADD.S [A0], F1, F2
    JEQ.W done@WORD_PCREL16
    JMP.L done@WORD_PCREL32
    CALL ext_func@PLT32
done:
    RET
.size foo, .-foo

.data
.globl object
.type object, @object
object:
    .quad foo@ABS64
    .long 0x12345678
    .asciz "bedrock"
.size object, .-object

.bss
.globl scratch
.type scratch, @object
scratch:
    .zero 16
.size scratch, .-scratch
