from __future__ import annotations

import os
import secrets
import uuid
from dataclasses import dataclass
from pathlib import Path

import bcrypt
import psycopg


def _load_root_env() -> None:
    root = Path(__file__).resolve().parents[2]
    env_path = root / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("#") or "=" not in trimmed:
            continue
        key, value = trimmed.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_root_env()

API_KEY_PREFIX = "cd_live_"


def generate_api_key_secret() -> str:
    body = secrets.token_urlsafe(24)
    return f"{API_KEY_PREFIX}{body}"


@dataclass
class TestKeyFixture:
    user_id: str
    api_key_id: str
    raw_key: str
    conn: psycopg.Connection

    def cleanup(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute('DELETE FROM usage_logs WHERE user_id = %s', (self.user_id,))
            cur.execute('DELETE FROM api_keys WHERE id = %s', (self.api_key_id,))
            cur.execute('DELETE FROM subscriptions WHERE user_id = %s', (self.user_id,))
            cur.execute('DELETE FROM "user" WHERE id = %s', (self.user_id,))
        self.conn.commit()
        self.conn.close()


def create_test_api_key() -> TestKeyFixture:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required to create a test API key")

    user_id = str(uuid.uuid4())
    api_key_id = str(uuid.uuid4())
    sub_id = str(uuid.uuid4())
    raw_key = generate_api_key_secret()
    key_prefix = raw_key[:16]
    key_hash = bcrypt.hashpw(raw_key.encode(), bcrypt.gensalt(rounds=10)).decode()
    email = f"sdk-python-test-{user_id}@example.com"

    conn = psycopg.connect(database_url, autocommit=False)
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO "user" (id, name, email, email_verified, balance_cents, account_status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, "SDK Python Test", email, True, 0, "active"),
        )
        cur.execute(
            """
            INSERT INTO subscriptions (
              id, user_id, plan, status, weekly_pool_limit, weekly_pool_used,
              overage_enabled, overage_used_cents
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (sub_id, user_id, "pro", "active", 1_000_000, 0, False, 0),
        )
        cur.execute(
            """
            INSERT INTO api_keys (id, user_id, name, key_prefix, key_hash)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (api_key_id, user_id, "SDK Python test key", key_prefix, key_hash),
        )
    conn.commit()

    return TestKeyFixture(
        user_id=user_id,
        api_key_id=api_key_id,
        raw_key=raw_key,
        conn=conn,
    )
