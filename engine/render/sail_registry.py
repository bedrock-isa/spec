"""Render active Sail operation and architectural type registries."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from ..composition import SailProgram
from ..project import InstructionBundle


ROUTE_CONSTRUCTORS = {
    "atomics": "RouteAtomics",
    "bounds": "RouteBounds",
    "cache": "RouteCache",
    "control_flow": "RouteControlFlow",
    "core_control": "RouteCoreControl",
    "data_movement": "RouteDataMovement",
    "ea_utility": "RouteEaUtility",
    "fpu": "RouteFpu",
    "fpu_transcendental_approx": "RouteFpuTranscendental",
    "integer_alu": "RouteIntegerAlu",
    "integer_bitfield": "RouteIntegerBitfield",
    "integer_mul_div": "RouteIntegerMulDiv",
    "integer_unary": "RouteIntegerUnary",
    "system_registers": "RouteSystemRegisters",
    "tlb_and_context": "RouteTlbContext",
    "vector": "RouteVector",
}

BASE_FAULT_CONSTRUCTORS = (
    "NoFault", "IllegalInstruction", "PrivilegeFault", "ExtensionUnavailable",
    "InvalidControlState", "DivideByZero", "DivideOverflow", "BoundsFault",
    "AlignmentFault", "TranslationFault", "AccessFault", "EventFault",
)

BASE_EFFECT_CONSTRUCTORS = (
    "NoEffect", "ReadMemory", "WriteMemory", "AtomicMemory",
    "TranslateAddress", "CacheOperation", "TlbOperation",
    "ControlRegisterAccess", "EventDelivery", "TraceMarker", "HaltProcessor",
    "ResetProcessor", "RepeatBody", "FenceOperation", "IntegerCompute",
)


@dataclass(frozen=True, slots=True)
class SailTypeContribution:
    instruction_sets: tuple[str, ...] = ()
    fault_kinds: tuple[str, ...] = ()
    effect_kinds: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SailOperationProjection:
    operation: str
    mnemonic: str
    route: str


@dataclass(frozen=True, slots=True)
class SailEventProjection:
    event_id: str
    class_value: int
    selector: int | None
    frame: str
    family: str | None


@dataclass(frozen=True, slots=True)
class SailRegistryProjection:
    """Active operation, type, CPUID, and event semantics for Sail."""

    cpuid_flags: tuple[str, ...]
    instruction_sets: tuple[str, ...]
    fault_kinds: tuple[str, ...]
    effect_kinds: tuple[str, ...]
    event_families: tuple[str, ...]
    events: tuple[SailEventProjection, ...]
    operations: tuple[SailOperationProjection, ...]


EXTENSION_CONTRIBUTIONS = {
    "FP": SailTypeContribution(
        instruction_sets=("FpuSet",),
        fault_kinds=("FloatingPointFault",),
        effect_kinds=("FloatingPointCompute",),
    ),
    "FPTRANSA": SailTypeContribution(
        instruction_sets=("FpuTranscendentalSet",),
        effect_kinds=("TranscendentalCompute",),
    ),
    "VECTOR": SailTypeContribution(
        instruction_sets=("VectorSet",),
        fault_kinds=("VectorRangeFault",),
    ),
    "VECTORFP": SailTypeContribution(
        instruction_sets=("VectorFpuSet",),
    ),
}


class SailRegistryRenderer:
    def project(self, program: SailProgram) -> SailRegistryProjection:
        cpuid_flags = tuple(
            dict.fromkeys(
                field.id
                for bundle in program.bundles
                for field in bundle.required_cpuid_flags
            )
        )
        instruction_sets = ["BaseSet"]
        faults = list(BASE_FAULT_CONSTRUCTORS)
        effects = list(BASE_EFFECT_CONSTRUCTORS)
        for extension_id in program.configuration.extension_ids:
            contribution = EXTENSION_CONTRIBUTIONS.get(
                extension_id, SailTypeContribution()
            )
            instruction_sets.extend(contribution.instruction_sets)
            faults.extend(contribution.fault_kinds)
            effects.extend(contribution.effect_kinds)
        event_entries = program.project.events.resolved_events(
            program.configuration.owners
        )
        event_families = tuple(
            dict.fromkeys(
                item.event.family
                for item in event_entries
                if item.event.family is not None
            )
        )

        return SailRegistryProjection(
            cpuid_flags,
            tuple(instruction_sets),
            tuple(faults),
            tuple(effects),
            event_families,
            tuple(
                SailEventProjection(
                    item.event.id,
                    item.code.class_value,
                    item.code.event_selector,
                    item.event.frame,
                    item.event.family,
                )
                for item in event_entries
            ),
            tuple(
                SailOperationProjection(
                    _operation(bundle),
                    bundle.instruction.mnemonic,
                    bundle.instruction.route,
                )
                for bundle in program.bundles
            ),
        )

    def render(self, program: SailProgram) -> str:
        from .sail_catalog import catalog_id_declarations

        projection = self.project(program)
        routes = tuple(dict.fromkeys(item.route for item in projection.operations))
        lines = [
            "// Generated from instruction.yaml owners. Do not edit.", "",
            "default Order dec", "", "$include <prelude.sail>",
            "$include <generic_equality.sail>", "",
            *catalog_id_declarations(program), "",
            "enum Cpuid_flag =", *_constructors(f"CpuidFlag_{flag}" for flag in projection.cpuid_flags), "",
            "enum Semantic_route =",
            *_constructors(ROUTE_CONSTRUCTORS[route] for route in routes), "",
            "enum Instruction_set =", *_constructors(projection.instruction_sets), "",
            "enum Fault_kind =", *_constructors(projection.fault_kinds), "",
            "enum Effect_kind =", *_constructors(projection.effect_kinds), "",
            "enum Event_frame_type =",
            *_constructors(("EventFrameBasic", "EventFrameError", "EventFramePage", "EventFrameAuxiliary")), "",
            "enum Event_family =",
            *_constructors(("EventFamilyNone", *(f"EventFamily_{family}" for family in projection.event_families))), "",
            "enum Architectural_event =",
            *_constructors(f"Event_{item.event_id}" for item in projection.events), "",
            "enum Semantic_operation =",
            *_constructors(item.operation for item in projection.operations), "",
            "function semantic_route(operation : Semantic_operation) -> Semantic_route = match operation {",
        ]
        lines.extend(
            f"  {item.operation} => {ROUTE_CONSTRUCTORS[item.route]},"
            for item in projection.operations
        )
        lines.extend(["}", "", "function semantic_mnemonic(operation : Semantic_operation) -> string = match operation {"])
        lines.extend(
            f'  {item.operation} => "{item.mnemonic}",'
            for item in projection.operations
        )
        lines.extend([
            "}", "", "function all_semantic_operations() -> list(Semantic_operation) = [|",
            "  " + ", ".join(item.operation for item in projection.operations),
            "|]", "",
            "function architectural_event_class(event : Architectural_event) -> bits(8) = match event {",
        ])
        for item in projection.events:
            lines.append(
                f"  Event_{item.event_id} => 0x{item.class_value:02x},"
            )
        lines.extend([
            "}", "",
            "function architectural_event_selector(event : Architectural_event) -> option(bits(24)) = match event {",
        ])
        lines.extend(
            f"  Event_{item.event_id} => "
            + (
                f"Some(0x{item.selector:06x})"
                if item.selector is not None
                else "None()"
            )
            + ","
            for item in projection.events
        )
        lines.extend([
            "}", "",
            "function architectural_event_frame(event : Architectural_event) -> Event_frame_type = match event {",
        ])
        frame_constructors = {
            "basic": "EventFrameBasic",
            "error": "EventFrameError",
            "page": "EventFramePage",
            "auxiliary": "EventFrameAuxiliary",
        }
        lines.extend(
            f"  Event_{item.event_id} => {frame_constructors[item.frame]},"
            for item in projection.events
        )
        lines.extend([
            "}", "",
            "function architectural_event_family(event : Architectural_event) -> Event_family = match event {",
        ])
        lines.extend(
            f"  Event_{item.event_id} => "
            f"{f'EventFamily_{item.family}' if item.family is not None else 'EventFamilyNone'},"
            for item in projection.events
        )
        lines.extend([
            "}", "",
            "function all_architectural_events() -> list(Architectural_event) = [|",
            "  " + ", ".join(f"Event_{item.event_id}" for item in projection.events),
            "|]", "",
        ])
        return "\n".join(lines)


def _constructors(values: Iterable[str]) -> list[str]:
    return [
        f"  {value}" if index == 0 else f"| {value}"
        for index, value in enumerate(values)
    ]


def _operation(bundle: InstructionBundle) -> str:
    return f"Op_{bundle.instruction.mnemonic}"
