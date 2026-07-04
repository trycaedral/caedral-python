"""Quickstart smoke test — run against local gateway."""

from caedral import Caedral
import os
import sys


def main() -> int:
    api_key = os.environ.get("CAEDRAL_TEST_API_KEY") or os.environ.get("CAEDRAL_API_KEY")
    if not api_key:
        print("Set CAEDRAL_TEST_API_KEY or CAEDRAL_API_KEY", file=sys.stderr)
        return 1

    base_url = os.environ.get("CAEDRAL_BASE_URL", "http://localhost:5001")

    with Caedral(api_key=api_key, base_url=base_url) as client:
        models = client.models.list()
        print(f"Models: {[m.id for m in models.data]}")

        completion = client.chat.completions.create(
            model="caedral-base",
            messages=[{"role": "user", "content": "Say hello in one short sentence."}],
        )
        content = completion.choices[0].message.get("content", "")
        print(f"Assistant: {content}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
