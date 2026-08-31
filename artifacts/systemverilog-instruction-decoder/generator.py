from pathlib import Path

from artifacts._shared.systemverilog_decoder import SystemVerilogDecoderArtifactGenerator
from engine.generation import ArtifactGenerationContext, GeneratedArtifactSet
from engine.systemverilog.generate_decoder import render_outputs


class Generator(SystemVerilogDecoderArtifactGenerator):
    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        rendered = render_outputs(Path("."))
        return self._outputs(
            {
                "d0-decoder": rendered[Path("bedrock_decode_d0.sv")],
                "d1-decoder": rendered[Path("bedrock_decode_d1.sv")],
            }
        )

__all__ = ["Generator"]
