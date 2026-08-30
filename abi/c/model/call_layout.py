#!/usr/bin/env python3
"""Call-layout projection of a resolved C calling-convention object."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

from engine.reference import Reference

from typing import TYPE_CHECKING

from .project import (
    CAbiProject,
    RegisterClass,
    ResolvedCallingConvention,
    ResolvedRegisterClass,
    ResolvedValueClass,
)

if TYPE_CHECKING:
    from engine.register import Register


@dataclass(frozen=True, slots=True)
class Argument:
    name: str
    kind: str
    named: bool = True
    size: int | None = None


@dataclass(frozen=True, slots=True)
class ReturnValue:
    kind: str
    size: int | None = None


@dataclass(frozen=True, slots=True)
class Call:
    arguments: tuple[Argument, ...]
    return_value: ReturnValue
    variadic: bool = False
    prototyped: bool = True


@dataclass(frozen=True, slots=True)
class CallRules:
    convention: ResolvedCallingConvention
    register_classes_by_id: dict[str, ResolvedRegisterClass]

    @classmethod
    def from_convention(cls, convention: ResolvedCallingConvention) -> "CallRules":
        return cls(
            convention,
            {
                item.definition.id: item
                for item in convention.register_classes.values()
            },
        )

    @property
    def value_classes(self) -> dict[str, ResolvedValueClass]:
        return dict(self.convention.value_classes)

    def value_class(self, kind: str) -> ResolvedValueClass:
        try:
            return self.convention.value_classes[kind]
        except KeyError as error:
            raise ValueError(f"unsupported call kind {kind!r}") from error

    def register_class(self, reference: Reference[RegisterClass]) -> ResolvedRegisterClass:
        try:
            return self.convention.register_classes[reference]
        except KeyError as error:
            raise ValueError("calling convention omits a requested register class") from error


def _positive_aggregate_size(kind: str, size: int | None, context: str) -> None:
    if kind == "aggregate":
        if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
            raise ValueError(f"{context}: aggregate size must be a positive integer")
    elif size is not None:
        raise ValueError(f"{context}: size is valid only for aggregate values")


def _argument(data: dict[str, Any], index: int, rules: CallRules) -> Argument:
    name = data.get("name")
    kind = data.get("kind")
    if not isinstance(name, str) or not name:
        raise ValueError(f"argument {index}: name must be a nonempty string")
    if not isinstance(kind, str) or kind not in rules.convention.value_classes:
        raise ValueError(f"argument {name}: unsupported kind {kind!r}")
    named = data.get("named", True)
    if not isinstance(named, bool):
        raise ValueError(f"argument {name}: named must be boolean")
    size = data.get("size")
    _positive_aggregate_size(kind, size, f"argument {name}")
    return Argument(name=name, kind=kind, named=named, size=size)


def _return_value(data: dict[str, Any], rules: CallRules) -> ReturnValue:
    kind = data.get("kind")
    if kind != "void" and (
        not isinstance(kind, str) or kind not in rules.convention.value_classes
    ):
        raise ValueError(f"return value: unsupported kind {kind!r}")
    size = data.get("size")
    _positive_aggregate_size(kind, size, "return value")
    return ReturnValue(kind=kind, size=size)


def parse_call(data: dict[str, Any], rules: CallRules | None = None) -> Call:
    rules = rules or default_rules()
    arguments_data = data.get("arguments", [])
    if not isinstance(arguments_data, list):
        raise ValueError("call arguments must be a list")
    arguments = tuple(
        _argument(item, index, rules) for index, item in enumerate(arguments_data)
    )
    return_data = data.get("return", {"kind": "void"})
    if not isinstance(return_data, dict):
        raise ValueError("call return must be an object")
    variadic = data.get("variadic", False)
    prototyped = data.get("prototyped", True)
    if not isinstance(variadic, bool) or not isinstance(prototyped, bool):
        raise ValueError("variadic and prototyped must be boolean")
    if variadic and not prototyped:
        raise ValueError("a call cannot be both variadic and unprototyped")
    if not variadic and any(not argument.named for argument in arguments):
        raise ValueError("unnamed arguments require a variadic call")
    seen_unnamed = False
    for argument in arguments:
        if argument.named:
            if seen_unnamed:
                raise ValueError("named arguments must precede variadic arguments")
        else:
            seen_unnamed = True
    return Call(
        arguments=arguments,
        return_value=_return_value(return_data, rules),
        variadic=variadic,
        prototyped=prototyped,
    )


def _uses_sret(value: ReturnValue, rules: CallRules) -> bool:
    if value.kind == "void":
        return False
    policy = rules.value_class(value.kind).definition.result
    if policy.mode == "sret":
        return True
    if policy.mode == "size_dependent":
        assert policy.direct_maximum_bytes is not None
        assert value.size is not None
        return value.size > policy.direct_maximum_bytes
    return False


def _register_name(register: Register) -> str:
    return register.id


def _format_registers(registers: tuple[Register, ...], kind: str) -> str:
    names = tuple(_register_name(register) for register in registers)
    if len(names) == 1:
        return names[0]
    if kind.startswith("complex_"):
        return f"{names[0]}(real)+{names[1]}(imag)"
    return ":".join(reversed(names))


def return_location(
    value: ReturnValue, rules: CallRules | None = None
) -> str | None:
    """Project a result value to its canonical register spelling."""

    rules = rules or default_rules()
    if value.kind == "void":
        return None
    if _uses_sret(value, rules):
        return _register_name(rules.convention.sret_register)
    value_class = rules.value_class(value.kind)
    policy = value_class.definition.result
    register_class = value_class.result_register_class
    if register_class is None or policy.units is None:
        raise ValueError(f"result kind {value.kind!r} has no direct location")
    return _format_registers(register_class.results[: policy.units], value.kind)


def layout_call(call: Call, rules: CallRules | None = None) -> dict[str, Any]:
    """Project one call signature through the resolved calling convention."""

    rules = rules or default_rules()
    stack = rules.convention.definition.stack
    uses_sret = _uses_sret(call.return_value, rules)
    cursors = {reference: 0 for reference in rules.convention.register_classes}
    exhausted: set[Reference[RegisterClass]] = set()
    general = rules.register_classes_by_id["GENERAL"]
    general_reference = general.definition.reference
    if uses_sret:
        cursors[general_reference] = 1
    next_stack_offset = stack.first_argument_offset_bytes
    assignments: list[dict[str, Any]] = []

    def stack_location() -> str:
        nonlocal next_stack_offset
        location = f"[SP+{next_stack_offset}]"
        next_stack_offset += stack.argument_slot_bytes
        return location

    def allocate(
        register_class: ResolvedRegisterClass,
        *,
        units: int,
        alignment: int,
        kind: str,
    ) -> str | None:
        reference = register_class.definition.reference
        cursor = cursors[reference]
        aligned = ((cursor + alignment - 1) // alignment) * alignment
        if reference in exhausted or aligned + units > len(register_class.arguments):
            if register_class.definition.exhaustion == "permanent":
                exhausted.add(reference)
                cursors[reference] = len(register_class.arguments)
            return None
        selected = register_class.arguments[aligned : aligned + units]
        cursors[reference] = aligned + units
        return _format_registers(selected, kind)

    for argument in call.arguments:
        force_stack = (not call.prototyped) or (call.variadic and not argument.named)
        effective_kind = (
            rules.convention.promotions.get(argument.kind, argument.kind)
            if force_stack
            else argument.kind
        )
        value_class = rules.value_class(effective_kind)
        policy = value_class.definition.argument
        mode = "copy-address" if policy.mode == "copy_address" else "value"
        location: str | None

        if force_stack:
            if policy.mode == "copy_address" or effective_kind in {"vector", "predicate"}:
                mode = "copy-address"
            location = stack_location()
        else:
            register_class = value_class.argument_register_class
            if register_class is None or policy.units is None:
                raise ValueError(f"argument kind {effective_kind!r} has no location policy")
            location = allocate(
                register_class,
                units=policy.units,
                alignment=policy.alignment_units,
                kind=effective_kind,
            )
            if location is None and policy.fallback == "indirect":
                mode = "copy-address"
                location = allocate(general, units=1, alignment=1, kind="pointer")
            if location is None:
                location = stack_location()

        assert location is not None

        assignments.append(
            {
                "name": argument.name,
                "source_kind": argument.kind,
                "effective_kind": effective_kind,
                "mode": mode,
                "location": location,
            }
        )

    return {
        "sret": _register_name(rules.convention.sret_register) if uses_sret else None,
        "return_location": return_location(call.return_value, rules),
        "arguments": assignments,
        "stack_size": next_stack_offset - stack.first_argument_offset_bytes,
    }


@cache
def default_rules() -> CallRules:
    """Load the repository's default C calling convention and its ISA objects."""

    from engine.project import IsaProject
    from engine.workspace import SpecWorkspace

    repository = Path(__file__).resolve().parents[3]
    workspace = SpecWorkspace.from_isa(IsaProject.load(repository / "isa"))
    project = workspace.require_provider("abi.c")
    if not isinstance(project, CAbiProject):
        raise TypeError("abi.c provider must be a CAbiProject")
    resolved = project.resolved_calling_convention(workspace)
    return CallRules.from_convention(resolved)
