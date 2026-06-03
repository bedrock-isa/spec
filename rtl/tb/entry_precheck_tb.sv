`timescale 1ns/1ps
`default_nettype none

module entry_precheck_tb;
  import bedrock_pkg::*;

  logic [32*WORD_BITS-1:0] line_words;
  logic [31:0] entry_valid;
  logic [31:0] prefix_valid;
  logic [31:0] decode_valid;
  logic [31:0] repeat_present;
  logic [31:0] end_group;
  logic [31:0] repcc_allowed;
  logic [31:0] repg_allowed;
  logic [31:0] repg_fast_candidate;
  logic [31:0] repcc_valid;
  logic [31:0] repg_valid;
  logic [31:0] repeat_valid;
  logic [31:0] repeat_invalid;
  int failures;

  bedrock_line_entry_precheck dut (
    .line_i(line_words),
    .entry_valid_o(entry_valid),
    .prefix_valid_o(prefix_valid),
    .decode_valid_o(decode_valid),
    .repeat_present_o(repeat_present),
    .end_group_o(end_group),
    .repcc_allowed_o(repcc_allowed),
    .repg_allowed_o(repg_allowed),
    .repg_fast_candidate_o(repg_fast_candidate),
    .repcc_valid_o(repcc_valid),
    .repg_valid_o(repg_valid),
    .repeat_valid_o(repeat_valid),
    .repeat_invalid_o(repeat_invalid)
  );

  task automatic set_line_word(
    input int unsigned index,
    input word_t value
  );
    begin
      line_words[index*WORD_BITS +: WORD_BITS] = value;
    end
  endtask

  task automatic expect_entry(
    input int unsigned index,
    input logic expected_entry_valid,
    input logic expected_repeat_present,
    input logic expected_end_group,
    input logic expected_repcc_allowed,
    input logic expected_repg_allowed,
    input logic expected_repg_fast,
    input logic expected_repcc_valid,
    input logic expected_repg_valid,
    input logic expected_repeat_invalid
  );
    begin
      #1;
      if (entry_valid[index] !== expected_entry_valid) begin
        $error("entry[%0d] valid got %0b expected %0b", index, entry_valid[index], expected_entry_valid);
        failures++;
      end
      if (repeat_present[index] !== expected_repeat_present) begin
        $error("entry[%0d] repeat_present got %0b expected %0b", index, repeat_present[index], expected_repeat_present);
        failures++;
      end
      if (end_group[index] !== expected_end_group) begin
        $error("entry[%0d] end_group got %0b expected %0b", index, end_group[index], expected_end_group);
        failures++;
      end
      if (repcc_allowed[index] !== expected_repcc_allowed) begin
        $error("entry[%0d] repcc_allowed got %0b expected %0b", index, repcc_allowed[index], expected_repcc_allowed);
        failures++;
      end
      if (repg_allowed[index] !== expected_repg_allowed) begin
        $error("entry[%0d] repg_allowed got %0b expected %0b", index, repg_allowed[index], expected_repg_allowed);
        failures++;
      end
      if (repg_fast_candidate[index] !== expected_repg_fast) begin
        $error("entry[%0d] repg_fast got %0b expected %0b", index, repg_fast_candidate[index], expected_repg_fast);
        failures++;
      end
      if (repcc_valid[index] !== expected_repcc_valid) begin
        $error("entry[%0d] repcc_valid got %0b expected %0b", index, repcc_valid[index], expected_repcc_valid);
        failures++;
      end
      if (repg_valid[index] !== expected_repg_valid) begin
        $error("entry[%0d] repg_valid got %0b expected %0b", index, repg_valid[index], expected_repg_valid);
        failures++;
      end
      if (repeat_invalid[index] !== expected_repeat_invalid) begin
        $error("entry[%0d] repeat_invalid got %0b expected %0b", index, repeat_invalid[index], expected_repeat_invalid);
        failures++;
      end
    end
  endtask

  initial begin
    failures = 0;
    line_words = '0;

    // ADD.D_TO_D with REPcc T,D0.
    set_line_word(0, 16'h9080);
    set_line_word(1, 16'h0080);
    expect_entry(0, 1'b1, 1'b1, 1'b0, 1'b1, 1'b1, 1'b1, 1'b1, 1'b0, 1'b0);

    // RET is control flow, so a REPcc prefix is structurally invalid.
    set_line_word(2, 16'h9007);
    set_line_word(3, 16'h0080);
    expect_entry(2, 1'b1, 1'b1, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b1);

    // ADD.D_TO_D with REPG D0 and ENDG on the same instruction.
    set_line_word(4, 16'h9080);
    set_line_word(5, 16'h6860);
    expect_entry(4, 1'b1, 1'b1, 1'b1, 1'b1, 1'b1, 1'b1, 1'b0, 1'b1, 1'b0);

    // CPUID is a REPG-general state query, but not a REPcc operation.
    set_line_word(6, 16'haf63);
    set_line_word(7, 16'h0060);
    set_line_word(8, 16'h001b);
    expect_entry(6, 1'b1, 1'b1, 1'b0, 1'b0, 1'b1, 1'b0, 1'b0, 1'b1, 1'b0);

    set_line_word(9, 16'haf63);
    set_line_word(10, 16'h0080);
    set_line_word(11, 16'h001b);
    expect_entry(9, 1'b1, 1'b1, 1'b0, 1'b0, 1'b1, 1'b0, 1'b0, 1'b0, 1'b1);

    // Stack operations are excluded from REPG.
    set_line_word(12, 16'h9008);
    set_line_word(13, 16'h0060);
    expect_entry(12, 1'b1, 1'b1, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b1);

    if (failures != 0) begin
      $fatal(1, "entry_precheck_tb failed with %0d failure(s)", failures);
    end
    $display("entry_precheck_tb PASS");
    $finish;
  end
endmodule

`default_nettype wire
