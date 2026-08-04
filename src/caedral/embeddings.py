"""Embedding contract constants for Caedral E1 Small."""

from __future__ import annotations

DEFAULT_EMBEDDING_MODEL = "caedral-embed-e1-small-v1"
DEFAULT_EMBEDDING_DIMENSIONS = 384

SUPPORTED_MODELS = frozenset({DEFAULT_EMBEDDING_MODEL})
SUPPORTED_DIMENSIONS = frozenset({DEFAULT_EMBEDDING_DIMENSIONS})


class EmbeddingValidationError(ValueError):
    """Raised when embedding request parameters are invalid."""


def validate_embedding_model(model: str) -> str:
    if model not in SUPPORTED_MODELS:
        raise EmbeddingValidationError(f"unsupported embedding model: {model}")
    return model


def validate_embedding_dimensions(dimensions: int) -> int:
    if dimensions not in SUPPORTED_DIMENSIONS:
        raise EmbeddingValidationError(f"unsupported embedding dimensions: {dimensions}")
    return dimensions
