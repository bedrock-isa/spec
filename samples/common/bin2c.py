#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


C_KEYWORDS = frozenset(
    {
        "alignas",
        "alignof",
        "auto",
        "bool",
        "break",
        "case",
        "char",
        "const",
        "constexpr",
        "continue",
        "default",
        "do",
        "double",
        "else",
        "enum",
        "extern",
        "false",
        "float",
        "for",
        "goto",
        "if",
        "inline",
        "int",
        "long",
        "nullptr",
        "register",
        "restrict",
        "return",
        "short",
        "signed",
        "sizeof",
        "static",
        "static_assert",
        "struct",
        "switch",
        "thread_local",
        "true",
        "typedef",
        "typeof",
        "typeof_unqual",
        "union",
        "unsigned",
        "void",
        "volatile",
        "while",
    }
)


def c_identifier(value: str) -> str:
    if (
        re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value) is None
        or value.startswith("_")
        or value in C_KEYWORDS
    ):
        raise argparse.ArgumentTypeError(
            f"not a portable file-scope C identifier: {value!r}"
        )
    return value


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a binary file to C byte-array declarations."
    )
    parser.add_argument("input", metavar="INPUT", type=Path, help="binary input file")
    parser.add_argument(
        "symbol",
        metavar="SYMBOL",
        type=c_identifier,
        help="portable file-scope C identifier used for the generated array and length",
    )
    args = parser.parse_args()

    data = args.input.read_bytes()
    symbol = args.symbol
    print('#include "tiny_kernel.h"')
    print("")
    print(f"const u8 {symbol}[] = {{")
    for offset in range(0, len(data), 12):
        chunk = data[offset : offset + 12]
        body = ", ".join(f"0x{byte:02x}" for byte in chunk)
        print(f"    {body},")
    print("};")
    print(f"const u64 {symbol}_len = sizeof({symbol});")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
