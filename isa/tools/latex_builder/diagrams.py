"""Reusable LaTeX/TikZ diagram helpers for the ISA reference generator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from spec_model.encoding import (
    control_register_class_width,
    control_register_class_registers,
    data_register_banking_selector_name,
    register_class_names,
    register_class_width,
    special_register_class_width,
    special_register_class_registers,
    special_register_width,
)
from .common import LatexComponent, caption_title, listed_figure_caption, tex_escape


def bit_segments(bits: str) -> list[tuple[str, str, int]]:
    """Return (kind, label, width) segments for a compact bit-field drawing."""
    clean = "".join(ch for ch in bits if not ch.isspace())
    if not clean:
        return []
    out: list[tuple[str, str, int]] = []
    index = 0
    while index < len(clean):
        ch = clean[index]
        if ch in "01":
            end = index + 1
            while end < len(clean) and clean[end] in "01":
                end += 1
            chunk_start = index
            while chunk_start < end:
                chunk_end = min(end, chunk_start + 4)
                out.append(("fixed", clean[chunk_start:chunk_end], chunk_end - chunk_start))
                chunk_start = chunk_end
            index = end
            continue
        if ch == "-":
            end = index + 1
            while end < len(clean) and clean[end] == "-":
                end += 1
            out.append(("wild", "-" * (end - index), end - index))
            index = end
            continue
        end = index + 1
        while end < len(clean) and clean[end] == ch:
            end += 1
        out.append(("field", ch, end - index))
        index = end
    return out


def bit_row_commands(bits: str, y: float, label: str, total_bits: int) -> list[str]:
    commands: list[str] = []
    x = 0
    commands.append(rf"\node[anchor=east] at (-0.35,{y + 0.5:.2f}) {{{tex_escape(label)}}};")
    commands.append(rf"\node[anchor=south] at (0,{y + 1.18:.2f}) {{{total_bits - 1}}};")
    commands.append(rf"\node[anchor=south] at ({total_bits},{y + 1.18:.2f}) {{0}};")
    if total_bits >= 16:
        for tick in range(4, total_bits, 4):
            commands.append(rf"\draw[LightRule] ({tick},{y:.2f}) -- ({tick},{y + 1:.2f});")
    for _kind, raw_label, width in bit_segments(bits):
        commands.append(rf"\draw ({x},{y:.2f}) rectangle ({x + width},{y + 1:.2f});")
        commands.append(rf"\node at ({x + width / 2:.2f},{y + 0.5:.2f}) {{\texttt{{{tex_escape(raw_label)}}}}};")
        x += width
    return commands


@dataclass(frozen=True)
class BitDiagram(LatexComponent):
    tokens: list[str]
    caption: str
    labels: list[str] | None = None
    listed: bool = False

    def render(self) -> str:
        rows = []
        clean_tokens = ["".join(token.split()) for token in self.tokens if token and not token.startswith("<")]
        labels = self.labels
        if labels is None:
            labels = [f"word {index}" for index in range(len(clean_tokens))]
        if not clean_tokens:
            return ""
        max_bits = max(len(token) for token in clean_tokens)
        x_scale = min(0.30, 4.85 / max_bits)
        needspace = 0.80 + 0.45 * len(clean_tokens)
        rows.append(rf"\Needspace{{{needspace:.2f}in}}")
        rows.append(r"\begin{center}\vspace{3pt}")
        rows.append(rf"\begin{{tikzpicture}}[x={x_scale:.3f}in,y=0.22in,every node/.style={{font=\scriptsize}}]")
        for index, token in enumerate(clean_tokens):
            total_bits = len(token)
            y = -2.08 * index
            rows.extend(bit_row_commands(token, y, labels[index] if index < len(labels) else f"word {index}", total_bits))
        rows.append(r"\end{tikzpicture}")
        caption_macro = "manualfigurecaption" if self.listed else "manualcaption"
        rows.append(rf"\{caption_macro}{{{tex_escape(caption_title(self.caption))}}}")
        rows.append(r"\end{center}")
        return "\n".join(rows) + "\n"


def bit_diagram(tokens: list[str], caption: str, labels: list[str] | None = None, listed: bool = False) -> str:
    return BitDiagram(tokens, caption, labels, listed).render()


def bit_index_labels(total_bits: int, bits: list[int]) -> list[tuple[float, str]]:
    return [(total_bits - bit - 0.5, str(bit)) for bit in bits]


@dataclass(frozen=True)
class BitFieldFigure(LatexComponent):
    fields: list[tuple[str, int]]
    caption: str
    row_label: str
    total_bits: int
    top_labels: list[tuple[float, str]] | None = None
    listed: bool = False

    def render(self) -> str:
        if not self.fields:
            return ""
        x_scale = min(0.30, 4.85 / self.total_bits)
        rows = [
            r"\Needspace{1.35in}",
            r"\begin{center}\vspace{3pt}",
            rf"\begin{{tikzpicture}}[x={x_scale:.3f}in,y=0.24in,every node/.style={{font=\scriptsize}}]",
            rf"\node[anchor=east] at (-0.35,0.50) {{{tex_escape(self.row_label)}}};",
        ]
        top_labels = self.top_labels
        if top_labels is None:
            top_labels = bit_index_labels(self.total_bits, [self.total_bits - 1, 0])
        for x, text in top_labels:
            rows.append(rf"\node[anchor=south] at ({x:.2f},{1.18:.2f}) {{{tex_escape(text)}}};")
        x = 0
        for label, width in self.fields:
            rows.append(rf"\draw ({x},0) rectangle ({x + width},1);")
            rows.append(rf"\node at ({x + width / 2:.2f},0.50) {{{tex_escape(label)}}};")
            x += width
        rows.extend(
            [
                r"\end{tikzpicture}",
                rf"\{'manualfigurecaption' if self.listed else 'manualcaption'}{{{tex_escape(caption_title(self.caption))}}}",
                r"\end{center}",
            ]
        )
        return "\n".join(rows) + "\n"


def bit_field_figure(
    fields: list[tuple[str, int]],
    caption: str,
    row_label: str,
    total_bits: int,
    top_labels: list[tuple[float, str]] | None = None,
    listed: bool = False,
) -> str:
    return BitFieldFigure(fields, caption, row_label, total_bits, top_labels, listed).render()


@dataclass(frozen=True)
class AbbreviatedBitFieldFigure(LatexComponent):
    fields: list[tuple[str, float]]
    caption: str
    row_label: str
    top_labels: list[tuple[float, str]]
    break_after_first: bool = True
    listed: bool = False

    def render(self) -> str:
        if not self.fields:
            return ""
        total_units = sum(width for _label, width in self.fields)
        x_scale = min(0.42, 4.85 / total_units)
        rows = [
            r"\Needspace{1.35in}",
            r"\begin{center}\vspace{3pt}",
            rf"\begin{{tikzpicture}}[x={x_scale:.3f}in,y=0.24in,every node/.style={{font=\scriptsize}}]",
            rf"\node[anchor=east] at (-0.35,0.50) {{{tex_escape(self.row_label)}}};",
        ]
        for x, text in self.top_labels:
            rows.append(rf"\node[anchor=south] at ({x:.2f},{1.18:.2f}) {{{tex_escape(text)}}};")
        x = 0.0
        for index, (label, width) in enumerate(self.fields):
            rows.append(rf"\draw ({x:.2f},0) rectangle ({x + width:.2f},1);")
            rows.append(rf"\node at ({x + width / 2:.2f},0.50) {{{tex_escape(label)}}};")
            x += width
            if index == 0 and self.break_after_first:
                rows.append(
                    rf"\draw[decorate,decoration={{zigzag,amplitude=1.0pt,segment length=3pt}}] "
                    rf"({x:.2f},0.03) -- ({x:.2f},0.97);"
                )
        rows.extend(
            [
                r"\end{tikzpicture}",
                rf"\{'manualfigurecaption' if self.listed else 'manualcaption'}{{{tex_escape(caption_title(self.caption))}}}",
                r"\end{center}",
            ]
        )
        return "\n".join(rows) + "\n"


def abbreviated_bit_field_figure(
    fields: list[tuple[str, float]],
    caption: str,
    row_label: str,
    top_labels: list[tuple[float, str]],
    break_after_first: bool = True,
    listed: bool = False,
) -> str:
    return AbbreviatedBitFieldFigure(fields, caption, row_label, top_labels, break_after_first, listed).render()


def boundary_bit_field_labels(total_bits: int, fields: list[tuple[str, int]], y: float) -> list[str]:
    """Place high/low bit numbers at field edges without centered-label overlap."""
    rows: list[str] = []
    x = 0
    high_bit = total_bits - 1
    for _label, width in fields:
        low_bit = high_bit - width + 1
        rows.append(rf"\node[anchor=south west] at ({x:.2f},{y:.2f}) {{{tex_escape(high_bit)}}};")
        rows.append(rf"\node[anchor=south east] at ({x + width:.2f},{y:.2f}) {{{tex_escape(low_bit)}}};")
        x += width
        high_bit = low_bit - 1
    return rows


def multiline_node(*lines: Any) -> str:
    return r"\\".join(tex_escape(line) for line in lines)


def paging_mode_figure(mode: str, fields: list[tuple[str, int]], index_labels: list[str], caption: str) -> str:
    bit_x = 0.55
    bit_y = 6.02
    bit_width = 5.15
    bit_height = 0.40
    unit = bit_width / 64.0
    rows = [
        r"\begin{center}\vspace{3pt}",
        r"\begin{tikzpicture}[x=1in,y=1in,every node/.style={font=\scriptsize},>=stealth]",
        rf"\node[anchor=east] at ({bit_x - 0.06:.2f},{bit_y + bit_height / 2:.2f}) {{{tex_escape(mode)}}};",
    ]

    index_fields: dict[str, tuple[float, int, int]] = {}
    offset_center = bit_x + bit_width
    sign_center: float | None = None
    guide_style = "black,densely dashed,line width=0.35pt"
    cursor = bit_x
    high_bit = 63
    for label, width_bits in fields:
        low_bit = high_bit - width_bits + 1
        width = width_bits * unit
        center = cursor + width / 2
        rows.append(rf"\node[anchor=south west] at ({cursor:.2f},{bit_y + bit_height + 0.04:.2f}) {{{tex_escape(high_bit)}}};")
        rows.append(rf"\node[anchor=south east] at ({cursor + width:.2f},{bit_y + bit_height + 0.04:.2f}) {{{tex_escape(low_bit)}}};")
        rows.append(rf"\draw ({cursor:.2f},{bit_y:.2f}) rectangle ({cursor + width:.2f},{bit_y + bit_height:.2f});")
        rows.append(rf"\node[align=center] at ({center:.2f},{bit_y + bit_height / 2:.2f}) {{{tex_escape(label)}}};")
        if label == "sign":
            sign_center = center
        elif label == "offset":
            offset_center = center
        else:
            index_fields[label.split()[0]] = (center, high_bit, low_bit)
        cursor += width
        high_bit = low_bit - 1

    if sign_center is not None:
        rows.extend(
            [
                rf"\node[draw,align=center,minimum width=0.78in,minimum height=0.30in] (canon) at (0.95,5.42) {{{multiline_node('canonical', 'check')}}};",
                rf"\draw[->,{guide_style}] ({sign_center:.2f},{bit_y:.2f}) -- ({sign_center:.2f},5.62) -- (canon.north);",
            ]
        )

    first_y = 4.78
    row_step = 0.67
    root_x = 0.70
    table_x = 1.75
    entry_x = 3.25
    guide_rail_base_x = entry_x + 0.68
    guide_top_base_y = bit_y - 0.16
    previous_entry = ""
    previous_y = first_y
    last_entry = ""
    last_y = first_y
    for index, label in enumerate(index_labels):
        y = first_y - index * row_step
        table_id = f"tbl{index}"
        entry_id = f"ent{index}"
        field_center, field_hi, field_lo = index_fields.get(label, (bit_x, 0, 0))
        is_leaf = index == len(index_labels) - 1
        entry_label = (
            multiline_node("selected", f"{label} leaf PTE", "PFN + flags")
            if is_leaf
            else multiline_node("selected", f"{label} entry", "next table")
        )
        rows.append(
            rf"\node[draw,align=center,minimum width=0.82in,minimum height=0.34in,inner sep=1.5pt] ({table_id}) at ({table_x:.2f},{y:.2f}) {{{multiline_node(label, 'table page')}}};"
        )
        rows.append(
            rf"\node[draw,align=center,minimum width=1.12in,minimum height=0.42in,inner sep=1.5pt] ({entry_id}) at ({entry_x:.2f},{y:.2f}) {{{entry_label}}};"
        )
        if index == 0:
            rows.append(
                rf"\node[draw,align=center,minimum width=0.72in,minimum height=0.34in,inner sep=1.5pt] (root) at ({root_x:.2f},{y:.2f}) {{{multiline_node('PTCR', 'root_page')}}};"
            )
            rows.append(rf"\draw[->] (root.east) -- ({table_id}.west);")
        else:
            prev_bottom = previous_y - 0.21
            table_top = y + 0.17
            route_y = (prev_bottom + table_top) / 2
            rows.append(
                rf"\draw[->] ({previous_entry}.south) -- ({entry_x:.2f},{route_y:.2f}) -- ({table_x:.2f},{route_y:.2f}) -- ({table_id}.north);"
            )
        rows.append(
            rf"\draw[->] ({table_id}.east) -- node[above,align=center,font=\tiny] {{{multiline_node(f'{label} idx', f'bits {field_hi}..{field_lo}')}}} ({entry_id}.west);"
        )
        guide_rail_x = guide_rail_base_x + index * 0.10
        guide_top_y = guide_top_base_y - index * 0.04
        rows.append(
            rf"\draw[->,{guide_style}] ({field_center:.2f},{bit_y:.2f}) -- ({field_center:.2f},{guide_top_y:.2f}) -- "
            rf"({guide_rail_x:.2f},{guide_top_y:.2f}) -- ({guide_rail_x:.2f},{y:.2f}) -- ({entry_id}.east);"
        )
        previous_entry = entry_id
        previous_y = y
        last_entry = entry_id
        last_y = y

    bottom_y = first_y - (len(index_labels) - 1) * row_step
    frame_y = bottom_y - 0.74
    plus_x = 3.12
    phys_x = 4.55
    rows.extend(
        [
            rf"\node[draw,align=center,minimum width=1.10in,minimum height=0.36in] (frame) at ({table_x:.2f},{frame_y:.2f}) {{{multiline_node('physical', 'page frame')}}};",
            rf"\draw[->] ({last_entry}.south) -- ({entry_x:.2f},{(last_y - 0.21 + frame_y + 0.18) / 2:.2f}) -- ({table_x:.2f},{(last_y - 0.21 + frame_y + 0.18) / 2:.2f}) -- (frame.north);",
            rf"\node[draw,circle,inner sep=1.8pt] (plus) at ({plus_x:.2f},{frame_y:.2f}) {{+}};",
            rf"\node[draw,align=center,minimum width=1.03in,minimum height=0.36in] (phys) at ({phys_x:.2f},{frame_y:.2f}) {{{multiline_node('physical', 'address')}}};",
            r"\draw[->] (frame.east) -- node[above] {PFN} (plus.west);",
            r"\draw[->] (plus.east) -- (phys.west);",
            rf"\draw[->,{guide_style}] ({offset_center:.2f},{bit_y:.2f}) -- ({offset_center:.2f},{guide_top_base_y - len(index_labels) * 0.04:.2f}) -- "
            rf"({guide_rail_base_x + len(index_labels) * 0.10:.2f},{guide_top_base_y - len(index_labels) * 0.04:.2f}) -- "
            rf"({guide_rail_base_x + len(index_labels) * 0.10:.2f},{frame_y + 0.20:.2f}) -- "
            rf"({plus_x:.2f},{frame_y + 0.20:.2f}) -- (plus.north);",
            rf"\node[draw,align=left,minimum width=4.55in,inner sep=2.5pt] at (3.02,{frame_y - 0.58:.2f}) {{{multiline_node('Each index selects one entry in its table. Non-leaf entries point to the next table;', 'the leaf PTE supplies the physical frame number and access attributes.')}}};",
            r"\end{tikzpicture}",
            listed_figure_caption(caption),
            r"\end{center}",
        ]
    )
    return "\n".join(rows) + "\n"


def register_model_figure(spec: dict[str, Any]) -> str:
    d_regs = register_class_names(spec, "D")
    a_regs = register_class_names(spec, "A")
    sp_regs = register_class_names(spec, "SP")
    pc_regs = register_class_names(spec, "PC")
    f_regs = register_class_names(spec, "F")
    s_regs = special_register_class_registers(spec, "S")
    cr_regs = control_register_class_registers(spec, "CR")
    data_bank_selector = data_register_banking_selector_name(spec)
    d_width = register_class_width(spec, "D")
    a_width = register_class_width(spec, "A")
    sp_width = register_class_width(spec, "SP")
    pc_width = register_class_width(spec, "PC")
    f_width = register_class_width(spec, "F")
    s_width = special_register_class_width(spec, "S")
    cr_width = control_register_class_width(spec, "CR")
    integer_state_regs = ["FLAGS", "STATUS"]
    fpu_state_regs = ["FFLAGS", "FSTATUS"]
    integer_state_width = max(special_register_width(spec, name) for name in integer_state_regs)
    fpu_state_width = max(special_register_width(spec, name) for name in fpu_state_regs)
    canvas_width = max(d_width, a_width, sp_width, pc_width, f_width, s_width, cr_width, integer_state_width, fpu_state_width)
    reg_w = 1.70
    rows: list[str] = [
        r"\begin{center}",
        r"\resizebox{0.98\linewidth}{!}{%",
        r"\begin{tikzpicture}[x=1in,y=1in,every node/.style={font=\scriptsize}]",
        rf"\def\regw{{{reg_w:.2f}}}",
        r"\def\rowh{0.18}",
        r"\def\gap{0.055}",
    ]

    def compact_registers(names: list[str], limit: int = 6) -> list[str]:
        if len(names) <= limit:
            return [str(name) for name in names]
        head = [str(name) for name in names[: max(1, limit - 2)]]
        return [*head, "...", str(names[-1])]

    def byte_lane_marks(width_bits: int) -> list[int]:
        candidates = [width_bits - 1, width_bits // 2 - 1, width_bits // 4 - 1, width_bits // 8 - 1, 0]
        out: list[int] = []
        for mark in candidates:
            if 0 <= mark < width_bits and mark not in out:
                out.append(mark)
        return out

    def emit_group(
        x0: float,
        start_row: int,
        names: list[str],
        group_label: str,
        *,
        width_bits: int,
        midline: bool = True,
        label_side: str = "right",
        label_limit_x: float | None = None,
        bit_marks: list[int] | None = None,
        align: str = "left",
    ) -> None:
        if not names:
            return
        display_w = reg_w * width_bits / canvas_width
        draw_x0 = x0 + (reg_w - display_w if align == "right" else 0.0)
        if bit_marks is None:
            bit_marks = [width_bits - 1, width_bits // 2 - 1, 0] if midline else [width_bits - 1, 0]

        def mark_x(mark: int) -> float:
            if mark >= width_bits - 1:
                return draw_x0
            if mark <= 0:
                return draw_x0 + display_w
            return draw_x0 + display_w * (width_bits - (mark + 1)) / width_bits

        label_tex = r"\\".join(tex_escape(part) for part in group_label.split("\\"))
        y_top = -start_row * 0.235
        for mark in bit_marks:
            rows.append(rf"\node[anchor=south] at ({mark_x(mark):.3f},{y_top + 0.02:.3f}) {{{mark}}};")
        for offset, name in enumerate(names):
            y = -(start_row + offset) * 0.235 - 0.18
            rows.append(rf"\draw ({draw_x0:.3f},{y:.3f}) rectangle ({draw_x0 + display_w:.3f},{y + 0.18:.3f});")
            for mark in bit_marks[1:-1]:
                split_x = mark_x(mark)
                rows.append(rf"\draw ({split_x:.3f},{y:.3f}) -- ({split_x:.3f},{y + 0.18:.3f});")
            rows.append(rf"\node[anchor=west] at ({draw_x0 + display_w + 0.08:.3f},{y + 0.09:.3f}) {{{tex_escape(name)}}};")
        y_bottom = -(start_row + len(names) - 1) * 0.235 - 0.18
        brace_x = draw_x0 + display_w + 0.72
        tick = 0.14
        bracket_top = y_top
        rows.append(
            rf"\draw ({brace_x - tick:.3f},{bracket_top:.3f}) -- "
            rf"({brace_x:.3f},{bracket_top:.3f}) -- "
            rf"({brace_x:.3f},{y_bottom:.3f}) -- "
            rf"({brace_x - tick:.3f},{y_bottom:.3f});"
        )
        label_y = (bracket_top + y_bottom) / 2
        if label_side == "left":
            limit_x = label_limit_x if label_limit_x is not None else brace_x - 0.12
            rows.append(rf"\node[anchor=east,align=right] at ({limit_x:.3f},{label_y:.3f}) {{\shortstack[r]{{{label_tex}}}}};")
        else:
            rows.append(rf"\node[anchor=west] at ({brace_x + 0.18:.3f},{label_y:.3f}) {{\shortstack[l]{{{label_tex}}}}};")

    right_x = 3.45
    left_row = 0
    emit_group(0.0, left_row, d_regs, f"DATA\\REGISTERS\\D[{data_bank_selector}]", width_bits=d_width, bit_marks=byte_lane_marks(d_width))
    left_row += len(d_regs) + 1
    emit_group(0.0, left_row, a_regs, "ADDRESS\\REGISTERS", midline=False, width_bits=a_width)
    left_row += len(a_regs) + 1
    emit_group(0.0, left_row, sp_regs, "STACK\\POINTER", midline=False, width_bits=sp_width)
    left_row += 2
    emit_group(0.0, left_row, pc_regs, "PROGRAM\\COUNTER", midline=False, width_bits=pc_width)
    left_row += 2
    emit_group(0.0, left_row, integer_state_regs, "INTEGER\\STATE", midline=False, width_bits=integer_state_width, align="right")

    right_row = 0
    f_display_regs = compact_registers(f_regs, limit=5)
    emit_group(right_x, right_row, f_display_regs, "F\\REGISTERS", width_bits=f_width)
    right_row += len(f_display_regs) + 1
    emit_group(right_x, right_row, fpu_state_regs, "FPU\\STATE", midline=False, width_bits=fpu_state_width, align="right")
    right_row += 3
    s_display_regs = compact_registers(s_regs, limit=7)
    emit_group(right_x, right_row, s_display_regs, "SEGMENT\\REGISTERS", midline=False, width_bits=s_width)
    right_row += len(s_display_regs) + 1
    cr_display_regs = compact_registers(cr_regs, limit=7)
    emit_group(right_x, right_row, cr_display_regs, "CONTROL\\REGISTERS", midline=False, width_bits=cr_width)
    rows.extend(
        [
            r"\end{tikzpicture}",
            r"}",
            listed_figure_caption("User Programming Model"),
            r"\end{center}",
        ]
    )
    return "\n".join(rows) + "\n"


def supervisor_stack_frame(control: dict[str, Any]) -> dict[str, Any]:
    frame = control.get("supervisor_stack_frame") if isinstance(control, dict) else None
    if isinstance(frame, dict):
        return frame
    return {}


def stack_frame_figure(control: dict[str, Any]) -> str:
    frame = supervisor_stack_frame(control)
    slots = frame.get("layout") or []
    if not slots:
        return ""
    base_size = int(frame.get("base_size_bytes", len(slots) * int(frame.get("slot_size_bytes", 8))))
    rows = [
        r"\begin{center}\vspace{3pt}",
        r"\begin{tikzpicture}[x=1in,y=0.23in,every node/.style={font=\scriptsize}]",
        r"\node[anchor=south] at (0.00,0.26) {63};",
        r"\node[anchor=south] at (4.60,0.26) {0};",
    ]

    def draw_slot(row_index: int, offset: int, name: str, *, dashed: bool = False) -> None:
        y = -0.58 * row_index
        style = "[densely dashed] " if dashed else " "
        rows.append(rf"\node[anchor=east] at (-0.28,{y - 0.21:.2f}) {{\texttt{{+0x{offset:02X}}}}};")
        rows.append(rf"\draw{style}(0,{y:.2f}) rectangle (4.60,{y - 0.42:.2f});")
        rows.append(rf"\node at (2.30,{y - 0.21:.2f}) {{{tex_escape(name)}}};")

    draw_slot(0, base_size, "type-selected payload slots", dashed=True)
    for index, slot in enumerate(reversed(slots), start=1):
        offset = int(slot.get("offset", 0))
        name = str(slot.get("name", "reserved"))
        draw_slot(index, offset, name)
    rows.extend(
        [
            r"\end{tikzpicture}",
            listed_figure_caption("Supervisor Entry Stack Frame"),
            r"\end{center}",
        ]
    )
    return "\n".join(rows) + "\n"
