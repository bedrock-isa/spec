"""Effective-addressing section rendering for the ISA reference manual."""

from __future__ import annotations

from typing import Any

from .common import compact_text, readable_text, render_latex_template, tex_code, tex_escape
from .diagrams import bit_diagram, bit_field_figure, bit_index_labels


EA_FORM_TEXT_NEEDSPACE_IN = 2.35


def is_immediate_form(form: dict[str, Any]) -> bool:
    return form.get("class") == "immediate" or str(form.get("name", "")).startswith("IMM")


def is_compact_ea_escape(form: dict[str, Any]) -> bool:
    return str(form.get("name", "")) in {"EXTENDED", "S32_INDEXED_EXTENDED"}


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
        entry = ea_manual_entry(spec, form)
        if is_compact_ea_escape(entry):
            continue
        compact_entries.append((entry, str(form.get("pattern", ""))))
    for form in spec.get("ea", {}).get("extended_ea_forms", []) or []:
        entry = ea_manual_entry(spec, form)
        escape = str(form.get("escape", "EXTENDED"))
        extended_entries.append((entry, f"{escape} mode=0x{int(form.get('value', 0)):x}"))
    return render_latex_template(
        "effective_address_modes.tex",
        {
            "COMPACT_ADDRESSING_BLOCKS": ea_addressing_blocks(compact_entries, extended=False),
            "EXTENDED_EA_SEQUENCE": extended_ea_sequence_figure(spec),
            "EXTENDED_EA_DESCRIPTOR": extended_ea_figure(spec),
            "EXTENDED_EA_INDEXED_EXTRA": extended_ea_indexed_extra_figure(spec),
            "EXTENDED_ADDRESSING_BLOCKS": ea_addressing_blocks(extended_entries, extended=True),
        },
    )


def ea_manual_entry(spec: dict[str, Any], form: dict[str, Any]) -> dict[str, Any]:
    return dict(form)


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
    return EA_FORM_TEXT_NEEDSPACE_IN + ea_flow_needspace(form)


def ea_flow_needspace(form: dict[str, Any]) -> float:
    if is_compact_ea_escape(form):
        return 0.0
    if form.get("register_class") or is_immediate_form(form):
        return 1.55
    if form.get("index"):
        return 3.30
    if displacement_token(form.get("displacement", "")):
        return 2.35
    return 2.10


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
    if is_compact_ea_escape(form):
        if form.get("index_extension") == "signed32_to_64":
            return "one descriptor word followed by signed-32 indexed mode payload words"
        return "one descriptor word followed by mode-specific payload words"
    displacement = form.get("displacement")
    absolute = form.get("absolute")
    if displacement and str(displacement) != "none":
        words = payload_word_count(form)
        return payload_with_descriptor(extended, f"{word_count_text(words)} {signed_size_text(displacement, 'displacement')} {plural(words, 'word')}")
    if absolute:
        return payload_with_descriptor(extended, f"a {word_count_text(payload_word_count(form))}-word {signed_size_text(absolute, 'absolute address')}")
    words = payload_word_count(form)
    if extended and words == 0:
        return "descriptor word only"
    if is_immediate_form(form):
        return f"{word_count_text(words)} immediate payload {plural(words, 'word')}"
    if words > 0:
        return payload_with_descriptor(extended, f"{word_count_text(words)} payload {plural(words, 'word')}")
    return "no payload words"


def register_value_text(register_class: Any) -> str:
    text = str(register_class)
    if text == "PC":
        return text
    if text == "SP":
        return "contents(SP)"
    return f"contents({text}n)"


def ea_form_description(form: dict[str, Any], extended: bool) -> str:
    return tex_escape(compact_text(ea_form_description_text(form, extended)))


def ea_form_description_text(form: dict[str, Any], extended: bool) -> str:
    if is_compact_ea_escape(form):
        if form.get("index_extension") == "signed32_to_64":
            return "Compact escape to the signed-32 indexed extended EA descriptor."
        return "Compact escape to the extended EA descriptor."
    register_class = form.get("register_class")
    if register_class:
        register_labels = {"D": "data-register", "A": "address-register", "SP": "stack-pointer"}
        register_names = {"D": "Dn", "A": "An", "SP": "SP"}
        label = register_labels.get(str(register_class), f"{register_class}-register")
        selected = register_names.get(str(register_class), str(register_class))
        return f"Direct {label} operand. The EA field selects {selected} and does not imply a memory access."
    if is_immediate_form(form):
        text = "Immediate operand supplied by following payload words."
        if form.get("sign_extension") == "operand_size":
            text += " The value is sign-extended to the instruction operand size."
        elif form.get("sign_extension") == "none":
            text += " The value is not sign-extended."
        return text
    pieces: list[str] = []
    if form.get("absolute"):
        pieces.append(("Segment-selectable " if form.get("segment_selectable") else "") + "absolute memory operand")
        pieces.append(f"using a {signed_size_text(form['absolute'], 'address payload')}")
    elif form.get("index"):
        prefix = "Segment-selectable " if form.get("segment_selectable") else ""
        if form.get("index_extension") == "signed32_to_64":
            prefix += "signed-32 indexed "
        else:
            prefix += "indexed "
        pieces.append(prefix + "memory operand")
        pieces.append(f"using {base_operand_text(form)}, {index_operand_text(form)}, and scale")
    elif form.get("base"):
        prefix = "Segment-selectable " if form.get("segment_selectable") else ""
        pieces.append(prefix + base_memory_text(form))
    if displacement_token(form.get("displacement", "")):
        pieces.append(f"with a {signed_size_text(form['displacement'], 'displacement payload')}")
    if form.get("fixed_segment"):
        pieces.append(f"using fixed {form['fixed_segment']} segment selection")
    if form.get("segment_field") == "reserved_zero":
        pieces.append("with the descriptor segment field reserved")
    if form.get("default_segment_syntax"):
        pieces.append("omitted segment syntax assembles to the default data segment")
    if form.get("update_eligible"):
        pieces.append("address-update prefixes may use this form")
    return ". ".join(piece.rstrip(".") for piece in pieces if piece) + "."


def payload_with_descriptor(extended: bool, text: str) -> str:
    return f"descriptor word plus {text}" if extended else text


def payload_word_count(form: dict[str, Any]) -> int:
    words = form.get("extra_words")
    if isinstance(words, int):
        return words
    if words is not None and str(words).isdigit():
        return int(str(words))
    extra = ea_extra_words(form)
    if extra.startswith("+") and extra[1:].isdigit():
        return int(extra[1:])
    return 0


def word_count_text(words: int) -> str:
    names = {0: "zero", 1: "one", 2: "two", 4: "four"}
    return names.get(words, str(words))


def plural(count: int, noun: str) -> str:
    return noun if count == 1 else noun + "s"


def signed_size_text(value: Any, noun: str) -> str:
    text = str(value)
    sign = "signed" if text.startswith("signed") else "unsigned" if text.startswith("unsigned") else ""
    bits = "".join(ch for ch in text if ch.isdigit())
    return " ".join(part for part in (sign, f"{bits}-bit" if bits else "", noun) if part)


def base_operand_text(form: dict[str, Any]) -> str:
    base = str(form.get("base", ""))
    return {"A": "An", "SP": "SP", "PC": "PC"}.get(base, base)


def index_operand_text(form: dict[str, Any]) -> str:
    return "Dn[31:0]" if form.get("index_extension") == "signed32_to_64" else "Dn"


def base_memory_text(form: dict[str, Any]) -> str:
    base = str(form.get("base", ""))
    disp = displacement_token(form.get("displacement", ""))
    if base == "A":
        return "address-register relative memory operand" if disp else "address-register indirect memory operand"
    if base == "PC":
        return "program-counter relative memory operand"
    if base == "SP":
        return "stack-pointer relative memory operand"
    return readable_text(base) + " memory operand"


def ea_flow_figure(form: dict[str, Any], title: str, extended: bool) -> str:
    flow = ea_flow_macro_call(form, title, extended)
    return flow + "\n" if flow else ""


def ea_flow_caption(form: dict[str, Any], title: str) -> str:
    if form.get("register_class") or is_immediate_form(form):
        return f"Direct operand selection for {title}"
    return f"Address calculation for {title}"


def latex_macro_call(name: str, *args: Any) -> str:
    return "\\" + name + "".join("{" + tex_escape(arg) + "}" for arg in args)


def ea_register_source(form: dict[str, Any]) -> tuple[str, str]:
    reg_class = str(form.get("register_class"))
    if reg_class == "D":
        return "DATA REGISTER", "Dn CONTENTS"
    if reg_class == "A":
        return "ADDRESS REGISTER", "An CONTENTS"
    if reg_class == "SP":
        return "STACK POINTER", "SP CONTENTS"
    return "REGISTER", f"{reg_class} CONTENTS"


def ea_base_source(form: dict[str, Any]) -> tuple[str, str]:
    if form.get("absolute"):
        return "ABSOLUTE ADDRESS", "ADDRESS PAYLOAD"
    base = str(form.get("base", ""))
    rows = {"A": "ADDRESS REGISTER", "SP": "STACK POINTER", "PC": "PROGRAM COUNTER"}
    texts = {"A": "An CONTENTS", "PC": "PC", "SP": "SP CONTENTS"}
    return rows.get(base, "BASE REGISTER"), texts.get(base, f"{base} CONTENTS")


def ea_index_text(form: dict[str, Any]) -> str:
    if form.get("index_extension") == "signed32_to_64":
        return "SIGN-EXTEND Dn[31:0]"
    return "Dn CONTENTS"


def ea_flow_macro_call(form: dict[str, Any], title: str, extended: bool) -> str:
    if is_compact_ea_escape(form):
        return ""
    caption = ea_flow_caption(form, title)
    if form.get("register_class"):
        row, source = ea_register_source(form)
        return latex_macro_call("manualeadirectflow", caption, row, source, "REGISTER VALUE")
    if is_immediate_form(form):
        return latex_macro_call("manualeaimmediateflow", caption, "PAYLOAD VALUE", "IMMEDIATE VALUE")
    row, source = ea_base_source(form)
    disp = displacement_token(form.get("displacement", ""))
    if form.get("index"):
        return latex_macro_call(
            "manualeaindexedmemoryflow",
            caption,
            row,
            source,
            f"SIGN-EXTENDED {disp}" if disp else "",
            ea_index_text(form),
            "EFFECTIVE ADDRESS",
        )
    if disp:
        return latex_macro_call(
            "manualeaadditivememoryflow",
            caption,
            row,
            source,
            f"SIGN-EXTENDED {disp}",
            "EFFECTIVE ADDRESS",
        )
    return latex_macro_call(
        "manualeasimplememoryflow",
        caption,
        row,
        source,
        "EFFECTIVE ADDRESS",
    )


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
