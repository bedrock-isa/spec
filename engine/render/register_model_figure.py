"""Catalog-backed architectural register-model figure renderer."""

from __future__ import annotations

from dataclasses import dataclass

from ..register import RegisterGroup, RegisterNamespace
from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider


ROW_HEIGHT = 0.18
ROW_PITCH = 0.235
HEADER_HEIGHT = 0.25
BLOCK_GAP = 0.30
BAND_GAP = 0.41
REGISTER_WIDTH = 1.70
COLUMN_X = (0.0, 3.45)
SUMMARY_HEIGHT = 0.65


@dataclass(frozen=True, slots=True)
class _Block:
    group: RegisterGroup
    rows: tuple[object | None, ...]
    height: float
    summary: bool = False


@dataclass(frozen=True, slots=True)
class _PlacedBlock:
    block: _Block
    column: int
    top: float


@dataclass(frozen=True, slots=True)
class _Band:
    owner: str
    blocks: tuple[_PlacedBlock, ...]
    top: float
    height: float


class RegisterModelFigureRenderer(DocumentFragmentProvider):
    """Expand the register-model figure from the loaded register catalog."""

    PLACEHOLDER = r"\BedrockGeneratedRegisterModelFigure"

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset((self.PLACEHOLDER,))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        if self.PLACEHOLDER not in text:
            return text
        return text.replace(self.PLACEHOLDER, self.render(context.project.registers))

    def render(self, catalog) -> str:
        namespaces = tuple(
            namespace
            for namespace in catalog.namespaces.values()
            if namespace.groups
        )
        lines: list[str] = []
        for namespace in namespaces:
            lines.extend(_render_figure(namespace))
        return "\n".join(lines)


def _render_figure(namespace: RegisterNamespace) -> list[str]:
    band = _layout_band(namespace, 0.0)
    if namespace.diagram is None:
        raise ValueError(f"{namespace.owner}: register namespace has no diagram layout")

    lines = [
        r"\begin{center}",
        r"\begin{minipage}{\linewidth}",
        r"\centering",
        r"\resizebox{0.98\linewidth}{!}{%",
        r"\begin{tikzpicture}[x=1in,y=1in,every node/.style={font=\scriptsize}]",
    ]
    lines.extend(_render_band(band))
    lines.extend(
        (
            r"\end{tikzpicture}",
            "}",
            rf"\BedrockFigureCaption{{{_tex(namespace.diagram.caption)}}}",
            r"\end{minipage}",
            r"\end{center}",
        )
    )
    return lines


def _compact_rows(group: RegisterGroup) -> tuple[object | None, ...]:
    registers = tuple(group.registers.values())
    if len(registers) <= 5:
        return registers
    return (*registers[:3], None, registers[-1])


def _block(group: RegisterGroup, mode: str) -> _Block:
    if mode == "summary":
        return _Block(group, (), SUMMARY_HEIGHT, summary=True)
    registers = tuple(group.registers.values())
    rows = _compact_rows(group) if mode == "compact" else registers
    rows_height = (len(rows) - 1) * ROW_PITCH + ROW_HEIGHT
    return _Block(group, rows, HEADER_HEIGHT + rows_height)


def _column_height(blocks: list[_Block]) -> float:
    if not blocks:
        return 0.0
    return sum(block.height for block in blocks) + BLOCK_GAP * (len(blocks) - 1)


def _layout_band(namespace: RegisterNamespace, top: float) -> _Band:
    diagram = namespace.diagram
    if diagram is None:
        raise ValueError(
            f"{namespace.group_inventory.source}: register namespace with groups "
            "has no diagram layout"
        )
    columns: tuple[list[_Block], list[_Block]] = ([], [])
    for column_index, group_ids in enumerate(diagram.columns):
        for group_id in group_ids:
            group = namespace.groups[group_id]
            default = "compact" if group.register_inventory is None else "all"
            columns[column_index].append(
                _block(group, diagram.display.get(group_id, default))
            )

    heights = tuple(_column_height(column) for column in columns)
    content_height = max(heights, default=0.0)
    placed: list[_PlacedBlock] = []
    for column_index, column in enumerate(columns):
        center_offset = (
            (content_height - heights[column_index]) / 2
            if namespace.owner != "base"
            else 0
        )
        cursor = top + center_offset
        for block in column:
            placed.append(_PlacedBlock(block, column_index, cursor))
            cursor += block.height + BLOCK_GAP
    return _Band(
        namespace.owner,
        tuple(placed),
        top,
        content_height,
    )


def _tex(value: str) -> str:
    return value.replace("_", r"\_")


def _fmt(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def _y(value: float) -> str:
    return _fmt(-value)


def _group_label(group: RegisterGroup) -> str:
    return rf"\shortstack[l]{{{_tex(group.id)}\\REGISTERS}}"


def _bit_labels(group: RegisterGroup, x: float, row_top: float) -> list[str]:
    width = group.width
    label_y = row_top - 0.02
    right = x + REGISTER_WIDTH
    if isinstance(width, int):
        image_width = REGISTER_WIDTH * min(width, 64) / 64
        left = right - image_width
        lines = [
            rf"\node[anchor=south] at ({_fmt(left)},{_y(label_y)}) {{{width - 1}}};",
            rf"\node[anchor=south] at ({_fmt(right)},{_y(label_y)}) {{0}};",
        ]
        if width == 64:
            middle = x + REGISTER_WIDTH / 2
            lines.insert(
                1,
                rf"\node[anchor=south] at ({_fmt(middle)},{_y(label_y)}) {{31}};",
            )
        return lines

    expression = width.expression.replace(" ", "")
    solid_left = x + 0.65
    return [
        rf"\node[anchor=south] at ({_fmt(x)},{_y(label_y)}) {{{expression}-1}};",
        rf"\node[anchor=south] at ({_fmt(solid_left)},{_y(label_y)}) {{{width.minimum - 1}}};",
        rf"\node[anchor=south] at ({_fmt(right)},{_y(label_y)}) {{0}};",
    ]


def _register_image(group: RegisterGroup, x: float, row_top: float) -> list[str]:
    bottom = row_top + ROW_HEIGHT
    right = x + REGISTER_WIDTH
    width = group.width
    if isinstance(width, int):
        image_width = REGISTER_WIDTH * min(width, 64) / 64
        left = right - image_width
        lines = [
            rf"\draw ({_fmt(left)},{_y(row_top)}) rectangle "
            rf"({_fmt(right)},{_y(bottom)});"
        ]
        if width == 64:
            middle = x + REGISTER_WIDTH / 2
            lines.append(
                rf"\draw ({_fmt(middle)},{_y(row_top)}) -- "
                rf"({_fmt(middle)},{_y(bottom)});"
            )
        return lines

    solid_left = x + 0.65
    return [
        rf"\draw[dashed] ({_fmt(x)},{_y(row_top)}) -- "
        rf"({_fmt(solid_left)},{_y(row_top)});",
        rf"\draw ({_fmt(solid_left)},{_y(row_top)}) -- "
        rf"({_fmt(right)},{_y(row_top)}) -- ({_fmt(right)},{_y(bottom)}) -- "
        rf"({_fmt(solid_left)},{_y(bottom)});",
        rf"\draw[dashed] ({_fmt(solid_left)},{_y(bottom)}) -- "
        rf"({_fmt(x)},{_y(bottom)}) -- ({_fmt(x)},{_y(row_top)});",
    ]


def _render_block(placed: _PlacedBlock) -> list[str]:
    block = placed.block
    group = block.group
    x = COLUMN_X[placed.column]
    if block.summary:
        bottom = placed.top + block.height
        bracket_left = x + 2.28
        bracket_right = x + 2.42
        return [
            rf"\draw ({_fmt(x)},{_y(placed.top)}) rectangle "
            rf"({_fmt(x + REGISTER_WIDTH)},{_y(bottom)});",
            rf"\node[align=center] at ({_fmt(x + REGISTER_WIDTH / 2)},"
            rf"{_y((placed.top + bottom) / 2)}) "
            rf"{{{len(group.registers)} named\\registers}};",
            rf"\draw ({_fmt(bracket_left)},{_y(placed.top)}) -- "
            rf"({_fmt(bracket_right)},{_y(placed.top)}) -- "
            rf"({_fmt(bracket_right)},{_y(bottom)}) -- "
            rf"({_fmt(bracket_left)},{_y(bottom)});",
            rf"\node[anchor=west] at ({_fmt(x + 2.60)},"
            rf"{_y((placed.top + bottom) / 2)}) {{{_group_label(group)}}};",
        ]

    first_row_top = placed.top + HEADER_HEIGHT
    lines = _bit_labels(group, x, first_row_top)
    for index, register in enumerate(block.rows):
        row_top = first_row_top + index * ROW_PITCH
        lines.extend(_register_image(group, x, row_top))
        name = r"\ldots" if register is None else _tex(register.id)
        lines.append(
            rf"\node[anchor=west] at ({_fmt(x + 1.78)},"
            rf"{_y(row_top + ROW_HEIGHT / 2)}) {{{name}}};"
        )

    last_row_bottom = first_row_top + (len(block.rows) - 1) * ROW_PITCH + ROW_HEIGHT
    bracket_left = x + 2.28
    bracket_right = x + 2.42
    lines.extend(
        (
            rf"\draw ({_fmt(bracket_left)},{_y(first_row_top)}) -- "
            rf"({_fmt(bracket_right)},{_y(first_row_top)}) -- "
            rf"({_fmt(bracket_right)},{_y(last_row_bottom)}) -- "
            rf"({_fmt(bracket_left)},{_y(last_row_bottom)});",
            rf"\node[anchor=west] at ({_fmt(x + 2.60)},"
            rf"{_y((first_row_top + last_row_bottom) / 2)}) "
            rf"{{{_group_label(group)}}};",
        )
    )
    return lines


def _render_band(band: _Band) -> list[str]:
    lines: list[str] = []
    for block in sorted(band.blocks, key=lambda item: (item.column, item.top)):
        lines.extend(_render_block(block))
    return lines
