#!/usr/bin/env python3
"""Validate the direct TeX ABI and compiler-interface document sources."""

from __future__ import annotations

from pathlib import Path
import re

import abi_call_model


ROOT = Path(__file__).resolve().parents[2]
COMMON = ROOT / "isa" / "tex" / "bedrock-reference-common.tex"
DOCUMENTS = {
    ROOT / "isa" / "abi" / "bedrock-elf-abi.tex": "binary",
    ROOT / "isa" / "abi" / "bedrock-c-abi.tex": "language",
}
NON_ABI_DOCUMENTS = (
    ROOT / "isa" / "c" / "bedrock-c-far-extensions.tex",
    ROOT / "isa" / "c" / "bedrock-target-intrinsics.tex",
)
HEADER_ROOT = ROOT / "isa" / "c" / "include"
SEGMENT_DEFS = ROOT / "isa" / "defs" / "segments.yaml"
CALL_CASES = ROOT / "isa" / "abi" / "calling_convention_cases.json"
EVENT_MODEL = ROOT / "isa" / "tools" / "latex_builder" / "templates" / "interrupt_model.tex"
CONTROL_REGISTER_REFERENCE = (
    ROOT / "isa" / "tools" / "latex_builder" / "templates" / "fragments" / "control_register_reference.tex"
)
POINTER_ADDRESS_DOCUMENTS = (
    ROOT / "isa" / "abi" / "bedrock-elf-abi.tex",
    ROOT / "isa" / "abi" / "bedrock-c-abi.tex",
    ROOT / "isa" / "c" / "bedrock-c-far-extensions.tex",
    ROOT / "isa" / "tools" / "latex_builder" / "templates" / "terminology.tex",
    ROOT / "isa" / "tools" / "latex_builder" / "templates" / "memory_address_translation.tex",
)


def normalize_tex(text: str) -> str:
    return (
        text.replace(r"\_\allowbreak{}", "_")
        .replace(r"\_", "_")
        .replace(r"\allowbreak{}", "")
        .replace(r"\textless{}", "<")
        .replace(r"\textgreater{}", ">")
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_layers() -> None:
    require(COMMON.is_file(), f"missing shared TeX component: {COMMON}")
    common_text = COMMON.read_text(encoding="utf-8")
    for label in (
        "Architecture / ISA Specification",
        "Platform / OS ABI",
        "Binary Format ABI",
        "Language ABI",
        "Language Standard Library ABI",
        "Application ABI",
    ):
        require(label in common_text, f"shared layer diagram is missing {label!r}")
    for obsolete in ("Language Extension ABI", "Compiler ABI", "spans layers 1--5"):
        require(obsolete not in common_text, f"shared layer diagram still contains {obsolete!r}")

    for path, target in DOCUMENTS.items():
        require(path.is_file(), f"missing document: {path}")
        text = path.read_text(encoding="utf-8")
        require(r"\input{isa/tex/bedrock-reference-common.tex}" in text, f"{path}: does not use shared TeX")
        require(rf"\BedrockContractDiagram{{{target}}}" in text, f"{path}: wrong or missing contract marker")

    for path in NON_ABI_DOCUMENTS:
        require(path.is_file(), f"missing non-ABI document: {path}")
        text = path.read_text(encoding="utf-8")
        require(r"\input{isa/tex/bedrock-reference-common.tex}" in text, f"{path}: does not use shared TeX")
        require(r"\BedrockContractDiagram" not in text, f"{path}: non-ABI document appears in the ABI stack")


def validate_relocations() -> None:
    path = ROOT / "isa" / "abi" / "bedrock-elf-abi.tex"
    text = normalize_tex(path.read_text(encoding="utf-8"))
    rows = re.findall(r"(?m)^(\d+)\s*&\s*\\texttt\{(R_BEDROCK_[A-Z0-9_]+)\}", text)
    ids = [int(item[0]) for item in rows]
    names = [item[1] for item in rows]
    require(ids == list(range(51)), f"{path}: relocation IDs must be exactly 0 through 50; found {ids}")
    require(len(names) == len(set(names)), f"{path}: duplicate relocation names")


def builtin_tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"__builtin_bedrock_[A-Za-z0-9_]+", normalize_tex(text))
        if token != "__builtin_bedrock_"
    }


def validate_target_intrinsics() -> None:
    path = ROOT / "isa" / "c" / "bedrock-target-intrinsics.tex"
    source = path.read_text(encoding="utf-8")
    suffixes = re.findall(r"\\compilerbuiltin\{([a-z0-9_]+)\}", source)
    require(len(suffixes) == len(set(suffixes)), f"{path}: duplicate target builtin entry")
    documented = {f"__builtin_bedrock_{suffix}" for suffix in suffixes}
    headers = set()
    for header in sorted(HEADER_ROOT.glob("*.h")):
        headers.update(builtin_tokens(header.read_text(encoding="utf-8")))
    require(len(headers) == 51, f"{HEADER_ROOT}: expected 51 intrinsic builtins, found {len(headers)}")
    missing = sorted(headers - documented)
    extra = sorted(documented - headers)
    require(not missing, f"{path}: missing header builtins: {', '.join(missing)}")
    require(not extra, f"{path}: documents undefined builtins: {', '.join(extra)}")

    public = (HEADER_ROOT / "bedrockintrin.h").read_text(encoding="utf-8")
    system = (HEADER_ROOT / "bedrocksystemintrin.h").read_text(encoding="utf-8")
    far = (HEADER_ROOT / "bedrockfarintrin.h").read_text(encoding="utf-8")
    for declaration in (
        "typedef unsigned __int128 __bedrock_far_uintptr_t;",
        "typedef unsigned __int128 __bedrock_far_func_uintptr_t;",
    ):
        require(declaration in far, f"bedrockfarintrin.h is missing {declaration!r}")
    for macro in (
        "__BEDROCK_SEGMENT_IMAGE",
        "__BEDROCK_SEGMENT_IMAGE_FOR_BASE",
        "__BEDROCK_SEGMENT_DISABLED",
    ):
        require(f"#define {macro}" in far, f"bedrockfarintrin.h is missing {macro}")
        require(
            macro in normalize_tex(source),
            f"{path}: does not document {macro}",
        )
    for name in (
        "bedrockfarintrin.h", "bedrockcoreintrin.h", "bedrockmemoryintrin.h",
        "bedrockintegerintrin.h", "bedrockfpuintrin.h",
    ):
        require(f"#include <{name}>" in public, f"bedrockintrin.h does not include {name}")
    for name in (
        "bedrocksysregintrin.h", "bedrockcacheintrin.h", "bedrockmmuintrin.h",
        "bedrockstateintrin.h", "bedrockvirtintrin.h",
    ):
        require(f"#include <{name}>" in system, f"bedrocksystemintrin.h does not include {name}")

    segment_source = SEGMENT_DEFS.read_text(encoding="utf-8")
    metadata_selectors: dict[str, int] = {}
    for match in re.finditer(
        r"(?ms)^- name: ([A-Z][A-Z0-9]*)\n(?P<body>.*?)(?=^- name:|\Z)",
        segment_source,
    ):
        encoding = re.search(r"(?m)^\s+sreg_encoding:\s*(\d+)\s*$", match.group("body"))
        if encoding is not None:
            metadata_selectors[match.group(1)] = int(encoding.group(1))

    sysreg_header_path = HEADER_ROOT / "bedrocksysregintrin.h"
    sysreg_header = sysreg_header_path.read_text(encoding="utf-8")
    header_selectors = {
        name: int(value)
        for name, value in re.findall(r"__BEDROCK_SEG_([A-Z0-9]+)\s*=\s*(\d+)", sysreg_header)
    }
    require(
        header_selectors == metadata_selectors,
        f"{sysreg_header_path}: segment-register selector set does not match {SEGMENT_DEFS}",
    )
    require("CS" not in metadata_selectors, f"{SEGMENT_DEFS}: CS must not be an SREG operand")
    require(
        "__bedrock_read_code_segment()" in sysreg_header,
        f"{sysreg_header_path}: missing dedicated CS-read wrapper",
    )
    require(
        r"\compilerbuiltin{read_code_segment}" in source and r"\texttt{RDSEG CS}" in source,
        f"{path}: dedicated CS-read builtin is not documented",
    )


def validate_event_model() -> None:
    """Keep the machine-visible event-model names and selectors synchronized."""
    instruction_list = (ROOT / "isa" / "defs" / "base" / "instructions.yaml").read_text(encoding="utf-8")
    allocation = (ROOT / "isa" / "alloc" / "extrashort.yaml").read_text(encoding="utf-8")
    eret_path = ROOT / "isa" / "defs" / "base" / "instructions" / "ERET" / "instruction.yaml"
    require(eret_path.is_file(), f"missing ERET definition: {eret_path}")
    require("- instructions/ERET" in instruction_list, "base instruction list does not include ERET")
    require(
        re.search(
            r'id:\s*extrashort\.eret\s+bits:\s*"0000100"\s+text:\s*"ERET"',
            allocation,
        ) is not None,
        "ERET must retain extrashort opcode 0000100",
    )
    require("mnemonic: ERET" in eret_path.read_text(encoding="utf-8"), "ERET definition has wrong mnemonic")

    expected_selectors = {
        "PTCR": 0x0000, "ASCR": 0x0001, "ECR": 0x0002,
        "SPC": 0x0100, "SCS": 0x0101, "SDS": 0x0102,
        "URPC": 0x0108, "URSP": 0x0109, "URCS": 0x010A,
        "URDS": 0x010B, "URSS": 0x010C, "URCTL": 0x010D,
        "EPC": 0x0110, "ECS": 0x0111, "EDS": 0x0112,
        "SSS": 0x0200, "SSP": 0x0201, "ISS": 0x0210, "ISP": 0x0211,
        "FSS": 0x0220, "FSP": 0x0221, "DSS": 0x0230, "DSP": 0x0231,
        "BOOTPC": 0x1000, "BOOTCFG": 0x1001, "PMC": 0x1100,
    }
    header_path = HEADER_ROOT / "bedrocksysregintrin.h"
    header = header_path.read_text(encoding="utf-8")
    header_selectors = {
        name: int(value, 16)
        for name, value in re.findall(r"__BEDROCK_CR_([A-Z0-9]+)\s*=\s*0x([0-9A-Fa-f]+)", header)
    }
    require(header_selectors == expected_selectors, f"{header_path}: control-register selector set is stale")

    control_reference = CONTROL_REGISTER_REFERENCE.read_text(encoding="utf-8")
    documented_selectors = {
        name: int(value, 16)
        for value, name in re.findall(
            r"\\texttt\{0x([0-9A-Fa-f]+)\}\s*&\s*\\texttt\{([A-Z0-9]+)\}",
            control_reference,
        )
    }
    require(
        documented_selectors == expected_selectors,
        f"{CONTROL_REGISTER_REFERENCE}: selector table does not match the public C constants",
    )

    event_model = EVENT_MODEL.read_text(encoding="utf-8")
    for required in (
        r"\section{Architectural Event Processing Model}",
        "EVENT\\_INFO",
        "ECR.MAX\\_EDEPTH",
        "STATUS.EA",
        "DOUBLE\\_FAULT",
        "SHUTDOWN",
        "saved\\_edepth",
        "saved\\_esl",
    ):
        require(required in event_model, f"{EVENT_MODEL}: missing event-model invariant {required!r}")

    legacy_fragments = (
        "cpu_vector_table.tex", "ivt_entry_diagrams.tex", "ivt_entry_table.tex", "vector_range_table.tex",
    )
    fragment_root = EVENT_MODEL.parent / "fragments"
    for name in legacy_fragments:
        require(not (fragment_root / name).exists(), f"obsolete event-model fragment remains: {name}")

    scan_paths = [
        ROOT / "isa" / "defs",
        ROOT / "isa" / "alloc",
        ROOT / "isa" / "tools" / "latex_builder" / "templates",
        HEADER_ROOT,
    ]
    legacy_patterns = {
        "IRET": re.compile(r"\bIRET\b"),
        "ICR": re.compile(r"\bICR\b"),
        "numbered supervisor stack": re.compile(r"\b(?:SSS|SSP)[0-3]\b"),
        "MAX_IDEPTH": re.compile(r"MAX[_\\]IDEPTH"),
        "saved_idepth": re.compile(r"saved[_\\]idepth"),
        "rep_fault": re.compile(r"rep[_\\]fault"),
        "FAULT_AUX": re.compile(r"FAULT[_\\]AUX"),
        "STATUS.IN": re.compile(r"STATUS\.IN"),
        "IVT": re.compile(r"\bIVT\b"),
    }
    for root in scan_paths:
        paths = [root] if root.is_file() else [path for path in root.rglob("*") if path.is_file()]
        for path in paths:
            if path.suffix not in {".yaml", ".tex", ".h"}:
                continue
            text = path.read_text(encoding="utf-8")
            for label, pattern in legacy_patterns.items():
                require(pattern.search(text) is None, f"{path}: obsolete event-model term remains: {label}")


def validate_document_boundaries() -> None:
    c_abi_path = ROOT / "isa" / "abi" / "bedrock-c-abi.tex"
    c_abi_source = c_abi_path.read_text(encoding="utf-8")
    c_abi = normalize_tex(c_abi_source)
    require("__far" not in c_abi, "C ABI contains source-language __far syntax")
    require("bedrock-c-far" in c_abi, "C ABI is missing the far-pointer type family")
    for title in (
        "C Call Relocation Quick Reference",
        "Native Atomic Primitive Quick Reference",
    ):
        require(title in c_abi, f"baseline C ABI is missing refactored table {title!r}")
    require(
        r"\begin{manuallistedbitdiagram}{Far Pointer Object Representation}" in c_abi_source,
        "baseline C ABI is missing the common far-pointer layout diagram",
    )
    for obsolete in (
        "Freestanding Compiler and Linkage Rules",
        "C Atomic Object Support",
        "Basic C Scalar Policies",
        "128-bit Integer ABI",
        "Long Double ABI",
        "Unsupported Extended Scalar Types",
        "Far Data Pointer Object Layout",
        "Far Function Pointer Object Layout",
    ):
        require(obsolete not in c_abi, f"baseline C ABI still contains obsolete rule/value table {obsolete!r}")
    require("Scalar Type Semantics" in c_abi, "baseline C ABI is missing scalar semantic rules")
    require("Aggregate Layout" in c_abi, "baseline C ABI is missing aggregate layout rules")
    for decision in (
        "requires the base floating-point extension",
        "defines no soft-float calling convention",
        "not supported as C atomic",
        "do not create distinct C",
    ):
        require(decision in c_abi, f"baseline C ABI is missing decision {decision!r}")
    for decision in (
        "does not require automatic veneer synthesis",
        "A cast is not an implicit",
    ):
        require(decision in c_abi, f"baseline C ABI is missing decision {decision!r}")

    elf_path = ROOT / "isa" / "abi" / "bedrock-elf-abi.tex"
    elf_abi = elf_path.read_text(encoding="utf-8")
    captions = re.findall(r"\\manualtablecaption\{([^{}]+)\}", elf_abi)
    require(len(captions) == 18, f"{elf_path}: expected 18 structured tables after refactor, found {len(captions)}")
    for title in (
        "ELF e\\_ident Values",
        "Segment-Domain Record Layout",
        "Bedrock ELF Relocation Types",
        "Global Offset Table Reserved Entries",
        "TLS Relocation Families",
        "Bedrock Code Models",
    ):
        require(title in captions, f"{elf_path}: missing structured table {title!r}")
    for obsolete in (
        "ELF Identification",
        "ELF Program Header Rules",
        "ELF Section and Symbol Rules",
        "ELF Loading Rules",
        "Loader Execution Environment",
        "Loader Initial Non-Segment State",
        "Far ELF Profile Scope",
        "Far Model Object Compatibility",
        "Relocation Expression Model",
        "Dynamic Linking Rules",
        "TLS Base Model",
        "TLSDESC Resolver Call ABI",
        "low Code Model Details",
        "small Code Model Details",
        "medium Code Model Details",
        "high Code Model Details",
        "large Code Model Details",
    ):
        require(obsolete not in captions, f"{elf_path}: still contains obsolete rule/value table {obsolete!r}")

    c_ext_path = ROOT / "isa" / "c" / "bedrock-c-far-extensions.tex"
    c_ext_source = c_ext_path.read_text(encoding="utf-8")
    c_ext = normalize_tex(c_ext_source)
    for token in ("__far", "far_ptr_init", "cross-segment alias barrier"):
        require(token in c_ext, f"C extension document is missing {token!r}")
    for decision in (
        "has undefined behavior",
        "No runtime check or trap is required",
        "constraint violation that requires a diagnostic",
        "Such a cast never",
    ):
        require(decision in c_ext, f"C extension document is missing decision {decision!r}")
    c_ext_captions = re.findall(r"\\manualtablecaption\{([^{}]+)\}", c_ext_source)
    require(
        len(c_ext_captions) == 2,
        f"{c_ext_path}: expected 2 source-interface tables after ABI extraction, found {len(c_ext_captions)}",
    )
    for title in (
        "Far Pointer Construction Interface",
        "Cross-Segment Alias-Barrier Triggers",
    ):
        require(title in c_ext_captions, f"{c_ext_path}: missing structured table {title!r}")
    for abi_title in (
        "Far Data Pointer Object Layout",
        "Far Data Pointer Register Assignment",
        "Far Function Pointer Object Layout",
    ):
        require(
            abi_title not in c_ext_captions,
            f"{c_ext_path}: still contains ABI table {abi_title!r}",
        )

    intrinsics_path = ROOT / "isa" / "c" / "bedrock-target-intrinsics.tex"
    intrinsics_source = intrinsics_path.read_text(encoding="utf-8")
    intrinsics_captions = re.findall(r"\\manualtablecaption\{([^{}]+)\}", intrinsics_source)
    require(
        len(intrinsics_captions) == 12,
        f"{intrinsics_path}: expected 12 structured tables, found {len(intrinsics_captions)}",
    )
    for title in (
        "Target Intrinsic Header Families",
        "Far Pointer Builtins",
        "Core Builtins",
        "Memory Builtins",
        "Integer Builtins",
        "Floating-Point Builtins",
        "System-Register Builtins",
        "Cache-Management Builtins",
        "MMU Builtins",
        "Processor-State Builtins",
        "Virtualization-Acceleration Builtin",
        "Target Intrinsic Shared Types",
    ):
        require(title in intrinsics_captions, f"{intrinsics_path}: missing structured table {title!r}")
    for title in intrinsics_captions:
        require(
            not title.endswith((" Spellings", " Contracts")),
            f"{intrinsics_path}: still contains split spelling/contract table {title!r}",
        )


def validate_pointer_address_stage() -> None:
    """Keep ABI-visible pointer words on the input side of segment processing."""
    for path in POINTER_ADDRESS_DOCUMENTS:
        text = path.read_text(encoding="utf-8")
        require(
            "post-segment" not in text,
            f"{path}: ABI-visible pointers are pre-segment addresses; "
            "call the segment result a linear address",
        )


def validate_calling_convention_model() -> None:
    documented_cases = abi_call_model.validate_cases(CALL_CASES)
    c_abi_path = ROOT / "isa" / "abi" / "bedrock-c-abi.tex"
    c_abi = c_abi_path.read_text(encoding="utf-8")
    markers = re.findall(r"(?m)^% ABI-CALL-CASE: ([a-z0-9-]+)$", c_abi)
    require(len(markers) == len(set(markers)), f"{c_abi_path}: duplicate ABI call-case marker")
    marker_set = set(markers)
    missing = sorted(documented_cases - marker_set)
    extra = sorted(marker_set - documented_cases)
    require(not missing, f"{c_abi_path}: missing documented call cases: {', '.join(missing)}")
    require(not extra, f"{c_abi_path}: unknown documented call cases: {', '.join(extra)}")


def validate_codegen_examples() -> None:
    c_abi_path = ROOT / "isa" / "abi" / "bedrock-c-abi.tex"
    c_abi = c_abi_path.read_text(encoding="utf-8")
    markers = re.findall(r"(?m)^% ABI-ASM-EXAMPLE: ([a-z0-9-]+)$", c_abi)
    require(len(markers) == len(set(markers)), f"{c_abi_path}: duplicate ABI assembly-example marker")
    expected = {"scalar-leaf", "nonleaf-preservation"}
    require(set(markers) == expected, f"{c_abi_path}: assembly examples must be exactly {sorted(expected)}")

    scalar_start = c_abi.index("% ABI-ASM-EXAMPLE: scalar-leaf")
    nonleaf_start = c_abi.index("% ABI-ASM-EXAMPLE: nonleaf-preservation")
    scalar_example = c_abi[scalar_start:nonleaf_start]
    rep_line = r"\hspace{1.2em}rep\hspace{1.05em}r1, add.l [r2++], r0\tabularnewline"
    require(rep_line in scalar_example, f"{c_abi_path}: scalar leaf must use parenthesis-free REP syntax")
    require("repg" not in scalar_example.lower(), f"{c_abi_path}: scalar leaf still uses REPG")

def main() -> int:
    validate_layers()
    validate_relocations()
    validate_target_intrinsics()
    validate_event_model()
    validate_document_boundaries()
    validate_pointer_address_stage()
    validate_calling_convention_model()
    validate_codegen_examples()
    print("Document validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
