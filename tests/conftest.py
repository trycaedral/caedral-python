from __future__ import annotations

import os

import pytest

from caedral import Caedral
from tests.helpers import TestKeyFixture, create_test_api_key

BASE_URL = os.environ.get("CAEDRAL_BASE_URL", "http://localhost:5001")


@pytest.fixture(scope="module")
def api_key() -> str:
    if os.environ.get("CAEDRAL_TEST_API_KEY"):
        return os.environ["CAEDRAL_TEST_API_KEY"]
    fixture = create_test_api_key()
    yield fixture.raw_key
    fixture.cleanup()


@pytest.fixture(scope="module")
def client(api_key: str) -> Caedral:
    caedral = Caedral(api_key=api_key, base_url=BASE_URL)
    yield caedral
    caedral.close()
