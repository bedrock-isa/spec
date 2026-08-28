"""Inject canonical entity anchors into registry-backed static reference tables."""

from __future__ import annotations

from collections import defaultdict

from ..entity import entity_label
from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider


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
        if location == "ea/documents/fragments/compact_ea_reference_blocks.tex":
            return self._compact_ea_modes(text, context)
        if location == (
            "ea/documents/fragments/extended_descriptor_reference_blocks.tex"
        ):
            return self._extended_ea_modes(text, context)
        return text

    @staticmethod
    def _control_registers(text: str, context: DocumentFragmentContext) -> str:
        catalog = context.project.registers
        group = catalog.references.groups.resolve("base.registers.CONTROL")
        markers: dict[str, list[str]] = defaultdict(list)
        first = next(iter(group.registers.values()))
        markers[rf"\texttt{{{first.id}}}"].append(entity_label(group.reference))
        for register in group.registers.values():
            markers[rf"\texttt{{{register.id}}}"].append(
                entity_label(register.reference)
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
            if str(group.reference) == "base.registers.CONTROL":
                continue
            registers = tuple(group.registers.values())
            if not registers:
                continue
            marker = group_markers[(group.owner, group.id)]
            markers[marker].append(entity_label(group.reference))
            markers[marker].extend(
                entity_label(register.reference) for register in registers
            )
        return _inject(text, markers, context.source)

    @staticmethod
    def _cpuid_directory(text: str, context: DocumentFragmentContext) -> str:
        catalog = context.project.cpuid
        markers: dict[str, list[str]] = defaultdict(list)
        for cpuid_class in catalog.references.classes.values():
            if cpuid_class.extends is not None:
                continue
            assert cpuid_class.value is not None
            marker = rf"\texttt{{0x{cpuid_class.value:08X}}} & --"
            markers[marker].append(entity_label(cpuid_class.reference))
        for leaf in catalog.references.leaves.values():
            if leaf.extends is not None:
                continue
            cpuid_class = catalog.references.classes.resolve(
                f"{leaf.reference.owner}.cpuid.{leaf.reference.path[-1]}"
            )
            while cpuid_class.extends is not None:
                cpuid_class = catalog.references.classes.resolve(cpuid_class.extends)
            assert cpuid_class.value is not None and leaf.value is not None
            marker = (
                rf"\texttt{{0x{cpuid_class.value:08X}}} & "
                rf"\texttt{{0x{leaf.value:04X}}}"
            )
            markers[marker].append(entity_label(leaf.reference))
        return _inject(text, markers, context.source)

    @staticmethod
    def _compact_ea_modes(text: str, context: DocumentFragmentContext) -> str:
        markers = {
            r"\textbf{\texttt{Rn Memory}}\par": [
                entity_label("base.ea.modes.compact.register")
            ],
            r"\textbf{\texttt{SP Memory}}\par": [
                entity_label("base.ea.modes.compact.stack_pointer_displaced"),
                entity_label("base.ea.modes.compact.stack_pointer_indirect"),
            ],
            r"\textbf{\texttt{PC Memory}}\par": [
                entity_label("base.ea.modes.compact.program_counter_displaced")
            ],
            r"\textbf{\texttt{Absolute Memory}}\par": [
                entity_label("base.ea.modes.compact.absolute")
            ],
            r"\textbf{\texttt{Immediate}}\par": [
                entity_label("base.ea.modes.compact.immediate")
            ],
            r"\textbf{\texttt{EXT1 Escape}}\par": [
                entity_label("base.ea.modes.compact.ext1")
            ],
            r"\textbf{\texttt{EXT2 Escape}}\par": [
                entity_label("base.ea.modes.compact.ext2")
            ],
        }
        return _inject(text, markers, context.source)

    @staticmethod
    def _extended_ea_modes(text: str, context: DocumentFragmentContext) -> str:
        markers = {
            r"\textbf{\texttt{EXT1 Explicit Segment Base}}\par": [
                entity_label("base.ea.modes.EXT1.explicit_segment_base")
            ],
            r"\textbf{\texttt{EXT2 Explicit Segment Indexed}}\par": [
                entity_label("base.ea.modes.EXT2.explicit_segment_index")
            ],
            r"\textbf{\texttt{EXT1 Explicit Segment Zero Base}}\par": [
                entity_label("base.ea.modes.EXT1.explicit_segment_zero_base")
            ],
            r"\textbf{\texttt{EXT2 Explicit Segment Base Auto-Update}}\par": [
                entity_label("base.ea.modes.EXT2.explicit_segment_base")
            ],
            r"\textbf{\texttt{EXT2 Explicit Segment Zero-Base Indexed}}\par": [
                entity_label("base.ea.modes.EXT2.explicit_segment_zero_base_index")
            ],
            r"\textbf{\texttt{EXT2 SP/PC Indexed}}\par": [
                entity_label("base.ea.modes.EXT2.stack_pointer_index"),
                entity_label("base.ea.modes.EXT2.program_counter_index"),
            ],
            r"\textbf{\texttt{EXT1 Default-Segment Base Auto-Update}}\par": [
                entity_label("base.ea.modes.EXT1.default_segment_base")
            ],
        }
        return _inject(text, markers, context.source)


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
