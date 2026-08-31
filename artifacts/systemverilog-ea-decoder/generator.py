from pathlib import Path

from artifacts._shared.systemverilog_decoder import SystemVerilogDecoderArtifactGenerator
from engine.generation import ArtifactGenerationContext, GeneratedArtifactSet


class Generator(SystemVerilogDecoderArtifactGenerator):
    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        rendered = self._render(self.project())
        return self._outputs({"decoder": rendered[Path("bedrock_decode_ea.sv")]})

__all__ = ["Generator"]
