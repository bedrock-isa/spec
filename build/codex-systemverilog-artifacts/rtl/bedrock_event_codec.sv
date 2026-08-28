// Generated from canonical Bedrock ISA definitions. Do not edit.
module bedrock_event_codec
  import bedrock_event_pkg::*;
(
  input  logic [31:0] code_i,
  output logic        known_o,
  output bedrock_event_frame_type_e frame_o,
  output logic [BEDROCK_EVENT_PAYLOAD_KINDS-1:0] payload_mask_o
);
  always_comb begin
    known_o = 1'b1;
    frame_o = EVENT_FRAME_BASIC;
    payload_mask_o = '0;
    unique case (code_i)
      EVENT_BASE_DEBUG_TRACE: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_BREAKPOINT: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_PRIVILEGE_VIOLATION: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_SYSTEM_CALL: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_DIVIDE_BY_ZERO: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_SIGNED_DIVIDE_OVERFLOW: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_INVALID_OPCODE: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_INVALID_ADDRESSING_FORM: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_RESERVED_INSTRUCTION_ENCODING: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_UNAVAILABLE_INSTRUCTION_EXTENSION: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_EXPLICIT_ILLEGAL_INSTRUCTION: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_TRUNCATED_INSTRUCTION: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_INVALID_OPERAND_RELATION: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_PAGE_NOT_PRESENT: begin frame_o = EVENT_FRAME_PAGE; payload_mask_o = 15'h6167; end
      EVENT_BASE_PAGE_PERMISSION_VIOLATION: begin frame_o = EVENT_FRAME_PAGE; payload_mask_o = 15'h6167; end
      EVENT_BASE_MALFORMED_PAGE_TABLE_ENTRY: begin frame_o = EVENT_FRAME_PAGE; payload_mask_o = 15'h6167; end
      EVENT_BASE_NONCANONICAL_ADDRESS: begin frame_o = EVENT_FRAME_PAGE; payload_mask_o = 15'h2167; end
      EVENT_BASE_SEGMENT_BOUNDS_VIOLATION: begin frame_o = EVENT_FRAME_PAGE; payload_mask_o = 15'h2167; end
      EVENT_BASE_ATOMIC_ALIGNMENT_FAULT: begin frame_o = EVENT_FRAME_PAGE; payload_mask_o = 15'h2163; end
      EVENT_BASE_MEMORY_TYPE_FAULT: begin frame_o = EVENT_FRAME_PAGE; payload_mask_o = 15'h6167; end
      EVENT_BASE_PHYSICAL_ADDRESS_FAULT: begin frame_o = EVENT_FRAME_PAGE; payload_mask_o = 15'h2167; end
      EVENT_BASE_MMIO_ALIGNMENT_FAULT: begin frame_o = EVENT_FRAME_PAGE; payload_mask_o = 15'h2167; end
      EVENT_BASE_UNSUPPORTED_MMIO_OPERATION: begin frame_o = EVENT_FRAME_PAGE; payload_mask_o = 15'h2167; end
      EVENT_BASE_INVALID_CONTROL_SELECTOR: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_RESERVED_CONTROL_BITS: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_INVALID_CONTROL_IMAGE: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_INVALID_CONTROL_TRANSITION: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_BASE_BUS_NO_RESPONDER: begin frame_o = EVENT_FRAME_AUXILIARY; payload_mask_o = 15'h656f; end
      EVENT_BASE_BUS_ACCESS_DENIED: begin frame_o = EVENT_FRAME_AUXILIARY; payload_mask_o = 15'h656f; end
      EVENT_BASE_BUS_TIMEOUT: begin frame_o = EVENT_FRAME_AUXILIARY; payload_mask_o = 15'h656f; end
      EVENT_BASE_BUS_DATA_ERROR: begin frame_o = EVENT_FRAME_AUXILIARY; payload_mask_o = 15'h656f; end
      EVENT_BASE_BUS_OTHER_ERROR: begin frame_o = EVENT_FRAME_AUXILIARY; payload_mask_o = 15'h656f; end
      EVENT_BASE_EVENT_ENTRY_STATE_FAILURE: begin frame_o = EVENT_FRAME_AUXILIARY; payload_mask_o = 15'h10; end
      EVENT_BASE_EVENT_STACK_STATE_FAILURE: begin frame_o = EVENT_FRAME_AUXILIARY; payload_mask_o = 15'h10; end
      EVENT_BASE_EVENT_FRAME_ADDRESS_FAILURE: begin frame_o = EVENT_FRAME_AUXILIARY; payload_mask_o = 15'h70; end
      EVENT_BASE_EVENT_FRAME_STORE_FAILURE: begin frame_o = EVENT_FRAME_AUXILIARY; payload_mask_o = 15'h70; end
      EVENT_BASE_MACHINE_CHECK: begin frame_o = EVENT_FRAME_AUXILIARY; payload_mask_o = 15'h1e68; end
      EVENT_FP_FLOATING_POINT_EXCEPTION: begin frame_o = EVENT_FRAME_ERROR; payload_mask_o = 15'h80; end
      EVENT_VECTOR_VECTOR_LOOP_OFFSET_OUT_OF_RANGE: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      EVENT_VECTOR_VECTOR_LANE_INDEX_OUT_OF_RANGE: begin frame_o = EVENT_FRAME_BASIC; payload_mask_o = 15'h0; end
      default: begin
        unique case (code_i[31:24])
      8'h01: frame_o = EVENT_FRAME_BASIC;
      8'h02: frame_o = EVENT_FRAME_BASIC;
          default: known_o = 1'b0;
        endcase
      end
    endcase
  end
endmodule
