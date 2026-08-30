"""Inject canonical entity anchors into registry-backed static reference tables."""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from ..reference import Reference
from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider

if TYPE_CHECKING:
    from ..register import RegisterGroup


_CONTROL_REGISTER_GROUP: Reference["RegisterGroup"] = Reference(
    "base", ("registers",), "CONTROL"
)


class RegistryAnchorRenderer(DocumentFragmentProvider):
    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset()

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        if context.source is None:
            return text
        source = context.source.resolve()
        isa_root = context.project.root.resolve()
        if not source.is_relative_to(isa_root):
            return text
        relative = source.relative_to(isa_root)
        location = str(relative)
        if location == "registers/documents/fragments/control_register_selectors.tex":
            return self._control_registers(text, context)
        if location == "indexes/documents/fragments/architectural_state_index.tex":
            return self._architectural_registers(text, context)
        if location == "cpuid/documents/fragments/cpuid_class_leaf_directory.tex":
            return self._cpuid_directory(text, context)
        if (
            len(relative.parts) >= 6
            and relative.parts[0] == "extensions"
            and relative.parts[2:5] == ("documents", "topics", "cpuid")
        ):
            return self._extension_cpuid_topic(text, context, relative.parts[1])
        return text

    @staticmethod
    def _control_registers(text: str, context: DocumentFragmentContext) -> str:
        catalog = context.project.registers
        group = catalog.references.groups.resolve(_CONTROL_REGISTER_GROUP)
        markers: dict[str, list[str]] = defaultdict(list)
        first = next(iter(group.registers.values()))
        markers[rf"\texttt{{{first.id}}}"].append(
            _label(context.project, group.reference)
        )
        for register in group.registers.values():
            markers[rf"\texttt{{{register.id}}}"].append(
                _label(context.project, register.reference)
            )
        return _inject(text, markers, context.source)

    @staticmethod
    def _architectural_registers(
        text: str, context: DocumentFragmentContext
    ) -> str:
        markers: dict[str, list[str]] = defaultdict(list)
        group_markers = {
            ("base", "GPR"): r"\texttt{R0{-}{-}R15}",
            ("base", "SPECIAL"): r"\hyperref[section:register-model]{\texttt{SP}}",
            ("base", "SEGMENT"): r"\hyperref[section:segment-registers]{\texttt{CS},",
            ("base", "STATE"): r"\hyperref[section:state-register-formats]{\texttt{FLAGS},",
            ("base", "PERFORMANCE"): r"\hyperref[section:performance-counter-discovery]{\texttt{CYCLE},",
            ("FP", "FPR"): r"\texttt{F0{-}{-}F15}",
            ("FP", "STATE"): r"\hyperref[section:state-register-formats]{\texttt{FFLAGS},",
            ("VECTOR", "VECTOR"): r"\hyperref[section:vector-register-model]{\texttt{V0},",
            ("VECTOR", "PREDICATE"): r"\hyperref[section:vector-register-model]{\texttt{P0},",
        }
        for group in context.project.registers.references.groups.values():
            if group.owner == "base" and group.id == "CONTROL":
                continue
            registers = tuple(group.registers.values())
            if not registers:
                continue
            marker = group_markers[(group.owner, group.id)]
            markers[marker].append(_label(context.project, group.reference))
            markers[marker].extend(
                _label(context.project, register.reference) for register in registers
            )
        return _inject(text, markers, context.source)

    @staticmethod
    def _cpuid_directory(text: str, context: DocumentFragmentContext) -> str:
        catalog = context.project.cpuid
        markers: dict[str, list[str]] = defaultdict(list)
        base = catalog.namespaces["base"]
        for cpuid_class in base.classes.values():
            if cpuid_class.extends is not None:
                continue
            assert cpuid_class.value is not None
            marker = rf"\texttt{{0x{cpuid_class.value:08X}}} & --"
            markers[marker].append(_label(context.project, cpuid_class.reference))
        for cpuid_class in base.classes.values():
            root_class = cpuid_class
            while root_class.extends is not None:
                root_class = catalog.references.classes.resolve(root_class.extends)
            for leaf in cpuid_class.leaves.values():
                if leaf.extends is not None:
                    continue
                assert root_class.value is not None and leaf.value is not None
                marker = (
                    rf"\texttt{{0x{root_class.value:08X}}} & "
                    rf"\texttt{{0x{leaf.value:04X}}}"
                )
                markers[marker].append(_label(context.project, leaf.reference))
        return _inject(text, markers, context.source)

    @staticmethod
    def _extension_cpuid_topic(
        text: str, context: DocumentFragmentContext, owner: str
    ) -> str:
        catalog = context.project.cpuid
        namespace = catalog.namespaces[owner]
        labels: list[str] = []
        labels.extend(
            _label(context.project, cpuid_class.reference)
            for cpuid_class in namespace.classes.values()
            if cpuid_class.extends is None
        )
        labels.extend(
            _label(context.project, leaf.reference)
            for cpuid_class in namespace.classes.values()
            for leaf in cpuid_class.leaves.values()
            if leaf.extends is None
        )
        if not labels:
            return text
        heading_end = text.find("\n")
        if heading_end < 0:
            raise ValueError(f"{context.source}: CPUID topic has no heading line")
        anchors = "".join(
            rf"\phantomsection\label{{{label}}}" for label in labels
        )
        return text[: heading_end + 1] + anchors + "\n" + text[heading_end + 1 :]

def _inject(text: str, markers: dict[str, list[str]], source) -> str:
    for marker, labels in markers.items():
        count = text.count(marker)
        if count != 1:
            raise ValueError(
                f"{source}: entity anchor marker {marker!r} occurs {count} times"
            )
        anchors = "".join(
            rf"\phantomsection\label{{{label}}}" for label in labels
        )
        text = text.replace(marker, anchors + marker, 1)
    return text


def _label(project, reference) -> str:
    label = project.entities.resolve(reference).latex_label
    if label is None:
        raise ValueError("entity has no target in this LaTeX artifact")
    return label
