"""Parser and value objects for the Bedrock instruction metasyntax."""

from __future__ import annotations

from dataclasses import dataclass, field
import re

try:
    from .metasyntax import Metasyntax, MetasyntaxError
except ImportError:  # Support loading engine directly on PYTHONPATH.
    from metasyntax import Metasyntax, MetasyntaxError


class InstructionMetasyntaxError(MetasyntaxError):
    """Raised when an instruction metasyntax value is malformed."""


@dataclass(frozen=True, slots=True)
class InstructionMetasyntaxOperand:
    """One operand, group, or address-expression node."""

    kind: str
    name: str | None = None
    angled: bool = False
    field: str | None = None
    literal: int | None = None
    group_style: str | None = None
    members: tuple["InstructionMetasyntaxOperand", ...] = ()


@dataclass(frozen=True, slots=True)
class _ParsedInstruction:
    mnemonic: str
    fixed_size_suffix: str | None
    selected_size_codes: tuple[str, ...]
    size_field: str | None
    order_field: str | None
    operands: tuple[InstructionMetasyntaxOperand, ...]


@dataclass(frozen=True, slots=True)
class InstructionMetasyntax(Metasyntax):
    """A validated instruction presentation template and its parsed structure."""

    mnemonic: str = field(init=False)
    fixed_size_suffix: str | None = field(init=False)
    selected_size_codes: tuple[str, ...] = field(init=False)
    size_field: str | None = field(init=False)
    order_field: str | None = field(init=False)
    operands: tuple[InstructionMetasyntaxOperand, ...] = field(init=False)

    def _validate(self) -> None:
        if not isinstance(self.code, str) or not self.code:
            raise InstructionMetasyntaxError(
                "instruction metasyntax must be a non-empty string"
            )
        parsed = _InstructionMetasyntaxParser(self.code).parse()
        for name in (
            "mnemonic",
            "fixed_size_suffix",
            "selected_size_codes",
            "size_field",
            "order_field",
            "operands",
        ):
            object.__setattr__(self, name, getattr(parsed, name))

    @property
    def displayed_operands(self) -> tuple[InstructionMetasyntaxOperand, ...]:
        """Return displayed operands with address references flattened."""

        def address_references(
            operand: InstructionMetasyntaxOperand,
        ) -> list[InstructionMetasyntaxOperand]:
            result: list[InstructionMetasyntaxOperand] = []
            for member in operand.members:
                if member.kind == "reference":
                    result.append(member)
                elif member.kind == "lane_index":
                    result.extend(address_references(member))
            return result

        result: list[InstructionMetasyntaxOperand] = []
        for operand in self.operands:
            if operand.kind == "address":
                result.extend(address_references(operand))
            elif operand.kind != "group":
                result.append(operand)
        return tuple(result)

    @property
    def encoding_id(self) -> str:
        """Return the canonical local encoding ID derived without the mnemonic."""

        remainder = self.code[len(self.mnemonic) :]
        remainder = remainder.replace("+", "_add_").replace("*", "_mul_")
        normalized = re.sub(r"[^A-Za-z0-9_]+", "_", remainder)
        normalized = re.sub(r"_+", "_", normalized).strip("_").lower()
        return normalized or "plain"


class _InstructionMetasyntaxParser:
    def __init__(self, value: str) -> None:
        self.value = value
        self.index = 0

    def fail(self, message: str) -> None:
        raise InstructionMetasyntaxError(
            f"instruction metasyntax: {message} at character {self.index + 1}"
        )

    def take(self, literal: str) -> bool:
        if self.value.startswith(literal, self.index):
            self.index += len(literal)
            return True
        return False

    def require(self, literal: str) -> None:
        if not self.take(literal):
            self.fail(f"expected {literal!r}")

    def identifier(self, label: str, *, mnemonic: bool = False) -> str:
        pattern = r"[A-Za-z][A-Za-z0-9]*" if mnemonic else r"[A-Za-z][A-Za-z0-9_]*"
        match = re.match(pattern, self.value[self.index :])
        if match is None:
            self.fail(f"expected {label}")
        result = match.group(0)
        self.index += len(result)
        return result

    def field_expression(self) -> str:
        self.require("(")
        if (
            self.index >= len(self.value)
            or self.value[self.index] not in "abcdefghijklmnopqrstuvwxyz"
        ):
            self.fail("expected lowercase field marker")
        marker = self.value[self.index]
        self.index += 1
        self.require(")")
        return marker

    def operand_reference(self) -> tuple[str, bool]:
        angled = self.take("<")
        name = self.identifier("operand name")
        if angled:
            self.require(">")
        return name, angled

    def address_expression(self, kind: str) -> InstructionMetasyntaxOperand:
        members: list[InstructionMetasyntaxOperand] = []
        while True:
            if self.index >= len(self.value):
                self.fail("unterminated address expression")
            if self.take("]"):
                return InstructionMetasyntaxOperand(kind=kind, members=tuple(members))
            if self.value[self.index].isspace():
                self.index += 1
                continue
            if self.take("["):
                members.append(self.address_expression("lane_index"))
                continue
            if self.value[self.index] in "+*":
                members.append(
                    InstructionMetasyntaxOperand(
                        kind="operator", name=self.value[self.index]
                    )
                )
                self.index += 1
                continue
            decimal = re.match(r"[0-9]+", self.value[self.index :])
            if decimal is not None:
                spelling = decimal.group(0)
                self.index += len(spelling)
                members.append(
                    InstructionMetasyntaxOperand(
                        kind="decimal", literal=int(spelling, 10)
                    )
                )
                continue
            name, angled = self.operand_reference()
            marker = (
                self.field_expression()
                if self.index < len(self.value) and self.value[self.index] == "("
                else None
            )
            members.append(
                InstructionMetasyntaxOperand(
                    kind="scale" if name == "scale" else "reference",
                    name=name,
                    angled=angled,
                    field=marker,
                )
            )

    def operand(self) -> InstructionMetasyntaxOperand:
        if self.take("["):
            return self.address_expression("address")
        if self.take("{ "):
            name, angled = self.operand_reference()
            self.require("... }")
            return InstructionMetasyntaxOperand(
                kind="group", name=name, angled=angled, group_style="braced"
            )
        if self.take("("):
            name, angled = self.operand_reference()
            self.require(")")
            return InstructionMetasyntaxOperand(
                kind="group", name=name, angled=angled, group_style="parenthesized"
            )
        decimal = re.match(r"[0-9]+", self.value[self.index :])
        if decimal is not None:
            spelling = decimal.group(0)
            self.index += len(spelling)
            return InstructionMetasyntaxOperand(
                kind="decimal", literal=int(spelling, 10)
            )
        name, angled = self.operand_reference()
        marker = (
            self.field_expression()
            if self.index < len(self.value) and self.value[self.index] == "("
            else None
        )
        return InstructionMetasyntaxOperand(
            kind="reference", name=name, angled=angled, field=marker
        )

    def parse(self) -> _ParsedInstruction:
        mnemonic = self.identifier("mnemonic name", mnemonic=True)
        fixed_size_suffix: str | None = None
        selected_size_codes: tuple[str, ...] = ()
        size_field: str | None = None
        order_field: str | None = None
        if self.take("."):
            if self.take("{"):
                codes = [self.identifier("public size suffix")]
                while self.take("|"):
                    codes.append(self.identifier("public size suffix"))
                self.require("}")
                if len(set(codes)) != len(codes):
                    self.fail("repeated public size suffix")
                selected_size_codes = tuple(codes)
                size_field = self.field_expression()
                if self.take("/order"):
                    order_field = self.field_expression()
            else:
                fixed_size_suffix = "." + self.identifier("fixed size suffix")

        operands: list[InstructionMetasyntaxOperand] = []
        if self.index < len(self.value):
            self.require(" ")
            operands.append(self.operand())
            while self.index < len(self.value):
                self.require(", ")
                operands.append(self.operand())
        if self.index != len(self.value):
            self.fail("unexpected text")
        return _ParsedInstruction(
            mnemonic=mnemonic,
            fixed_size_suffix=fixed_size_suffix,
            selected_size_codes=selected_size_codes,
            size_field=size_field,
            order_field=order_field,
            operands=tuple(operands),
        )
