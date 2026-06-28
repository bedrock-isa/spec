`timescale 1ns/1ps
`default_nettype none

module bedrock_full_decode
  import bedrock_pkg::*;
  import bedrock_decode_pkg::*;
  import bedrock_prefix_decode_pkg::*;
  import bedrock_ea_decode_pkg::*;
  import bedrock_agu_pkg::*;
(
  input  logic [MAX_INSTRUCTION_WORDS*WORD_BITS-1:0] words_i,

  output logic                      valid_o,
  output logic                      prefix_present_o,
  output logic                      prefix_valid_o,
  output logic                      decode_valid_o,
  output logic                      undersized_o,
  output instruction_length_t       length_words_o,
  output logic [3:0]                required_words_o,

  output bedrock_opcode_id_e        opcode_id_o,
  output bedrock_field_format_id_e  field_format_id_o,
  output bedrock_ext_root_e         ext_root_o,
  output logic                      needs_extension_o,

  output logic                      nospec_o,
  output logic                      saturate_o,
  output logic                      nontemporal_o,
  output bedrock_update_mode_e      update_mode_o,
  output bedrock_access_mode_e      access_mode_o,
  output bedrock_repeat_kind_e      repeat_kind_o,
  output logic [3:0]                repeat_condition_o,
  output logic [2:0]                repeat_counter_o,
  output logic                      end_group_o,
  output logic                      repg_fast_candidate_o,
  output logic                      repcc_valid_o,
  output logic                      repg_valid_o,
  output logic                      repeat_present_o,
  output logic                      repeat_valid_o,
  output logic                      repeat_invalid_o,

  output logic [1:0]                 ea_present_o,
  output logic [5:0]                 ea_value_o [2],
  output logic [3:0]                 ea_descriptor_token_o [2],
  output logic                       ea_valid_o [2],
  output logic                       ea_reserved_o [2],
  output logic                       ea_needs_descriptor_o [2],
  output bedrock_ea_form_e           ea_form_o [2],
  output logic                       ea_is_register_o [2],
  output logic                       ea_is_memory_o [2],
  output logic                       ea_is_immediate_o [2],
  output logic                       ea_update_eligible_o [2],
  output bedrock_ea_segment_e        ea_segment_o [2],
  output bedrock_ea_base_e           ea_base_o [2],
  output logic [2:0]                 ea_base_reg_o [2],
  output logic [2:0]                 ea_index_reg_o [2],
  output logic [1:0]                 ea_scale_log2_o [2],
  output logic [2:0]                 ea_payload_words_o [2],

  output bedrock_agu_request_t       agu_request_o [2]
);

  word_t word0;
  primary_payload_t primary_payload;
  word_t prefix_word;
  word_t extension_word;
  word_t token0_word;
  word_t token1_word;
  word_t token2_word;
  word_t token3_word;
  word_t token4_word;
  word_t token5_word;
  word_t token6_word;
  word_t token7_word;
  logic prefix_decode_valid;
  logic instruction_decode_valid;
  logic [3:0] decode_required_words;
  logic [3:0] field_token_words;
  logic [3:0] dynamic_required_words;
  logic [3:0] total_required_words;
  logic [3:0] ea_payload_words_sum;
  logic all_ea_valid;
  logic base_valid;
  logic [3:0] ea0_descriptor_token;
  logic [3:0] ea1_descriptor_token;
  word_t ea0_descriptor_word;
  word_t ea1_descriptor_word;
  logic ea_signed32_index_escape [2];
  logic ea_segment_selectable [2];
  logic ea_segment_valid [2];
  logic ea_has_base_reg [2];
  logic ea_has_index_reg [2];
  logic ea_has_displacement [2];
  logic ea_has_absolute [2];
  logic [2:0] ea_displacement_words [2];
  logic [2:0] ea0_payload_words;
  logic [2:0] ea1_payload_words;
  bedrock_decode_field_extract_t field_extract;

  function automatic word_t physical_word_at(input int unsigned index);
    if (index < MAX_INSTRUCTION_WORDS) begin
      physical_word_at = words_i[index*WORD_BITS +: WORD_BITS];
    end else begin
      physical_word_at = word_t'(16'h0000);
    end
  endfunction

  assign word0 = physical_word_at(0);
  assign prefix_present_o = word0_prefix_present(word0);
  assign length_words_o = word0_length_words(word0);
  assign primary_payload = word0_primary_payload(word0);
  assign prefix_word = prefix_present_o ? physical_word_at(1) : word_t'(16'h0000);
  assign token0_word = word0;
  assign token1_word = prefix_present_o ? physical_word_at(2) : physical_word_at(1);
  assign token2_word = prefix_present_o ? physical_word_at(3) : physical_word_at(2);
  assign token3_word = prefix_present_o ? physical_word_at(4) : physical_word_at(3);
  assign token4_word = prefix_present_o ? physical_word_at(5) : physical_word_at(4);
  assign token5_word = prefix_present_o ? physical_word_at(6) : physical_word_at(5);
  assign token6_word = prefix_present_o ? physical_word_at(7) : physical_word_at(6);
  assign token7_word = prefix_present_o ? physical_word_at(8) : physical_word_at(7);
  assign extension_word = token1_word;

  bedrock_prefix_decode prefix_decode (
    .prefix_word_i(prefix_word),
    .valid_o(prefix_decode_valid),
    .nospec_o(nospec_o),
    .saturate_o(saturate_o),
    .nontemporal_o(nontemporal_o),
    .update_mode_o(update_mode_o),
    .access_mode_o(access_mode_o),
    .repeat_kind_o(repeat_kind_o),
    .repeat_condition_o(repeat_condition_o),
    .repeat_counter_o(repeat_counter_o),
    .end_group_o(end_group_o)
  );

  bedrock_decode decode (
    .primary_payload_i(primary_payload),
    .extension_word_i(extension_word),
    .valid_o(instruction_decode_valid),
    .needs_extension_o(needs_extension_o),
    .opcode_id_o(opcode_id_o),
    .field_format_id_o(field_format_id_o),
    .required_words_o(decode_required_words),
    .ext_root_o(ext_root_o),
    .repg_fast_candidate_o(repg_fast_candidate_o)
  );

  assign field_extract = bedrock_decode_extract_fields(
    field_format_id_o,
    token0_word,
    token1_word,
    token2_word,
    token3_word,
    token4_word,
    token5_word,
    token6_word,
    token7_word
  );

  assign ea1_descriptor_word = bedrock_decode_ea1_descriptor_word(
    field_format_id_o,
    ea0_payload_words,
    token0_word,
    token1_word,
    token2_word,
    token3_word,
    token4_word,
    token5_word,
    token6_word,
    token7_word
  );

  assign ea_present_o = field_extract.ea_present;
  assign ea_value_o[0] = field_extract.ea_value[5:0];
  assign ea_value_o[1] = field_extract.ea_value[11:6];
  assign field_token_words = field_extract.token_words;
  assign ea0_descriptor_token = field_token_words;
  assign ea1_descriptor_token = field_token_words + {1'b0, ea0_payload_words};
  assign ea0_descriptor_word = field_extract.ea0_descriptor_word;
  assign ea_descriptor_token_o[0] = ea0_descriptor_token;
  assign ea_descriptor_token_o[1] = ea1_descriptor_token;
  assign ea_payload_words_o[0] = ea0_payload_words;
  assign ea_payload_words_o[1] = ea1_payload_words;

  bedrock_ea_decode ea0_decode (
    .ea_i(ea_value_o[0]),
    .descriptor_i(ea0_descriptor_word),
    .valid_o(ea_valid_o[0]),
    .reserved_o(ea_reserved_o[0]),
    .needs_descriptor_o(ea_needs_descriptor_o[0]),
    .form_o(ea_form_o[0]),
    .is_register_o(ea_is_register_o[0]),
    .is_memory_o(ea_is_memory_o[0]),
    .is_immediate_o(ea_is_immediate_o[0]),
    .update_eligible_o(ea_update_eligible_o[0]),
    .signed32_index_escape_o(ea_signed32_index_escape[0]),
    .segment_selectable_o(ea_segment_selectable[0]),
    .segment_valid_o(ea_segment_valid[0]),
    .has_base_reg_o(ea_has_base_reg[0]),
    .has_index_reg_o(ea_has_index_reg[0]),
    .has_displacement_o(ea_has_displacement[0]),
    .has_absolute_o(ea_has_absolute[0]),
    .segment_o(ea_segment_o[0]),
    .base_o(ea_base_o[0]),
    .base_reg_o(ea_base_reg_o[0]),
    .index_reg_o(ea_index_reg_o[0]),
    .scale_log2_o(ea_scale_log2_o[0]),
    .displacement_words_o(ea_displacement_words[0]),
    .payload_words_o(ea0_payload_words)
  );

  bedrock_ea_decode ea1_decode (
    .ea_i(ea_value_o[1]),
    .descriptor_i(ea1_descriptor_word),
    .valid_o(ea_valid_o[1]),
    .reserved_o(ea_reserved_o[1]),
    .needs_descriptor_o(ea_needs_descriptor_o[1]),
    .form_o(ea_form_o[1]),
    .is_register_o(ea_is_register_o[1]),
    .is_memory_o(ea_is_memory_o[1]),
    .is_immediate_o(ea_is_immediate_o[1]),
    .update_eligible_o(ea_update_eligible_o[1]),
    .signed32_index_escape_o(ea_signed32_index_escape[1]),
    .segment_selectable_o(ea_segment_selectable[1]),
    .segment_valid_o(ea_segment_valid[1]),
    .has_base_reg_o(ea_has_base_reg[1]),
    .has_index_reg_o(ea_has_index_reg[1]),
    .has_displacement_o(ea_has_displacement[1]),
    .has_absolute_o(ea_has_absolute[1]),
    .segment_o(ea_segment_o[1]),
    .base_o(ea_base_o[1]),
    .base_reg_o(ea_base_reg_o[1]),
    .index_reg_o(ea_index_reg_o[1]),
    .scale_log2_o(ea_scale_log2_o[1]),
    .displacement_words_o(ea_displacement_words[1]),
    .payload_words_o(ea1_payload_words)
  );

  bedrock_agu_request_build agu0_request (
    .ea_present_i(ea_present_o[0]),
    .ea_value_i(ea_value_o[0]),
    .descriptor_token_i(ea_descriptor_token_o[0]),
    .ea_valid_i(ea_valid_o[0]),
    .ea_reserved_i(ea_reserved_o[0]),
    .ea_needs_descriptor_i(ea_needs_descriptor_o[0]),
    .ea_form_i(ea_form_o[0]),
    .ea_is_register_i(ea_is_register_o[0]),
    .ea_is_memory_i(ea_is_memory_o[0]),
    .ea_is_immediate_i(ea_is_immediate_o[0]),
    .ea_update_eligible_i(ea_update_eligible_o[0]),
    .ea_signed32_index_escape_i(ea_signed32_index_escape[0]),
    .ea_segment_selectable_i(ea_segment_selectable[0]),
    .ea_segment_valid_i(ea_segment_valid[0]),
    .ea_has_base_reg_i(ea_has_base_reg[0]),
    .ea_has_index_reg_i(ea_has_index_reg[0]),
    .ea_has_displacement_i(ea_has_displacement[0]),
    .ea_has_absolute_i(ea_has_absolute[0]),
    .ea_segment_i(ea_segment_o[0]),
    .ea_base_i(ea_base_o[0]),
    .ea_base_reg_i(ea_base_reg_o[0]),
    .ea_index_reg_i(ea_index_reg_o[0]),
    .ea_scale_log2_i(ea_scale_log2_o[0]),
    .ea_displacement_words_i(ea_displacement_words[0]),
    .ea_payload_words_i(ea0_payload_words),
    .update_mode_i(update_mode_o),
    .request_o(agu_request_o[0])
  );

  bedrock_agu_request_build agu1_request (
    .ea_present_i(ea_present_o[1]),
    .ea_value_i(ea_value_o[1]),
    .descriptor_token_i(ea_descriptor_token_o[1]),
    .ea_valid_i(ea_valid_o[1]),
    .ea_reserved_i(ea_reserved_o[1]),
    .ea_needs_descriptor_i(ea_needs_descriptor_o[1]),
    .ea_form_i(ea_form_o[1]),
    .ea_is_register_i(ea_is_register_o[1]),
    .ea_is_memory_i(ea_is_memory_o[1]),
    .ea_is_immediate_i(ea_is_immediate_o[1]),
    .ea_update_eligible_i(ea_update_eligible_o[1]),
    .ea_signed32_index_escape_i(ea_signed32_index_escape[1]),
    .ea_segment_selectable_i(ea_segment_selectable[1]),
    .ea_segment_valid_i(ea_segment_valid[1]),
    .ea_has_base_reg_i(ea_has_base_reg[1]),
    .ea_has_index_reg_i(ea_has_index_reg[1]),
    .ea_has_displacement_i(ea_has_displacement[1]),
    .ea_has_absolute_i(ea_has_absolute[1]),
    .ea_segment_i(ea_segment_o[1]),
    .ea_base_i(ea_base_o[1]),
    .ea_base_reg_i(ea_base_reg_o[1]),
    .ea_index_reg_i(ea_index_reg_o[1]),
    .ea_scale_log2_i(ea_scale_log2_o[1]),
    .ea_displacement_words_i(ea_displacement_words[1]),
    .ea_payload_words_i(ea1_payload_words),
    .update_mode_i(update_mode_o),
    .request_o(agu_request_o[1])
  );

  assign prefix_valid_o = !prefix_present_o || prefix_decode_valid;
  assign decode_valid_o = instruction_decode_valid;
  assign repeat_present_o = prefix_present_o && (repeat_kind_o != BR_REPEAT_NONE);
  assign repcc_valid_o = base_valid && (repeat_kind_o == BR_REPEAT_REPCC);
  assign repg_valid_o = base_valid && (repeat_kind_o == BR_REPEAT_REPG);
  assign repeat_valid_o = !repeat_present_o || repcc_valid_o || repg_valid_o;
  assign repeat_invalid_o = repeat_present_o && !repeat_valid_o;
  assign all_ea_valid =
    (!ea_present_o[0] || (ea_valid_o[0] && !ea_reserved_o[0]))
    && (!ea_present_o[1] || (ea_valid_o[1] && !ea_reserved_o[1]));
  assign ea_payload_words_sum =
    (ea_present_o[0] ? {1'b0, ea0_payload_words} : 4'd0)
    + (ea_present_o[1] ? {1'b0, ea1_payload_words} : 4'd0);
  assign dynamic_required_words =
    ((field_token_words + ea_payload_words_sum) > decode_required_words)
      ? (field_token_words + ea_payload_words_sum)
      : decode_required_words;
  assign total_required_words = dynamic_required_words + (prefix_present_o ? 4'd1 : 4'd0);
  assign required_words_o = total_required_words;
  assign undersized_o = length_words_o < total_required_words;
  assign base_valid =
    prefix_valid_o
    && decode_valid_o
    && all_ea_valid
    && !undersized_o;
  assign valid_o = base_valid && !repeat_invalid_o;
endmodule

`default_nettype wire
