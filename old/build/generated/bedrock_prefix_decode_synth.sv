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
        8'h00: begin end
        8'h01: nospec_o = 1'b1;
        8'h02: saturate_o = 1'b1;
        8'h03: nontemporal_o = 1'b1;
        8'h04: update_mode_o = 3'd1;
        8'h05: update_mode_o = 3'd2;
        8'h06: update_mode_o = 3'd3;
        8'h07: update_mode_o = 3'd4;
        8'h08: access_mode_o = 2'd1;
        8'h09: access_mode_o = 2'd2;
        8'h0a: access_mode_o = 2'd3;
        8'b1???_????: begin repeat_kind_o = 2'd1; repeat_condition_o = p[6:3]; repeat_counter_o = p[2:0]; end
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
