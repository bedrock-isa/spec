"""Domain-neutral generated artifact contracts, registry, and output."""

from .artifact import (
    ArtifactDefinition,
    ArtifactGenerationContext,
    ArtifactGenerator,
    ArtifactGeneratorRegistry,
    GeneratedArtifact,
    GeneratedArtifactSet,
    PlannedArtifactGenerator,
)
from .authored_tex import AuthoredTexArtifactGenerator
from .writer import ArtifactWriter

__all__ = [
    "ArtifactDefinition",
    "ArtifactGenerationContext",
    "ArtifactGenerator",
    "ArtifactGeneratorRegistry",
    "AuthoredTexArtifactGenerator",
    "ArtifactWriter",
    "GeneratedArtifact",
    "GeneratedArtifactSet",
    "PlannedArtifactGenerator",
]
