"""SystemVerilog decoder artifacts generated from the current ISA model."""

from __future__ import annotations

from engine.generation import (
    ArtifactGenerator,
    GeneratedArtifact,
    GeneratedArtifactSet,
)


class SystemVerilogDecoderArtifactGenerator(ArtifactGenerator):
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
