"""Generate public C target-interface headers from structured catalogs."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import TypeAlias

from engine.generation import (
    ArtifactGenerationContext,
    ArtifactGenerator,
    GeneratedArtifact,
    GeneratedArtifactSet,
)
from engine.reference import QualifiedReference
from interfaces.c.model import CInterfaceProject, InterfaceIntrinsic, InterfaceType
from interfaces.c.model.naming import (
    clang_builtin_spelling,
    intrinsic_collection_header,
    intrinsic_group_header,
    intrinsic_spelling,
)


_C_TYPES = {
    "void": "void",
    "u8": "uint8_t",
    "u16": "uint16_t",
    "u32": "uint32_t",
    "u64": "uint64_t",
    "f32": "float",
    "f64": "double",
    "size": "size_t",
    "void_pointer": "void *",
    "const_void_pointer": "const void *",
    "u8_pointer": "uint8_t *",
    "u16_pointer": "uint16_t *",
    "u32_pointer": "uint32_t *",
    "u64_pointer": "uint64_t *",
    "f32_pointer": "float *",
    "f64_pointer": "double *",
}

CType: TypeAlias = str | QualifiedReference[InterfaceType]


class Generator(ArtifactGenerator):
    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        project = context.require_provider("interfaces.c")
        if not isinstance(project, CInterfaceProject):
            raise TypeError("interfaces.c provider must be a CInterfaceProject")
        artifacts = [
            GeneratedArtifact(
                Path("include") / intrinsic_group_header(group.id),
                _render_group(project, context, group.id),
            )
            for group in project.intrinsic_groups.values()
        ]
        artifacts.extend(
            GeneratedArtifact(
                Path("include") / intrinsic_collection_header(collection.id),
                _render_collection(collection.id, collection.groups),
            )
            for collection in project.collections.values()
        )
        return GeneratedArtifactSet(tuple(artifacts), artifact_id=self.artifact_id)


def _render_group(
    project: CInterfaceProject,
    context: ArtifactGenerationContext,
    group_id: str,
) -> str:
    guard = f"__BEDROCK{group_id.upper()}INTRIN_H"
    groups = [
        group
        for catalog in (
            project.intrinsic_groups,
            project.type_groups,
            project.utility_groups,
        )
        for group in catalog.values()
        if group.id == group_id
    ]
    includes = tuple(
        dict.fromkeys(
            include
            for group in groups
            for include in group.data.get("includes", ())
        )
    )
    sections = [f"#ifndef {guard}", f"#define {guard}", ""]
    sections.extend(f"#include <{include}>" for include in includes)
    if includes:
        sections.append("")
    utilities = [item for item in project.utilities.values() if item.group == group_id]
    types = [item for item in project.types.values() if item.group == group_id]
    intrinsics = [
        item for item in project.intrinsics.values() if item.group == group_id
    ]
    for utility in utilities:
        sections.extend((_render_utility(utility.data), ""))
    for interface_type in types:
        sections.extend((_render_type(interface_type, context, project), ""))
    for intrinsic in intrinsics:
        sections.extend((_render_intrinsic(intrinsic, project), ""))
    sections.extend((f"#endif /* {guard} */", ""))
    return "\n".join(sections)


def _render_collection(collection_id: str, groups: tuple[str, ...]) -> str:
    filename = intrinsic_collection_header(collection_id)
    guard = "__" + filename.removesuffix(".h").upper() + "_H"
    lines = [f"#ifndef {guard}", f"#define {guard}", ""]
    lines.extend(f"#include <{intrinsic_group_header(group)}>" for group in groups)
    lines.extend(("", f"#endif /* {guard} */", ""))
    return "\n".join(lines)


def _render_utility(data: Mapping[str, object]) -> str:
    name = "__BEDROCK_" + str(data["id"]).upper()
    parameters = data.get("parameters", ())
    suffix = f"({', '.join(str(item) for item in parameters)})" if parameters else ""
    return f"#define {name}{suffix} {data['body']}"


def _render_type(
    interface_type: InterfaceType,
    context: ArtifactGenerationContext,
    project: CInterfaceProject,
) -> str:
    data = interface_type.data
    type_id = str(data["id"])
    spelling = f"__bedrock_{type_id}_t"
    tag = f"__bedrock_{type_id}"
    if data["kind"] == "enum":
        values = data["values"]
        if interface_type.enum_source is None:
            raise ValueError(f"{interface_type.source}: enum type lacks a source")
        source = context.workspace.resolve(interface_type.enum_source)
        prefix = str(values["member-prefix"])
        entries = [
            (name, item.encoding)
            for name, item in source.registers.items()
            if item.encoding is not None
        ]
        body = ",\n".join(f"  {prefix}{name} = {value:#x}" for name, value in entries)
        return f"typedef enum {tag} {{\n{body}\n}} {spelling};"
    if data["kind"] == "struct":
        raw_fields = data["fields"]
        if not isinstance(raw_fields, list):
            raise ValueError(f"{interface_type.source}: struct fields must be a list")
        fields = []
        for field, field_type in zip(raw_fields, interface_type.field_types):
            if not isinstance(field, Mapping):
                raise ValueError(
                    f"{interface_type.source}: struct field must be a mapping"
                )
            name = str(field["id"])
            if field.get("role") == "reserved":
                name = "__" + name
            count = f"[{field['count']}]" if "count" in field else ""
            fields.append(f"  {_c_type(field_type, project)} {name}{count};")
        return f"typedef struct {tag} {{\n" + "\n".join(fields) + f"\n}} {spelling};"
    raise ValueError(f"unsupported generated C type kind {data['kind']!r}")


def _render_intrinsic(
    intrinsic: InterfaceIntrinsic, project: CInterfaceProject
) -> str:
    data = intrinsic.data
    intrinsic_id = str(data["id"])
    public = intrinsic_spelling(intrinsic_id)
    builtin = clang_builtin_spelling(intrinsic_id)
    signature = data["signature"]
    parameters = signature["parameters"]
    names = [str(parameter["id"]) for parameter in parameters]
    wrapper = data.get("wrapper", {})
    wrapper_kind = wrapper.get("kind", "inline")
    if wrapper_kind == "macro":
        return f"#define {public}({', '.join(names)}) \\\n  {builtin}({', '.join(names)})"
    if wrapper_kind in {"aggregate-result", "aggregate-result-macro"}:
        return _render_aggregate_wrapper(
            public,
            builtin,
            signature,
            intrinsic.result_type,
            intrinsic.parameter_types,
            wrapper_kind == "aggregate-result-macro",
            project,
        )
    result = _c_type(intrinsic.result_type, project)
    declaration = _parameter_declaration(
        parameters, intrinsic.parameter_types, project
    )
    call = f"{builtin}({', '.join(names)})"
    statement = f"return {call};" if result != "void" else f"{call};"
    return f"static __inline__ {result}\n{public}({declaration})\n{{\n  {statement}\n}}"


def _render_aggregate_wrapper(
    public: str,
    builtin: str,
    signature: Mapping[str, object],
    result_type: CType,
    parameter_types: tuple[CType, ...],
    macro: bool,
    project: CInterfaceProject,
) -> str:
    parameters = signature["parameters"]
    names = [str(parameter["id"]) for parameter in parameters]
    result = _c_type(result_type, project)
    call_arguments = (*names, "&result.value", "&result.flags")
    if macro:
        args = ", ".join(names)
        call = ", ".join(call_arguments).replace("result.", "__result.")
        return (
            f"#define {public}({args}) \\\n"
            "  __extension__ ({ \\\n"
            f"    {result} __result = {{0}}; \\\n"
            f"    {builtin}({call}); \\\n"
            "    __result; \\\n"
            "  })"
        )
    declaration = _parameter_declaration(parameters, parameter_types, project)
    return (
        f"static __inline__ {result}\n{public}({declaration})\n{{\n"
        f"  {result} result = {{0}};\n"
        f"  {builtin}({', '.join(call_arguments)});\n"
        "  return result;\n}"
    )


def _parameter_declaration(
    parameters: list[Mapping[str, object]],
    parameter_types: tuple[CType, ...],
    project: CInterfaceProject,
) -> str:
    if not parameters:
        return "void"
    return ", ".join(
        f"{_c_type(parameter_type, project)} {parameter['id']}"
        for parameter, parameter_type in zip(parameters, parameter_types, strict=True)
    )


def _c_type(type_id: CType, project: CInterfaceProject) -> str:
    if isinstance(type_id, QualifiedReference):
        interface_type = project.resolve(type_id.local)
        if not isinstance(interface_type, InterfaceType):
            raise ValueError("C interface type reference has a non-type target")
        return f"__bedrock_{interface_type.id}_t"
    try:
        return _C_TYPES[type_id]
    except KeyError as error:
        raise ValueError(f"unknown C interface type {type_id!r}") from error
