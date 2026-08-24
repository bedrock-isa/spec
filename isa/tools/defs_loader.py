"""Load ISA definition indexes and extension metadata."""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import product
from pathlib import Path
import re
from typing import Any

from artifact_overlay import resolve_source
from defs_schema import (
    CpuidFlag,
    DiagramArtifactRef,
    FLAG_EFFECT_REFERENCE_KIND,
    FlagEffectDefinition,
    FormApplicability,
    LogicalOperandDefinition,
    NamedValueDefinition,
    OperationArtifactRef,
    OperationArtifacts,
    OperationCase,
    OperationDocument,
    OperationEventContract,
    OperationFlagBankContract,
    OperationRepeatEligibility,
    PredicateContract,
    PublicInstructionRef,
    decode_encodings,
    decode_extension_catalog,
    decode_extension_manifest,
    decode_cpuid_flag_registry,
    decode_flag_effect_definition_registry,
    decode_instruction_set_index,
    decode_named_value_registry,
    decode_operation,
    decode_operand_registry,
    decode_register_registry,
    decode_semantic_condition_registry,
    decode_size_registry,
)
from encoding_fields import FieldTypeRegistry, build_field_type_registry

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment error path
    raise SystemExit("PyYAML is required to load ISA definition files") from exc


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ExtensionDef:
    path: Path
    name: str
    data: dict[str, Any]


@dataclass(frozen=True)
class InstructionSetDef:
    name: str
    root: Path
    include: Path
    title: str
    introduction: Path | None = None


@dataclass(frozen=True)
class CanonicalOperation:
    """Format-neutral operation projection returned by the sole coordinator."""

    id: str
    title: str
    summary: str
    public_instruction: PublicInstructionRef
    execution_route: str | None
    privilege: str
    base_requirements: tuple[str, ...]
    repeat: OperationRepeatEligibility
    logical_operand_ids: tuple[str, ...]
    operands: tuple[LogicalOperandDefinition, ...] | None
    forms: tuple[str, ...]
    cases: tuple["CanonicalOperationCase", ...]
    artifacts: OperationArtifacts | None


@dataclass(frozen=True)
class CanonicalOperationCase:
    id: str | None
    applies_to: FormApplicability
    additional_requirements: tuple[str, ...]
    resolved_requirements: tuple[str, ...]
    predicate: PredicateContract | None
    flags: tuple[OperationFlagBankContract, ...] | None
    events: tuple[OperationEventContract, ...] | None
    sail_entry: str | None
    conversion: object | None


def _artifact_file(bundle_root: Path, manifest_path: Path, reference: OperationArtifactRef | DiagramArtifactRef) -> Path:
    candidate = bundle_root / reference.path
    resolved_root = bundle_root.resolve()
    logical_source = candidate.resolve()
    if not logical_source.is_relative_to(resolved_root):
        raise ValueError(
            f"{manifest_path}: artifact {reference.path!r} resolves outside its operation bundle"
        )
    if logical_source.is_relative_to(REPOSITORY_ROOT.resolve()):
        resolved = resolve_source(logical_source, REPOSITORY_ROOT).resolve()
        if not resolved.is_file() and logical_source.suffix == ".tex":
            resolved = resolve_source(
                logical_source.with_suffix(logical_source.suffix + ".in"), REPOSITORY_ROOT
            ).resolve()
    else:
        resolved = logical_source
    if not resolved.is_file():
        raise ValueError(f"{manifest_path}: artifact {reference.path!r} does not exist as a file")
    expected_suffixes = {
        "sail": (".sail",),
        "tex": (".tex",),
        "markdown": (".md", ".markdown"),
    }
    suffixes = expected_suffixes.get(reference.kind, (".yaml",))
    if not any(reference.path.endswith(suffix) for suffix in suffixes):
        raise ValueError(
            f"{manifest_path}: artifact {reference.path!r} has wrong file kind for {reference.kind!r}"
        )
    return resolved


def _range_values(value: int | str) -> set[int]:
    if isinstance(value, int):
        return {value}
    text = value.replace("_", "")
    if ".." in text:
        lower, upper = text.split("..", 1)
        return set(range(int(lower, 0), int(upper, 0) + 1))
    return {int(text, 0)}


def _selector_domains(form: Any, size_definitions: dict[str, Any] | None, path: Path) -> dict[str, tuple[str, ...]]:
    result: dict[str, tuple[str, ...]] = {}
    for marker, field in form.fields.items():
        if not field.type.startswith("size."):
            continue
        domain = field.type.removeprefix("size.")
        if domain in result:
            raise ValueError(f"{path}:{form.id}: selector domain {domain!r} occurs more than once")
        if size_definitions is None:
            raise ValueError(f"{path}:{form.id}: size definitions are required for selector {domain!r}")
        kind = size_definitions.get("size_kinds", {}).get(domain)
        if not isinstance(kind, dict) or not isinstance(kind.get("values"), list):
            raise ValueError(f"{path}:{form.id}: unknown selector domain {domain!r}")
        allowed_raw = {
            int(entry["value"], 0) if isinstance(entry["value"], str) else int(entry["value"])
            for entry in kind["values"]
        }
        for constraint in form.constraints:
            if constraint.field == marker and constraint.allow:
                allowed_raw &= set().union(*(_range_values(value) for value in constraint.allow))
        values = tuple(
            str(entry["code"])
            for entry in kind["values"]
            if (int(entry["value"], 0) if isinstance(entry["value"], str) else int(entry["value"])) in allowed_raw
        )
        if not values:
            raise ValueError(f"{path}:{form.id}: selector domain {domain!r} has no legal values")
        result[domain] = values
    return result


def _legal_case_tuples(
    encodings: Any,
    size_definitions: dict[str, Any] | None,
    path: Path,
) -> tuple[tuple[str, tuple[tuple[str, str], ...], tuple[tuple[str, str], ...]], ...]:
    tuples: list[tuple[str, tuple[tuple[str, str], ...], tuple[tuple[str, str], ...]]] = []
    for form in encodings.forms:
        selectors = _selector_domains(form, size_definitions, path)
        selector_names = tuple(sorted(selectors))
        selector_products = product(*(selectors[name] for name in selector_names))
        profiles = tuple(sorted((operand.name, operand.type) for operand in form.operands))
        for selected_values in selector_products:
            tuples.append(
                (
                    form.id,
                    tuple(zip(selector_names, selected_values)),
                    profiles,
                )
            )
    return tuple(tuples)


def _case_matches(
    case: OperationCase,
    legal_tuple: tuple[str, tuple[tuple[str, str], ...], tuple[tuple[str, str], ...]],
) -> bool:
    form_id, selector_values, operand_profiles = legal_tuple
    if form_id not in case.applies_to.forms:
        return False
    selector_map = dict(selector_values)
    if any(
        selector_map.get(selector.domain) not in selector.values
        for selector in case.applies_to.selectors
    ):
        return False
    profile_map = dict(operand_profiles)
    return not any(
        profile_map.get(selector.operand) not in selector.profiles
        for selector in case.applies_to.operand_profiles
    )


def _validate_conversion_signatures(
    manifest_path: Path, document: OperationDocument, encodings: Any
) -> None:
    """Tie each typed conversion source format to its encoding selectors.

    A conversion case with a selector is deliberately not permitted to name a
    second, display-derived size set.  Its source formats must be precisely the
    values selected by the case across its forms.  Fixed destination formats are
    represented explicitly because they have no selector field to recover from.
    """

    forms_by_id = {form.id: form for form in encodings.forms}
    for case in document.cases:
        signature = case.conversion
        if signature is None:
            continue
        selected: set[str] = set()
        for selector in case.applies_to.selectors:
            selected.update(selector.values)
        if selected and set(signature.source_formats) != selected:
            raise ValueError(
                f"{manifest_path}: case {case.id!r} conversion source formats "
                f"{list(signature.source_formats)!r} do not match selected formats "
                f"{sorted(selected)!r}"
            )
        if not selected:
            # A selector-free conversion must explicitly identify an applicable
            # form whose operands establish the two numeric domains.
            if not case.applies_to.forms:
                raise ValueError(
                    f"{manifest_path}: case {case.id!r} conversion has no applicable forms"
                )
        for form_id in case.applies_to.forms:
            if form_id not in forms_by_id:
                raise ValueError(
                    f"{manifest_path}: case {case.id!r} conversion references unknown form {form_id!r}"
                )


def _encoding_transport_matches_logical_access(
    declared_operand: LogicalOperandDefinition,
    encoded_operand: Any,
) -> bool:
    """Match one encoding transport to its operation-level logical access."""

    vector_value_destination_profiles = frozenset({"Vn", "VEA"})
    uses_vector_value_destination_pair = (
        declared_operand.role == "destination"
        and declared_operand.access == "read_write"
        and declared_operand.value_domain == "vector"
        and frozenset(declared_operand.profiles)
        == vector_value_destination_profiles
    )
    if uses_vector_value_destination_pair:
        if encoded_operand.type == "Vn":
            return (
                encoded_operand.access == "read_write"
                and encoded_operand.ea_role is None
            )
        if encoded_operand.type == "VEA":
            return (
                encoded_operand.access in {"write", "read_write"}
                and encoded_operand.ea_role == "value"
            )
        return False

    address_transport_profiles = frozenset({"EA", "Rn"})
    uses_address_transport_pair = (
        declared_operand.role == "address"
        and declared_operand.access == "address"
        and frozenset(declared_operand.profiles) == address_transport_profiles
    )
    if not uses_address_transport_pair:
        return encoded_operand.access == declared_operand.access
    if encoded_operand.type == "EA":
        return (
            encoded_operand.access == "address"
            and encoded_operand.ea_role == "address"
        )
    if encoded_operand.type == "Rn":
        return encoded_operand.access == "read" and encoded_operand.ea_role is None
    return False


def _validate_bundle_contract(
    manifest_path: Path,
    document: OperationDocument,
    encodings: Any,
    operand_types: dict[str, Any],
    size_definitions: dict[str, Any] | None,
) -> None:
    encoded_forms = tuple(form.id for form in encodings.forms)
    encoded = set(encoded_forms)
    if not encoded_forms:
        raise ValueError(
            f"{manifest_path}: encodings.yaml must define at least one operation form"
        )
    for case in document.cases:
        unknown_forms = set(case.applies_to.forms) - encoded
        if unknown_forms:
            raise ValueError(
                f"{manifest_path}: case {case.id!r} applies_to.forms references "
                f"unknown encoding forms {', '.join(sorted(unknown_forms))}"
            )
    declared_operands = {operand.id: operand for operand in document.operands}
    reached_operands: set[str] = set()
    reached_profiles: dict[str, set[str]] = {
        operand.id: set() for operand in document.operands
    }
    forms_by_id = {form.id: form for form in encodings.forms}
    for form in encodings.forms:
        for operand in form.operands:
            if operand.type not in operand_types:
                raise ValueError(
                    f"{manifest_path}: form {form.id!r} references unknown operand profile {operand.type!r}"
                )
            declared_operand = declared_operands.get(operand.name)
            if declared_operand is None:
                raise ValueError(
                    f"{manifest_path}: form {form.id!r} references undeclared logical operand {operand.name!r}"
                )
            reached_operands.add(operand.name)
            reached_profiles[operand.name].add(operand.type)
            if operand.type not in declared_operand.profiles:
                raise ValueError(
                    f"{manifest_path}: form {form.id!r} operand {operand.name!r} uses undeclared profile {operand.type!r}"
                )
            if not _encoding_transport_matches_logical_access(
                declared_operand, operand
            ):
                raise ValueError(
                    f"{manifest_path}: form {form.id!r} operand {operand.name!r} "
                    "access differs from its logical operand or its encoding transport "
                    f"is incompatible (logical role {declared_operand.role!r}, access "
                    f"{declared_operand.access!r}, profiles {declared_operand.profiles!r}; "
                    f"encoded profile {operand.type!r}, access {operand.access!r}, "
                    f"ea_role {operand.ea_role!r})"
                )
    unreachable_operands = set(declared_operands) - reached_operands
    if unreachable_operands:
        raise ValueError(
            f"{manifest_path}: logical operands are unreachable: {', '.join(sorted(unreachable_operands))}"
        )
    for operand in document.operands:
        unused_profiles = set(operand.profiles) - reached_profiles[operand.id]
        if unused_profiles:
            raise ValueError(
                f"{manifest_path}: logical operand {operand.id!r} has unreachable profiles "
                f"{', '.join(sorted(unused_profiles))}"
            )
    repeat_observed = document.repeat.observed
    repeat_operand = getattr(repeat_observed, "operand", None)
    if repeat_operand is not None:
        missing_forms = [
            form.id
            for form in encodings.forms
            if repeat_operand not in {operand.name for operand in form.operands}
        ]
        if missing_forms:
            raise ValueError(
                f"{manifest_path}: repeat operand {repeat_operand!r} is absent from forms "
                f"{', '.join(missing_forms)}"
            )

    legal_tuples = _legal_case_tuples(encodings, size_definitions, manifest_path)
    for case in document.cases:
        predicate_operands = tuple(
            reference
            for reference in (
                case.predicate.condition_operand,
                case.predicate.destination_operand,
                case.predicate.counter_operand,
            )
            if reference is not None
        )
        for form_id in case.applies_to.forms:
            form_operand_names = {
                operand.name for operand in forms_by_id[form_id].operands
            }
            missing_predicate_operands = set(predicate_operands) - form_operand_names
            if missing_predicate_operands:
                raise ValueError(
                    f"{manifest_path}: case {case.id!r} predicate operands are absent "
                    f"from form {form_id!r}: {', '.join(sorted(missing_predicate_operands))}"
                )
        for selector in case.applies_to.selectors:
            legal_values: set[str] = set()
            for form_id in case.applies_to.forms:
                domains = _selector_domains(forms_by_id[form_id], size_definitions, manifest_path)
                if selector.domain not in domains:
                    raise ValueError(
                        f"{manifest_path}: case {case.id!r} selector {selector.domain!r} is absent from form {form_id!r}"
                    )
                legal_values.update(domains[selector.domain])
            unknown = set(selector.values) - legal_values
            if unknown:
                raise ValueError(
                    f"{manifest_path}: case {case.id!r} selector {selector.domain!r} has unreachable values {sorted(unknown)}"
                )
        for selector in case.applies_to.operand_profiles:
            legal_profiles: set[str] = set()
            for form_id in case.applies_to.forms:
                form_profiles = {
                    operand.name: operand.type for operand in forms_by_id[form_id].operands
                }
                if selector.operand not in form_profiles:
                    raise ValueError(
                        f"{manifest_path}: case {case.id!r} operand profile {selector.operand!r} is absent from form {form_id!r}"
                    )
                legal_profiles.add(form_profiles[selector.operand])
            unknown = set(selector.profiles) - legal_profiles
            if unknown:
                raise ValueError(
                    f"{manifest_path}: case {case.id!r} operand {selector.operand!r} has unreachable profiles {sorted(unknown)}"
                )

    reachability = {case.id: 0 for case in document.cases}
    for legal_tuple in legal_tuples:
        matches = [case for case in document.cases if _case_matches(case, legal_tuple)]
        if not matches:
            raise ValueError(
                f"{manifest_path}: operation cases leave a gap for form {legal_tuple[0]!r}, "
                f"selectors {dict(legal_tuple[1])}, operand profiles {dict(legal_tuple[2])}"
            )
        if len(matches) != 1:
            raise ValueError(
                f"{manifest_path}: operation cases overlap for form {legal_tuple[0]!r}, "
                f"selectors {dict(legal_tuple[1])}, operand profiles {dict(legal_tuple[2])}: "
                f"{', '.join(case.id for case in matches)}"
            )
        reachability[matches[0].id] += 1
    unreachable_cases = sorted(case_id for case_id, count in reachability.items() if count == 0)
    if unreachable_cases:
        raise ValueError(
            f"{manifest_path}: operation cases are unreachable: {', '.join(unreachable_cases)}"
        )


def _validate_base_requirements(
    bundle_root: Path,
    base_requirements: tuple[str, ...],
    known_cpuid_flags: frozenset[str],
) -> tuple[str, ...]:
    unknown = set(base_requirements) - known_cpuid_flags
    if unknown:
        raise ValueError(
            f"{bundle_root}: unknown inherited CPUID flags "
            f"{', '.join(sorted(unknown))}"
        )
    return tuple(sorted(set(base_requirements)))


def _load_operation(
    bundle_root: Path,
    *,
    operand_types: dict[str, Any],
    size_definitions: dict[str, Any] | None = None,
    base_requirements: tuple[str, ...] = (),
    known_cpuid_flags: frozenset[str],
    known_event_ids: frozenset[str],
    known_event_causes: dict[str, frozenset[str]],
    known_condition_ids: frozenset[str],
    known_named_value_ids: frozenset[str],
    known_diagram_kinds: frozenset[str],
    known_flag_effect_definitions: dict[str, FlagEffectDefinition],
) -> CanonicalOperation:
    bundle_root = bundle_root.resolve()
    operation_path = bundle_root / "operation.yaml"
    encodings_path = bundle_root / "encodings.yaml"
    encodings = decode_encodings(encodings_path, load_yaml(encodings_path))
    base_requirements = _validate_base_requirements(
        bundle_root, base_requirements, known_cpuid_flags
    )
    document = decode_operation(operation_path, load_yaml(operation_path))
    unknown_case_requirements = {
        requirement
        for case in document.cases
        for requirement in case.additional_requirements
        if requirement not in known_cpuid_flags
    }
    if unknown_case_requirements:
        raise ValueError(
            f"{operation_path}: unknown case CPUID flags "
            f"{', '.join(sorted(unknown_case_requirements))}"
        )
    repeated_case_requirements = {
        requirement
        for case in document.cases
        for requirement in case.additional_requirements
        if requirement in base_requirements
    }
    if repeated_case_requirements:
        raise ValueError(
            f"{operation_path}: case requirements repeat inherited CPUID flags "
            f"{', '.join(sorted(repeated_case_requirements))}"
        )
    public_mnemonics = {
        document.public_instruction.mnemonic,
        *document.public_instruction.aliases,
    }
    from defs_schema import parse_assembly_template

    for form in encodings.forms:
        syntax_mnemonic = parse_assembly_template(
            form.syntax, f"{operation_path}:{form.id}"
        ).mnemonic
        if syntax_mnemonic not in public_mnemonics:
            raise ValueError(
                f"{operation_path}: form {form.id!r} uses mnemonic {syntax_mnemonic!r}; "
                "expected the declared public mnemonic or alias"
            )
    _validate_bundle_contract(
        operation_path, document, encodings, operand_types, size_definitions
    )
    _validate_conversion_signatures(operation_path, document, encodings)
    unknown_predicate_values = {
        case.predicate.observed
        for case in document.cases
        if case.predicate.observed is not None
        and case.predicate.observed not in known_named_value_ids
    }
    if unknown_predicate_values:
        raise ValueError(
            f"{operation_path}: predicates reference unknown named value IDs "
            f"{', '.join(sorted(unknown_predicate_values))}"
        )
    unknown_events = {
        event.event
        for case in document.cases
        for event in case.events
        if event.event not in known_event_ids
    }
    if unknown_events:
        raise ValueError(
            f"{operation_path}: unknown event IDs {', '.join(sorted(unknown_events))}"
        )
    unknown_conditions = {
        event.condition
        for case in document.cases
        for event in case.events
        if event.condition not in known_condition_ids
    }
    if unknown_conditions:
        raise ValueError(
            f"{operation_path}: unknown semantic condition IDs "
            f"{', '.join(sorted(unknown_conditions))}"
        )
    for case in document.cases:
        forms_by_id = {form.id: form for form in encodings.forms}
        for event in case.events:
            if event.cause is not None:
                event_causes = known_event_causes.get(event.event, frozenset())
                if event.cause not in event_causes:
                    owners = sorted(
                        event_name
                        for event_name, causes in known_event_causes.items()
                        if event.cause in causes
                    )
                    if owners:
                        raise ValueError(
                            f"{operation_path}: case {case.id!r} cause {event.cause} "
                            f"belongs to {', '.join(owners)}, not {event.event}"
                        )
                    if not event_causes:
                        raise ValueError(
                            f"{operation_path}: case {case.id!r} event {event.event} "
                            f"has no architected cause space for {event.cause}"
                        )
                    raise ValueError(
                        f"{operation_path}: case {case.id!r} event {event.event} "
                        f"has unknown architectural cause {event.cause}"
                    )
            if event.condition == "destination_overlap":
                missing_overlap = [
                    form_id
                    for form_id in case.applies_to.forms
                    if not any(
                        relation.rule == "illegal_instruction"
                        for relation in forms_by_id[form_id].destination_overlap
                    )
                ]
                if missing_overlap:
                    raise ValueError(
                        f"{operation_path}: case {case.id!r} destination-overlap "
                        "event requires an illegal_instruction destination_overlap "
                        "relation in forms "
                        + ", ".join(missing_overlap)
                    )
    for case in document.cases:
        for bank in case.flags:
            for effect in bank.effects:
                if effect.reference is None:
                    continue
                definition = known_flag_effect_definitions.get(effect.reference)
                if definition is None:
                    raise ValueError(
                        f"{operation_path}: case {case.id!r} {bank.bank}.{effect.flag} "
                        f"references unknown flag effect definition {effect.reference!r}"
                    )
                expected_kind = FLAG_EFFECT_REFERENCE_KIND[effect.effect]
                if definition.kind != expected_kind:
                    raise ValueError(
                        f"{operation_path}: case {case.id!r} {bank.bank}.{effect.flag} "
                        f"uses {definition.kind!r} definition {effect.reference!r} for "
                        f"{effect.effect!r}; expected {expected_kind!r}"
                    )
    unknown_diagram_kinds = {
        diagram.kind
        for diagram in document.artifacts.diagrams
        if diagram.kind not in known_diagram_kinds
    }
    if unknown_diagram_kinds:
        raise ValueError(
            f"{operation_path}: unknown diagram kinds "
            f"{', '.join(sorted(unknown_diagram_kinds))}"
        )
    case_ids = {case.id for case in document.cases}
    unknown_diagram_cases = {
        diagram.case for diagram in document.artifacts.diagrams
        if diagram.case is not None and diagram.case not in case_ids
    }
    if unknown_diagram_cases:
        raise ValueError(
            f"{operation_path}: diagrams reference unknown case IDs "
            f"{', '.join(sorted(unknown_diagram_cases))}"
        )
    _artifact_file(bundle_root, operation_path, document.artifacts.semantics)
    _artifact_file(bundle_root, operation_path, document.artifacts.description)
    for diagram in document.artifacts.diagrams:
        _artifact_file(bundle_root, operation_path, diagram)
    canonical_artifacts = replace(
        document.artifacts,
        bundle_root=str(bundle_root),
        manifest_path=str(operation_path),
    )
    canonical_cases = tuple(
        CanonicalOperationCase(
            id=case.id,
            applies_to=case.applies_to,
            additional_requirements=case.additional_requirements,
            resolved_requirements=tuple(
                sorted(set(base_requirements) | set(case.additional_requirements))
            ),
            predicate=case.predicate,
            flags=case.flags,
            events=case.events,
            sail_entry=case.sail_entry,
            conversion=case.conversion,
        )
        for case in document.cases
    )
    return CanonicalOperation(
        id=document.id,
        title=document.title,
        summary=document.summary,
        public_instruction=document.public_instruction,
        execution_route=document.execution_route,
        privilege=document.privilege,
        base_requirements=tuple(sorted(set(base_requirements))),
        repeat=document.repeat,
        logical_operand_ids=tuple(operand.id for operand in document.operands),
        operands=document.operands,
        forms=tuple(form.id for form in encodings.forms),
        cases=canonical_cases,
        artifacts=canonical_artifacts,
    )


def load_operation(
    bundle_root: Path,
    *,
    operand_types: dict[str, Any],
    size_definitions: dict[str, Any] | None = None,
    base_requirements: tuple[str, ...] = (),
    known_cpuid_flags: frozenset[str],
    known_event_ids: frozenset[str],
    known_event_causes: dict[str, frozenset[str]],
    known_condition_ids: frozenset[str],
    known_named_value_ids: frozenset[str],
    known_diagram_kinds: frozenset[str],
    known_flag_effect_definitions: dict[str, FlagEffectDefinition],
) -> CanonicalOperation:
    """Load the required operation bundle for one instruction directory."""

    bundle_root = bundle_root.resolve()
    if not (bundle_root / "operation.yaml").is_file():
        raise ValueError(f"{bundle_root}: expected operation.yaml")
    return _load_operation(
        bundle_root,
        operand_types=operand_types,
        size_definitions=size_definitions,
        base_requirements=base_requirements,
        known_cpuid_flags=known_cpuid_flags,
        known_event_ids=known_event_ids,
        known_event_causes=known_event_causes,
        known_condition_ids=known_condition_ids,
        known_named_value_ids=known_named_value_ids,
        known_diagram_kinds=known_diagram_kinds,
        known_flag_effect_definitions=known_flag_effect_definitions,
    )


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def load_extension_catalog(defs_root: Path) -> dict[str, Any]:
    path = defs_root / "extensions.yaml"
    data = load_yaml(path)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    decode_extension_catalog(path, data)
    return data


def load_extensions(
    defs_root: Path,
    catalog: dict[str, Any] | None = None,
) -> dict[str, ExtensionDef]:
    catalog = catalog if catalog is not None else load_extension_catalog(defs_root)
    extensions: dict[str, ExtensionDef] = {}
    loaded_paths: set[Path] = set()

    def visit(
        path: Path,
        parent_name: str | None = None,
        expected_local_name: str | None = None,
    ) -> None:
        resolved_path = path.resolve()
        if resolved_path in loaded_paths:
            raise ValueError(f"{path}: extension definition is referenced more than once")
        loaded_paths.add(resolved_path)
        data = load_yaml(path)
        if not isinstance(data, dict):
            raise ValueError(f"{path}: expected mapping")
        decode_extension_manifest(path, data)
        local_name = data.get("name")
        if not isinstance(local_name, str) or not local_name:
            raise ValueError(f"{path}: extension name must be a non-empty string")
        if expected_local_name is not None and local_name != expected_local_name:
            raise ValueError(
                f"{path}: extension name {local_name!r} does not match "
                f"catalog entry {expected_local_name!r}"
            )
        qualified_name = f"{parent_name}.{local_name}" if parent_name else local_name
        if qualified_name in extensions:
            raise ValueError(f"{path}: duplicate extension name {qualified_name!r}")
        extensions[qualified_name] = ExtensionDef(path, qualified_name, data)

        children = data.get("extensions", [])
        if not isinstance(children, list):
            raise ValueError(f"{path}: extensions must be a list")
        for child_ref in children:
            if not isinstance(child_ref, str) or not child_ref:
                raise ValueError(f"{path}: extension references must be non-empty strings")
            visit(path.parent / child_ref, qualified_name)

    extension_names = catalog.get("extensions", [])
    catalog_path = defs_root / "extensions.yaml"
    if not isinstance(extension_names, list):
        raise ValueError(f"{catalog_path}: extensions must be a list")
    for extension_name in extension_names:
        if not isinstance(extension_name, str) or not extension_name:
            raise ValueError(
                f"{catalog_path}: extension names must be non-empty strings"
            )
        visit(
            defs_root / "extensions" / extension_name / "extension.yaml",
            expected_local_name=extension_name,
        )
    return extensions


def extension_cpuid_requirements(
    extensions: dict[str, ExtensionDef],
    cpuid_flags: dict[str, CpuidFlag],
) -> tuple[frozenset[str], dict[str, tuple[str, ...]]]:
    """Validate local references and return inherited flags per instruction set."""

    known_flags = frozenset(cpuid_flags)
    by_set: dict[str, tuple[str, ...]] = {"base": ()}
    for extension_name in extensions:
        requirements: list[str] = []
        parts = extension_name.split(".")
        for length in range(1, len(parts) + 1):
            ancestor = extensions[".".join(parts[:length])]
            availability = ancestor.data.get("availability")
            if availability is not None:
                local = availability.get("required_cpuid_flags")
                if not isinstance(local, list):
                    raise ValueError(
                        f"{ancestor.path}: availability.required_cpuid_flags must be a list"
                    )
                for flag in local:
                    if flag not in known_flags:
                        raise ValueError(
                            f"{ancestor.path}: unknown required CPUID flag {flag!r}"
                        )
                    if flag in requirements:
                        raise ValueError(
                            f"{ancestor.path}: required CPUID flag {flag!r} duplicates an inherited requirement"
                        )
                    requirements.append(flag)
        by_set[extension_name] = tuple(requirements)
    return known_flags, by_set


def load_cpuid_flags(defs_root: Path) -> dict[str, CpuidFlag]:
    """Load the authoritative CPUID flag registry keyed by stable ID."""

    path = defs_root / "cpuid_flags.yaml"
    registry = decode_cpuid_flag_registry(path, load_yaml(path))
    return {flag.id: flag for flag in registry.cpuid_flags}


def load_semantic_conditions(defs_root: Path) -> dict[str, str]:
    """Load semantic condition IDs with their reader-facing conditional prose."""

    path = defs_root / "semantic_conditions.yaml"
    registry = decode_semantic_condition_registry(path, load_yaml(path))
    return {
        condition.id: condition.reader_text for condition in registry.conditions
    }


def load_named_values(defs_root: Path) -> dict[str, NamedValueDefinition]:
    """Load operation-defined semantic values keyed by stable ID."""

    path = defs_root / "named_values.yaml"
    registry = decode_named_value_registry(path, load_yaml(path))
    return {value.id: value for value in registry.values}


def load_flag_effect_definitions(
    defs_root: Path,
) -> dict[str, FlagEffectDefinition]:
    """Load typed flag definitions keyed by their internal reference ID."""

    path = defs_root / "flag_effect_definitions.yaml"
    registry = decode_flag_effect_definition_registry(path, load_yaml(path))
    return {definition.id: definition for definition in registry.definitions}


def load_architectural_event_ids(path: Path) -> frozenset[str]:
    """Load event IDs from the architecture event table owner."""

    data = load_yaml(path)
    events = data.get("architectural_events") if isinstance(data, dict) else None
    if not isinstance(events, list):
        raise ValueError(f"{path}: architectural_events must be a list")
    result: list[str] = []
    for index, item in enumerate(events):
        if not isinstance(item, dict):
            raise ValueError(f"{path}: architectural_events[{index}] must be a mapping")
        name = item.get("name")
        if not isinstance(name, str) or not re.fullmatch(r"[A-Z][A-Z0-9_]*", name):
            raise ValueError(f"{path}: architectural_events[{index}].name is invalid")
        result.append(name)
    if len(result) != len(set(result)):
        raise ValueError(f"{path}: architectural event names must be unique")
    return frozenset(result)


def load_architectural_event_causes(path: Path) -> dict[str, frozenset[str]]:
    """Load each event's finite architectural cause namespace."""

    data = load_yaml(path)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    event_ids = load_architectural_event_ids(path)
    raw_spaces = data.get("exception_causes")
    if not isinstance(raw_spaces, dict):
        raise ValueError(f"{path}: exception_causes must be a mapping")
    unknown_events = set(raw_spaces) - event_ids
    if unknown_events:
        raise ValueError(
            f"{path}: exception_causes names unknown events "
            f"{', '.join(sorted(unknown_events))}"
        )
    result: dict[str, frozenset[str]] = {event: frozenset() for event in event_ids}
    for event, raw_causes in raw_spaces.items():
        if not isinstance(raw_causes, list):
            raise ValueError(f"{path}: exception_causes.{event} must be a list")
        names: list[str] = []
        for index, raw_cause in enumerate(raw_causes):
            if not isinstance(raw_cause, dict):
                raise ValueError(
                    f"{path}: exception_causes.{event}[{index}] must be a mapping"
                )
            name = raw_cause.get("name")
            if not isinstance(name, str) or not re.fullmatch(r"[A-Z][A-Z0-9_]*", name):
                raise ValueError(
                    f"{path}: exception_causes.{event}[{index}].name is invalid"
                )
            names.append(name)
        if len(names) != len(set(names)):
            raise ValueError(f"{path}: exception_causes.{event} names must be unique")
        result[event] = frozenset(names)
    return result


def load_instruction_sets(
    defs_root: Path,
    extensions: dict[str, ExtensionDef] | None = None,
) -> list[InstructionSetDef]:
    extensions = extensions if extensions is not None else load_extensions(defs_root)
    base_include = defs_root / "instructions.yaml"
    base_index = decode_instruction_set_index(base_include, load_yaml(base_include))
    instruction_sets = [
        InstructionSetDef(
            "base",
            defs_root,
            base_include,
            base_index.title,
            base_include.parent / base_index.introduction
            if base_index.introduction
            else None,
        )
    ]
    names = {"base"}

    for extension in extensions.values():
        include_ref = extension.data.get("instructions")
        if include_ref is None:
            continue
        if not isinstance(include_ref, str) or not include_ref:
            raise ValueError(f"{extension.path}: instructions path must be a string")
        if extension.name in names:
            raise ValueError(f"{extension.path}: duplicate instruction set {extension.name!r}")
        include_path = extension.path.parent / include_ref
        index = decode_instruction_set_index(include_path, load_yaml(include_path))
        instruction_sets.append(
            InstructionSetDef(
                extension.name,
                extension.path.parent,
                include_path,
                index.title,
                include_path.parent / index.introduction
                if index.introduction
                else None,
            )
        )
        names.add(extension.name)
    return instruction_sets


def load_operand_types(
    defs_root: Path,
    extensions: dict[str, ExtensionDef] | None = None,
) -> dict[str, Any]:
    extensions = extensions if extensions is not None else load_extensions(defs_root)
    paths = [defs_root / "operands.yaml"]
    for extension in extensions.values():
        operands_ref = extension.data.get("operands")
        if operands_ref is None:
            continue
        if not isinstance(operands_ref, str) or not operands_ref:
            raise ValueError(f"{extension.path}: operands path must be a string")
        paths.append(extension.path.parent / operands_ref)

    operand_types: dict[str, Any] = {}
    for path in paths:
        data = load_yaml(path)
        decode_operand_registry(path, data)
        declared = data.get("operand_types") if isinstance(data, dict) else None
        if not isinstance(declared, dict):
            raise ValueError(f"{path}: expected operand_types mapping")
        for name, definition in declared.items():
            if name in operand_types:
                raise ValueError(f"{path}: duplicate operand type {name!r}")
            if not isinstance(definition, dict):
                raise ValueError(f"{path}: operand type {name!r} must be a mapping")
            operand_types[str(name)] = definition
    return operand_types


def load_size_definitions(
    defs_root: Path,
    extensions: dict[str, ExtensionDef] | None = None,
) -> dict[str, Any]:
    extensions = extensions if extensions is not None else load_extensions(defs_root)
    paths = [defs_root / "sizes.yaml"]
    for extension in extensions.values():
        sizes_ref = extension.data.get("sizes")
        if sizes_ref is None:
            continue
        if not isinstance(sizes_ref, str) or not sizes_ref:
            raise ValueError(f"{extension.path}: sizes path must be a string")
        paths.append(extension.path.parent / sizes_ref)

    merged: dict[str, dict[str, Any]] = {
        "size_codes": {},
        "size_kinds": {},
    }
    for path in paths:
        data = load_yaml(path)
        decode_size_registry(path, data)
        if not isinstance(data, dict):
            raise ValueError(f"{path}: expected mapping")
        for section, definitions in merged.items():
            additions = data.get(section, {})
            if not isinstance(additions, dict):
                raise ValueError(f"{path}: {section} must be a mapping")
            duplicates = definitions.keys() & additions.keys()
            if duplicates:
                duplicate = sorted(duplicates)[0]
                raise ValueError(f"{path}: duplicate {section} entry {duplicate!r}")
            definitions.update(additions)
    return merged


def load_field_types(
    defs_root: Path,
    extensions: dict[str, ExtensionDef] | None = None,
) -> FieldTypeRegistry:
    extensions = extensions if extensions is not None else load_extensions(defs_root)
    return build_field_type_registry(
        load_operand_types(defs_root, extensions),
        load_size_definitions(defs_root, extensions),
    )


def load_register_groups(
    defs_root: Path,
    extensions: dict[str, ExtensionDef] | None = None,
) -> dict[str, Any]:
    extensions = extensions if extensions is not None else load_extensions(defs_root)
    paths = [defs_root / "registers.yaml"]
    for extension in extensions.values():
        registers_ref = extension.data.get("registers")
        if registers_ref is None:
            continue
        if not isinstance(registers_ref, str) or not registers_ref:
            raise ValueError(f"{extension.path}: registers path must be a string")
        paths.append(extension.path.parent / registers_ref)

    groups: dict[str, Any] = {}
    for path in paths:
        data = load_yaml(path)
        decode_register_registry(path, data)
        if not isinstance(data, dict) or not isinstance(data.get("registers"), dict):
            raise ValueError(f"{path}: expected registers mapping")
        for name, group in data["registers"].items():
            if name in groups:
                raise ValueError(f"{path}: duplicate register group {name!r}")
            groups[str(name)] = group
    return groups
