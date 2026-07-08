`timescale 1ns/1ps
`default_nettype none

module prefix_ea_tb;
import bedrock_prefix_decode_pkg::*;
import bedrock_ea_decode_pkg::*;

  logic [15:0] prefix_word;
  logic prefix_valid;
  logic nospec;
  logic saturate;
  logic nontemporal;
  bedrock_update_mode_e update_mode;
  bedrock_access_mode_e access_mode;
  bedrock_repeat_kind_e repeat_kind;
  logic [3:0] repeat_condition;
  logic [2:0] repeat_counter;
  logic end_group;

  logic [5:0] ea;
  logic [15:0] descriptor;
  logic ea_valid;
  logic ea_reserved;
  logic needs_descriptor;
  bedrock_ea_form_e ea_form;
  logic is_register;
  logic is_memory;
  logic is_immediate;
  logic update_eligible;
  logic signed32_index_escape;
  logic segment_selectable;
  logic segment_valid;
  logic has_base_reg;
  logic has_index_reg;
  logic has_displacement;
  logic has_absolute;
  bedrock_ea_segment_e segment;
  bedrock_ea_base_e base;
  logic [2:0] base_reg;
  logic [2:0] index_reg;
  logic [1:0] scale_log2;
  logic [2:0] displacement_words;
  logic [2:0] payload_words;
  int failures;

  bedrock_prefix_decode prefix_dut (
                          .prefix_word_i(prefix_word),
                          .valid_o(prefix_valid),
                          .nospec_o(nospec),
                          .saturate_o(saturate),
                          .nontemporal_o(nontemporal),
                          .update_mode_o(update_mode),
                          .access_mode_o(access_mode),
                          .repeat_kind_o(repeat_kind),
                          .repeat_condition_o(repeat_condition),
                          .repeat_counter_o(repeat_counter),
                          .end_group_o(end_group)
                        );

  bedrock_ea_decode ea_dut (
                      .ea_i(ea),
                      .descriptor_i(descriptor),
                      .valid_o(ea_valid),
                      .reserved_o(ea_reserved),
                      .needs_descriptor_o(needs_descriptor),
                      .form_o(ea_form),
                      .is_register_o(is_register),
                      .is_memory_o(is_memory),
                      .is_immediate_o(is_immediate),
                      .update_eligible_o(update_eligible),
                      .signed32_index_escape_o(signed32_index_escape),
                      .segment_selectable_o(segment_selectable),
                      .segment_valid_o(segment_valid),
                      .has_base_reg_o(has_base_reg),
                      .has_index_reg_o(has_index_reg),
                      .has_displacement_o(has_displacement),
                      .has_absolute_o(has_absolute),
                      .segment_o(segment),
                      .base_o(base),
                      .base_reg_o(base_reg),
                      .index_reg_o(index_reg),
                      .scale_log2_o(scale_log2),
                      .displacement_words_o(displacement_words),
                      .payload_words_o(payload_words)
                    );


  task automatic expect_prefix(
      input logic expected_valid,
      input logic expected_nospec,
      input logic expected_saturate,
      input bedrock_update_mode_e expected_update,
      input bedrock_access_mode_e expected_access,
      input bedrock_repeat_kind_e expected_repeat,
      input logic [3:0] expected_condition,
      input logic [2:0] expected_counter,
      input logic expected_end_group
    );
    begin
      #1;
      if (prefix_valid !== expected_valid)
      begin
        $error("prefix %04h valid got %0b expected %0b", prefix_word, prefix_valid, expected_valid);
        failures++;
      end
      if (nospec !== expected_nospec)
      begin
        $error("prefix %04h nospec got %0b expected %0b", prefix_word, nospec, expected_nospec);
        failures++;
      end
      if (saturate !== expected_saturate)
      begin
        $error("prefix %04h saturate got %0b expected %0b", prefix_word, saturate, expected_saturate);
        failures++;
      end
      if (update_mode !== expected_update)
      begin
        $error("prefix %04h update got %0d expected %0d", prefix_word, update_mode, expected_update);
        failures++;
      end
      if (access_mode !== expected_access)
      begin
        $error("prefix %04h access got %0d expected %0d", prefix_word, access_mode, expected_access);
        failures++;
      end
      if (repeat_kind !== expected_repeat)
      begin
        $error("prefix %04h repeat got %0d expected %0d", prefix_word, repeat_kind, expected_repeat);
        failures++;
      end
      if (repeat_condition !== expected_condition)
      begin
        $error("prefix %04h condition got %0d expected %0d", prefix_word, repeat_condition, expected_condition);
        failures++;
      end
      if (repeat_counter !== expected_counter)
      begin
        $error("prefix %04h counter got %0d expected %0d", prefix_word, repeat_counter, expected_counter);
        failures++;
      end
      if (end_group !== expected_end_group)
      begin
        $error("prefix %04h end_group got %0b expected %0b", prefix_word, end_group, expected_end_group);
        failures++;
      end
    end
  endtask

  task automatic expect_ea(
      input logic expected_valid,
      input logic expected_reserved,
      input bedrock_ea_form_e expected_form,
      input bedrock_ea_base_e expected_base,
      input bedrock_ea_segment_e expected_segment,
      input logic [2:0] expected_base_reg,
      input logic [2:0] expected_index_reg,
      input logic [1:0] expected_scale,
      input logic [2:0] expected_payload_words
    );
    begin
      #1;
      if (ea_valid !== expected_valid)
      begin
        $error("ea %02h desc %04h valid got %0b expected %0b", ea, descriptor, ea_valid, expected_valid);
        failures++;
      end
      if (ea_reserved !== expected_reserved)
      begin
        $error("ea %02h desc %04h reserved got %0b expected %0b", ea, descriptor, ea_reserved, expected_reserved);
        failures++;
      end
      if (ea_form !== expected_form)
      begin
        $error("ea %02h desc %04h form got %0d expected %0d", ea, descriptor, ea_form, expected_form);
        failures++;
      end
      if (base !== expected_base)
      begin
        $error("ea %02h desc %04h base got %0d expected %0d", ea, descriptor, base, expected_base);
        failures++;
      end
      if (segment !== expected_segment)
      begin
        $error("ea %02h desc %04h segment got %0d expected %0d", ea, descriptor, segment, expected_segment);
        failures++;
      end
      if (base_reg !== expected_base_reg)
      begin
        $error("ea %02h desc %04h base_reg got %0d expected %0d", ea, descriptor, base_reg, expected_base_reg);
        failures++;
      end
      if (index_reg !== expected_index_reg)
      begin
        $error("ea %02h desc %04h index_reg got %0d expected %0d", ea, descriptor, index_reg, expected_index_reg);
        failures++;
      end
      if (scale_log2 !== expected_scale)
      begin
        $error("ea %02h desc %04h scale got %0d expected %0d", ea, descriptor, scale_log2, expected_scale);
        failures++;
      end
      if (payload_words !== expected_payload_words)
      begin
        $error("ea %02h desc %04h payload_words got %0d expected %0d", ea, descriptor, payload_words, expected_payload_words);
        failures++;
      end
    end
  endtask

  initial
  begin
    failures = 0;

    prefix_word = 16'h0000;
    expect_prefix(1'b1, 1'b0, 1'b0, BR_UPDATE_NONE, BR_ACCESS_C, BR_REPEAT_NONE, 4'd0, 3'd0, 1'b0);

    prefix_word = 16'h0201;
    expect_prefix(1'b1, 1'b1, 1'b1, BR_UPDATE_NONE, BR_ACCESS_C, BR_REPEAT_NONE, 4'd0, 3'd0, 1'b0);

    prefix_word = 16'h0604;
    expect_prefix(1'b1, 1'b0, 1'b0, BR_UPDATE_POSTDEC, BR_ACCESS_C, BR_REPEAT_NONE, 4'd0, 3'd0, 1'b0);

    prefix_word = 16'h008d;
    expect_prefix(1'b1, 1'b0, 1'b0, BR_UPDATE_NONE, BR_ACCESS_C, BR_REPEAT_REPCC, 4'd1, 3'd5, 1'b0);

    prefix_word = 16'h0073;
    expect_prefix(1'b1, 1'b0, 1'b0, BR_UPDATE_NONE, BR_ACCESS_C, BR_REPEAT_REPG, 4'd0, 3'd3, 1'b0);

    prefix_word = 16'h0078;
    expect_prefix(1'b1, 1'b0, 1'b0, BR_UPDATE_NONE, BR_ACCESS_C, BR_REPEAT_NONE, 4'd0, 3'd0, 1'b1);

    prefix_word = 16'h6900;
    expect_prefix(1'b0, 1'b0, 1'b0, BR_UPDATE_NONE, BR_ACCESS_C, BR_REPEAT_NONE, 4'd0, 3'd0, 1'b0);

    prefix_word = 16'h0008;
    expect_prefix(1'b1, 1'b0, 1'b0, BR_UPDATE_NONE, BR_ACCESS_U2C, BR_REPEAT_NONE, 4'd0, 3'd0, 1'b0);

    descriptor = 16'h0000;
    ea = 6'h05;
    expect_ea(1'b1, 1'b0, BR_EA_DREG, BR_EA_BASE_D, BR_EA_SEG_DS, 3'd5, 3'd0, 2'd0, 3'd0);

    ea = 6'h1a;
    expect_ea(1'b1, 1'b0, BR_EA_A_DISP16, BR_EA_BASE_A, BR_EA_SEG_DS, 3'd2, 3'd0, 2'd0, 3'd1);

    ea = 6'h32;
    expect_ea(1'b1, 1'b0, BR_EA_IMM16, BR_EA_BASE_IMM, BR_EA_SEG_DS, 3'd0, 3'd0, 2'd0, 3'd1);

    ea = 6'h2b;
    expect_ea(1'b0, 1'b1, BR_EA_INVALID, BR_EA_BASE_NONE, BR_EA_SEG_CS, 3'd0, 3'd0, 2'd0, 3'd0);

    ea = 6'h3f;
    descriptor = 16'h01d2; // mode 0, DS, A6 + D4 * 4
    expect_ea(1'b1, 1'b0, BR_EA_SEG_A_INDEX, BR_EA_BASE_A, BR_EA_SEG_DS, 3'd6, 3'd4, 2'd2, 3'd1);

    ea = 6'h3e;
    descriptor = 16'h01d2; // S32 escape selects signed-32-indexed variant
    expect_ea(1'b1, 1'b0, BR_EA_S32_SEG_A_INDEX, BR_EA_BASE_A, BR_EA_SEG_DS, 3'd6, 3'd4, 2'd2, 3'd1);

    ea = 6'h3f;
    descriptor = 16'h4a12; // mode 9, nonzero segment field is reserved for SP-index form
    expect_ea(1'b0, 1'b0, BR_EA_SP_INDEX_DISP16, BR_EA_BASE_SP, BR_EA_SEG_SS, 3'd0, 3'd4, 2'd2, 3'd2);

    if (failures != 0)
    begin
      $fatal(1, "prefix_ea_tb failed with %0d failure(s)", failures);
    end
    $display("prefix_ea_tb PASS");
    $finish;
  end
endmodule

`default_nettype wire
