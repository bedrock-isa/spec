`timescale 1ns/1ps
`default_nettype none

module bedrock_prefix_decode_synth(
  input  [15:0] prefix_word_i,
  output reg        valid_o,
  output reg        nospec_o,
  output reg        saturate_o,
  output reg        nontemporal_o,
  output reg [2:0]  update_mode_o,
  output reg [1:0]  access_mode_o,
  output reg [1:0]  repeat_kind_o,
  output reg [3:0]  repeat_condition_o,
  output reg [2:0]  repeat_counter_o
);
  task automatic apply_prefix(input [7:0] p);
    begin
      casez (p)
@PREFIX_SYNTH_APPLY_CASES@
        default: valid_o = 1'b0;
      endcase
    end
  endtask
  always @* begin
    valid_o = 1'b1;
    nospec_o = 1'b0;
    saturate_o = 1'b0;
    nontemporal_o = 1'b0;
    update_mode_o = 3'd0;
    access_mode_o = 2'd0;
    repeat_kind_o = 2'd0;
    repeat_condition_o = 4'd0;
    repeat_counter_o = 3'd0;
    apply_prefix(prefix_word_i[7:0]);
    apply_prefix(prefix_word_i[15:8]);
  end
endmodule

`default_nettype wire
