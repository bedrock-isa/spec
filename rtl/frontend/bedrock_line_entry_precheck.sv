`timescale 1ns/1ps
`default_nettype none

module bedrock_line_entry_precheck #(
  parameter int LINE_WORDS = 32
) (
  input  logic [LINE_WORDS*bedrock_pkg::WORD_BITS-1:0] line_i,
  output logic [LINE_WORDS-1:0]                        entry_valid_o,
  output logic [LINE_WORDS-1:0]                        prefix_valid_o,
  output logic [LINE_WORDS-1:0]                        decode_valid_o,
  output logic [LINE_WORDS-1:0]                        repeat_present_o,
  output logic [LINE_WORDS-1:0]                        end_group_o,
  output logic [LINE_WORDS-1:0]                        repcc_allowed_o,
  output logic [LINE_WORDS-1:0]                        repg_allowed_o,
  output logic [LINE_WORDS-1:0]                        repg_fast_candidate_o,
  output logic [LINE_WORDS-1:0]                        repcc_valid_o,
  output logic [LINE_WORDS-1:0]                        repg_valid_o,
  output logic [LINE_WORDS-1:0]                        repeat_valid_o,
  output logic [LINE_WORDS-1:0]                        repeat_invalid_o
);

  function automatic bedrock_pkg::word_t line_word_at(input int unsigned index);
    if (index < LINE_WORDS) begin
      line_word_at = line_i[index*bedrock_pkg::WORD_BITS +: bedrock_pkg::WORD_BITS];
    end else begin
      line_word_at = bedrock_pkg::word_t'(16'h0000);
    end
  endfunction

  for (genvar word_index = 0; word_index < LINE_WORDS; word_index++) begin : gen_entry
    localparam int PREFIX_INDEX = word_index + 1;
    localparam int EXT_NO_PREFIX_INDEX = word_index + 1;
    localparam int EXT_WITH_PREFIX_INDEX = word_index + 2;

    bedrock_pkg::word_t word0;
    bedrock_pkg::primary_payload_t primary_payload;
    bedrock_pkg::word_t prefix_word;
    bedrock_pkg::word_t extension_word;
    logic prefix_present;
    logic prefix_word_available;
    logic ext_no_prefix_available;
    logic ext_with_prefix_available;
    logic extension_word_available;
    logic decode_valid_raw;
    logic needs_extension;
    logic alias_form;
    bedrock_decode_pkg::bedrock_form_id_e form_id;
    bedrock_decode_pkg::bedrock_ext_root_e ext_root;
    logic prefix_valid_raw;
    logic repcc_allowed_raw;
    logic repg_allowed_raw;
    logic repg_fast_candidate_raw;
    logic nospec;
    logic saturate;
    logic nontemporal;
    bedrock_prefix_decode_pkg::bedrock_update_mode_e update_mode;
    bedrock_prefix_decode_pkg::bedrock_repeat_kind_e repeat_kind;
    logic [3:0] repeat_condition;
    logic [2:0] repeat_counter;

    assign word0 = line_word_at(word_index);
    assign prefix_present = bedrock_pkg::word0_prefix_present(word0);
    assign primary_payload = bedrock_pkg::word0_primary_payload(word0);
    assign prefix_word_available = (PREFIX_INDEX < LINE_WORDS);
    assign ext_no_prefix_available = (EXT_NO_PREFIX_INDEX < LINE_WORDS);
    assign ext_with_prefix_available = (EXT_WITH_PREFIX_INDEX < LINE_WORDS);
    assign prefix_word = prefix_present ? line_word_at(PREFIX_INDEX) : bedrock_pkg::word_t'(16'h0000);
    assign extension_word = prefix_present ? line_word_at(EXT_WITH_PREFIX_INDEX) : line_word_at(EXT_NO_PREFIX_INDEX);
    assign extension_word_available = prefix_present ? ext_with_prefix_available : ext_no_prefix_available;

    bedrock_prefix_decode prefix_decode (
      .prefix_word_i(prefix_word),
      .valid_o(prefix_valid_raw),
      .nospec_o(nospec),
      .saturate_o(saturate),
      .nontemporal_o(nontemporal),
      .update_mode_o(update_mode),
      .repeat_kind_o(repeat_kind),
      .repeat_condition_o(repeat_condition),
      .repeat_counter_o(repeat_counter),
      .end_group_o(end_group_o[word_index])
    );

    bedrock_decode decode (
      .primary_payload_i(primary_payload),
      .extension_word_i(extension_word),
      .valid_o(decode_valid_raw),
      .needs_extension_o(needs_extension),
      .alias_o(alias_form),
      .form_id_o(form_id),
      .ext_root_o(ext_root),
      .repcc_allowed_o(repcc_allowed_raw),
      .repg_allowed_o(repg_allowed_raw),
      .repg_fast_candidate_o(repg_fast_candidate_raw)
    );

    assign prefix_valid_o[word_index] = !prefix_present || (prefix_word_available && prefix_valid_raw);
    assign decode_valid_o[word_index] = decode_valid_raw && (!needs_extension || extension_word_available);
    assign entry_valid_o[word_index] = prefix_valid_o[word_index] && decode_valid_o[word_index];
    assign repcc_allowed_o[word_index] = entry_valid_o[word_index] && repcc_allowed_raw;
    assign repg_allowed_o[word_index] = entry_valid_o[word_index] && repg_allowed_raw;
    assign repg_fast_candidate_o[word_index] = entry_valid_o[word_index] && repg_fast_candidate_raw;
    assign repeat_present_o[word_index] = prefix_present && (repeat_kind != bedrock_prefix_decode_pkg::BR_REPEAT_NONE);
    assign repcc_valid_o[word_index] =
      entry_valid_o[word_index]
      && (repeat_kind == bedrock_prefix_decode_pkg::BR_REPEAT_REPCC)
      && repcc_allowed_o[word_index];
    assign repg_valid_o[word_index] =
      entry_valid_o[word_index]
      && (repeat_kind == bedrock_prefix_decode_pkg::BR_REPEAT_REPG)
      && repg_allowed_o[word_index];
    assign repeat_valid_o[word_index] =
      !repeat_present_o[word_index]
      || repcc_valid_o[word_index]
      || repg_valid_o[word_index];
    assign repeat_invalid_o[word_index] = repeat_present_o[word_index] && !repeat_valid_o[word_index];
  end
endmodule

`default_nettype wire
