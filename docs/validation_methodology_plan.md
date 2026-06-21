# Bedrock ISA 검증 방법론 계획서

이 문서는 Bedrock의 명령어 밀도와 디코더 복잡도 tradeoff를 AArch64, RV64GC와 비교하기 위한 논문용 검증 방법론을 정의한다. 핵심 원칙은 결과 표를 손으로 관리하지 않고, repo 안의 benchmark, generator, RTL synthesis tooling에서 재현 가능한 산출물을 만들도록 하는 것이다.

## 검증할 주장

Bedrock은 opcode allocation만으로 평가하면 안 되고, ISA와 front-end 설계점을 함께 평가해야 한다. 논문에서 검증할 1차 주장은 다음이다.

- Bedrock은 scalar system kernel 성격의 코드에서 RV64GC/AArch64 대비 같거나 더 나은 code density를 보이면서, 1차 instruction decode와 normalized full decode의 하드웨어 비용을 과도하게 키우지 않는다.

논문 결과는 한 축만 보여주면 설득력이 약하다. 최소한 다음 두 축을 같이 제시한다.

| 축 | 의미 | 1차 metric |
| --- | --- | --- |
| code density | 같은 C source를 target별로 컴파일했을 때 코드가 얼마나 작은가 | executable `.text` bytes |
| decoder complexity | target ISA를 decode하는 combinational front-end logic이 얼마나 큰가 | synthesized cell count |

보조 metric은 static instruction count, mapped area, critical path, benchmark category별 분포로 둔다.

## 비교 대상

1차 비교 대상:

| Target | 역할 | 현재 repo 경로 |
| --- | --- | --- |
| Bedrock | 후보 ISA | `qbe/bedrock`, `isa/asm`, `rtl/frontend` |
| AArch64 | fixed-width 64-bit baseline | `tools/compare_arch.py`가 Clang target으로 생성 |
| RV64GC | compressed RISC baseline | `tools/compare_arch.py`가 Clang target으로 생성 |

보조 비교 대상:

| Target | 역할 |
| --- | --- |
| x86-64 | mature dense CISC context. decoder 비교의 주대상으로 두지 않는다. |
| m68k | historical compact CISC context. density 참고값으로만 쓴다. |

논문 본문은 Bedrock/AArch64/RV64GC 중심으로 구성한다. x86-64와 m68k는 compiler maturity, ABI, decoder 구조가 크게 달라서 primary hardware-cost claim에 직접 섞으면 해석이 흐려진다.

## 현재 재사용할 수 있는 산출물

명령어 밀도:

- `benchmarks/arch_compare/*.c`: 현재 scalar benchmark corpus.
- `tools/compare_arch.py`: target별 code-density runner.
- `benchmarks/Makefile`: density 비교 재현 entry point.
- `build/compare/arch_compare.md`: 생성된 사람이 읽는 report.
- `build/compare/arch_compare.json`: 생성된 machine-readable result.

디코더 복잡도:

- `isa/spec/**`: instruction, operand, register, EA, prefix, semantic SoT.
- `isa/tools/gen_sv_decode.py`: instruction decoder generator.
- `isa/tools/gen_sv_aux_decode.py`: prefix/EA decoder generator.
- `rtl/frontend/bedrock_full_decode.sv`: integrated normalized decode RTL.
- `rtl/Makefile`: Verilator/Yosys entry point.
- `build/yosys/*_synth.rpt`: Yosys synthesis report.
- `build/yosys/*.json`: synthesized netlist JSON.

## 명령어 밀도 측정 방법

동일한 C source를 각 target으로 컴파일하고, ELF `.text` section size를 primary metric으로 쓴다. 현재 runner는 reference target에 대해 freestanding 환경을 사용하고, unwind table, stack protector, builtin noise를 제거한다.

기본 실행:

```sh
make -C benchmarks arch-compare
```

논문 본문용 1차 target만 다시 뽑는 실행:

```sh
python3 tools/compare_arch.py benchmarks/arch_compare \
  --targets bedrock aarch64 rv64gc \
  --qbe build/qbe/obj/qbe \
  --minic qbe/minic/minic \
  --bedrock-as build/host/bedrock-as \
  --bedrock-cmodel small \
  --clang clang \
  --opt Oz \
  --out-dir build/compare/arch \
  --report build/compare/arch_compare.md \
  --json build/compare/arch_compare.json
```

측정값:

| Metric | Source | 용도 |
| --- | --- | --- |
| `.text` bytes | `tools/compare_arch.py`의 ELF section parser | primary code-density metric |
| static ASM instruction count | generated assembly parser | instruction selection 설명용 보조 metric |
| object bytes | ELF file size | diagnostic. 논문 primary metric으로 쓰지 않는다. |
| target metadata | runner target table | ABI, code model, ISA option 공개 |

집계 방식:

- benchmark별 `.text` bytes를 표로 낸다.
- benchmark별 Bedrock 대비 ratio를 표로 낸다.
- corpus 전체 `.text` bytes 합계를 낸다.
- per-case ratio의 arithmetic mean을 낸다.
- normalized comparison용으로 per-case ratio의 geometric mean을 낸다.
- 최종 논문 표와 그림은 `arch_compare.json`에서 생성한다. 숫자를 손으로 옮긴 표를 SoT로 두지 않는다.

현재 local snapshot은 sanity tracking 용도로만 쓴다.

| Target | Cases | Total `.text` bytes | Bedrock total | Arithmetic mean ratio vs Bedrock | Geometric mean ratio vs Bedrock |
| --- | ---: | ---: | ---: | ---: | ---: |
| AArch64 | 21 | 1772 | 1178 | 1.613 | 1.591 |
| RV64GC | 21 | 1476 | 1178 | 1.357 | 1.317 |
| x86-64 | 21 | 1380 | 1178 | 1.230 | 1.214 |
| m68k | 21 | 1598 | 1178 | 1.658 | 1.501 |

이 값들은 paper-ready result가 아니다. 최종 결과는 clean commit에서 tool version을 기록한 뒤 다시 생성한다.

## 디코더 복잡도 측정 방법

디코더 비교는 반드시 같은 boundary를 맞춰야 한다. Bedrock generated decoder를 다른 ISA의 production core 전체 front-end와 비교하거나, 반대로 단순 opcode classifier와 비교하면 결론이 무의미해진다.

Bedrock은 세 boundary로 나눠 측정한다.

| Boundary | Bedrock module | 의미 |
| --- | --- | --- |
| instruction form decode | `bedrock_decode_synth` | primary word classification과 operand field extraction |
| auxiliary decode | `bedrock_prefix_decode_synth`, `bedrock_ea_decode_synth` | prefix metadata와 effective-address metadata decode |
| normalized full decode | `bedrock_full_decode` | integrated decode record, prefix legality, EA classification, AGU request construction |

기본 synthesis 실행:

```sh
make -C rtl decode-synth
```

synthesis 전 검증:

```sh
make -C isa validate
make -C rtl decode-test
```

측정값:

| Metric | Source | 용도 |
| --- | --- | --- |
| generic cell count | Yosys `stat` | primary decoder-cost metric |
| cell mix | Yosys `stat` | mux/comparator pressure 설명 |
| wire bits, port bits | Yosys `stat` | interface-size diagnostic |
| critical path | technology-mapped Yosys/ABC run | 최종 논문 claim에 필요 |
| mapped area | 고정한 standard-cell library 또는 open PDK | 최종 논문 claim에 필요 |

현재 Bedrock local snapshot은 regression sanity 용도로만 둔다.

| Module | Generic cells |
| --- | ---: |
| `bedrock_decode_synth` | 1905 |
| `bedrock_prefix_decode_synth` | 104 |
| `bedrock_ea_decode_synth` | 274 |
| `bedrock_full_decode` | 4097 |

논문 최종 결과에는 generic cell count만 두지 말고, 동일한 technology mapping 아래의 area와 critical path를 같이 제시한다.

## AArch64/RV64GC 디코더 baseline 구성

임의의 open-source core decoder를 가져와 비교하지 않는다. 비교 baseline은 Bedrock `bedrock_full_decode`와 가능한 한 같은 normalized output contract를 갖는 작은 decoder RTL로 만든다.

공통 output contract:

- instruction length 또는 fixed-length 확인;
- opcode class;
- integer source/destination register fields;
- immediate class와 sign/zero extension metadata;
- branch/call/return class;
- load/store width와 addressing class;
- fence 또는 memory-ordering class;
- illegal/reserved instruction indication.

AArch64 baseline:

- fixed 32-bit instruction length;
- benchmark compiler output에 필요한 scalar integer, branch, load/store, system/fence subset;
- primary scalar result에서는 SVE/SME/NEON datapath decode를 제외한다;
- corpus가 FP/vector를 포함하도록 확장되면 appendix에서 별도 full-feature run을 둔다.

RV64GC baseline:

- 16/32-bit length classification;
- `-march=rv64gc`에 맞는 RV64I, M, A, F, D, C decode class;
- compressed instruction을 먼저 expansion하는지, 직접 normalized decode하는지 명시한다;
- RV64GC가 density 이득을 얻는 경로이므로 compressed form 식별 logic은 primary decoder cost에 포함한다.

공정성 규칙:

- 모든 target decoder는 combinational logic으로 두고 같은 Yosys command sequence로 합성한다.
- 모든 target decoder는 ISA가 지원하는 범위에서 같은 normalized control category를 내보낸다.
- benchmark-reachable subset만 구현할 경우, target별 subset table을 논문에 반드시 싣는다.
- vendor manual diagram이나 prose를 비교하지 않는다. 같은 flow에서 합성된 RTL끼리 비교한다.
- register file, branch predictor, fetch queue, instruction cache, execution datapath는 primary decoder metric에서 제외한다.

## 통합 분석 방법

논문에는 density와 decoder cost를 같은 표와 같은 plot에 묶어서 제시한다.

target별 요약 표:

| Target | `.text` total | Geomean density ratio | Decoder cells | Mapped area | Critical path | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- |

tradeoff metric:

- `density_ratio_to_bedrock = target_text_bytes / bedrock_text_bytes`.
- `decoder_cell_ratio_to_bedrock = target_decoder_cells / bedrock_decoder_cells`.
- `density_gain_per_decoder_cell = (target_text_bytes - bedrock_text_bytes) / bedrock_decoder_cells`.
- 같은 boundary에서 code size와 decode cost가 둘 다 큰 target은 dominated point로 표시한다.

benchmark별 scatter plot은 density가 어디서 나오는지 설명하는 데 쓴다.

- memory addressing kernels;
- branch-heavy kernels;
- register-pressure kernels;
- call/return kernels;
- arithmetic and bit-manipulation kernels.

## 재현성 요구사항

최종 실험 run마다 다음 metadata를 기록한다.

- git commit hash;
- worktree clean 여부;
- host OS와 architecture;
- `clang --version`;
- `yosys -V`;
- `sv2v --version`;
- `verilator --version`;
- Bedrock QBE build command와 commit state;
- benchmark command line;
- synthesis command line;
- generated report paths.

권장 결과 directory layout:

```text
results/YYYYMMDD-HHMMSS/
  manifest.json
  arch_compare.md
  arch_compare.json
  synth/
    bedrock_decode_synth.rpt
    bedrock_prefix_decode_synth.rpt
    bedrock_ea_decode_synth.rpt
    bedrock_full_decode_synth.rpt
    *.json
  plots/
    density_geomean.pdf
    density_by_case.pdf
    decode_cells.pdf
    density_decode_pareto.pdf
```

## 추가로 필요한 tooling

논문 제출 전까지 다음 자동화를 추가한다.

- `results/YYYYMMDD-HHMMSS`에 한 번에 실험 결과를 capture하는 command;
- Yosys report/JSON에서 cell count, mapped area, critical path를 추출하는 parser;
- `arch_compare.json`에서 aggregate density summary를 생성하는 script;
- AArch64/RV64GC comparison decoder RTL 또는 decoder generator;
- compiler-emitted benchmark instruction을 이용한 AArch64/RV64GC decoder unit test;
- result JSON에서 paper figure를 생성하는 plot script;
- 측정 script가 계속 실행되는지 확인하는 CI smoke target.

## Threats To Validity

Compiler maturity:

Bedrock은 현재 local QBE backend와 `bedrock-as`를 쓰고, AArch64/RV64GC는 mature Clang codegen을 쓴다. 이 차이는 어느 방향으로도 bias를 만들 수 있다. 논문에서는 density를 "toolchain-observed code density"로 표현하고, pure ISA optimum처럼 주장하지 않는다.

ABI effects:

call-heavy, register-pressure case는 calling convention, callee-save rule, argument register, stack alignment, code model에 민감하다. 모든 result set에는 ABI context table을 같이 둔다.

Benchmark representativeness:

현재 corpus는 작은 scalar kernel 중심이다. controlled front-end experiment에는 적합하지만 whole-program density claim에는 부족하다. 큰 freestanding workload는 별도 단계에서 추가한다.

Decoder subset effects:

AArch64/RV64GC decoder baseline은 지원 subset을 명시해야 한다. subset이 benchmark-reachable scalar decode라면 complete ISA decoder라고 쓰면 안 된다.

Synthesis-flow effects:

generic Yosys cell count는 portable complexity metric으로 유용하지만, 최종 paper claim에는 technology-mapped area/timing이 필요하다. generic cell은 portable primary metric, mapped area는 corroborating metric으로 둔다.

## Acceptance Criteria

다음 조건을 만족하면 paper-result collection에 들어갈 수 있다.

- `make -C benchmarks arch-compare`가 Markdown과 JSON을 생성한다.
- `make -C rtl decode-test`가 통과한다.
- `make -C rtl decode-synth`가 Bedrock decoder report를 모두 생성한다.
- AArch64/RV64GC baseline decoder가 Bedrock과 같은 normalized output contract를 쓴다.
- plot/table data가 JSON 또는 synthesis report에서 생성되고, 손으로 복사한 숫자를 SoT로 쓰지 않는다.
- 최종 result bundle에 tool version과 git commit을 담은 manifest가 포함된다.

