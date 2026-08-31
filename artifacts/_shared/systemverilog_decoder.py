"""SystemVerilog decoder artifacts generated from the current ISA model."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from engine.generation import (
    ArtifactGenerator,
    GeneratedArtifact,
    GeneratedArtifactSet,
)
from engine.systemverilog import decoder_ir, lowering


@dataclass(frozen=True)
class DecoderPortProjection:
    name: str
    direction: str
    type_name: str


@dataclass(frozen=True)
class D1OverlapProjection:
    form_key: str
    left_operand: int
    right_operand: int
    rule: str


@dataclass(frozen=True)
class DecoderProjection:
    limits: decoder_ir.DerivedLimitsIR
    d0_ports: tuple[DecoderPortProjection, ...]
    d1_ports: tuple[DecoderPortProjection, ...]
    d1_overlaps: tuple[D1OverlapProjection, ...]
    source_ir: decoder_ir.DecodeIR = field(repr=False, compare=False)

    @classmethod
    def create(cls, source_ir: decoder_ir.DecodeIR) -> DecoderProjection:
        overlaps = []
        for form in source_ir.forms:
            operand_slots = {
                operand.name: index for index, operand in enumerate(form.operands)
            }
            overlaps.extend(
                D1OverlapProjection(
                    form.key,
                    operand_slots[overlap.left],
                    operand_slots[overlap.right],
                    overlap.rule,
                )
                for overlap in form.overlaps
            )
        return cls(
            limits=source_ir.limits,
            d0_ports=(
                DecoderPortProjection("valid_i", "input", "logic"),
                DecoderPortProjection("opcode_class_i", "input", "opcode_class_e"),
                DecoderPortProjection(
                    "opcode_i", "input", "logic [BEDROCK_OPCODE_BITS-1:0]"
                ),
                DecoderPortProjection("result_o", "output", "d0_result_t"),
                DecoderPortProjection("ea_result_o", "output", "d0_ea_result_t"),
            ),
            d1_ports=(
                DecoderPortProjection("d0_i", "input", "d0_result_t"),
                DecoderPortProjection(
                    "record_i",
                    "input",
                    "logic [BEDROCK_RECORD_BYTES*8-1:0]",
                ),
                DecoderPortProjection("byte_count_i", "input", "logic [4:0]"),
                DecoderPortProjection("result_o", "output", "d1_opcode_result_t"),
            ),
            d1_overlaps=tuple(overlaps),
            source_ir=source_ir,
        )


class SystemVerilogDecoderArtifactGenerator(ArtifactGenerator):
    def project(self) -> DecoderProjection:
        return DecoderProjection.create(decoder_ir.load_decode_ir())

    def _render(self, projection: DecoderProjection) -> dict[Path, str]:
        outputs = lowering.lower(projection.source_ir)
        return {
            Path("bedrock_decode_pkg.sv"): outputs.package,
            Path("bedrock_decode_d0.sv"): outputs.d0,
            Path("bedrock_decode_d1.sv"): outputs.d1,
            Path("bedrock_decode_ea.sv"): outputs.ea,
        }

    def _outputs(self, contents: dict[str, str]) -> GeneratedArtifactSet:
        declared = self.definition.outputs
        if set(declared) != set(contents):
            raise ValueError(
                f"{self.definition.source}: declared output roles {sorted(declared)} do not "
                f"match rendered output roles {sorted(contents)}"
            )
        return GeneratedArtifactSet(
            tuple(
                GeneratedArtifact(declared[role], content)
                for role, content in contents.items()
            ),
            self.artifact_id,
        )
