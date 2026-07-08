`timescale 1ns/1ps
`default_nettype none

module agu_tb;
  import bedrock_prefix_decode_pkg::*;
  import bedrock_ea_decode_pkg::*;
  import bedrock_agu_pkg::*;

  bedrock_agu_request_t request;
  logic [63:0] base_reg_value;
  logic [63:0] index_reg_value;
  logic [63:0] pc_value;
  logic [63:0] sp_value;
  logic [63:0] payload_value;
  logic [3:0] access_size_bytes;
  logic valid;
  logic address_valid;
  logic [63:0] effective_address;
  logic [63:0] immediate_value;
  logic update_write;
  logic [63:0] update_value;
  logic update_invalid;
  int failures;

  bedrock_agu dut (
    .request_i(request),
    .base_reg_value_i(base_reg_value),
    .index_reg_value_i(index_reg_value),
    .pc_value_i(pc_value),
    .sp_value_i(sp_value),
    .payload_value_i(payload_value),
    .access_size_bytes_i(access_size_bytes),
    .valid_o(valid),
    .address_valid_o(address_valid),
    .effective_address_o(effective_address),
    .immediate_value_o(immediate_value),
    .update_write_o(update_write),
    .update_value_o(update_value),
    .update_invalid_o(update_invalid)
  );

  task automatic clear_inputs;
    begin
      request = '0;
      request.present = 1'b1;
      request.raw_valid = 1'b1;
      request.valid = 1'b1;
      request.segment_valid = 1'b1;
      base_reg_value = 64'd0;
      index_reg_value = 64'd0;
      pc_value = 64'd0;
      sp_value = 64'd0;
      payload_value = 64'd0;
      access_size_bytes = 4'd8;
    end
  endtask

  task automatic expect_logic(input string name, input logic got, input logic expected);
    if (got !== expected) begin
      $error("%s got %0b expected %0b", name, got, expected);
      failures++;
    end
  endtask

  task automatic expect_u64(input string name, input logic [63:0] got, input logic [63:0] expected);
    if (got !== expected) begin
      $error("%s got 0x%016x expected 0x%016x", name, got, expected);
      failures++;
    end
  endtask

  initial begin
    failures = 0;

    // [An + disp16] sign-extends the displacement and uses the selected A value.
    clear_inputs();
    request.is_memory = 1'b1;
    request.form = BR_EA_A_DISP16;
    request.base = BR_EA_BASE_A;
    request.has_base_reg = 1'b1;
    request.has_displacement = 1'b1;
    request.displacement_words = 3'd1;
    base_reg_value = 64'h0000_0000_0000_1000;
    payload_value = 64'h0000_0000_0000_fff0;
    #1;
    expect_logic("disp16 valid", valid, 1'b1);
    expect_logic("disp16 address valid", address_valid, 1'b1);
    expect_u64("disp16 address", effective_address, 64'h0000_0000_0000_0ff0);

    // PC-relative displacement forms are ordinary base + signed displacement.
    clear_inputs();
    request.is_memory = 1'b1;
    request.base = BR_EA_BASE_PC;
    request.has_displacement = 1'b1;
    request.displacement_words = 3'd2;
    pc_value = 64'h0000_0000_0000_2000;
    payload_value = 64'h0000_0000_ffff_fffc;
    #1;
    expect_u64("pc disp32 address", effective_address, 64'h0000_0000_0000_1ffc);

    // Indexed forms scale the selected D index before adding displacement.
    clear_inputs();
    request.is_memory = 1'b1;
    request.base = BR_EA_BASE_A;
    request.has_base_reg = 1'b1;
    request.has_index_reg = 1'b1;
    request.scale_log2 = 2'd2;
    request.has_displacement = 1'b1;
    request.displacement_words = 3'd1;
    base_reg_value = 64'h0000_0000_0000_1000;
    index_reg_value = 64'd3;
    payload_value = 64'h0020;
    #1;
    expect_u64("indexed address", effective_address, 64'h0000_0000_0000_102c);

    // ABS32 is a signed absolute address payload.
    clear_inputs();
    request.is_memory = 1'b1;
    request.has_absolute = 1'b1;
    request.base = BR_EA_BASE_ABS;
    request.displacement_words = 3'd2;
    payload_value = 64'h0000_0000_ffff_fff0;
    #1;
    expect_u64("abs32 address", effective_address, 64'hffff_ffff_ffff_fff0);

    // Immediate forms carry a payload but do not produce a memory address.
    clear_inputs();
    request.is_immediate = 1'b1;
    request.base = BR_EA_BASE_IMM;
    payload_value = 64'h1234;
    #1;
    expect_logic("immediate valid", valid, 1'b1);
    expect_logic("immediate address invalid", address_valid, 1'b0);
    expect_u64("immediate value", immediate_value, 64'h1234);

    // PREINC changes the address and writes the updated base value.
    clear_inputs();
    request.is_memory = 1'b1;
    request.base = BR_EA_BASE_A;
    request.has_base_reg = 1'b1;
    request.update_eligible = 1'b1;
    request.update_requested = 1'b1;
    request.update_valid = 1'b1;
    request.update_mode = BR_UPDATE_PREINC;
    base_reg_value = 64'h1000;
    access_size_bytes = 4'd8;
    #1;
    expect_logic("preinc update write", update_write, 1'b1);
    expect_u64("preinc address", effective_address, 64'h1008);
    expect_u64("preinc update value", update_value, 64'h1008);

    // POSTDEC uses the old address but writes the decremented base value.
    clear_inputs();
    request.is_memory = 1'b1;
    request.base = BR_EA_BASE_A;
    request.has_base_reg = 1'b1;
    request.update_eligible = 1'b1;
    request.update_requested = 1'b1;
    request.update_valid = 1'b1;
    request.update_mode = BR_UPDATE_POSTDEC;
    base_reg_value = 64'h1000;
    access_size_bytes = 4'd8;
    #1;
    expect_logic("postdec update write", update_write, 1'b1);
    expect_u64("postdec address", effective_address, 64'h1000);
    expect_u64("postdec update value", update_value, 64'h0ff8);

    // Decode marks ineligible update prefixes, and AGU suppresses the request.
    clear_inputs();
    request.is_memory = 1'b1;
    request.base = BR_EA_BASE_A;
    request.has_base_reg = 1'b1;
    request.update_requested = 1'b1;
    request.update_invalid = 1'b1;
    request.update_mode = BR_UPDATE_POSTINC;
    #1;
    expect_logic("invalid update valid", valid, 1'b0);
    expect_logic("invalid update write", update_write, 1'b0);
    expect_logic("invalid update flag", update_invalid, 1'b1);

    if (failures != 0) begin
      $fatal(1, "agu_tb failed with %0d failure(s)", failures);
    end
    $display("agu_tb PASS");
    $finish;
  end
endmodule

`default_nettype wire
