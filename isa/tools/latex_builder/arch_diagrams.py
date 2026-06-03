"""Architecture-level LaTeX diagram helpers."""

from __future__ import annotations

from typing import Any

from .common import listed_figure_caption, tex_escape
from .diagrams import (
    abbreviated_bit_field_figure,
    bit_diagram,
    bit_field_figure,
    bit_index_labels,
    paging_mode_figure,
)

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


def flags_register_figure() -> str:
    return bit_field_figure(
        [("0", 12), ("Z", 1), ("N", 1), ("C", 1), ("V", 1)],
        "Figure 1-2. FLAGS Register Format",
        "FLAGS[15:0]",
        16,
        bit_index_labels(16, [15, 3, 2, 1, 0]),
        listed=True,
    )


def status_register_figure() -> str:
    return bit_field_figure(
        [("0", 9), ("IE", 1), ("PM", 1), ("RF", 1), ("TF", 1), ("UA", 1), ("NI", 1), ("IN", 1)],
        "Figure 1-3. STATUS Register Format",
        "STATUS[15:0]",
        16,
        bit_index_labels(16, [15, 6, 5, 4, 3, 2, 1, 0]),
        listed=True,
    )


def segment_register_figure() -> str:
    return abbreviated_bit_field_figure(
        [("base_page", 5.4), ("e", 1.7), ("m", 2.2), ("b", 1.1)],
        "Figure 1-4. Segment Register Format",
        "segment[63:0]",
        [(0, "63"), (5.4, "11"), (7.1, "6"), (9.3, "1"), (10.4, "0")],
        listed=True,
    )


def ptcr_register_figure() -> str:
    return abbreviated_bit_field_figure(
        [("root_page", 5.2), ("PABITS", 2.3), ("LA57", 1.35), ("reserved", 1.9), ("PE", 1.1)],
        "Figure 1-5. PTCR Format",
        "PTCR[63:0]",
        [(0, "63"), (5.2, "11"), (7.5, "7"), (8.85, "6"), (10.75, "1"), (11.85, "0")],
        listed=True,
    )


def ascr_register_figure() -> str:
    return abbreviated_bit_field_figure(
        [("reserved", 4.2), ("ASID", 2.8), ("reserved", 2.8), ("AE", 1.2)],
        "Figure 1-6. ASCR Format",
        "ASCR[63:0]",
        [(0, "63"), (4.2, "31"), (7.0, "15"), (9.8, "1"), (11.0, "0")],
        listed=True,
    )


def icr_register_figure() -> str:
    return abbreviated_bit_field_figure(
        [("ivt_page", 5.0), ("MAX_IDEPTH", 2.35), ("NMI_P", 1.35), ("NMI_L", 1.35), ("DF", 1.05), ("reserved", 1.6), ("V", 0.95)],
        "Figure 1-7. ICR Format",
        "ICR[63:0]",
        [(0, "63"), (5.0, "11"), (7.35, "7"), (8.70, "6"), (10.05, "5"), (11.10, "4"), (12.70, "1"), (13.65, "0")],
        listed=True,
    )


def pte_attribute_figure() -> str:
    return bit_field_figure(
        [("T", 1), ("SW0", 1), ("CP", 2), ("AT", 1), ("D", 1), ("A", 1), ("G", 1), ("U", 1), ("X", 1), ("W", 1), ("P", 1)],
        "Figure 3-1. PTE Low Attribute Bits",
        "PTE[11:0]",
        12,
        bit_index_labels(12, [11, 7, 0]),
        listed=True,
    )


def ivt_entry_figure() -> str:
    return bit_field_figure(
        [("handler address", 8), ("control", 1), ("reserved", 7)],
        "Figure 1-8. Interrupt Vector Table Entry",
        "entry bytes",
        16,
        [(0.5, "0"), (7.5, "7"), (8.5, "8"), (15.5, "15")],
        listed=True,
    )


def ivt_control_byte_figure() -> str:
    return bit_field_figure(
        [("reserved", 4), ("SN", 2), ("0", 1), ("HP", 1)],
        "Figure 1-9. IVT Entry Control Byte",
        "byte 8",
        8,
        bit_index_labels(8, [7, 3, 2, 1, 0]),
        listed=True,
    )


def supervisor_stack_frame(control: dict[str, Any]) -> dict[str, Any]:
    frame = control.get("supervisor_stack_frame") if isinstance(control, dict) else None
    if isinstance(frame, dict):
        return frame
    return {
        "slot_size_bytes": 8,
        "base_size_bytes": 64,
        "frame_size_unit_bytes": 8,
        "layout": [
            {"offset": 0x00, "name": "FRAME_INFO", "description": "frame metadata and entry flags"},
            {"offset": 0x08, "name": "SAVED_DBANK", "description": "saved interrupted DBANK selector in bits 3..0; bits 63..4 are reserved, must be zero"},
            {"offset": 0x10, "name": "FLAGS_STATUS", "description": "saved FLAGS and STATUS state"},
            {"offset": 0x18, "name": "SAVED_PC", "description": "saved program counter"},
            {"offset": 0x20, "name": "SAVED_SP", "description": "saved stack pointer"},
            {"offset": 0x28, "name": "SAVED_CS", "description": "saved code segment selector"},
            {"offset": 0x30, "name": "SAVED_DS", "description": "saved data segment selector"},
            {"offset": 0x38, "name": "SAVED_SS", "description": "saved stack segment selector"},
        ],
        "payload_slots": {
            "ERROR_CODE": {"description": "exception-specific error code"},
            "FAULT_EA": {"description": "faulting effective-address operand information"},
            "FAULT_LINEAR": {"description": "faulting linear address"},
            "FAULT_AUX": {"description": "auxiliary fault information"},
        },
        "repeat_fault_aux": {
            "fields": {
                "counter_register": {"bits": [0, 2], "description": "D-register counter number, D0-D7"},
                "group_start_delta_words": {
                    "bits": [3, 7],
                    "description": "REPG-general/REPG-fast negative word displacement from fault_pc to group start",
                },
                "repeat_kind": {
                    "bits": [8, 9],
                    "description": "repeat context kind: 0=REP/REPcc, 1=REPG-general, 2=REPG-fast, 3=reserved",
                },
                "reserved": {"bits": [10, 63], "description": "reserved, must be zero"},
            }
        },
        "frame_types": [
            {"code": 0x0, "name": "BASIC", "payload": [], "description": "fixed frame only"},
            {"code": 0x1, "name": "ERROR", "payload": ["ERROR_CODE"], "description": "fixed frame plus exception error code"},
            {"code": 0x2, "name": "PAGE_FAULT", "payload": ["ERROR_CODE", "FAULT_EA", "FAULT_LINEAR"], "description": "fixed frame plus page-fault code, effective-address context, and linear address"},
            {"code": 0x3, "name": "AUX_FAULT", "payload": ["ERROR_CODE", "FAULT_EA", "FAULT_LINEAR", "FAULT_AUX"], "description": "fixed frame plus full auxiliary fault context"},
        ],
    }


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


def frame_info_figure() -> str:
    rows = [
        r"\begin{center}\vspace{3pt}",
        r"\begin{tikzpicture}[x=0.130in,y=0.30in,every node/.style={font=\scriptsize}]",
        r"\node[anchor=east] at (-0.40,2.20) {FRAME\_INFO[63:32]};",
        r"\node[anchor=south] at (0,2.88) {63};",
        r"\node[anchor=south] at (32,2.88) {32};",
        r"\draw (0,1.70) rectangle (32,2.70);",
        r"\node at (16,2.20) {reserved};",
        r"\node[anchor=east] at (-0.40,0.50) {FRAME\_INFO[31:0]};",
        r"\node[anchor=south] at (0,1.18) {31};",
        r"\node[anchor=south] at (5,1.18) {27};",
        r"\node[anchor=south east] at (8,1.18) {24};",
        r"\node[anchor=south west] at (9,1.18) {23};",
        r"\node[anchor=south] at (12,1.18) {20};",
        r"\node[anchor=south] at (16,1.18) {16};",
        r"\node[anchor=south] at (24,1.18) {8};",
        r"\node[anchor=south] at (32,1.18) {0};",
        r"\draw (0,0) rectangle (5,1);",
        r"\node at (2.50,0.50) {reserved};",
        r"\draw (5,0) rectangle (8,1);",
        r"\node[rotate=90] at (6.50,0.50) {flags};",
        r"\draw (8,0) rectangle (12,1);",
        r"\node at (10.00,0.50) {frame type};",
        r"\draw (12,0) rectangle (16,1);",
        r"\node at (14.00,0.50) {idepth};",
        r"\draw (16,0) rectangle (24,1);",
        r"\node at (20.00,0.50) {frame size};",
        r"\draw (24,0) rectangle (32,1);",
        r"\node at (28.00,0.50) {vector};",
        r"\end{tikzpicture}",
        listed_figure_caption("FRAME_INFO Format"),
        r"\end{center}\vspace{4pt}",
    ]
    return "\n".join(rows) + "\n"


def translation_pipeline_figure() -> str:
    rows = [
        r"\begin{center}\vspace{3pt}",
        r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={font=\scriptsize},>=stealth,line width=0.82pt]",
        r"\tikzset{box/.style={draw,align=center,minimum height=0.70cm,inner sep=2pt}, lab/.style={fill=white,inner sep=1pt}}",
        r"\node[box,minimum width=1.15cm] (ea) at (0.55,0) {EA\\address};",
        r"\node[box,minimum width=1.30cm] (sel) at (1.95,0) {select\\segment};",
        r"\node[box,minimum width=1.45cm] (check) at (3.65,0) {enabled\\window\\check};",
        r"\node[box,minimum width=2.45cm] (add) at (6.10,1.55) {$m\ne0$, $b=0$\\linear = base + EA};",
        r"\node[box,minimum width=2.45cm] (keep) at (6.10,0) {$m\ne0$, $b=1$\\linear = EA};",
        r"\node[box,minimum width=2.45cm] (disabled) at (6.10,-1.55) {$m=0$\\linear = EA};",
        r"\node[box,minimum width=1.45cm] (lin) at (8.45,0) {linear\\address};",
        r"\node[box,minimum width=2.00cm] (page) at (10.65,0.95) {PTCR.PE=1\\page-table\\translation};",
        r"\node[box,minimum width=2.00cm] (direct) at (10.65,-0.95) {PTCR.PE=0\\use linear\\directly};",
        r"\node[box,minimum width=1.75cm] (out) at (12.90,0) {memory-system\\address};",
        r"\draw[->] (ea.east) -- (sel.west);",
        r"\coordinate (modebranch) at (2.75,0);",
        r"\draw (sel.east) -- (modebranch);",
        r"\draw[->] (modebranch) -- (check.west);",
        r"\draw[->] (modebranch) |- node[lab,pos=0.20,right] {$m=0$} (disabled.west);",
        r"\coordinate (segbranch) at (4.55,0);",
        r"\draw[->] (check.east) -- (segbranch) |- (add.west);",
        r"\draw[->] (check.east) -- (keep.west);",
        r"\draw[->] (check.south) -- ++(0,-0.58) node[lab,below] {window fail: PAGE\_FAULT};",
        r"\coordinate (linmerge) at (7.45,0);",
        r"\draw (add.east) -- ++(0.34,0) |- (linmerge);",
        r"\draw (keep.east) -- (linmerge);",
        r"\draw (disabled.east) -- ++(0.34,0) |- (linmerge);",
        r"\draw[->] (linmerge) -- (lin.west);",
        r"\node[anchor=south] at (6.10,2.02) {segment register mode};",
        r"\coordinate (pebranch) at (9.45,0);",
        r"\draw[->] (lin.east) -- (pebranch) |- (page.west);",
        r"\draw[->] (lin.east) -- (pebranch) |- (direct.west);",
        r"\draw[->] (page.east) -| (out.north);",
        r"\draw[->] (direct.east) -| (out.south);",
        r"\end{tikzpicture}",
        listed_figure_caption("Address Translation Pipeline"),
        r"\end{center}",
    ]
    return "\n".join(rows) + "\n"


def la48_paging_figure() -> str:
    return paging_mode_figure(
        "LA48",
        [("sign", 16), ("L4 idx", 9), ("L3 idx", 9), ("L2 idx", 9), ("L1 idx", 9), ("offset", 12)],
        ["L4", "L3", "L2", "L1"],
        "LA48 Four-Level Page Walk",
    )


def la57_paging_figure() -> str:
    return paging_mode_figure(
        "LA57",
        [("sign", 7), ("L5 idx", 9), ("L4 idx", 9), ("L3 idx", 9), ("L2 idx", 9), ("L1 idx", 9), ("offset", 12)],
        ["L5", "L4", "L3", "L2", "L1"],
        "LA57 Five-Level Page Walk",
    )


def primary_word_figure() -> str:
    return bit_diagram(
        ["----pppppppppppp", "ssssssssssssssss", "xxxxxxxxxxxxxxxx"],
        "Figure 2-7. Instruction Word Format Families",
        ["primary", "descriptor", "payload"],
        listed=True,
    )


def word0_overview_figure() -> str:
    return bit_field_figure(
        [("P", 1), ("L", 3), ("primary opcode/fields", 12)],
        "Word 0 Format",
        "word 0",
        16,
        bit_index_labels(16, [15, 14, 11, 0]),
        listed=True,
    )


def prefix_word_figure() -> str:
    return bit_field_figure(
        [("prefix1", 8), ("prefix0", 8)],
        "Prefix Word Format",
        "word 1",
        16,
        bit_index_labels(16, [15, 8, 7, 0]),
        listed=True,
    )
