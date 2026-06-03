`timescale 1ns/1ps
`default_nettype none

module decode_tb;
  import bedrock_pkg::*;
  import bedrock_decode_pkg::*;

  primary_payload_t primary_payload;
  logic [15:0] extension_word;
  logic valid;
  logic needs_extension;
  logic alias_form;
  bedrock_form_id_e form_id;
  bedrock_ext_root_e ext_root;
  logic repcc_allowed;
  logic repg_allowed;
  logic repg_fast_candidate;
  int failures;

  bedrock_decode dut (
    .primary_payload_i(primary_payload),
    .extension_word_i(extension_word),
    .valid_o(valid),
    .needs_extension_o(needs_extension),
    .alias_o(alias_form),
    .form_id_o(form_id),
    .ext_root_o(ext_root),
    .repcc_allowed_o(repcc_allowed),
    .repg_allowed_o(repg_allowed),
    .repg_fast_candidate_o(repg_fast_candidate)
  );

  task automatic check_decode(
    input primary_payload_t payload,
    input logic [15:0] ext_word,
    input logic expected_valid,
    input logic expected_extended
  );
    begin
      primary_payload = payload;
      extension_word = ext_word;
      #1;
      if (valid !== expected_valid) begin
        $error("payload=%03h ext=%04h valid got %0b expected %0b", payload, ext_word, valid, expected_valid);
        failures++;
      end
      if (needs_extension !== expected_extended) begin
        $error("payload=%03h ext=%04h extended got %0b expected %0b", payload, ext_word, needs_extension, expected_extended);
        failures++;
      end
    end
  endtask

  initial begin
    failures = 0;

    check_decode(12'h000, 16'h0000, 1'b1, 1'b0); // HALT sentinel
    check_decode(12'hfff, 16'h0000, 1'b1, 1'b0); // ILLEGAL sentinel
    check_decode(12'hef1, 16'h0104, 1'b1, 1'b1); // EXT.integer_alu ADD.EA_TO_D.BWLQ in current allocation
    check_decode(12'hef1, 16'h0118, 1'b0, 1'b1); // valid extension root, unallocated extension opcode

    if (failures != 0) begin
      $fatal(1, "decode_tb failed with %0d failure(s)", failures);
    end
    $display("decode_tb PASS");
    $finish;
  end
endmodule

`default_nettype wire
