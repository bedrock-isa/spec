#pragma once

#include "sail.h"
#include "sail_config.h"
#include "rts.h"
#include "elf.h"
#ifdef __cplusplus
extern "C" {
#endif
extern void (*sail_rts_set_coverage_file)(const char *);

// union option<i>
enum kind_zoptionzIizK { Kind_zNonezIizK, Kind_zSomezIizK };

struct zoptionzIizK {
  enum kind_zoptionzIizK kind;
  union {
    struct { unit zNonezIizK; };
    struct { sail_int zSomezIizK; };
  } variants;
};

// union option<b>
enum kind_zoptionzIbzK { Kind_zNonezIbzK, Kind_zSomezIbzK };

struct zoptionzIbzK {
  enum kind_zoptionzIbzK kind;
  union {
    struct { unit zNonezIbzK; };
    struct { lbits zSomezIbzK; };
  } variants;
};

struct zz5vecz8z5bvz9 {
  size_t len;
  lbits *data;
};
typedef struct zz5vecz8z5bvz9 zz5vecz8z5bvz9;

// union option<Vb>
enum kind_zoptionzIVbzK { Kind_zNonezIVbzK, Kind_zSomezIVbzK };

struct zoptionzIVbzK {
  enum kind_zoptionzIVbzK kind;
  union {
    struct { unit zNonezIVbzK; };
    struct { zz5vecz8z5bvz9 zSomezIVbzK; };
  } variants;
};

struct node_zz5listz8z5bvz9 {
  unsigned int rc;
  lbits hd;
  struct node_zz5listz8z5bvz9 *tl;
};
typedef struct node_zz5listz8z5bvz9 *zz5listz8z5bvz9;

// union option<Lb>
enum kind_zoptionzILbzK { Kind_zNonezILbzK, Kind_zSomezILbzK };

struct zoptionzILbzK {
  enum kind_zoptionzILbzK kind;
  union {
    struct { unit zNonezILbzK; };
    struct { zz5listz8z5bvz9 zSomezILbzK; };
  } variants;
};

// union exception
enum kind_zexception { Kind_z__dummy_exnz3 };

struct zexception {
  enum kind_zexception kind;
  union {struct { unit z__dummy_exnz3; };} variants;
};

// type abbreviation bit
typedef uint64_t zbit;

struct zz5vecz8z5listz8z5bvz9z9 {
  size_t len;
  zz5listz8z5bvz9 *data;
};
typedef struct zz5vecz8z5listz8z5bvz9z9 zz5vecz8z5listz8z5bvz9z9;

// type abbreviation Vector_registers
typedef zz5vecz8z5listz8z5bvz9z9 zVector_registers;

// struct Vector_fp_reduction
struct zVector_fp_reduction {
  uint64_t zgenerated_causes;
  uint64_t zvalue;
};

// union option<RVector_fp_reduction>
enum kind_zoptionzIRVector_fp_reductionzK { Kind_zNonezIRVector_fp_reductionzK, Kind_zSomezIRVector_fp_reductionzK };

struct zoptionzIRVector_fp_reductionzK {
  enum kind_zoptionzIRVector_fp_reductionzK kind;
  union {
    struct { unit zNonezIRVector_fp_reductionzK; };
    struct { struct zVector_fp_reduction zSomezIRVector_fp_reductionzK; };
  } variants;
};

// struct Vector_fp_image
struct zVector_fp_image {
  zz5listz8z5bvz9 zbytes;
  uint64_t zgenerated_causes;
};

// union option<RVector_fp_image>
enum kind_zoptionzIRVector_fp_imagezK { Kind_zNonezIRVector_fp_imagezK, Kind_zSomezIRVector_fp_imagezK };

struct zoptionzIRVector_fp_imagezK {
  enum kind_zoptionzIRVector_fp_imagezK kind;
  union {
    struct { unit zNonezIRVector_fp_imagezK; };
    struct { struct zVector_fp_image zSomezIRVector_fp_imagezK; };
  } variants;
};

// enum Transaction_response_kind
enum zTransaction_response_kind { zResponseTranslation, zResponseProbe, zResponseRead, zResponseStoreAck, zResponseStackRange, zResponseSegmentBounds, zResponseIntegerExternal, zResponseAtomic, zResponseAddressTranslation, zResponsePteRead, zResponseCacheMaintenance, zResponseFenceCompletion, zResponseTlbOperation, zResponseTranslationQuery, zResponseContextSwitch, zResponseStateSave, zResponseStateRestore, zResponseRepeatFetch, zResponseEventFrame, zResponseVectorMemory, zResponseCpuidQuery, zResponsePerformanceCounter, zResponseControlTransition, zResponseResetSerializze };

// enum Transaction_access
enum zTransaction_access { zNoTransactionAccess, zAccessLoad, zAccessStore, zAccessReadModifyWrite, zAccessExecute, zAccessStackRead, zAccessStackWrite, zAccessAddressOnly };

// struct Staged_register_update
struct zStaged_register_update {
  uint64_t zindex;
  uint64_t zvalue;
};

// enum Size_code
enum zSizze_code { zSizze_B, zSizze_D, zSizze_H, zSizze_L, zSizze_Q, zSizze_S, zSizze_W };

// enum Semantic_route
enum zSemantic_route { zRouteIntegerUnary, zRouteIntegerAlu, zRouteCoreControl, zRouteIntegerBitfield, zRouteBounds, zRouteControlFlow, zRouteIntegerMulDiv, zRouteAtomics, zRouteSystemRegisters, zRouteCache, zRouteTlbContext, zRouteEaUtility, zRouteDataMovement, zRouteFpu, zRouteFpuTranscendental, zRouteVector };

// enum Semantic_operation
enum zSemantic_operation { zOp_ABS, zOp_ADC, zOp_ADD, zOp_AFENCE, zOp_AND, zOp_BCHG, zOp_BCLR, zOp_BKPT, zOp_BNDSII, zOp_BNDSIX, zOp_BNDSXI, zOp_BNDSXX, zOp_BNDUII, zOp_BNDUIX, zOp_BNDUXI, zOp_BNDUXX, zOp_BSET, zOp_BTEST, zOp_CALL, zOp_CALLcc, zOp_CLMUL, zOp_CLMULH, zOp_CLR, zOp_CLS, zOp_CLZ, zOp_CMP, zOp_CMPJcc, zOp_CMPXCHG, zOp_CPUID, zOp_CTS, zOp_CTZ, zOp_DEC, zOp_DECF, zOp_DIVMODS, zOp_DIVMODU, zOp_DIVS, zOp_DIVU, zOp_DJcc, zOp_ERET, zOp_EXTRACT, zOp_EXTSL, zOp_EXTSQ, zOp_EXTSW, zOp_EXTZL, zOp_EXTZQ, zOp_EXTZW, zOp_FETCHADD, zOp_FETCHAND, zOp_FETCHOR, zOp_FETCHSUB, zOp_FETCHXOR, zOp_FLSHDCACHE, zOp_HALT, zOp_IJcc, zOp_ILLEGAL, zOp_INC, zOp_INCF, zOp_INVASID, zOp_INVDCACHE, zOp_INVICACHE, zOp_INVPAGE, zOp_INVTLB, zOp_Jcc, zOp_JMP, zOp_LCALL, zOp_LEA, zOp_LJMP, zOp_LRET, zOp_MAXS, zOp_MAXU, zOp_MINS, zOp_MINU, zOp_MODS, zOp_MODU, zOp_MOV, zOp_MOVcc, zOp_MOVCU, zOp_MOVNT, zOp_MOVUC, zOp_MOVUU, zOp_MUL, zOp_MULHS, zOp_MULHSU, zOp_MULHU, zOp_NEG, zOp_NOP, zOp_NOT, zOp_OR, zOp_PARITY, zOp_POP, zOp_POPCNT, zOp_POPP, zOp_PREFETCH, zOp_PREFETCHNT, zOp_PTQUERY, zOp_PUSH, zOp_PUSHP, zOp_RDCR, zOp_RDFLAGS, zOp_RDPMC, zOp_RDSEG, zOp_RDSTATUS, zOp_REPcc, zOp_RESET, zOp_RESTORE, zOp_RET, zOp_REVBYTE, zOp_RFENCE, zOp_ROL, zOp_ROR, zOp_SAR, zOp_SAVE, zOp_SBB, zOp_SEGLEA, zOp_SET, zOp_SETcc, zOp_SETF, zOp_SHL, zOp_SHR, zOp_SUB, zOp_SWPT, zOp_SWPTA, zOp_SYNCCACHE, zOp_SYSCALL, zOp_TEST, zOp_TESTJcc, zOp_TRACE, zOp_VTOP, zOp_WAIT, zOp_WFENCE, zOp_WRBKDCACHE, zOp_WRCR, zOp_WRFLAGS, zOp_WRSEG, zOp_WRSTATUS, zOp_XCHG, zOp_XOR, zOp_YIELD, zOp_FABS, zOp_FADD, zOp_FBNDII, zOp_FBNDIX, zOp_FBNDXI, zOp_FBNDXX, zOp_FCEIL, zOp_FCLASS, zOp_FCLR, zOp_FCMP, zOp_FCOPYSIGN, zOp_FCVT, zOp_FCVTU, zOp_FDIV, zOp_FFLOOR, zOp_FGETEXP, zOp_FGETMAN, zOp_FINT, zOp_FINTRZ, zOp_FMADD, zOp_FMAX, zOp_FMIN, zOp_FMOD, zOp_FMOV, zOp_FMOVcc, zOp_FMOVCR, zOp_FMSUB, zOp_FMUL, zOp_FNEG, zOp_FNMADD, zOp_FNMSUB, zOp_FPOPP, zOp_FPUSHP, zOp_FREM, zOp_FROUND, zOp_FSCALE, zOp_FSQRT, zOp_FSUB, zOp_FTEST, zOp_FTRUNC, zOp_FXCHG, zOp_RDFFLAGS, zOp_RDFSTATUS, zOp_WRFFLAGS, zOp_WRFSTATUS, zOp_FACOSA, zOp_FASINA, zOp_FATANA, zOp_FATANHA, zOp_FCOSA, zOp_FCOSHA, zOp_FETOXA, zOp_FETOXM1A, zOp_FLOG10A, zOp_FLOG2A, zOp_FLOGNA, zOp_FLOGNP1A, zOp_FSINA, zOp_FSINCOSA, zOp_FSINHA, zOp_FTANA, zOp_FTANHA, zOp_FTENTOXA, zOp_FTWOTOXA, zOp_VDUP, zOp_VMOV, zOp_PHEAD, zOp_PTAIL, zOp_PFIRST, zOp_PLAST, zOp_PCOUNT, zOp_PAND, zOp_POR, zOp_PXOR, zOp_PUNPKLO, zOp_PUNPKHI, zOp_PPACKLO, zOp_PPACKHI, zOp_VCLR, zOp_VINDEX, zOp_VLCNT, zOp_VLCADD, zOp_VGATHER1, zOp_VSCATTER1, zOp_PTRUE, zOp_PFALSE, zOp_PNOT, zOp_BPANY, zOp_BPNONE, zOp_BPALL, zOp_VNEG, zOp_VABS, zOp_VNOT, zOp_VCLZ, zOp_VCTZ, zOp_VCLS, zOp_VCTS, zOp_VPOPCNT, zOp_VREVBYTE, zOp_VSQRT, zOp_VROUND, zOp_VTRUNC, zOp_VFLOOR, zOp_VCEIL, zOp_VCLASS, zOp_PPERM, zOp_PSLIDEUP, zOp_PSLIDEDN, zOp_VCMPcc, zOp_VTESTZ, zOp_VTESTNZ, zOp_VADD, zOp_VSUB, zOp_VMUL, zOp_VAND, zOp_VOR, zOp_VXOR, zOp_VMINS, zOp_VMINU, zOp_VMAXS, zOp_VMAXU, zOp_VMULHS, zOp_VMULHU, zOp_VMULHSU, zOp_VSHL, zOp_VSHR, zOp_VSAR, zOp_VROL, zOp_VROR, zOp_VMIN, zOp_VMAX, zOp_VDIV, zOp_VCOPYSIGN, zOp_VEXTZW, zOp_VEXTSW, zOp_VEXTZL, zOp_VEXTSL, zOp_VEXTZQ, zOp_VEXTSQ, zOp_VTRUNCB, zOp_VTRUNCW, zOp_VTRUNCL, zOp_VCVTS, zOp_VCVTD, zOp_VCVTUS, zOp_VCVTUD, zOp_VCVTL, zOp_VCVTUL, zOp_VCVTQ, zOp_VCVTUQ, zOp_VPERM, zOp_VZIPLO, zOp_VZIPHI, zOp_VUZIPLO, zOp_VUZIPHI, zOp_VTRNLO, zOp_VTRNHI, zOp_VCVTH, zOp_VCVTUH, zOp_VMADD, zOp_VMSUB, zOp_VNMADD, zOp_VNMSUB, zOp_VSLICE, zOp_VSLIDEUP, zOp_VSLIDEDN, zOp_VEXTRACT, zOp_VINSERT, zOp_VREDADD, zOp_VREDMINS, zOp_VREDMINU, zOp_VREDMAXS, zOp_VREDMAXU, zOp_VREDAND, zOp_VREDOR, zOp_VREDXOR, zOp_VREDMIN, zOp_VREDMAX, zOp_PSEL, zOp_PZIPLO, zOp_PZIPHI, zOp_PUZIPLO, zOp_PUZIPHI, zOp_PTRNLO, zOp_PTRNHI, zOp_PSLICE, zOp_VMOVZ, zOp_PLOOP, zOp_PMOV };

// union option<ESemantic_operation%>
enum kind_zoptionzIESemantic_operationz5zK { Kind_zNonezIESemantic_operationz5zK, Kind_zSomezIESemantic_operationz5zK };

struct zoptionzIESemantic_operationz5zK {
  enum kind_zoptionzIESemantic_operationz5zK kind;
  union {
    struct { unit zNonezIESemantic_operationz5zK; };
    struct { enum zSemantic_operation zSomezIESemantic_operationz5zK; };
  } variants;
};

struct zz5vecz8z5bv64z9 {
  size_t len;
  uint64_t *data;
};
typedef struct zz5vecz8z5bv64z9 zz5vecz8z5bv64z9;

// type abbreviation Segment_registers
typedef zz5vecz8z5bv64z9 zSegment_registers;

// struct Segment_point
struct zSegment_point {
  bool zin_bounds;
  uint64_t zlinear;
};

// enum Run_state
enum zRun_state { zRunning, zHalted, zShutdown };

// enum Request_role
enum zRequest_role { zRequestRoleNone, zRequestRoleValue, zRequestRoleAddress, zRequestRoleControlTarget, zRequestRoleSingle, zRequestRoleStack, zRequestRoleEventEntryTarget, zRequestRoleEventFrameRange, zRequestRoleEventFrameStore, zRequestRoleUserReturnTarget, zRequestRoleUserBankTarget, zRequestRoleCacheTranslate, zRequestRoleFptransContractQuery, zRequestRolePtqueryPte, zRequestRoleVtopPte, zRequestRolePhysicalPrefetch, zRequestRolePhysicalCacheBlock };

// enum Request_domain
enum zRequest_domain { zRequestDomainCurrent, zRequestDomainUser, zRequestDomainCode, zRequestDomainStack, zRequestDomainPhysicalPageTable };

// struct Repeat_state
struct zRepeat_state {
  bool zactive;
  uint64_t zbody_start;
  uint64_t zcondition;
  uint64_t zcounter;
  zz5listz8z5bvz9 zfixed_body;
  uint64_t zprefix_start;
  uint64_t zremaining;
};

// type abbreviation Registers
typedef zz5vecz8z5bv64z9 zRegisters;

// enum Record_class
enum zRecord_class { zFixedExtraShort, zFixedShort, zExtendedMedium, zExtendedLong, zExtendedExtraLong, zExtendedXxlong };

// enum Privilege_level
enum zPrivilege_level { zUserPrivilege, zSupervisorPrivilege, zAnyPrivilege };

// enum Primitive_request_kind
enum zPrimitive_request_kind { zNoPrimitiveRequest, zTranslationExecuteProbe, zMemoryProbe, zMemoryRead, zMemoryStore, zCompoundMemoryStore, zNonTemporalStore, zStackRange, zSegmentBoundsPoint, zAtomicReadModifyWrite, zAddressTranslateRequest, zPhysicalPteRead, zCacheMaintenanceBlock, zPrefetchHint, zFenceCompletion, zTlbInvalidateRequest, zTranslationQueryRequest, zContextSwitchRequest, zStateSaveRequest, zStateRestoreRequest, zRepeatBodyFetch, zEventFrameAccess, zCpuidQueryRequest, zPerformanceCounterRequest, zControlTransitionRequest, zResetSerializzeRequest, zVectorMemoryRead, zVectorMemoryWrite, zExternalIntegerRequest };

struct node_zz5listz8z5structz0zzStaged_register_updatez9 {
  unsigned int rc;
  struct zStaged_register_update hd;
  struct node_zz5listz8z5structz0zzStaged_register_updatez9 *tl;
};
typedef struct node_zz5listz8z5structz0zzStaged_register_updatez9 *zz5listz8z5structz0zzStaged_register_updatez9;

// struct Primitive_request
struct zPrimitive_request {
  enum zTransaction_access zaccess;
  bool zaddress_translation;
  uint64_t zauxiliary;
  sail_int zbody_length;
  sail_int zcache_policy;
  bool zcommit_point;
  uint64_t zdesired;
  enum zRequest_domain zdomain;
  uint64_t zeffective_address;
  uint64_t zexpected;
  enum zPrimitive_request_kind zkind;
  uint64_t zlinear_address;
  sail_int zmemory_order;
  sail_int zordinal;
  zz5listz8z5bvz9 zpayload_bytes;
  uint64_t zrange_end;
  bool zrange_end_at_modulus;
  sail_int zrange_length;
  uint64_t zrange_start;
  bool zrange_wrap;
  enum zRequest_role zrole;
  sail_int zsegment;
  uint64_t zsegment_image;
  uint64_t zselector;
  zz5listz8z5structz0zzStaged_register_updatez9 zstaged_updates;
  bool zsuppress_fault;
  uint64_t zvalue;
  sail_int zwidth;
};

// type abbreviation Predicate_registers
typedef zz5vecz8z5listz8z5bvz9z9 zPredicate_registers;

// enum Predicate_mode
enum zPredicate_mode { zPredicateNone, zAnnulOnFalse, zTemporary, zCounterAndCondition, zWriteBoolean };

// enum Physical_memory_class
enum zPhysical_memory_class { zNormalPhysical, zDevicePhysical };

// enum Operand_type
enum zOperand_type { zOperandType_CS, zOperandType_EA, zOperandType_FEA, zOperandType_FPAIRn, zOperandType_Fn, zOperandType_PAIRn, zOperandType_Pn, zOperandType_Rn, zOperandType_SP, zOperandType_SREG, zOperandType_VEA, zOperandType_Vn, zOperandType_condition, zOperandType_fconstid, zOperandType_flags_bitmap, zOperandType_imm, zOperandType_imm16, zOperandType_imm16s, zOperandType_imm32, zOperandType_imm32s, zOperandType_imm6, zOperandType_imm64, zOperandType_imm7, zOperandType_imm8, zOperandType_imm8s, zOperandType_memory_order, zOperandType_pt_level, zOperandType_sizze_BW, zOperandType_sizze_BWL, zOperandType_sizze_BWLQ, zOperandType_sizze_B_ONLY, zOperandType_sizze_HD, zOperandType_sizze_HS, zOperandType_sizze_HSD, zOperandType_sizze_LQ, zOperandType_sizze_Q_ONLY, zOperandType_sizze_SD, zOperandType_sizze_VTYPE, zOperandType_sizze_V_BW, zOperandType_sizze_V_LQ, zOperandType_sizze_V_SD, zOperandType_sizze_WLQ };

// enum Operand_id
enum zOperand_id { zOperand_address, zOperand_asid, zOperand_base, zOperand_bit_index, zOperand_bound, zOperand_cc, zOperand_constant_id, zOperand_cos_dst, zOperand_count, zOperand_counter, zOperand_counter_id, zOperand_cr, zOperand_cursor, zOperand_desired, zOperand_disp16s, zOperand_disp32s, zOperand_disp64, zOperand_disp8s, zOperand_dst, zOperand_expected, zOperand_govern, zOperand_hi, zOperand_high, zOperand_imm, zOperand_immediate, zOperand_index, zOperand_level, zOperand_lhs, zOperand_lo, zOperand_low_dst, zOperand_magnitude_src, zOperand_marker, zOperand_mask, zOperand_memory, zOperand_new_cs, zOperand_new_ptcr, zOperand_offset, zOperand_order, zOperand_page, zOperand_pair_id, zOperand_phys, zOperand_predicate, zOperand_quotient, zOperand_reg, zOperand_remainder, zOperand_remaining, zOperand_rhs, zOperand_seg, zOperand_select, zOperand_sign_src, zOperand_sin_dst, zOperand_src, zOperand_stride, zOperand_target, zOperand_value, zOperand_virt };

// union option<EOperand_id%>
enum kind_zoptionzIEOperand_idz5zK { Kind_zNonezIEOperand_idz5zK, Kind_zSomezIEOperand_idz5zK };

struct zoptionzIEOperand_idz5zK {
  enum kind_zoptionzIEOperand_idz5zK kind;
  union {
    struct { unit zNonezIEOperand_idz5zK; };
    struct { enum zOperand_id zSomezIEOperand_idz5zK; };
  } variants;
};

// enum Operand_domain
enum zOperand_domain { zOperandDomain_user };

// union option<EOperand_domain%>
enum kind_zoptionzIEOperand_domainz5zK { Kind_zNonezIEOperand_domainz5zK, Kind_zSomezIEOperand_domainz5zK };

struct zoptionzIEOperand_domainz5zK {
  enum kind_zoptionzIEOperand_domainz5zK kind;
  union {
    struct { unit zNonezIEOperand_domainz5zK; };
    struct { enum zOperand_domain zSomezIEOperand_domainz5zK; };
  } variants;
};

// enum Metadata_field_kind
enum zMetadata_field_kind { zFieldRn, zFieldFreg, zFieldEa, zFieldCondition, zFieldSizze, zFieldImmediate, zFieldBits };

// enum Metadata_access
enum zMetadata_access { zAccessRead, zAccessWrite, zAccessReadWrite, zAccessAddress };

// struct Memory_write
struct zMemory_write {
  uint64_t zeffective_address;
  uint64_t zlinear_address;
  sail_int zsegment;
  sail_int zslot;
  uint64_t zvalue;
  sail_int zwidth;
};

// enum Memory_access_class
enum zMemory_access_class { zNormalAccess, zMmioAccess };

// enum Instruction_set
enum zInstruction_set { zBaseSet, zFpuSet, zFpuTranscendentalSet, zVectorSet, zVectorFpuSet };

// struct Framed_record
struct zFramed_record {
  sail_int zencoded_length;
  enum zRecord_class zrecord_class;
};

// union option<RFramed_record>
enum kind_zoptionzIRFramed_recordzK { Kind_zNonezIRFramed_recordzK, Kind_zSomezIRFramed_recordzK };

struct zoptionzIRFramed_recordzK {
  enum kind_zoptionzIRFramed_recordzK kind;
  union {
    struct { unit zNonezIRFramed_recordzK; };
    struct { struct zFramed_record zSomezIRFramed_recordzK; };
  } variants;
};

// enum Fptrans_contract_status
enum zFptrans_contract_status { zFptransContractUnknown, zFptransContractAbsent, zFptransContractMalformed, zFptransContractPresent };

// struct Fptrans_contract_lookup
struct zFptrans_contract_lookup {
  uint64_t zallowed_causes;
  uint64_t zcontract_word;
  uint64_t zd_max_ulp_q8_8;
  struct zoptionzIESemantic_operationz5zK zoperation;
  uint64_t zs_max_ulp_q8_8;
  enum zFptrans_contract_status zstatus;
};

// enum Fp_value_kind
enum zFp_value_kind { zFpValueNone, zFpBits32, zFpBits64, zFpRaw64, zFpSigned64, zFpUnsigned64 };

// enum Fp_result_policy
enum zFp_result_policy { zFpResultNone, zFpResultFnByFormat, zFpResultByForm, zFpResultFn32, zFpResultFn64, zFpResultRn64, zFpResultFlags, zFpResultFlagsVOnly, zFpResultFnPairByFormat, zFpResultFnPair32, zFpResultFnPair64, zFpResultMemory32, zFpResultMemory64 };

// union option<EFp_result_policy%>
enum kind_zoptionzIEFp_result_policyz5zK { Kind_zNonezIEFp_result_policyz5zK, Kind_zSomezIEFp_result_policyz5zK };

struct zoptionzIEFp_result_policyz5zK {
  enum kind_zoptionzIEFp_result_policyz5zK kind;
  union {
    struct { unit zNonezIEFp_result_policyz5zK; };
    struct { enum zFp_result_policy zSomezIEFp_result_policyz5zK; };
  } variants;
};

// enum Fp_result_kind
enum zFp_result_kind { zFpResultValueNone, zFpResultBits32, zFpResultBits64, zFpResultRaw64, zFpResultInteger, zFpResultValueFlags, zFpResultPair32, zFpResultPair64, zFpResultPairRaw64 };

// union option<EFp_result_kind%>
enum kind_zoptionzIEFp_result_kindz5zK { Kind_zNonezIEFp_result_kindz5zK, Kind_zSomezIEFp_result_kindz5zK };

struct zoptionzIEFp_result_kindz5zK {
  enum kind_zoptionzIEFp_result_kindz5zK kind;
  union {
    struct { unit zNonezIEFp_result_kindz5zK; };
    struct { enum zFp_result_kind zSomezIEFp_result_kindz5zK; };
  } variants;
};

// enum Fp_path
enum zFp_path { zFpPathR, zFpPathS1, zFpPathS2, zFpPathD1, zFpPathStack };

// union option<EFp_path%>
enum kind_zoptionzIEFp_pathz5zK { Kind_zNonezIEFp_pathz5zK, Kind_zSomezIEFp_pathz5zK };

struct zoptionzIEFp_pathz5zK {
  enum kind_zoptionzIEFp_pathz5zK kind;
  union {
    struct { unit zNonezIEFp_pathz5zK; };
    struct { enum zFp_path zSomezIEFp_pathz5zK; };
  } variants;
};

// struct Fp_semantics
struct zFp_semantics {
  uint64_t zallowed_causes;
  uint64_t zcontract_id;
  uint64_t zflags_mask;
  enum zFp_path zpath;
  enum zFp_result_policy zresult_policy;
  sail_int zsource_count;
  bool ztranscendental;
};

// union option<RFp_semantics>
enum kind_zoptionzIRFp_semanticszK { Kind_zNonezIRFp_semanticszK, Kind_zSomezIRFp_semanticszK };

struct zoptionzIRFp_semanticszK {
  enum kind_zoptionzIRFp_semanticszK kind;
  union {
    struct { unit zNonezIRFp_semanticszK; };
    struct { struct zFp_semantics zSomezIRFp_semanticszK; };
  } variants;
};

// struct Fp_operand_image
struct zFp_operand_image {
  uint64_t zbits;
  enum zFp_value_kind zkind;
  bool zvalid;
};

// union option<RFp_operand_image>
enum kind_zoptionzIRFp_operand_imagezK { Kind_zNonezIRFp_operand_imagezK, Kind_zSomezIRFp_operand_imagezK };

struct zoptionzIRFp_operand_imagezK {
  enum kind_zoptionzIRFp_operand_imagezK kind;
  union {
    struct { unit zNonezIRFp_operand_imagezK; };
    struct { struct zFp_operand_image zSomezIRFp_operand_imagezK; };
  } variants;
};

// struct Fp_postprocess_result
struct zFp_postprocess_result {
  uint64_t zgenerated_causes;
  struct zFp_operand_image zvalue;
};

// struct Fp_operand_slots
struct zFp_operand_slots {
  struct zFp_operand_image zoperand0;
  struct zFp_operand_image zoperand1;
  struct zFp_operand_image zoperand2;
};

// union option<RFp_operand_slots>
enum kind_zoptionzIRFp_operand_slotszK { Kind_zNonezIRFp_operand_slotszK, Kind_zSomezIRFp_operand_slotszK };

struct zoptionzIRFp_operand_slotszK {
  enum kind_zoptionzIRFp_operand_slotszK kind;
  union {
    struct { unit zNonezIRFp_operand_slotszK; };
    struct { struct zFp_operand_slots zSomezIRFp_operand_slotszK; };
  } variants;
};

// enum Fp_nan_origin
enum zFp_nan_origin { zFpNotNan, zFpNanOperand0, zFpNanOperand1, zFpNanOperand2, zFpNanGeneratedDefault };

// union option<EFp_nan_origin%>
enum kind_zoptionzIEFp_nan_originz5zK { Kind_zNonezIEFp_nan_originz5zK, Kind_zSomezIEFp_nan_originz5zK };

struct zoptionzIEFp_nan_originz5zK {
  enum kind_zoptionzIEFp_nan_originz5zK kind;
  union {
    struct { unit zNonezIEFp_nan_originz5zK; };
    struct { enum zFp_nan_origin zSomezIEFp_nan_originz5zK; };
  } variants;
};

// struct Fp_primitive_evaluation
struct zFp_primitive_evaluation {
  uint64_t zaccuracy_mask;
  uint64_t zerror0_q8_8_up;
  uint64_t zerror1_q8_8_up;
  uint64_t zflags_value;
  uint64_t zgenerated_causes;
  uint64_t zprimary;
  enum zFp_nan_origin zprimary_nan_origin;
  uint64_t zsecondary;
  enum zFp_nan_origin zsecondary_nan_origin;
};

// union option<RFp_primitive_evaluation>
enum kind_zoptionzIRFp_primitive_evaluationzK { Kind_zNonezIRFp_primitive_evaluationzK, Kind_zSomezIRFp_primitive_evaluationzK };

struct zoptionzIRFp_primitive_evaluationzK {
  enum kind_zoptionzIRFp_primitive_evaluationzK kind;
  union {
    struct { unit zNonezIRFp_primitive_evaluationzK; };
    struct { struct zFp_primitive_evaluation zSomezIRFp_primitive_evaluationzK; };
  } variants;
};

// struct Fp_final_values
struct zFp_final_values {
  uint64_t zgenerated_causes;
  uint64_t zprimary;
  uint64_t zsecondary;
};

// struct Fp_exchange_result
struct zFp_exchange_result {
  uint64_t zlhs;
  uint64_t zrhs;
};

// union option<RFp_exchange_result>
enum kind_zoptionzIRFp_exchange_resultzK { Kind_zNonezIRFp_exchange_resultzK, Kind_zSomezIRFp_exchange_resultzK };

struct zoptionzIRFp_exchange_resultzK {
  enum kind_zoptionzIRFp_exchange_resultzK kind;
  union {
    struct { unit zNonezIRFp_exchange_resultzK; };
    struct { struct zFp_exchange_result zSomezIRFp_exchange_resultzK; };
  } variants;
};

// enum Fp_destination_kind
enum zFp_destination_kind { zFpDestinationNone, zFpDestinationFn, zFpDestinationRn, zFpDestinationMemory, zFpDestinationFlags, zFpDestinationFnPair };

// struct Fp_pending_image
struct zFp_pending_image {
  uint64_t zcandidate0;
  uint64_t zcandidate1;
  uint64_t zcandidate_causes;
  uint64_t zcandidate_flags;
  uint64_t zcontract_id;
  uint64_t zcontract_word;
  uint64_t zdestination0;
  uint64_t zdestination1;
  enum zFp_destination_kind zdestination_kind;
  struct zFp_operand_image zeffective0;
  struct zFp_operand_image zeffective1;
  struct zFp_operand_image zeffective2;
  uint64_t zflags_mask;
  uint64_t zfstatus_image;
  sail_int znext_source;
  enum zFp_path zpath;
  struct zFp_operand_image zraw0;
  struct zFp_operand_image zraw1;
  struct zFp_operand_image zraw2;
  enum zFp_result_kind zresult_kind;
  uint64_t zsource_valid;
  bool zvalid;
};

// enum Fp_class
enum zFp_class { zFpZero, zFpSubnormal, zFpNormal, zFpInfinity, zFpQuietNan, zFpSignalingNan };

// union option<EFp_class%>
enum kind_zoptionzIEFp_classz5zK { Kind_zNonezIEFp_classz5zK, Kind_zSomezIEFp_classz5zK };

struct zoptionzIEFp_classz5zK {
  enum kind_zoptionzIEFp_classz5zK kind;
  union {
    struct { unit zNonezIEFp_classz5zK; };
    struct { enum zFp_class zSomezIEFp_classz5zK; };
  } variants;
};

// struct Fp_candidate_result
struct zFp_candidate_result {
  uint64_t zflags_mask;
  uint64_t zflags_value;
  uint64_t zgenerated_causes;
  uint64_t zprimary;
  enum zFp_result_kind zresult_kind;
  uint64_t zsecondary;
  bool zshape_valid;
  bool ztrap;
  uint64_t ztrap_errors;
};

// enum Form_id
enum zForm_id { zForm_invalid, zForm_short_abs_l_q_zz_rn_r, zForm_medium_abs_b_w_l_q_zz_ea_e, zForm_medium_adc_b_w_l_q_zz_rn_s_rn_d, zForm_long_adc_b_w_l_q_zz_rn_s_ea_e, zForm_long_adc_b_w_l_q_zz_ea_e_rn_s, zForm_extrashort_add_q_8_sp, zForm_short_add_l_q_zz_rn_s_rn_d, zForm_short_add_q_imm8_i_sp, zForm_medium_add_q_imm16s_sp, zForm_medium_add_q_imm32s_sp, zForm_medium_add_b_w_l_q_zz_rn_s_ea_e, zForm_medium_add_b_w_l_q_zz_ea_e_rn_d, zForm_medium_add_b_w_l_q_zz_imm8s_ea_e, zForm_medium_add_w_l_q_zz_imm16s_ea_e, zForm_medium_add_l_q_zz_imm32s_ea_e, zForm_medium_add_q_imm64_ea_e, zForm_extrashort_afence_plain, zForm_short_and_l_q_zz_rn_s_rn_d, zForm_medium_and_b_w_l_q_zz_rn_s_ea_e, zForm_medium_and_b_w_l_q_zz_ea_e_rn_d, zForm_medium_and_b_w_l_q_zz_imm8s_ea_e, zForm_medium_and_w_l_q_zz_imm16s_ea_e, zForm_medium_and_l_q_zz_imm32s_ea_e, zForm_medium_and_q_imm64_ea_e, zForm_long_bchg_rn_b_ea_e, zForm_long_bchg_imm6_i_ea_e, zForm_medium_bchg_rn_b_rn_e, zForm_long_bchg_imm6_i_rn_e, zForm_long_bclr_rn_b_ea_e, zForm_long_bclr_imm6_i_ea_e, zForm_medium_bclr_rn_b_rn_e, zForm_long_bclr_imm6_i_rn_e, zForm_extrashort_bkpt_plain, zForm_extralong_bndsii_b_w_l_q_zz_rn_l_ea_e_rn_h, zForm_extralong_bndsii_b_w_l_q_zz_rn_l_rn_v_rn_h, zForm_extralong_bndsix_b_w_l_q_zz_rn_l_ea_e_rn_h, zForm_extralong_bndsix_b_w_l_q_zz_rn_l_rn_v_rn_h, zForm_extralong_bndsxi_b_w_l_q_zz_rn_l_ea_e_rn_h, zForm_extralong_bndsxi_b_w_l_q_zz_rn_l_rn_v_rn_h, zForm_extralong_bndsxx_b_w_l_q_zz_rn_l_ea_e_rn_h, zForm_extralong_bndsxx_b_w_l_q_zz_rn_l_rn_v_rn_h, zForm_extralong_bnduii_b_w_l_q_zz_rn_l_ea_e_rn_h, zForm_extralong_bnduii_b_w_l_q_zz_rn_l_rn_v_rn_h, zForm_extralong_bnduix_b_w_l_q_zz_rn_l_ea_e_rn_h, zForm_extralong_bnduix_b_w_l_q_zz_rn_l_rn_v_rn_h, zForm_extralong_bnduxi_b_w_l_q_zz_rn_l_ea_e_rn_h, zForm_extralong_bnduxi_b_w_l_q_zz_rn_l_rn_v_rn_h, zForm_extralong_bnduxx_b_w_l_q_zz_rn_l_ea_e_rn_h, zForm_extralong_bnduxx_b_w_l_q_zz_rn_l_rn_v_rn_h, zForm_long_bset_rn_b_ea_e, zForm_long_bset_imm6_i_ea_e, zForm_medium_bset_rn_b_rn_e, zForm_long_bset_imm6_i_rn_e, zForm_long_btest_rn_b_ea_e, zForm_long_btest_imm6_i_ea_e, zForm_medium_btest_rn_b_rn_e, zForm_long_btest_imm6_i_rn_e, zForm_medium_call_imm16s, zForm_medium_call_imm32s, zForm_medium_call_ea_e, zForm_medium_call_rn_r, zForm_medium_callcc_imm16s, zForm_medium_callcc_imm32s, zForm_long_callcc_ea_e, zForm_long_callcc_rn_r, zForm_long_clmul_b_w_l_q_zz_ea_e_rn_d, zForm_medium_clmul_b_w_l_q_zz_rn_s_rn_d, zForm_long_clmulh_q_ea_e_rn_d, zForm_medium_clmulh_q_rn_s_rn_d, zForm_extrashort_clr_q_rn_r, zForm_short_clr_l_rn_r, zForm_medium_clr_b_w_l_q_zz_ea_e, zForm_long_cls_b_w_l_q_zz_ea_e_rn_d, zForm_medium_cls_b_w_l_q_zz_rn_s_rn_d, zForm_long_clzz_b_w_l_q_zz_ea_e_rn_d, zForm_medium_clzz_b_w_l_q_zz_rn_s_rn_d, zForm_short_cmp_l_q_zz_rn_s_rn_d, zForm_medium_cmp_b_w_l_q_zz_rn_s_ea_e, zForm_medium_cmp_b_w_l_q_zz_ea_e_rn_d, zForm_long_cmp_b_w_l_q_zz_ea_s_ea_d, zForm_long_cmpjcc_b_w_l_q_zz_rn_s_rn_d_imm8s, zForm_long_cmpjcc_b_w_l_q_zz_rn_s_rn_d_imm16s, zForm_extralong_cmpxchg_b_w_l_q_zz_order_o_rn_x_rn_d_ea_e, zForm_medium_cpuid_rn_r, zForm_long_cts_b_w_l_q_zz_ea_e_rn_d, zForm_medium_cts_b_w_l_q_zz_rn_s_rn_d, zForm_long_ctzz_b_w_l_q_zz_ea_e_rn_d, zForm_medium_ctzz_b_w_l_q_zz_rn_s_rn_d, zForm_short_dec_l_q_zz_rn_r, zForm_medium_dec_b_w_l_q_zz_ea_e, zForm_medium_decf_b_w_l_q_zz_rn_r, zForm_extralong_divmods_b_w_l_q_zz_ea_e_rn_q_rn_r, zForm_extralong_divmods_b_w_l_q_zz_rn_e_rn_q_rn_r, zForm_extralong_divmodu_b_w_l_q_zz_ea_e_rn_q_rn_r, zForm_extralong_divmodu_b_w_l_q_zz_rn_e_rn_q_rn_r, zForm_long_divs_b_w_l_q_zz_ea_e_rn_d, zForm_medium_divs_b_w_l_q_zz_rn_s_rn_d, zForm_long_divu_b_w_l_q_zz_ea_e_rn_d, zForm_medium_divu_b_w_l_q_zz_rn_s_rn_d, zForm_long_djcc_rn_r_ea_e, zForm_long_djcc_rn_r_rn_e, zForm_extrashort_eret_plain, zForm_extralong_extract_b_w_l_q_zz_imm7_i_rn_h_rn_l, zForm_long_extsl_b_rn_s_ea_e, zForm_long_extsl_w_rn_s_ea_e, zForm_long_extsl_b_w_zz_ea_s_ea_d, zForm_medium_extsq_b_rn_s_rn_d, zForm_medium_extsq_w_rn_s_rn_d, zForm_short_extsq_l_rn_s_rn_d, zForm_long_extsq_b_rn_s_ea_e, zForm_medium_extsq_b_ea_e_rn_d, zForm_long_extsq_w_rn_s_ea_e, zForm_medium_extsq_w_ea_e_rn_d, zForm_long_extsq_l_rn_s_ea_e, zForm_medium_extsq_l_ea_e_rn_d, zForm_long_extsq_b_ea_s_ea_d, zForm_long_extsq_w_ea_s_ea_d, zForm_long_extsq_l_ea_s_ea_d, zForm_long_extsw_b_rn_s_ea_e, zForm_long_extsw_b_ea_s_ea_d, zForm_long_extzzl_b_rn_s_ea_e, zForm_long_extzzl_w_rn_s_ea_e, zForm_long_extzzl_b_w_zz_ea_s_ea_d, zForm_long_extzzq_b_rn_s_ea_e, zForm_long_extzzq_w_rn_s_ea_e, zForm_long_extzzq_l_rn_s_ea_e, zForm_long_extzzq_b_ea_s_ea_d, zForm_long_extzzq_w_ea_s_ea_d, zForm_long_extzzq_l_ea_s_ea_d, zForm_long_extzzw_b_rn_s_ea_e, zForm_long_extzzw_b_ea_s_ea_d, zForm_extralong_fetchadd_b_w_l_q_zz_order_o_rn_s_ea_e, zForm_extralong_fetchand_b_w_l_q_zz_order_o_rn_s_ea_e, zForm_extralong_fetchor_b_w_l_q_zz_order_o_rn_s_ea_e, zForm_extralong_fetchsub_b_w_l_q_zz_order_o_rn_s_ea_e, zForm_extralong_fetchxor_b_w_l_q_zz_order_o_rn_s_ea_e, zForm_medium_flshdcache_ea_e, zForm_short_halt_plain, zForm_extralong_ijcc_rn_i_rn_b_ea_e, zForm_extralong_ijcc_rn_i_rn_b_rn_e, zForm_extrashort_illegal_plain, zForm_short_inc_l_q_zz_rn_r, zForm_medium_inc_b_w_l_q_zz_ea_e, zForm_medium_incf_b_w_l_q_zz_rn_r, zForm_medium_invasid_imm16, zForm_medium_invdcache_ea_e, zForm_medium_invicache_ea_e, zForm_medium_invpage_ea_e, zForm_medium_invpage_rn_r, zForm_medium_invtlb_plain, zForm_short_jcc_imm8s_i, zForm_medium_jcc_imm16s, zForm_medium_jcc_imm32s, zForm_long_jcc_l_q_zz_ea_e, zForm_long_jcc_l_q_zz_rn_r, zForm_short_jmp_imm8s_i, zForm_medium_jmp_imm16s, zForm_medium_jmp_imm32s, zForm_medium_jmp_l_q_zz_ea_e, zForm_medium_jmp_l_q_zz_rn_r, zForm_long_lcall_rn_r_ea_e, zForm_medium_lcall_rn_s_rn_d, zForm_medium_lea_b_w_l_q_zz_ea_e_rn_d, zForm_medium_lea_b_w_l_q_zz_rn_s_rn_d, zForm_long_ljmp_rn_r_ea_e, zForm_medium_ljmp_rn_s_rn_d, zForm_extrashort_lret_plain, zForm_long_maxs_b_w_l_q_zz_ea_e_rn_d, zForm_long_maxs_b_w_l_q_zz_rn_s_ea_e, zForm_medium_maxs_b_w_l_q_zz_rn_s_rn_d, zForm_long_maxu_b_w_l_q_zz_ea_e_rn_d, zForm_long_maxu_b_w_l_q_zz_rn_s_ea_e, zForm_medium_maxu_b_w_l_q_zz_rn_s_rn_d, zForm_long_mins_b_w_l_q_zz_ea_e_rn_d, zForm_long_mins_b_w_l_q_zz_rn_s_ea_e, zForm_medium_mins_b_w_l_q_zz_rn_s_rn_d, zForm_long_minu_b_w_l_q_zz_ea_e_rn_d, zForm_long_minu_b_w_l_q_zz_rn_s_ea_e, zForm_medium_minu_b_w_l_q_zz_rn_s_rn_d, zForm_long_mods_b_w_l_q_zz_ea_e_rn_d, zForm_medium_mods_b_w_l_q_zz_rn_s_rn_d, zForm_long_modu_b_w_l_q_zz_ea_e_rn_d, zForm_medium_modu_b_w_l_q_zz_rn_s_rn_d, zForm_extrashort_mov_q_rn_r_sp, zForm_extrashort_mov_q_sp_rn_r, zForm_short_mov_l_q_zz_rn_s_rn_d, zForm_short_mov_b_rn_s_rn_d, zForm_short_mov_w_rn_s_rn_d, zForm_medium_mov_b_w_l_q_zz_rn_s_ea_e, zForm_medium_mov_b_w_l_q_zz_ea_e_rn_d, zForm_long_mov_b_w_l_q_zz_ea_s_ea_d, zForm_extralong_movcc_b_w_l_q_zz_rn_s_ea_e, zForm_extralong_movcc_b_w_l_q_zz_ea_e_rn_d, zForm_long_movcc_b_w_l_q_zz_rn_s_rn_d, zForm_long_movcu_b_w_l_q_zz_ea_s_ea_d, zForm_medium_movcu_b_w_l_q_zz_rn_s_rn_d, zForm_long_movcu_b_w_l_q_zz_rn_s_ea_d, zForm_long_movcu_b_w_l_q_zz_ea_s_rn_d, zForm_long_movnt_b_w_l_q_zz_rn_s_ea_e, zForm_long_movuc_b_w_l_q_zz_ea_s_ea_d, zForm_medium_movuc_b_w_l_q_zz_rn_s_rn_d, zForm_long_movuc_b_w_l_q_zz_rn_s_ea_d, zForm_long_movuc_b_w_l_q_zz_ea_s_rn_d, zForm_long_movuu_b_w_l_q_zz_ea_s_ea_d, zForm_long_mul_b_w_l_q_zz_ea_e_rn_d, zForm_medium_mul_b_w_l_q_zz_rn_s_rn_d, zForm_medium_mulhs_q_rn_s_rn_d, zForm_medium_mulhsu_q_rn_s_rn_d, zForm_medium_mulhu_q_rn_s_rn_d, zForm_short_neg_l_q_zz_rn_r, zForm_medium_neg_b_w_l_q_zz_ea_e, zForm_extrashort_nop_plain, zForm_short_not_l_q_zz_rn_r, zForm_medium_not_b_w_l_q_zz_ea_e, zForm_short_or_l_q_zz_rn_s_rn_d, zForm_medium_or_b_w_l_q_zz_rn_s_ea_e, zForm_medium_or_b_w_l_q_zz_ea_e_rn_d, zForm_medium_or_b_w_l_q_zz_imm8s_ea_e, zForm_medium_or_w_l_q_zz_imm16s_ea_e, zForm_medium_or_l_q_zz_imm32s_ea_e, zForm_medium_or_q_imm64_ea_e, zForm_long_parity_b_w_l_q_zz_ea_e_rn_d, zForm_medium_parity_b_w_l_q_zz_rn_s_rn_d, zForm_extrashort_pop_rn_r, zForm_short_pop_sreg_s, zForm_long_popcnt_b_w_l_q_zz_ea_e_rn_d, zForm_medium_popcnt_b_w_l_q_zz_rn_s_rn_d, zForm_extrashort_popp_pairn_i, zForm_medium_prefetch_ea_e, zForm_medium_prefetchnt_ea_e, zForm_long_ptquery_pt_level_i_ea_e_rn_d, zForm_long_ptquery_pt_level_i_rn_s_rn_d, zForm_extrashort_push_cs, zForm_extrashort_push_rn_r, zForm_short_push_sreg_s, zForm_extrashort_pushp_pairn_i, zForm_medium_rdcr_imm16_rn_d, zForm_medium_rdflags_rn_d, zForm_medium_rdpmc_imm16_rn_d, zForm_medium_rdseg_sreg_s_rn_d, zForm_medium_rdseg_cs_rn_d, zForm_medium_rdstatus_rn_d, zForm_medium_repcc_rn_r_instruction, zForm_short_reset_plain, zForm_medium_restore_ea_e, zForm_medium_restore_rn_r, zForm_extrashort_ret_plain, zForm_short_revbyte_w_rn_r, zForm_short_revbyte_l_rn_r, zForm_short_revbyte_q_rn_r, zForm_medium_revbyte_w_ea_e, zForm_medium_revbyte_l_ea_e, zForm_medium_revbyte_q_ea_e, zForm_extrashort_rfence_plain, zForm_short_rol_l_q_zz_rn_s_rn_d, zForm_long_rol_b_w_l_q_zz_rn_s_ea_e, zForm_long_rol_b_w_l_q_zz_imm6_i_ea_e, zForm_short_ror_l_q_zz_rn_s_rn_d, zForm_long_ror_b_w_l_q_zz_rn_s_ea_e, zForm_long_ror_b_w_l_q_zz_imm6_i_ea_e, zForm_short_sar_l_q_zz_rn_s_rn_d, zForm_long_sar_b_w_l_q_zz_rn_s_ea_e, zForm_long_sar_b_w_l_q_zz_imm6_i_ea_e, zForm_medium_save_ea_e, zForm_medium_save_rn_r, zForm_medium_sbb_b_w_l_q_zz_rn_s_rn_d, zForm_long_sbb_b_w_l_q_zz_rn_s_ea_e, zForm_long_sbb_b_w_l_q_zz_ea_e_rn_d, zForm_long_seglea_b_w_l_q_zz_ea_e_rn_d, zForm_medium_seglea_b_w_l_q_zz_rn_s_rn_d, zForm_short_set_rn_r, zForm_short_setcc_rn_r, zForm_medium_setf_flags_bitmap_m, zForm_short_shl_l_q_zz_rn_s_rn_d, zForm_long_shl_b_w_l_q_zz_rn_s_ea_e, zForm_long_shl_b_w_l_q_zz_imm6_i_ea_e, zForm_short_shr_l_q_zz_rn_s_rn_d, zForm_long_shr_b_w_l_q_zz_rn_s_ea_e, zForm_long_shr_b_w_l_q_zz_imm6_i_ea_e, zForm_extrashort_sub_q_8_sp, zForm_short_sub_l_q_zz_rn_s_rn_d, zForm_short_sub_q_imm8_i_sp, zForm_medium_sub_q_imm16s_sp, zForm_medium_sub_q_imm32s_sp, zForm_medium_sub_b_w_l_q_zz_rn_s_ea_e, zForm_medium_sub_b_w_l_q_zz_ea_e_rn_d, zForm_long_sub_b_w_l_q_zz_imm8s_ea_e, zForm_long_sub_w_l_q_zz_imm16s_ea_e, zForm_long_sub_l_q_zz_imm32s_ea_e, zForm_medium_sub_q_imm64_ea_e, zForm_medium_swpt_rn_p, zForm_medium_swpta_rn_p_rn_a, zForm_medium_synccache_ea_e, zForm_extrashort_syscall_plain, zForm_short_test_l_q_zz_rn_s_rn_d, zForm_long_test_b_w_l_q_zz_rn_s_ea_e, zForm_medium_test_b_w_l_q_zz_ea_e_rn_d, zForm_long_testjcc_b_w_l_q_zz_rn_s_rn_d_imm8s, zForm_long_testjcc_b_w_l_q_zz_rn_s_rn_d_imm16s, zForm_medium_trace_imm16, zForm_medium_vtop_rn_v_rn_p, zForm_extrashort_wait_plain, zForm_extrashort_wfence_plain, zForm_medium_wrbkdcache_ea_e, zForm_medium_wrcr_rn_s_imm16, zForm_medium_wrflags_rn_s, zForm_medium_wrseg_rn_d_sreg_s, zForm_medium_wrstatus_rn_s, zForm_short_xchg_l_q_zz_rn_s_rn_d, zForm_long_xchg_b_w_l_q_zz_rn_s_ea_e, zForm_long_xchg_b_w_l_q_zz_ea_e_rn_d, zForm_short_xor_l_q_zz_rn_s_rn_d, zForm_medium_xor_b_w_l_q_zz_rn_s_ea_e, zForm_medium_xor_b_w_l_q_zz_ea_e_rn_d, zForm_long_xor_b_w_l_q_zz_imm8s_ea_e, zForm_long_xor_w_l_q_zz_imm16s_ea_e, zForm_long_xor_l_q_zz_imm32s_ea_e, zForm_medium_xor_q_imm64_ea_e, zForm_extrashort_yield_plain, zForm_medium_fabs_s_d_zz_fn_s_fn_d, zForm_long_fabs_s_d_zz_ea_e_fn_d, zForm_long_fabs_s_d_zz_fn_s_ea_e, zForm_medium_fadd_s_d_zz_fn_s_fn_d, zForm_long_fadd_s_d_zz_ea_e_fn_d, zForm_extralong_fbndii_s_d_zz_fn_l_fn_v_fn_h, zForm_extralong_fbndii_s_d_zz_fn_l_ea_v_fn_h, zForm_extralong_fbndii_s_d_zz_ea_l_fn_v_ea_h, zForm_extralong_fbndix_s_d_zz_fn_l_fn_v_fn_h, zForm_extralong_fbndix_s_d_zz_fn_l_ea_v_fn_h, zForm_extralong_fbndix_s_d_zz_ea_l_fn_v_ea_h, zForm_extralong_fbndxi_s_d_zz_fn_l_fn_v_fn_h, zForm_extralong_fbndxi_s_d_zz_fn_l_ea_v_fn_h, zForm_extralong_fbndxi_s_d_zz_ea_l_fn_v_ea_h, zForm_extralong_fbndxx_s_d_zz_fn_l_fn_v_fn_h, zForm_extralong_fbndxx_s_d_zz_fn_l_ea_v_fn_h, zForm_extralong_fbndxx_s_d_zz_ea_l_fn_v_ea_h, zForm_medium_fceil_s_d_zz_fn_s_fn_d, zForm_long_fceil_s_d_zz_ea_e_fn_d, zForm_long_fceil_s_d_zz_fn_s_ea_e, zForm_long_fclass_s_d_zz_fn_s_rn_d, zForm_medium_fclr_fn_d, zForm_medium_fcmp_s_d_zz_fn_s_fn_d, zForm_long_fcmp_s_d_zz_ea_e_fn_d, zForm_long_fcopysign_s_d_zz_fn_s_fn_m_fn_d, zForm_medium_fcvt_s_d_zz_fn_s_fn_d, zForm_long_fcvt_s_d_zz_fn_s_rn_d, zForm_long_fcvt_s_d_zz_rn_s_fn_d, zForm_medium_fcvtu_s_d_zz_fn_s_fn_d, zForm_long_fcvtu_s_d_zz_fn_s_rn_d, zForm_long_fcvtu_s_d_zz_rn_s_fn_d, zForm_medium_fdiv_s_d_zz_fn_s_fn_d, zForm_long_fdiv_s_d_zz_ea_e_fn_d, zForm_medium_ffloor_s_d_zz_fn_s_fn_d, zForm_long_ffloor_s_d_zz_ea_e_fn_d, zForm_long_ffloor_s_d_zz_fn_s_ea_e, zForm_long_fgetexp_s_d_zz_ea_e_fn_d, zForm_medium_fgetexp_s_d_zz_fn_s_fn_d, zForm_long_fgetman_s_d_zz_ea_e_fn_d, zForm_medium_fgetman_s_d_zz_fn_s_fn_d, zForm_long_fint_s_d_zz_ea_e_fn_d, zForm_medium_fint_s_d_zz_fn_s_fn_d, zForm_long_fint_s_d_zz_fn_s_ea_e, zForm_long_fintrzz_s_d_zz_ea_e_fn_d, zForm_medium_fintrzz_s_d_zz_fn_s_fn_d, zForm_long_fintrzz_s_d_zz_fn_s_ea_e, zForm_long_fmadd_s_d_zz_fn_l_fn_r_fn_d, zForm_extralong_fmadd_s_d_zz_ea_l_fn_r_fn_d, zForm_extralong_fmadd_s_d_zz_fn_l_ea_r_fn_d, zForm_medium_fmax_s_d_zz_fn_s_fn_d, zForm_long_fmax_s_d_zz_ea_e_fn_d, zForm_medium_fmin_s_d_zz_fn_s_fn_d, zForm_long_fmin_s_d_zz_ea_e_fn_d, zForm_long_fmod_s_d_zz_ea_e_fn_d, zForm_medium_fmod_s_d_zz_fn_s_fn_d, zForm_medium_fmov_s_d_zz_fn_s_fn_d, zForm_long_fmov_s_d_zz_ea_e_fn_d, zForm_long_fmov_s_d_zz_fn_s_ea_e, zForm_long_fmovcc_fn_s_fn_d, zForm_long_fmovcc_s_d_zz_ea_e_fn_d, zForm_long_fmovcc_s_d_zz_fn_s_ea_e, zForm_medium_fmovcr_s_d_zz_fconst_id_fn_d, zForm_long_fmsub_s_d_zz_fn_l_fn_r_fn_d, zForm_extralong_fmsub_s_d_zz_ea_l_fn_r_fn_d, zForm_extralong_fmsub_s_d_zz_fn_l_ea_r_fn_d, zForm_medium_fmul_s_d_zz_fn_s_fn_d, zForm_long_fmul_s_d_zz_ea_e_fn_d, zForm_medium_fneg_s_d_zz_fn_s_fn_d, zForm_long_fneg_s_d_zz_ea_e_fn_d, zForm_long_fneg_s_d_zz_fn_s_ea_e, zForm_long_fnmadd_s_d_zz_fn_l_fn_r_fn_d, zForm_extralong_fnmadd_s_d_zz_ea_l_fn_r_fn_d, zForm_extralong_fnmadd_s_d_zz_fn_l_ea_r_fn_d, zForm_long_fnmsub_s_d_zz_fn_l_fn_r_fn_d, zForm_extralong_fnmsub_s_d_zz_ea_l_fn_r_fn_d, zForm_extralong_fnmsub_s_d_zz_fn_l_ea_r_fn_d, zForm_extrashort_fpopp_fpairn_i, zForm_extrashort_fpushp_fpairn_i, zForm_long_frem_s_d_zz_ea_e_fn_d, zForm_medium_frem_s_d_zz_fn_s_fn_d, zForm_medium_fround_s_d_zz_fn_s_fn_d, zForm_long_fround_s_d_zz_ea_e_fn_d, zForm_long_fround_s_d_zz_fn_s_ea_e, zForm_long_fscale_s_d_zz_ea_e_fn_d, zForm_medium_fscale_s_d_zz_fn_s_fn_d, zForm_medium_fsqrt_s_d_zz_fn_s_fn_d, zForm_long_fsqrt_s_d_zz_ea_e_fn_d, zForm_long_fsqrt_s_d_zz_fn_s_ea_e, zForm_medium_fsub_s_d_zz_fn_s_fn_d, zForm_long_fsub_s_d_zz_ea_e_fn_d, zForm_long_ftest_s_d_zz_ea_e, zForm_medium_ftest_s_d_zz_fn_s, zForm_medium_ftrunc_s_d_zz_fn_s_fn_d, zForm_long_ftrunc_s_d_zz_ea_e_fn_d, zForm_long_ftrunc_s_d_zz_fn_s_ea_e, zForm_medium_fxchg_fn_l_fn_r, zForm_medium_rdfflags_rn_d, zForm_medium_rdfstatus_rn_d, zForm_medium_wrfflags_rn_s, zForm_medium_wrfstatus_rn_s, zForm_long_facosa_s_d_zz_fn_s_fn_d, zForm_long_fasina_s_d_zz_fn_s_fn_d, zForm_long_fatana_s_d_zz_fn_s_fn_d, zForm_long_fatanha_s_d_zz_fn_s_fn_d, zForm_long_fcosa_s_d_zz_fn_s_fn_d, zForm_long_fcosha_s_d_zz_fn_s_fn_d, zForm_long_fetoxa_s_d_zz_fn_s_fn_d, zForm_long_fetoxm1a_s_d_zz_fn_s_fn_d, zForm_long_flog10a_s_d_zz_fn_s_fn_d, zForm_long_flog2a_s_d_zz_fn_s_fn_d, zForm_long_flogna_s_d_zz_fn_s_fn_d, zForm_long_flognp1a_s_d_zz_fn_s_fn_d, zForm_long_fsina_s_d_zz_fn_s_fn_d, zForm_long_fsincosa_s_d_zz_fn_s_fn_d_fn_c, zForm_long_fsinha_s_d_zz_fn_s_fn_d, zForm_long_ftana_s_d_zz_fn_s_fn_d, zForm_long_ftanha_s_d_zz_fn_s_fn_d, zForm_long_ftentoxa_s_d_zz_fn_s_fn_d, zForm_long_ftwotoxa_s_d_zz_fn_s_fn_d, zForm_long_vdup_b_w_l_q_zz_rn_r_vn_v, zForm_long_vdup_h_s_d_zz_fn_r_vn_v, zForm_long_vdup_b_imm8_vn_v, zForm_long_vdup_w_imm16_vn_v, zForm_long_vdup_l_imm32_vn_v, zForm_long_vdup_q_imm64_vn_v, zForm_long_vmov_vn_v_vn_w, zForm_extralong_vmov_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_xxlong_vmov_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vmov_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_long_phead_b_w_l_q_zz_rn_r_pn_p, zForm_long_ptail_b_w_l_q_zz_rn_r_pn_p, zForm_long_pfirst_b_w_l_q_zz_pn_p_rn_r, zForm_long_plast_b_w_l_q_zz_pn_p_rn_r, zForm_long_pcount_b_w_l_q_zz_pn_p_rn_r, zForm_long_pand_pn_p_pn_q, zForm_long_por_pn_p_pn_q, zForm_long_pxor_pn_p_pn_q, zForm_long_punpklo_b_w_l_zz_pn_p_pn_q, zForm_long_punpkhi_b_w_l_zz_pn_p_pn_q, zForm_long_ppacklo_w_l_q_zz_pn_p_pn_q, zForm_long_ppackhi_w_l_q_zz_pn_p_pn_q, zForm_long_vclr_vn_v, zForm_long_vindex_b_w_l_q_zz_vn_v, zForm_long_vlcnt_b_w_l_q_zz_rn_r, zForm_long_vlcadd_b_w_l_q_zz_imm8s_rn_r, zForm_xxlong_vgather1_b_w_l_q_zz_pn_p_rn_b_add_rn_i_mul_rn_s_vn_v, zForm_xxlong_vgather1_l_pn_p_vn_x_rn_i_vn_v, zForm_xxlong_vgather1_q_pn_p_vn_x_rn_i_vn_v, zForm_xxlong_vgather1_b_w_l_q_zz_pn_p_rn_b_add_vn_x_rn_i_vn_v, zForm_xxlong_vgather1_b_w_l_q_zz_pn_p_rn_b_add_vn_x_rn_i_mul_scale_vn_v, zForm_xxlong_vgather1_b_w_l_q_zz_pn_p_rn_b_add_vn_x_rn_i_mul_scale_add_disp8s_vn_v, zForm_xxlong_vgather1_b_w_l_q_zz_pn_p_rn_b_add_vn_x_rn_i_mul_scale_add_disp16s_vn_v, zForm_xxlong_vgather1_b_w_l_q_zz_pn_p_rn_b_add_vn_x_rn_i_mul_scale_add_disp32s_vn_v, zForm_xxlong_vgather1_b_w_l_q_zz_pn_p_rn_b_add_vn_x_rn_i_mul_scale_add_disp64_vn_v, zForm_xxlong_vscatter1_b_w_l_q_zz_pn_p_vn_v_rn_b_add_rn_i_mul_rn_s, zForm_xxlong_vscatter1_l_pn_p_vn_v_vn_x_rn_i, zForm_xxlong_vscatter1_q_pn_p_vn_v_vn_x_rn_i, zForm_xxlong_vscatter1_b_w_l_q_zz_pn_p_vn_v_rn_b_add_vn_x_rn_i, zForm_xxlong_vscatter1_b_w_l_q_zz_pn_p_vn_v_rn_b_add_vn_x_rn_i_mul_scale, zForm_xxlong_vscatter1_b_w_l_q_zz_pn_p_vn_v_rn_b_add_vn_x_rn_i_mul_scale_add_disp8s, zForm_xxlong_vscatter1_b_w_l_q_zz_pn_p_vn_v_rn_b_add_vn_x_rn_i_mul_scale_add_disp16s, zForm_xxlong_vscatter1_b_w_l_q_zz_pn_p_vn_v_rn_b_add_vn_x_rn_i_mul_scale_add_disp32s, zForm_xxlong_vscatter1_b_w_l_q_zz_pn_p_vn_v_rn_b_add_vn_x_rn_i_mul_scale_add_disp64, zForm_long_ptrue_b_w_l_q_zz_pn_p, zForm_long_pfalse_pn_p, zForm_long_pnot_pn_p, zForm_long_bpany_pn_p_imm32s, zForm_xxlong_bpany_pn_p_ea_e, zForm_long_bpnone_pn_p_imm32s, zForm_xxlong_bpnone_pn_p_ea_e, zForm_long_bpall_b_w_l_q_zz_pn_p_imm32s, zForm_xxlong_bpall_b_w_l_q_zz_pn_p_ea_e, zForm_long_vneg_b_w_l_q_h_s_d_x_pn_p_vn_v, zForm_xxlong_vneg_b_w_l_q_h_s_d_x_pn_p_ea_e_vn_v, zForm_xxlong_vneg_b_w_l_q_h_s_d_x_pn_p_vn_v_ea_e, zForm_long_vabs_b_w_l_q_h_s_d_x_pn_p_vn_v, zForm_xxlong_vabs_b_w_l_q_h_s_d_x_pn_p_ea_e_vn_v, zForm_xxlong_vabs_b_w_l_q_h_s_d_x_pn_p_vn_v_ea_e, zForm_long_vnot_b_w_l_q_zz_pn_p_vn_v, zForm_xxlong_vnot_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vnot_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_long_vclzz_b_w_l_q_zz_pn_p_vn_v, zForm_xxlong_vclzz_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vclzz_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_long_vctzz_b_w_l_q_zz_pn_p_vn_v, zForm_xxlong_vctzz_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vctzz_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_long_vcls_b_w_l_q_zz_pn_p_vn_v, zForm_xxlong_vcls_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vcls_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_long_vcts_b_w_l_q_zz_pn_p_vn_v, zForm_xxlong_vcts_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vcts_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_long_vpopcnt_b_w_l_q_zz_pn_p_vn_v, zForm_xxlong_vpopcnt_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vpopcnt_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_long_vrevbyte_w_l_q_zz_pn_p_vn_v, zForm_xxlong_vrevbyte_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vrevbyte_w_l_q_zz_pn_p_vn_v_ea_e, zForm_long_vsqrt_h_s_d_zz_pn_p_vn_v, zForm_xxlong_vsqrt_h_s_d_zz_pn_p_ea_e_vn_v, zForm_xxlong_vsqrt_h_s_d_zz_pn_p_vn_v_ea_e, zForm_long_vround_h_s_d_zz_pn_p_vn_v, zForm_xxlong_vround_h_s_d_zz_pn_p_ea_e_vn_v, zForm_xxlong_vround_h_s_d_zz_pn_p_vn_v_ea_e, zForm_long_vtrunc_h_s_d_zz_pn_p_vn_v, zForm_xxlong_vtrunc_h_s_d_zz_pn_p_ea_e_vn_v, zForm_xxlong_vtrunc_h_s_d_zz_pn_p_vn_v_ea_e, zForm_long_vfloor_h_s_d_zz_pn_p_vn_v, zForm_xxlong_vfloor_h_s_d_zz_pn_p_ea_e_vn_v, zForm_xxlong_vfloor_h_s_d_zz_pn_p_vn_v_ea_e, zForm_long_vceil_h_s_d_zz_pn_p_vn_v, zForm_xxlong_vceil_h_s_d_zz_pn_p_ea_e_vn_v, zForm_xxlong_vceil_h_s_d_zz_pn_p_vn_v_ea_e, zForm_long_vclass_h_s_d_zz_pn_p_vn_v, zForm_xxlong_vclass_h_s_d_zz_pn_p_ea_e_vn_v, zForm_xxlong_vclass_h_s_d_zz_pn_p_vn_v_ea_e, zForm_long_pperm_b_w_l_q_zz_vn_v_pn_p, zForm_long_pslideup_b_w_l_q_zz_imm6_i_pn_p, zForm_long_pslidedn_b_w_l_q_zz_imm6_i_pn_p, zForm_extralong_vcmpcc_b_w_l_q_x_pn_p_vn_v_vn_w_pn_q, zForm_extralong_vcmpcc_h_s_d_x_pn_p_vn_v_vn_w_pn_q, zForm_xxlong_vcmpcc_b_w_l_q_x_pn_p_vn_v_ea_e_pn_q, zForm_xxlong_vcmpcc_h_s_d_x_pn_p_vn_v_ea_e_pn_q, zForm_extralong_vtestzz_b_w_l_q_zz_pn_p_vn_v_vn_w_pn_q, zForm_xxlong_vtestzz_b_w_l_q_zz_pn_p_vn_v_ea_e_pn_q, zForm_extralong_vtestnzz_b_w_l_q_zz_pn_p_vn_v_vn_w_pn_q, zForm_xxlong_vtestnzz_b_w_l_q_zz_pn_p_vn_v_ea_e_pn_q, zForm_extralong_vadd_b_w_l_q_h_s_d_x_pn_p_vn_v_vn_w, zForm_xxlong_vadd_b_w_l_q_h_s_d_x_pn_p_ea_e_vn_v, zForm_xxlong_vadd_b_w_l_q_h_s_d_x_pn_p_vn_v_ea_e, zForm_extralong_vsub_b_w_l_q_h_s_d_x_pn_p_vn_v_vn_w, zForm_xxlong_vsub_b_w_l_q_h_s_d_x_pn_p_ea_e_vn_v, zForm_xxlong_vsub_b_w_l_q_h_s_d_x_pn_p_vn_v_ea_e, zForm_extralong_vmul_b_w_l_q_h_s_d_x_pn_p_vn_v_vn_w, zForm_xxlong_vmul_b_w_l_q_h_s_d_x_pn_p_ea_e_vn_v, zForm_xxlong_vmul_b_w_l_q_h_s_d_x_pn_p_vn_v_ea_e, zForm_extralong_vand_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_xxlong_vand_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vand_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_extralong_vor_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_xxlong_vor_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vor_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_extralong_vxor_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_xxlong_vxor_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vxor_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_extralong_vmins_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_xxlong_vmins_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vmins_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_extralong_vminu_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_xxlong_vminu_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vminu_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_extralong_vmaxs_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_xxlong_vmaxs_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vmaxs_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_extralong_vmaxu_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_xxlong_vmaxu_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vmaxu_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_extralong_vmulhs_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_xxlong_vmulhs_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vmulhs_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_extralong_vmulhu_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_xxlong_vmulhu_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vmulhu_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_extralong_vmulhsu_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_xxlong_vmulhsu_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vmulhsu_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_extralong_vshl_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vshl_b_w_l_q_zz_pn_p_imm6_i_vn_v, zForm_xxlong_vshl_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vshl_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_xxlong_vshl_b_w_l_q_zz_pn_p_imm6_i_ea_e, zForm_extralong_vshr_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vshr_b_w_l_q_zz_pn_p_imm6_i_vn_v, zForm_xxlong_vshr_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vshr_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_xxlong_vshr_b_w_l_q_zz_pn_p_imm6_i_ea_e, zForm_extralong_vsar_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vsar_b_w_l_q_zz_pn_p_imm6_i_vn_v, zForm_xxlong_vsar_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vsar_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_xxlong_vsar_b_w_l_q_zz_pn_p_imm6_i_ea_e, zForm_extralong_vrol_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vrol_b_w_l_q_zz_pn_p_imm6_i_vn_v, zForm_xxlong_vrol_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vrol_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_xxlong_vrol_b_w_l_q_zz_pn_p_imm6_i_ea_e, zForm_extralong_vror_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vror_b_w_l_q_zz_pn_p_imm6_i_vn_v, zForm_xxlong_vror_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_vror_b_w_l_q_zz_pn_p_vn_v_ea_e, zForm_xxlong_vror_b_w_l_q_zz_pn_p_imm6_i_ea_e, zForm_extralong_vmin_h_s_d_zz_pn_p_vn_v_vn_w, zForm_xxlong_vmin_h_s_d_zz_pn_p_ea_e_vn_v, zForm_xxlong_vmin_h_s_d_zz_pn_p_vn_v_ea_e, zForm_extralong_vmax_h_s_d_zz_pn_p_vn_v_vn_w, zForm_xxlong_vmax_h_s_d_zz_pn_p_ea_e_vn_v, zForm_xxlong_vmax_h_s_d_zz_pn_p_vn_v_ea_e, zForm_extralong_vdiv_h_s_d_zz_pn_p_vn_v_vn_w, zForm_xxlong_vdiv_h_s_d_zz_pn_p_ea_e_vn_v, zForm_xxlong_vdiv_h_s_d_zz_pn_p_vn_v_ea_e, zForm_extralong_vcopysign_h_s_d_zz_pn_p_vn_v_vn_w, zForm_xxlong_vcopysign_h_s_d_zz_pn_p_ea_e_vn_v, zForm_xxlong_vcopysign_h_s_d_zz_pn_p_vn_v_ea_e, zForm_extralong_vextzzw_b_zz_pn_p_vn_v_vn_w, zForm_extralong_vextsw_b_zz_pn_p_vn_v_vn_w, zForm_extralong_vextzzl_b_w_zz_pn_p_vn_v_vn_w, zForm_extralong_vextsl_b_w_zz_pn_p_vn_v_vn_w, zForm_extralong_vextzzq_b_w_l_zz_pn_p_vn_v_vn_w, zForm_extralong_vextsq_b_w_l_zz_pn_p_vn_v_vn_w, zForm_extralong_vtruncb_w_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vtruncw_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vtruncl_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vcvts_h_d_zz_pn_p_vn_v_vn_w, zForm_extralong_vcvts_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vcvtd_h_s_zz_pn_p_vn_v_vn_w, zForm_extralong_vcvtd_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vcvtus_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vcvtud_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vcvtl_h_s_d_zz_pn_p_vn_v_vn_w, zForm_extralong_vcvtul_h_s_d_zz_pn_p_vn_v_vn_w, zForm_extralong_vcvtq_h_s_d_zz_pn_p_vn_v_vn_w, zForm_extralong_vcvtuq_h_s_d_zz_pn_p_vn_v_vn_w, zForm_extralong_vperm_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vzziplo_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vzziphi_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vuzziplo_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vuzziphi_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vtrnlo_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vtrnhi_b_w_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vcvth_s_d_zz_pn_p_vn_v_vn_w, zForm_extralong_vcvth_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vcvtuh_l_q_zz_pn_p_vn_v_vn_w, zForm_extralong_vmadd_h_s_d_zz_pn_p_vn_v_vn_w_vn_y, zForm_extralong_vmsub_h_s_d_zz_pn_p_vn_v_vn_w_vn_y, zForm_extralong_vnmadd_h_s_d_zz_pn_p_vn_v_vn_w_vn_y, zForm_extralong_vnmsub_h_s_d_zz_pn_p_vn_v_vn_w_vn_y, zForm_extralong_vslice_b_w_l_q_zz_pn_p_vn_v_imm6_i_vn_w, zForm_extralong_vslideup_b_w_l_q_zz_pn_p_imm6_i_vn_v, zForm_extralong_vslidedn_b_w_l_q_zz_pn_p_imm6_i_vn_v, zForm_extralong_vextract_b_w_l_q_zz_vn_v_rn_r_rn_s, zForm_extralong_vextract_h_s_d_zz_vn_v_rn_r_fn_s, zForm_extralong_vinsert_b_w_l_q_zz_rn_r_rn_s_vn_v, zForm_extralong_vinsert_h_s_d_zz_fn_r_rn_s_vn_v, zForm_extralong_vredadd_b_w_l_q_zz_pn_p_vn_v_rn_r, zForm_extralong_vredadd_h_s_d_zz_pn_p_vn_v_fn_r, zForm_xxlong_vredadd_b_w_l_q_zz_pn_p_ea_e_rn_r, zForm_xxlong_vredadd_h_s_d_zz_pn_p_ea_e_fn_r, zForm_extralong_vredmins_b_w_l_q_zz_pn_p_vn_v_rn_r, zForm_xxlong_vredmins_b_w_l_q_zz_pn_p_ea_e_rn_r, zForm_extralong_vredminu_b_w_l_q_zz_pn_p_vn_v_rn_r, zForm_xxlong_vredminu_b_w_l_q_zz_pn_p_ea_e_rn_r, zForm_extralong_vredmaxs_b_w_l_q_zz_pn_p_vn_v_rn_r, zForm_xxlong_vredmaxs_b_w_l_q_zz_pn_p_ea_e_rn_r, zForm_extralong_vredmaxu_b_w_l_q_zz_pn_p_vn_v_rn_r, zForm_xxlong_vredmaxu_b_w_l_q_zz_pn_p_ea_e_rn_r, zForm_extralong_vredand_b_w_l_q_zz_pn_p_vn_v_rn_r, zForm_xxlong_vredand_b_w_l_q_zz_pn_p_ea_e_rn_r, zForm_extralong_vredor_b_w_l_q_zz_pn_p_vn_v_rn_r, zForm_xxlong_vredor_b_w_l_q_zz_pn_p_ea_e_rn_r, zForm_extralong_vredxor_b_w_l_q_zz_pn_p_vn_v_rn_r, zForm_xxlong_vredxor_b_w_l_q_zz_pn_p_ea_e_rn_r, zForm_extralong_vredmin_h_s_d_zz_pn_p_vn_v_fn_r, zForm_xxlong_vredmin_h_s_d_zz_pn_p_ea_e_fn_r, zForm_extralong_vredmax_h_s_d_zz_pn_p_vn_v_fn_r, zForm_xxlong_vredmax_h_s_d_zz_pn_p_ea_e_fn_r, zForm_extralong_psel_pn_p_pn_q_pn_h, zForm_extralong_pzziplo_b_w_l_q_zz_pn_p_pn_q_pn_h, zForm_extralong_pzziphi_b_w_l_q_zz_pn_p_pn_q_pn_h, zForm_extralong_puzziplo_b_w_l_q_zz_pn_p_pn_q_pn_h, zForm_extralong_puzziphi_b_w_l_q_zz_pn_p_pn_q_pn_h, zForm_extralong_ptrnlo_b_w_l_q_zz_pn_p_pn_q_pn_h, zForm_extralong_ptrnhi_b_w_l_q_zz_pn_p_pn_q_pn_h, zForm_extralong_pslice_b_w_l_q_zz_pn_p_imm6_i_pn_q, zForm_xxlong_vmovzz_b_w_l_q_zz_pn_p_ea_e_vn_v, zForm_xxlong_ploop_b_w_l_q_zz_rn_r_rn_s_pn_p_ea_e, zForm_xxlong_pmov_ea_e_pn_p, zForm_xxlong_pmov_pn_p_ea_e };

// struct Representative_record
struct zRepresentative_record {
  zz5listz8z5bvz9 zbytes;
  enum zForm_id zform_id;
};

// struct Fp_request_image
struct zFp_request_image {
  uint64_t zallowed_causes;
  uint64_t zcontract_id;
  uint64_t zcontract_word;
  bool zdazz;
  bool zdn;
  uint64_t zflags_mask;
  enum zForm_id zform_id;
  bool zftzz;
  struct zFp_operand_image zoperand0;
  struct zFp_operand_image zoperand1;
  struct zFp_operand_image zoperand2;
  sail_int zoperand_count;
  enum zSemantic_operation zoperation;
  sail_int zoperation_width;
  enum zFp_path zpath;
  enum zFp_result_kind zresult_kind;
  uint64_t zrounding_mode;
  bool ztranscendental;
  bool zvalid;
};

// union option<RFp_request_image>
enum kind_zoptionzIRFp_request_imagezK { Kind_zNonezIRFp_request_imagezK, Kind_zSomezIRFp_request_imagezK };

struct zoptionzIRFp_request_imagezK {
  enum kind_zoptionzIRFp_request_imagezK kind;
  union {
    struct { unit zNonezIRFp_request_imagezK; };
    struct { struct zFp_request_image zSomezIRFp_request_imagezK; };
  } variants;
};

// struct Fp_response_image
struct zFp_response_image {
  uint64_t zaccuracy_mask;
  struct zFp_request_image zecho;
  uint64_t zerror0_q8_8_up;
  uint64_t zerror1_q8_8_up;
  uint64_t zflags_mask;
  uint64_t zflags_value;
  uint64_t zgenerated_causes;
  uint64_t zprimary;
  enum zFp_nan_origin zprimary_nan_origin;
  enum zFp_result_kind zresult_kind;
  uint64_t zsecondary;
  enum zFp_nan_origin zsecondary_nan_origin;
  bool zvalid;
};

// union option<RFp_response_image>
enum kind_zoptionzIRFp_response_imagezK { Kind_zNonezIRFp_response_imagezK, Kind_zSomezIRFp_response_imagezK };

struct zoptionzIRFp_response_imagezK {
  enum kind_zoptionzIRFp_response_imagezK kind;
  union {
    struct { unit zNonezIRFp_response_imagezK; };
    struct { struct zFp_response_image zSomezIRFp_response_imagezK; };
  } variants;
};

// type abbreviation Floating_registers
typedef zz5vecz8z5bv64z9 zFloating_registers;

// enum Field_id
enum zField_id { zField_a, zField_b, zField_c, zField_d, zField_e, zField_h, zField_i, zField_l, zField_m, zField_o, zField_p, zField_q, zField_r, zField_s, zField_v, zField_w, zField_x, zField_y, zField_zz };

// union option<EField_id%>
enum kind_zoptionzIEField_idz5zK { Kind_zNonezIEField_idz5zK, Kind_zSomezIEField_idz5zK };

struct zoptionzIEField_idz5zK {
  enum kind_zoptionzIEField_idz5zK kind;
  union {
    struct { unit zNonezIEField_idz5zK; };
    struct { enum zField_id zSomezIEField_idz5zK; };
  } variants;
};

// enum Fault_kind
enum zFault_kind { zNoFault, zIllegalInstruction, zPrivilegeFault, zExtensionUnavailable, zInvalidControlState, zDivideByZero, zDivideOverflow, zBoundsFault, zAlignmentFault, zTranslationFault, zAccessFault, zEventFault, zFloatingPointFault, zVectorRangeFault };

// struct Transaction_response
struct zTransaction_response {
  enum zMemory_access_class zaccess_class;
  bool zatomic_store_happened;
  zz5listz8z5bvz9 zbody_bytes;
  bool zbounds_passed;
  sail_int zcache_policy;
  sail_string zdetail;
  sail_int zfault_cause;
  enum zFault_kind zfault_kind;
  uint64_t zflags;
  uint64_t zgenerated_fflags;
  enum zTransaction_response_kind zkind;
  bool zknown;
  enum zPhysical_memory_class zphysical_class;
  bool zpresent;
  uint64_t zsecondary_value;
  bool zsuccess;
  uint64_t zvalue;
  bool zwrite_flags;
};

// struct Execution_fault
struct zExecution_fault {
  bool zbus_error;
  sail_string zdetail;
  uint64_t zerror_code;
  enum zFault_kind zkind;
  enum zSemantic_operation zoperation;
};

// union option<RExecution_fault>
enum kind_zoptionzIRExecution_faultzK { Kind_zNonezIRExecution_faultzK, Kind_zSomezIRExecution_faultzK };

struct zoptionzIRExecution_faultzK {
  enum kind_zoptionzIRExecution_faultzK kind;
  union {
    struct { unit zNonezIRExecution_faultzK; };
    struct { struct zExecution_fault zSomezIRExecution_faultzK; };
  } variants;
};

// enum Event_kind
enum zEvent_kind { zEventNone, zEventSynchronous, zEventDebugTrace, zEventNmi, zEventInterrupt };

// enum Event_frame_type
enum zEvent_frame_type { zEventFrameBasic, zEventFrameError, zEventFramePage, zEventFrameAuxiliary };

// struct Event_record
struct zEvent_record {
  uint64_t zcode;
  uint64_t zerror_code;
  uint64_t zevent_aux;
  uint64_t zfault_ea;
  uint64_t zfault_linear;
  enum zEvent_frame_type zframe_type;
  enum zEvent_kind zkind;
  sail_int zpriority;
  uint64_t zsaved_pc;
};

// union option<REvent_record>
enum kind_zoptionzIREvent_recordzK { Kind_zNonezIREvent_recordzK, Kind_zSomezIREvent_recordzK };

struct zoptionzIREvent_recordzK {
  enum kind_zoptionzIREvent_recordzK kind;
  union {
    struct { unit zNonezIREvent_recordzK; };
    struct { struct zEvent_record zSomezIREvent_recordzK; };
  } variants;
};

// enum Event_family
enum zEvent_family { zEventFamilyNone, zEventFamily_DEBUG, zEventFamily_PRIVILEGE, zEventFamily_CONTROL_TRANSFER, zEventFamily_INTEGER_DIVIDE, zEventFamily_INSTRUCTION_VALIDATION, zEventFamily_ADDRESS_TRANSLATION, zEventFamily_PHYSICAL_ACCESS, zEventFamily_CONTROL_STATE, zEventFamily_BUS_FAILURE, zEventFamily_EVENT_DELIVERY_FAILURE, zEventFamily_MACHINE_STATE, zEventFamily_FLOATING_POINT, zEventFamily_VECTOR_RANGE };

// enum Encoding_class
enum zEncoding_class { zExtraShort, zShort, zMedium, zLong, zExtraLong, zXxlong };

// enum Effect_kind
enum zEffect_kind { zNoEffect, zReadMemory, zWriteMemory, zAtomicMemory, zTranslateAddress, zCacheOperation, zTlbOperation, zControlRegisterAccess, zEventDelivery, zTraceMarker, zHaltProcessor, zResetProcessor, zRepeatBody, zFenceOperation, zIntegerCompute, zFloatingPointCompute, zTranscendentalCompute };

// enum Ea_width
enum zEa_width { zEaWidth_B, zEaWidth_L, zEaWidth_Q, zEaWidth_W, zEaWidth_operation_sizze, zEaWidth_predicate };

// union option<EEa_width%>
enum kind_zoptionzIEEa_widthz5zK { Kind_zNonezIEEa_widthz5zK, Kind_zSomezIEEa_widthz5zK };

struct zoptionzIEEa_widthz5zK {
  enum kind_zoptionzIEEa_widthz5zK kind;
  union {
    struct { unit zNonezIEEa_widthz5zK; };
    struct { enum zEa_width zSomezIEEa_widthz5zK; };
  } variants;
};

// enum Ea_update_target
enum zEa_update_target { zEaUpdateTarget_b, zEaUpdateTarget_i };

// union option<EEa_update_target%>
enum kind_zoptionzIEEa_update_targetz5zK { Kind_zNonezIEEa_update_targetz5zK, Kind_zSomezIEEa_update_targetz5zK };

struct zoptionzIEEa_update_targetz5zK {
  enum kind_zoptionzIEEa_update_targetz5zK kind;
  union {
    struct { unit zNonezIEEa_update_targetz5zK; };
    struct { enum zEa_update_target zSomezIEEa_update_targetz5zK; };
  } variants;
};

// enum Ea_update_mode
enum zEa_update_mode { zEaUpdateMode_postincrement, zEaUpdateMode_predecrement };

// union option<EEa_update_mode%>
enum kind_zoptionzIEEa_update_modez5zK { Kind_zNonezIEEa_update_modez5zK, Kind_zSomezIEEa_update_modez5zK };

struct zoptionzIEEa_update_modez5zK {
  enum kind_zoptionzIEEa_update_modez5zK kind;
  union {
    struct { unit zNonezIEEa_update_modez5zK; };
    struct { enum zEa_update_mode zSomezIEEa_update_modez5zK; };
  } variants;
};

// enum Ea_segment
enum zEa_segment { zEaSegment_CS, zEaSegment_SS, zEaSegment_default, zEaSegment_explicit };

// union option<EEa_segment%>
enum kind_zoptionzIEEa_segmentz5zK { Kind_zNonezIEEa_segmentz5zK, Kind_zSomezIEEa_segmentz5zK };

struct zoptionzIEEa_segmentz5zK {
  enum kind_zoptionzIEEa_segmentz5zK kind;
  union {
    struct { unit zNonezIEEa_segmentz5zK; };
    struct { enum zEa_segment zSomezIEEa_segmentz5zK; };
  } variants;
};

// enum Ea_role
enum zEa_role { zEaRole_address, zEaRole_base, zEaRole_control_target, zEaRole_index, zEaRole_segment, zEaRole_value };

// union option<EEa_role%>
enum kind_zoptionzIEEa_rolez5zK { Kind_zNonezIEEa_rolez5zK, Kind_zSomezIEEa_rolez5zK };

struct zoptionzIEEa_rolez5zK {
  enum kind_zoptionzIEEa_rolez5zK kind;
  union {
    struct { unit zNonezIEEa_rolez5zK; };
    struct { enum zEa_role zSomezIEEa_rolez5zK; };
  } variants;
};

// enum Ea_profile
enum zEa_profile { zEaProfile_ea, zEaProfile_fea, zEaProfile_vea };

// union option<EEa_profile%>
enum kind_zoptionzIEEa_profilez5zK { Kind_zNonezIEEa_profilez5zK, Kind_zSomezIEEa_profilez5zK };

struct zoptionzIEEa_profilez5zK {
  enum kind_zoptionzIEEa_profilez5zK kind;
  union {
    struct { unit zNonezIEEa_profilez5zK; };
    struct { enum zEa_profile zSomezIEEa_profilez5zK; };
  } variants;
};

// struct Ea_pattern
struct zEa_pattern {
  uint64_t zmask;
  uint64_t zvalue;
  sail_int zwidth;
};

// enum Ea_kind
enum zEa_kind { zEaKind_escape, zEaKind_float_immediate, zEaKind_immediate, zEaKind_memory };

// enum Ea_form_id
enum zEa_form_id { zEaForm_absolute_32s, zEaForm_absolute_64, zEaForm_default_segment_base_postincrement, zEaForm_default_segment_base_predecrement, zEaForm_explicit_segment_base, zEaForm_explicit_segment_base_postincrement, zEaForm_explicit_segment_base_predecrement, zEaForm_explicit_segment_index, zEaForm_explicit_segment_index_postincrement, zEaForm_explicit_segment_index_predecrement, zEaForm_explicit_segment_zzero_base, zEaForm_explicit_segment_zzero_base_index, zEaForm_explicit_segment_zzero_base_index_postincrement, zEaForm_explicit_segment_zzero_base_index_predecrement, zEaForm_ext1, zEaForm_ext1_disp16s, zEaForm_ext1_disp32s, zEaForm_ext1_disp64, zEaForm_ext1_disp8s, zEaForm_ext2, zEaForm_ext2_disp16s, zEaForm_ext2_disp32s, zEaForm_ext2_disp64, zEaForm_ext2_disp8s, zEaForm_immediate_16s, zEaForm_immediate_32s, zEaForm_immediate_64, zEaForm_immediate_8s, zEaForm_immediate_df, zEaForm_immediate_sf, zEaForm_program_counter_disp16s, zEaForm_program_counter_disp32s, zEaForm_program_counter_disp64, zEaForm_program_counter_disp8s, zEaForm_program_counter_index, zEaForm_program_counter_index_postincrement, zEaForm_program_counter_index_predecrement, zEaForm_register_disp16s, zEaForm_register_disp32s, zEaForm_register_disp64, zEaForm_register_disp8s, zEaForm_register_indirect, zEaForm_stack_pointer_disp16s, zEaForm_stack_pointer_disp32s, zEaForm_stack_pointer_disp64, zEaForm_stack_pointer_disp8s, zEaForm_stack_pointer_index, zEaForm_stack_pointer_index_postincrement, zEaForm_stack_pointer_index_predecrement, zEaForm_stack_pointer_indirect };

// union option<EEa_form_id%>
enum kind_zoptionzIEEa_form_idz5zK { Kind_zNonezIEEa_form_idz5zK, Kind_zSomezIEEa_form_idz5zK };

struct zoptionzIEEa_form_idz5zK {
  enum kind_zoptionzIEEa_form_idz5zK kind;
  union {
    struct { unit zNonezIEEa_form_idz5zK; };
    struct { enum zEa_form_id zSomezIEEa_form_idz5zK; };
  } variants;
};

struct node_zz5listz8z5iz9 {
  unsigned int rc;
  sail_int hd;
  struct node_zz5listz8z5iz9 *tl;
};
typedef struct node_zz5listz8z5iz9 *zz5listz8z5iz9;

// struct Ea_field
struct zEa_field {
  enum zOperand_type zoperand_type;
  zz5listz8z5iz9 zpositions;
  enum zEa_role zrole;
  enum zField_id zsymbol;
};

// struct Ea_evaluation
struct zEa_evaluation {
  struct zoptionzIEOperand_domainz5zK zdomain;
  uint64_t zeffective_address;
  enum zEa_kind zkind;
  uint64_t zlinear_address;
  enum zOperand_id zoperand_name;
  struct zoptionzIEEa_rolez5zK zrole;
  sail_int zsegment;
  uint64_t zsegment_image;
  zz5listz8z5structz0zzStaged_register_updatez9 zstaged_updates;
  uint64_t zvalue;
  sail_int zwidth;
};

// union option<REa_evaluation>
enum kind_zoptionzIREa_evaluationzK { Kind_zNonezIREa_evaluationzK, Kind_zSomezIREa_evaluationzK };

struct zoptionzIREa_evaluationzK {
  enum kind_zoptionzIREa_evaluationzK kind;
  union {
    struct { unit zNonezIREa_evaluationzK; };
    struct { struct zEa_evaluation zSomezIREa_evaluationzK; };
  } variants;
};

// enum Ea_descriptor_family
enum zEa_descriptor_family { zEaDescriptor_ext1, zEaDescriptor_ext2 };

// union option<EEa_descriptor_family%>
enum kind_zoptionzIEEa_descriptor_familyz5zK { Kind_zNonezIEEa_descriptor_familyz5zK, Kind_zSomezIEEa_descriptor_familyz5zK };

struct zoptionzIEEa_descriptor_familyz5zK {
  enum kind_zoptionzIEEa_descriptor_familyz5zK kind;
  union {
    struct { unit zNonezIEEa_descriptor_familyz5zK; };
    struct { enum zEa_descriptor_family zSomezIEEa_descriptor_familyz5zK; };
  } variants;
};

// enum Ea_base
enum zEa_base { zEaBase_PC, zEaBase_SP, zEaBase_zzero };

// union option<EEa_base%>
enum kind_zoptionzIEEa_basez5zK { Kind_zNonezIEEa_basez5zK, Kind_zSomezIEEa_basez5zK };

struct zoptionzIEEa_basez5zK {
  enum kind_zoptionzIEEa_basez5zK kind;
  union {
    struct { unit zNonezIEEa_basez5zK; };
    struct { enum zEa_base zSomezIEEa_basez5zK; };
  } variants;
};

struct node_zz5listz8z5structz0zzEa_fieldz9 {
  unsigned int rc;
  struct zEa_field hd;
  struct node_zz5listz8z5structz0zzEa_fieldz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzEa_fieldz9 *zz5listz8z5structz0zzEa_fieldz9;

struct node_zz5listz8z5structz0zzEa_patternz9 {
  unsigned int rc;
  struct zEa_pattern hd;
  struct node_zz5listz8z5structz0zzEa_patternz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzEa_patternz9 *zz5listz8z5structz0zzEa_patternz9;

// struct Ea_form
struct zEa_form {
  struct zoptionzIEEa_basez5zK zbase;
  struct zoptionzIEEa_descriptor_familyz5zK zdescriptor;
  sail_int zdescriptor_bytes;
  struct zoptionzIEEa_descriptor_familyz5zK zdescriptor_family;
  zz5listz8z5structz0zzEa_fieldz9 zfields;
  enum zEa_kind zkind;
  enum zEa_form_id zname;
  zz5listz8z5structz0zzEa_patternz9 zpatterns;
  bool zpayload_signed;
  sail_int zpayload_width;
  struct zoptionzIEEa_profilez5zK zprofile;
  struct zoptionzIEEa_segmentz5zK zsegment;
  struct zoptionzIEEa_update_modez5zK zupdate_mode;
  struct zoptionzIEEa_update_targetz5zK zupdate_target;
};

// union option<REa_form>
enum kind_zoptionzIREa_formzK { Kind_zNonezIREa_formzK, Kind_zSomezIREa_formzK };

struct zoptionzIREa_formzK {
  enum kind_zoptionzIREa_formzK kind;
  union {
    struct { unit zNonezIREa_formzK; };
    struct { struct zEa_form zSomezIREa_formzK; };
  } variants;
};

// struct Decoded_field
struct zDecoded_field {
  enum zMetadata_field_kind zkind;
  enum zOperand_type zoperand_type;
  struct zoptionzIEEa_rolez5zK zrole;
  enum zField_id zsymbol;
  sail_int zvalue;
};

// union option<RDecoded_field>
enum kind_zoptionzIRDecoded_fieldzK { Kind_zNonezIRDecoded_fieldzK, Kind_zSomezIRDecoded_fieldzK };

struct zoptionzIRDecoded_fieldzK {
  enum kind_zoptionzIRDecoded_fieldzK kind;
  union {
    struct { unit zNonezIRDecoded_fieldzK; };
    struct { struct zDecoded_field zSomezIRDecoded_fieldzK; };
  } variants;
};

struct node_zz5listz8z5structz0zzDecoded_fieldz9 {
  unsigned int rc;
  struct zDecoded_field hd;
  struct node_zz5listz8z5structz0zzDecoded_fieldz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzDecoded_fieldz9 *zz5listz8z5structz0zzDecoded_fieldz9;

// struct Decoded_ea
struct zDecoded_ea {
  struct zoptionzIEEa_basez5zK zbase;
  enum zEa_form_id zcompact_name;
  sail_int zdescriptor_bytes;
  struct zoptionzIEEa_form_idz5zK zdescriptor_name;
  zz5listz8z5structz0zzDecoded_fieldz9 zfields;
  enum zEa_kind zkind;
  struct zoptionzIEEa_widthz5zK zoperand_width;
  uint64_t zpayload;
  bool zpayload_signed;
  sail_int zpayload_width;
  enum zEa_profile zprofile;
  sail_int zraw;
  struct zoptionzIEEa_segmentz5zK zsegment;
  struct zoptionzIEEa_update_modez5zK zupdate_mode;
  struct zoptionzIEEa_update_targetz5zK zupdate_target;
};

// union option<RDecoded_ea>
enum kind_zoptionzIRDecoded_eazK { Kind_zNonezIRDecoded_eazK, Kind_zSomezIRDecoded_eazK };

struct zoptionzIRDecoded_eazK {
  enum kind_zoptionzIRDecoded_eazK kind;
  union {
    struct { unit zNonezIRDecoded_eazK; };
    struct { struct zDecoded_ea zSomezIRDecoded_eazK; };
  } variants;
};

// struct Decoded_operand
struct zDecoded_operand {
  enum zMetadata_access zaccess;
  struct zoptionzIEOperand_domainz5zK zdomain;
  struct zoptionzIRDecoded_eazK zea;
  struct zoptionzIEEa_rolez5zK zea_role;
  struct zoptionzIEEa_widthz5zK zea_width;
  enum zOperand_id zname;
  enum zOperand_type zoperand_type;
  uint64_t zvalue;
};

// union option<RDecoded_operand>
enum kind_zoptionzIRDecoded_operandzK { Kind_zNonezIRDecoded_operandzK, Kind_zSomezIRDecoded_operandzK };

struct zoptionzIRDecoded_operandzK {
  enum kind_zoptionzIRDecoded_operandzK kind;
  union {
    struct { unit zNonezIRDecoded_operandzK; };
    struct { struct zDecoded_operand zSomezIRDecoded_operandzK; };
  } variants;
};

struct node_zz5listz8z5structz0zzDecoded_operandz9 {
  unsigned int rc;
  struct zDecoded_operand hd;
  struct node_zz5listz8z5structz0zzDecoded_operandz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzDecoded_operandz9 *zz5listz8z5structz0zzDecoded_operandz9;

// struct Operand_parse
struct zOperand_parse {
  sail_int zcursor;
  zz5listz8z5structz0zzDecoded_operandz9 zoperands;
};

// union option<ROperand_parse>
enum kind_zoptionzIROperand_parsezK { Kind_zNonezIROperand_parsezK, Kind_zSomezIROperand_parsezK };

struct zoptionzIROperand_parsezK {
  enum kind_zoptionzIROperand_parsezK kind;
  union {
    struct { unit zNonezIROperand_parsezK; };
    struct { struct zOperand_parse zSomezIROperand_parsezK; };
  } variants;
};

// struct Ea_binding
struct zEa_binding {
  struct zDecoded_ea zea;
  enum zOperand_id zoperand_name;
};

// struct tuple_(%struct zEa_binding, %i)
struct ztuple_z8z5structz0zzEa_bindingzCz0z5iz9 {
  struct zEa_binding ztup0;
  sail_int ztup1;
};

// union option<(REa_binding,i)>
enum kind_zoptionzIz8REa_bindingzCiz9zK { Kind_zNonezIz8REa_bindingzCiz9zK, Kind_zSomezIz8REa_bindingzCiz9zK };

struct zoptionzIz8REa_bindingzCiz9zK {
  enum kind_zoptionzIz8REa_bindingzCiz9zK kind;
  union {
    struct { unit zNonezIz8REa_bindingzCiz9zK; };
    struct { struct ztuple_z8z5structz0zzEa_bindingzCz0z5iz9 zSomezIz8REa_bindingzCiz9zK; };
  } variants;
};

struct node_zz5listz8z5structz0zzEa_bindingz9 {
  unsigned int rc;
  struct zEa_binding hd;
  struct node_zz5listz8z5structz0zzEa_bindingz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzEa_bindingz9 *zz5listz8z5structz0zzEa_bindingz9;

// struct Ea_parse
struct zEa_parse {
  zz5listz8z5structz0zzEa_bindingz9 zbindings;
  sail_int zcursor;
};

// union option<REa_parse>
enum kind_zoptionzIREa_parsezK { Kind_zNonezIREa_parsezK, Kind_zSomezIREa_parsezK };

struct zoptionzIREa_parsezK {
  enum kind_zoptionzIREa_parsezK kind;
  union {
    struct { unit zNonezIREa_parsezK; };
    struct { struct zEa_parse zSomezIREa_parsezK; };
  } variants;
};

// enum Decode_stage
enum zDecode_stage { zDecodeSuccess, zDecodeFetch, zDecodeFraming, zDecodeOpcode, zDecodeConstraint, zDecodeEaDescriptor, zDecodeEaPayload, zDecodeStandalonePayload, zDecodeRecordLength, zDecodeStaticLegality };

// enum Cpuid_flag
enum zCpuid_flag { zCpuidFlag_FP, zCpuidFlag_FPTRANSA, zCpuidFlag_VECTOR };

struct node_zz5listz8z5enumz0zzCpuid_flagz9 {
  unsigned int rc;
  enum zCpuid_flag hd;
  struct node_zz5listz8z5enumz0zzCpuid_flagz9 *tl;
};
typedef struct node_zz5listz8z5enumz0zzCpuid_flagz9 *zz5listz8z5enumz0zzCpuid_flagz9;

// union option<LECpuid_flag%>
enum kind_zoptionzILECpuid_flagz5zK { Kind_zNonezILECpuid_flagz5zK, Kind_zSomezILECpuid_flagz5zK };

struct zoptionzILECpuid_flagz5zK {
  enum kind_zoptionzILECpuid_flagz5zK kind;
  union {
    struct { unit zNonezILECpuid_flagz5zK; };
    struct { zz5listz8z5enumz0zzCpuid_flagz9 zSomezILECpuid_flagz5zK; };
  } variants;
};

// struct Cpu_state
struct zCpu_state {
  uint64_t zcache_maintenance_granule;
  zz5vecz8z5bv64z9 zcontrols;
  bool zcurrent_dfa;
  uint64_t zfflags;
  uint64_t zflags;
  zz5vecz8z5bv64z9 zfloating_registers;
  uint64_t zfp_component_alignment;
  uint64_t zfp_component_bitmap_bit;
  uint64_t zfp_component_id;
  uint64_t zfp_component_init_policy;
  bool zfp_component_modified;
  sail_int zfp_component_offset;
  bool zfp_component_present;
  sail_int zfp_component_sizze;
  bool zfp_enabled;
  bool zfptrans_enabled;
  uint64_t zfstatus;
  bool zhalted;
  uint64_t zmachine_check_error_code;
  uint64_t zmachine_check_event_aux;
  uint64_t zmachine_check_fault_ea;
  uint64_t zmachine_check_fault_linear;
  uint64_t zmachine_check_payload;
  bool zmachine_check_pending;
  uint64_t znmi_latched_source;
  bool znmi_relatched;
  uint64_t znmi_relatched_source;
  uint64_t zpc;
  zz5vecz8z5listz8z5bvz9z9 zpredicate_registers;
  zz5vecz8z5bv64z9 zregisters;
  struct zRepeat_state zrepeat_state;
  enum zRun_state zrun_state;
  sail_int zsave_area_sizze;
  uint64_t zsave_bitmap_words;
  sail_int zsave_fixed_sizze;
  uint64_t zsave_format;
  zz5vecz8z5bv64z9 zsegments;
  uint64_t zsp;
  uint64_t zstatus;
  bool zsupervisor;
  uint64_t zvector_component_alignment;
  uint64_t zvector_component_bitmap_bit;
  uint64_t zvector_component_id;
  uint64_t zvector_component_init_policy;
  bool zvector_component_modified;
  sail_int zvector_component_offset;
  bool zvector_component_present;
  sail_int zvector_component_sizze;
  bool zvector_enabled;
  sail_int zvector_length_bytes;
  zz5vecz8z5listz8z5bvz9z9 zvector_registers;
};

// union option<RCpu_state>
enum kind_zoptionzIRCpu_statezK { Kind_zNonezIRCpu_statezK, Kind_zSomezIRCpu_statezK };

struct zoptionzIRCpu_statezK {
  enum kind_zoptionzIRCpu_statezK kind;
  union {
    struct { unit zNonezIRCpu_statezK; };
    struct { struct zCpu_state zSomezIRCpu_statezK; };
  } variants;
};

// struct tuple_(%struct zEa_evaluation, %struct zCpu_state)
struct ztuple_z8z5structz0zzEa_evaluationzCz0z5structz0zzCpu_statez9 {
  struct zEa_evaluation ztup0;
  struct zCpu_state ztup1;
};

// union option<(REa_evaluation,RCpu_state)>
enum kind_zoptionzIz8REa_evaluationzCRCpu_statez9zK { Kind_zNonezIz8REa_evaluationzCRCpu_statez9zK, Kind_zSomezIz8REa_evaluationzCRCpu_statez9zK };

struct zoptionzIz8REa_evaluationzCRCpu_statez9zK {
  enum kind_zoptionzIz8REa_evaluationzCRCpu_statez9zK kind;
  union {
    struct { unit zNonezIz8REa_evaluationzCRCpu_statez9zK; };
    struct { struct ztuple_z8z5structz0zzEa_evaluationzCz0z5structz0zzCpu_statez9 zSomezIz8REa_evaluationzCRCpu_statez9zK; };
  } variants;
};

// struct Resolved_execution
struct zResolved_execution {
  uint64_t zdestination_value;
  struct zCpu_state zstate;
};

// union option<RResolved_execution>
enum kind_zoptionzIRResolved_executionzK { Kind_zNonezIRResolved_executionzK, Kind_zSomezIRResolved_executionzK };

struct zoptionzIRResolved_executionzK {
  enum kind_zoptionzIRResolved_executionzK kind;
  union {
    struct { unit zNonezIRResolved_executionzK; };
    struct { struct zResolved_execution zSomezIRResolved_executionzK; };
  } variants;
};

struct node_zz5listz8z5structz0zzEa_evaluationz9 {
  unsigned int rc;
  struct zEa_evaluation hd;
  struct node_zz5listz8z5structz0zzEa_evaluationz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzEa_evaluationz9 *zz5listz8z5structz0zzEa_evaluationz9;

// struct Ea_evaluation_set
struct zEa_evaluation_set {
  zz5listz8z5structz0zzEa_evaluationz9 zevaluations;
  struct zCpu_state zimage;
};

// type abbreviation Control_registers
typedef zz5vecz8z5bv64z9 zControl_registers;

// enum Continuation_phase
enum zContinuation_phase { zContinuationNone, zPhaseSourceAddress, zPhaseSourceRead, zPhaseDestinationAddress, zPhaseDestinationProbe, zPhaseDestinationWrite, zPhaseMemoryWriteFirst, zPhaseMemoryWriteSecond, zPhaseTargetRead, zPhaseTargetExecuteProbe, zPhaseStackRange, zPhaseStackReadFirst, zPhaseStackReadSecond, zPhaseStackWriteFirst, zPhaseIntegerExternal, zPhaseAtomicRmw, zPhaseCacheTranslate, zPhaseCacheMaintenance, zPhaseFenceCompletion, zPhaseTlbOperation, zPhaseTranslationQuery, zPhasePteRead, zPhaseContextSwitch, zPhaseStateSave, zPhaseStateRestoreHeader, zPhaseStateRestoreRange, zPhaseStateRestore, zPhaseRepeatFetch, zPhaseEventFrameHeader, zPhaseEventFrame, zPhaseEventTargetProbe, zPhaseEventStackProbe, zPhaseEventFrameStore, zPhaseEventReturnExecute, zPhaseFpContractQuery, zPhaseFpSourceRead, zPhaseFpDestinationProbe, zPhaseFpDestinationWrite, zPhaseVectorMemoryRead, zPhaseVectorMemoryWrite, zPhaseVectorFpMemoryRead, zPhaseVectorFpMemoryWrite, zPhaseCpuidQuery, zPhasePerformanceCounter, zPhaseControlTransition, zPhaseResetSerializze };

// enum Constraint_kind
enum zConstraint_kind { zAllowRanges, zExcludeImmediate };

// enum Commit_kind
enum zCommit_kind { zCommitNone, zCommitRegisters, zCommitMemory, zCommitControl, zCommitEvent };

// enum Commit_destination_kind
enum zCommit_destination_kind { zDestinationNone, zDestinationRn, zDestinationFn, zDestinationSP };

// struct Commit_destination
struct zCommit_destination {
  uint64_t zindex;
  enum zCommit_destination_kind zkind;
  sail_int zwidth;
};

// union option<RCommit_destination>
enum kind_zoptionzIRCommit_destinationzK { Kind_zNonezIRCommit_destinationzK, Kind_zSomezIRCommit_destinationzK };

struct zoptionzIRCommit_destinationzK {
  enum kind_zoptionzIRCommit_destinationzK kind;
  union {
    struct { unit zNonezIRCommit_destinationzK; };
    struct { struct zCommit_destination zSomezIRCommit_destinationzK; };
  } variants;
};

// struct Catalog_range
struct zCatalog_range {
  sail_int zlower;
  sail_int zupper;
};

// struct Catalog_payload
struct zCatalog_payload {
  enum zOperand_id zoperand_name;
  enum zOperand_type zoperand_type;
  bool zsigned;
  sail_int zwidth;
};

// union option<RCatalog_payload>
enum kind_zoptionzIRCatalog_payloadzK { Kind_zNonezIRCatalog_payloadzK, Kind_zSomezIRCatalog_payloadzK };

struct zoptionzIRCatalog_payloadzK {
  enum kind_zoptionzIRCatalog_payloadzK kind;
  union {
    struct { unit zNonezIRCatalog_payloadzK; };
    struct { struct zCatalog_payload zSomezIRCatalog_payloadzK; };
  } variants;
};

// struct Catalog_operand
struct zCatalog_operand {
  enum zMetadata_access zaccess;
  struct zoptionzIEOperand_domainz5zK zdomain;
  struct zoptionzIEEa_profilez5zK zea_profile;
  struct zoptionzIEEa_rolez5zK zea_role;
  struct zoptionzIEEa_widthz5zK zea_width;
  zz5listz8z5iz9 zfield_positions;
  struct zoptionzIEField_idz5zK zfield_symbol;
  sail_int zfixed_value;
  bool zhas_fixed_value;
  zz5listz8z5iz9 zlegal_values;
  enum zOperand_id zname;
  enum zOperand_type zoperand_type;
};

// struct Catalog_field
struct zCatalog_field {
  enum zMetadata_field_kind zkind;
  enum zOperand_type zoperand_type;
  zz5listz8z5iz9 zpositions;
  enum zField_id zsymbol;
};

struct node_zz5listz8z5structz0zzCatalog_rangez9 {
  unsigned int rc;
  struct zCatalog_range hd;
  struct node_zz5listz8z5structz0zzCatalog_rangez9 *tl;
};
typedef struct node_zz5listz8z5structz0zzCatalog_rangez9 *zz5listz8z5structz0zzCatalog_rangez9;

// struct Catalog_constraint
struct zCatalog_constraint {
  zz5listz8z5iz9 zfield_positions;
  enum zConstraint_kind zkind;
  zz5listz8z5structz0zzCatalog_rangez9 zranges;
  sail_string zreason;
};

// struct Catalog_availability_selector
struct zCatalog_availability_selector {
  enum zField_id zfield_symbol;
  zz5listz8z5iz9 zvalues;
};

struct node_zz5listz8z5enumz0zzOperand_typez9 {
  unsigned int rc;
  enum zOperand_type hd;
  struct node_zz5listz8z5enumz0zzOperand_typez9 *tl;
};
typedef struct node_zz5listz8z5enumz0zzOperand_typez9 *zz5listz8z5enumz0zzOperand_typez9;

// struct Catalog_availability_operand_profile
struct zCatalog_availability_operand_profile {
  sail_int zoperand_ordinal;
  zz5listz8z5enumz0zzOperand_typez9 zoperand_types;
};

struct node_zz5listz8z5structz0zzCatalog_availability_operand_profilez9 {
  unsigned int rc;
  struct zCatalog_availability_operand_profile hd;
  struct node_zz5listz8z5structz0zzCatalog_availability_operand_profilez9 *tl;
};
typedef struct node_zz5listz8z5structz0zzCatalog_availability_operand_profilez9 *zz5listz8z5structz0zzCatalog_availability_operand_profilez9;

struct node_zz5listz8z5structz0zzCatalog_availability_selectorz9 {
  unsigned int rc;
  struct zCatalog_availability_selector hd;
  struct node_zz5listz8z5structz0zzCatalog_availability_selectorz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzCatalog_availability_selectorz9 *zz5listz8z5structz0zzCatalog_availability_selectorz9;

// struct Catalog_availability_rule
struct zCatalog_availability_rule {
  sail_string zcase_id;
  zz5listz8z5structz0zzCatalog_availability_operand_profilez9 zoperand_profiles;
  zz5listz8z5enumz0zzCpuid_flagz9 zrequired_flags;
  zz5listz8z5structz0zzCatalog_availability_selectorz9 zselectors;
};

struct node_zz5listz8z5enumz0zzSizzzze_codez9 {
  unsigned int rc;
  enum zSizze_code hd;
  struct node_zz5listz8z5enumz0zzSizzzze_codez9 *tl;
};
typedef struct node_zz5listz8z5enumz0zzSizzzze_codez9 *zz5listz8z5enumz0zzSizzzze_codez9;

struct node_zz5listz8z5structz0zzCatalog_availability_rulez9 {
  unsigned int rc;
  struct zCatalog_availability_rule hd;
  struct node_zz5listz8z5structz0zzCatalog_availability_rulez9 *tl;
};
typedef struct node_zz5listz8z5structz0zzCatalog_availability_rulez9 *zz5listz8z5structz0zzCatalog_availability_rulez9;

struct node_zz5listz8z5structz0zzCatalog_constraintz9 {
  unsigned int rc;
  struct zCatalog_constraint hd;
  struct node_zz5listz8z5structz0zzCatalog_constraintz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzCatalog_constraintz9 *zz5listz8z5structz0zzCatalog_constraintz9;

struct node_zz5listz8z5structz0zzCatalog_fieldz9 {
  unsigned int rc;
  struct zCatalog_field hd;
  struct node_zz5listz8z5structz0zzCatalog_fieldz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzCatalog_fieldz9 *zz5listz8z5structz0zzCatalog_fieldz9;

struct node_zz5listz8z5structz0zzCatalog_operandz9 {
  unsigned int rc;
  struct zCatalog_operand hd;
  struct node_zz5listz8z5structz0zzCatalog_operandz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzCatalog_operandz9 *zz5listz8z5structz0zzCatalog_operandz9;

struct node_zz5listz8z5structz0zzCatalog_payloadz9 {
  unsigned int rc;
  struct zCatalog_payload hd;
  struct node_zz5listz8z5structz0zzCatalog_payloadz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzCatalog_payloadz9 *zz5listz8z5structz0zzCatalog_payloadz9;

// struct Catalog_entry
struct zCatalog_entry {
  zz5listz8z5structz0zzCatalog_payloadz9 zappended_payloads;
  zz5listz8z5structz0zzCatalog_availability_rulez9 zavailability_rules;
  zz5listz8z5enumz0zzCpuid_flagz9 zcommon_required_cpuid_flags;
  zz5listz8z5structz0zzCatalog_constraintz9 zconstraints;
  enum zEncoding_class zencoding_class;
  zz5listz8z5structz0zzCatalog_fieldz9 zfields;
  enum zForm_id zform_id;
  enum zInstruction_set zinstruction_set;
  uint64_t zmask;
  zz5listz8z5structz0zzCatalog_operandz9 zoperands;
  enum zSemantic_operation zoperation;
  enum zPredicate_mode zpredicate_mode;
  enum zPrivilege_level zprivilege;
  bool zrepeat_rep;
  bool zrepeat_repcc;
  enum zSemantic_route zroute;
  zz5listz8z5enumz0zzSizzzze_codez9 zsizzes;
  uint64_t zvalue;
};

// union option<RCatalog_entry>
enum kind_zoptionzIRCatalog_entryzK { Kind_zNonezIRCatalog_entryzK, Kind_zSomezIRCatalog_entryzK };

struct zoptionzIRCatalog_entryzK {
  enum kind_zoptionzIRCatalog_entryzK kind;
  union {
    struct { unit zNonezIRCatalog_entryzK; };
    struct { struct zCatalog_entry zSomezIRCatalog_entryzK; };
  } variants;
};

// struct Decoded_instruction
struct zDecoded_instruction {
  zz5listz8z5bvz9 zbytes;
  sail_int zencoded_length;
  zz5listz8z5structz0zzDecoded_fieldz9 zfields;
  struct zCatalog_entry zform;
  uint64_t zopcode_allocation;
  zz5listz8z5structz0zzDecoded_operandz9 zoperands;
  sail_int zrequired_length;
};

// union option<RDecoded_instruction>
enum kind_zoptionzIRDecoded_instructionzK { Kind_zNonezIRDecoded_instructionzK, Kind_zSomezIRDecoded_instructionzK };

struct zoptionzIRDecoded_instructionzK {
  enum kind_zoptionzIRDecoded_instructionzK kind;
  union {
    struct { unit zNonezIRDecoded_instructionzK; };
    struct { struct zDecoded_instruction zSomezIRDecoded_instructionzK; };
  } variants;
};

// struct Decode_outcome
struct zDecode_outcome {
  struct zoptionzIRCatalog_entryzK zcandidate_form;
  sail_string zdetail;
  struct zoptionzIRDecoded_instructionzK zinstruction;
  enum zDecode_stage zstage;
};

// enum Boundary_class
enum zBoundary_class { zBoundaryOrdinary, zBoundaryRepeatIteration, zBoundaryEventEntry };

struct node_zz5listz8z5structz0zzMemory_writez9 {
  unsigned int rc;
  struct zMemory_write hd;
  struct node_zz5listz8z5structz0zzMemory_writez9 *tl;
};
typedef struct node_zz5listz8z5structz0zzMemory_writez9 *zz5listz8z5structz0zzMemory_writez9;

// struct Pending_commit
struct zPending_commit {
  struct zoptionzIRCpu_statezK zafter;
  bool zatomic;
  enum zBoundary_class zboundary_class;
  uint64_t zcaptured_first;
  uint64_t zcaptured_second;
  struct zCommit_destination zdestination;
  struct zoptionzIREvent_recordzK zevent;
  sail_int zevent_attempt;
  struct zFp_pending_image zfp_pending;
  struct zoptionzIRDecoded_instructionzK zinstruction;
  enum zCommit_kind zkind;
  zz5listz8z5structz0zzMemory_writez9 zmemory_writes;
  enum zSemantic_operation zoperation;
  sail_int zordinal;
  enum zContinuation_phase zphase;
  struct zoptionzIRDecoded_instructionzK zrepeat_body;
  zz5listz8z5bvz9 zrepeat_bytes;
  bool zrepeat_parent_active;
  zz5listz8z5bvz9 zvector_payload0;
  zz5listz8z5bvz9 zvector_payload1;
};

// enum Architectural_event
enum zArchitectural_event { zEvent_DEBUG_TRACE, zEvent_BREAKPOINT, zEvent_PRIVILEGE_VIOLATION, zEvent_SYSTEM_CALL, zEvent_DIVIDE_BY_ZERO, zEvent_SIGNED_DIVIDE_OVERFLOW, zEvent_INVALID_OPCODE, zEvent_INVALID_ADDRESSING_FORM, zEvent_RESERVED_INSTRUCTION_ENCODING, zEvent_UNAVAILABLE_INSTRUCTION_EXTENSION, zEvent_EXPLICIT_ILLEGAL_INSTRUCTION, zEvent_TRUNCATED_INSTRUCTION, zEvent_INVALID_OPERAND_RELATION, zEvent_PAGE_NOT_PRESENT, zEvent_PAGE_PERMISSION_VIOLATION, zEvent_MALFORMED_PAGE_TABLE_ENTRY, zEvent_NONCANONICAL_ADDRESS, zEvent_SEGMENT_BOUNDS_VIOLATION, zEvent_ATOMIC_ALIGNMENT_FAULT, zEvent_MEMORY_TYPE_FAULT, zEvent_PHYSICAL_ADDRESS_FAULT, zEvent_MMIO_ALIGNMENT_FAULT, zEvent_UNSUPPORTED_MMIO_OPERATION, zEvent_INVALID_CONTROL_SELECTOR, zEvent_RESERVED_CONTROL_BITS, zEvent_INVALID_CONTROL_IMAGE, zEvent_INVALID_CONTROL_TRANSITION, zEvent_BUS_NO_RESPONDER, zEvent_BUS_ACCESS_DENIED, zEvent_BUS_TIMEOUT, zEvent_BUS_DATA_ERROR, zEvent_BUS_OTHER_ERROR, zEvent_EVENT_ENTRY_STATE_FAILURE, zEvent_EVENT_STACK_STATE_FAILURE, zEvent_EVENT_FRAME_ADDRESS_FAILURE, zEvent_EVENT_FRAME_STORE_FAILURE, zEvent_MACHINE_CHECK, zEvent_INTERRUPT, zEvent_NMI, zEvent_FLOATING_POINT_EXCEPTION, zEvent_VECTOR_LOOP_OFFSET_OUT_OF_RANGE, zEvent_VECTOR_LANE_INDEX_OUT_OF_RANGE };

// struct Architectural_effect
struct zArchitectural_effect {
  uint64_t zaddress;
  uint64_t zfflags;
  uint64_t zflags;
  enum zForm_id zform_id;
  uint64_t zfstatus;
  enum zEffect_kind zkind;
  zz5listz8z5structz0zzDecoded_operandz9 zoperands;
  enum zSemantic_operation zoperation;
  sail_int zorder;
  uint64_t zpc;
  uint64_t zstatus;
  bool zsuppress_fault;
  uint64_t zvalue;
  sail_int zwidth;
};

struct node_zz5listz8z5structz0zzArchitectural_effectz9 {
  unsigned int rc;
  struct zArchitectural_effect hd;
  struct node_zz5listz8z5structz0zzArchitectural_effectz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzArchitectural_effectz9 *zz5listz8z5structz0zzArchitectural_effectz9;

// struct Execution_result
struct zExecution_result {
  bool zawaiting_environment;
  zz5listz8z5structz0zzArchitectural_effectz9 zeffects;
  struct zoptionzIRExecution_faultzK zfault;
  struct zPending_commit zpending;
  struct zPrimitive_request zrequest;
  struct zCpu_state zstate;
};

// union option<RExecution_result>
enum kind_zoptionzIRExecution_resultzK { Kind_zNonezIRExecution_resultzK, Kind_zSomezIRExecution_resultzK };

struct zoptionzIRExecution_resultzK {
  enum kind_zoptionzIRExecution_resultzK kind;
  union {
    struct { unit zNonezIRExecution_resultzK; };
    struct { struct zExecution_result zSomezIRExecution_resultzK; };
  } variants;
};

struct node_zz5listz8z5structz0zzCatalog_entryz9 {
  unsigned int rc;
  struct zCatalog_entry hd;
  struct node_zz5listz8z5structz0zzCatalog_entryz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzCatalog_entryz9 *zz5listz8z5structz0zzCatalog_entryz9;

struct node_zz5listz8z5structz0zzEa_formz9 {
  unsigned int rc;
  struct zEa_form hd;
  struct node_zz5listz8z5structz0zzEa_formz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzEa_formz9 *zz5listz8z5structz0zzEa_formz9;

struct node_zz5listz8z5structz0zzRepresentative_recordz9 {
  unsigned int rc;
  struct zRepresentative_record hd;
  struct node_zz5listz8z5structz0zzRepresentative_recordz9 *tl;
};
typedef struct node_zz5listz8z5structz0zzRepresentative_recordz9 *zz5listz8z5structz0zzRepresentative_recordz9;

// struct tuple_(%enum zEncoding_class, %list(%bv))
struct ztuple_z8z5enumz0zzEncoding_classzCz0z5listz8z5bvz9z9 {
  enum zEncoding_class ztup0;
  zz5listz8z5bvz9 ztup1;
};

// struct tuple_(%union zoptionzIEEa_profilez5zK, %union zoptionzIEField_idz5zK)
struct ztuple_z8z5unionz0zzoptionzzIEEa_profilezz5zzKzCz0z5unionz0zzoptionzzIEField_idzz5zzKz9 {
  struct zoptionzIEEa_profilez5zK ztup0;
  struct zoptionzIEField_idz5zK ztup1;
};

// struct tuple_(%union zoptionzIRDecoded_fieldzK, %union zoptionzIRCatalog_payloadzK)
struct ztuple_z8z5unionz0zzoptionzzIRDecoded_fieldzzKzCz0z5unionz0zzoptionzzIRCatalog_payloadzzKz9 {
  struct zoptionzIRDecoded_fieldzK ztup0;
  struct zoptionzIRCatalog_payloadzK ztup1;
};

// struct tuple_(%list(%struct zCatalog_operand), %list(%struct zDecoded_operand))
struct ztuple_z8z5listz8z5structz0zzCatalog_operandz9zCz0z5listz8z5structz0zzDecoded_operandz9z9 {
  zz5listz8z5structz0zzCatalog_operandz9 ztup0;
  zz5listz8z5structz0zzDecoded_operandz9 ztup1;
};

// struct tuple_(%union zoptionzIRFp_semanticszK, %union zoptionzIEFp_pathz5zK, %union zoptionzIEFp_result_policyz5zK)
struct ztuple_z8z5unionz0zzoptionzzIRFp_semanticszzKzCz0z5unionz0zzoptionzzIEFp_pathzz5zzKzCz0z5unionz0zzoptionzzIEFp_result_policyzz5zzKz9 {
  struct zoptionzIRFp_semanticszK ztup0;
  struct zoptionzIEFp_pathz5zK ztup1;
  struct zoptionzIEFp_result_policyz5zK ztup2;
};

// struct tuple_(%union zoptionzIbzK, %union zoptionzIbzK)
struct ztuple_z8z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKz9 {
  struct zoptionzIbzK ztup0;
  struct zoptionzIbzK ztup1;
};

// struct tuple_(%union zoptionzIEFp_nan_originz5zK, %union zoptionzIEFp_nan_originz5zK)
struct ztuple_z8z5unionz0zzoptionzzIEFp_nan_originzz5zzKzCz0z5unionz0zzoptionzzIEFp_nan_originzz5zzKz9 {
  struct zoptionzIEFp_nan_originz5zK ztup0;
  struct zoptionzIEFp_nan_originz5zK ztup1;
};

// struct tuple_(%bv64, %bv4)
struct ztuple_z8z5bv64zCz0z5bv4z9 {
  uint64_t ztup0;
  uint64_t ztup1;
};

// struct tuple_(%union zoptionzIRDecoded_operandzK, %union zoptionzIRDecoded_operandzK)
struct ztuple_z8z5unionz0zzoptionzzIRDecoded_operandzzKzCz0z5unionz0zzoptionzzIRDecoded_operandzzKz9 {
  struct zoptionzIRDecoded_operandzK ztup0;
  struct zoptionzIRDecoded_operandzK ztup1;
};

// struct tuple_(%union zoptionzIbzK, %union zoptionzIRCommit_destinationzK)
struct ztuple_z8z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIRCommit_destinationzzKz9 {
  struct zoptionzIbzK ztup0;
  struct zoptionzIRCommit_destinationzK ztup1;
};

// struct tuple_(%union zoptionzIbzK, %union zoptionzIRDecoded_operandzK)
struct ztuple_z8z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIRDecoded_operandzzKz9 {
  struct zoptionzIbzK ztup0;
  struct zoptionzIRDecoded_operandzK ztup1;
};

// struct tuple_(%union zoptionzIbzK, %union zoptionzIRCommit_destinationzK, %union zoptionzIRCommit_destinationzK)
struct ztuple_z8z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIRCommit_destinationzzKzCz0z5unionz0zzoptionzzIRCommit_destinationzzKz9 {
  struct zoptionzIbzK ztup0;
  struct zoptionzIRCommit_destinationzK ztup1;
  struct zoptionzIRCommit_destinationzK ztup2;
};

// struct tuple_(%union zoptionzIbzK, %union zoptionzIRDecoded_operandzK, %union zoptionzIRDecoded_operandzK)
struct ztuple_z8z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIRDecoded_operandzzKzCz0z5unionz0zzoptionzzIRDecoded_operandzzKz9 {
  struct zoptionzIbzK ztup0;
  struct zoptionzIRDecoded_operandzK ztup1;
  struct zoptionzIRDecoded_operandzK ztup2;
};

// struct tuple_(%union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIRDecoded_operandzK)
struct ztuple_z8z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIRDecoded_operandzzKz9 {
  struct zoptionzIbzK ztup0;
  struct zoptionzIbzK ztup1;
  struct zoptionzIRDecoded_operandzK ztup2;
};

// struct tuple_(%union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIRCommit_destinationzK, %union zoptionzIRCommit_destinationzK)
struct ztuple_z8z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIRCommit_destinationzzKzCz0z5unionz0zzoptionzzIRCommit_destinationzzKz9 {
  struct zoptionzIbzK ztup0;
  struct zoptionzIbzK ztup1;
  struct zoptionzIRCommit_destinationzK ztup2;
  struct zoptionzIRCommit_destinationzK ztup3;
};

// struct tuple_(%union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIbzK)
struct ztuple_z8z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKz9 {
  struct zoptionzIbzK ztup0;
  struct zoptionzIbzK ztup1;
  struct zoptionzIbzK ztup2;
};

// struct tuple_(%union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIizK)
struct ztuple_z8z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIizzKz9 {
  struct zoptionzIbzK ztup0;
  struct zoptionzIbzK ztup1;
  struct zoptionzIbzK ztup2;
  struct zoptionzIizK ztup3;
};

// struct tuple_(%bv64, %bv64)
struct ztuple_z8z5bv64zCz0z5bv64z9 {
  uint64_t ztup0;
  uint64_t ztup1;
};

// struct tuple_(%union zoptionzIEFp_pathz5zK, %union zoptionzIEFp_result_kindz5zK)
struct ztuple_z8z5unionz0zzoptionzzIEFp_pathzz5zzKzCz0z5unionz0zzoptionzzIEFp_result_kindzz5zzKz9 {
  struct zoptionzIEFp_pathz5zK ztup0;
  struct zoptionzIEFp_result_kindz5zK ztup1;
};

// struct tuple_(%list(%bv), %list(%bv))
struct ztuple_z8z5listz8z5bvz9zCz0z5listz8z5bvz9z9 {
  zz5listz8z5bvz9 ztup0;
  zz5listz8z5bvz9 ztup1;
};

// struct tuple_(%list(%bv), %list(%bv), %list(%bv))
struct ztuple_z8z5listz8z5bvz9zCz0z5listz8z5bvz9zCz0z5listz8z5bvz9z9 {
  zz5listz8z5bvz9 ztup0;
  zz5listz8z5bvz9 ztup1;
  zz5listz8z5bvz9 ztup2;
};

// struct tuple_(%union zoptionzILbzK, %union zoptionzILbzK)
struct ztuple_z8z5unionz0zzoptionzzILbzzKzCz0z5unionz0zzoptionzzILbzzKz9 {
  struct zoptionzILbzK ztup0;
  struct zoptionzILbzK ztup1;
};

// struct tuple_(%union zoptionzIVbzK, %union zoptionzIbzK, %union zoptionzIbzK)
struct ztuple_z8z5unionz0zzoptionzzIVbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKz9 {
  struct zoptionzIVbzK ztup0;
  struct zoptionzIbzK ztup1;
  struct zoptionzIbzK ztup2;
};

// struct tuple_(%union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIbzK)
struct ztuple_z8z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKz9 {
  struct zoptionzIbzK ztup0;
  struct zoptionzIbzK ztup1;
  struct zoptionzIbzK ztup2;
  struct zoptionzIbzK ztup3;
  struct zoptionzIbzK ztup4;
  struct zoptionzIbzK ztup5;
};

// struct tuple_(%union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIbzK)
struct ztuple_z8z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKz9 {
  struct zoptionzIbzK ztup0;
  struct zoptionzIbzK ztup1;
  struct zoptionzIbzK ztup2;
  struct zoptionzIbzK ztup3;
  struct zoptionzIbzK ztup4;
  struct zoptionzIbzK ztup5;
  struct zoptionzIbzK ztup6;
  struct zoptionzIbzK ztup7;
};

// struct tuple_(%union zoptionzIRDecoded_operandzK, %union zoptionzIRCommit_destinationzK)
struct ztuple_z8z5unionz0zzoptionzzIRDecoded_operandzzKzCz0z5unionz0zzoptionzzIRCommit_destinationzzKz9 {
  struct zoptionzIRDecoded_operandzK ztup0;
  struct zoptionzIRCommit_destinationzK ztup1;
};

// struct tuple_(%union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIbzK, %union zoptionzIbzK)
struct ztuple_z8z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKzCz0z5unionz0zzoptionzzIbzzKz9 {
  struct zoptionzIbzK ztup0;
  struct zoptionzIbzK ztup1;
  struct zoptionzIbzK ztup2;
  struct zoptionzIbzK ztup3;
};

// struct tuple_(%union zoptionzIRDecoded_operandzK, %union zoptionzIRDecoded_operandzK, %union zoptionzIbzK)
struct ztuple_z8z5unionz0zzoptionzzIRDecoded_operandzzKzCz0z5unionz0zzoptionzzIRDecoded_operandzzKzCz0z5unionz0zzoptionzzIbzzKz9 {
  struct zoptionzIRDecoded_operandzK ztup0;
  struct zoptionzIRDecoded_operandzK ztup1;
  struct zoptionzIbzK ztup2;
};

bool zneq_int(sail_int, sail_int);

bool zneq_bool(bool, bool);

bool zneq_anythingzIVbzK(zz5vecz8z5bvz9, zz5vecz8z5bvz9);

bool zneq_anythingzIVLbzK(zz5vecz8z5listz8z5bvz9z9, zz5vecz8z5listz8z5bvz9z9);

bool zneq_anythingzIOzIbzKzK(struct zoptionzIbzK, struct zoptionzIbzK);

bool zneq_anythingzIOzILbzKzK(struct zoptionzILbzK, struct zoptionzILbzK);

bool zneq_anythingzIOzIRExecution_faultzKzK(struct zoptionzIRExecution_faultzK, struct zoptionzIRExecution_faultzK);

bool zneq_anythingzIOzIEOperand_idz5zKzK(struct zoptionzIEOperand_idz5zK, struct zoptionzIEOperand_idz5zK);

bool zneq_anythingzIESemantic_operationz5zK(enum zSemantic_operation, enum zSemantic_operation);

bool zneq_anythingzIERun_statez5zK(enum zRun_state, enum zRun_state);

bool zneq_anythingzIEOperand_typez5zK(enum zOperand_type, enum zOperand_type);

bool zneq_anythingzIEFp_result_kindz5zK(enum zFp_result_kind, enum zFp_result_kind);

bool zneq_anythingzIEForm_idz5zK(enum zForm_id, enum zForm_id);

enum zSemantic_route zsemantic_route(enum zSemantic_operation);

void create_letbind_0(void);
void kill_letbind_0(void);


void create_letbind_1(void);
void kill_letbind_1(void);


void create_letbind_2(void);
void kill_letbind_2(void);


void create_letbind_3(void);
void kill_letbind_3(void);


void create_letbind_4(void);
void kill_letbind_4(void);


void create_letbind_5(void);
void kill_letbind_5(void);


void zprimary_form_catalog_for(zz5listz8z5structz0zzCatalog_entryz9 *rop, enum zEncoding_class);

void create_letbind_6(void);
void kill_letbind_6(void);


void zeffective_address_catalog(zz5listz8z5structz0zzEa_formz9 *rop, unit);

void create_letbind_7(void);
void kill_letbind_7(void);


void zextracted_field(sail_int *rop, uint64_t, zz5listz8z5iz9, sail_int);

bool zvalue_in_ranges(sail_int, zz5listz8z5structz0zzCatalog_rangez9);

bool zconstraint_matches(uint64_t, struct zCatalog_constraint);

bool zconstraints_match(uint64_t, zz5listz8z5structz0zzCatalog_constraintz9);

bool zcatalog_entry_matches(uint64_t, struct zCatalog_entry);

void zbyte_count(sail_int *rop, zz5listz8z5bvz9);

void zclass_minimum(sail_int *rop, enum zRecord_class);

enum zRecord_class zextended_class(sail_int, sail_int);

void zframe_record(struct zoptionzIRFramed_recordzK *rop, zz5listz8z5bvz9);

bool zrequired_bytes_sufficient(struct zFramed_record, sail_int);

void zbyte_at(struct zoptionzIbzK *rop, zz5listz8z5bvz9, sail_int);

void zread_le_int(struct zoptionzIizK *rop, zz5listz8z5bvz9, sail_int, sail_int, sail_int, sail_int);

void zread_le_bits(struct zoptionzIbzK *rop, zz5listz8z5bvz9, sail_int, sail_int);

void zread_be_int(struct zoptionzIizK *rop, zz5listz8z5bvz9, sail_int, sail_int, sail_int);

void zread_be_bits(struct zoptionzIbzK *rop, zz5listz8z5bvz9, sail_int, sail_int);

void zopcode_allocation(struct zoptionzIbzK *rop, zz5listz8z5bvz9, enum zEncoding_class);

enum zEncoding_class zencoding_class_of_record(enum zRecord_class);

void zfind_catalog_entry(struct zoptionzIRCatalog_entryzK *rop, uint64_t, enum zEncoding_class, zz5listz8z5structz0zzCatalog_entryz9);

void zfind_opcode_entry(struct zoptionzIRCatalog_entryzK *rop, uint64_t, enum zEncoding_class, zz5listz8z5structz0zzCatalog_entryz9);

void zdecode_fields(zz5listz8z5structz0zzDecoded_fieldz9 *rop, uint64_t, zz5listz8z5structz0zzCatalog_fieldz9);

void zfind_decoded_field(struct zoptionzIRDecoded_fieldzK *rop, enum zField_id, zz5listz8z5structz0zzDecoded_fieldz9);

bool zea_patterns_match(zz5listz8z5structz0zzEa_patternz9, zz5listz8z5bvz9, sail_int);

void zea_pattern_count(sail_int *rop, zz5listz8z5structz0zzEa_patternz9);

bool zcompact_ea_matches(struct zEa_form, enum zEa_profile, uint64_t);

void zfind_compact_ea(struct zoptionzIREa_formzK *rop, enum zEa_profile, uint64_t, zz5listz8z5structz0zzEa_formz9);

void zfind_extended_ea(struct zoptionzIREa_formzK *rop, enum zEa_descriptor_family, zz5listz8z5bvz9, sail_int, zz5listz8z5structz0zzEa_formz9);

void zextracted_ea_field(sail_int *rop, uint64_t, zz5listz8z5iz9, sail_int);

void zdecode_ea_field_list(zz5listz8z5structz0zzDecoded_fieldz9 *rop, uint64_t, zz5listz8z5structz0zzEa_fieldz9);

void zappend_decoded_fields(zz5listz8z5structz0zzDecoded_fieldz9 *rop, zz5listz8z5structz0zzDecoded_fieldz9, zz5listz8z5structz0zzDecoded_fieldz9);

void zdecode_ea_fields(zz5listz8z5structz0zzDecoded_fieldz9 *rop, zz5listz8z5bvz9, sail_int, struct zEa_form);

void zparse_one_ea(struct zoptionzIz8REa_bindingzCiz9zK *rop, enum zOperand_id, struct zoptionzIEEa_widthz5zK, enum zEa_profile, sail_int, zz5listz8z5bvz9, sail_int);

void zparse_ea_operands(struct zoptionzIREa_parsezK *rop, zz5listz8z5structz0zzCatalog_operandz9, zz5listz8z5structz0zzDecoded_fieldz9, zz5listz8z5bvz9, sail_int);

enum zDecode_stage zea_failure_stage(zz5listz8z5structz0zzCatalog_operandz9, zz5listz8z5structz0zzDecoded_fieldz9, zz5listz8z5bvz9, sail_int);

void zfind_ea_binding(struct zoptionzIRDecoded_eazK *rop, enum zOperand_id, zz5listz8z5structz0zzEa_bindingz9);

void zfind_payload(struct zoptionzIRCatalog_payloadzK *rop, enum zOperand_id, zz5listz8z5structz0zzCatalog_payloadz9);

void zdecode_operand_list(struct zoptionzIROperand_parsezK *rop, zz5listz8z5structz0zzCatalog_operandz9, zz5listz8z5structz0zzCatalog_payloadz9, zz5listz8z5structz0zzDecoded_fieldz9, zz5listz8z5structz0zzEa_bindingz9, zz5listz8z5bvz9, sail_int);

bool zint_member(sail_int, zz5listz8z5iz9);

bool zlegal_value_or_unrestricted(sail_int, zz5listz8z5iz9);

bool zoperands_statically_legal(zz5listz8z5structz0zzCatalog_operandz9, zz5listz8z5structz0zzDecoded_operandz9);

void zdecode_success(struct zDecode_outcome *rop, struct zCatalog_entry, uint64_t, zz5listz8z5structz0zzDecoded_fieldz9, struct zOperand_parse, struct zFramed_record, zz5listz8z5bvz9);

void zdecode_full_record_execution_outcome(struct zDecode_outcome *rop, zz5listz8z5bvz9);

void zdecode_full_record_outcome(struct zDecode_outcome *rop, zz5listz8z5bvz9);

void zdecode_full_record(struct zoptionzIRDecoded_instructionzK *rop, zz5listz8z5bvz9);

void create_letbind_8(void);
void kill_letbind_8(void);


void create_letbind_9(void);
void kill_letbind_9(void);


void create_letbind_10(void);
void kill_letbind_10(void);


void create_letbind_11(void);
void kill_letbind_11(void);


void create_letbind_12(void);
void kill_letbind_12(void);


void create_letbind_13(void);
void kill_letbind_13(void);


void create_letbind_14(void);
void kill_letbind_14(void);


void create_letbind_15(void);
void kill_letbind_15(void);


void create_letbind_16(void);
void kill_letbind_16(void);


void create_letbind_17(void);
void kill_letbind_17(void);


void zfp_info(struct zFp_semantics *rop, enum zFp_path, sail_int, enum zFp_result_policy, uint64_t, uint64_t, bool, sail_int);

void zfp_semantics(struct zoptionzIRFp_semanticszK *rop, enum zSemantic_operation);

bool zfp_causes_valid(struct zFp_semantics, uint64_t);

bool zfp_operation_causes_valid(enum zSemantic_operation, uint64_t);

uint64_t zfp_enabled_causes(uint64_t, uint64_t);

bool zfp_traps(uint64_t, uint64_t);

void zfp_ea_read_count(sail_int *rop, zz5listz8z5structz0zzCatalog_operandz9);

bool zfp_has_ea_write(zz5listz8z5structz0zzCatalog_operandz9);

bool zfp_has_rn_write(zz5listz8z5structz0zzCatalog_operandz9);

void zfp_form_path(struct zoptionzIEFp_pathz5zK *rop, struct zCatalog_entry);

enum zFp_result_policy zfp_fn_result(sail_int);

enum zFp_result_policy zfp_pair_result(sail_int);

enum zFp_result_policy zfp_memory_result(sail_int);

void zfp_form_result_policy(struct zoptionzIEFp_result_policyz5zK *rop, struct zCatalog_entry, sail_int);

void zfp_form_semantics(struct zoptionzIRFp_semanticszK *rop, struct zCatalog_entry, sail_int);

void zfptrans_contract_operation(struct zoptionzIESemantic_operationz5zK *rop, uint64_t);

bool zfptrans_contract_word_present(uint64_t);

bool zfptrans_bound_valid(uint64_t);

bool zfptrans_contract_word_valid(uint64_t);

void zfptrans_selected_bound(struct zoptionzIbzK *rop, uint64_t, sail_int);

uint64_t zfptrans_cpuid_selector(uint64_t);

void zfptrans_contract_lookup(struct zFptrans_contract_lookup *rop, uint64_t, uint64_t);

struct zFp_operand_image zempty_fp_operand(unit);

struct zFp_operand_slots zempty_fp_operand_slots(unit);

void zempty_fp_pending(struct zFp_pending_image *rop, unit);

uint64_t zfp_fstatus_rounding_mode(uint64_t);

bool zfp_fstatus_ftzz(uint64_t);

bool zfp_fstatus_dazz(uint64_t);

bool zfp_fstatus_dn(uint64_t);

bool zfp_fstatus_valid(uint64_t);

void zfp_classify_raw(struct zoptionzIEFp_classz5zK *rop, uint64_t, sail_int);

void zfp_operand_width(sail_int *rop, struct zFp_operand_image);

void zfp_operand_class(struct zoptionzIEFp_classz5zK *rop, struct zFp_operand_image);

bool zfp_class_is_nan(enum zFp_class);

bool zfp_operand_is_class(struct zFp_operand_image, enum zFp_class);

uint64_t zfp_signed_zzero(uint64_t, sail_int);

struct zFp_operand_image zfp_apply_dazz(struct zFp_operand_image, bool);

uint64_t zfp_default_nan(sail_int);

uint64_t zfp_quiet_nan(uint64_t, sail_int);

struct zFp_operand_image zfp_apply_dn(struct zFp_operand_image, bool);

struct zFp_postprocess_result zfp_apply_ftzz(struct zFp_operand_image, bool, bool, uint64_t);

struct zFp_postprocess_result zfp_postprocess(struct zFp_operand_image, uint64_t, bool, uint64_t);

struct zFp_postprocess_result zfp_postprocess_pre_dn_response(struct zFp_operand_image, struct zFp_request_image, uint64_t);

enum zFp_nan_origin zfp_origin_for_index(sail_int);

struct zFp_operand_image zfp_request_operand(struct zFp_request_image, sail_int);

void zfp_first_source_class(struct zoptionzIEFp_nan_originz5zK *rop, struct zFp_request_image, enum zFp_class, sail_int);

void zfp_source_nan_origin(struct zoptionzIEFp_nan_originz5zK *rop, struct zFp_request_image);

enum zFp_nan_origin zfp_expected_nan_origin(struct zFp_request_image, struct zFp_operand_image);

bool zfp_nan_origin_valid(struct zFp_request_image, struct zFp_operand_image, enum zFp_nan_origin);

void zfp_nan_source(struct zoptionzIRFp_operand_imagezK *rop, struct zFp_request_image);

void zfp_convert_nan_payload(struct zoptionzIbzK *rop, uint64_t, sail_int, sail_int);

void zfp_expected_pre_dn_nan(struct zoptionzIbzK *rop, struct zFp_request_image, sail_int);

bool zfp_request_has_signaling_nan(struct zFp_request_image);

bool zfp_pre_dn_nan_payload_valid(struct zFp_request_image, struct zFp_operand_image);

void zfp_width_mask(struct zoptionzIbzK *rop, sail_int);

void zfp_sign_mask(struct zoptionzIbzK *rop, sail_int);

void zfp_bitwise_fmov(struct zoptionzIbzK *rop, uint64_t, sail_int);

void zfp_bitwise_fabs(struct zoptionzIbzK *rop, uint64_t, sail_int);

void zfp_bitwise_fneg(struct zoptionzIbzK *rop, uint64_t, sail_int);

void zfp_bitwise_fcopysign(struct zoptionzIbzK *rop, uint64_t, uint64_t, sail_int);

struct zFp_exchange_result zfp_bitwise_fxchg(uint64_t, uint64_t);

void zfp_fclass(struct zoptionzIbzK *rop, uint64_t, sail_int);

void zfp_fmovcr(struct zoptionzIbzK *rop, uint64_t);

uint64_t zfp_primitive_value_kind_code(enum zFp_value_kind);

uint64_t zfp_primitive_result_kind_code(enum zFp_result_kind);

uint64_t zfp_primitive_control(uint64_t, bool, bool, bool);

void zfp_primitive_nan_origin(struct zoptionzIEFp_nan_originz5zK *rop, uint64_t);

void zfp_primitive_evaluate(struct zoptionzIRFp_primitive_evaluationzK *rop, enum zSemantic_operation, sail_int, uint64_t, uint64_t, sail_int, uint64_t, uint64_t, uint64_t, uint64_t, uint64_t, uint64_t, bool);

void zfp_primitive_response(struct zoptionzIRFp_response_imagezK *rop, struct zFp_request_image);

bool zfp_operation_is_exact_local(enum zSemantic_operation);

bool zfp_operand_image_valid(struct zFp_operand_image);

void zfp_operand_slot_get(struct zoptionzIRFp_operand_imagezK *rop, struct zFp_operand_slots, sail_int);

void zfp_operand_slot_set(struct zoptionzIRFp_operand_slotszK *rop, struct zFp_operand_slots, sail_int, struct zFp_operand_image);

uint64_t zfp_operand_valid_bitmap(struct zFp_operand_slots);

void zfp_operand_count_bitmap(struct zoptionzIbzK *rop, sail_int);

bool zfp_operand_slots_valid(struct zFp_operand_slots, sail_int);

bool zfp_operand_slot_valid(struct zFp_operand_image, bool);

bool zfp_request_arity_valid(struct zFp_request_image);

void zfp_result_kind_width(sail_int *rop, enum zFp_result_kind);

bool zfp_result_kind_is_pair(enum zFp_result_kind);

bool zfp_result_kind_is_float(enum zFp_result_kind);

void zfp_fn_write_count(sail_int *rop, zz5listz8z5structz0zzCatalog_operandz9);

void zfp_policy_result_kind(struct zoptionzIEFp_result_kindz5zK *rop, enum zFp_result_policy, enum zSemantic_operation);

void zfp_derive_result_kind(struct zoptionzIEFp_result_kindz5zK *rop, struct zCatalog_entry, sail_int);

enum zFp_destination_kind zfp_derive_destination_kind(struct zCatalog_entry);

void zfp_request_width(sail_int *rop, struct zFp_request_image);

bool zfp_operand_needs_format_conversion(struct zFp_operand_image, sail_int);

bool zfp_request_needs_format_conversion(struct zFp_request_image);

bool zfp_request_is_exact_local(struct zFp_request_image);

uint64_t zfp_request_conversion_allowed_causes(struct zFp_request_image);

bool zfp_result_policy_matches(enum zFp_result_kind, enum zFp_result_policy, enum zSemantic_operation);

void zfp_find_form(struct zoptionzIRCatalog_entryzK *rop, zz5listz8z5structz0zzCatalog_entryz9, enum zForm_id);

void zfp_find_primary_form(struct zoptionzIRCatalog_entryzK *rop, enum zForm_id);

bool zfp_request_contract_valid(struct zFp_request_image, struct zFp_semantics);

bool zfp_request_form_valid(struct zFp_request_image);

bool zfp_request_valid(struct zFp_request_image);

struct zFp_operand_image zfp_prepare_request_operand(enum zSemantic_operation, struct zFp_operand_image, sail_int, bool);

void zfp_build_request(struct zoptionzIRFp_request_imagezK *rop, enum zSemantic_operation, struct zCatalog_entry, enum zFp_path, enum zFp_result_kind, sail_int, struct zFp_operand_slots, uint64_t, uint64_t);

bool zfp_result_primary_used(enum zFp_result_kind);

bool zfp_response_unused_valid(struct zFp_response_image);

bool zfp_response_upper_zzero_valid(struct zFp_response_image);

struct zFp_operand_image zfp_result_operand(enum zFp_result_kind, uint64_t);

bool zfp_response_nan_origins_valid(struct zFp_request_image, struct zFp_response_image);

bool zfp_response_signaling_nan_valid(struct zFp_request_image, struct zFp_response_image);

bool zfp_result_requires_accuracy(uint64_t, sail_int);

bool zfp_response_accuracy_valid(struct zFp_request_image, struct zFp_response_image);

bool zfp_response_valid(struct zFp_request_image, struct zFp_response_image);

void zfp_local_pre_dn_values(struct zoptionzIRFp_exchange_resultzK *rop, struct zFp_request_image, uint64_t);

void zfp_local_response(struct zoptionzIRFp_response_imagezK *rop, struct zFp_request_image, uint64_t);

struct zFp_candidate_result zempty_fp_candidate_result(unit);

bool zfp_request_fstatus_matches(struct zFp_request_image, uint64_t);

struct zFp_final_values zfp_postprocess_response_values(struct zFp_request_image, struct zFp_response_image);

struct zFp_candidate_result zfp_finalizze_response(struct zFp_request_image, struct zFp_response_image, uint64_t);

void zexecute_operation_entry(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state);

void zzzero_vector_bytes(zz5listz8z5bvz9 *rop, sail_int);

void zzzero_vector_registers(zz5vecz8z5listz8z5bvz9z9 *rop, sail_int);

void zzzero_predicate_registers(zz5vecz8z5listz8z5bvz9z9 *rop, sail_int);

void zinitial_cpu(struct zCpu_state *rop, unit);

uint64_t znext_pc(struct zCpu_state, struct zDecoded_instruction);

void zstatus_event_depth(sail_int *rop, uint64_t);

bool zstatus_user_origin(uint64_t);

uint64_t zstatus_with_event_state(uint64_t, sail_int, bool);

void zadvance_pc(struct zCpu_state *rop, struct zCpu_state, struct zDecoded_instruction);

void ztyped_effect(struct zArchitectural_effect *rop, enum zEffect_kind, struct zDecoded_instruction, struct zCpu_state, uint64_t, uint64_t, sail_int, sail_int, bool);

void zempty_destination(struct zCommit_destination *rop, unit);

void zempty_primitive_request(struct zPrimitive_request *rop, unit);

void zempty_pending(struct zPending_commit *rop, struct zoptionzIRCpu_statezK, enum zSemantic_operation, enum zCommit_kind);

void zcompleted(struct zExecution_result *rop, struct zCpu_state, struct zCpu_state, enum zCommit_kind, zz5listz8z5structz0zzArchitectural_effectz9);

void zfaulted(struct zExecution_result *rop, struct zCpu_state, enum zSemantic_operation, enum zFault_kind, const_sail_string);

void zpending_after(struct zCpu_state *rop, struct zExecution_result);

void zfaulted_with_error_code(struct zExecution_result *rop, struct zCpu_state, enum zSemantic_operation, enum zFault_kind, const_sail_string, uint64_t);

bool zflag_zz(uint64_t);

bool zflag_n(uint64_t);

bool zflag_c(uint64_t);

bool zflag_v(uint64_t);

bool zcondition_holds(sail_int, uint64_t);

void zcondition_field(struct zoptionzIizK *rop, zz5listz8z5structz0zzDecoded_fieldz9);

bool zpredicate_holds(struct zDecoded_instruction, struct zCpu_state);

void zoperand_at(struct zoptionzIRDecoded_operandzK *rop, sail_int, zz5listz8z5structz0zzDecoded_operandz9);

void zfind_operand_by_name(struct zoptionzIRDecoded_operandzK *rop, enum zOperand_id, zz5listz8z5structz0zzDecoded_operandz9);

bool zavailability_int_contains(zz5listz8z5iz9, sail_int);

bool zavailability_operand_type_contains(zz5listz8z5enumz0zzOperand_typez9, enum zOperand_type);

bool zavailability_selector_matches(struct zCatalog_availability_selector, zz5listz8z5structz0zzDecoded_fieldz9);

bool zavailability_selectors_match(zz5listz8z5structz0zzCatalog_availability_selectorz9, zz5listz8z5structz0zzDecoded_fieldz9);

bool zavailability_operand_profile_matches(struct zCatalog_availability_operand_profile, zz5listz8z5structz0zzDecoded_operandz9);

bool zavailability_operand_profiles_match(zz5listz8z5structz0zzCatalog_availability_operand_profilez9, zz5listz8z5structz0zzDecoded_operandz9);

bool zcpuid_flag_enabled(enum zCpuid_flag, struct zCpu_state);

bool zcpuid_flags_available(zz5listz8z5enumz0zzCpuid_flagz9, struct zCpu_state);

void zmatching_availability_flags(struct zoptionzILECpuid_flagz5zK *rop, zz5listz8z5structz0zzCatalog_availability_rulez9, zz5listz8z5structz0zzDecoded_fieldz9, zz5listz8z5structz0zzDecoded_operandz9);

bool zinstruction_available(struct zDecoded_instruction, struct zCpu_state);

bool zcandidate_form_available(struct zCatalog_entry, struct zCpu_state);

void zfirst_ea_operand(struct zoptionzIRDecoded_operandzK *rop, zz5listz8z5structz0zzDecoded_operandz9);

void zcommit_destination_for(struct zCommit_destination *rop, zz5listz8z5structz0zzDecoded_operandz9, sail_int);

void zsizze_code_bytes(sail_int *rop, enum zSizze_code);

void zsizze_list_count(sail_int *rop, zz5listz8z5enumz0zzSizzzze_codez9);

enum zSizze_code zsizze_at(zz5listz8z5enumz0zzSizzzze_codez9, sail_int);

void zcondition_sizze_field(struct zoptionzIizK *rop, zz5listz8z5structz0zzDecoded_fieldz9);

void zoperation_width(sail_int *rop, struct zDecoded_instruction);

bool zvector_operand_type_present(zz5listz8z5structz0zzDecoded_operandz9, enum zOperand_type);

bool zvector_fp_arithmetic_operation(enum zSemantic_operation);

bool zvector_fp_unary_operation(enum zSemantic_operation);

bool zvector_fp_conversion_operation(enum zSemantic_operation);

bool zvector_instruction_requires_fp(struct zDecoded_instruction);

void zea_field_role(struct zoptionzIizK *rop, enum zEa_role, zz5listz8z5structz0zzDecoded_fieldz9);

void zea_segment_index(sail_int *rop, struct zDecoded_ea);

uint64_t zea_signed_payload(struct zDecoded_ea);

void zstaged_register(zz5listz8z5structz0zzStaged_register_updatez9 *rop, sail_int, uint64_t);

uint64_t zimage_register(struct zCpu_state, sail_int);

uint64_t zimage_segment(struct zCpu_state, sail_int);

void zea_width_shift(sail_int *rop, sail_int);

struct zSegment_point zsegment_point(uint64_t, uint64_t);

void zevaluate_decoded_ea(struct ztuple_z8z5structz0zzEa_evaluationzCz0z5structz0zzCpu_statez9 *rop, struct zDecoded_operand, struct zDecoded_ea, struct zCpu_state, uint64_t, sail_int);

void zevaluate_decoded_vector_ea(struct ztuple_z8z5structz0zzEa_evaluationzCz0z5structz0zzCpu_statez9 *rop, struct zDecoded_operand, struct zDecoded_ea, struct zCpu_state, uint64_t, sail_int);

void zevaluate_vector_instruction_ea(struct zoptionzIz8REa_evaluationzCRCpu_statez9zK *rop, zz5listz8z5structz0zzDecoded_operandz9, struct zCpu_state, uint64_t, sail_int);

void zextension_destination_width(sail_int *rop, enum zSemantic_operation);

void zinstruction_ea_width(sail_int *rop, enum zSemantic_operation, struct zDecoded_operand, sail_int);

void zevaluate_instruction_eas(struct zEa_evaluation_set *rop, zz5listz8z5structz0zzDecoded_operandz9, enum zSemantic_operation, struct zCpu_state, uint64_t, sail_int);

uint64_t zwidth_mask(sail_int);

uint64_t zsign_extend_width(uint64_t, sail_int);

bool zsigned_register_result(enum zSemantic_operation);

uint64_t zcanonical_register_result(enum zSemantic_operation, uint64_t, sail_int);

bool zwidth_sign(uint64_t, sail_int);

uint64_t zflags_value(bool, bool, bool, bool);

uint64_t zshift_result(enum zSemantic_operation, uint64_t, uint64_t, sail_int);

void zroute_environment(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state, enum zEffect_kind, enum zCommit_kind, bool);

void zstart_memory_transaction(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zresume_transaction(struct zExecution_result *rop, struct zExecution_result, struct zTransaction_response);

void zexecute_full(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state);

void zsigned_width(sail_int *rop, uint64_t, sail_int);

void zwidth_modulus(sail_int *rop, sail_int);

void zwidth_bits(sail_int *rop, sail_int);

uint64_t znarrow_bits(uint64_t, sail_int);

uint64_t zbits_from_int(sail_int);

uint64_t zimmediate_value(struct zDecoded_operand);

void zlocal_ea_value(struct zoptionzIbzK *rop, struct zCpu_state, struct zDecoded_ea);

void zlocal_operand_value(struct zoptionzIbzK *rop, struct zCpu_state, struct zDecoded_operand);

void zlocal_destination(struct zoptionzIRCommit_destinationzK *rop, struct zDecoded_operand, sail_int);

void zwrite_local_destination(struct zCpu_state *rop, struct zCpu_state, enum zSemantic_operation, struct zCommit_destination, uint64_t);

void zoperand_named(struct zoptionzIRDecoded_operandzK *rop, struct zDecoded_instruction, enum zOperand_id);

void zvalue_named(struct zoptionzIbzK *rop, struct zDecoded_instruction, struct zCpu_state, enum zOperand_id);

void zdestination_named(struct zoptionzIRCommit_destinationzK *rop, struct zDecoded_instruction, enum zOperand_id, sail_int);

struct ztuple_z8z5bv64zCz0z5bv4z9 zadd_with_flags(uint64_t, uint64_t, sail_int, sail_int);

struct ztuple_z8z5bv64zCz0z5bv4z9 zsub_with_flags(uint64_t, uint64_t, sail_int, sail_int);

void zbit_count_from(sail_int *rop, uint64_t, sail_int, sail_int);

void zcount_from_low(sail_int *rop, uint64_t, sail_int, sail_int, uint64_t);

void zcount_from_high(sail_int *rop, uint64_t, sail_int, uint64_t);

void zreverse_bytes_int(sail_int *rop, sail_int, sail_int, sail_int);

uint64_t zreverse_bytes(uint64_t, sail_int);

void zcarryless_loop(lbits *rop, lbits, uint64_t, sail_int, lbits);

void zcarryless_product(lbits *rop, uint64_t, uint64_t);

uint64_t zcarryless_high(lbits, sail_int);

void zsigned_minimum(sail_int *rop, sail_int);

void zlocal_result(struct zExecution_result *rop, struct zCpu_state, struct zDecoded_instruction, struct zCpu_state, enum zCommit_kind);

void zfirst_binary_operand(struct zoptionzIRDecoded_operandzK *rop, zz5listz8z5structz0zzDecoded_operandz9);

void zsecond_binary_operand(struct zoptionzIRDecoded_operandzK *rop, zz5listz8z5structz0zzDecoded_operandz9);

void zexecute_binary_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_sp_arithmetic_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_unary_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_shift_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_bit_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_count_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_parity_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_revbyte_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

uint64_t zproduct_high(uint64_t, uint64_t, sail_int, bool, bool);

void zexecute_math_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_divide_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_divmod_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zconcatenated_pair(lbits *rop, uint64_t, uint64_t, sail_int);

void zexecute_extract_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_extend_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_xchg_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_set_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_move_sp_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_bounds_comparison_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state, bool, bool, bool);

void zcontrol_target_local(struct zoptionzIbzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_compare_jump_local(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zstart_control_transaction(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_count_jump(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state);

bool zsegment_image_valid(uint64_t);

int64_t zsreg_index(struct zDecoded_operand);

void zcontrol_index(struct zoptionzIbzK *rop, sail_int);

bool zcontrol_segment_requires_valid_image(sail_int);

bool zcontrol_pointer_requires_alignment(sail_int);

bool zpaging_canonical(uint64_t, uint64_t);

bool zevent_stack_pair_valid(uint64_t, uint64_t);

bool zevent_control_bank_valid(struct zCpu_state);

bool zuinfo_event_code_valid(uint64_t);

bool zuser_return_bank_image_valid(struct zCpu_state);

void zstate_with_control_write(struct zCpu_state *rop, struct zCpu_state, sail_int, uint64_t);

void ztarget_probe_request(struct zPrimitive_request *rop, sail_int, uint64_t, uint64_t);

void zread_state_register(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state, uint64_t);

void zwarm_reset_state(struct zCpu_state *rop, struct zCpu_state);

void zevaluation_named(struct zoptionzIREa_evaluationzK *rop, enum zOperand_id, zz5listz8z5structz0zzEa_evaluationz9);

void zmemory_evaluation_for(struct zoptionzIREa_evaluationzK *rop, zz5listz8z5structz0zzDecoded_operandz9, zz5listz8z5structz0zzEa_evaluationz9, bool);

void znext_memory_source(struct zoptionzIREa_evaluationzK *rop, zz5listz8z5structz0zzDecoded_operandz9, zz5listz8z5structz0zzEa_evaluationz9, struct zoptionzIEOperand_idz5zK);

bool zevaluation_option_named(struct zoptionzIREa_evaluationzK, enum zOperand_id);

void zevaluation_option_name(struct zoptionzIEOperand_idz5zK *rop, struct zoptionzIREa_evaluationzK);

enum zRequest_role zrequest_role_for_ea(struct zoptionzIEEa_rolez5zK);

enum zRequest_domain zrequest_domain_for_operand(struct zoptionzIEOperand_domainz5zK);

void zrequest_for_evaluation(struct zPrimitive_request *rop, enum zPrimitive_request_kind, sail_int, struct zEa_evaluation, enum zTransaction_access, uint64_t, bool);

void zwaiting_transaction(struct zExecution_result *rop, struct zCpu_state, struct zCpu_state, struct zDecoded_instruction, enum zCommit_kind, struct zCommit_destination, enum zContinuation_phase, sail_int, uint64_t, uint64_t, struct zPrimitive_request);

uint64_t zsource_value_for_transaction(struct zDecoded_instruction, struct zCpu_state);

uint64_t zatomic_selector(enum zSemantic_operation);

void zstart_atomic_transaction(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zfirst_evaluation(struct zoptionzIREa_evaluationzK *rop, zz5listz8z5structz0zzEa_evaluationz9);

void zappend_bytes(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, zz5listz8z5bvz9);

void zzzero_byte_count(zz5listz8z5bvz9 *rop, sail_int);

void zle64_bytes(zz5listz8z5bvz9 *rop, uint64_t);

void zserializze_register_file(zz5listz8z5bvz9 *rop, zz5vecz8z5bv64z9, sail_int);

void zserializze_fp_file(zz5listz8z5bvz9 *rop, zz5vecz8z5bv64z9, sail_int);

void zserializze_vector_file(zz5listz8z5bvz9 *rop, zz5vecz8z5listz8z5bvz9z9, sail_int);

void zserializze_predicate_file(zz5listz8z5bvz9 *rop, zz5vecz8z5listz8z5bvz9z9, sail_int);

bool zvalid_vector_length_bytes(sail_int);

void zserializze_saved_segments(zz5listz8z5bvz9 *rop, zz5vecz8z5bv64z9, sail_int);

bool zfp_save_layout_valid(struct zCpu_state);

bool zvector_save_layout_valid(struct zCpu_state);

bool zsave_layout_valid(struct zCpu_state);

uint64_t zsave_header(struct zCpu_state);

bool zrestored_event_state_valid(struct zCpu_state, uint64_t, bool);

void zfp_save_payload(zz5listz8z5bvz9 *rop, struct zCpu_state);

void zvector_save_payload(zz5listz8z5bvz9 *rop, struct zCpu_state);

void zsave_image_bytes(zz5listz8z5bvz9 *rop, struct zCpu_state);

void zstart_cache_transaction(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

uint64_t zpaging_pfn_mask(uint64_t);

bool zphysical_address_fits_pabits(uint64_t);

uint64_t zpaging_level_index(uint64_t, sail_int);

uint64_t zpaging_leaf_offset_mask(sail_int);

uint64_t zpaging_leaf_alignment_mask(sail_int);

bool zpte_structurally_valid(uint64_t, sail_int);

void zpte_read_request(struct zPrimitive_request *rop, struct zCpu_state, struct zDecoded_instruction, uint64_t, uint64_t, sail_int, sail_int, sail_int);

void zquery_result(struct zExecution_result *rop, struct zExecution_result, uint64_t, bool);

void zstart_tlb_context_transaction(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state);

void zstart_system_request(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_lea_transaction(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zstack_request(struct zPrimitive_request *rop, enum zPrimitive_request_kind, sail_int, struct zCpu_state, uint64_t, uint64_t, enum zTransaction_access, uint64_t, bool);

void zcompound_stack_store(struct zPrimitive_request *rop, sail_int, struct zCpu_state, uint64_t, uint64_t, uint64_t);

void zpair_first_index(sail_int *rop, sail_int);

struct ztuple_z8z5bv64zCz0z5bv64z9 zpush_source_values(struct zDecoded_instruction, struct zCpu_state);

void zstart_stack_transaction(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

uint64_t zevent_frame_control(struct zCpu_state, sail_int, sail_int);

void zevent_frame_type_code(sail_int *rop, enum zEvent_frame_type);

void zevent_frame_slots(sail_int *rop, enum zEvent_frame_type);

void zmake_event(struct zEvent_record *rop, enum zEvent_kind, enum zEvent_frame_type, uint64_t, sail_int, uint64_t);

void zencode_event_frame(zz5listz8z5bvz9 *rop, struct zCpu_state, struct zEvent_record, uint64_t);

bool zevent_uses_user_bank(struct zCpu_state);

void zevent_payload_slots(sail_int *rop, enum zEvent_frame_type);

void zevent_storage_slots(sail_int *rop, struct zEvent_record, struct zCpu_state);

uint64_t zevent_stack_segment(struct zEvent_record, struct zCpu_state);

uint64_t zevent_stack_top(struct zEvent_record, struct zCpu_state);

bool zevent_entry_state_valid(struct zCpu_state);

bool zevent_stack_state_valid(struct zEvent_record, struct zCpu_state);

bool zevent_frame_address_valid(struct zEvent_record, struct zCpu_state);

void zevent_target_request(struct zPrimitive_request *rop, struct zCpu_state);

void zevent_stack_range_request(struct zPrimitive_request *rop, struct zEvent_record, struct zCpu_state, sail_int);

void zevent_frame_store_request(struct zPrimitive_request *rop, struct zEvent_record, struct zCpu_state, sail_int);

void zcommitted_event_entry(struct zCpu_state *rop, struct zCpu_state, struct zEvent_record, uint64_t, uint64_t);

void zwaiting_event_transaction(struct zExecution_result *rop, struct zCpu_state, struct zEvent_record, sail_int, enum zContinuation_phase, sail_int, struct zPrimitive_request);

void zstart_event_attempt(struct zExecution_result *rop, struct zEvent_record, struct zCpu_state, sail_int);

void zdouble_fault_event(struct zEvent_record *rop, struct zEvent_record, sail_int);

void zevent_shutdown(struct zExecution_result *rop, struct zCpu_state);

void zstart_admitted_event(struct zExecution_result *rop, struct zEvent_record, struct zCpu_state);

void zevent_delivery_failed(struct zExecution_result *rop, struct zExecution_result, sail_int);

void zstart_user_return(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state);

void zstart_event_control(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state);

bool zvalid_frame_control(uint64_t, struct zCpu_state);

void zbyte_list_length(sail_int *rop, zz5listz8z5bvz9);

bool zrepeat_body_available(struct zDecoded_instruction, struct zCpu_state);

bool zrepeat_body_control_forbidden(struct zDecoded_instruction);

void zrepeat_fetch_request(struct zPrimitive_request *rop, struct zDecoded_instruction, struct zCpu_state, uint64_t);

void zstart_repeat_transaction(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state);

void zrun_repeat_single(struct zExecution_result *rop, struct zDecoded_instruction, zz5listz8z5bvz9, struct zCpu_state);

void zfinish_repeat_single(struct zExecution_result *rop, struct zDecoded_instruction, zz5listz8z5bvz9, struct zCpu_state, struct zCpu_state, uint64_t);

void zattach_repeat_parent(struct zExecution_result *rop, struct zExecution_result, struct zDecoded_instruction, zz5listz8z5bvz9);

bool zrepeat_observation_computed(enum zSemantic_operation);

bool zrepeat_observation_uses_source(enum zSemantic_operation);

void zrepeat_observation_operand(struct zoptionzIRDecoded_operandzK *rop, bool, zz5listz8z5structz0zzDecoded_operandz9);

uint64_t zrepeat_observation_with_capture(struct zDecoded_instruction, struct zCpu_state, struct zCpu_state, uint64_t);

bool zfp_source_candidate(struct zDecoded_operand);

void zfp_source_at(struct zoptionzIRDecoded_operandzK *rop, zz5listz8z5structz0zzDecoded_operandz9, sail_int, sail_int);

bool zfp_destination_is_fn(struct zDecoded_instruction);

enum zFp_value_kind zfp_operand_kind_for(struct zDecoded_instruction, struct zDecoded_operand, sail_int);

struct zFp_operand_image zfp_decoded_operand_image(struct zDecoded_instruction, struct zCpu_state, struct zDecoded_operand, sail_int);

struct zFp_operand_slots zfp_pending_raw_slots(struct zFp_pending_image);

void zfp_pending_with_slots(struct zFp_pending_image *rop, struct zFp_pending_image, struct zFp_operand_slots);

struct zFp_operand_slots zfp_initial_slots(struct zDecoded_instruction, struct zCpu_state, sail_int, sail_int, struct zFp_operand_slots);

void zfp_first_missing_source(sail_int *rop, struct zFp_operand_slots, sail_int, sail_int);

void zfp_writable_fn_at(struct zoptionzIRDecoded_operandzK *rop, zz5listz8z5structz0zzDecoded_operandz9, sail_int, sail_int);

void zfp_waiting(struct zExecution_result *rop, struct zCpu_state, struct zCpu_state, struct zDecoded_instruction, enum zContinuation_phase, sail_int, struct zPrimitive_request, struct zFp_pending_image);

void zfp_preserve_repeat_parent(struct zExecution_result *rop, struct zExecution_result, struct zExecution_result);

void zfp_fault_with_causes(struct zExecution_result *rop, struct zCpu_state, enum zSemantic_operation, uint64_t);

void zfp_start_compute(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state, struct zCpu_state, struct zFp_pending_image, uint64_t, sail_int);

void zfp_commit_candidate(struct zExecution_result *rop, struct zCpu_state, struct zCpu_state, struct zDecoded_instruction, struct zFp_candidate_result, struct zFp_pending_image, sail_int);

void zfp_continue_after_sources(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state, struct zCpu_state, struct zFp_pending_image, uint64_t, sail_int);

void zfp_start_operands(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state, uint64_t);

void zstart_fp_transaction(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state);

void zresume_fp_phase(struct zExecution_result *rop, struct zExecution_result, struct zTransaction_response);

uint64_t zvector_byte_at(zz5listz8z5bvz9, sail_int);

void zvector_replace_byte(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, sail_int, uint64_t);

void zvector_power_of_two(sail_int *rop, sail_int);

bool zpredicate_bit(zz5listz8z5bvz9, sail_int);

void zpredicate_set_bit(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, sail_int, bool);

void zpredicate_fill_typed(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, sail_int, sail_int, sail_int, sail_int, sail_int);

void zpredicate_raw_binary(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, zz5listz8z5bvz9, enum zSemantic_operation);

void zpredicate_raw_not(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9);

void zpredicate_raw_select(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9);

void zvector_lane_unsigned_loop(sail_int *rop, zz5listz8z5bvz9, sail_int, sail_int, sail_int, sail_int);

void zvector_lane_unsigned(sail_int *rop, zz5listz8z5bvz9, sail_int, sail_int);

void zvector_write_lane_loop(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, sail_int, sail_int, sail_int, sail_int, sail_int);

void zvector_write_lane(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, sail_int, sail_int, sail_int);

void zvector_merge_image(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int);

void zvector_duplicate_image(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, sail_int, sail_int, sail_int, sail_int);

void zvector_index_image(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, sail_int, sail_int, sail_int);

void zvector_normalizzed(sail_int *rop, sail_int, sail_int);

void zvector_signed_lane(sail_int *rop, sail_int, sail_int);

void zvector_integer_binary_value(sail_int *rop, enum zSemantic_operation, sail_int, sail_int, sail_int);

void zvector_integer_binary_image(zz5listz8z5bvz9 *rop, enum zSemantic_operation, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int);

bool zvector_integer_reduction_operation(enum zSemantic_operation);

void zvector_integer_reduction_identity(sail_int *rop, enum zSemantic_operation, sail_int);

void zvector_integer_reduction_value(sail_int *rop, enum zSemantic_operation, sail_int, sail_int, sail_int);

void zvector_integer_reduction_image(sail_int *rop, enum zSemantic_operation, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int, sail_int);

void zvector_integer_unary_value(sail_int *rop, enum zSemantic_operation, sail_int, sail_int);

void zvector_integer_unary_image(zz5listz8z5bvz9 *rop, enum zSemantic_operation, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int);

void zvector_integer_unary_source_image(zz5listz8z5bvz9 *rop, enum zSemantic_operation, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int);

enum zSemantic_operation zvector_shift_operation(enum zSemantic_operation);

void zvector_shift_image(zz5listz8z5bvz9 *rop, enum zSemantic_operation, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, bool, zz5listz8z5bvz9, sail_int, sail_int, sail_int);

bool zvector_integer_condition(sail_int, sail_int, sail_int, sail_int);

void zvector_integer_compare_image(zz5listz8z5bvz9 *rop, enum zSemantic_operation, sail_int, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int);

void zvector_width_change_destination_bytes(sail_int *rop, enum zSemantic_operation);

void zvector_write_at_base(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, sail_int, sail_int, sail_int, sail_int, sail_int);

void zvector_width_change_image(zz5listz8z5bvz9 *rop, enum zSemantic_operation, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int, sail_int);

void zvector_permute_value(sail_int *rop, enum zSemantic_operation, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int, sail_int);

void zvector_permute_image(zz5listz8z5bvz9 *rop, enum zSemantic_operation, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int, sail_int);

bool zpredicate_pair_lane(enum zSemantic_operation, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int);

void zpredicate_pair_image(zz5listz8z5bvz9 *rop, enum zSemantic_operation, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int);

void zpredicate_unpack_image(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int, bool);

void zpredicate_pack_image(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int, bool);

void zpredicate_permute_image(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int);

void zpredicate_slide_image(zz5listz8z5bvz9 *rop, enum zSemantic_operation, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int, sail_int);

void zpredicate_count(sail_int *rop, zz5listz8z5bvz9, sail_int, sail_int, sail_int, sail_int);

void zpredicate_first(sail_int *rop, zz5listz8z5bvz9, sail_int, sail_int, sail_int);

void zpredicate_last(sail_int *rop, zz5listz8z5bvz9, sail_int, sail_int);

bool zpredicate_any(zz5listz8z5bvz9);

bool zpredicate_all_typed(zz5listz8z5bvz9, sail_int, sail_int, sail_int);

void zpredicate_register_index(struct zoptionzIbzK *rop, struct zDecoded_instruction, enum zOperand_id);

void zvector_register_index(struct zoptionzIbzK *rop, struct zDecoded_instruction, enum zOperand_id);

void zvector_finish(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state, struct zCpu_state);

bool zvector_operand_writes(enum zOperand_id, zz5listz8z5structz0zzDecoded_operandz9);

void zvector_memory_predicate(zz5listz8z5bvz9 *rop, struct zDecoded_instruction, struct zCpu_state);

bool zvector_fp_basic_operation(enum zSemantic_operation);

bool zvector_fp_convert_operation(enum zSemantic_operation);

bool zvector_reduce_operation(enum zSemantic_operation);

bool zvector_fp_compute_operation(enum zSemantic_operation);

void zvector_writable_operand(struct zoptionzIRDecoded_operandzK *rop, zz5listz8z5structz0zzDecoded_operandz9);

uint64_t zvector_fp_allowed_causes(enum zSemantic_operation);

bool zvector_fp_reduction_operation(enum zSemantic_operation);

enum zSemantic_operation zvector_fp_reduction_scalar_operation(enum zSemantic_operation);

uint64_t zvector_fp_value_kind(sail_int);

uint64_t zvector_fp_result_kind(sail_int);

uint64_t zvector_fp_reduction_identity(enum zSemantic_operation, sail_int);

void zvector_fp_reduce_lanes(struct zoptionzIRVector_fp_reductionzK *rop, enum zSemantic_operation, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int, uint64_t, uint64_t, uint64_t);

void zvector_fp_reduction_commit(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state, struct zCpu_state, zz5listz8z5bvz9);

enum zSemantic_operation zvector_fp_scalar_operation(enum zSemantic_operation);

bool zvector_fp_primitive_operation(enum zSemantic_operation);

bool zvector_fp_exact_operation(enum zSemantic_operation);

void zvector_fp_lane_exact(struct zoptionzIbzK *rop, enum zSemantic_operation, sail_int, uint64_t, uint64_t, bool);

void zvector_fp_arithmetic_lanes(struct zoptionzIRVector_fp_imagezK *rop, enum zSemantic_operation, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int, uint64_t, zz5listz8z5bvz9, uint64_t, bool);

bool zvector_fp_condition_selected(uint64_t, sail_int);

void zvector_fp_compare_lanes(struct zoptionzIRVector_fp_imagezK *rop, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int, uint64_t, sail_int, zz5listz8z5bvz9, uint64_t);

void zvector_fp_conversion_destination_bytes(sail_int *rop, enum zSemantic_operation);

bool zvector_fp_conversion_destination_fp(enum zSemantic_operation);

uint64_t zvector_fp_conversion_source_kind(struct zDecoded_instruction, sail_int);

void zvector_fp_conversion_lanes(struct zoptionzIRVector_fp_imagezK *rop, struct zDecoded_instruction, zz5listz8z5bvz9, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, sail_int, sail_int, sail_int, uint64_t, zz5listz8z5bvz9, uint64_t);

void zvector_fp_named_image(struct zoptionzILbzK *rop, struct zDecoded_instruction, struct zCpu_state, zz5listz8z5bvz9, enum zOperand_id);

void zvector_fp_commit_image(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state, struct zVector_fp_image);

void zvector_fp_evaluate_image(struct zoptionzIRVector_fp_imagezK *rop, struct zDecoded_instruction, struct zCpu_state, zz5listz8z5bvz9);

void zexecute_vector_fp_register(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zvector_fp_waiting(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state, struct zCpu_state, enum zContinuation_phase, struct zPrimitive_request, zz5listz8z5bvz9);

void zvector_memory_operand(struct zoptionzIRDecoded_operandzK *rop, zz5listz8z5structz0zzDecoded_operandz9);

void zvector_memory_request(struct zPrimitive_request *rop, enum zPrimitive_request_kind, struct zDecoded_instruction, struct zCpu_state, struct zEa_evaluation, zz5listz8z5bvz9, zz5listz8z5bvz9, sail_int, enum zTransaction_access);

void zvector_memory_waiting(struct zExecution_result *rop, struct zDecoded_instruction, struct zCpu_state, struct zCpu_state, enum zContinuation_phase, struct zPrimitive_request);

void zstart_vector_fp_transaction(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zvector_fp_commit_memory_image(struct zExecution_result *rop, struct zExecution_result, struct zDecoded_instruction, struct zVector_fp_image, zz5listz8z5bvz9);

bool zvector_integer_binary_operation(enum zSemantic_operation);

bool zvector_integer_unary_operation(enum zSemantic_operation);

bool zvector_shift_operation_p(enum zSemantic_operation);

bool zvector_integer_compare_operation(enum zSemantic_operation);

void zvector_memory_direct_store_image(struct zoptionzILbzK *rop, struct zDecoded_instruction, struct zCpu_state, zz5listz8z5bvz9, sail_int, sail_int);

bool zvector_step_operation(enum zSemantic_operation);

void zvector_lane_bytes_loop(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, sail_int, sail_int);

void zvector_lane_bytes(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, sail_int, sail_int);

void zvector_step_register_index(struct zoptionzIbzK *rop, struct zDecoded_instruction, enum zOperand_id);

bool zvector_step_overlap_conflict(struct zDecoded_instruction);

void zvector_step_payload(sail_int *rop, struct zDecoded_instruction, enum zOperand_id, bool);

void zvector_step_address(struct zoptionzIbzK *rop, struct zDecoded_instruction, struct zCpu_state, sail_int, sail_int);

void zvector_step_request(struct zPrimitive_request *rop, struct zDecoded_instruction, struct zCpu_state, uint64_t, sail_int, zz5listz8z5bvz9);

void zstart_vector_step_transaction(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zstart_vector_memory_transaction(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zvector_response_length(sail_int *rop, struct zDecoded_instruction, struct zCpu_state);

void zvector_memory_source_result(struct zoptionzIRCpu_statezK *rop, struct zDecoded_instruction, struct zCpu_state, struct zCpu_state, zz5listz8z5bvz9);

void zvector_memory_destination_result(struct zoptionzILbzK *rop, struct zDecoded_instruction, struct zCpu_state, zz5listz8z5bvz9);

void zresume_vector_phase(struct zExecution_result *rop, struct zExecution_result, struct zTransaction_response);

void zarchitectural_state_fault(struct zoptionzIRExecution_faultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zcontinue_with_request(struct zExecution_result *rop, struct zExecution_result, enum zContinuation_phase, sail_int, uint64_t, uint64_t, struct zPrimitive_request);

bool zregister_operand_uses(sail_int, struct zDecoded_operand, struct zoptionzIEOperand_idz5zK);

bool zregister_is_used(sail_int, zz5listz8z5structz0zzDecoded_operandz9, struct zoptionzIEOperand_idz5zK);

void zavailable_scratch(sail_int *rop, zz5listz8z5structz0zzDecoded_operandz9, struct zoptionzIEOperand_idz5zK, sail_int);

bool zoption_operand_writes(struct zoptionzIRDecoded_operandzK);

enum zMetadata_access zoperand_access_named(enum zOperand_id, zz5listz8z5structz0zzDecoded_operandz9);

void zresolved_operand(struct zDecoded_operand *rop, struct zDecoded_operand, struct zoptionzIEOperand_idz5zK, uint64_t, struct zoptionzIEOperand_idz5zK, uint64_t, sail_int);

void zresolved_operand_list(zz5listz8z5structz0zzDecoded_operandz9 *rop, zz5listz8z5structz0zzDecoded_operandz9, struct zoptionzIEOperand_idz5zK, uint64_t, struct zoptionzIEOperand_idz5zK, uint64_t, sail_int);

void zexecute_resolved_operands(struct zoptionzIRResolved_executionzK *rop, struct zDecoded_instruction, struct zCpu_state, struct zoptionzIEOperand_idz5zK, uint64_t, struct zoptionzIEOperand_idz5zK, uint64_t);

void zcommit_response_destination(struct zExecution_result *rop, struct zExecution_result, uint64_t, struct zTransaction_response);

void zrestore_register_file(struct zoptionzIVbzK *rop, zz5listz8z5bvz9, sail_int, zz5vecz8z5bv64z9);

void zrestore_fp_file(struct zoptionzIVbzK *rop, zz5listz8z5bvz9, sail_int, sail_int, zz5vecz8z5bv64z9);

void zdrop_restore_bytes(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, sail_int);

void ztake_restore_bytes(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, sail_int);

void zrestore_byte_slice(zz5listz8z5bvz9 *rop, zz5listz8z5bvz9, sail_int, sail_int);

void zrestore_vector_file(zz5vecz8z5listz8z5bvz9z9 *rop, zz5listz8z5bvz9, sail_int, sail_int, sail_int, zz5vecz8z5listz8z5bvz9z9);

void zrestore_predicate_file(zz5vecz8z5listz8z5bvz9z9 *rop, zz5listz8z5bvz9, sail_int, sail_int, sail_int, zz5vecz8z5listz8z5bvz9z9);

void zrestore_vector_component_and_complete(struct zExecution_result *rop, struct zCpu_state, struct zCpu_state, zz5listz8z5bvz9, uint64_t);

void zrestore_raw_image(struct zExecution_result *rop, struct zExecution_result, zz5listz8z5bvz9, uint64_t, uint64_t);

void zcontinue_event_return(struct zExecution_result *rop, struct zExecution_result, zz5listz8z5bvz9);

bool zresponse_matches_phase(enum zContinuation_phase, struct zPrimitive_request, enum zTransaction_response_kind);

void ztransaction_faulted(struct zExecution_result *rop, struct zExecution_result, enum zFault_kind, const_sail_string);

uint64_t zaddress_context_error_code(struct zPrimitive_request, sail_int);

void zarchitectural_memory_fault(struct zExecution_result *rop, struct zExecution_result, enum zFault_kind, sail_int, const_sail_string);

bool zmmio_scalar_request(struct zExecution_result);

bool zmmio_naturally_aligned(struct zPrimitive_request);

void zresume_memory_phase(struct zExecution_result *rop, struct zExecution_result, struct zTransaction_response);

void zresume_control_phase(struct zExecution_result *rop, struct zExecution_result, struct zTransaction_response);

void zresume_system_phase(struct zExecution_result *rop, struct zExecution_result, struct zTransaction_response);

void zresume_repeat_phase(struct zExecution_result *rop, struct zExecution_result, struct zTransaction_response);

void zresume_events_phase(struct zExecution_result *rop, struct zExecution_result, struct zTransaction_response);

void zresume_transaction_inner(struct zExecution_result *rop, struct zExecution_result, struct zTransaction_response);

void zexecute_ABS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_ABS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_ADC_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_ADC(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_ADD_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_ADD(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_AFENCE_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_AFENCE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_AND_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_AND(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BCHG_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BCHG(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BCLR_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BCLR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BKPT_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BKPT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDSII_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDSII(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDSIX_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDSIX(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDSXI_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDSXI(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDSXX_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDSXX(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDUII_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDUII(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDUIX_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDUIX(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDUXI_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDUXI(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDUXX_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BNDUXX(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BSET_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BSET(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BTEST_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BTEST(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CALL_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CALL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CALLcc_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CALLcc(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CLMUL_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CLMUL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CLMULH_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CLMULH(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CLR_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CLR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CLS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CLS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CLZ_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CLZ(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CMP_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CMP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CMPJcc_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CMPJcc(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CMPXCHG_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CMPXCHG(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CPUID_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CPUID(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CTS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CTS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CTZ_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_CTZ(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_DEC_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_DEC(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_DECF_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_DECF(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_DIVMODS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_DIVMODS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_DIVMODU_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_DIVMODU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_DIVS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_DIVS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_DIVU_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_DIVU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_DJcc_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_DJcc(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_ERET_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_ERET(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_EXTRACT_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_EXTRACT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_EXTSL_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_EXTSL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_EXTSQ_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_EXTSQ(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_EXTSW_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_EXTSW(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_EXTZL_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_EXTZL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_EXTZQ_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_EXTZQ(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_EXTZW_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_EXTZW(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FETCHADD_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FETCHADD(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FETCHAND_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FETCHAND(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FETCHOR_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FETCHOR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FETCHSUB_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FETCHSUB(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FETCHXOR_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FETCHXOR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FLSHDCACHE_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FLSHDCACHE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_HALT_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_HALT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_IJcc_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_IJcc(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_ILLEGAL_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_ILLEGAL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_INC_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_INC(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_INCF_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_INCF(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_INVASID_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_INVASID(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_INVDCACHE_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_INVDCACHE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_INVICACHE_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_INVICACHE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_INVPAGE_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_INVPAGE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_INVTLB_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_INVTLB(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_Jcc_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_Jcc(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_JMP_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_JMP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_LCALL_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_LCALL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_LEA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_LEA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_LJMP_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_LJMP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_LRET_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_LRET(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MAXS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MAXS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MAXU_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MAXU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MINS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MINS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MINU_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MINU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MODS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MODS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MODU_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MODU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MOV_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MOV(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MOVcc_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MOVcc(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MOVCU_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MOVCU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MOVNT_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MOVNT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MOVUC_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MOVUC(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MOVUU_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MOVUU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MUL_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MUL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MULHS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MULHS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MULHSU_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MULHSU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MULHU_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_MULHU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_NEG_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_NEG(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_NOP_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_NOP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_NOT_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_NOT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_OR_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_OR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PARITY_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PARITY(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_POP_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_POP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_POPCNT_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_POPCNT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_POPP_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_POPP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PREFETCH_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PREFETCH(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PREFETCHNT_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PREFETCHNT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PTQUERY_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PTQUERY(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PUSH_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PUSH(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PUSHP_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PUSHP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RDCR_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RDCR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RDFLAGS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RDFLAGS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RDPMC_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RDPMC(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RDSEG_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RDSEG(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RDSTATUS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RDSTATUS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_REPcc_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_REPcc(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RESET_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RESET(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RESTORE_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RESTORE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RET_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RET(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_REVBYTE_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_REVBYTE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RFENCE_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RFENCE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_ROL_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_ROL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_ROR_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_ROR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SAR_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SAR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SAVE_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SAVE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SBB_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SBB(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SEGLEA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SEGLEA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SET_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SET(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SETcc_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SETcc(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SETF_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SETF(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SHL_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SHL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SHR_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SHR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SUB_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SUB(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SWPT_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SWPT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SWPTA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SWPTA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SYNCCACHE_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SYNCCACHE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SYSCALL_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_SYSCALL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_TEST_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_TEST(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_TESTJcc_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_TESTJcc(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_TRACE_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_TRACE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VTOP_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VTOP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WAIT_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WAIT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WFENCE_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WFENCE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WRBKDCACHE_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WRBKDCACHE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WRCR_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WRCR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WRFLAGS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WRFLAGS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WRSEG_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WRSEG(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WRSTATUS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WRSTATUS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_XCHG_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_XCHG(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_XOR_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_XOR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_YIELD_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_YIELD(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FABS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FABS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FADD_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FADD(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FBNDII_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FBNDII(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FBNDIX_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FBNDIX(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FBNDXI_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FBNDXI(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FBNDXX_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FBNDXX(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCEIL_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCEIL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCLASS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCLASS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCLR_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCLR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCMP_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCMP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCOPYSIGN_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCOPYSIGN(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCVT_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCVT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCVTU_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCVTU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FDIV_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FDIV(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FFLOOR_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FFLOOR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FGETEXP_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FGETEXP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FGETMAN_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FGETMAN(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FINT_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FINT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FINTRZ_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FINTRZ(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMADD_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMADD(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMAX_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMAX(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMIN_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMIN(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMOD_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMOD(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMOV_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMOV(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMOVcc_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMOVcc(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMOVCR_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMOVCR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMSUB_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMSUB(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMUL_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FMUL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FNEG_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FNEG(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FNMADD_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FNMADD(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FNMSUB_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FNMSUB(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FPOPP_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FPOPP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FPUSHP_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FPUSHP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FREM_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FREM(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FROUND_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FROUND(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FSCALE_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FSCALE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FSQRT_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FSQRT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FSUB_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FSUB(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FTEST_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FTEST(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FTRUNC_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FTRUNC(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FXCHG_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FXCHG(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RDFFLAGS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RDFFLAGS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RDFSTATUS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_RDFSTATUS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WRFFLAGS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WRFFLAGS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WRFSTATUS_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_WRFSTATUS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FACOSA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FACOSA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FASINA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FASINA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FATANA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FATANA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FATANHA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FATANHA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCOSA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCOSA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCOSHA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FCOSHA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FETOXA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FETOXA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FETOXM1A_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FETOXM1A(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FLOG10A_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FLOG10A(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FLOG2A_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FLOG2A(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FLOGNA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FLOGNA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FLOGNP1A_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FLOGNP1A(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FSINA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FSINA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FSINCOSA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FSINCOSA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FSINHA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FSINHA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FTANA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FTANA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FTANHA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FTANHA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FTENTOXA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FTENTOXA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FTWOTOXA_local_entry(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_FTWOTOXA(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VDUP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMOV(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PHEAD(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PTAIL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PFIRST(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PLAST(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PCOUNT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PAND(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_POR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PXOR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PUNPKLO(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PUNPKHI(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PPACKLO(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PPACKHI(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCLR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VINDEX(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VLCNT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VLCADD(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VGATHER1(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VSCATTER1(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PTRUE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PFALSE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PNOT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BPANY(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BPNONE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_BPALL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VNEG_integer(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VNEG_floating(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VABS_integer(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VABS_floating(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VNOT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCLZ(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCTZ(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCLS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCTS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VPOPCNT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VREVBYTE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VSQRT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VROUND(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VTRUNC(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VFLOOR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCEIL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCLASS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PPERM(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PSLIDEUP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PSLIDEDN(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCMPcc_integer(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCMPcc_floating(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VTESTZ(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VTESTNZ(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VADD_integer(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VADD_floating(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VSUB_integer(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VSUB_floating(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMUL_integer(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMUL_floating(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VAND(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VOR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VXOR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMINS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMINU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMAXS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMAXU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMULHS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMULHU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMULHSU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VSHL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VSHR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VSAR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VROL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VROR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMIN(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMAX(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VDIV(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCOPYSIGN(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VEXTZW(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VEXTSW(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VEXTZL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VEXTSL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VEXTZQ(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VEXTSQ(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VTRUNCB(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VTRUNCW(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VTRUNCL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCVTS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCVTD(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCVTUS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCVTUD(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCVTL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCVTUL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCVTQ(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCVTUQ(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VPERM(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VZIPLO(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VZIPHI(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VUZIPLO(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VUZIPHI(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VTRNLO(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VTRNHI(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCVTH(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VCVTUH(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMADD(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMSUB(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VNMADD(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VNMSUB(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VSLICE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VSLIDEUP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VSLIDEDN(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VEXTRACT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VINSERT(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VREDADD(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VREDMINS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VREDMINU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VREDMAXS(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VREDMAXU(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VREDAND(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VREDOR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VREDXOR(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VREDMIN(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VREDMAX(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PSEL(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PZIPLO(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PZIPHI(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PUZIPLO(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PUZIPHI(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PTRNLO(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PTRNHI(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PSLICE(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_VMOVZ(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PLOOP(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

void zexecute_PMOV(struct zoptionzIRExecution_resultzK *rop, struct zDecoded_instruction, struct zCpu_state);

bool zlive_event_state_valid(struct zCpu_state);

bool zfp_static_operand_relation_valid(struct zDecoded_instruction);

void zplatform_reset(struct zCpu_state *rop, struct zCpu_state);

void zdecode_and_execute_full(struct zoptionzIRExecution_resultzK *rop, zz5listz8z5bvz9, struct zCpu_state);

unit zinitializze_registers(unit);

extern struct zexception *current_exception;

extern bool have_exception;

extern sail_string *throw_location;



#ifdef __cplusplus
}
#endif
