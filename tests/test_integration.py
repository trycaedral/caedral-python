from __future__ import annotations

import pytest

from caedral import Caedral, CaedralAPIError


def test_lists_models(client: Caedral) -> None:
    models = client.models.list()

    assert models.object == "list"
    assert len(models.data) >= 4
    model_ids = {model.id for model in models.data}
    assert {
        "caedral-base",
        "caedral-titan",
        "caedral-olympus",
        "caedral-primordial",
    }.issubset(model_ids)
    first = models.data[0]
    assert first.object == "model"
    assert first.owned_by == "caedral"
    assert first.context_window > 0
    assert first.pricing_tier


def test_chat_completion(client: Caedral) -> None:
    completion = client.chat.completions.create(
        model="caedral-base",
        messages=[{"role": "user", "content": "Reply with exactly: PYTHON SDK OK"}],
    )

    assert completion.object == "chat.completion"
    assert completion.model == "caedral-base"
    assert completion.choices[0].message.get("content")


def test_chat_streaming(client: Caedral) -> None:
    stream = client.chat.completions.create(
        model="caedral-base",
        messages=[{"role": "user", "content": "Count to 3."}],
        stream=True,
    )

    chunks: list[str] = []
    for chunk in stream:
        assert chunk.object == "chat.completion.chunk"
        delta = chunk.choices[0].delta.get("content")
        if delta:
            chunks.append(delta)

    assert len("".join(chunks)) > 0


def test_usage_get(client: Caedral) -> None:
    usage = client.usage.get()

    assert isinstance(usage.accountStatus, str)
    assert isinstance(usage.plan, str)
    assert isinstance(usage.planStatus, str)
    assert isinstance(usage.balanceCents, int)
    assert usage.weeklyPool.limit >= 0
    assert usage.weeklyPool.used >= 0
    assert usage.weeklyPool.remaining >= 0
    assert isinstance(usage.overage.enabled, bool)
    assert isinstance(usage.overage.usedCents, int)
    assert isinstance(usage.balanceWeightedUnitsAffordable, int)


def test_invalid_api_key() -> None:
    bad_client = Caedral(
        api_key="cd_live_invalid_integration_test_key",
        base_url="http://localhost:5001",
    )
    try:
        with pytest.raises(CaedralAPIError) as exc_info:
            bad_client.chat.completions.create(
                model="caedral-base",
                messages=[{"role": "user", "content": "Hello"}],
            )
        err = exc_info.value
        assert err.type == "invalid_api_key"
        assert err.status_code == 401

        with pytest.raises(CaedralAPIError) as usage_exc:
            bad_client.usage.get()
        assert usage_exc.value.type == "invalid_api_key"
        assert usage_exc.value.status_code == 401
    finally:
        bad_client.close()
