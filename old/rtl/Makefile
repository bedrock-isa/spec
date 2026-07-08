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

DOLOMITE0_SRCS := $(COMMON_DIR)/bedrock_pkg.sv $(DOLOMITE0_DIR)/bedrock_core_pkg.sv
DECODE_SRCS := $(COMMON_DIR)/bedrock_pkg.sv $(GEN_DIR)/bedrock_decode_pkg.sv $(GEN_DIR)/bedrock_decode.sv
DECODE_SYNTH_SRC := $(GEN_DIR)/bedrock_decode_synth.sv
PREFIX_DECODE_SRCS := $(GEN_DIR)/bedrock_prefix_decode_pkg.sv $(GEN_DIR)/bedrock_prefix_decode.sv
PREFIX_DECODE_SYNTH_SRC := $(GEN_DIR)/bedrock_prefix_decode_synth.sv
EA_DECODE_SRCS := $(GEN_DIR)/bedrock_ea_decode_pkg.sv $(GEN_DIR)/bedrock_ea_decode.sv
EA_DECODE_SYNTH_SRC := $(GEN_DIR)/bedrock_ea_decode_synth.sv
FULL_DECODE_SRCS := $(COMMON_DIR)/bedrock_pkg.sv $(GEN_DIR)/bedrock_decode_pkg.sv $(GEN_DIR)/bedrock_prefix_decode_pkg.sv $(GEN_DIR)/bedrock_ea_decode_pkg.sv $(COMMON_DIR)/bedrock_agu_pkg.sv $(GEN_DIR)/bedrock_decode.sv $(GEN_DIR)/bedrock_prefix_decode.sv $(GEN_DIR)/bedrock_ea_decode.sv $(FRONTEND_DIR)/bedrock_agu_request_build.sv $(FRONTEND_DIR)/bedrock_full_decode.sv
AGU_SRCS := $(GEN_DIR)/bedrock_prefix_decode_pkg.sv $(GEN_DIR)/bedrock_ea_decode_pkg.sv $(COMMON_DIR)/bedrock_agu_pkg.sv $(EXECUTE_DIR)/bedrock_agu.sv
FULL_DECODE_HAND_SRCS := $(COMMON_DIR)/bedrock_pkg.sv $(COMMON_DIR)/bedrock_agu_pkg.sv $(FRONTEND_DIR)/bedrock_agu_request_build.sv $(FRONTEND_DIR)/bedrock_full_decode.sv
AGU_HAND_SRCS := $(COMMON_DIR)/bedrock_agu_pkg.sv $(EXECUTE_DIR)/bedrock_agu.sv
DECODE_TB_SRCS := $(TB_DIR)/decode_tb.sv
PREFIX_EA_TB_SRCS := $(TB_DIR)/prefix_ea_tb.sv
FULL_DECODE_TB_SRCS := $(TB_DIR)/full_decode_tb.sv
AGU_TB_SRCS := $(TB_DIR)/agu_tb.sv

TEST_TOP ?= decode_tb
TEST_RTL_SRCS ?= $(DECODE_SRCS)
TEST_TB_SRCS ?= $(DECODE_TB_SRCS)
TEST_BUILD_DIR := $(BUILD_DIR)/$(TEST_TOP)
TEST_BIN := $(TEST_BUILD_DIR)/V$(TEST_TOP)
DECODE_SYNTH_REPORT := $(YOSYS_BUILD_DIR)/decode_synth.rpt
DECODE_SYNTH_JSON := $(YOSYS_BUILD_DIR)/bedrock_decode_synth.json
PREFIX_SYNTH_REPORT := $(YOSYS_BUILD_DIR)/prefix_decode_synth.rpt
PREFIX_SYNTH_JSON := $(YOSYS_BUILD_DIR)/bedrock_prefix_decode_synth.json
EA_SYNTH_REPORT := $(YOSYS_BUILD_DIR)/ea_decode_synth.rpt
EA_SYNTH_JSON := $(YOSYS_BUILD_DIR)/bedrock_ea_decode_synth.json
FULL_DECODE_SYNTH_REPORT := $(YOSYS_BUILD_DIR)/full_decode_synth.rpt
FULL_DECODE_SYNTH_JSON := $(YOSYS_BUILD_DIR)/bedrock_full_decode.json
FULL_DECODE_SV2V := $(YOSYS_BUILD_DIR)/bedrock_full_decode_sv2v.v
AGU_SYNTH_REPORT := $(YOSYS_BUILD_DIR)/agu_synth.rpt
AGU_SYNTH_JSON := $(YOSYS_BUILD_DIR)/bedrock_agu.json
AGU_SV2V := $(YOSYS_BUILD_DIR)/bedrock_agu_sv2v.v

VERILATORFLAGS ?= -sv -Wall -Wno-UNUSEDPARAM -Wno-UNUSEDSIGNAL --timing --assert

.PHONY: help lint test run-test core-lint decode-sv decode-lint decode-test decode-synth execute-lint execute-test execute-synth clean

help:
	@printf '%s\n' 'RTL targets:'
	@printf '  %-16s %s\n' 'lint' 'Lint active SystemVerilog RTL with Verilator.'
	@printf '  %-16s %s\n' 'test' 'Build and run decoder and execute smoke testbenches.'
	@printf '  %-16s %s\n' 'core-lint' 'Lint baseline scalar core packages.'
	@printf '  %-16s %s\n' 'decode-sv' 'Generate instruction/prefix/EA decoders through the ISA tooling.'
	@printf '  %-16s %s\n' 'decode-lint' 'Lint generated instruction/prefix/EA decoders with Verilator.'
	@printf '  %-16s %s\n' 'decode-test' 'Build and run generated decoder and full-decode smoke testbenches.'
	@printf '  %-16s %s\n' 'decode-synth' 'Synthesize generated decoders with Yosys and report generic cell stats.'
	@printf '  %-16s %s\n' 'execute-lint' 'Lint hand-written execute-stage helper units.'
	@printf '  %-16s %s\n' 'execute-test' 'Build and run execute-stage helper testbenches.'
	@printf '  %-16s %s\n' 'execute-synth' 'Synthesize hand-written execute-stage helper units.'
	@printf '  %-16s %s\n' 'clean' 'Remove RTL Verilator build artifacts.'

lint: core-lint decode-lint execute-lint

core-lint: $(DOLOMITE0_SRCS)
	$(VERILATOR) $(VERILATORFLAGS) --lint-only $(DOLOMITE0_SRCS)

decode-sv:
	$(MAKE) -C ../isa decode-sv

decode-lint: decode-sv
	$(VERILATOR) $(VERILATORFLAGS) --lint-only --top-module bedrock_decode $(DECODE_SRCS)
	$(VERILATOR) $(VERILATORFLAGS) --lint-only --top-module bedrock_prefix_decode $(PREFIX_DECODE_SRCS)
	$(VERILATOR) $(VERILATORFLAGS) --lint-only --top-module bedrock_ea_decode $(EA_DECODE_SRCS)
	$(VERILATOR) $(VERILATORFLAGS) --lint-only --top-module bedrock_full_decode $(FULL_DECODE_SRCS)

$(TEST_BIN): $(TEST_RTL_SRCS) $(TEST_TB_SRCS)
	@mkdir -p "$(TEST_BUILD_DIR)"
	$(VERILATOR) $(VERILATORFLAGS) --binary --Mdir "$(TEST_BUILD_DIR)" --top-module $(TEST_TOP) $(TEST_RTL_SRCS) $(TEST_TB_SRCS)

run-test: $(TEST_BIN)
	$(TEST_BIN)

test: decode-test execute-test

decode-test: decode-sv $(DECODE_TB_SRCS) $(PREFIX_EA_TB_SRCS) $(FULL_DECODE_TB_SRCS)
	$(MAKE) run-test TEST_TOP=decode_tb TEST_RTL_SRCS="$(DECODE_SRCS)" TEST_TB_SRCS="$(DECODE_TB_SRCS)"
	$(MAKE) run-test TEST_TOP=prefix_ea_tb TEST_RTL_SRCS="$(PREFIX_DECODE_SRCS) $(EA_DECODE_SRCS)" TEST_TB_SRCS="$(PREFIX_EA_TB_SRCS)"
	$(MAKE) run-test TEST_TOP=full_decode_tb TEST_RTL_SRCS="$(FULL_DECODE_SRCS)" TEST_TB_SRCS="$(FULL_DECODE_TB_SRCS)"

execute-lint: decode-sv $(AGU_HAND_SRCS)
	$(VERILATOR) $(VERILATORFLAGS) --lint-only --top-module bedrock_agu $(AGU_SRCS)

execute-test: decode-sv $(AGU_HAND_SRCS) $(AGU_TB_SRCS)
	$(MAKE) run-test TEST_TOP=agu_tb TEST_RTL_SRCS="$(AGU_SRCS)" TEST_TB_SRCS="$(AGU_TB_SRCS)"

execute-synth: decode-sv $(AGU_SYNTH_REPORT)
	@tail -60 "$(AGU_SYNTH_REPORT)"

decode-synth: decode-sv $(DECODE_SYNTH_REPORT) $(PREFIX_SYNTH_REPORT) $(EA_SYNTH_REPORT) $(FULL_DECODE_SYNTH_REPORT)
	@tail -80 "$(DECODE_SYNTH_REPORT)"
	@tail -50 "$(PREFIX_SYNTH_REPORT)"
	@tail -50 "$(EA_SYNTH_REPORT)"
	@tail -60 "$(FULL_DECODE_SYNTH_REPORT)"

$(DECODE_SYNTH_REPORT): | decode-sv
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(YOSYS) -Q -p 'read_verilog -sv $(DECODE_SYNTH_SRC); synth -top bedrock_decode_synth; stat -top bedrock_decode_synth; write_json $(DECODE_SYNTH_JSON)' > "$(DECODE_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(DECODE_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(DECODE_SYNTH_JSON)"

$(PREFIX_SYNTH_REPORT): | decode-sv
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(YOSYS) -Q -p 'read_verilog -sv $(PREFIX_DECODE_SYNTH_SRC); synth -top bedrock_prefix_decode_synth; stat -top bedrock_prefix_decode_synth; write_json $(PREFIX_SYNTH_JSON)' > "$(PREFIX_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(PREFIX_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(PREFIX_SYNTH_JSON)"

$(EA_SYNTH_REPORT): | decode-sv
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(YOSYS) -Q -p 'read_verilog -sv $(EA_DECODE_SYNTH_SRC); synth -top bedrock_ea_decode_synth; stat -top bedrock_ea_decode_synth; write_json $(EA_SYNTH_JSON)' > "$(EA_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(EA_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(EA_SYNTH_JSON)"

$(FULL_DECODE_SV2V): $(FULL_DECODE_HAND_SRCS) | decode-sv
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(SV2V) $(FULL_DECODE_SRCS) > "$(FULL_DECODE_SV2V)"
	@printf 'wrote %s\n' "$(FULL_DECODE_SV2V)"

$(FULL_DECODE_SYNTH_REPORT): $(FULL_DECODE_SV2V)
	@mkdir -p "$(YOSYS_BUILD_DIR)"
	$(YOSYS) -Q -p 'read_verilog $(FULL_DECODE_SV2V); synth -top bedrock_full_decode; stat -top bedrock_full_decode; write_json $(FULL_DECODE_SYNTH_JSON)' > "$(FULL_DECODE_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(FULL_DECODE_SYNTH_REPORT)"
	@printf 'wrote %s\n' "$(FULL_DECODE_SYNTH_JSON)"

$(AGU_SV2V): $(AGU_HAND_SRCS) | decode-sv
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
