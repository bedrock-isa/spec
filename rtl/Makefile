VERILATOR ?= verilator
YOSYS ?= yosys
SV2V ?= sv2v

BUILD_DIR ?= ../build/verilator
YOSYS_BUILD_DIR ?= ../build/yosys
GEN_DIR ?= ../build/generated
COMMON_DIR := common
DOLOMITE0_DIR := dolomite0
FRONTEND_DIR := frontend
EXECUTE_DIR := execute
TB_DIR := tb

RTL_SRCS := $(COMMON_DIR)/bedrock_pkg.sv $(FRONTEND_DIR)/bedrock_predecode.sv $(FRONTEND_DIR)/bedrock_line_predecode.sv
DOLOMITE0_SRCS := $(COMMON_DIR)/bedrock_pkg.sv $(DOLOMITE0_DIR)/bedrock_core_pkg.sv
DECODE_SRCS := $(COMMON_DIR)/bedrock_pkg.sv $(GEN_DIR)/bedrock_decode_pkg.sv $(GEN_DIR)/bedrock_decode.sv
DECODE_SYNTH_SRC := $(GEN_DIR)/bedrock_decode_synth.sv
PREFIX_DECODE_SRCS := $(GEN_DIR)/bedrock_prefix_decode_pkg.sv $(GEN_DIR)/bedrock_prefix_decode.sv
PREFIX_DECODE_SYNTH_SRC := $(GEN_DIR)/bedrock_prefix_decode_synth.sv
EA_DECODE_SRCS := $(GEN_DIR)/bedrock_ea_decode_pkg.sv $(GEN_DIR)/bedrock_ea_decode.sv
EA_DECODE_SYNTH_SRC := $(GEN_DIR)/bedrock_ea_decode_synth.sv
ENTRY_PRECHECK_SRCS := $(COMMON_DIR)/bedrock_pkg.sv $(GEN_DIR)/bedrock_decode_pkg.sv $(GEN_DIR)/bedrock_prefix_decode_pkg.sv $(GEN_DIR)/bedrock_decode.sv $(GEN_DIR)/bedrock_prefix_decode.sv $(FRONTEND_DIR)/bedrock_line_entry_precheck.sv
FULL_DECODE_SRCS := $(COMMON_DIR)/bedrock_pkg.sv $(GEN_DIR)/bedrock_decode_pkg.sv $(GEN_DIR)/bedrock_prefix_decode_pkg.sv $(GEN_DIR)/bedrock_ea_decode_pkg.sv $(COMMON_DIR)/bedrock_agu_pkg.sv $(GEN_DIR)/bedrock_decode.sv $(GEN_DIR)/bedrock_prefix_decode.sv $(GEN_DIR)/bedrock_ea_decode.sv $(FRONTEND_DIR)/bedrock_agu_request_build.sv $(FRONTEND_DIR)/bedrock_full_decode.sv
AGU_SRCS := $(GEN_DIR)/bedrock_prefix_decode_pkg.sv $(GEN_DIR)/bedrock_ea_decode_pkg.sv $(COMMON_DIR)/bedrock_agu_pkg.sv $(EXECUTE_DIR)/bedrock_agu.sv
TB_SRCS := $(TB_DIR)/predecode_tb.sv
DECODE_TB_SRCS := $(TB_DIR)/decode_tb.sv
PREFIX_EA_TB_SRCS := $(TB_DIR)/prefix_ea_tb.sv
ENTRY_PRECHECK_TB_SRCS := $(TB_DIR)/entry_precheck_tb.sv
FULL_DECODE_TB_SRCS := $(TB_DIR)/full_decode_tb.sv
AGU_TB_SRCS := $(TB_DIR)/agu_tb.sv

LINT_TOP ?= bedrock_predecode
TEST_TOP ?= predecode_tb
TEST_BUILD_DIR := $(BUILD_DIR)/$(TEST_TOP)
TEST_BIN := $(TEST_BUILD_DIR)/V$(TEST_TOP)
DECODE_SYNTH_REPORT := $(YOSYS_BUILD_DIR)/decode_synth.rpt
DECODE_SYNTH_JSON := $(YOSYS_BUILD_DIR)/bedrock_decode_synth.json
PREDECODE_SYNTH_REPORT := $(YOSYS_BUILD_DIR)/line_predecode_synth.rpt
PREDECODE_SYNTH_JSON := $(YOSYS_BUILD_DIR)/bedrock_line_predecode.json
PREFIX_SYNTH_REPORT := $(YOSYS_BUILD_DIR)/prefix_decode_synth.rpt
PREFIX_SYNTH_JSON := $(YOSYS_BUILD_DIR)/bedrock_prefix_decode_synth.json
EA_SYNTH_REPORT := $(YOSYS_BUILD_DIR)/ea_decode_synth.rpt
EA_SYNTH_JSON := $(YOSYS_BUILD_DIR)/bedrock_ea_decode_synth.json
ENTRY_PRECHECK_SYNTH_REPORT := $(YOSYS_BUILD_DIR)/entry_precheck_synth.rpt
ENTRY_PRECHECK_SYNTH_JSON := $(YOSYS_BUILD_DIR)/bedrock_line_entry_precheck.json
ENTRY_PRECHECK_SV2V := $(YOSYS_BUILD_DIR)/bedrock_line_entry_precheck_sv2v.v
FULL_DECODE_SYNTH_REPORT := $(YOSYS_BUILD_DIR)/full_decode_synth.rpt
FULL_DECODE_SYNTH_JSON := $(YOSYS_BUILD_DIR)/bedrock_full_decode.json
FULL_DECODE_SV2V := $(YOSYS_BUILD_DIR)/bedrock_full_decode_sv2v.v
AGU_SYNTH_REPORT := $(YOSYS_BUILD_DIR)/agu_synth.rpt
AGU_SYNTH_JSON := $(YOSYS_BUILD_DIR)/bedrock_agu.json
AGU_SV2V := $(YOSYS_BUILD_DIR)/bedrock_agu_sv2v.v

VERILATORFLAGS ?= -sv -Wall -Wno-UNUSEDPARAM -Wno-UNUSEDSIGNAL --timing --assert

.PHONY: help lint test predecode-synth core-lint decode-lint decode-test decode-synth execute-lint execute-test execute-synth clean

help:
	@printf '%s\n' 'RTL targets:'
	@printf '  %-10s %s\n' 'lint' 'Lint SystemVerilog RTL with Verilator.'
	@printf '  %-10s %s\n' 'test' 'Build and run SystemVerilog testbench with Verilator.'
	@printf '  %-10s %s\n' 'predecode-synth' 'Synthesize line predecoder with Yosys and report generic cell stats.'
	@printf '  %-10s %s\n' 'core-lint' 'Lint baseline scalar core packages.'
	@printf '  %-10s %s\n' 'decode-lint' 'Lint generated instruction/prefix/EA decoders with Verilator.'
	@printf '  %-10s %s\n' 'decode-test' 'Build and run generated decoder and full-decode smoke testbenches.'
	@printf '  %-10s %s\n' 'decode-synth' 'Synthesize generated decoders with Yosys and report generic cell stats.'
	@printf '  %-10s %s\n' 'execute-lint' 'Lint hand-written execute-stage helper units.'
	@printf '  %-10s %s\n' 'execute-test' 'Build and run execute-stage helper testbenches.'
	@printf '  %-10s %s\n' 'execute-synth' 'Synthesize hand-written execute-stage helper units.'
	@printf '  %-10s %s\n' 'clean' 'Remove RTL Verilator build artifacts.'

lint: $(RTL_SRCS)
	$(VERILATOR) $(VERILATORFLAGS) --lint-only --top-module $(LINT_TOP) $(RTL_SRCS)
	$(VERILATOR) $(VERILATORFLAGS) --lint-only --top-module bedrock_line_predecode $(RTL_SRCS)

core-lint: $(DOLOMITE0_SRCS)
	$(VERILATOR) $(VERILATORFLAGS) --lint-only $(DOLOMITE0_SRCS)

decode-lint: $(DECODE_SRCS)
	$(VERILATOR) $(VERILATORFLAGS) --lint-only --top-module bedrock_decode $(DECODE_SRCS)
	$(VERILATOR) $(VERILATORFLAGS) --lint-only --top-module bedrock_prefix_decode $(PREFIX_DECODE_SRCS)
	$(VERILATOR) $(VERILATORFLAGS) --lint-only --top-module bedrock_ea_decode $(EA_DECODE_SRCS)
	$(VERILATOR) $(VERILATORFLAGS) --lint-only --top-module bedrock_line_entry_precheck $(ENTRY_PRECHECK_SRCS)
	$(VERILATOR) $(VERILATORFLAGS) --lint-only --top-module bedrock_full_decode $(FULL_DECODE_SRCS)

$(TEST_BIN): $(RTL_SRCS) $(TB_SRCS)
	@mkdir -p "$(TEST_BUILD_DIR)"
	$(VERILATOR) $(VERILATORFLAGS) --binary --Mdir "$(TEST_BUILD_DIR)" --top-module $(TEST_TOP) $(RTL_SRCS) $(TB_SRCS)

test: $(TEST_BIN)
	$(TEST_BIN)

predecode-synth: $(PREDECODE_SYNTH_REPORT)
	@tail -60 "$(PREDECODE_SYNTH_REPORT)"

$(PREDECODE_SYNTH_REPORT): $(RTL_SRCS)
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(YOSYS) -Q -p 'read_verilog -sv $(RTL_SRCS); synth -top bedrock_line_predecode; stat -top bedrock_line_predecode; write_json $(PREDECODE_SYNTH_JSON)' > "$(PREDECODE_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(PREDECODE_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(PREDECODE_SYNTH_JSON)"

decode-test: $(DECODE_SRCS) $(DECODE_TB_SRCS) $(PREFIX_DECODE_SRCS) $(EA_DECODE_SRCS) $(PREFIX_EA_TB_SRCS) $(ENTRY_PRECHECK_SRCS) $(ENTRY_PRECHECK_TB_SRCS) $(FULL_DECODE_SRCS) $(FULL_DECODE_TB_SRCS)
	$(MAKE) test TEST_TOP=decode_tb RTL_SRCS="$(DECODE_SRCS)" TB_SRCS="$(DECODE_TB_SRCS)"
	$(MAKE) test TEST_TOP=prefix_ea_tb RTL_SRCS="$(PREFIX_DECODE_SRCS) $(EA_DECODE_SRCS)" TB_SRCS="$(PREFIX_EA_TB_SRCS)"
	$(MAKE) test TEST_TOP=entry_precheck_tb RTL_SRCS="$(ENTRY_PRECHECK_SRCS)" TB_SRCS="$(ENTRY_PRECHECK_TB_SRCS)"
	$(MAKE) test TEST_TOP=full_decode_tb RTL_SRCS="$(FULL_DECODE_SRCS)" TB_SRCS="$(FULL_DECODE_TB_SRCS)"

execute-lint: $(AGU_SRCS)
	$(VERILATOR) $(VERILATORFLAGS) --lint-only --top-module bedrock_agu $(AGU_SRCS)

execute-test: $(AGU_SRCS) $(AGU_TB_SRCS)
	$(MAKE) test TEST_TOP=agu_tb RTL_SRCS="$(AGU_SRCS)" TB_SRCS="$(AGU_TB_SRCS)"

execute-synth: $(AGU_SYNTH_REPORT)
	@tail -60 "$(AGU_SYNTH_REPORT)"

decode-synth: $(DECODE_SYNTH_REPORT) $(PREFIX_SYNTH_REPORT) $(EA_SYNTH_REPORT) $(ENTRY_PRECHECK_SYNTH_REPORT) $(FULL_DECODE_SYNTH_REPORT)
	@tail -80 "$(DECODE_SYNTH_REPORT)"
	@tail -50 "$(PREFIX_SYNTH_REPORT)"
	@tail -50 "$(EA_SYNTH_REPORT)"
	@tail -60 "$(ENTRY_PRECHECK_SYNTH_REPORT)"
	@tail -60 "$(FULL_DECODE_SYNTH_REPORT)"

$(DECODE_SYNTH_REPORT): $(DECODE_SYNTH_SRC)
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(YOSYS) -Q -p 'read_verilog -sv $(DECODE_SYNTH_SRC); synth -top bedrock_decode_synth; stat -top bedrock_decode_synth; write_json $(DECODE_SYNTH_JSON)' > "$(DECODE_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(DECODE_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(DECODE_SYNTH_JSON)"

$(PREFIX_SYNTH_REPORT): $(PREFIX_DECODE_SYNTH_SRC)
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(YOSYS) -Q -p 'read_verilog -sv $(PREFIX_DECODE_SYNTH_SRC); synth -top bedrock_prefix_decode_synth; stat -top bedrock_prefix_decode_synth; write_json $(PREFIX_SYNTH_JSON)' > "$(PREFIX_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(PREFIX_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(PREFIX_SYNTH_JSON)"

$(EA_SYNTH_REPORT): $(EA_DECODE_SYNTH_SRC)
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(YOSYS) -Q -p 'read_verilog -sv $(EA_DECODE_SYNTH_SRC); synth -top bedrock_ea_decode_synth; stat -top bedrock_ea_decode_synth; write_json $(EA_SYNTH_JSON)' > "$(EA_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(EA_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(EA_SYNTH_JSON)"

$(ENTRY_PRECHECK_SV2V): $(ENTRY_PRECHECK_SRCS)
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(SV2V) $(ENTRY_PRECHECK_SRCS) > "$(ENTRY_PRECHECK_SV2V)"
	@printf 'wrote %s\n' "$(ENTRY_PRECHECK_SV2V)"

$(ENTRY_PRECHECK_SYNTH_REPORT): $(ENTRY_PRECHECK_SV2V)
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(YOSYS) -Q -p 'read_verilog $(ENTRY_PRECHECK_SV2V); synth -top bedrock_line_entry_precheck; stat -top bedrock_line_entry_precheck; write_json $(ENTRY_PRECHECK_SYNTH_JSON)' > "$(ENTRY_PRECHECK_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(ENTRY_PRECHECK_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(ENTRY_PRECHECK_SYNTH_JSON)"

$(FULL_DECODE_SV2V): $(FULL_DECODE_SRCS)
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(SV2V) $(FULL_DECODE_SRCS) > "$(FULL_DECODE_SV2V)"
	@printf 'wrote %s\n' "$(FULL_DECODE_SV2V)"

$(FULL_DECODE_SYNTH_REPORT): $(FULL_DECODE_SV2V)
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(YOSYS) -Q -p 'read_verilog $(FULL_DECODE_SV2V); synth -top bedrock_full_decode; stat -top bedrock_full_decode; write_json $(FULL_DECODE_SYNTH_JSON)' > "$(FULL_DECODE_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(FULL_DECODE_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(FULL_DECODE_SYNTH_JSON)"

$(AGU_SV2V): $(AGU_SRCS)
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(SV2V) $(AGU_SRCS) > "$(AGU_SV2V)"
	@printf 'wrote %s\n' "$(AGU_SV2V)"

$(AGU_SYNTH_REPORT): $(AGU_SV2V)
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(YOSYS) -Q -p 'read_verilog $(AGU_SV2V); synth -top bedrock_agu; stat -top bedrock_agu; write_json $(AGU_SYNTH_JSON)' > "$(AGU_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(AGU_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(AGU_SYNTH_JSON)"

clean:
	rm -rf "$(BUILD_DIR)"
