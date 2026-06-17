"""Architecture-level LaTeX diagram helpers."""

from __future__ import annotations

from typing import Any

from .common import listed_figure_caption, tex_escape

def register_model_figure(spec: dict[str, Any]) -> str:
    registers = spec.get("registers", {})
    d_count = int((registers.get("register_classes") or {}).get("D", {}).get("count", 8))
    a_count = int((registers.get("register_classes") or {}).get("A", {}).get("count", 8))
    f_count = int((registers.get("register_classes") or {}).get("F", {}).get("count", 0))
    width = int((registers.get("register_classes") or {}).get("D", {}).get("width", 64))
    s_regs = list(((registers.get("special_register_classes") or {}).get("S") or {}).get("registers", []) or [])
    cr_regs = list(((registers.get("control_register_classes") or {}).get("CR") or {}).get("registers", []) or [])
    reg_w = 1.70
    mid_x = reg_w / 2
    rows: list[str] = [
        r"\begin{center}",
        r"\resizebox{0.98\linewidth}{!}{%",
        r"\begin{tikzpicture}[x=1in,y=1in,every node/.style={font=\scriptsize}]",
        rf"\def\regw{{{reg_w:.2f}}}",
        r"\def\rowh{0.18}",
        r"\def\gap{0.055}",
    ]

    def compact_names(prefix: str, count: int) -> list[str]:
        if count <= 0:
            return []
        if count <= 8:
            return [f"{prefix}{i}" for i in range(count)]
        return [f"{prefix}0", f"{prefix}1", f"{prefix}2", "...", f"{prefix}{count - 1}"]

    def compact_registers(names: list[str], limit: int = 6) -> list[str]:
        if len(names) <= limit:
            return [str(name) for name in names]
        head = [str(name) for name in names[: max(1, limit - 2)]]
        return [*head, "...", str(names[-1])]

    def emit_group(
        x0: float,
        start_row: int,
        names: list[str],
        group_label: str,
        *,
        midline: bool = True,
        label_side: str = "right",
        label_limit_x: float | None = None,
        width_bits: int = 64,
        bit_marks: list[int] | None = None,
        align: str = "left",
    ) -> None:
        if not names:
            return
        display_w = reg_w * width_bits / 64.0
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
    emit_group(0.0, left_row, [f"D{i}" for i in range(d_count)], "DATA\\REGISTERS\\D[DBANK]", bit_marks=[63, 31, 15, 7, 0])
    left_row += d_count + 1
    emit_group(0.0, left_row, [f"A{i}" for i in range(a_count)], "ADDRESS\\REGISTERS", midline=False)
    left_row += a_count + 1
    emit_group(0.0, left_row, ["SP"], "STACK\\POINTER", midline=False)
    left_row += 2
    emit_group(0.0, left_row, ["PC"], "PROGRAM\\COUNTER", midline=False)
    left_row += 2
    emit_group(0.0, left_row, ["FLAGS", "STATUS"], "INTEGER\\STATE", midline=False, width_bits=16, align="right")

    right_row = 0
    emit_group(right_x, right_row, compact_names("F", f_count), "F\\REGISTERS")
    right_row += len(compact_names("F", f_count)) + 1
    emit_group(right_x, right_row, ["FFLAGS", "FSTATUS"], "FPU\\STATE", midline=False, width_bits=16, align="right")
    right_row += 3
    emit_group(right_x, right_row, compact_registers(s_regs, limit=7), "SEGMENT\\REGISTERS", midline=False)
    right_row += len(compact_registers(s_regs, limit=7)) + 1
    emit_group(right_x, right_row, compact_registers(cr_regs, limit=7), "CONTROL\\REGISTERS", midline=False)
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
    for index, slot in enumerate(slots):
        y = -0.58 * index
        offset = int(slot.get("offset", 0))
        name = str(slot.get("name", "reserved"))
        rows.append(rf"\node[anchor=east] at (-0.28,{y - 0.21:.2f}) {{\texttt{{+0x{offset:02X}}}}};")
        rows.append(rf"\draw (0,{y:.2f}) rectangle (4.60,{y - 0.42:.2f});")
        rows.append(rf"\node at (2.30,{y - 0.21:.2f}) {{{tex_escape(name)}}};")
    y = -0.58 * len(slots)
    rows.append(rf"\node[anchor=east] at (-0.28,{y - 0.21:.2f}) {{\texttt{{+0x{base_size:02X}}}}};")
    rows.append(rf"\draw[densely dashed] (0,{y:.2f}) rectangle (4.60,{y - 0.42:.2f});")
    rows.append(rf"\node at (2.30,{y - 0.21:.2f}) {{type-selected payload slots}};")
    rows.extend(
        [
            r"\end{tikzpicture}",
            listed_figure_caption("Supervisor Entry Stack Frame"),
            r"\end{center}",
        ]
    )
    return "\n".join(rows) + "\n"
