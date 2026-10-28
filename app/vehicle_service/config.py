"""Configuration loaded from the environment.

Secrets (the API key) are NEVER hardcoded or committed — they are read from
environment variables at runtime, matching the collection's API-key auth and
the repo's security requirement. See ``.env.example`` for the variable names.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


# Environment variable names
ENV_BASE_URL = "VEHICLE_API_BASE_URL"
ENV_API_KEY = "VEHICLE_API_KEY"

# The header the API expects the key in (from the collection's apikey auth).
API_KEY_HEADER = "X-API-Key"


@dataclass
class Config:
    base_url: str
    api_key: str

    @classmethod
    def from_env(cls) -> "Config":
        base_url = os.environ.get(ENV_BASE_URL, "").strip().rstrip("/")
        api_key = os.environ.get(ENV_API_KEY, "").strip()

        if not base_url:
            raise RuntimeError(
                f"{ENV_BASE_URL} is not set. Point it at your running service, "
                "e.g. the Vehicle Service Mock (http://localhost:<port>)."
            )
        if not api_key:
            raise RuntimeError(
                f"{ENV_API_KEY} is not set. Export your API key in the environment; "
                "never hardcode it in source."
            )
        return cls(base_url=base_url, api_key=api_key)
