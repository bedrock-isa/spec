# `isa_reference` 비교 검토 결과

- 검토 대상: `build/isa_reference.tex`
- 비교 자료:
  - `325462-091-sdm-vol-1-2abcd-3abcd-4-v2.pdf` — Intel® 64 and IA-32 Architectures Software Developer's Manual, Combined Volumes, 2026-03
  - `M68000PRM.pdf` — M68000 Family Programmer's Reference Manual, 1992
- 검토일: 2026-07-25

## 1. 검토 방식과 판정 기준

이 문서는 명령 이름·목차·문장 일치율을 기계적으로 비교한 결과가 아니다. `isa_reference`를 독립적인 CPU, 어셈블러, 운영체제, 디버거 구현자가 읽는다는 전제로 다음을 수동으로 대조했다.

1. 하나의 명령 또는 상태 전이가 문서만으로 유일하게 결정되는가.
2. 같은 입력에서 서로 다른 두 구현이 동일한 가시 결과, 예외, 플래그, 메모리 순서를 만들 수 있는가.
3. 소프트웨어가 기능을 발견하고 안전하게 사용할 수 있는가.
4. Intel SDM과 M68000 PRM이 반복해서 사용하는 명세 장치—비트 단위 형식, 명령별 operation, 정확한 주소지정 허용표, 플래그표, 예외표, 초기 상태표, opcode map—중 이 ISA에도 필요한데 빠진 것이 있는가.

`build/isa_reference.tex`가 `\input`으로 포함하는 생성 조각도 최종 문서의 일부로 보아 함께 확인했다.

심각도는 다음과 같다.

| 등급 | 의미 |
|---|---|
| **B — 구현 차단** | 서로 호환되지 않는 구현이 모두 현재 문장을 만족할 수 있거나, 필요한 크기·형식·연산을 계산할 수 없음 |
| **H — 높은 위험** | 단일 구현은 임의 선택으로 진행할 수 있으나 OS, 도구, 멀티코어 또는 보안 경계에서 호환성이 깨질 가능성이 큼 |
| **M — 보완 필요** | 핵심 의미는 추정할 수 있으나 검증, 이식성, 문서 사용성이 부족함 |
| **E — 편집/설명** | 규범 의미보다 탐색성, 용어, 예시 또는 문서 완성도의 문제 |

## 2. 총평

현재 문서는 초안 수준을 상당히 넘는다. 특히 1–18바이트 명령 레코드, little-endian payload, EA의 temporary-image/commit 규칙, 결과 우선순위와 fault atomicity, 페이지 워크의 A/D 원자 갱신, multi-copy atomic 메모리 모델, 이벤트 프레임과 이중 장애, 반복 명령의 재시작 상태, FPTRANSA의 ULP 계약은 강점이다.

초기 검토에서 분류한 CPUID, SAVE/RESTORE, 공통 부동소수점, 캐시 유지보수 block,
EA role/width 다섯 항목과 H-01~H-08, M-01~M-08, E-01~E-02를 ISA 정의와 생성 문서에 반영했다.

## 3. 발견 사항 요약

| ID | 등급 | 영역 | 핵심 문제 |
|---|---:|---|---|
| B-01 | 해결 | CPUID | Class 2 directory, cache topology, performance counter, SAVE layout payload를 비트 단위로 정의 |
| B-02 | 해결 | SAVE/RESTORE | FMT, 전체 크기, component descriptor, bitmap/GS 및 clean lifecycle을 정의 |
| B-03 | 해결 | 부동소수점 | format, NaN, rounding, exception/commit, compare/min/max/convert 공통 규칙을 정의 |
| B-04 | 해결 | 캐시 명령 | CPUID maintenance granule과 한 EA당 한 physical block, 전파 범위를 정의 |
| B-05 | 해결 | EA | 모든 EA operand에 role과 interpretation width를 부여 |
| H-01 | 해결 | Reset | 실행 LP 범위, 전체 reset state, 보존 상태와 완료·직렬화 조건을 정의 |
| H-02 | 해결 | 메모리 타입 | CP0–CP3의 공통 coherence·원자성 및 정책별 차이와 alias 의미를 정의 |
| H-03 | 해결 | TLB/ASID | translation identity, 전이별 무효화 범위와 remote shootdown 순서를 정의 |
| H-04 | 해결 | Segment/control | segment image 검사와 WRSTATUS/WRCR 전이·commit·무효화 규칙을 정의 |
| H-05 | 해결 | 이벤트/디버그 | event manifest와 priority, saved PC·commit·payload 및 TF/RF 규칙을 정의 |
| H-06 | 해결 | 반복 실행 | 명령별 repeat context와 REPcc 관찰값 및 REPGF 표기 의미를 정의 |
| H-07 | 해결 | 명령 항목 | Operation, feature/repeat, exceptions, flag 보존 및 destination overlap을 구조화 |
| H-08 | 해결 | 인코딩 | 전체 allocation map과 extended LEN·padding·fetch·disassembly 규칙을 정의 |
| M-01 | 해결 | 원자성/메모리 순서 | atomic RMW 목록, 실패한 CMPXCHG와 fence ordered-before 표 및 litmus를 정의 |
| M-02 | 해결 | Paging | paging-off 주소 의미와 cross-page 검사·fault·A/D commit 순서를 정의 |
| M-03 | 해결 | 발견/버전 | identity field의 namespace와 architecture revision 호환성 수준을 정의 |
| M-04 | 해결 | Stack/control flow | implicit stack 주소식, slot 폭, pair/far/event commit 규칙을 공통화 |
| M-05 | 해결 | 성능 카운터 | PMC.EN과 unprivileged RDPMC, wrap/reset/freeze 계약이 현재 형식과 일치함을 확인 |
| M-06 | 해결 | WAIT/HALT | WAIT를 spin-wait hint로, HALT를 event admission에 연결된 per-LP 정지로 정의 |
| M-07 | 해결 | 도구 문법 | canonical assembly grammar와 exact encoding/disassembly vector를 정의 |
| M-08 | 해결 | 검증/준수 | 규범 우선순위, conformance manifest와 영역별 검증 vector를 정의 |
| E-01 | 해결 | 용어/상호참조 | canonical field-name 표와 normal-memory·slot·trace 용어의 정의 위치를 통일 |
| E-02 | 해결 | 탐색성 | 다섯 통합 색인과 Unreleased/released revision history를 생성 원본에 연결 |

## 4. 상세 검토

### B-01. CPUID payload — 해결

Class 2 leaf 0은 common header만 갖는 `IMPLEMENTATION_DIRECTORY`로 정리했고, leaf `0x0001`은
`CACHE_TOPOLOGY`, leaf `0x0002`는 `PERFORMANCE_COUNTERS`, leaf `0x0004`는 `SAVE_AREA_LAYOUT`으로
연결했다. 각 leaf의 index 범위와 반환 비트가 규범 표에 있으며 index 0 common header의
`MAX_LEAF`/`MAX_INDEX` 규칙과 직접 연결된다.

### B-02. SAVE/RESTORE image — 해결

`SAVE_AREA_SIZE_BYTES`, fixed block 크기, component 수, bitmap word 수, `FMT`, component ID/bitmap
bit/offset/size/alignment/init policy를 CPUID index로 정의했다. 현재 형식은 `FMT=0`, fixed block은
`0x0c0`, FP component는 ID 1과 bitmap bit 0을 사용한다.

SAVE는 `GS_VALID=0x3f`를 기록한다. RESTORE의 clear GS bit는 현재 값을 보존하며, clear component bit는
그 component의 초기 상태를 설치한다. reset·RESTORE·component write에 따른 clean/modified 전이,
SAVE가 그 상태를 바꾸지 않는 규칙, CPUID 전체 크기의 선검증과 fault 시 무부분효과도 규범화했다.

### B-03. Floating-Point Common Semantics — 해결

FPU instruction group 앞에 binary32/64 layout, sNaN/qNaN, default NaN, S register upper bits, DAZ/DN/FTZ,
rounding과 tininess, overflow/underflow/inexact, fused 단일 rounding, enabled exception의 commit 규칙을
추가했다.

FCMP/FTEST의 ZNCV 네 관계, FMIN/FMAX의 NaN·signed-zero 선택, FROUND nearest-even, FCVT의 S↔D 방향과
64-bit integer 폭을 고정했다. FP→integer invalid 결과는 부호 방향 포화와 NaN=0 규칙을 사용하며,
invalid에는 NV만, 유효한 절삭에는 NX만 발생한다. S/D 각각에 대해 NaN, signed zero, subnormal,
네 rounding mode, enabled trap, 포화 변환 회귀 벡터를 추가했다.

### B-04. Cache-maintenance block — 해결

`CACHE_TOPOLOGY` index 1은 1–4096 byte의 power-of-two maintenance granule을 반환하고 index 2 이후는
cache type, level, line size, sharing scope와 ID를 열거한다. 한 cache 명령은 변환된 physical address를
granule로 내림 정렬한 block 하나를 처리한다.

Data-cache 조작은 coherence domain의 D/unified copy 전체에 완료된다. Instruction-cache invalidation은
실행 logical processor에 적용되며 원격 실행자는 rendezvous 뒤 각자 INVICACHE를 실행한다. C range
builtin은 byte range와 교차하는 block을 순회하고, 각 block 명령의 fault/retirement 경계를 유지한다.
granule 경계, 2-block range, page 경계 fault, data-domain broadcast, 원격 I-cache rendezvous 벡터로
각 경계를 고정했다.

### B-05. EA role과 interpretation width — 해결

모든 EA operand가 `value`, `address`, `control_target` 중 하나의 role과
`operation_size|B|W|L|Q` interpretation width를 갖는다. 문서 생성도 operand 위치 대신 이 role로
필드 설명을 만든다.

크기 없는 address/control form은 Q-width를 사용하므로 EXT0 scale과 base auto-update는 8 bytes이다.
SAVE/RESTORE는 save-area base를 제공하는 address role이며, control-target memory form은 선언된 폭의
target을 읽고 register/immediate form은 값을 직접 사용한다.

## 5. 높은 위험 항목 — 해결

### H-01. Reset 상태와 범위 — 해결

`Processor Reset and Initialization`의 `Warm RESET Contract`와 `Architectural Reset State` 표에
실행한 logical processor 하나를 대상으로 하는 RESET 계약을 추가했다. 명령은 supervisor 직렬화
명령이며, 이전 메모리 효과와 write-combining store를 완료한 뒤 상태를 전환한다.

R0–R15, SP, FLAGS, segment register, control register, counter, FPU와 확장 상태 및 hidden state를
빠짐없이 분류했다. `STATUS.PM=1`, 나머지 STATUS bit는 0, `PC=BOOTPC`로 정하고 BOOTPC와 BOOTCFG는
보존한다. repeat, reservation, translation/page-walk/prefetch와 pending NMI 상태는 지우고,
coherent cache 내용은 유지하되 BOOTPC fetch 전에 instruction-fetch synchronization을 완료한다.
다른 logical processor의 상태는 변하지 않는다.

### H-02. PTE cache policy와 메모리 모델 — 해결

`Normal-Memory Cache Policies` 표에 CP0 cacheable write-back, CP1 coherent uncacheable,
CP2 coherent write-through, CP3 coherent uncached/write-combining을 정의했다. 네 정책 모두 같은
normal-memory coherence, tearing, atomic, fence 규칙을 사용하며 allocation, dirty-copy 보유,
store 결합만 다르다.

CP2 store의 coherence 진입과 dirty-copy 금지, CP3 read/fetch의 uncached 처리와 byte-write·
per-location order 보존을 고정했다. 동일 physical location의 mixed-CP alias는 같은 coherent 값을
관찰하고 atomic operation은 physical location을 기준으로 직렬화된다. WFENCE/AFENCE와 해당
writeback·flush·synchronization이 pending CP3 store를 완료하며 self-modifying-code 순서는 모든 CP에
동일하게 적용된다.

### H-03. Translation identity와 shootdown — 해결

`Translation-Cache Identity and Transition Rules` 표는 translation identity를 linear page, LA57,
PABITS_SEL과 AE가 켜진 non-global entry의 ASID로 정의한다. PTCR root는 tag가 아니며 한 ASID를
하나의 PTCR image에 결속하는 조건은 소프트웨어 규약이다. Global entry는 ASID를 무시하지만 모든
context에서 PFN, permission, CP와 AT가 같아야 한다.

AE 전환, PTCR·ASCR 변경, SWPT/SWPTA, INVPAGE/INVASID/INVTLB가 보존하거나 폐기하는 항목을 표로
고정했다. Page walker는 CP0 coherent normal-memory access로 64-bit PTE의 단일 coherence version을
읽는다. `Translation Shootdown Protocol`에는 PTE store부터 AFENCE, local invalidate, target별
acquire/invalidate/release acknowledgement, 최종 acknowledgement acquire와 reclaim 전 AFENCE까지의
순서를 규정했다.

### H-04. Segment와 control transition — 해결

`Memory Address Translation`은 `m=0` segment image를 disabled image로 인정하고, `m!=0`일 때
`base+(m<<e)<<12`가 64-bit 범위를 넘지 않도록 검사한다. 접근 검사는 segment bounds, paging 사용 시
canonicality, paging 순으로 적용한다.

`Control-Register Write Rules` 표는 모든 WRCR selector의 writable mask, reserved-bit 검사, image
검사, commit 시점과 translation invalidation 효과를 단일 근원으로 정의한다. WRSTATUS는 IE, NI,
TF, RF만 바꿀 수 있고 PM과 EA는 현재 값과 같아야 한다. Pending NMI가 있는 상태에서 NI를 1에서
0으로 바꾸면 다음 instruction boundary에서 admission한다. PTCR 그림도 PABITS_SEL과 LA57이라는 실제
필드명을 사용한다.

### H-05. Event와 TF/RF — 해결

`Architectural Event Manifest`에 모든 exception, interrupt와 NMI의 producer, fault/trap 종류,
saved PC, commit/restart 상태, frame, payload와 priority를 배치했다. 우선순위는 delivery failure,
machine check, 현재 동기 fault, explicit trap, DEBUG_TRACE, NMI, maskable interrupt 순이다.

Trace unit은 일반 명령 하나, REP/REPcc의 committed body iteration 하나, REPG의 completed group
iteration 하나 및 zero-count completion으로 정의했다. TF는 unit 시작 시 샘플링한다. RF는 다음에
완료되는 trace unit의 DEBUG_TRACE만 한 번 억제하고 그 commit에서 지워지며, commit 전 fault나
비동기 event에서는 보존된다. Event entry는 이전 TF/RF를 frame에 저장한 뒤 live TF/RF를 지우며
BKPT 같은 explicit trap은 RF 억제 대상이 아니다.

### H-06. Repeat 계약 — 해결

`Instruction Repeat Contracts` 표와 instruction schema에 명령별 REP, REPcc, REPG context 및 REPcc
관찰 방식을 추가했다. `flags`는 body 뒤 FLAGS 전체, `result`와 `source`는 지정 operand에서 얻은
Z/N과 C=V=0을 사용하며 이 임시 값은 architectural FLAGS를 바꾸지 않는다.

Flags writer, 단일-result 명령, MOVNT/PUSH, POP, DIVMOD quotient, SETcc와 SEGLEA의 관찰 방식을
각각 명시했다. MOVcc, XCHG, PUSHP/POPP, FPOPP/FPUSHP에는 REPcc가 없고 FPU 반복은 REP와 REPG로
정리했다. REPGF는 별도 architectural context가 아니라 REPG와 counter-write 조건에서 파생되는
assembler spelling이다.

### H-07. Instruction entry 폐쇄성 — 해결

기존 schema의 form별 EA role, interpretation width와 허용 form은 유지하고 생성 문서가 그대로
표시하도록 검사한다. 각 instruction entry는 `description`을 규범 `Operation`으로 출력하며 Details는
보충 의미로 구분한다. Feature와 repeat attribute는 실제 값이 있는 항목에만 표시한다.

Instruction별 exception은 event와 적용 form을 참조하는 구조화 항목이다. 같은 종류의 writable
destination이 둘 이상인 form은 overlap 관계를 가져야 한다. XCHG와 FXCHG의 동일 register는
unchanged이고, FSINCOSA와 DIVMODS/U의 중복 destination은
`ILLEGAL_INSTRUCTION.INVALID_OPERAND_RELATION`이다. FLAGS/FFLAGS 표는 언급되지 않은 bit를
preserved로 출력하고 명시적 undefined 값도 표현할 수 있다. CMPXCHG의 flag 이름은 `Z`로 바로잡았다.

### H-08. Opcode map과 padding — 해결

`Opcode Allocation Map`은 encoding 저장소에서 class, opcode pattern, form ID, operand 제약,
feature owner, required byte 수, 허용 LEN 범위와 destination overlap 관계를 생성한다.

Extended instruction의 concrete form이 요구하는 길이를 `required`라 할 때 `required ≤ n ≤ 18`인
모든 총길이를 허용한다. Trailing padding은 0을 포함한 임의의 byte이며 operand나 opcode 일부로
해석하지 않는다. 전체 `n` byte의 fetch·permission 검사를 operand 실행 전에 끝내고
`n<required`에는 `ILLEGAL_INSTRUCTION.INSUFFICIENT_LENGTH`를 발생시킨다.

어셈블리 문법은 `LEN n, <instruction>`이며 `n`은 총 byte 수다. 생략하면 최단형, 명시하면 요청
길이까지 0 padding을 생성한다. 역어셈블러는 overlong record에 `LEN n,`을 출력해 길이만 보존하고
재어셈블 시 padding은 0으로 만든다. Extrashort와 short 형식은 고정 길이다.

## 6. 보완 필요 항목 — 해결

### M-01. 원자 명령과 fence의 ordered-before 관계 — 해결

Memory Model은 `CMPXCHG`, `FETCHADD`, `FETCHSUB`, `FETCHAND`, `FETCHOR`, `FETCHXOR`를 atomic
read-modify-write 집합으로 열거한다. `CMPXCHG`의 order selector는 성공과 실패 모두에 적용된다. 실패는
memory read와 expected-register/FLAGS 결과를 commit하며 acquire와 release가 정한 ordered-before를
유지하지만 memory write를 만들지 않는다. 실패한 `CMPXCHG.SEQCST`는 global SC order의 load로
참여한다.

`RFENCE`, `WFENCE`, `AFENCE`가 각각 만드는 R/W ordered-before 조합은 한 표에서 추적된다. Ordinary
`XCHG`, `BSET`, `BCLR`, `BCHG` memory form은 normal-memory load, 계산, store 순서로 정의된다.
Physical alias 직렬화와 cumulative AFENCE를 포함한 결과는 concrete litmus vector로 고정했다.

### M-02. Paging 경계·주소폭·cross-page 접근 — 해결

Paging이 꺼지면 64-bit linear address 전체가 byte-addressed memory-system address가 되고
`PABITS_SEL`은 paging geometry에만 적용된다. Byte range가 여러 page와 교차하면 낮은 linear page부터
translation, permission과 address type을 확인하고 첫 실패 page를 보고한다.

Store는 전체 range와 필요한 D update가 성공한 뒤 data를 commit한다. 뒤 page의 fault는 data와 D를
바꾸지 않으며 앞 page의 A는 기존 speculative-A 규칙을 따른다. Cross-page instruction record fetch도
같은 page 순서와 첫 fault 규칙을 사용한다.

### M-03. Identity와 revision 호환성 — 해결

`ARCHITECTURE_ID`는 하나의 호환 가능한 base architecture line을 식별한다.
`ARCHITECTURE_REVISION`은 그 line 안의 16-bit 단조 호환성 수준이며 높은 값은 낮은 값의 base behavior를
보존한다. Optional instruction과 state 사용 여부는 revision 값이 아니라 해당 CPUID leaf와 feature
predicate로 결정한다.

`VENDOR_ID`는 implementation identity namespace를 식별하고 `IMPLEMENTATION_ID`는 그 vendor 안에서
해석된다. `IMPLEMENTATION_REVISION`의 비교 범위는 같은 vendor와 implementation ID 조합이다. Unknown
CPUID selector와 reserved result bit는 기존 Query Model 규칙으로 처리된다.

### M-04. Stack과 control transfer 공통 규칙 — 해결

`Implicit Stack Operations` 표는 push 계열의 `SP-n`, pop 계열의 `SP+n`, 8-byte single slot, 16-byte
pair와 far frame, event frame의 range와 commit을 한곳에 모은다. Address 계산은 mathematical range
규칙과 SS segment pre-translation을 사용한다.

`PUSHP`/`POPP`는 complete two-slot range를 먼저 검사하고 두 slot, 두 register와 SP를 한 instruction
commit으로 처리한다. CALL/RET, LCALL/LRET과 event frame은 같은 표에서 해당 상세 규칙으로 연결된다.

### M-05. 성능 카운터 형식과 접근 계약 — 해결

현재 PMC image는 `EN`을 counter increment enable로 정의한다. `RDPMC`는 모든 privilege level에서
구현된 counter를 읽으며 standard counter는 64-bit modulo wrap, cold/warm reset clear와 `PMC.EN=0`
freeze 규칙을 갖는다. CPUID performance-counter leaf와 instruction entry가 같은 counter ID 집합을
사용한다.

### M-06. WAIT와 HALT 실행 경계 — 해결

`WAIT`는 spin-wait loop를 위한 unprivileged execution hint이다. 정상 retire 뒤 다음 instruction으로
진행하며 구현이 선택하는 유한한 지연은 0일 수 있다.

`HALT`는 실행 logical processor의 다음 PC를 continuation으로 retire한다. 같은 boundary에서 event가
admissible하면 halt 상태를 거치지 않고 기존 priority로 전달한다. 그렇지 않으면 그 logical processor가
fetch를 멈추고, 이후 기존 admission 규칙을 만족한 event를 continuation PC로 전달하기 전에는 다음
instruction을 실행하지 않는다.

### M-07. Canonical assembly와 golden encoding — 해결

`Assembler Language and Canonical Text`는 token, register와 literal, EA, condition 및 size suffix,
operand order와 `LEN`의 concrete grammar를 정의한다. Form matching은 operand와 field constraint를
만족하는 후보 중 shortest valid encoding을 선택하며 기존 alias는 primary condition과 instruction
spelling으로 canonicalize된다.

다섯 encoding class와 compact/EXT0 EA, condition-size, alias 및 overlong padding을 포함하는 vector가
canonical assembly, form ID, field, payload byte, complete encoding과 canonical disassembly를 함께
고정한다.

### M-08. 규범 준수 기준과 검증 묶음 — 해결

Conformance 절은 byte decode에는 encoding form과 field constraint, instruction 실행에는 Operation과
Detailed Semantics, 공통 동작에는 architecture chapter의 규칙을 적용한다. Summary와 guide는 이
규범 의미를 바꾸지 않으며 같은 수준의 규범 자료가 충돌하면 specification defect이다.

통합 conformance manifest는 encoding, atomic ordering, address translation, stack/event, floating-point,
cache synchronization vector를 연결한다. 각 source의 case ID와 실제 파일을 검증하고,
현재 문서에 존재하는 implementation-defined 항목의 정의 위치와 publication channel을 함께 추적한다.

## 7. 편집·상호참조 문제 — 해결

### E-01. 용어와 상호참조 통일 — 해결

URCTL selector의 `use` 문자열은 YAML inline comma까지 포함하는 하나의 값으로 고정했으며, generator는
control-register row의 key 집합을 엄격히 검사한다. 생성 selector 표는 FLAGS, STATUS와 valid state를 모두
표시한다.

Terminology는 `AT=0`을 byte-addressed normal memory로, `CP=0..3`을 그 cache-policy 집합으로 정의한다.
`cacheable`은 CP0만 가리키며 `AT=1`은 externally acknowledged slot-addressed transaction이다. 별도 구조가
없던 device-memory 문장은 삭제했다.

`TRACE`는 trace stream marker instruction, trace unit은 TF가 관찰하는 completion unit,
`DEBUG_TRACE`는 그 완료 뒤 전달되는 event로 각각 연결했다. FLAGS, STATUS, PTCR, ASCR, ECR, URCTL, PMC,
PTE와 instruction header의 canonical field-name 표는 실제 정의 절을 가리킨다. 검증기는 구식 `ZF`와
`PSEL` 표기가 원본에 다시 들어오는 것을 거부한다.

### E-02. 통합 색인과 변경 이력 — 해결

`Reference Indexes and Revision History` 부록은 기존 단일 원본에서 다음을 생성한다.

- mnemonic에서 instruction page, form ID와 encoding class/opcode pattern
- architectural state와 field에서 정의, reader/writer와 reset value
- event code에서 producer, priority, frame과 정의 절
- CPUID predicate에서 selector, gated instruction과 관련 state/SAVE component
- opcode, compact/EXT0 EA, operand/control selector, event ID와 CPUID namespace의 allocation 상태

수동 navigation 원본은 state-group 보충 정보, canonical field group과 revision history만 보유한다.
instruction form, control register, event와 extension feature는 각각 encoding store와 기존 manifest에서
직접 파생된다. 현재 draft는 숫자 revision을 만들지 않고 `Unreleased`에 기록되며, released entry만
16-bit `ARCHITECTURE_REVISION`을 사용한다.

## 8. 수정 순서

### 완료 — 상호 의존성이 큰 구현 차단 항목

1. CPUID class 2 leaf schema와 `SAVE_AREA_LAYOUT`
2. SAVE/RESTORE format 및 component lifecycle
3. Floating-Point Common Semantics
4. EA operand-role/interpretation-width schema
5. cache-maintenance granule, block 및 scope

### 완료 — OS, 디버거와 도구 경계

1. reset-state 표
2. segment/control-register validation 및 side effect
3. event별 exception matrix와 TF/RF
4. TLB/ASID/context-switch/shootdown protocol
5. PTE cache policy와 memory model 연결
6. instruction repeat·exception·destination-overlap schema
7. opcode allocation map과 LEN/padding 규칙

### 완료 — 편집과 탐색성

1. 용어와 canonical field-name 상호참조 통일
2. mnemonic, register, exception, CPUID와 allocation 통합 색인
3. Unreleased/released architecture revision history

## 9. 완료 판정 체크리스트

아래 질문에 모두 문서의 한 표 또는 한 절로 답할 수 있으면 독립 구현 기준에 가까워진다.

- [x] CPUID만으로 SAVE buffer의 총 크기, 정렬, 모든 component offset을 계산할 수 있는가?
- [x] 모든 FP special-value 조합의 결과 bit pattern과 exception/commit 여부가 유일한가?
- [x] 모든 `<ea>` operand의 역할과 scale/update width가 form별로 정해지는가?
- [x] cache 명령 한 번이 건드리는 정확한 byte/line 집합과 processor scope를 알 수 있는가?
- [x] reset 후 모든 architectural state가 value/undefined/preserved 중 하나인가?
- [x] OS가 PTE를 바꾼 뒤 다른 hardware thread까지 안전하게 translation을 폐기할 수 있는가?
- [x] 각 exception의 saved PC, error payload, priority, restart 성질이 표에 있는가?
- [x] TF/RF 및 repeat의 상호작용을 debugger가 추정 없이 구현할 수 있는가?
- [x] 각 instruction form의 정확한 EA, flags, exceptions, aliases, repeat eligibility가 한곳에 있는가?
- [x] 모든 opcode byte pattern이 valid, reserved, extension 중 하나로 분류되는가?
- [x] padding의 canonical encoding과 fetch/fault 의미가 하나로 정의되는가?
- [x] 같은 physical location의 cache-policy alias 및 atomic operation 결과가 정해지는가?
- [x] paging-off와 cross-page access에서 주소폭, fault 우선순위, 부분 효과가 정해지는가?
- [x] implementation-defined 항목과 구현자가 공개해야 할 값이 목록화되어 있는가?
- [x] canonical assembly가 하나의 form과 exact byte sequence로 연결되는가?
- [x] 규범 자료의 적용 순서와 conformance vector source가 추적되는가?
- [x] canonical field name과 normal-memory·slot·trace 용어가 한 정의 위치로 연결되는가?
- [x] instruction, state, event, CPUID와 allocation을 통합 색인에서 역추적할 수 있는가?
- [x] 현재 draft와 released architecture revision의 변경 이력을 구분할 수 있는가?

## 10. 최종 판단

`isa_reference`의 B등급 연결, H-01~H-08, M-01~M-08과 E-01~E-02는 닫혔다. Reset, PTE/cache policy, translation
shootdown, segment/control transition, event/debug trace, repeat, instruction entry와 encoding padding의
규범 정의에 더해 atomic/fence, cross-page, revision, stack, WAIT/HALT, assembler와 conformance 규칙이
schema, vector와 생성 문서에 연결되어 있다. 용어와 canonical field name은 glossary와 생성 표로
고정했고, 통합 색인과 revision history가 각 규범 원본을 역추적한다. 이 검토에서 분류한 미해결 항목은 없다.
