# Changelog

## 2.0.0 — 2026-08-04

### Breaking

- Embeddings default to `caedral-embed-e1-small-v1` with 384 dimensions (E1 Small)
- Legacy `caedral-embed` and non-384 dimension requests are rejected client-side

## 1.0.0 — 2026-07-29

First stable release of the official Caedral Python SDK.

- Typed client for chat, embeddings, images, audio, and rerank
- httpx + pydantic v2 stack
- Production/Stable classifier on PyPI
