#!/usr/bin/env python3
"""Validate editorial navigation, canonical names, and revision history."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from typing import Any

import yaml

TOOL_DIR = Path(__file__).resolve().parent
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from defs_loader import load_extensions, load_register_groups  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = ROOT / "isa" / "reference" / "reference_navigation.yaml"
ARCHITECTURE_SOURCE = ROOT / "isa" / "reference" / "architecture_tables.yaml"
TEMPLATE_ROOT = ROOT / "isa" / "tools" / "latex_builder" / "templates"

TOP_KEYS = {
    "schema_version",
    "state_groups",
    "canonical_field_groups",
    "revision_history",
}
STATE_GROUP_KEYS = {"id", "members", "fields", "definition", "readers", "writers"}
FIELD_GROUP_KEYS = {"owner", "fields", "definition"}
REVISION_HISTORY_KEYS = {"unreleased", "released"}
UNRELEASED_KEYS = {"status", "architecture_revision", "changes"}
RELEASED_KEYS = {"architecture_revision", "title", "compatibility", "changes"}

REQUIRED_FIELD_GROUPS = {
    "FLAGS": ("Z", "N", "C", "V"),
    "STATUS": ("IE", "PM", "RF", "TF", "NI", "EA"),
    "PTCR": ("root_page", "PABITS_SEL", "LA57", "PE"),
    "ASCR": ("ASID", "AE"),
    "ECR": ("MAX_EDEPTH", "NMI_P", "V"),
    "URCTL": ("V", "STATUS", "FLAGS"),
    "PMC": ("EN",),
    "PTE": ("P", "W", "X", "U", "G", "A", "D", "AT", "CP", "SW0", "T", "PFN"),
    "instruction_header": ("L",),
}
SUPPLEMENTAL_STATE = {"FLAGS", "STATUS", "FFLAGS", "FSTATUS"}


class NavigationError(ValueError):
    """The navigation source is incomplete or inconsistent."""


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def mapping(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise NavigationError(f"{where}: expected mapping")
    return value


def list_value(value: Any, where: str, *, allow_empty: bool = False) -> list[Any]:
    if not isinstance(value, list) or (not allow_empty and not value):
        qualifier = "" if allow_empty else " non-empty"
        raise NavigationError(f"{where}: expected{qualifier} list")
    return value


def exact_keys(value: dict[str, Any], expected: set[str], where: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = ", ".join(sorted(expected - actual)) or "-"
        extra = ", ".join(sorted(actual - expected)) or "-"
        raise NavigationError(
            f"{where}: key mismatch; missing [{missing}], extra [{extra}]"
        )


def nonempty_string(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise NavigationError(f"{where}: expected non-empty string")
    return value


def string_list(value: Any, where: str, *, allow_empty: bool = False) -> list[str]:
    items = list_value(value, where, allow_empty=allow_empty)
    if any(not isinstance(item, str) or not item for item in items):
        raise NavigationError(f"{where}: expected string entries")
    if len(items) != len(set(items)):
        raise NavigationError(f"{where}: duplicate entry")
    return items


def template_anchors() -> set[str]:
    anchors: set[str] = set()
    for path in TEMPLATE_ROOT.rglob("*.tex"):
        anchors.update(re.findall(r"\\label\{([^}]+)\}", path.read_text(encoding="utf-8")))
    return anchors


def known_registers() -> set[str]:
    extensions = load_extensions(ROOT / "isa" / "defs")
    groups = load_register_groups(ROOT / "isa" / "defs", extensions)
    result: set[str] = set()
    for group in groups.values():
        entries = group.get("entries") if isinstance(group, dict) else None
        if not isinstance(entries, list):
            raise NavigationError("register manifest: expected entries list")
        for entry in entries:
            if not isinstance(entry, dict):
                raise NavigationError("register manifest: expected mapping entry")
            result.add(nonempty_string(entry.get("name"), "register manifest.name"))
    return result


def architecture_data() -> dict[str, Any]:
    return mapping(load_yaml(ARCHITECTURE_SOURCE), str(ARCHITECTURE_SOURCE))


def validate_state_groups(raw: Any, anchors: set[str]) -> None:
    architecture = architecture_data()
    counters = {
        nonempty_string(item.get("name"), "performance_counters.name")
        for item in list_value(
            architecture.get("performance_counters"),
            "architecture.performance_counters",
        )
        if isinstance(item, dict)
    }
    expected_members = known_registers() | SUPPLEMENTAL_STATE | counters
    seen_ids: set[str] = set()
    seen_members: set[str] = set()
    for index, raw_group in enumerate(list_value(raw, "state_groups")):
        where = f"state_groups[{index}]"
        group = mapping(raw_group, where)
        exact_keys(group, STATE_GROUP_KEYS, where)
        identifier = nonempty_string(group["id"], f"{where}.id")
        if identifier in seen_ids:
            raise NavigationError(f"{where}.id: duplicate {identifier!r}")
        seen_ids.add(identifier)
        members = string_list(group["members"], f"{where}.members")
        duplicates = seen_members & set(members)
        if duplicates:
            raise NavigationError(
                f"{where}.members: state appears in multiple groups: "
                + ", ".join(sorted(duplicates))
            )
        seen_members.update(members)
        string_list(group["fields"], f"{where}.fields", allow_empty=True)
        definition = nonempty_string(group["definition"], f"{where}.definition")
        if definition not in anchors:
            raise NavigationError(f"{where}.definition: unknown anchor {definition!r}")
        nonempty_string(group["readers"], f"{where}.readers")
        nonempty_string(group["writers"], f"{where}.writers")

    missing = expected_members - seen_members
    extra = seen_members - expected_members
    if missing or extra:
        raise NavigationError(
            "state_groups membership mismatch; missing "
            f"[{', '.join(sorted(missing)) or '-'}], "
            f"extra [{', '.join(sorted(extra)) or '-'}]"
        )


def validate_field_groups(raw: Any, anchors: set[str]) -> None:
    groups: dict[str, tuple[str, ...]] = {}
    for index, raw_group in enumerate(list_value(raw, "canonical_field_groups")):
        where = f"canonical_field_groups[{index}]"
        group = mapping(raw_group, where)
        exact_keys(group, FIELD_GROUP_KEYS, where)
        owner = nonempty_string(group["owner"], f"{where}.owner")
        if owner in groups:
            raise NavigationError(f"{where}.owner: duplicate {owner!r}")
        fields = tuple(string_list(group["fields"], f"{where}.fields"))
        definition = nonempty_string(group["definition"], f"{where}.definition")
        if definition not in anchors:
            raise NavigationError(f"{where}.definition: unknown anchor {definition!r}")
        groups[owner] = fields
    if groups != REQUIRED_FIELD_GROUPS:
        raise NavigationError(
            "canonical_field_groups must match the architectural canonical-name set"
        )


def validate_revision_history(raw: Any) -> None:
    history = mapping(raw, "revision_history")
    exact_keys(history, REVISION_HISTORY_KEYS, "revision_history")
    unreleased = mapping(history["unreleased"], "revision_history.unreleased")
    exact_keys(unreleased, UNRELEASED_KEYS, "revision_history.unreleased")
    if unreleased["status"] != "Unreleased":
        raise NavigationError("revision_history.unreleased.status: expected Unreleased")
    if unreleased["architecture_revision"] is not None:
        raise NavigationError(
            "revision_history.unreleased.architecture_revision: expected null"
        )
    string_list(unreleased["changes"], "revision_history.unreleased.changes")

    revisions: list[int] = []
    for index, raw_release in enumerate(
        list_value(history["released"], "revision_history.released", allow_empty=True)
    ):
        where = f"revision_history.released[{index}]"
        release = mapping(raw_release, where)
        exact_keys(release, RELEASED_KEYS, where)
        revision = release["architecture_revision"]
        if (
            not isinstance(revision, int)
            or isinstance(revision, bool)
            or not 0 <= revision <= 0xFFFF
        ):
            raise NavigationError(
                f"{where}.architecture_revision: expected unsigned 16-bit integer"
            )
        revisions.append(revision)
        nonempty_string(release["title"], f"{where}.title")
        nonempty_string(release["compatibility"], f"{where}.compatibility")
        string_list(release["changes"], f"{where}.changes")
    if revisions != sorted(set(revisions)):
        raise NavigationError(
            "revision_history.released: revisions must be unique and increasing"
        )


def validate_architecture_rows() -> None:
    architecture = architecture_data()
    registers = list_value(
        architecture.get("control_registers"), "architecture.control_registers"
    )
    names: set[str] = set()
    for index, raw_register in enumerate(registers):
        where = f"architecture.control_registers[{index}]"
        register = mapping(raw_register, where)
        exact_keys(register, {"selector", "name", "use"}, where)
        name = nonempty_string(register["name"], f"{where}.name")
        if name in names:
            raise NavigationError(f"{where}.name: duplicate {name!r}")
        names.add(name)
        nonempty_string(register["use"], f"{where}.use")
    urctl = next(item for item in registers if item["name"] == "URCTL")
    if urctl["use"] != "user-return FLAGS, STATUS, and valid state":
        raise NavigationError("URCTL selector description is incomplete")


def validate_canonical_source_spelling() -> None:
    roots = (
        ROOT / "isa" / "defs",
        ROOT / "isa" / "reference",
        TEMPLATE_ROOT,
    )
    stale = re.compile(r"\b(?:ZF|PSEL)\b")
    for root in roots:
        for path in root.rglob("*"):
            if path.suffix not in {".tex", ".yaml", ".md", ".in"} or not path.is_file():
                continue
            match = stale.search(path.read_text(encoding="utf-8"))
            if match:
                raise NavigationError(
                    f"{path.relative_to(ROOT)}: stale canonical name {match.group(0)!r}"
                )
    memory_model = (TEMPLATE_ROOT / "memory_model.tex").read_text(encoding="utf-8")
    if "Platform-defined device memory" in memory_model:
        raise NavigationError("memory_model.tex: undefined device-memory category remains")
    terminology = (TEMPLATE_ROOT / "terminology.tex").read_text(encoding="utf-8")
    required = (
        "Byte-addressed normal memory",
        r"\texttt{CP=0}",
        "slot-addressed transaction",
        r"\texttt{AT=1}",
        r"\texttt{TRACE} instruction",
        r"\texttt{DEBUG\_TRACE}",
    )
    for text in required:
        if text not in terminology:
            raise NavigationError(f"terminology.tex: missing canonical text {text!r}")


def validate_document(raw: Any) -> None:
    document = mapping(raw, "reference navigation")
    exact_keys(document, TOP_KEYS, "reference navigation")
    if document["schema_version"] != 0:
        raise NavigationError("reference navigation.schema_version: expected 0")
    anchors = template_anchors()
    validate_state_groups(document["state_groups"], anchors)
    validate_field_groups(document["canonical_field_groups"], anchors)
    validate_revision_history(document["revision_history"])
    validate_architecture_rows()
    validate_canonical_source_spelling()


def validate_path(path: Path = DEFAULT_SOURCE) -> dict[str, Any]:
    raw = load_yaml(path)
    validate_document(raw)
    return mapping(raw, str(path))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()
    try:
        validate_path(args.source)
    except (NavigationError, ValueError) as exc:
        print(f"reference navigation validation failed: {exc}", file=sys.stderr)
        return 1
    print("reference navigation and canonical names are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
