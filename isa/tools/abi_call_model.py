#!/usr/bin/env python3
"""Executable reference model for the Bedrock C call ABI.

The normative contract lives in ``isa/interfaces/abi/bedrock-c-abi.tex``.  This module
models only the deterministic argument-location procedure so that compiler,
runtime, and conformance-test work can share executable examples without
turning the whole ABI document into structured data.
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import json
from pathlib import Path
from typing import Any


GENERAL_REGISTERS = tuple(f"R{index}" for index in range(8))
FLOAT_REGISTERS = tuple(f"F{index}" for index in range(8))
FIRST_STACK_ARGUMENT_OFFSET = 16
STACK_SLOT_SIZE = 16

GENERAL_SCALARS = {
    "bool", "i8", "u8", "i16", "u16", "i32", "u32", "i64", "u64",
    "pointer", "function_pointer",
}
GENERAL_PAIRS = {"i128", "u128"}
FLOAT_SCALARS = {"f32", "f64", "long_double"}
FLOAT_PAIRS = {"complex_f32", "complex_f64", "complex_long_double"}
SCALAR_KINDS = GENERAL_SCALARS | GENERAL_PAIRS | FLOAT_SCALARS | FLOAT_PAIRS
DEFAULT_PROMOTIONS = {
    "bool": "i32",
    "i8": "i32",
    "u8": "i32",
    "i16": "i32",
    "u16": "i32",
    "f32": "f64",
}


@dataclass(frozen=True)
class Argument:
    name: str
    kind: str
    named: bool = True
    size: int | None = None


@dataclass(frozen=True)
class ReturnValue:
    kind: str
    size: int | None = None


@dataclass(frozen=True)
class Call:
    arguments: tuple[Argument, ...]
    return_value: ReturnValue
    variadic: bool = False
    prototyped: bool = True


def _positive_aggregate_size(kind: str, size: int | None, context: str) -> None:
    if kind == "aggregate":
        if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
            raise ValueError(f"{context}: aggregate size must be a positive integer")
    elif size is not None:
        raise ValueError(f"{context}: size is valid only for aggregate values")


def _argument(data: dict[str, Any], index: int) -> Argument:
    name = data.get("name")
    kind = data.get("kind")
    if not isinstance(name, str) or not name:
        raise ValueError(f"argument {index}: name must be a nonempty string")
    if kind not in SCALAR_KINDS | {"aggregate"}:
        raise ValueError(f"argument {name}: unsupported kind {kind!r}")
    named = data.get("named", True)
    if not isinstance(named, bool):
        raise ValueError(f"argument {name}: named must be boolean")
    size = data.get("size")
    _positive_aggregate_size(kind, size, f"argument {name}")
    return Argument(name=name, kind=kind, named=named, size=size)


def _return_value(data: dict[str, Any]) -> ReturnValue:
    kind = data.get("kind")
    if kind not in SCALAR_KINDS | {"aggregate", "void"}:
        raise ValueError(f"return value: unsupported kind {kind!r}")
    size = data.get("size")
    _positive_aggregate_size(kind, size, "return value")
    return ReturnValue(kind=kind, size=size)


def parse_call(data: dict[str, Any]) -> Call:
    arguments_data = data.get("arguments", [])
    if not isinstance(arguments_data, list):
        raise ValueError("call arguments must be a list")
    arguments = tuple(_argument(item, index) for index, item in enumerate(arguments_data))
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
        if not argument.named:
            seen_unnamed = True
        elif seen_unnamed:
            raise ValueError("named arguments must precede variadic arguments")
    return Call(
        arguments=arguments,
        return_value=_return_value(return_data),
        variadic=variadic,
        prototyped=prototyped,
    )


def _uses_sret(value: ReturnValue) -> bool:
    return value.kind == "aggregate" and value.size is not None and value.size > 16


def _effective_kind(argument: Argument, force_stack: bool) -> str:
    if force_stack:
        return DEFAULT_PROMOTIONS.get(argument.kind, argument.kind)
    return argument.kind


def return_location(value: ReturnValue) -> str | None:
    """Return the canonical register location for a result value."""

    if value.kind == "void":
        return None
    if value.kind in GENERAL_SCALARS:
        return "R0"
    if value.kind in GENERAL_PAIRS:
        return "R1:R0"
    if value.kind in FLOAT_SCALARS:
        return "F0"
    if value.kind in FLOAT_PAIRS:
        return "F0(real)+F1(imag)"
    if value.kind == "aggregate":
        return "R1:R0" if value.size is not None and value.size <= 16 else "R0"
    raise AssertionError(f"unhandled return kind: {value.kind}")


def layout_call(call: Call) -> dict[str, Any]:
    """Return the canonical location assignment for one call signature."""

    uses_sret = _uses_sret(call.return_value)
    general_cursor = 1 if uses_sret else 0
    float_cursor = 0
    general_exhausted = False
    float_exhausted = False
    next_stack_offset = FIRST_STACK_ARGUMENT_OFFSET
    assignments: list[dict[str, Any]] = []

    def stack_location() -> str:
        nonlocal next_stack_offset
        location = f"[SP+{next_stack_offset}]"
        next_stack_offset += STACK_SLOT_SIZE
        return location

    for argument in call.arguments:
        force_stack = not call.prototyped or (call.variadic and not argument.named)
        effective_kind = _effective_kind(argument, force_stack)
        mode = "copy-address" if effective_kind == "aggregate" else "value"

        if force_stack:
            location = stack_location()
        elif effective_kind == "aggregate" or effective_kind in GENERAL_SCALARS:
            if not general_exhausted and general_cursor < len(GENERAL_REGISTERS):
                location = GENERAL_REGISTERS[general_cursor]
                general_cursor += 1
            else:
                general_exhausted = True
                general_cursor = len(GENERAL_REGISTERS)
                location = stack_location()
        elif effective_kind in GENERAL_PAIRS:
            pair_low = general_cursor if general_cursor % 2 == 0 else general_cursor + 1
            if not general_exhausted and pair_low + 1 < len(GENERAL_REGISTERS):
                location = f"R{pair_low + 1}:R{pair_low}"
                general_cursor = pair_low + 2
            else:
                general_exhausted = True
                general_cursor = len(GENERAL_REGISTERS)
                location = stack_location()
        elif effective_kind in FLOAT_SCALARS:
            if not float_exhausted and float_cursor < len(FLOAT_REGISTERS):
                location = FLOAT_REGISTERS[float_cursor]
                float_cursor += 1
            else:
                float_exhausted = True
                float_cursor = len(FLOAT_REGISTERS)
                location = stack_location()
        elif effective_kind in FLOAT_PAIRS:
            if not float_exhausted and float_cursor + 1 < len(FLOAT_REGISTERS):
                location = f"F{float_cursor}(real)+F{float_cursor + 1}(imag)"
                float_cursor += 2
            else:
                float_exhausted = True
                float_cursor = len(FLOAT_REGISTERS)
                location = stack_location()
        else:  # pragma: no cover - parse_call keeps this unreachable.
            raise AssertionError(f"unhandled argument kind: {effective_kind}")

        assignments.append(
            {
                "name": argument.name,
                "source_kind": argument.kind,
                "effective_kind": effective_kind,
                "mode": mode,
                "location": location,
            }
        )

    stack_size = next_stack_offset - FIRST_STACK_ARGUMENT_OFFSET
    return {
        "sret": "R0" if uses_sret else None,
        "return_location": return_location(call.return_value),
        "arguments": assignments,
        "stack_size": stack_size,
    }


def load_cases(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError(f"{path}: unsupported schema_version")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"{path}: cases must be a nonempty list")
    return data


def validate_cases(path: Path) -> set[str]:
    data = load_cases(path)
    case_ids: set[str] = set()
    documented: set[str] = set()
    for case in data["cases"]:
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"{path}: every case needs a nonempty id")
        if case_id in case_ids:
            raise ValueError(f"{path}: duplicate case id {case_id!r}")
        case_ids.add(case_id)
        if case.get("documented", False):
            documented.add(case_id)
        actual = layout_call(parse_call(case.get("call", {})))
        expected = case.get("expect")
        if actual != expected:
            raise ValueError(
                f"{path}: case {case_id!r} does not match the reference model\n"
                f"expected: {json.dumps(expected, indent=2, sort_keys=True)}\n"
                f"actual:   {json.dumps(actual, indent=2, sort_keys=True)}"
            )
    return documented


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    path = root / "isa" / "abi" / "calling_convention_cases.json"
    documented = validate_cases(path)
    print(f"C ABI call model passed {len(load_cases(path)['cases'])} cases ({len(documented)} documented)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
