`timescale 1ns/1ps
`default_nettype none

module full_decode_tb;
  import bedrock_pkg::*;
  import bedrock_decode_pkg::*;
  import bedrock_prefix_decode_pkg::*;
  import bedrock_ea_decode_pkg::*;
  import bedrock_agu_pkg::*;

  logic [MAX_INSTRUCTION_WORDS*WORD_BITS-1:0] words;
  logic valid;
  logic prefix_present;
  logic prefix_valid;
  logic decode_valid;
  logic undersized;
  instruction_length_t length_words;
  logic [3:0] required_words;
  bedrock_opcode_id_e opcode_id;
  bedrock_field_format_id_e field_format_id;
  bedrock_ext_root_e ext_root;
  logic needs_extension;
  logic nospec;
  logic saturate;
  logic nontemporal;
  bedrock_update_mode_e update_mode;
  bedrock_access_mode_e access_mode;
  bedrock_repeat_kind_e repeat_kind;
  logic [3:0] repeat_condition;
  logic [2:0] repeat_counter;
  logic end_group;
  logic repg_fast_candidate;
  logic repcc_valid;
  logic repg_valid;
  logic repeat_present;
  logic repeat_valid;
  logic repeat_invalid;
  logic [1:0] ea_present;
  logic [5:0] ea_value [2];
  logic [3:0] ea_descriptor_token [2];
  logic ea_valid [2];
  logic ea_reserved [2];
  logic ea_needs_descriptor [2];
  bedrock_ea_form_e ea_form [2];
  logic ea_is_register [2];
  logic ea_is_memory [2];
  logic ea_is_immediate [2];
  logic ea_update_eligible [2];
  bedrock_ea_segment_e ea_segment [2];
  bedrock_ea_base_e ea_base [2];
  logic [2:0] ea_base_reg [2];
  logic [2:0] ea_index_reg [2];
  logic [1:0] ea_scale_log2 [2];
  logic [2:0] ea_payload_words [2];
  bedrock_agu_request_t agu_request [2];
  int failures;

  bedrock_full_decode dut (
    .words_i(words),
    .valid_o(valid),
    .prefix_present_o(prefix_present),
    .prefix_valid_o(prefix_valid),
    .decode_valid_o(decode_valid),
    .undersized_o(undersized),
    .length_words_o(length_words),
    .required_words_o(required_words),
    .opcode_id_o(opcode_id),
    .field_format_id_o(field_format_id),
    .ext_root_o(ext_root),
    .needs_extension_o(needs_extension),
    .nospec_o(nospec),
    .saturate_o(saturate),
    .nontemporal_o(nontemporal),
    .update_mode_o(update_mode),
    .access_mode_o(access_mode),
    .repeat_kind_o(repeat_kind),
    .repeat_condition_o(repeat_condition),
    .repeat_counter_o(repeat_counter),
    .end_group_o(end_group),
    .repg_fast_candidate_o(repg_fast_candidate),
    .repcc_valid_o(repcc_valid),
    .repg_valid_o(repg_valid),
    .repeat_present_o(repeat_present),
    .repeat_valid_o(repeat_valid),
    .repeat_invalid_o(repeat_invalid),
    .ea_present_o(ea_present),
    .ea_value_o(ea_value),
    .ea_descriptor_token_o(ea_descriptor_token),
    .ea_valid_o(ea_valid),
    .ea_reserved_o(ea_reserved),
    .ea_needs_descriptor_o(ea_needs_descriptor),
    .ea_form_o(ea_form),
    .ea_is_register_o(ea_is_register),
    .ea_is_memory_o(ea_is_memory),
    .ea_is_immediate_o(ea_is_immediate),
    .ea_update_eligible_o(ea_update_eligible),
    .ea_segment_o(ea_segment),
    .ea_base_o(ea_base),
    .ea_base_reg_o(ea_base_reg),
    .ea_index_reg_o(ea_index_reg),
    .ea_scale_log2_o(ea_scale_log2),
    .ea_payload_words_o(ea_payload_words),
    .agu_request_o(agu_request)
  );

  task automatic set_word(input int unsigned index, input word_t value);
    words[index*WORD_BITS +: WORD_BITS] = value;
  endtask

  task automatic clear_words;
    words = '0;
  endtask

  task automatic expect_logic(input string name, input logic got, input logic expected);
    if (got !== expected) begin
      $error("%s got %0b expected %0b", name, got, expected);
      failures++;
    end
  endtask

  task automatic expect_u16(input string name, input logic [15:0] got, input logic [15:0] expected);
    if (got !== expected) begin
      $error("%s got 0x%04x expected 0x%04x", name, got, expected);
      failures++;
    end
  endtask

  initial begin
    failures = 0;

    // One-word ADD.Q D1,D2.
    clear_words();
    set_word(0, 16'h00d1);
    #1;
    expect_logic("add valid", valid, 1'b1);
    if (opcode_id !== BR_OPCODE_ADD || field_format_id !== BR_FIELD_FORMAT_F035) begin
      $error("add decode got opcode %0d field format %0d expected ADD/F035", opcode_id, field_format_id);
      failures++;
    end
    expect_logic("add ea absent", |ea_present, 1'b0);

    // MOV.L [A0 + disp16], D3 requires one EA payload word.
    clear_words();
    set_word(0, 16'h18d8);
    set_word(1, 16'h0010);
    #1;
    expect_logic("mov valid", valid, 1'b1);
    if (opcode_id !== BR_OPCODE_MOV || field_format_id !== BR_FIELD_FORMAT_F040) begin
      $error("mov decode got opcode %0d field format %0d expected MOV/F040", opcode_id, field_format_id);
      failures++;
    end
    expect_u16("mov ea raw", {10'd0, ea_value[0]}, 16'h0018);
    if (ea_form[0] !== BR_EA_A_DISP16) begin
      $error("mov ea form got %0d expected A_DISP16", ea_form[0]);
      failures++;
    end
    expect_logic("mov agu present", agu_request[0].present, 1'b1);
    expect_logic("mov agu memory", agu_request[0].is_memory, 1'b1);
    expect_logic("mov agu displacement", agu_request[0].has_displacement, 1'b1);
    expect_u16("mov agu payload base", {12'd0, agu_request[0].payload_base_token}, 16'd1);
    expect_u16("mov required words", {12'd0, required_words}, 16'd2);

    // Same encoding without the displacement word is structurally undersized.
    clear_words();
    set_word(0, 16'h08d8);
    #1;
    expect_logic("undersized mov valid", valid, 1'b0);
    expect_logic("undersized mov flag", undersized, 1'b1);

    // ADD.Q D1,D2 with REPcc T,D0 in the prefix word.
    clear_words();
    set_word(0, 16'h90d1);
    set_word(1, 16'h0080);
    #1;
    expect_logic("rep add valid", valid, 1'b1);
    expect_logic("rep prefix present", prefix_present, 1'b1);
    expect_logic("rep present", repeat_present, 1'b1);
    expect_logic("repcc valid", repcc_valid, 1'b1);
    if (repeat_kind !== BR_REPEAT_REPCC) begin
      $error("repeat kind got %0d expected REPCC", repeat_kind);
      failures++;
    end

    // Extended ADD.L D2,D3 through the EA_TO_D form with a DREG EA source.
    clear_words();
    set_word(0, 16'h2f31);
    set_word(1, 16'h0104);
    set_word(2, 16'h04c2);
    #1;
    expect_logic("extended add valid", valid, 1'b1);
    if (opcode_id !== BR_OPCODE_ADD || field_format_id !== BR_FIELD_FORMAT_F047) begin
      $error("extended add decode got opcode %0d field format %0d expected ADD/F047", opcode_id, field_format_id);
      failures++;
    end
    expect_logic("extended add needs extension", needs_extension, 1'b1);
    expect_u16("extended add ea", {10'd0, ea_value[0]}, 16'd2);
    if (ea_form[0] !== BR_EA_DREG) begin
      $error("extended add ea form got %0d expected DREG", ea_form[0]);
      failures++;
    end
    expect_u16("extended add required", {12'd0, required_words}, 16'd3);

    // Extended MOV.L D1,[A0 + disp16] has two EA operands and one EA payload word.
    clear_words();
    set_word(0, 16'h2f3a);
    set_word(1, 16'h6601);
    set_word(2, 16'h0020);
    #1;
    expect_logic("mov ea ea valid", valid, 1'b1);
    if (opcode_id !== BR_OPCODE_MOV || field_format_id !== BR_FIELD_FORMAT_F044) begin
      $error("mov ea ea decode got opcode %0d field format %0d expected MOV/F044", opcode_id, field_format_id);
      failures++;
    end
    if (ea_present !== 2'b11) begin
      $error("mov ea ea present got %0b expected 11", ea_present);
      failures++;
    end
    if (ea_form[0] !== BR_EA_DREG) begin
      $error("mov src ea form got %0d expected DREG", ea_form[0]);
      failures++;
    end
    if (ea_form[1] !== BR_EA_A_DISP16) begin
      $error("mov dst ea form got %0d expected A_DISP16", ea_form[1]);
      failures++;
    end
    expect_logic("mov ea ea src agu register", agu_request[0].is_register, 1'b1);
    expect_logic("mov ea ea dst agu memory", agu_request[1].is_memory, 1'b1);
    expect_u16("mov ea ea dst payload base", {12'd0, agu_request[1].payload_base_token}, 16'd2);
    expect_u16("mov ea ea required", {12'd0, required_words}, 16'd3);

    // POSTINC is update-valid for plain [A] EA operands.
    clear_words();
    set_word(0, 16'h98d0);
    set_word(1, 16'h0004);
    #1;
    expect_logic("postinc mov valid", valid, 1'b1);
    expect_logic("postinc requested", agu_request[0].update_requested, 1'b1);
    expect_logic("postinc valid", agu_request[0].update_valid, 1'b1);
    expect_logic("postinc invalid", agu_request[0].update_invalid, 1'b0);

    // The same prefix is marked invalid for displacement EA operands.
    clear_words();
    set_word(0, 16'ha8d8);
    set_word(1, 16'h0004);
    set_word(2, 16'h0010);
    #1;
    expect_logic("postinc disp structural valid", valid, 1'b1);
    expect_logic("postinc disp requested", agu_request[0].update_requested, 1'b1);
    expect_logic("postinc disp invalid", agu_request[0].update_invalid, 1'b1);

    if (failures != 0) begin
      $fatal(1, "full_decode_tb failed with %0d failure(s)", failures);
    end
    $display("full_decode_tb PASS");
    $finish;
  end
endmodule

`default_nettype wire
