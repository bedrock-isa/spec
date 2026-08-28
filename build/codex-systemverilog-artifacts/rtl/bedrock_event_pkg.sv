// Generated from canonical Bedrock ISA definitions. Do not edit.
package bedrock_event_pkg;
  localparam integer BEDROCK_EVENT_PAYLOAD_KINDS = 15;
  typedef enum logic [1:0] {
    EVENT_FRAME_BASIC = 2'd0,
    EVENT_FRAME_ERROR = 2'd1,
    EVENT_FRAME_PAGE = 2'd2,
    EVENT_FRAME_AUXILIARY = 2'd3
  } bedrock_event_frame_type_e;
  typedef struct packed {
    logic [7:0] class_id;
    logic [23:0] selector;
  } bedrock_event_code_t;

  localparam logic [31:0] EVENT_BASE_DEBUG_TRACE = 32'h00000000;
  localparam logic [31:0] EVENT_BASE_BREAKPOINT = 32'h00000001;
  localparam logic [31:0] EVENT_BASE_PRIVILEGE_VIOLATION = 32'h00000002;
  localparam logic [31:0] EVENT_BASE_SYSTEM_CALL = 32'h00000003;
  localparam logic [31:0] EVENT_BASE_DIVIDE_BY_ZERO = 32'h00000004;
  localparam logic [31:0] EVENT_BASE_SIGNED_DIVIDE_OVERFLOW = 32'h00000005;
  localparam logic [31:0] EVENT_BASE_INVALID_OPCODE = 32'h00000010;
  localparam logic [31:0] EVENT_BASE_INVALID_ADDRESSING_FORM = 32'h00000011;
  localparam logic [31:0] EVENT_BASE_RESERVED_INSTRUCTION_ENCODING = 32'h00000012;
  localparam logic [31:0] EVENT_BASE_UNAVAILABLE_INSTRUCTION_EXTENSION = 32'h00000013;
  localparam logic [31:0] EVENT_BASE_EXPLICIT_ILLEGAL_INSTRUCTION = 32'h00000014;
  localparam logic [31:0] EVENT_BASE_TRUNCATED_INSTRUCTION = 32'h00000015;
  localparam logic [31:0] EVENT_BASE_INVALID_OPERAND_RELATION = 32'h00000016;
  localparam logic [31:0] EVENT_BASE_PAGE_NOT_PRESENT = 32'h00000020;
  localparam logic [31:0] EVENT_BASE_PAGE_PERMISSION_VIOLATION = 32'h00000021;
  localparam logic [31:0] EVENT_BASE_MALFORMED_PAGE_TABLE_ENTRY = 32'h00000022;
  localparam logic [31:0] EVENT_BASE_NONCANONICAL_ADDRESS = 32'h00000023;
  localparam logic [31:0] EVENT_BASE_SEGMENT_BOUNDS_VIOLATION = 32'h00000024;
  localparam logic [31:0] EVENT_BASE_ATOMIC_ALIGNMENT_FAULT = 32'h00000025;
  localparam logic [31:0] EVENT_BASE_MEMORY_TYPE_FAULT = 32'h00000026;
  localparam logic [31:0] EVENT_BASE_PHYSICAL_ADDRESS_FAULT = 32'h00000030;
  localparam logic [31:0] EVENT_BASE_MMIO_ALIGNMENT_FAULT = 32'h00000031;
  localparam logic [31:0] EVENT_BASE_UNSUPPORTED_MMIO_OPERATION = 32'h00000032;
  localparam logic [31:0] EVENT_BASE_INVALID_CONTROL_SELECTOR = 32'h00000040;
  localparam logic [31:0] EVENT_BASE_RESERVED_CONTROL_BITS = 32'h00000041;
  localparam logic [31:0] EVENT_BASE_INVALID_CONTROL_IMAGE = 32'h00000042;
  localparam logic [31:0] EVENT_BASE_INVALID_CONTROL_TRANSITION = 32'h00000043;
  localparam logic [31:0] EVENT_BASE_BUS_NO_RESPONDER = 32'h00000070;
  localparam logic [31:0] EVENT_BASE_BUS_ACCESS_DENIED = 32'h00000071;
  localparam logic [31:0] EVENT_BASE_BUS_TIMEOUT = 32'h00000072;
  localparam logic [31:0] EVENT_BASE_BUS_DATA_ERROR = 32'h00000073;
  localparam logic [31:0] EVENT_BASE_BUS_OTHER_ERROR = 32'h00000074;
  localparam logic [31:0] EVENT_BASE_EVENT_ENTRY_STATE_FAILURE = 32'h00000078;
  localparam logic [31:0] EVENT_BASE_EVENT_STACK_STATE_FAILURE = 32'h00000079;
  localparam logic [31:0] EVENT_BASE_EVENT_FRAME_ADDRESS_FAILURE = 32'h0000007a;
  localparam logic [31:0] EVENT_BASE_EVENT_FRAME_STORE_FAILURE = 32'h0000007b;
  localparam logic [31:0] EVENT_BASE_MACHINE_CHECK = 32'h0000007c;
  localparam logic [31:0] EVENT_FP_FLOATING_POINT_EXCEPTION = 32'h00000060;
  localparam logic [31:0] EVENT_VECTOR_VECTOR_LOOP_OFFSET_OUT_OF_RANGE = 32'h00000050;
  localparam logic [31:0] EVENT_VECTOR_VECTOR_LANE_INDEX_OUT_OF_RANGE = 32'h00000051;
  localparam logic [14:0] EVENT_PAYLOAD_ACCESS = 15'h1;
  localparam logic [14:0] EVENT_PAYLOAD_ACCESS_SIZE = 15'h2;
  localparam logic [14:0] EVENT_PAYLOAD_ATOMIC = 15'h4;
  localparam logic [14:0] EVENT_PAYLOAD_EVENT_AUX = 15'h8;
  localparam logic [14:0] EVENT_PAYLOAD_FAILED_EVENT_CODE = 15'h10;
  localparam logic [14:0] EVENT_PAYLOAD_FAULT_EA = 15'h20;
  localparam logic [14:0] EVENT_PAYLOAD_FAULT_LINEAR = 15'h40;
  localparam logic [14:0] EVENT_PAYLOAD_FP_EXCEPTION_FLAGS = 15'h80;
  localparam logic [14:0] EVENT_PAYLOAD_OPERAND = 15'h100;
  localparam logic [14:0] EVENT_PAYLOAD_PRECISE = 15'h200;
  localparam logic [14:0] EVENT_PAYLOAD_RETRY_SAFE = 15'h400;
  localparam logic [14:0] EVENT_PAYLOAD_SEVERITY = 15'h800;
  localparam logic [14:0] EVENT_PAYLOAD_SOURCE = 15'h1000;
  localparam logic [14:0] EVENT_PAYLOAD_USER_DOMAIN = 15'h2000;
  localparam logic [14:0] EVENT_PAYLOAD_WALK_LEVEL = 15'h4000;
endpackage
