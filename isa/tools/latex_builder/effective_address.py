"""Effective-addressing section rendering for the ISA reference manual."""

from __future__ import annotations

from typing import Any

from .common import readable_text, tex_code, tex_escape
from .diagrams import bit_diagram, bit_field_figure, bit_index_labels


def is_immediate_form(form: dict[str, Any]) -> bool:
    return form.get("class") == "immediate" or str(form.get("name", "")).startswith("IMM")


def compact_ea_figure() -> str:
    return bit_field_figure(
        [("mode", 3), ("register/form", 3)],
        "Figure 2-1. Compact Effective-Address Field",
        "EA[5:0]",
        6,
        bit_index_labels(6, [5, 2, 0]),
        listed=True,
    )


def compact_ea_form_map_figure() -> str:
    return bit_diagram(
        ["000ddd", "001aaa", "010aaa", "011aaa", "100aaa", "101xxx", "110xxx", "111110", "111111"],
        "Figure 2-2. Compact EA Form Map",
        ["DREG", "AREG", "[A]", "[A + disp16]", "[A + disp32]", "PC/SP", "ABS/IMM", "S32 XEA", "XEA"],
        listed=True,
    )


def compact_ea_sequence_figure() -> str:
    return bit_diagram(
        ["mmmmrr", "pppppppppppppppp", "pppppppppppppppp"],
        "Figure 2-3. Compact EA Payload Sequence",
        ["EA field", "optional word 1", "optional word 2"],
        listed=True,
    )


def extended_ea_descriptor_layout(spec: dict[str, Any]) -> list[tuple[str, int]]:
    descriptor = spec.get("ea", {}).get("extended_ea_descriptor", {}) or {}
    fields = descriptor.get("fields", {}) or {}
    out: list[tuple[str, int]] = []
    for name, label in (("mode", "mode"), ("segment", "seg"), ("extra", "extra")):
        bits = fields.get(name, {}).get("bits")
        if isinstance(bits, list) and len(bits) == 2:
            width = abs(int(bits[0]) - int(bits[1])) + 1
        else:
            width = {"mode": 4, "segment": 3, "extra": 9}[name]
        out.append((label, width))
    return out


def extended_ea_descriptor_label_bits(spec: dict[str, Any]) -> list[int]:
    descriptor = spec.get("ea", {}).get("extended_ea_descriptor", {}) or {}
    fields = descriptor.get("fields", {}) or {}
    bits: set[int] = set()
    for name in ("mode", "segment", "extra"):
        pair = fields.get(name, {}).get("bits")
        if isinstance(pair, list) and len(pair) == 2:
            bits.update(int(bit) for bit in pair)
    return sorted(bits or {15, 12, 11, 9, 8, 0}, reverse=True)


def extended_ea_extra_width(spec: dict[str, Any]) -> int:
    for label, width in extended_ea_descriptor_layout(spec):
        if label == "extra":
            return width
    return 9


def extended_ea_figure(spec: dict[str, Any]) -> str:
    layout = extended_ea_descriptor_layout(spec)
    return bit_field_figure(
        layout,
        "Figure 2-5. Extended Effective-Address Descriptor",
        "descriptor[15:0]",
        16,
        bit_index_labels(16, extended_ea_descriptor_label_bits(spec)),
        listed=True,
    )


def extended_ea_sequence_figure(spec: dict[str, Any]) -> str:
    descriptor_bits = "".join(
        marker * width
        for marker, (_label, width) in zip(("m", "s", "x"), extended_ea_descriptor_layout(spec))
    )
    return bit_diagram(
        ["11111e", descriptor_bits, "pppppppppppppppp"],
        "Figure 2-4. Extended EA Word Sequence",
        ["compact EA escape", "descriptor", "optional payload"],
        listed=True,
    )


def extended_ea_indexed_extra_figure(spec: dict[str, Any]) -> str:
    extra_width = extended_ea_extra_width(spec)
    fields = [("base", 3), ("index D", 3), ("scale", 2)]
    if extra_width > 8:
        fields.append(("r", extra_width - 8))
    return bit_field_figure(
        fields,
        "Figure 2-6. Representative Indexed Extended-EA Extra Field",
        f"extra[{extra_width - 1}:0]",
        extra_width,
        bit_index_labels(extra_width, sorted({extra_width - 1, extra_width - 3, extra_width - 4, extra_width - 6, 1, 0}, reverse=True)),
        listed=True,
    )

def ea_table(spec: dict[str, Any]) -> str:
    compact_entries = []
    extended_entries = []
    ea_forms = spec.get("ea", {}).get("ea_forms", []) or []
    compact = ea_forms.get("compact", []) if isinstance(ea_forms, dict) else ea_forms
    for form in compact:
        compact_entries.append((form, str(form.get("pattern", ""))))
    for form in spec.get("ea", {}).get("extended_ea_forms", []) or []:
        entry = dict(form)
        escape = str(form.get("escape", "EXTENDED"))
        extended_entries.append((entry, f"{escape} mode=0x{int(form.get('value', 0)):x}"))
    intro = (
        "Effective-address operands are encoded through a compact six-bit EA field. Most instructions that accept EA "
        "therefore share the same operand sublayout, which keeps register and memory forms visually regular. "
        "The high three bits select the addressing family and the low three bits normally carry the register number or a small form selector. "
        "Forms that need displacement, absolute address, immediate data, or an extended descriptor append payload words after the instruction word."
    )
    return "\n".join(
        [
            intro,
            compact_ea_figure(),
            compact_ea_form_map_figure(),
            "Compact EA forms keep the register selector in EA[2:0] whenever the form is register-based. "
            "The PC/SP, absolute, and immediate groups reuse those low bits as form selectors. "
            "The S32 XEA and XEA compact forms are escapes to the descriptor shown below.",
            compact_ea_sequence_figure(),
            r"\subsection{Compact EA Addressing Modes}",
            ea_addressing_blocks(compact_entries, extended=False),
            r"\subsection{Extended EA Descriptor}",
            r"\Needspace{2.8in}",
            extended_ea_sequence_figure(spec),
            extended_ea_figure(spec),
            "The compact XEA form uses the six-bit value 111111; the S32 XEA form uses 111110 and selects the same descriptor layout with signed 32-bit index extension. "
            "Each escape is followed by a 16-bit descriptor. The descriptor mode field selects the extended EA form. Segment-selectable forms use the segment field to select "
            "an explicit or default segment; fixed-segment forms reserve that field and use their architectural segment. "
            "The three-bit segment field encodes default, CS, DS, SS, GS0, GS1, or a reserved selector value. "
            "The extra field carries mode-specific register, index, scale, or selector bits. "
            "Displacements and absolute addresses remain in following payload words instead of being split across opcode fields. "
            "Segment-qualified memory addresses pass through segmentation first when the selected segment is enabled, and then through paging.",
            extended_ea_indexed_extra_figure(spec),
            "For indexed extended EA forms, the extra field is interpreted as a compact base/index/scale descriptor. "
            "The S32 XEA escape uses the same descriptor fields, but sign-extends the low 32 bits of the D-index register before scaling. "
            "Assembly syntax for indexed EA forms always writes the scale term explicitly, including the scale-one case; "
            r"\texttt{[A0 + D1 * 1]} is valid, while \texttt{[A0 + D1]} is not an indexed-EA spelling. "
            "Other extended modes use the same descriptor word but assign the low bits to the fields needed by that mode.",
            r"\subsection{Extended EA Addressing Modes}",
            ea_addressing_blocks(extended_entries, extended=True),
        ]
    )


def ea_row(form: dict[str, Any], encoding: str) -> list[str]:
    words = str(form.get("extra_words", ""))
    if not words:
        words = ea_extra_words(form)
    return [
        tex_code(form.get("name", "")),
        tex_code(form.get("syntax", form.get("name", ""))),
        tex_code(encoding),
        tex_escape(ea_meaning(form)),
        tex_escape(words),
        tex_escape("yes" if form.get("update_eligible") else "no"),
    ]


def ea_meaning(form: dict[str, Any]) -> str:
    cls = str(form.get("class", "-"))
    pieces = [cls]
    if form.get("register_class"):
        pieces.append(f"{form['register_class']} register")
    if form.get("base"):
        pieces.append(f"base {form['base']}")
    if form.get("index"):
        pieces.append(f"index {form['index']}")
    if form.get("index_extension"):
        pieces.append(readable_text(str(form["index_extension"])))
    if form.get("scale"):
        pieces.append("scale " + "/".join(str(value) for value in form["scale"]))
    if form.get("fixed_segment"):
        pieces.append(f"fixed segment {form['fixed_segment']}")
    if form.get("displacement"):
        pieces.append(str(form["displacement"]))
    if form.get("absolute"):
        pieces.append(str(form["absolute"]))
    if form.get("segment_selectable"):
        pieces.append("segment selectable")
    if form.get("segment_field"):
        pieces.append(f"segment field {readable_text(form['segment_field'])}")
    if form.get("extension"):
        pieces.append("uses extended descriptor")
    return readable_text("; ".join(pieces))


def ea_addressing_blocks(entries: list[tuple[dict[str, Any], str]], extended: bool) -> str:
    blocks = []
    for form, encoding in entries:
        blocks.append(ea_addressing_block(form, encoding, extended))
    return "\n".join(blocks)


def ea_addressing_block(form: dict[str, Any], encoding: str, extended: bool) -> str:
    title = extended_ea_form_label(form) if extended else compact_ea_form_label(form)
    syntax = ea_syntax_text(form)
    payload = ea_payload_text(form, extended)
    update = "eligible" if form.get("update_eligible") else "not eligible"
    encoding_label = encoding.replace("mode=", "descriptor mode ")
    heading = rf"\par\smallskip\noindent{{\bfseries {tex_escape(title)}}}\par"
    return "\n".join(
        [
            rf"\Needspace{{{ea_block_needspace(form):.1f}in}}",
            heading,
            ea_form_description(form, extended),
            rf"\manualfield{{Generation:}}{{{tex_escape(ea_generation_text(form, extended))}}}",
            rf"\manualfield{{Assembler Syntax:}}{{{syntax}}}",
            rf"\manualfield{{Encoding:}}{{{tex_code(encoding_label)}}}",
            rf"\manualfield{{Payload:}}{{{tex_escape(payload)}}}",
            rf"\manualfield{{Address Update:}}{{{tex_escape(update)}}}",
            ea_flow_figure(form, title, extended),
        ]
    )


def ea_block_needspace(form: dict[str, Any]) -> float:
    name = str(form.get("name", ""))
    if name in {"EXTENDED", "S32_INDEXED_EXTENDED"}:
        return 2.1
    if form.get("index"):
        return 5.3
    if form.get("register_class") or is_immediate_form(form):
        return 3.6
    if displacement_token(form.get("displacement", "")):
        return 4.4
    return 3.6


def compact_ea_form_label(form: dict[str, Any]) -> str:
    name = str(form.get("name", ""))
    disp = displacement_token(form.get("displacement", ""))
    if form.get("register_class") == "D":
        return "Data Register Direct"
    if form.get("register_class") == "A":
        return "Address Register Direct"
    if form.get("register_class") == "SP":
        return "Stack Pointer Direct"
    if form.get("base") == "A":
        return "Address Register Indirect" + (f" with {disp}" if disp else "")
    if form.get("base") == "PC":
        return "Program Counter Relative" + (f" with {disp}" if disp else "")
    if form.get("base") == "SP":
        return "Stack Pointer Relative" + (f" with {disp}" if disp else "")
    if form.get("absolute"):
        return "Absolute Memory" + absolute_suffix(form.get("absolute"))
    if is_immediate_form(form):
        return "Immediate Operand " + name.removeprefix("IMM")
    if name == "EXTENDED":
        return "Extended Effective Address Escape"
    if name == "S32_INDEXED_EXTENDED":
        return "Signed 32-bit Indexed Extended Effective Address Escape"
    return readable_text(name)


def absolute_suffix(value: Any) -> str:
    text = str(value)
    if text.endswith("32"):
        return " 32-bit"
    if text.endswith("64"):
        return " 64-bit"
    return ""


def ea_syntax_text(form: dict[str, Any]) -> str:
    syntaxes = []
    default_syntax = form.get("default_segment_syntax")
    if default_syntax:
        syntaxes.append(tex_code(default_syntax))
    syntax = form.get("syntax")
    if syntax:
        syntaxes.append(tex_code(syntax))
    elif form.get("register_class") == "D":
        syntaxes.append(tex_code("Dn"))
    elif form.get("register_class") == "A":
        syntaxes.append(tex_code("An"))
    else:
        syntaxes.append(tex_code(form.get("name", "")))
    return " / ".join(syntaxes)


def ea_generation_text(form: dict[str, Any], extended: bool) -> str:
    name = str(form.get("name", ""))
    disp = displacement_token(form.get("displacement", ""))
    if form.get("register_class") == "D":
        return "operand = contents(Dn)"
    if form.get("register_class") == "A":
        return "operand = contents(An)"
    if form.get("register_class") == "SP":
        return "operand = contents(SP)"
    if is_immediate_form(form):
        return "operand = immediate payload"
    if name == "EXTENDED":
        return "decode descriptor and selected extended EA payload"
    if name == "S32_INDEXED_EXTENDED":
        return "decode descriptor and sign-extend D-index low 32 bits before scaling"
    if form.get("absolute"):
        return "EA = absolute payload"
    base = str(form.get("base", ""))
    if form.get("index"):
        index_term = "sign_extend(Dn[31:0]) * scale" if form.get("index_extension") == "signed32_to_64" else "Dn * scale"
        parts = [register_value_text(base), index_term]
        if disp:
            parts.append(disp)
        return "EA = " + " + ".join(parts)
    if base:
        return "EA = " + " + ".join(part for part in [register_value_text(base), disp] if part)
    return "EA selected by descriptor" if extended else "EA selected by compact field"


def ea_payload_text(form: dict[str, Any], extended: bool) -> str:
    words = extended_ea_words(form) if extended else ea_extra_words(form)
    if form.get("name") == "EXTENDED":
        return "one descriptor word, followed by mode-specific payload words"
    disp = displacement_token(form.get("displacement", ""))
    if disp:
        return f"{words} word(s), carrying {disp}"
    if form.get("absolute"):
        return f"{words} word(s), carrying absolute address"
    if form.get("index") and extended:
        if words == "+0":
            return "no displacement payload; base/index/scale are in descriptor extra bits"
        return f"{words} displacement word(s); base/index/scale are in descriptor extra bits"
    if extended:
        if words == "+0":
            return "no displacement payload; descriptor carries segment and extra fields"
        return f"{words} displacement word(s); descriptor carries segment and extra fields"
    return f"{words} extension word(s)"


def register_value_text(register_class: Any) -> str:
    text = str(register_class)
    if text == "PC":
        return text
    if text == "SP":
        return "contents(SP)"
    return f"contents({text}n)"


def ea_form_description(form: dict[str, Any], extended: bool) -> str:
    name = str(form.get("name", ""))
    if form.get("register_class") == "D":
        return "This is a direct register operand. The low three EA bits select a data register, and the instruction uses that register value without a memory access."
    if form.get("register_class") == "A":
        return "This is a direct register operand. The low three EA bits select an address register, and the instruction uses that register value without a memory access."
    if form.get("register_class") == "SP":
        return "This is a direct register operand. The EA code selects the stack pointer, and the instruction uses SP without a memory access."
    if is_immediate_form(form):
        return "The operand value is taken from following payload words. The compact EA code selects the immediate payload width; narrower immediates are sign-extended to the instruction operand size."
    if name in {"EXTENDED", "S32_INDEXED_EXTENDED"}:
        return "The compact EA field escapes to the extended descriptor. The descriptor chooses a segment-aware or indexed addressing form."
    if form.get("absolute"):
        prefix = "The operand address is supplied by following payload words."
        if form.get("segment_selectable"):
            prefix += " The selected segment may pre-translate the absolute address before paging."
        return prefix
    if form.get("index"):
        base = form.get("base", "base register")
        base_text = {
            "A": "an address register",
            "SP": "the stack pointer",
            "PC": "the program counter",
        }.get(str(base), str(base))
        index_text = "a scaled sign-extended 32-bit data-register index" if form.get("index_extension") == "signed32_to_64" else "a scaled data-register index"
        text = f"The operand address is formed from {base_text}, {index_text}, and an optional displacement."
        if form.get("segment_selectable"):
            text += " The segment field selects either the default segment or an explicit segment register."
        elif form.get("fixed_segment"):
            text += f" The address is interpreted through the fixed {form['fixed_segment']} segment; the descriptor segment field is reserved."
        return text
    base = form.get("base")
    if base:
        text = f"This is an indirect memory operand. The instruction first forms an effective address from {base} and the optional displacement payload, then accesses memory at that address."
        if form.get("segment_selectable"):
            text += " Segment pre-translation is applied when the selected segment is enabled."
        elif form.get("fixed_segment"):
            text += f" The address is interpreted through the fixed {form['fixed_segment']} segment."
        if form.get("update_eligible"):
            text += " Address-update prefixes may use this form."
        return text
    return "The effective-address form is selected by the encoded EA mode."


def ea_flow_figure(form: dict[str, Any], title: str, extended: bool) -> str:
    commands = ea_flow_commands(form, extended)
    if not commands:
        return ""
    lines = [
        r"\begin{center}\vspace{2pt}",
        r"\begin{tikzpicture}[x=1in,y=1in,every node/.style={font=\scriptsize},>=stealth]",
    ]
    lines.extend(commands)
    lines.extend(
        [
            r"\end{tikzpicture}",
            rf"\manualcaption{{{tex_escape(ea_flow_caption(form, title))}}}",
            r"\end{center}",
        ]
    )
    return "\n".join(lines)


def ea_flow_caption(form: dict[str, Any], title: str) -> str:
    if form.get("register_class") or is_immediate_form(form):
        return f"Direct operand selection for {title}"
    return f"Address calculation for {title}"


def prm_row_label(label: str, y: float, x_start: float = 1.55, x_end: float = 2.15) -> list[str]:
    return [
        rf"\node[anchor=west] at (0.02,{y:.2f}) {{{tex_escape(label)}}};",
        rf"\draw ({x_start:.2f},{y:.2f}) -- ({x_end:.2f},{y:.2f});",
    ]


def prm_box(
    name: str,
    x: float,
    y: float,
    width: float,
    label: str,
    height: float = 0.26,
    bits: bool = True,
) -> list[str]:
    out = [
        rf"\node[draw,align=center,minimum width={width:.2f}in,minimum height={height:.2f}in] "
        rf"({name}) at ({x:.2f},{y:.2f}) {{{tex_escape(label)}}};"
    ]
    if bits:
        left = x - width / 2
        right = x + width / 2
        out.append(rf"\node[anchor=south] at ({left:.2f},{y + height / 2 + 0.03:.2f}) {{63}};")
        out.append(rf"\node[anchor=south] at ({right:.2f},{y + height / 2 + 0.03:.2f}) {{0}};")
    return out


def prm_labeled_box(
    row_label: str,
    node_name: str,
    y: float,
    text: str,
    x: float = 3.82,
    width: float = 3.05,
    bits: bool = True,
) -> list[str]:
    left = x - width / 2
    return prm_row_label(row_label, y, x_end=left) + prm_box(node_name, x, y, width, text, bits=bits)


def prm_circle(name: str, x: float, y: float, text: str) -> str:
    return rf"\node[draw,circle,inner sep=0pt,minimum size=0.27in] ({name}) at ({x:.2f},{y:.2f}) {{{tex_escape(text)}}};"


def prm_memory_tail(pointer_node: str = "ptr", memory_y: float = -1.62, x: float = 3.82, width: float = 3.10) -> list[str]:
    return [
        *prm_labeled_box("MEMORY", "mem", memory_y, "OPERAND", x=x, width=width, bits=False),
        rf"\draw[->] ({pointer_node}.south) -- node[midway,right] {{POINTS TO}} (mem.north);",
    ]


def ea_uses_segment_stage(form: dict[str, Any]) -> bool:
    return bool(form.get("segment_selectable") or form.get("fixed_segment"))


def ea_segment_stage_label(form: dict[str, Any]) -> str:
    fixed = form.get("fixed_segment")
    if fixed:
        return f"{fixed} CHECK / TRANSLATE"
    return "CHECK / TRANSLATE"


def direct_register_flow(form: dict[str, Any]) -> list[str]:
    reg_class = str(form.get("register_class"))
    row = "DATA REGISTER" if reg_class == "D" else "ADDRESS REGISTER"
    reg_name = "Dn" if reg_class == "D" else "An"
    return [
        *prm_labeled_box(row, "reg", 0.18, f"{reg_name} CONTENTS"),
        *prm_labeled_box("OPERAND", "operand", -0.62, "REGISTER VALUE", x=3.82, width=3.05, bits=False),
        r"\draw[->] (reg.south) -- (operand.north);",
    ]


def immediate_flow() -> list[str]:
    return [
        *prm_labeled_box("IMMEDIATE DATA", "imm", 0.20, "PAYLOAD VALUE", x=3.82, width=3.05),
        *prm_labeled_box("OPERAND", "operand", -0.62, "IMMEDIATE VALUE", x=3.82, width=3.05, bits=False),
        r"\draw[->] (imm.south) -- (operand.north);",
    ]


def extended_escape_flow() -> list[str]:
    return [
        *prm_labeled_box("EA FIELD", "escape", 0.42, "111111", x=2.92, width=0.82, bits=False),
        *prm_labeled_box("DESCRIPTOR", "desc", -0.20, "MODE / SEGMENT / EXTRA", x=3.82, width=3.05, bits=False),
        *prm_labeled_box("SELECTED FORM", "selected", -0.88, "EXTENDED EA MODE", x=3.82, width=3.05, bits=False),
        r"\draw[->] (escape.south) -- (desc.north);",
        r"\draw[->] (desc.south) -- (selected.north);",
    ]


def simple_memory_flow(form: dict[str, Any]) -> list[str]:
    commands = []
    base = form.get("base")
    absolute = form.get("absolute")
    if absolute:
        commands.extend(prm_labeled_box("ABSOLUTE ADDRESS", "src", 0.18, "ADDRESS PAYLOAD"))
    else:
        row = {"A": "ADDRESS REGISTER", "SP": "STACK POINTER", "PC": "PROGRAM COUNTER"}.get(str(base), "BASE REGISTER")
        text = {"PC": "PC", "SP": "SP CONTENTS"}.get(str(base), f"{base}n CONTENTS")
        commands.extend(prm_labeled_box(row, "src", 0.18, text))
    if ea_uses_segment_stage(form):
        commands.extend(prm_labeled_box("SEGMENT", "seg", -0.62, ea_segment_stage_label(form), x=3.82, width=3.05, bits=False))
        commands.extend(prm_labeled_box("OPERAND POINTER", "ptr", -1.32, "LINEAR ADDRESS", x=3.82, width=3.05))
        commands.extend(
            [
                r"\draw[->] (src.south) -- (seg.north);",
                r"\draw[->] (seg.south) -- (ptr.north);",
                *prm_memory_tail("ptr", -2.10),
            ]
        )
        return commands
    commands.extend(prm_labeled_box("OPERAND POINTER", "ptr", -0.64, "EFFECTIVE ADDRESS", x=3.82, width=3.05))
    commands.extend(
        [
            r"\draw[->] (src.south) -- (ptr.north);",
            *prm_memory_tail("ptr", -1.42),
        ]
    )
    return commands


def additive_memory_flow(form: dict[str, Any]) -> list[str]:
    commands = []
    base = form.get("base")
    row = {"A": "ADDRESS REGISTER", "SP": "STACK POINTER", "PC": "PROGRAM COUNTER"}.get(str(base), "BASE REGISTER")
    text = {"PC": "PC", "SP": "SP CONTENTS"}.get(str(base), f"{base}n CONTENTS")
    disp = displacement_token(form.get("displacement", ""))
    add_x = 4.62
    commands.extend(prm_labeled_box(row, "base", 0.72, text, x=add_x, width=2.25))
    commands.extend(prm_labeled_box("DISPLACEMENT", "disp", -0.10, f"SIGN-EXTENDED {disp}", x=3.20, width=2.05))
    commands.append(prm_circle("add", add_x, -0.10, "+"))
    commands.extend(
        [
            r"\draw[->] (base.south) -- (add.north);",
            r"\draw[->] (disp.east) -- (add.west);",
        ]
    )
    if ea_uses_segment_stage(form):
        commands.extend(prm_labeled_box("SEGMENT", "seg", -0.86, ea_segment_stage_label(form), x=add_x, width=2.25, bits=False))
        commands.extend(prm_labeled_box("OPERAND POINTER", "ptr", -1.56, "LINEAR ADDRESS", x=add_x, width=2.25))
        commands.extend(
            [
                r"\draw[->] (add.south) -- (seg.north);",
                r"\draw[->] (seg.south) -- (ptr.north);",
                *prm_memory_tail("ptr", -2.34, x=add_x, width=2.25),
            ]
        )
        return commands
    commands.extend(prm_labeled_box("OPERAND POINTER", "ptr", -0.94, "EFFECTIVE ADDRESS", x=add_x, width=2.25))
    commands.extend(
        [
            r"\draw[->] (add.south) -- (ptr.north);",
            *prm_memory_tail("ptr", -1.72, x=add_x, width=2.25),
        ]
    )
    return commands


def indexed_memory_flow(form: dict[str, Any]) -> list[str]:
    commands = []
    base = form.get("base")
    disp = displacement_token(form.get("displacement", ""))
    add_x = 4.48
    mul_x = 3.42
    row = {"A": "ADDRESS REGISTER", "SP": "STACK POINTER", "PC": "PROGRAM COUNTER"}.get(str(base), "BASE REGISTER")
    text = {"A": "An CONTENTS", "PC": "PC", "SP": "SP CONTENTS"}.get(str(base), f"{base} CONTENTS")
    commands.extend(prm_labeled_box(row, "base", 0.92, text, x=add_x, width=2.38))
    if disp:
        commands.extend(prm_labeled_box("DISPLACEMENT", "disp", 0.22, f"SIGN-EXTENDED {disp}", x=3.22, width=2.15))
    index_label = "SIGN-EXTEND Dn[31:0]" if form.get("index_extension") == "signed32_to_64" else "Dn CONTENTS"
    commands.extend(prm_labeled_box("INDEX REGISTER", "idx", -0.48, index_label, x=mul_x, width=1.85))
    commands.extend(prm_labeled_box("SCALE", "scale", -1.18, "SCALE VALUE", x=2.48, width=1.35, bits=False))
    commands.append(prm_circle("mul", mul_x, -1.18, "x"))
    commands.append(prm_circle("add_index", add_x, -1.18, "+"))
    if disp:
        commands.append(prm_circle("add_base", add_x, 0.22, "+"))
        commands.extend(
            [
                r"\draw[->] (base.south) -- (add_base.north);",
                r"\draw[->] (disp.east) -- (add_base.west);",
                r"\draw[->] (add_base.south) -- (add_index.north);",
            ]
        )
    else:
        commands.append(r"\draw[->] (base.south) -- (add_index.north);")
    commands.extend(
        [
            r"\draw[->] (idx.south) -- (mul.north);",
            r"\draw[->] (scale.east) -- (mul.west);",
            r"\draw[->] (mul.east) -- (add_index.west);",
        ]
    )
    if ea_uses_segment_stage(form):
        commands.extend(prm_labeled_box("SEGMENT", "seg", -1.52, ea_segment_stage_label(form), x=add_x, width=2.38, bits=False))
        commands.extend(prm_labeled_box("OPERAND POINTER", "ptr", -2.22, "LINEAR ADDRESS", x=add_x, width=2.38))
        commands.extend(
            [
                r"\draw[->] (add_index.south) -- (seg.north);",
                r"\draw[->] (seg.south) -- (ptr.north);",
                *prm_memory_tail("ptr", -3.00, x=add_x, width=2.38),
            ]
        )
        return commands
    commands.extend(prm_labeled_box("OPERAND POINTER", "ptr", -1.62, "EFFECTIVE ADDRESS", x=add_x, width=2.38))
    commands.extend(
        [
            r"\draw[->] (add_index.south) -- (ptr.north);",
            *prm_memory_tail("ptr", -2.40, x=add_x, width=2.38),
        ]
    )
    return commands


def ea_flow_commands(form: dict[str, Any], extended: bool) -> list[str]:
    name = str(form.get("name", ""))
    if form.get("register_class"):
        return direct_register_flow(form)
    if is_immediate_form(form):
        return immediate_flow()
    if name in {"EXTENDED", "S32_INDEXED_EXTENDED"}:
        return []
    if form.get("index"):
        return indexed_memory_flow(form)
    if displacement_token(form.get("displacement", "")):
        return additive_memory_flow(form)
    return simple_memory_flow(form)


def ea_address_terms(form: dict[str, Any]) -> list[tuple[list[str], str]]:
    terms: list[tuple[list[str], str]] = []
    if form.get("absolute"):
        terms.append((["absolute", "payload"], "absolute"))
        return terms
    base = form.get("base")
    if base:
        terms.append(([register_value_text(base)], "base"))
    if form.get("index"):
        terms.append((["Dn * scale", "index term"], "index"))
    disp = displacement_token(form.get("displacement", ""))
    if disp:
        terms.append(([disp, "payload"], "disp"))
    return terms


def needs_add_node(form: dict[str, Any]) -> bool:
    if form.get("absolute"):
        return False
    count = 0
    if form.get("base"):
        count += 1
    if form.get("index"):
        count += 1
    if displacement_token(form.get("displacement", "")):
        count += 1
    return count >= 2


def source_y_positions(count: int) -> list[float]:
    if count <= 1:
        return [0.0]
    if count == 2:
        return [0.42, -0.42]
    if count == 3:
        return [0.68, 0.0, -0.68]
    return [0.86, 0.29, -0.29, -0.86]


def ea_flow_steps(form: dict[str, Any], extended: bool) -> list[str]:
    name = str(form.get("name", ""))
    disp = displacement_token(form.get("displacement", ""))
    if form.get("register_class") == "D":
        return ["EA[2:0]", "Dn", "operand"]
    if form.get("register_class") == "A":
        return ["EA[2:0]", "An", "operand"]
    if is_immediate_form(form):
        return ["payload", "immediate", "operand"]
    if name == "EXTENDED":
        return ["EA=111111", "descriptor", "extended EA"]
    if name == "S32_INDEXED_EXTENDED":
        return ["EA=111110", "descriptor", "signed 32-bit indexed extended EA"]
    if form.get("absolute"):
        steps = ["absolute payload"]
        if ea_uses_segment_stage(form):
            steps.append(str(form.get("fixed_segment") or "segment"))
        steps.append("memory operand")
        return steps
    steps = []
    base = form.get("base")
    if base:
        steps.append(register_value_text(base))
    if form.get("index"):
        steps.append("sign_extend(Dn[31:0]) * scale" if form.get("index_extension") == "signed32_to_64" else "Dn * scale")
    if disp:
        steps.append(disp)
    if len(steps) > 1:
        steps.append("sum")
    if ea_uses_segment_stage(form):
        steps.append(str(form.get("fixed_segment") or "segment"))
    steps.append("memory operand")
    return steps


def extended_ea_syntax_cell(form: dict[str, Any]) -> str:
    lines = []
    default_syntax = form.get("default_segment_syntax")
    if default_syntax:
        lines.append(tex_code(default_syntax))
    lines.append(tex_code(form.get("syntax", form.get("name", ""))))
    return r"\begin{tabular}[t]{@{}l@{}}" + r"\\".join(lines) + r"\end{tabular}"


def extended_ea_words(form: dict[str, Any]) -> str:
    words = form.get("extra_words")
    if words is None or words == "":
        return ea_extra_words(form)
    return f"+{words}"


def displacement_token(value: Any) -> str:
    text = str(value)
    if text == "none" or not text:
        return ""
    if text.endswith("16"):
        return "disp16"
    if text.endswith("32"):
        return "disp32"
    if text.endswith("64"):
        return "disp64"
    return text


def extended_ea_form_label(form: dict[str, Any]) -> str:
    disp = displacement_token(form.get("displacement", ""))
    if form.get("index"):
        prefix = "Signed 32-bit Indexed" if form.get("index_extension") == "signed32_to_64" else "Indexed"
        return prefix + (f" with {disp}" if disp else "")
    if form.get("base") == "A":
        return "Segment-Qualified Address Register Indirect" + (f" with {disp}" if disp else "")
    if form.get("absolute"):
        absolute = str(form.get("absolute"))
        if absolute.endswith("32"):
            return "Segment-Qualified Absolute Memory 32-bit"
        if absolute.endswith("64"):
            return "Segment-Qualified Absolute Memory 64-bit"
        return "Segment-Qualified Absolute Memory"
    return readable_text(form.get("name", "extended"))


def extended_ea_operand_text(form: dict[str, Any]) -> str:
    pieces = []
    if form.get("base"):
        pieces.append(f"base {form['base']}")
    if form.get("index"):
        pieces.append(f"index {form['index']}")
    if form.get("scale"):
        pieces.append("scale " + "/".join(str(value) for value in form["scale"]))
    disp = displacement_token(form.get("displacement", ""))
    if disp:
        pieces.append(disp)
    if form.get("absolute"):
        pieces.append(str(form["absolute"]).replace("signed", "signed ").replace("unsigned", "unsigned "))
    return ", ".join(pieces) or "none"


def ea_extra_words(form: dict[str, Any]) -> str:
    if form.get("name") in {"EXTENDED", "S32_INDEXED_EXTENDED"}:
        return "+1"
    if "displacement" in form:
        text = str(form.get("displacement"))
        if text.endswith("16"):
            return "+1"
        if text.endswith("32"):
            return "+2"
        if text.endswith("64"):
            return "+4"
    if "absolute" in form:
        text = str(form.get("absolute"))
        if text.endswith("32"):
            return "+2"
        if text.endswith("64"):
            return "+4"
    return "+0"
