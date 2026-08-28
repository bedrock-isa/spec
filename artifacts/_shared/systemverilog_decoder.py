"""SystemVerilog decoder artifacts generated from the current ISA model."""

from __future__ import annotations

from pathlib import Path

from engine.systemverilog.generate_decoder import render_outputs
from engine.generation import (
    ArtifactDefinition,
    ArtifactGenerationContext,
    ArtifactGenerator,
    GeneratedArtifact,
    GeneratedArtifactSet,
)


_OUTPUTS = {
    "systemverilog-package": ("bedrock_decode_pkg.sv",),
    "systemverilog-instruction-decoder": (
        "bedrock_decode_d0.sv",
        "bedrock_decode_d1.sv",
    ),
    "systemverilog-ea-decoder": ("bedrock_decode_ea.sv",),
}


class SystemVerilogDecoderArtifactGenerator(ArtifactGenerator):
    def __init__(self, definition: ArtifactDefinition) -> None:
        super().__init__(definition)
        if definition.id not in _OUTPUTS:
            raise ValueError(f"unsupported SystemVerilog decoder artifact {definition.id!r}")

    def generate(
        self, context: ArtifactGenerationContext
    ) -> GeneratedArtifactSet:
        rendered = render_outputs(Path("."))
        artifacts = tuple(
            GeneratedArtifact(
                self._declared_path(name),
                rendered[Path(name)],
            )
            for name in _OUTPUTS[self.artifact_id]
        )
        return GeneratedArtifactSet(artifacts, self.artifact_id)

    def _declared_path(self, name: str) -> Path:
        matches = [
            path for path in self.definition.declared_outputs if path.name == name
        ]
        if len(matches) != 1:
            raise ValueError(
                f"{self.definition.source}: expected one declared output named {name}"
            )
        return matches[0]
