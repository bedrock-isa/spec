"""ELF ABI document projection from the typed ELF object catalog."""

from abi.elf.model import ElfAbiProject
from engine.generation import (
    AuthoredTexArtifactGenerator,
    GeneratedArtifact,
    GeneratedArtifactSet,
)


_ROWS_INPUT = r"\BedrockGeneratedElfRelocationRows"
_DEBUG_REGISTER_TABLE_INPUT = r"\BedrockGeneratedElfDebugRegisterTable"
_ENTRY_STATE_TABLE_INPUT = r"\BedrockGeneratedElfEntryStateTable"


class Generator(AuthoredTexArtifactGenerator):
    """Publish authored prose with the relocation table derived from YAML."""

    def generate(self, context):
        provider = context.require_provider("abi.elf")
        if not isinstance(provider, ElfAbiProject):
            raise TypeError("abi.elf provider must be an ElfAbiProject")
        generated = super().generate(context)
        artifacts = tuple(
            GeneratedArtifact(
                artifact.relative_path,
                artifact.content
                .replace(_ROWS_INPUT, _relocation_rows(provider))
                .replace(
                    _DEBUG_REGISTER_TABLE_INPUT,
                    _debug_register_table(provider, context.workspace),
                )
                .replace(
                    _ENTRY_STATE_TABLE_INPUT,
                    _entry_state_table(provider, context.workspace),
                ),
            )
            for artifact in generated.artifacts
        )
        if any("BedrockGeneratedElf" in item.content for item in artifacts):
            raise AssertionError("ELF ABI table projection remained unresolved")
        return GeneratedArtifactSet(artifacts, generated.artifact_id)


def _relocation_rows(project: ElfAbiProject) -> str:
    rows = []
    for relocation in sorted(project.relocations.values(), key=lambda item: item.value):
        result = relocation.result
        if result.kind.value == "none":
            size = "0"
        elif result.kind.value == "bytes":
            size = "variable-size"
        elif result.kind.value == "pair":
            size = f"{result.width_bits}-bit pair"
        else:
            sign = "signed" if result.signed else "unsigned"
            size = f"{result.width_bits}-bit {sign}"
        rows.append(
            f"{relocation.value} & {_code(relocation.id)} & {_code(size)} & "
            f"{_code(relocation.calculation.code)}\\\\"
        )
    return "\\newcommand{\\bedrockelfrelocationrows}{%\n" + "\n".join(rows) + "\n}"


def _code(value: str) -> str:
    escaped = value.replace("_", r"\_")
    return rf"\texttt{{{escaped}}}"


def _debug_register_table(project: ElfAbiProject, workspace) -> str:
    rows: list[str] = []
    for assignment in sorted(
        project.resolved_debug_registers(workspace), key=lambda item: item.first
    ):
        number = (
            f"{assignment.first} and greater"
            if assignment.last is None
            else str(assignment.first)
            if assignment.first == assignment.last
            else f"{assignment.first}..{assignment.last}"
        )
        registers = (
            "---"
            if not assignment.registers
            else _register_display(assignment.registers, workspace)
        )
        status = assignment.status
        if assignment.condition is not None:
            status = f"{status}; {assignment.condition}"
        rows.append(f"{number} & {_code(registers) if registers != '---' else registers} & {status}\\\\")
    return "\n".join(
        (
            r"\manualtablecaption{Bedrock DWARF Register Numbers}",
            r"\begin{manuallongtable}{@{}>{\raggedright\arraybackslash}p{1.10in}>{\raggedright\arraybackslash}p{1.75in}>{\raggedright\arraybackslash}p{2.55in}@{}}",
            r"\toprule",
            r"\rowcolor{ManualHeaderFill}",
            r"\textbf{Numbers} & \textbf{Registers} & \textbf{Status}\\",
            r"\midrule",
            r"\endfirsthead",
            r"\multicolumn{3}{l}{\scriptsize\itshape Table \themanualtable\ (continued)}\\",
            r"\toprule",
            r"\rowcolor{ManualHeaderFill}",
            r"\textbf{Numbers} & \textbf{Registers} & \textbf{Status}\\",
            r"\midrule",
            r"\endhead",
            *rows,
            r"\bottomrule",
            r"\end{manuallongtable}",
        )
    )


def _register_display(registers, workspace) -> str:
    names = [workspace.resolve(item).id for item in registers]
    if len(names) == 1:
        return names[0]
    return f"{names[0]}..{names[-1]}"


def _entry_state_table(project: ElfAbiProject, workspace) -> str:
    state = project.process_entry
    segments = "/".join(
        workspace.resolve(state.segment_contexts[role]).id
        for role in ("code", "data", "stack")
    )
    permissions = "/".join(state.stack_permissions)
    cleared = ", ".join(workspace.resolve(item).id for item in state.cleared)
    readiness = ", ".join(item.replace("_", " ") for item in state.readiness)
    entry_pc = f"{workspace.resolve(state.entry_point).id} = {state.entry_point_source}"
    entry_stack = (
        f"{workspace.resolve(state.stack).id}, {state.stack_alignment_bytes}-byte aligned, "
        f"{permissions}"
    )
    rows = (
        f"Entry PC & {_code(entry_pc)}\\\\",
        f"Entry stack & {_code(entry_stack)}\\\\",
        f"Segment contexts & {_code(segments)}\\\\",
        f"TLS base & {_code(workspace.resolve(state.tls_base).id if state.tls_base else 'absent')}\\\\",
        f"Readiness & {readiness}\\\\",
        f"Cleared state & {_code(cleared)}\\\\",
        f"Stack payload owner & {_code(state.payload_owner)}\\\\",
    )
    return "\n".join(
        (
            r"\manualtablecaption{Language-Independent ELF Program Entry State}",
            r"\begin{manuallongtable}{@{}p{1.55in}p{3.85in}@{}}",
            r"\toprule",
            r"\textbf{Property} & \textbf{Contract}\\",
            r"\midrule",
            r"\endhead",
            *rows,
            r"\bottomrule",
            r"\end{manuallongtable}",
        )
    )

__all__ = ["Generator"]
