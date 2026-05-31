`timescale 1ns/1ps
`default_nettype none

module predecode_tb;
  import bedrock_pkg::*;

  word_t word0;
  logic prefix_present;
  length_field_t length_field;
  instruction_length_t length_words;
  primary_payload_t primary_payload;
  logic sentinel_halt;
  logic sentinel_illegal;
  logic [32*WORD_BITS-1:0] line_words;
  logic [31:0] line_prefix_present;
  logic [32*3-1:0] line_length_field;
  logic [32*4-1:0] line_length_words;
  logic [32*PRIMARY_PAYLOAD_BITS-1:0] line_primary_payload;
  logic [31:0] line_sentinel_halt;
  logic [31:0] line_sentinel_illegal;
  int failures;

  bedrock_predecode dut (
    .word0_i(word0),
    .prefix_present_o(prefix_present),
    .length_field_o(length_field),
    .length_words_o(length_words),
    .primary_payload_o(primary_payload),
    .sentinel_halt_o(sentinel_halt),
    .sentinel_illegal_o(sentinel_illegal)
  );

  bedrock_line_predecode line_dut (
    .line_i(line_words),
    .prefix_present_o(line_prefix_present),
    .length_field_o(line_length_field),
    .length_words_o(line_length_words),
    .primary_payload_o(line_primary_payload),
    .sentinel_halt_o(line_sentinel_halt),
    .sentinel_illegal_o(line_sentinel_illegal)
  );

  task automatic check_word0(
    input word_t value,
    input logic expected_prefix,
    input instruction_length_t expected_length,
    input primary_payload_t expected_payload,
    input logic expected_halt,
    input logic expected_illegal
  );
    begin
      word0 = value;
      #1;
      if (prefix_present !== expected_prefix) begin
        $error("word0=%04h prefix: got %0b expected %0b", value, prefix_present, expected_prefix);
        failures++;
      end
      if (length_words !== expected_length) begin
        $error("word0=%04h length: got %0d expected %0d", value, length_words, expected_length);
        failures++;
      end
      if (length_field !== value[WORD0_LENGTH_MSB:WORD0_LENGTH_LSB]) begin
        $error("word0=%04h length field mismatch", value);
        failures++;
      end
      if (primary_payload !== expected_payload) begin
        $error("word0=%04h payload: got %03h expected %03h", value, primary_payload, expected_payload);
        failures++;
      end
      if (sentinel_halt !== expected_halt) begin
        $error("word0=%04h HALT: got %0b expected %0b", value, sentinel_halt, expected_halt);
        failures++;
      end
      if (sentinel_illegal !== expected_illegal) begin
        $error("word0=%04h ILLEGAL: got %0b expected %0b", value, sentinel_illegal, expected_illegal);
        failures++;
      end
    end
  endtask

  task automatic set_line_word(
    input int unsigned index,
    input word_t value
  );
    begin
      line_words[index*WORD_BITS +: WORD_BITS] = value;
    end
  endtask

  task automatic check_line_word(
    input int unsigned index,
    input word_t expected_word
  );
    instruction_length_t expected_length;
    primary_payload_t expected_payload;
    begin
      expected_length = instruction_length_t'(expected_word[WORD0_LENGTH_MSB:WORD0_LENGTH_LSB]) + 4'd1;
      expected_payload = expected_word[WORD0_PAYLOAD_MSB:WORD0_PAYLOAD_LSB];
      #1;
      if (line_prefix_present[index] !== expected_word[WORD0_PREFIX_BIT]) begin
        $error("line[%0d]=%04h prefix got %0b expected %0b", index, expected_word, line_prefix_present[index], expected_word[WORD0_PREFIX_BIT]);
        failures++;
      end
      if (line_length_field[index*3 +: 3] !== expected_word[WORD0_LENGTH_MSB:WORD0_LENGTH_LSB]) begin
        $error("line[%0d]=%04h length field mismatch", index, expected_word);
        failures++;
      end
      if (line_length_words[index*4 +: 4] !== expected_length) begin
        $error("line[%0d]=%04h length got %0d expected %0d", index, expected_word, line_length_words[index*4 +: 4], expected_length);
        failures++;
      end
      if (line_primary_payload[index*PRIMARY_PAYLOAD_BITS +: PRIMARY_PAYLOAD_BITS] !== expected_payload) begin
        $error("line[%0d]=%04h payload got %03h expected %03h", index, expected_word, line_primary_payload[index*PRIMARY_PAYLOAD_BITS +: PRIMARY_PAYLOAD_BITS], expected_payload);
        failures++;
      end
      if (line_sentinel_halt[index] !== (expected_payload == PRIMARY_PAYLOAD_HALT)) begin
        $error("line[%0d]=%04h HALT mismatch", index, expected_word);
        failures++;
      end
      if (line_sentinel_illegal[index] !== (expected_payload == PRIMARY_PAYLOAD_ILLEGAL)) begin
        $error("line[%0d]=%04h ILLEGAL mismatch", index, expected_word);
        failures++;
      end
    end
  endtask

  initial begin
    failures = 0;

    check_word0(16'h0000, 1'b0, 4'd1, 12'h000, 1'b1, 1'b0);
    check_word0(16'h0fff, 1'b0, 4'd1, 12'hfff, 1'b0, 1'b1);
    check_word0(16'h5123, 1'b0, 4'd6, 12'h123, 1'b0, 1'b0);
    check_word0(16'h9123, 1'b1, 4'd2, 12'h123, 1'b0, 1'b0);
    check_word0(16'hf456, 1'b1, 4'd8, 12'h456, 1'b0, 1'b0);

    line_words = '0;
    set_line_word(0, 16'h0000);
    set_line_word(1, 16'h9123);
    set_line_word(7, 16'h5123);
    set_line_word(16, 16'h0fff);
    set_line_word(31, 16'hf456);
    check_line_word(0, 16'h0000);
    check_line_word(1, 16'h9123);
    check_line_word(7, 16'h5123);
    check_line_word(16, 16'h0fff);
    check_line_word(31, 16'hf456);

    if (failures != 0) begin
      $fatal(1, "predecode_tb failed with %0d failure(s)", failures);
    end
    $display("predecode_tb PASS");
    $finish;
  end
endmodule

`default_nettype wire
