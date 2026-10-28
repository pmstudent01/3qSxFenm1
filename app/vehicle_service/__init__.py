"""Vehicle Service — a hand-written, requests-based Python client for the Vehicle Service API.

This package is a lightweight SDK replacement generated directly from the
"Vehicle Service Collection" Postman contract. It exposes a typed client,
simple data models, and typed exceptions for every endpoint in the collection.
"""

from .client import VehicleServiceClient
from .models import Vehicle
from .exceptions import (
    VehicleServiceError,
    BadRequestError,
    UnauthorizedError,
    NotFoundError,
    ConflictError,
    ServerError,
)

__all__ = [
    "VehicleServiceClient",
    "Vehicle",
    "VehicleServiceError",
    "BadRequestError",
    "UnauthorizedError",
    "NotFoundError",
    "ConflictError",
    "ServerError",
]

__version__ = "0.1.0"
