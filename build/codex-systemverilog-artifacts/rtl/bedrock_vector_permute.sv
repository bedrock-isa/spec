// Generated from canonical Bedrock ISA definitions. Do not edit.
module bedrock_vector_permute
  import bedrock_vector_geometry_pkg::*;
#(
  parameter integer VLEN = 256
) (
  input  bedrock_vector_permute_e operation_i,
  input  logic [3:0] element_bytes_i,
  input  logic [VLEN-1:0] left_i,
  input  logic [VLEN-1:0] right_i,
  output logic valid_o,
  output logic [VLEN-1:0] result_o
);
  localparam integer VLEN_BYTES = VLEN / 8;
  integer output_byte;
  integer output_lane;
  integer lane_byte;
  integer lane_count;
  integer element_bytes;
  integer source_lane;
  integer source_byte;
  logic source_right;

  always_comb begin
    result_o = '0;
    element_bytes = {28'b0, element_bytes_i};
    output_lane = 0;
    lane_byte = 0;
    source_lane = 0;
    source_byte = 0;
    source_right = 1'b0;
    valid_o = (element_bytes == 1 || element_bytes == 2 ||
               element_bytes == 4 || element_bytes == 8);
    if (valid_o)
      valid_o = ((VLEN_BYTES % element_bytes) == 0);
    lane_count = valid_o ? VLEN_BYTES / element_bytes : 0;
    for (output_byte = 0; output_byte < VLEN_BYTES; output_byte = output_byte + 1) begin
      output_lane = valid_o ? output_byte / element_bytes : 0;
      lane_byte = valid_o ? output_byte % element_bytes : 0;
      source_lane = 0;
      source_right = 1'b0;
      if (valid_o) begin
        unique case (operation_i)
          VECTOR_PERMUTE_ZIP_LO: begin
            source_right = output_lane[0];
            source_lane = output_lane / 2;
          end
          VECTOR_PERMUTE_ZIP_HI: begin
            source_right = output_lane[0];
            source_lane = lane_count / 2 + output_lane / 2;
          end
          VECTOR_PERMUTE_UNZIP_LO: begin
            source_right = (2 * output_lane) >= lane_count;
            source_lane = (2 * output_lane) % lane_count;
          end
          VECTOR_PERMUTE_UNZIP_HI: begin
            source_right = (2 * output_lane + 1) >= lane_count;
            source_lane = (2 * output_lane + 1) % lane_count;
          end
          VECTOR_PERMUTE_TRANSPOSE_LO: begin
            source_right = output_lane >= lane_count / 2;
            source_lane = 2 * (output_lane % (lane_count / 2));
          end
          VECTOR_PERMUTE_TRANSPOSE_HI: begin
            source_right = output_lane >= lane_count / 2;
            source_lane = 2 * (output_lane % (lane_count / 2)) + 1;
          end
          default: valid_o = 1'b0;
        endcase
        source_byte = source_lane * element_bytes + lane_byte;
        if (valid_o && source_byte < VLEN_BYTES)
          result_o[output_byte*8 +: 8] = source_right
            ? right_i[source_byte*8 +: 8]
            : left_i[source_byte*8 +: 8];
      end
    end
  end
endmodule
