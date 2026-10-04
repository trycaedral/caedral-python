import json
from pathlib import Path

from caedral.types import ChatCompletion, ChatCompletionCreateParams, NotreOptions

FIXTURES = Path(__file__).parent / "fixtures" / "notre-contract"


def test_notre_auto_telemetry_request_parity() -> None:
    raw = json.loads((FIXTURES / "notre-auto-telemetry.json").read_text())
    params = ChatCompletionCreateParams.model_validate(raw)
    assert params.notre == NotreOptions(mode="auto", telemetry=True)
    assert params.model_dump(exclude_none=True) == raw


def test_notre_omitted_backward_compatible() -> None:
    raw = json.loads((FIXTURES / "notre-omitted.json").read_text())
    params = ChatCompletionCreateParams.model_validate(raw)
    assert params.notre is None
    dumped = params.model_dump(exclude_none=True)
    assert "notre" not in dumped


def test_response_telemetry_metadata_v1() -> None:
    raw = json.loads((FIXTURES / "notre-response-telemetry.json").read_text())
    completion = ChatCompletion.model_validate(raw)
    assert completion.notre is not None
    assert completion.notre.enabled is True
    assert completion.notre.mode == "auto"
    assert completion.notre.intervened is False
    assert completion.notre.fallback_used is False
    # V1 base shape: no economy fields.
    assert completion.notre.input_saved is None
    assert completion.notre.result is None
    assert not hasattr(completion.notre, "logical_tokens")


def test_response_telemetry_metadata_v2_flat_economy() -> None:
    raw = json.loads((FIXTURES / "notre-response-telemetry-v2.json").read_text())
    completion = ChatCompletion.model_validate(raw)
    assert completion.notre is not None
    assert completion.notre.enabled is True
    assert completion.notre.intervened is True
    assert completion.notre.input_before == 1200
    assert completion.notre.input_sent == 310
    assert completion.notre.input_saved == 890
    assert completion.notre.result == "optimized"
    assert completion.notre.value_usd == 0.00267


def test_response_telemetry_metadata_v3_shape_fields() -> None:
    raw = json.loads((FIXTURES / "notre-response-telemetry-v3.json").read_text())
    completion = ChatCompletion.model_validate(raw)
    assert completion.notre is not None
    assert completion.notre.shape == "chat"
    assert completion.notre.contract_version == 3
    assert completion.notre.saved_breakdown is not None
    assert completion.notre.saved_breakdown.cache_hit_tokens == 640
    assert completion.notre.saved_breakdown.dedup_tokens == 20
    assert completion.notre.saved_breakdown.prefilter_tokens == 0
    assert completion.notre.input_saved == completion.notre.input_before - completion.notre.input_sent
