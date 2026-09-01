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
    "NoFault",
    "IllegalInstruction",
    "PrivilegeFault",
    "ExtensionUnavailable",
    "InvalidControlState",
    "InvalidControlSelectorFault",
    "ReservedControlBitsFault",
    "InvalidControlImageFault",
    "InvalidControlTransitionFault",
    "DivideByZero",
    "DivideOverflow",
    "BoundsFault",
    "AlignmentFault",
    "TranslationFault",
    "AccessFault",
    "EventFault",
)

BASE_EFFECT_CONSTRUCTORS = (
    "NoEffect",
    "ReadMemory",
    "WriteMemory",
    "AtomicMemory",
    "TranslateAddress",
    "CacheOperation",
    "TlbOperation",
    "ControlRegisterAccess",
    "EventDelivery",
    "TraceMarker",
    "HaltProcessor",
    "ResetProcessor",
    "RepeatBody",
    "FenceOperation",
    "IntegerCompute",
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
class SailControlRegisterProjection:
    owner: str
    constructor: str
    selector: int
    state_field: str | None


@dataclass(frozen=True, slots=True)
class SailRegistryProjection:
    """Active operation, type, CPUID, and event semantics for Sail."""

    cpuid_flags: tuple[str, ...]
    instruction_sets: tuple[str, ...]
    fault_kinds: tuple[str, ...]
    effect_kinds: tuple[str, ...]
    event_families: tuple[str, ...]
    events: tuple[SailEventProjection, ...]
    control_registers: tuple[SailControlRegisterProjection, ...]
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
    "WAIT": SailTypeContribution(
        instruction_sets=("WaitSet",),
    ),
}


class SailRegistryRenderer:
    def project(self, program: SailProgram) -> SailRegistryProjection:
        cpuid_flags = tuple(
            dict.fromkeys(
                field.id
                for bundle in program.bundles
                for field in (
                    *bundle.required_cpuid_flags,
                    *(
                        local
                        for form in bundle.encodings.forms
                        for local in form.additional_cpuid_flags
                    ),
                )
            )
        )
        instruction_sets = ["BaseSet"]
        faults = list(BASE_FAULT_CONSTRUCTORS)
        effects = list(BASE_EFFECT_CONSTRUCTORS)
        for extension_id in program.configuration.extension_ids:
            contribution = EXTENSION_CONTRIBUTIONS.get(
                extension_id, SailTypeContribution()
            )
            declared_instruction_set = program.project.model.extensions[
                extension_id
            ].instruction_set
            instruction_sets.extend(
                (declared_instruction_set,)
                if declared_instruction_set is not None
                else contribution.instruction_sets
            )
            declared_faults = program.project.model.extensions[extension_id].fault_kinds
            faults.extend(declared_faults or contribution.fault_kinds)
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
        owner_order = {
            owner: index
            for index, owner in enumerate(
                ("base", *program.configuration.extension_ids)
            )
        }
        control_registers = tuple(
            sorted(
                program.project.control_registers.selected(
                    program.configuration.owners
                ),
                key=lambda item: (owner_order[item.owner], item.selector),
            )
        )
        generated_state_registers = frozenset(
            (owner, register_id)
            for owner in program.configuration.owners
            for register_id in program.project.control_registers.namespace(
                owner
            ).inventory.generated_state_registers
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
                SailControlRegisterProjection(
                    item.owner,
                    _control_register_constructor(item.owner, item.id),
                    item.selector,
                    (
                        _control_register_state_field(item.owner, item.id)
                        if (item.owner, item.id) in generated_state_registers
                        else None
                    ),
                )
                for item in control_registers
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
            "// Generated from selected ISA catalogs. Do not edit.",
            "",
            *catalog_id_declarations(program),
            "",
            "enum Cpuid_flag =",
            *_constructors(f"CpuidFlag_{flag}" for flag in projection.cpuid_flags),
            "",
            "enum Semantic_route =",
            *_constructors(ROUTE_CONSTRUCTORS[route] for route in routes),
            "",
            "enum Instruction_set =",
            *_constructors(projection.instruction_sets),
            "",
            "enum Fault_kind =",
            *_constructors(projection.fault_kinds),
            "",
            "enum Effect_kind =",
            *_constructors(projection.effect_kinds),
            "",
            "enum Event_frame_type =",
            *_constructors(
                (
                    "EventFrameBasic",
                    "EventFrameError",
                    "EventFramePage",
                    "EventFrameAuxiliary",
                )
            ),
            "",
            "enum Event_family =",
            *_constructors(
                (
                    "EventFamilyNone",
                    *(f"EventFamily_{family}" for family in projection.event_families),
                )
            ),
            "",
            "enum Architectural_event =",
            *_constructors(f"Event_{item.event_id}" for item in projection.events),
            "",
            "enum Control_register =",
            *_constructors(item.constructor for item in projection.control_registers),
            "",
            "struct Control_state = {",
            *(
                f"  {item.state_field} : bits(64),"
                for item in projection.control_registers
                if item.state_field is not None
            ),
            "  interrupt_file : Interrupt_file,",
            "  debug_trigger_file : Debug_trigger_file,",
            "}",
            "",
            "enum Semantic_operation =",
            *_constructors(item.operation for item in projection.operations),
            "",
            "function semantic_route(operation : Semantic_operation) -> Semantic_route = match operation {",
        ]
        lines.extend(
            f"  {item.operation} => {ROUTE_CONSTRUCTORS[item.route]},"
            for item in projection.operations
        )
        lines.extend(
            [
                "}",
                "",
                "function semantic_mnemonic(operation : Semantic_operation) -> string = match operation {",
            ]
        )
        lines.extend(
            f'  {item.operation} => "{item.mnemonic}",'
            for item in projection.operations
        )
        lines.extend(
            [
                "}",
                "",
                "function all_semantic_operations() -> list(Semantic_operation) = [|",
                "  " + ", ".join(item.operation for item in projection.operations),
                "|]",
                "",
                "function architectural_event_class(event : Architectural_event) -> bits(8) = match event {",
            ]
        )
        for item in projection.events:
            lines.append(f"  Event_{item.event_id} => 0x{item.class_value:02x},")
        lines.extend(
            [
                "}",
                "",
                "function architectural_event_selector(event : Architectural_event) -> option(bits(24)) = match event {",
            ]
        )
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
        lines.extend(
            [
                "}",
                "",
                "function architectural_event_frame(event : Architectural_event) -> Event_frame_type = match event {",
            ]
        )
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
        lines.extend(
            [
                "}",
                "",
                "function architectural_event_family(event : Architectural_event) -> Event_family = match event {",
            ]
        )
        lines.extend(
            f"  Event_{item.event_id} => "
            f"{f'EventFamily_{item.family}' if item.family is not None else 'EventFamilyNone'},"
            for item in projection.events
        )
        lines.extend(
            [
                "}",
                "",
                "function all_architectural_events() -> list(Architectural_event) = [|",
                "  "
                + ", ".join(f"Event_{item.event_id}" for item in projection.events),
                "|]",
                "",
            ]
        )
        lines.extend(
            [
                "function control_register_from_selector(selector : int) -> option(Control_register) =",
            ]
        )
        for index, item in enumerate(projection.control_registers):
            prefix = "  if" if index == 0 else "  else if"
            lines.append(
                f"{prefix} selector == {item.selector} then Some({item.constructor})"
            )
        lines.extend(("  else None()", ""))
        lines.extend(("function initial_control_state() -> Control_state = struct {",))
        lines.extend(
            f"  {item.state_field} = 0x0000000000000000,"
            for item in projection.control_registers
            if item.state_field is not None
        )
        lines.extend(
            (
                "  interrupt_file = initial_interrupt_file(),",
                "  debug_trigger_file = initial_debug_trigger_file(),",
                "}",
                "",
                "val control_state_value : (Control_state, Control_register) -> bits(64)",
                "",
                "scattered function control_state_value",
                "",
            )
        )
        lines.extend(
            f"function clause control_state_value(state, {item.constructor}) = "
            f"state.{item.state_field}"
            for item in projection.control_registers
            if item.state_field is not None
        )
        lines.extend(
            (
                "",
                "val control_state_with_value :",
                "  (Control_state, Control_register, bits(64)) -> Control_state",
                "",
                "scattered function control_state_with_value",
                "",
            )
        )
        lines.extend(
            f"function clause control_state_with_value(state, {item.constructor}, value) = "
            f"{{ state with {item.state_field} = value }}"
            for item in projection.control_registers
            if item.state_field is not None
        )
        lines.extend(("",))
        return "\n".join(lines)


def _constructors(values: Iterable[str]) -> list[str]:
    return [
        f"  {value}" if index == 0 else f"| {value}"
        for index, value in enumerate(values)
    ]


def _operation(bundle: InstructionBundle) -> str:
    return f"Op_{bundle.instruction.mnemonic}"


def _control_register_constructor(owner: str, register_id: str) -> str:
    return f"ControlRegister_{owner.upper()}_{register_id}"


def _control_register_state_field(owner: str, register_id: str) -> str:
    return f"{owner.lower()}_{register_id.lower()}"


def instruction_set_constructor(program: SailProgram, owner: str) -> str:
    if owner == "base":
        return "BaseSet"
    declared = program.project.model.extensions[owner].instruction_set
    if declared is not None:
        return declared
    contribution = EXTENSION_CONTRIBUTIONS.get(owner)
    if contribution is None or len(contribution.instruction_sets) != 1:
        raise ValueError(f"{owner}: no Sail instruction-set constructor")
    return contribution.instruction_sets[0]
