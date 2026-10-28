"""Data models for the Vehicle Service API.

The ``Vehicle`` shape mirrors the request/response bodies documented in the
Postman collection examples:

    {
      "id": 1,
      "nickName": "The Lisa Marie",
      "vin": "4M2DV11W4RDJ53329",
      "make": "Mercury",
      "model": "Villager",
      "year": "1994",
      "miles": 159864
    }
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class Vehicle:
    """A vehicle resource."""

    nickName: str
    vin: str
    make: str
    model: str
    year: str
    miles: int
    id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vehicle":
        """Build a Vehicle from an API response body, ignoring unknown keys."""
        return cls(
            id=data.get("id"),
            nickName=data.get("nickName"),
            vin=data.get("vin"),
            make=data.get("make"),
            model=data.get("model"),
            year=data.get("year"),
            miles=data.get("miles"),
        )

    def to_create_payload(self) -> Dict[str, Any]:
        """Serialize for POST /vehicles (the server assigns the id)."""
        payload = asdict(self)
        payload.pop("id", None)
        return payload

    def to_dict(self) -> Dict[str, Any]:
        """Serialize including the id (used for PATCH payloads / display)."""
        return {k: v for k, v in asdict(self).items() if v is not None}
