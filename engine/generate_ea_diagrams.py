"""Generate LaTeX encoding and address-flow diagrams from EA mode YAML."""

from __future__ import annotations

import argparse
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from math import sqrt
from pathlib import Path
import re
import sys

from .ea_mode import (
    EABaseSource,
    EAEncoding,
    EAMode,
    EAModeCatalog,
    ExtendedExtensionEAMode,
    FixedEASegment,
    ImmediateEAMode,
    MemoryEAMode,
)
from .reference import Reference
from .type_system import TypeSystem


def _tex(value: object) -> str:
    """Escape plain YAML text for use as LaTeX macro content."""

    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "#": r"\#",
        "$": r"\$",
        "%": r"\%",
        "&": r"\&",
        "_": r"\_",
        "^": r"\textasciicircum{}",
        "~": r"\textasciitilde{}",
    }
    return "".join(replacements.get(character, character) for character in str(value))


_TITLE_MINOR_WORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "as",
        "at",
        "but",
        "by",
        "for",
        "in",
        "nor",
        "of",
        "on",
        "or",
        "per",
        "the",
        "to",
        "via",
        "with",
    }
)


def _title_case(value: object) -> str:
    """Title-case a display heading while preserving acronyms and numeric IDs."""

    text = str(value)
    matches = list(re.finditer(r"[A-Za-z0-9]+", text))
    if not matches:
        return text
    parts: list[str] = []
    cursor = 0
    for index, match in enumerate(matches):
        parts.append(text[cursor : match.start()])
        word = match.group(0)
        lowered = word.lower()
        if word.isupper() or any(character.isdigit() for character in word):
            rendered = word
        elif any(character.isupper() for character in word[1:]):
            rendered = word
        elif lowered in _TITLE_MINOR_WORDS and index not in {0, len(matches) - 1}:
            rendered = lowered
        else:
            rendered = lowered.capitalize()
        parts.append(rendered)
        cursor = match.end()
    parts.append(text[cursor:])
    return "".join(parts)


def _flat_pattern(pattern: str | Sequence[str]) -> str:
    return pattern if isinstance(pattern, str) else "".join(pattern)


@dataclass(frozen=True, slots=True)
class EAEncodingFieldProjection:
    """One fixed-bit or named-field run in an EA encoding row."""

    code: str
    bits: int
    fixed: bool


@dataclass(frozen=True, slots=True)
class EAAutoupdateProjection:
    """One architected register update attached to an encoding variant."""

    encoding_index: int
    target: str
    update_type: str
    difference: str


@dataclass(frozen=True, slots=True)
class EAEncodingProjection:
    """One reader-facing encoding row and its optional update behavior."""

    label: str
    fields: tuple[EAEncodingFieldProjection, ...]
    autoupdate: EAAutoupdateProjection | None


class EAFlowProjection:
    """Base class for one address-generation flow projection."""

    __slots__ = ()


@dataclass(frozen=True, slots=True)
class ImmediateEAFlowProjection(EAFlowProjection):
    pass


@dataclass(frozen=True, slots=True)
class MemoryEAFlowProjection(EAFlowProjection):
    """The address-generation relation conveyed by a memory mode."""

    base_source: EABaseSource
    base_label: str
    base_operand: str
    index_operand: str | None
    has_displacement: bool
    has_scale: bool


@dataclass(frozen=True, slots=True)
class ExtensionEAFlowProjection(EAFlowProjection):
    pass


@dataclass(frozen=True, slots=True)
class EAModeDiagramProjection:
    """Owner-local semantic input to the EA diagram serializer."""

    reference: Reference[EAMode]
    owner: str
    source: Path
    title: str
    encodings: tuple[EAEncodingProjection, ...]
    flow: EAFlowProjection
    autoupdates: tuple[EAAutoupdateProjection, ...]
    authored_mode: EAMode


def _encoding_fields(
    pattern: str | Sequence[str],
) -> tuple[EAEncodingFieldProjection, ...]:
    fields: list[EAEncodingFieldProjection] = []
    flat = _flat_pattern(pattern)
    start = 0
    while start < len(flat):
        fixed = flat[start] in "01"
        end = start + 1
        while end < len(flat):
            if fixed:
                if flat[end] not in "01":
                    break
            elif flat[end] != flat[start]:
                break
            end += 1
        run = flat[start:end]
        fields.append(
            EAEncodingFieldProjection(run if fixed else run[0], len(run), fixed)
        )
        start = end
    return tuple(fields)


def _payload_type_id(mode: EAMode, encoding_index: int, payload_index: int) -> str:
    reference = mode.payload_type_reference(encoding_index, payload_index)
    return mode.type_system.payload_types.resolve(reference).id


def _encoding_label(
    mode: EAMode, encoding_index: int, encoding: EAEncoding
) -> str:
    parts: list[str] = []
    update = encoding.autoupdate
    if update is not None:
        parts.append(f"{update.target} {update.update_type}")
    parts.extend(
        _payload_type_id(mode, encoding_index, payload_index)
        for payload_index, _ in enumerate(encoding.payloads)
    )
    return " + ".join(parts) if parts else "plain"


def render_encoding_diagram(projection: EAModeDiagramProjection) -> str:
    """Render the wire encodings of one EA mode as a Bedrock format diagram."""

    caption = _title_case(f"{projection.title} encodings")
    lines = [f"\\begin{{BedrockFormatDiagram}}{{{_tex(caption)}}}"]
    for encoding in projection.encodings:
        lines.append(f"\\BedrockFormatRow{{{_tex(encoding.label)}}}{{%")
        for field in encoding.fields:
            macro = "Fixed" if field.fixed else "FieldCode"
            lines.append(
                f"  \\BedrockFormat{macro}{{{field.code}}}{{{field.bits}}}"
            )
        lines.append("}")
    lines.append("\\end{BedrockFormatDiagram}")
    return "\n".join(lines)


def _field_operand(mode: EAMode, role: str) -> str | None:
    field = mode.field_for_role(role)
    return f"Rn({field.symbol})" if field is not None else None


def _expression(mode: ImmediateEAMode | MemoryEAMode) -> str:
    return mode.pseudocode.split("=", 1)[1].strip()


def _base_operand(mode: EAMode, expression: str) -> tuple[str, str]:
    field = _field_operand(mode, "base")
    if field:
        return "BASE REGISTER", field
    for register, label in (("SP", "STACK POINTER"), ("PC", "PROGRAM COUNTER")):
        if register in expression.split():
            return label, register
    if "absolute" in expression.split():
        return "ABSOLUTE ADDRESS", "absolute"
    return "ZERO BASE", "0"


def project_mode(mode: EAMode) -> EAModeDiagramProjection:
    """Project one authored EA mode into its reader-facing diagram semantics."""

    updates: list[EAAutoupdateProjection] = []
    encodings: list[EAEncodingProjection] = []
    for encoding_index, encoding in enumerate(mode.encodings):
        raw_update = encoding.autoupdate
        update = None
        if raw_update is not None:
            update = EAAutoupdateProjection(
                encoding_index,
                raw_update.target,
                raw_update.update_type,
                str(raw_update.difference),
            )
            updates.append(update)
        encodings.append(
            EAEncodingProjection(
                _encoding_label(mode, encoding_index, encoding),
                _encoding_fields(encoding.patterns),
                update,
            )
        )

    flow: EAFlowProjection
    if isinstance(mode, ImmediateEAMode):
        flow = ImmediateEAFlowProjection()
    elif isinstance(mode, MemoryEAMode):
        expression = _expression(mode)
        words = expression.split()
        base_label, base_operand = _base_operand(mode, expression)
        flow = MemoryEAFlowProjection(
            mode.base_source,
            base_label,
            base_operand,
            _field_operand(mode, "index"),
            "displacement" in words,
            "scale" in words,
        )
    else:
        flow = ExtensionEAFlowProjection()

    return EAModeDiagramProjection(
        mode.reference,
        mode.reference.owner,
        mode.source,
        mode.name,
        tuple(encodings),
        flow,
        tuple(updates),
        mode,
    )


@dataclass(frozen=True)
class _FlowNode:
    """Common placement of one semantic flow node."""

    node_id: str
    row: int
    lane: str
    text: str


@dataclass(frozen=True)
class _FlowBoxNode(_FlowNode):
    row_label: str
    width_class: str = "word"
    show_bits: bool = False


@dataclass(frozen=True)
class _FlowOperationNode(_FlowNode):
    pass


class _EAFlowLayout:
    """Lay out an EA data-flow graph on a regular semantic grid.

    Diagram builders name rows and lanes only.  All dimensions, coordinates,
    box widths, and feedback ports are derived here so individual EA modes
    cannot accumulate hand-tuned geometry.
    """

    ROW_PITCH = 0.72
    TOP_Y = 0.90
    MAIN_X = 4.62
    WORD_WIDTH = 2.20
    AUX_WIDTH = 1.12
    OP_RADIUS = 0.135
    MILLIMETERS_PER_INCH = 25.4
    ARROW_HEAD_LENGTH = 2.0 / MILLIMETERS_PER_INCH
    EDGE_CLEARANCE = 0.06
    OP_GAP = ARROW_HEAD_LENGTH + EDGE_CLEARANCE
    FEEDBACK_PORT_OFFSET = 0.07
    FEEDBACK_INSET = 0.20

    def __init__(self, caption: str, row_count: int) -> None:
        self.caption = caption
        self.row_count = row_count
        self.nodes: dict[str, _FlowNode] = {}
        self.edges: list[str] = []
        self.memory_tail: tuple[str, int] | None = None

    @classmethod
    def _width(cls, width_class: str) -> float:
        if width_class == "word":
            return cls.WORD_WIDTH
        if width_class == "aux":
            return cls.AUX_WIDTH
        raise ValueError(f"unsupported EA flow width class: {width_class}")

    @classmethod
    def _lane_x(cls, lane: str, width_class: str = "word") -> float:
        width = cls._width(width_class)
        if lane == "main":
            return cls.MAIN_X
        if lane == "source":
            return cls.MAIN_X - cls.OP_RADIUS - cls.OP_GAP - width / 2
        if lane == "secondary":
            return cls._lane_x("source", "word")
        if lane == "side":
            secondary = cls._lane_x("secondary")
            return secondary - cls.OP_RADIUS - cls.OP_GAP - width / 2
        if lane == "merge":
            secondary = cls._lane_x("secondary")
            return (secondary + cls.MAIN_X) / 2
        if lane == "feedback":
            return cls.MAIN_X - cls.WORD_WIDTH / 2 + cls.FEEDBACK_INSET
        raise ValueError(f"unsupported EA flow lane: {lane}")

    @classmethod
    def _row_y(cls, row: int) -> float:
        return cls.TOP_Y - row * cls.ROW_PITCH

    @staticmethod
    def _number(value: float) -> str:
        rendered = f"{value:.3f}".rstrip("0").rstrip(".")
        return "0" if rendered == "-0" else rendered

    def add_box(
        self,
        node_id: str,
        row: int,
        lane: str,
        text: str,
        *,
        row_label: str,
        width_class: str = "word",
        show_bits: bool = False,
    ) -> None:
        self.nodes[node_id] = _FlowBoxNode(
            node_id,
            row,
            lane,
            text,
            row_label,
            width_class,
            show_bits,
        )

    def add_operation(self, node_id: str, row: int, lane: str, text: str) -> None:
        self.nodes[node_id] = _FlowOperationNode(node_id, row, lane, text)

    def connect(self, source: str, target: str) -> None:
        if source.endswith(".east") and target.endswith(".west"):
            source_id = source.removesuffix(".east")
            target_id = target.removesuffix(".west")
            source_node = self.nodes[source_id]
            target_node = self.nodes[target_id]
            source_half_width = (
                self.OP_RADIUS
                if isinstance(source_node, _FlowOperationNode)
                else self._width(source_node.width_class) / 2
            )
            target_half_width = (
                self.OP_RADIUS
                if isinstance(target_node, _FlowOperationNode)
                else self._width(target_node.width_class) / 2
            )
            source_width_class = (
                "word"
                if isinstance(source_node, _FlowOperationNode)
                else source_node.width_class
            )
            target_width_class = (
                "word"
                if isinstance(target_node, _FlowOperationNode)
                else target_node.width_class
            )
            source_right = (
                self._lane_x(source_node.lane, source_width_class)
                + source_half_width
            )
            target_left = (
                self._lane_x(target_node.lane, target_width_class)
                - target_half_width
            )
            if target_left - source_right + 1e-9 < self.OP_GAP:
                raise ValueError(
                    f"{source_id} -> {target_id}: horizontal edge gap "
                    f"{target_left - source_right:.3f} is smaller than "
                    f"{self.OP_GAP:.3f}"
                )
        self.edges.append(f"  \\draw[bedrockFlowArrow] ({source}) -- ({target});%")

    def connect_feedback(self, register_id: str, operation_id: str) -> None:
        register = self.nodes[register_id]
        operation = self.nodes[operation_id]
        if not isinstance(register, _FlowBoxNode) or not isinstance(
            operation, _FlowOperationNode
        ):
            raise TypeError("feedback requires a box and an operation node")
        register_x = self._lane_x(register.lane, register.width_class)
        register_width = self._width(register.width_class)
        operation_x = self._lane_x(operation.lane)
        offset = self.FEEDBACK_PORT_OFFSET
        if not register_x - register_width / 2 < operation_x - offset:
            raise ValueError(f"{operation_id}: feedback output misses {register_id}")
        if not operation_x + offset < register_x + register_width / 2:
            raise ValueError(f"{operation_id}: feedback input misses {register_id}")
        register_y = self._row_y(register.row) - 0.13
        operation_y = self._row_y(operation.row)
        operation_port_y = operation_y + sqrt(self.OP_RADIUS**2 - offset**2)
        out_id = f"{operation_id}feedbackout"
        in_id = f"{operation_id}feedbackin"
        op_in_id = f"{operation_id}in"
        op_out_id = f"{operation_id}out"
        number = self._number
        self.edges.extend(
            [
                f"  \\coordinate ({out_id}) at ({number(operation_x - offset)},{number(register_y)});%",
                f"  \\coordinate ({in_id}) at ({number(operation_x + offset)},{number(register_y)});%",
                f"  \\coordinate ({op_in_id}) at ({number(operation_x - offset)},{number(operation_port_y)});%",
                f"  \\coordinate ({op_out_id}) at ({number(operation_x + offset)},{number(operation_port_y)});%",
                f"  \\draw[bedrockFlowArrow] ({out_id}) -- ({op_in_id});%",
                f"  \\draw[bedrockFlowArrow] ({op_out_id}) -- ({in_id});%",
            ]
        )

    def connect_box_port_to_operation(
        self, box_id: str, operation_id: str, lane: str
    ) -> None:
        box = self.nodes[box_id]
        if not isinstance(box, _FlowBoxNode):
            raise TypeError("box-port connection requires a box node")
        x = self._lane_x(lane)
        box_y = self._row_y(box.row) - 0.13
        number = self._number
        port_id = f"{box_id}to{operation_id}"
        self.edges.append(
            f"  \\coordinate ({port_id}) at ({number(x)},{number(box_y)});%"
        )
        self.connect(port_id, f"{operation_id}.north")

    def add_memory_tail(self, pointer_id: str, row: int) -> None:
        self.memory_tail = (pointer_id, row)

    def render(self) -> str:
        number = self._number
        height = 0.70 + max(0, self.row_count - 1) * self.ROW_PITCH
        lines = [
            f"\\BedrockEAFlowStart{{{number(height)}in}}{{{self.caption}}}%"
        ]
        for node in self.nodes.values():
            width_class = (
                node.width_class if isinstance(node, _FlowBoxNode) else "word"
            )
            x = self._lane_x(node.lane, width_class)
            y = self._row_y(node.row)
            if isinstance(node, _FlowOperationNode):
                lines.append(
                    f"  \\BedrockEAFlowCircle{{{node.node_id}}}"
                    f"{{{number(x)}}}{{{number(y)}}}{{{node.text}}}%"
                )
            else:
                if not isinstance(node, _FlowBoxNode):
                    raise TypeError(f"unsupported flow node {type(node).__name__}")
                width = self._width(node.width_class)
                lines.append(
                    f"  \\BedrockEAFlowLabeledBox{{{node.row_label}}}"
                    f"{{{node.node_id}}}{{{number(y)}}}{{{number(x)}}}"
                    f"{{{number(width)}}}{{{node.text}}}"
                    f"{{{1 if node.show_bits else 0}}}%"
                )
        lines.extend(self.edges)
        if self.memory_tail is not None:
            pointer_id, row = self.memory_tail
            y = self._row_y(row)
            lines.append(
                f"  \\BedrockEAFlowMemoryTail{{{pointer_id}}}"
                f"{{{number(y)}}}{{{number(self.MAIN_X)}}}"
                f"{{{number(self.WORD_WIDTH)}}}%"
            )
        lines.append("  \\BedrockEAFlowEnd")
        return "\n".join(lines)


def _add_result_and_memory(
    layout: _EAFlowLayout, result_row: int, result_text: str
) -> None:
    layout.add_box(
        "ptr",
        result_row,
        "main",
        result_text,
        row_label="OPERAND POINTER",
        show_bits=True,
    )
    layout.add_memory_tail("ptr", result_row + 1)


def render_flow_diagram(projection: EAModeDiagramProjection) -> str | None:
    """Render one plain EA mode through the semantic grid layout engine."""

    flow = projection.flow
    if isinstance(flow, ExtensionEAFlowProjection):
        return None

    generated_value = (
        "operand" if isinstance(flow, ImmediateEAFlowProjection) else "address"
    )
    name = _tex(_title_case(f"{projection.title} {generated_value} generation"))
    if isinstance(flow, ImmediateEAFlowProjection):
        layout = _EAFlowLayout(name, 2)
        layout.add_box(
            "imm",
            0,
            "main",
            "immediate",
            row_label="IMMEDIATE DATA",
            show_bits=True,
        )
        layout.add_box(
            "operand",
            1,
            "main",
            "IMMEDIATE VALUE",
            row_label="OPERAND",
        )
        layout.connect("imm.south", "operand.north")
        return layout.render()

    if not isinstance(flow, MemoryEAFlowProjection):
        raise TypeError(f"unsupported EA flow {type(flow).__name__}")
    source_label, base = flow.base_label, flow.base_operand
    index = flow.index_operand
    if index and flow.has_scale:
        has_displacement = flow.has_displacement
        index_row = 2 if has_displacement else 1
        merge_row = index_row + 1
        layout = _EAFlowLayout(name, merge_row + 3)
        layout.add_box(
            "base", 0, "main", _tex(base), row_label=_tex(source_label), show_bits=True
        )
        if has_displacement:
            layout.add_box(
                "disp",
                1,
                "source",
                "displacement",
                row_label="DISPLACEMENT",
                show_bits=True,
            )
            layout.add_operation("addbase", 1, "main", "+")
            layout.connect("base.south", "addbase.north")
            layout.connect("disp.east", "addbase.west")
            main_source = "addbase.south"
        else:
            main_source = "base.south"
        layout.add_box(
            "idx",
            index_row,
            "secondary",
            _tex(index),
            row_label="INDEX REGISTER",
            show_bits=True,
        )
        layout.add_box(
            "scale",
            merge_row,
            "side",
            "SCALE VALUE",
            row_label="SCALE",
            width_class="aux",
        )
        layout.add_operation("mul", merge_row, "secondary", "x")
        layout.add_operation("addindex", merge_row, "main", "+")
        layout.connect(main_source, "addindex.north")
        layout.connect("idx.south", "mul.north")
        layout.connect("scale.east", "mul.west")
        layout.connect("mul.east", "addindex.west")
        _add_result_and_memory(layout, merge_row + 1, "EFFECTIVE ADDRESS")
        layout.connect("addindex.south", "ptr.north")
        return layout.render()
    if flow.has_displacement:
        layout = _EAFlowLayout(name, 4)
        layout.add_box(
            "base", 0, "main", _tex(base), row_label=_tex(source_label), show_bits=True
        )
        layout.add_box(
            "disp",
            1,
            "source",
            "displacement",
            row_label="DISPLACEMENT",
            show_bits=True,
        )
        layout.add_operation("add", 1, "main", "+")
        layout.connect("base.south", "add.north")
        layout.connect("disp.east", "add.west")
        _add_result_and_memory(layout, 2, "EFFECTIVE ADDRESS")
        layout.connect("add.south", "ptr.north")
        return layout.render()
    layout = _EAFlowLayout(name, 3)
    layout.add_box(
        "src", 0, "main", _tex(base), row_label=_tex(source_label), show_bits=True
    )
    _add_result_and_memory(layout, 1, "EFFECTIVE ADDRESS")
    layout.connect("src.south", "ptr.north")
    return layout.render()


def render_autoupdate_diagrams(
    projection: EAModeDiagramProjection, *, embedded: bool = False
) -> list[str]:
    """Render each autoupdate variant as an integrated address-generation flow."""

    flow = projection.flow
    if not isinstance(flow, MemoryEAFlowProjection):
        return []
    source_label, base = flow.base_label, flow.base_operand
    displacement = "displacement" if flow.has_displacement else ""
    index = flow.index_operand
    diagrams: list[str] = []
    for update in projection.autoupdates:
        target = update.target
        update_type = update.update_type
        difference = _tex(update.difference)
        suffix = f" / {update_type}"
        variant_name = (
            projection.title
            if projection.title.endswith(suffix)
            else projection.title + suffix
        )
        caption = _tex(_title_case(f"{variant_name} address generation"))
        if target == "base":
            operand = (
                flow.base_operand
                if flow.base_source is EABaseSource.ENCODED
                else None
            )
            if operand is None:
                raise ValueError(
                    f"{projection.source}: base autoupdate requires a base field"
                )
            layout = _EAFlowLayout(caption, 5)
            layout.add_box(
                "base",
                0,
                "main",
                _tex(operand),
                row_label=_tex(source_label),
                show_bits=True,
            )
            operation_lane = "feedback" if update_type == "postincrement" else "main"
            layout.add_box(
                "update",
                1,
                "side",
                difference,
                row_label="UPDATE DIFFERENCE",
                width_class="aux",
            )
            layout.add_operation(
                "updateop", 1, operation_lane, "+" if update_type == "postincrement" else "$-$"
            )
            layout.add_box(
                "disp",
                2,
                "source",
                _tex(displacement),
                row_label="DISPLACEMENT",
                show_bits=True,
            )
            layout.add_operation("add", 2, "main", "+")
            layout.connect("update.east", "updateop.west")
            layout.connect_feedback("base", "updateop")
            if update_type == "postincrement":
                layout.connect("base.south", "add.north")
            else:
                layout.connect("updateop.south", "add.north")
            layout.connect("disp.east", "add.west")
            _add_result_and_memory(layout, 3, "EFFECTIVE ADDRESS")
            layout.connect("add.south", "ptr.north")
            rendered = layout.render()
            diagrams.append(
                rendered
                if embedded
                else (
                    f"\\clearpage\n\\BedrockInstructionLead{{{_tex(_title_case(variant_name))}}}\n"
                    "\\par\\Needspace{4.70in}%\n"
                    f"{rendered}"
                )
            )
        elif target == "index":
            if index is None:
                raise ValueError(
                    f"{projection.source}: index autoupdate requires an index field"
                )
            layout = _EAFlowLayout(caption, 7)
            layout.add_box(
                "base", 0, "main", _tex(base), row_label=_tex(source_label), show_bits=True
            )
            layout.add_box(
                "disp",
                1,
                "source",
                _tex(displacement),
                row_label="DISPLACEMENT",
                show_bits=True,
            )
            layout.add_operation("addbase", 1, "main", "+")
            layout.add_box(
                "idx",
                2,
                "secondary",
                _tex(index),
                row_label="INDEX REGISTER",
                show_bits=True,
            )
            layout.add_box(
                "update",
                3,
                "side",
                difference,
                row_label="INDEX UPDATE",
                width_class="aux",
            )
            layout.add_operation(
                "updateop",
                3,
                "secondary",
                "+" if update_type == "postincrement" else "$-$",
            )
            layout.add_box(
                "scale",
                4,
                "side",
                "SCALE VALUE",
                row_label="SCALE",
                width_class="aux",
            )
            multiply_lane = "merge" if update_type == "postincrement" else "secondary"
            layout.add_operation("mul", 4, multiply_lane, "x")
            layout.add_operation("addindex", 4, "main", "+")
            layout.connect("base.south", "addbase.north")
            layout.connect("disp.east", "addbase.west")
            layout.connect("addbase.south", "addindex.north")
            layout.connect("update.east", "updateop.west")
            layout.connect_feedback("idx", "updateop")
            if update_type == "postincrement":
                layout.connect_box_port_to_operation("idx", "mul", "merge")
            else:
                layout.connect("updateop.south", "mul.north")
            layout.connect("scale.east", "mul.west")
            layout.connect("mul.east", "addindex.west")
            _add_result_and_memory(layout, 5, "EFFECTIVE ADDRESS")
            layout.connect("addindex.south", "ptr.north")
            rendered = layout.render()
            diagrams.append(
                rendered
                if embedded
                else (
                    f"\\clearpage\n\\BedrockInstructionLead{{{_tex(_title_case(variant_name))}}}\n"
                    "\\par\\Needspace{6.15in}%\n"
                    f"{rendered}"
                )
            )
        else:
            raise ValueError(
                f"{projection.source}: unsupported autoupdate target {target!r}"
            )
    return diagrams


def _block_height(projection: EAModeDiagramProjection) -> float:
    """Estimate the space used by the format diagram and its optional flow."""

    format_height = 0.90 + 0.68 * len(projection.encodings)
    flow = projection.flow
    if isinstance(flow, ExtensionEAFlowProjection):
        flow_height = 0.0
    elif isinstance(flow, ImmediateEAFlowProjection):
        flow_height = 1.55
    elif isinstance(flow, MemoryEAFlowProjection) and flow.index_operand and flow.has_scale:
        flow_height = 3.30
    elif isinstance(flow, MemoryEAFlowProjection) and flow.has_displacement:
        flow_height = 2.35
    else:
        flow_height = 2.10
    if any(update.target == "index" for update in projection.autoupdates):
        return 7.55
    if projection.autoupdates:
        return 6.35
    return min(7.0, format_height + flow_height + 0.70)


def _syntax_variants(mode: EAMode) -> tuple[str, ...]:
    if not isinstance(mode, (ImmediateEAMode, MemoryEAMode, ExtendedExtensionEAMode)):
        return ()
    syntax = mode.syntax
    variants: list[str] = []
    for encoding_index, encoding in enumerate(mode.encodings):
        rendered = syntax
        payloads = {
            payload.role: _payload_type_id(
                mode, encoding_index, payload_index
            ).lower()
            for payload_index, payload in enumerate(encoding.payloads)
        }
        optional_displacement = payloads.get("displacement")
        rendered = rendered.replace(
            "[+ displacement]",
            f"+ {optional_displacement}" if optional_displacement else "",
        )
        update = encoding.autoupdate
        match = re.search(r"update\((.+)\)", rendered)
        if match is not None:
            operand = match.group(1)
            if update is None:
                replacement = operand
            elif update.update_type == "postincrement":
                replacement = operand + "++"
            else:
                replacement = "--" + operand
            rendered = rendered[: match.start()] + replacement + rendered[match.end() :]
        for role, payload_type in payloads.items():
            rendered = re.sub(rf"\b{re.escape(role)}\b", payload_type, rendered)
        rendered = re.sub(r"\s+", " ", rendered).replace(" ]", "]")
        if rendered not in variants:
            variants.append(rendered)
    return tuple(variants)


def _encoding_description(mode: EAMode) -> str:
    descriptions = []
    for encoding_index, encoding in enumerate(mode.encodings):
        pattern = " ".join(encoding.patterns)
        details = []
        update = encoding.autoupdate
        if update is not None:
            details.append(f"{update.target} {update.update_type}")
        payloads = encoding.payloads
        if payloads:
            details.extend(
                _payload_type_id(mode, encoding_index, payload_index).lower()
                for payload_index, _ in enumerate(payloads)
            )
        suffix = f" ({', '.join(details)})" if details else ""
        descriptions.append(rf"\texttt{{{_tex(pattern)}}}{_tex(suffix)}")
    return "; ".join(descriptions) + "."


def _segment_description(mode: EAMode) -> str:
    segment = mode.segment if isinstance(mode, MemoryEAMode) else None
    if segment is None:
        return "Uses the operation default data segment."
    if isinstance(segment, FixedEASegment):
        return f"Fixed to {_tex(segment.register)}."
    return "SEG(s) selects the encoded segment register."


def _payload_description(mode: EAMode) -> str:
    payloads = []
    for encoding_index, encoding in enumerate(mode.encodings):
        for payload_index, payload in enumerate(encoding.payloads):
            item = (
                payload.role,
                _payload_type_id(mode, encoding_index, payload_index).lower(),
            )
            if item not in payloads:
                payloads.append(item)
    if payloads:
        listed = ", ".join(
            rf"\texttt{{{_tex(payload_type)}}} ({_tex(role)})"
            for role, payload_type in payloads
        )
        return f"Appends {listed} as selected by the encoding."
    if mode.catalog.mode_type != "compact":
        return "The descriptor is followed by the displacement selected by the compact EXT escape."
    return "No appended payload bytes."


def _update_description(mode: EAMode) -> str | None:
    updates = [
        encoding.autoupdate
        for encoding in mode.encodings
        if encoding.autoupdate is not None
    ]
    if not updates:
        return None
    sentences = []
    for update in updates:
        target = f"{update.target} register"
        difference = update.difference
        difference_text = (
            rf"\texttt{{{_tex(difference)}}}"
            if isinstance(difference, str)
            else str(difference)
        )
        if update.update_type == "postincrement":
            sentences.append(
                f"Postincrement uses the current temporary {target}, then adds {difference_text}."
            )
        else:
            sentences.append(
                f"Predecrement subtracts {difference_text} from the temporary {target} before use."
            )
    return " ".join(sentences)


def render_description_block(mode: EAMode) -> str:
    """Render the former hand-authored EA explanation block from mode data."""

    title = _title_case(f"{mode.catalog.name} {mode.name}")
    label = "EA encoding" if mode.catalog.mode_type == "compact" else "Descriptor"
    lines = [
        r"\begin{BedrockFormBlock}{2.75in}",
        rf"\BedrockEAProfileTitle{{{_tex(title)}}}",
        r"\begin{BedrockEAProfile}",
    ]
    lines.extend(
        rf"\BedrockEAProfileSyntax{{{_tex(syntax).replace('--', '{-}{-}')}}}"
        for syntax in _syntax_variants(mode)
    )
    lines.extend(
        (
            rf"\BedrockEAProfileLine{{{label}}}{{{_encoding_description(mode)}}}",
            rf"\BedrockEAProfileLine{{Segment}}{{{_segment_description(mode)}}}",
            rf"\BedrockEAProfileLine{{Payload}}{{{_payload_description(mode)}}}",
        )
    )
    update = _update_description(mode)
    if update is not None:
        lines.append(rf"\BedrockEAProfileLine{{Update}}{{{update}}}")
    lines.extend((r"\end{BedrockEAProfile}", r"\end{BedrockFormBlock}"))
    return "\n".join(lines)


def _encoding_variant_mode(
    mode: EAMode, encoding: EAEncoding
) -> EAMode:
    """Return a one-encoding view so each update form owns its explanation."""

    return mode.with_encoding(encoding)


def _render_mode_section(projection: EAModeDiagramProjection) -> str:
    mode = projection.authored_mode
    parts = [f"\\par\\Needspace{{{_block_height(projection):.2f}in}}%"]
    parts.extend(
        (
            render_description_block(mode),
            render_encoding_diagram(projection),
        )
    )
    update_flows = render_autoupdate_diagrams(projection, embedded=True)
    if update_flows:
        parts.extend(update_flows)
    else:
        flow = render_flow_diagram(projection)
        if flow:
            parts.append(flow)
    return "\n\n".join(parts)


def render_mode(projection: EAModeDiagramProjection) -> str:
    mode = projection.authored_mode
    relative_source = mode.source
    try:
        relative_source = mode.source.resolve().relative_to(mode.isa_root.resolve())
    except ValueError:
        pass
    header = f"% Generated from {relative_source.as_posix()}; do not edit this block."
    encodings = mode.encodings
    if len(encodings) > 1 and any(
        encoding.autoupdate is not None for encoding in encodings
    ):
        sections = []
        for index, encoding in enumerate(encodings):
            variant = project_mode(_encoding_variant_mode(mode, encoding))
            section = _render_mode_section(variant)
            sections.append(section if index == 0 else f"\\clearpage\n{section}")
        return "\n\n".join((header, *sections))

    return "\n\n".join(
        (
            header,
            _render_mode_section(projection),
        )
    )


def catalog_mode_paths(isa_root: Path) -> list[Path]:
    """Return concrete mode paths in each profile catalog's declared order."""

    types = TypeSystem.load(isa_root)
    return [
        catalog.mode_path(mode_id)
        for catalog in EAModeCatalog.discover(isa_root, types)
        for mode_id in catalog.modes
    ]


def render_paths(paths: Iterable[Path], isa_root: Path) -> str:
    """Load explicitly requested paths and render them for the debug CLI."""

    modes = [EAMode.load(path, isa_root) for path in paths]
    return render_modes(modes)


def render_modes(modes: Iterable[EAMode]) -> str:
    """Render an already-loaded EA mode inventory in its declared order."""

    header = "% Generated by engine.generate_ea_diagrams.\n"
    separator = "\n\n\\clearpage\n\n"
    return (
        header
        + separator.join(render_mode(project_mode(mode)) for mode in modes)
        + "\n"
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "modes",
        metavar="MODE_YAML",
        nargs="*",
        type=Path,
        help="mode.yaml files to render; defaults to every catalogued EA mode",
    )
    parser.add_argument(
        "--isa-root",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "isa",
        help="ISA definition root (default: repository/isa)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="write the TeX fragment here instead of stdout",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    isa_root = args.isa_root.resolve()
    paths = args.modes or catalog_mode_paths(isa_root)
    rendered = render_paths(paths, isa_root)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
