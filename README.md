# Caedral Python SDK

Official Python client for the [Caedral API](https://caedral.com). OpenAI-compatible request shapes — point your existing code at Caedral with minimal changes.

## Installation

```bash
pip install caedral
```

### Local development (editable install)

```bash
cd sdk-python
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Quickstart

```python
from caedral import Caedral

caedral = Caedral(
    api_key="cd_live_...",
    base_url="http://localhost:5001",  # local API gateway
)

completion = caedral.chat.completions.create(
    model="caedral-titan",
    messages=[{"role": "user", "content": "Hello!"}],
)

print(completion.choices[0].message["content"])
caedral.close()
```

Or use a context manager:

```python
with Caedral(api_key="cd_live_...", base_url="http://localhost:5001") as caedral:
    usage = caedral.usage.get()
    print(usage.weeklyPool.remaining)
```

Production default base URL: `https://api.caedral.com`.

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `api_key` | — | Required. Your `cd_live_...` API key |
| `base_url` | `https://api.caedral.com` | API gateway base URL |
| `max_retries` | `3` | Retries for idempotent GET requests (exponential backoff) |
| `timeout` | `120.0` | Request timeout in seconds |

## Methods

### `caedral.chat.completions.create(...)`

OpenAI-compatible chat completions.

**Non-streaming:**

```python
response = caedral.chat.completions.create(
    model="caedral-olympus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing briefly."},
    ],
    temperature=0.7,
    max_tokens=500,
)

print(response.choices[0].message["content"])
print(response.usage.total_tokens if response.usage else None)
```

**Streaming** (generator):

```python
stream = caedral.chat.completions.create(
    model="caedral-titan",
    messages=[{"role": "user", "content": "Write a haiku about code."}],
    stream=True,
)

for chunk in stream:
    delta = chunk.choices[0].delta.get("content")
    if delta:
        print(delta, end="", flush=True)
print()
```

Models: `caedral-base`, `caedral-titan`, `caedral-olympus`, `caedral-primordial`.

### `caedral.models.list()`

```python
models = caedral.models.list()
for model in models.data:
    print(model.id, model.name, model.pricing_tier)
```

### `caedral.usage.get()`

```python
usage = caedral.usage.get()
print("Pool remaining:", usage.weeklyPool.remaining)
print("Balance (cents):", usage.balanceCents)
print("Overage used:", usage.overage.usedCents)
```

### `caedral.embeddings.create(...)`

```python
result = caedral.embeddings.create(
    model="caedral-embed",
    input="Caedral unifies frontier models behind one API.",
)
print(len(result.data[0].embedding))
```

### `caedral.images.generate(...)`

```python
image = caedral.images.generate(
    model="caedral-vision",
    prompt="A minimal geometric logo on a dark background",
)
print(image.data[0].url or "b64 payload returned")
```

### `caedral.audio.generate(...)`

```python
audio = caedral.audio.generate(
    model="caedral-voice",
    input="Welcome to Caedral.",
    voice="alloy",
)
print(audio.model)
```

### `caedral.rerank.create(...)`

```python
ranked = caedral.rerank.create(
    model="caedral-rerank",
    query="billing and subscriptions",
    documents=[
        "Caedral pricing tiers include Starter and Pro.",
        "The API gateway runs on port 5001 in local dev.",
    ],
    top_n=2,
)
for item in ranked.results:
    print(item.index, item.relevance_score)
```

## Error handling

```python
from caedral import Caedral, CaedralAPIError

try:
    caedral.chat.completions.create(
        model="caedral-base",
        messages=[{"role": "user", "content": "Hi"}],
    )
except CaedralAPIError as err:
    print(err.status_code, err.type, err.message)
```

## Async client

`AsyncCaedral` is planned as a fast-follow. The synchronous client covers all endpoints today.

## Integration tests

Requires a running local gateway (`http://localhost:5001`) and `DATABASE_URL` in the repo root `.env` (tests create a temporary API key automatically).

```bash
cd sdk-python
pip install -e ".[dev]"
pytest -v
```

Optional environment variables:

| Variable | Description |
|----------|-------------|
| `CAEDRAL_BASE_URL` | Gateway URL (default `http://localhost:5001`) |
| `CAEDRAL_TEST_API_KEY` | Skip auto key creation and use an existing key |

## License

MIT
