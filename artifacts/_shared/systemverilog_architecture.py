"""SystemVerilog projections for non-decoder architectural contracts."""

from __future__ import annotations

from dataclasses import dataclass
import re

from engine.generation import (
    ArtifactGenerationContext,
    ArtifactGenerator,
    GeneratedArtifact,
    GeneratedArtifactSet,
)


def _identifier(value: object) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_").upper()
    if not text:
        raise ValueError(f"cannot form a SystemVerilog identifier from {value!r}")
    return f"N_{text}" if text[0].isdigit() else text


def _mask(lsb: int, bits: int) -> int:
    return ((1 << bits) - 1) << lsb


def _generated(body: str) -> str:
    return (
        "// Generated from canonical Bedrock ISA definitions. Do not edit.\n"
        + body.rstrip()
        + "\n"
    )


@dataclass(frozen=True)
class CpuidFieldProjection:
    id: str
    lsb: int
    bits: int
    mask: int


@dataclass(frozen=True)
class CpuidQueryProjection:
    owner: str
    class_id: str
    class_value: int
    leaf_id: str
    leaf_value: int
    query_id: str
    first_index: int
    last_index: int
    stride: int
    fields: tuple[CpuidFieldProjection, ...]


@dataclass(frozen=True)
class CpuidProjection:
    queries: tuple[CpuidQueryProjection, ...]


@dataclass(frozen=True)
class FixedEventRouteProjection:
    owner: str
    event_id: str
    code: int
    frame: str
    payload_mask: int


@dataclass(frozen=True)
class DynamicEventRouteProjection:
    class_value: int
    frame: str


@dataclass(frozen=True)
class EventCodecProjection:
    payload_bits: tuple[tuple[str, int], ...]
    fixed_routes: tuple[FixedEventRouteProjection, ...]
    dynamic_routes: tuple[DynamicEventRouteProjection, ...]


@dataclass(frozen=True)
class RegisterFieldProjection:
    id: str
    lsb: int
    mask: int


@dataclass(frozen=True)
class RegisterContractProjection:
    owner: str
    group_id: str
    group_index: int
    register_id: str
    encoding: int
    width_kind: int
    fixed_width: int
    writable_mask: int
    reset_known: bool
    reset_value: int
    fields: tuple[RegisterFieldProjection, ...]


@dataclass(frozen=True)
class RegisterContractsProjection:
    group_names: tuple[str, ...]
    registers: tuple[RegisterContractProjection, ...]


@dataclass(frozen=True)
class VectorGeometryProjection:
    vector_register_count: int
    predicate_register_count: int


class _Generator(ArtifactGenerator):
    def _outputs(self, contents: dict[str, str]) -> GeneratedArtifactSet:
        declared = self.definition.outputs
        if set(declared) != set(contents):
            raise ValueError(
                f"{self.definition.source}: declared output roles {sorted(declared)} do not "
                f"match rendered output roles {sorted(contents)}"
            )
        return GeneratedArtifactSet(
            tuple(
                GeneratedArtifact(declared[role], _generated(content))
                for role, content in contents.items()
            ),
            self.artifact_id,
        )


class ConditionEvaluatorGenerator(_Generator):
    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        context.require_provider("isa")
        body = """module bedrock_condition_eval (
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
endmodule"""
        return self._outputs({"evaluator": body})


class CpuidGenerator(_Generator):
    def project(self, context: ArtifactGenerationContext) -> CpuidProjection:
        project = context.require_provider("isa")
        queries = []
        for owner, namespace in project.cpuid.namespaces.items():
            for cpuid_class in namespace.classes.values():
                for leaf in cpuid_class.leaves.values():
                    resolved = project.cpuid.resolve_leaf(leaf)
                    for query in leaf.queries:
                        queries.append(
                            CpuidQueryProjection(
                                owner=owner,
                                class_id=cpuid_class.id,
                                class_value=resolved.class_value,
                                leaf_id=leaf.id,
                                leaf_value=resolved.leaf_value,
                                query_id=query.id,
                                first_index=query.indexes.first,
                                last_index=query.indexes.last,
                                stride=query.indexes.stride,
                                fields=tuple(
                                    CpuidFieldProjection(
                                        field.id,
                                        field.lsb,
                                        field.bits,
                                        _mask(field.lsb, field.bits),
                                    )
                                    for field in query.fields
                                ),
                            )
                        )
        return CpuidProjection(tuple(queries))

    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        constants: list[str] = []
        class_constants: set[tuple[str, str]] = set()
        leaf_constants: set[tuple[str, str, str]] = set()
        for query in self.project(context).queries:
            prefix = f"CPUID_{_identifier(query.owner)}_{_identifier(query.class_id)}"
            class_key = (query.owner, query.class_id)
            if class_key not in class_constants:
                class_constants.add(class_key)
                constants.append(
                    f"  localparam logic [31:0] {prefix}_CLASS = 32'h{query.class_value:08x};"
                )
            leaf_prefix = f"{prefix}_{_identifier(query.leaf_id)}"
            leaf_key = (query.owner, query.class_id, query.leaf_id)
            if leaf_key not in leaf_constants:
                leaf_constants.add(leaf_key)
                constants.append(
                    f"  localparam logic [15:0] {leaf_prefix}_LEAF = 16'h{query.leaf_value:04x};"
                )
            query_prefix = f"{leaf_prefix}_{_identifier(query.query_id)}"
            constants.extend(
                (
                    f"  localparam logic [15:0] {query_prefix}_FIRST = 16'h{query.first_index:04x};",
                    f"  localparam logic [15:0] {query_prefix}_LAST = 16'h{query.last_index:04x};",
                    f"  localparam logic [15:0] {query_prefix}_STRIDE = 16'd{query.stride};",
                )
            )
            for field in query.fields:
                field_prefix = f"{query_prefix}_{_identifier(field.id)}"
                constants.extend(
                    (
                        f"  localparam logic [6:0] {field_prefix}_LSB = 7'd{field.lsb};",
                        f"  localparam logic [6:0] {field_prefix}_BITS = 7'd{field.bits};",
                        f"  localparam logic [63:0] {field_prefix}_MASK = 64'h{field.mask:016x};",
                    )
                )

        package = (
            """package bedrock_cpuid_pkg;
  typedef struct packed {
    logic [31:0] class_id;
    logic [15:0] leaf_id;
    logic [15:0] index;
  } bedrock_cpuid_selector_t;

"""
            + "\n".join(constants)
            + "\nendpackage"
        )

        rom = """module bedrock_cpuid_rom #(
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
endmodule"""
        return self._outputs({"package": package, "rom": rom})


_FRAME_VALUES = {
    "basic": (0, 8),
    "error": (1, 10),
    "page": (2, 12),
    "auxiliary": (3, 12),
}


class EventCodecGenerator(_Generator):
    def project(self, context: ArtifactGenerationContext) -> EventCodecProjection:
        project = context.require_provider("isa")
        resolved = project.events.resolved_events()
        payload_names = sorted(
            {name for item in resolved for name in item.event.payload}
        )
        payload_bits = {name: bit for bit, name in enumerate(payload_names)}
        class_frames: dict[int, str] = {}
        fixed_routes = []
        for item in resolved:
            if item.code.selector.kind != "fixed":
                class_frames.setdefault(item.code.class_value, item.event.frame)
            if item.code.value is None:
                continue
            fixed_routes.append(
                FixedEventRouteProjection(
                    item.owner,
                    item.event.id,
                    item.code.value,
                    item.event.frame,
                    sum(1 << payload_bits[value] for value in item.event.payload),
                )
            )
        return EventCodecProjection(
            tuple(payload_bits.items()),
            tuple(fixed_routes),
            tuple(
                DynamicEventRouteProjection(class_value, frame)
                for class_value, frame in sorted(class_frames.items())
            ),
        )

    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        projection = self.project(context)
        payload_bits = dict(projection.payload_bits)
        constants: list[str] = []
        cases: list[str] = []
        for route in projection.fixed_routes:
            constant = (
                f"EVENT_{_identifier(route.owner)}_{_identifier(route.event_id)}"
            )
            constants.append(
                f"  localparam logic [31:0] {constant} = 32'h{route.code:08x};"
            )
            cases.append(
                f"      {constant}: begin frame_o = "
                f"EVENT_FRAME_{_identifier(route.frame)}; payload_mask_o = "
                f"{max(1, len(payload_bits))}'h{route.payload_mask:x}; end"
            )
        for name, bit in payload_bits.items():
            constants.append(
                f"  localparam logic [{max(1, len(payload_bits)) - 1}:0] "
                f"EVENT_PAYLOAD_{_identifier(name)} = {max(1, len(payload_bits))}'h{1 << bit:x};"
            )
        enum_items = ",\n".join(
            f"    EVENT_FRAME_{_identifier(name)} = 2'd{value[0]}"
            for name, value in _FRAME_VALUES.items()
        )
        package = f"""package bedrock_event_pkg;
  localparam integer BEDROCK_EVENT_PAYLOAD_KINDS = {max(1, len(payload_bits))};
  typedef enum logic [1:0] {{
{enum_items}
  }} bedrock_event_frame_type_e;
  typedef struct packed {{
    logic [7:0] class_id;
    logic [23:0] selector;
  }} bedrock_event_code_t;

{chr(10).join(constants)}
endpackage"""

        dynamic_cases = "\n".join(
            f"      8'h{route.class_value:02x}: frame_o = "
            f"EVENT_FRAME_{_identifier(route.frame)};"
            for route in projection.dynamic_routes
        )
        codec = f"""module bedrock_event_codec
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
{chr(10).join(cases)}
      default: begin
        unique case (code_i[31:24])
{dynamic_cases}
          default: known_o = 1'b0;
        endcase
      end
    endcase
  end
endmodule"""

        frame = """module bedrock_event_frame
  import bedrock_event_pkg::*;
(
  input  bedrock_event_frame_type_e frame_type_i,
  input  logic saved_dfa_i,
  input  logic [3:0] flags_i,
  input  logic [15:0] status_i,
  input  logic [31:0] event_code_i,
  input  logic [63:0] saved_pc_i,
  input  logic [63:0] saved_sp_i,
  input  logic [63:0] saved_cs_i,
  input  logic [63:0] saved_ds_i,
  input  logic [63:0] saved_ss_i,
  input  logic [63:0] error_code_i,
  input  logic [63:0] fault_ea_i,
  input  logic [63:0] fault_linear_i,
  input  logic [63:0] event_aux_i,
  output logic [7:0] frame_slots_o,
  output logic [12*64-1:0] frame_o
);
  always_comb begin
    frame_o = '0;
    unique case (frame_type_i)
      EVENT_FRAME_BASIC:     frame_slots_o = 8;
      EVENT_FRAME_ERROR:     frame_slots_o = 10;
      EVENT_FRAME_PAGE,
      EVENT_FRAME_AUXILIARY: frame_slots_o = 12;
    endcase
    frame_o[0*64 +: 64] = {12'b0, status_i, flags_i, 19'b0,
                            saved_dfa_i, 2'b0, frame_type_i, frame_slots_o};
    frame_o[1*64 +: 64] = {32'b0, event_code_i};
    frame_o[2*64 +: 64] = saved_pc_i;
    frame_o[3*64 +: 64] = saved_sp_i;
    frame_o[4*64 +: 64] = saved_cs_i;
    frame_o[5*64 +: 64] = saved_ds_i;
    frame_o[6*64 +: 64] = saved_ss_i;
    frame_o[7*64 +: 64] = '0;
    if (frame_type_i != EVENT_FRAME_BASIC)
      frame_o[8*64 +: 64] = error_code_i;
    if (frame_type_i == EVENT_FRAME_PAGE ||
        frame_type_i == EVENT_FRAME_AUXILIARY) begin
      frame_o[9*64 +: 64] = fault_ea_i;
      frame_o[10*64 +: 64] = fault_linear_i;
      frame_o[11*64 +: 64] = event_aux_i;
    end
  end
endmodule"""
        return self._outputs(
            {
                "package": package,
                "codec": codec,
                "frame": frame,
            }
        )


def _register_width_kind(width: object) -> int:
    if isinstance(width, int):
        return 0
    if str(width).strip() == "VLEN":
        return 1
    if str(width).replace(" ", "") == "VLEN/8":
        return 2
    return 3


class RegisterContractsGenerator(_Generator):
    def project(
        self, context: ArtifactGenerationContext
    ) -> RegisterContractsProjection:
        project = context.require_provider("isa")
        group_names = []
        registers = []
        for owner, namespace in project.registers.namespaces.items():
            for group in namespace.groups.values():
                group_name = (
                    f"REGISTER_GROUP_{_identifier(owner)}_{_identifier(group.id)}"
                )
                group_index = len(group_names)
                group_names.append(group_name)
                for register in group.registers.values():
                    if register.encoding is not None:
                        fields = register.layout.fields if register.layout else ()
                        writable_mask = (
                            sum(_mask(field.lsb, field.bits) for field in fields)
                            if register.layout is not None
                            else (1 << 64) - 1
                        )
                        reset_known = (
                            register.reset is not None
                            and register.reset.value is not None
                        )
                        registers.append(
                            RegisterContractProjection(
                                owner=owner,
                                group_id=group.id,
                                group_index=group_index,
                                register_id=register.id,
                                encoding=register.encoding,
                                width_kind=_register_width_kind(register.width),
                                fixed_width=(
                                    register.width
                                    if isinstance(register.width, int)
                                    else 0
                                ),
                                writable_mask=writable_mask,
                                reset_known=reset_known,
                                reset_value=(
                                    register.reset.value if reset_known else 0
                                ),
                                fields=tuple(
                                    RegisterFieldProjection(
                                        field.id,
                                        field.lsb,
                                        _mask(field.lsb, field.bits),
                                    )
                                    for field in fields
                                ),
                            )
                        )
        for owner, namespace in project.control_registers.namespaces.items():
            if not namespace.registers:
                continue
            group_name = (
                f"REGISTER_GROUP_{_identifier(owner)}_CONTROL_REGISTERS"
            )
            group_index = len(group_names)
            group_names.append(group_name)
            for register in namespace.registers.values():
                fields = register.layout.fields if register.layout else ()
                writable_mask = (
                    sum(_mask(field.lsb, field.bits) for field in fields)
                    if register.layout is not None
                    else (1 << 64) - 1
                )
                reset_known = (
                    register.reset is not None
                    and register.reset.value is not None
                )
                registers.append(
                    RegisterContractProjection(
                        owner=owner,
                        group_id="CONTROL_REGISTERS",
                        group_index=group_index,
                        register_id=register.id,
                        encoding=register.selector,
                        width_kind=0,
                        fixed_width=64,
                        writable_mask=writable_mask,
                        reset_known=reset_known,
                        reset_value=(
                            register.reset.value if reset_known else 0
                        ),
                        fields=tuple(
                            RegisterFieldProjection(
                                field.id,
                                field.lsb,
                                _mask(field.lsb, field.bits),
                            )
                            for field in fields
                        ),
                    )
                )
        return RegisterContractsProjection(tuple(group_names), tuple(registers))

    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        projection = self.project(context)
        group_width = max(1, (len(projection.group_names) - 1).bit_length())
        group_enum = ",\n".join(
            f"    {name} = {group_width}'d{index}"
            for index, name in enumerate(projection.group_names)
        )
        constants: list[str] = []
        cases: list[str] = []
        for register in projection.registers:
            group_name = projection.group_names[register.group_index]
            prefix = f"REGISTER_{_identifier(register.owner)}_{_identifier(register.group_id)}_{_identifier(register.register_id)}"
            constants.append(
                f"  localparam logic [15:0] {prefix} = 16'h{register.encoding:04x};"
            )
            for field in register.fields:
                field_prefix = f"{prefix}_{_identifier(field.id)}"
                constants.extend(
                    (
                        f"  localparam logic [6:0] {field_prefix}_LSB = 7'd{field.lsb};",
                        f"  localparam logic [63:0] {field_prefix}_MASK = 64'h{field.mask:016x};",
                    )
                )
            cases.append(
                f"      {{{group_name}, {prefix}}}: begin\n"
                f"        valid_o = 1'b1; width_kind_o = 2'd{register.width_kind};\n"
                f"        fixed_width_o = 16'd{register.fixed_width}; writable_mask_o = 64'h{register.writable_mask:016x};\n"
                f"        reset_known_o = 1'b{int(register.reset_known)}; reset_value_o = 64'h{register.reset_value:016x};\n"
                "      end"
            )
        package = f"""package bedrock_register_pkg;
  typedef enum logic [{group_width - 1}:0] {{
{group_enum}
  }} bedrock_register_group_e;

{chr(10).join(constants)}
endpackage"""
        contracts = f"""module bedrock_register_contracts
  import bedrock_register_pkg::*;
(
  input  bedrock_register_group_e group_i,
  input  logic [15:0] encoding_i,
  input  logic [63:0] write_data_i,
  output logic valid_o,
  output logic [1:0] width_kind_o,
  output logic [15:0] fixed_width_o,
  output logic [63:0] writable_mask_o,
  output logic reserved_zero_o,
  output logic reset_known_o,
  output logic [63:0] reset_value_o
);
  always_comb begin
    valid_o = 1'b0;
    width_kind_o = '0;
    fixed_width_o = '0;
    writable_mask_o = '0;
    reset_known_o = 1'b0;
    reset_value_o = '0;
    unique case ({{group_i, encoding_i}})
{chr(10).join(cases)}
      default: begin end
    endcase
    reserved_zero_o = valid_o && ((write_data_i & ~writable_mask_o) == 64'b0);
  end
endmodule"""
        return self._outputs(
            {
                "package": package,
                "contracts": contracts,
            }
        )


class VectorGeometryGenerator(_Generator):
    def project(self, context: ArtifactGenerationContext) -> VectorGeometryProjection:
        project = context.require_provider("isa")
        vector_namespace = project.registers.namespaces.get("VECTOR")
        if vector_namespace is None:
            raise ValueError("VECTOR register namespace is required")
        return VectorGeometryProjection(
            len(vector_namespace.groups["VECTOR"].registers),
            len(vector_namespace.groups["PREDICATE"].registers),
        )

    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        projection = self.project(context)
        package = f"""package bedrock_vector_geometry_pkg;
  localparam integer BEDROCK_VECTOR_REGISTER_COUNT = {projection.vector_register_count};
  localparam integer BEDROCK_PREDICATE_REGISTER_COUNT = {projection.predicate_register_count};
  typedef enum logic [2:0] {{
    VECTOR_PERMUTE_ZIP_LO,
    VECTOR_PERMUTE_ZIP_HI,
    VECTOR_PERMUTE_UNZIP_LO,
    VECTOR_PERMUTE_UNZIP_HI,
    VECTOR_PERMUTE_TRANSPOSE_LO,
    VECTOR_PERMUTE_TRANSPOSE_HI
  }} bedrock_vector_permute_e;

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
endpackage"""
        permute = """module bedrock_vector_permute
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
endmodule"""
        return self._outputs(
            {
                "package": package,
                "permuter": permute,
            }
        )


class AssertionsGenerator(_Generator):
    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        context.require_provider("isa")
        decode = """module bedrock_decode_assertions
  import bedrock_decode_pkg::*;
(
  input logic clk_i,
  input logic reset_i,
  input d0_result_t d0_i,
  input d1_opcode_result_t d1_i,
  input ea_decode_result_t ea_i
);
  default clocking cb @(posedge clk_i); endclocking
  default disable iff (reset_i);

  assert property (d0_i.status == D0_SUCCESS |-> d0_i.form != FORM_INVALID);
  assert property (d0_i.status == D0_SUCCESS |-> $onehot(d0_i.form_high_decode));
  assert property (d0_i.status == D0_SUCCESS |-> $onehot(d0_i.form_low_decode));
  assert property (d1_i.valid |-> d1_i.stage == D1_STAGE_SUCCESS);
  assert property (ea_i.valid |-> ea_i.stage == D1_STAGE_SUCCESS);
  assert property (d1_i.valid |-> d1_i.form == d0_i.form);
  cover property (d1_i.valid && ea_i.valid);
endmodule"""
        architecture = """module bedrock_architecture_assertions
  import bedrock_event_pkg::*;
(
  input logic clk_i,
  input logic reset_i,
  input logic register_valid_i,
  input logic register_reserved_zero_i,
  input logic register_write_i,
  input logic event_known_i,
  input bedrock_event_frame_type_e event_frame_i,
  input logic [7:0] event_frame_slots_i
);
  default clocking cb @(posedge clk_i); endclocking
  default disable iff (reset_i);

  assert property (register_valid_i && register_write_i |-> register_reserved_zero_i);
  assert property (event_known_i && event_frame_i == EVENT_FRAME_BASIC
                   |-> event_frame_slots_i == 8);
  assert property (event_known_i && event_frame_i == EVENT_FRAME_ERROR
                   |-> event_frame_slots_i == 10);
  assert property (event_known_i &&
                   (event_frame_i == EVENT_FRAME_PAGE ||
                    event_frame_i == EVENT_FRAME_AUXILIARY)
                   |-> event_frame_slots_i == 12);
endmodule"""
        return self._outputs(
            {
                "decode": decode,
                "architecture": architecture,
            }
        )
