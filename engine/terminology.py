"""Distributed terminology groups and renderer-independent definitions."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
import re
from types import MappingProxyType

from .extension import ExtensionSetCatalog
from .reference import Reference, ReferenceIndex
from .semantic_text import SemanticText, TermForm, TextOrigin
from .yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader


@dataclass(frozen=True, slots=True)
class TerminologyInventory:
    """One closed-world terminology group or term directory inventory."""

    owner: str
    kind: str
    source: Path
    root: Path
    declared: tuple[str, ...]
    actual: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TermForms:
    canonical: str
    plural: str | None = None
    adjective: str | None = None

    def supports(self, form: TermForm, abbreviation: "TermAbbreviation | None") -> bool:
        if form is TermForm.CANONICAL:
            return True
        if form is TermForm.PLURAL:
            return self.plural is not None
        if form is TermForm.ADJECTIVE:
            return self.adjective is not None
        return abbreviation is not None


@dataclass(frozen=True, slots=True)
class TermAbbreviation:
    canonical: str


@dataclass(frozen=True, slots=True)
class TermRelations:
    broader: tuple[Reference, ...] = ()
    related: tuple[Reference, ...] = ()


@dataclass(frozen=True, slots=True)
class Term:
    """One canonical terminology entry owned by a terminology group."""

    reference: Reference
    group: Reference
    source: Path
    root: Path
    owner: str
    id: str
    forms: TermForms
    abbreviation: TermAbbreviation | None
    article: str | None
    definition: SemanticText
    variants: Mapping[str, str]
    relations: TermRelations


@dataclass(frozen=True, slots=True)
class TermGroup:
    """A semantic group rendered as a subsection by the current manual."""

    reference: Reference
    source: Path
    root: Path
    owner: str
    id: str
    title: str
    term_inventory: TerminologyInventory
    terms: Mapping[str, Term]


@dataclass(frozen=True, slots=True)
class TerminologyNamespace:
    owner: str
    root: Path
    group_inventory: TerminologyInventory
    groups: Mapping[str, TermGroup]


@dataclass(frozen=True, slots=True)
class TermReferenceIndexes:
    groups: ReferenceIndex[TermGroup]
    terms: ReferenceIndex[Term]


@dataclass(frozen=True, slots=True)
class TermSpelling:
    reference: Reference
    form: str
    value: str


@dataclass(frozen=True, slots=True)
class TermCatalog:
    """The union of base and extension-owned terminology namespaces."""

    namespaces: Mapping[str, TerminologyNamespace]
    references: TermReferenceIndexes
    spellings: Mapping[str, tuple[TermSpelling, ...]]

    @classmethod
    def load(
        cls,
        isa_root: str | Path,
        extension_catalog: ExtensionSetCatalog | None = None,
    ) -> "TermCatalog":
        root = Path(isa_root).resolve()
        extensions = extension_catalog or ExtensionSetCatalog.load(root)
        schemas = {
            "group": root / "schemas/terminology-group.yaml",
            "term": root / "schemas/term.yaml",
        }
        references = TermReferenceIndexes(
            ReferenceIndex[TermGroup](), ReferenceIndex[Term]()
        )
        namespaces: dict[str, TerminologyNamespace] = {}
        for owner, namespace_root in (
            ("base", root),
            *((item, extensions.root / item) for item in extensions.declared),
        ):
            namespaces[owner] = _load_namespace(
                owner, namespace_root, schemas, references
            )
        spellings: dict[str, list[TermSpelling]] = {}
        for term in references.terms.values():
            for spelling in _term_spellings(term):
                spellings.setdefault(_normalize_spelling(spelling.value), []).append(
                    spelling
                )
        return cls(
            MappingProxyType(namespaces),
            references,
            MappingProxyType(
                {key: tuple(values) for key, values in spellings.items()}
            ),
        )

    @property
    def base(self) -> TerminologyNamespace:
        return self.namespaces["base"]

    def namespace(self, owner: str) -> TerminologyNamespace:
        try:
            return self.namespaces[owner]
        except KeyError as error:
            raise ValueError(f"unknown terminology namespace {owner!r}") from error


def _load_namespace(
    owner: str,
    namespace_root: Path,
    schemas: Mapping[str, Path],
    references: TermReferenceIndexes,
) -> TerminologyNamespace:
    groups_root = namespace_root / "terminology/groups"
    inventory = _load_inventory(owner, "group", groups_root, "groups")
    groups: dict[str, TermGroup] = {}
    for group_id in inventory.declared:
        group_root = groups_root / group_id
        if group_id in groups or not group_root.is_dir():
            continue
        group = _load_group(owner, group_root, schemas, references)
        references.groups.register(group.reference, group)
        groups[group_id] = group
    return TerminologyNamespace(
        owner, namespace_root, inventory, MappingProxyType(groups)
    )


def _load_group(
    owner: str,
    root: Path,
    schemas: Mapping[str, Path],
    references: TermReferenceIndexes,
) -> TermGroup:
    source = root / "group.yaml"
    raw = SchemaValidatedYamlLoader().load(source, schemas["group"])
    group_id = raw["id"]
    if group_id != root.name:
        raise ValueError(
            f"{source}: terminology group ID {group_id!r} does not match "
            f"directory {root.name!r}"
        )
    group_reference = Reference(owner, ("term_groups",), group_id)
    terms_root = root / "terms"
    inventory = _load_inventory(owner, "term", terms_root, "terms")
    terms: dict[str, Term] = {}
    for term_id in inventory.declared:
        term_root = terms_root / term_id
        if term_id in terms or not term_root.is_dir():
            continue
        term = _load_term(owner, group_reference, term_root, schemas["term"])
        references.terms.register(term.reference, term)
        terms[term_id] = term
    return TermGroup(
        group_reference,
        source,
        root,
        owner,
        group_id,
        raw["title"],
        inventory,
        MappingProxyType(terms),
    )


def _load_term(owner: str, group: Reference, root: Path, schema: Path) -> Term:
    source = root / "term.yaml"
    raw = SchemaValidatedYamlLoader().load(source, schema)
    term_id = raw["id"]
    if term_id != root.name:
        raise ValueError(
            f"{source}: term ID {term_id!r} does not match directory {root.name!r}"
        )
    display = raw["display"]
    abbreviation = raw.get("abbreviation")
    relations = raw.get("relations", {})
    return Term(
        reference=Reference(owner, ("terms",), term_id),
        group=group,
        source=source,
        root=root,
        owner=owner,
        id=term_id,
        forms=TermForms(
            display["canonical"], display.get("plural"), display.get("adjective")
        ),
        abbreviation=(
            TermAbbreviation(abbreviation["canonical"])
            if abbreviation is not None
            else None
        ),
        article=raw.get("article"),
        definition=SemanticText.parse(
            raw["definition"], origin=TextOrigin(source, ("definition",))
        ),
        variants=MappingProxyType(dict(raw.get("variants", {}))),
        relations=TermRelations(
            tuple(Reference.parse(item) for item in relations.get("broader", ())),
            tuple(Reference.parse(item) for item in relations.get("related", ())),
        ),
    )


def _load_inventory(
    owner: str, kind: str, root: Path, key: str
) -> TerminologyInventory:
    source = root / f"{key}.yaml"
    declared = _load_name_list(source, key) if source.is_file() else ()
    actual = (
        tuple(
            sorted(
                path.name
                for path in root.iterdir()
                if path.is_dir() and not path.name.startswith(".")
            )
        )
        if root.is_dir()
        else ()
    )
    return TerminologyInventory(owner, kind, source, root, declared, actual)


def _load_name_list(path: Path, key: str) -> tuple[str, ...]:
    document = YamlDocumentLoader().mapping(path)
    values = document.get(key)
    if not isinstance(values, list) or any(
        not isinstance(value, str) for value in values
    ):
        raise ValueError(f"{path}: expected a {key} list of strings")
    return tuple(values)


def _term_spellings(term: Term) -> tuple[TermSpelling, ...]:
    values = [TermSpelling(term.reference, "canonical", term.forms.canonical)]
    for name, value in (
        ("plural", term.forms.plural),
        ("adjective", term.forms.adjective),
    ):
        if value is not None:
            values.append(TermSpelling(term.reference, name, value))
    if term.abbreviation is not None:
        values.append(
            TermSpelling(term.reference, "short", term.abbreviation.canonical)
        )
    values.extend(
        TermSpelling(term.reference, f"variant:{name}", value)
        for name, value in term.variants.items()
    )
    return tuple(values)


def _normalize_spelling(value: str) -> str:
    return re.sub(r"[\s-]+", " ", value.casefold()).strip()
