"""C ABI document projection from the typed calling-convention catalog."""

from abi.c.model import CAbiProject
from engine.generation import (
    AuthoredTexArtifactGenerator,
    GeneratedArtifact,
    GeneratedArtifactSet,
)


_RETURN_TABLE_INPUT = (
    r"\BedrockGeneratedCReturnRegisterTable"
)
_MEMORY_ORDER_TABLE_INPUT = r"\BedrockGeneratedCMemoryOrderTable"
_ATOMIC_PRIMITIVE_TABLE_INPUT = r"\BedrockGeneratedCAtomicPrimitiveTable"
_FETCH_RMW_TABLE_INPUT = r"\BedrockGeneratedCFetchRmwTable"


class Generator(AuthoredTexArtifactGenerator):
    """Publish authored prose with calling-convention tables derived from YAML."""

    def generate(self, context) -> GeneratedArtifactSet:
        provider = context.require_provider("abi.c")
        if not isinstance(provider, CAbiProject):
            raise TypeError("abi.c provider must be a CAbiProject")
        generated = super().generate(context)
        return_table = _return_register_table(provider, context.workspace)
        memory_order_table = _memory_order_table(provider, context.workspace)
        atomic_primitive_table = _atomic_lowering_table(
            provider, context.workspace, fetch=False
        )
        fetch_rmw_table = _atomic_lowering_table(
            provider, context.workspace, fetch=True
        )
        artifacts = tuple(
            GeneratedArtifact(
                artifact.relative_path,
                artifact.content
                .replace(_RETURN_TABLE_INPUT, return_table)
                .replace(_MEMORY_ORDER_TABLE_INPUT, memory_order_table)
                .replace(_ATOMIC_PRIMITIVE_TABLE_INPUT, atomic_primitive_table)
                .replace(_FETCH_RMW_TABLE_INPUT, fetch_rmw_table),
            )
            for artifact in generated.artifacts
        )
        if any("BedrockGeneratedC" in item.content for item in artifacts):
            raise AssertionError("C ABI table projection remained unresolved")
        return GeneratedArtifactSet(artifacts, generated.artifact_id)


def _return_register_table(project: CAbiProject, workspace) -> str:
    convention = project.calling_convention
    classes = {
        reference: project.register_classes.resolve(reference)
        for reference in convention.register_classes
    }
    rows: list[str] = []
    for reference in convention.value_classes:
        value_class = project.value_classes.resolve(reference)
        policy = value_class.result
        register_class = (
            None
            if policy.register_class is None
            else classes.get(policy.register_class)
        )
        names = () if register_class is None else tuple(
            workspace.resolve(item).id
            for item in register_class.results[: policy.units or 0]
        )
        if policy.mode == "sret":
            rule = "sret pointer in R0; result pointer in R0"
        elif policy.mode == "size_dependent":
            direct = ":".join(reversed(names))
            rule = f"up to {policy.direct_maximum_bytes} bytes in {direct}; larger values use sret"
        elif len(names) == 2 and value_class.id == "FLOAT_PAIR":
            rule = f"real component in {names[0]}; imaginary component in {names[1]}"
        else:
            rule = ":".join(reversed(names))
        kinds = ", ".join(value_class.kinds)
        rows.append(f"{_code(kinds)} & {_code(rule)}\\\\")
    return "\n".join(
        (
            r"\manualtablecaption{C Return Register Quick Reference}",
            r"\begingroup\footnotesize",
            r"\setlength{\tabcolsep}{2pt}",
            r"\begin{longtable}{@{}p{2.15in}p{3.35in}@{}}",
            r"\toprule",
            r"\textbf{Result kinds} & \textbf{Register rule}\\",
            r"\midrule",
            r"\endhead",
            *rows,
            r"\bottomrule",
            r"\end{longtable}",
            r"\endgroup",
        )
    )


def _memory_order_table(project: CAbiProject, workspace) -> str:
    inventory = project.namespaces["base"].memory_order_inventory
    rows = []
    for entity_id in inventory.declared:
        mapping = project.namespaces["base"].memory_orders[entity_id]
        rows.append(
            " & ".join(
                (
                    _code(entity_id.lower()),
                    _code(mapping.instruction_order),
                    _sequence(mapping.load, "load", workspace),
                    _sequence(mapping.store, "store", workspace),
                    _sequence(mapping.thread_fence, "access", workspace),
                )
            )
            + r"\\"
        )
    return "\n".join(
        (
            r"\manualtablecaption{C Atomic Memory Order Mapping}",
            r"\begingroup\scriptsize",
            r"\setlength{\tabcolsep}{2pt}",
            r"\begin{longtable}{@{}p{0.7in}p{0.75in}p{1.35in}p{1.35in}p{1.0in}@{}}",
            r"\toprule",
            r"\textbf{C order} & \textbf{Instruction} & \textbf{Load} & \textbf{Store} & \textbf{Fence}\\",
            r"\midrule",
            r"\endhead",
            *rows,
            r"\bottomrule",
            r"\end{longtable}",
            r"\endgroup",
        )
    )


def _sequence(sequence, access_name: str, workspace) -> str:
    if sequence is None:
        return "---"
    if len(sequence) == 0:
        return "zero instructions"
    names = [
        access_name if item == "access" else workspace.resolve(item).instruction.mnemonic
        for item in sequence
    ]
    return _code("; ".join(names))


def _code(value: str) -> str:
    escaped = value.replace("_", r"\_")
    return rf"\texttt{{{escaped}}}"


def _atomic_lowering_table(project: CAbiProject, workspace, *, fetch: bool) -> str:
    inventory = project.namespaces["base"].atomic_lowering_inventory
    rows: list[str] = []
    for entity_id in inventory.declared:
        lowering = project.namespaces["base"].atomic_lowerings[entity_id]
        is_fetch = entity_id.startswith("FETCH_")
        if is_fetch != fetch:
            continue
        operations = ", ".join(lowering.c_operations)
        instructions = ", ".join(
            workspace.resolve(item).instruction.mnemonic
            for item in lowering.instructions
        )
        if lowering.strategy == "aligned_access":
            rule = f"aligned {instructions} access plus the order sequence"
        elif lowering.strategy == "compare_exchange_loop":
            rule = f"loop using {instructions}"
        else:
            rule = instructions
        rows.append(f"{_code(operations)} & {_code(rule)}\\\\")
    caption = "C Fetch RMW Lowering" if fetch else "Native Atomic Primitive Quick Reference"
    return "\n".join(
        (
            rf"\manualtablecaption{{{caption}}}",
            r"\begin{manuallongtable}{@{}p{2.15in}p{3.25in}@{}}",
            r"\toprule",
            r"\textbf{C operation} & \textbf{Bedrock lowering}\\",
            r"\midrule",
            r"\endhead",
            *rows,
            r"\bottomrule",
            r"\end{manuallongtable}",
        )
    )
