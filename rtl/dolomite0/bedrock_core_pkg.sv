`timescale 1ns/1ps
`default_nettype none

package bedrock_core_pkg;
  import bedrock_pkg::*;

  localparam logic [15:0] BEDROCK_IMPL_PROFILE_DOLOMITE0 = 16'h0001;
  localparam logic [15:0] BEDROCK_IMPL_PROFILE_ID = BEDROCK_IMPL_PROFILE_DOLOMITE0;

  localparam int BEDROCK_IMPL_ISSUE_WIDTH = 1;
  localparam logic BEDROCK_IMPL_IN_ORDER = 1'b1;
  localparam logic BEDROCK_IMPL_HAS_BRANCH_PREDICTOR = 1'b0;
  localparam logic BEDROCK_IMPL_HAS_SPECULATIVE_EXECUTION = 1'b0;
  localparam logic BEDROCK_IMPL_HAS_OUT_OF_ORDER = 1'b0;
  localparam logic BEDROCK_IMPL_HAS_FPU_DATAPATH = 1'b0;
  localparam logic BEDROCK_IMPL_HAS_SIMD_DATAPATH = 1'b0;
  localparam logic BEDROCK_IMPL_HAS_REPG_FAST = 1'b0;
  localparam logic BEDROCK_IMPL_HAS_UOP_CACHE = 1'b0;

  typedef enum logic [3:0] {
    BEDROCK_PIPE_F0 = 4'd0,
    BEDROCK_PIPE_F1 = 4'd1,
    BEDROCK_PIPE_P0 = 4'd2,
    BEDROCK_PIPE_D0 = 4'd3,
    BEDROCK_PIPE_R0 = 4'd4,
    BEDROCK_PIPE_X0 = 4'd5,
    BEDROCK_PIPE_X1 = 4'd6,
    BEDROCK_PIPE_M0 = 4'd7,
    BEDROCK_PIPE_W0 = 4'd8
  } bedrock_pipe_stage_e;

  typedef enum logic [2:0] {
    BEDROCK_REDIRECT_NONE = 3'd0,
    BEDROCK_REDIRECT_BRANCH = 3'd1,
    BEDROCK_REDIRECT_CALL = 3'd2,
    BEDROCK_REDIRECT_RETURN = 3'd3,
    BEDROCK_REDIRECT_EXCEPTION = 3'd4,
    BEDROCK_REDIRECT_INTERRUPT = 3'd5,
    BEDROCK_REDIRECT_REPLAY = 3'd6
  } bedrock_redirect_kind_e;

  typedef enum logic [2:0] {
    BEDROCK_PIPE_FAULT_NONE = 3'd0,
    BEDROCK_PIPE_FAULT_ILLEGAL_INSTRUCTION = 3'd1,
    BEDROCK_PIPE_FAULT_PRIVILEGE = 3'd2,
    BEDROCK_PIPE_FAULT_PAGE = 3'd3,
    BEDROCK_PIPE_FAULT_REPEAT = 3'd4,
    BEDROCK_PIPE_FAULT_INTERNAL = 3'd5
  } bedrock_pipe_fault_e;

  typedef struct packed {
    logic valid;
    logic [63:0] pc;
    instruction_length_t length_words;
    bedrock_pipe_fault_e fault;
    logic replay;
  } bedrock_pipe_meta_t;

  typedef struct packed {
    logic valid;
    bedrock_redirect_kind_e kind;
    logic [63:0] target_pc;
  } bedrock_redirect_t;
endpackage

`default_nettype wire
