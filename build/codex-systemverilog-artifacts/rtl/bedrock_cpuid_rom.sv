// Generated from canonical Bedrock ISA definitions. Do not edit.
module bedrock_cpuid_rom #(
  parameter integer ENTRY_COUNT = 1,
  parameter logic [63:0] ENTRY_SELECTOR [ENTRY_COUNT] = '{default: 64'h0},
  parameter logic [63:0] ENTRY_MASK [ENTRY_COUNT] = '{default: 64'hffffffffffffffff},
  parameter logic [63:0] ENTRY_DATA [ENTRY_COUNT] = '{default: 64'h0}
) (
  input  logic [63:0] selector_i,
  output logic        valid_o,
  output logic [63:0] data_o
);
  integer entry;
  always_comb begin
    valid_o = 1'b0;
    data_o = '0;
    for (entry = 0; entry < ENTRY_COUNT; entry = entry + 1) begin
      if (!valid_o &&
          ((selector_i & ENTRY_MASK[entry]) ==
           (ENTRY_SELECTOR[entry] & ENTRY_MASK[entry]))) begin
        valid_o = 1'b1;
        data_o = ENTRY_DATA[entry];
      end
    end
  end
endmodule
