"""Typed exceptions for the Vehicle Service client.

These map directly to the response codes documented in the Postman collection:
400, 401, 404, 409, 500. Every client call raises one of these on a
non-2xx response so callers can branch on the specific failure mode.
"""

from __future__ import annotations

from typing import Any, Optional


class VehicleServiceError(Exception):
    """Base error for all Vehicle Service client failures."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        payload: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        if self.status_code is not None:
            return f"[{self.status_code}] {self.message}"
        return self.message


class BadRequestError(VehicleServiceError):
    """400 - Missing or invalid request attribute."""


class UnauthorizedError(VehicleServiceError):
    """401 - Missing or invalid API key."""


class NotFoundError(VehicleServiceError):
    """404 - Vehicle ID does not exist."""


class ConflictError(VehicleServiceError):
    """409 - A vehicle with the same VIN already exists."""


class ServerError(VehicleServiceError):
    """500 - Unexpected server-side failure."""


def error_for_status(status_code: int, message: str, payload: Any = None) -> VehicleServiceError:
    """Return the most specific exception class for an HTTP status code."""
    mapping = {
        400: BadRequestError,
        401: UnauthorizedError,
        404: NotFoundError,
        409: ConflictError,
        500: ServerError,
    }
    error_cls = mapping.get(status_code, VehicleServiceError)
    return error_cls(message, status_code=status_code, payload=payload)
