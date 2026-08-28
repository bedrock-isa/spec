// Generated from canonical Bedrock ISA definitions. Do not edit.
module bedrock_condition_eval (
  input  logic [3:0] condition_i,
  input  logic [3:0] flags_i,
  output logic       holds_o
);
  logic flag_z;
  logic flag_n;
  logic flag_c;
  logic flag_v;

  always_comb begin
    flag_z = flags_i[3];
    flag_n = flags_i[2];
    flag_c = flags_i[1];
    flag_v = flags_i[0];
    unique case (condition_i)
      4'h0: holds_o = 1'b1;
      4'h1: holds_o = 1'b0;
      4'h2: holds_o = flag_z;
      4'h3: holds_o = !flag_z;
      4'h4: holds_o = flag_c;
      4'h5: holds_o = !flag_c;
      4'h6: holds_o = flag_n;
      4'h7: holds_o = !flag_n;
      4'h8: holds_o = flag_v;
      4'h9: holds_o = !flag_v;
      4'ha: holds_o = flag_c || flag_z;
      4'hb: holds_o = !flag_c && !flag_z;
      4'hc: holds_o = flag_n != flag_v;
      4'hd: holds_o = flag_n == flag_v;
      4'he: holds_o = flag_z || (flag_n != flag_v);
      4'hf: holds_o = !flag_z && (flag_n == flag_v);
    endcase
  end
endmodule
