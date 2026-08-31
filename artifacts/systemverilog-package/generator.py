from pathlib import Path

from artifacts._shared.systemverilog_decoder import SystemVerilogDecoderArtifactGenerator
from engine.generation import ArtifactGenerationContext, GeneratedArtifactSet


class Generator(SystemVerilogDecoderArtifactGenerator):
    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        rendered = self._render(self.project())
        return self._outputs({"package": rendered[Path("bedrock_decode_pkg.sv")]})

__all__ = ["Generator"]
