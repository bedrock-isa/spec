// Generated from canonical Bedrock ISA definitions. Do not edit.
package bedrock_vector_geometry_pkg;
  localparam integer BEDROCK_VECTOR_REGISTER_COUNT = 32;
  localparam integer BEDROCK_PREDICATE_REGISTER_COUNT = 16;
  typedef enum logic [2:0] {
    VECTOR_PERMUTE_ZIP_LO,
    VECTOR_PERMUTE_ZIP_HI,
    VECTOR_PERMUTE_UNZIP_LO,
    VECTOR_PERMUTE_UNZIP_HI,
    VECTOR_PERMUTE_TRANSPOSE_LO,
    VECTOR_PERMUTE_TRANSPOSE_HI
  } bedrock_vector_permute_e;

  function automatic integer bedrock_vector_lane_count(
    input integer vlen_bits,
    input integer element_bytes
  );
    bedrock_vector_lane_count = vlen_bits / (8 * element_bytes);
  endfunction

  function automatic integer bedrock_predicate_bit_index(
    input integer lane,
    input integer element_bytes
  );
    bedrock_predicate_bit_index = lane * element_bytes;
  endfunction
endpackage
