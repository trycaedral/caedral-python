"""Embedding contract constants for Caedral E1 Small."""

from __future__ import annotations

CANONICAL_EMBEDDING_MODEL = "caedral-embed-e1-small-v1"
LEGACY_EMBEDDING_MODEL = "caedral-embed"
DEFAULT_EMBEDDING_MODEL = CANONICAL_EMBEDDING_MODEL
DEFAULT_EMBEDDING_DIMENSIONS = 384

SUPPORTED_MODELS = frozenset({CANONICAL_EMBEDDING_MODEL, LEGACY_EMBEDDING_MODEL})
SUPPORTED_DIMENSIONS = frozenset({DEFAULT_EMBEDDING_DIMENSIONS})


class EmbeddingValidationError(ValueError):
    """Raised when embedding request parameters are invalid."""


def validate_embedding_model(model: str) -> str:
    if model not in SUPPORTED_MODELS:
        raise EmbeddingValidationError(f"unsupported embedding model: {model}")
    if model == LEGACY_EMBEDDING_MODEL:
        return CANONICAL_EMBEDDING_MODEL
    return model


def validate_embedding_dimensions(dimensions: int) -> int:
    if dimensions not in SUPPORTED_DIMENSIONS:
        raise EmbeddingValidationError(f"unsupported embedding dimensions: {dimensions}")
    return dimensions
