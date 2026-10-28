"""requests-based client for the Vehicle Service API.

Hand-written stand-in for a generated SDK. Each method maps 1:1 to a request
in the "Vehicle Service Collection":

    GET    /vehicles          -> list_vehicles()
    GET    /vehicles/:id       -> get_vehicle(vehicle_id)
    POST   /vehicles          -> create_vehicle(vehicle)
    PATCH  /vehicles/:id       -> update_vehicle(vehicle_id, changes)
    DELETE /vehicles/:id       -> delete_vehicle(vehicle_id)

Auth is an API key sent in the ``X-API-Key`` header. Non-2xx responses raise a
typed exception from ``vehicle_service.exceptions``.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

import requests

from .config import Config, API_KEY_HEADER
from .exceptions import error_for_status, VehicleServiceError
from .models import Vehicle


class VehicleServiceClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 10.0,
        session: Optional[requests.Session] = None,
    ) -> None:
        if base_url is None or api_key is None:
            cfg = Config.from_env()
            base_url = base_url or cfg.base_url
            api_key = api_key or cfg.api_key

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = session or requests.Session()
        self._session.headers.update(
            {
                API_KEY_HEADER: api_key,
                "Accept": "application/json",
            }
        )

    # -- internal helpers ---------------------------------------------------

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _request(self, method: str, path: str, json_body: Any = None) -> requests.Response:
        try:
            response = self._session.request(
                method=method,
                url=self._url(path),
                json=json_body,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise VehicleServiceError(f"Network error calling {method} {path}: {exc}") from exc

        if response.status_code >= 400:
            self._raise_for_response(response)
        return response

    @staticmethod
    def _raise_for_response(response: requests.Response) -> None:
        try:
            payload = response.json()
            message = payload.get("message") or payload.get("error") or response.reason
        except ValueError:
            payload = response.text
            message = response.reason or "Request failed"
        raise error_for_status(response.status_code, message, payload=payload)

    @staticmethod
    def _parse(response: requests.Response) -> Any:
        if response.status_code == 204 or not response.content:
            return None
        try:
            return response.json()
        except ValueError:
            return response.text

    # -- endpoints ----------------------------------------------------------

    def list_vehicles(self) -> List[Vehicle]:
        """GET /vehicles — list all vehicles (200)."""
        data = self._parse(self._request("GET", "/vehicles"))
        return [Vehicle.from_dict(item) for item in (data or [])]

    def get_vehicle(self, vehicle_id: Union[int, str]) -> Vehicle:
        """GET /vehicles/:id — fetch one vehicle (200, 404)."""
        data = self._parse(self._request("GET", f"/vehicles/{vehicle_id}"))
        return Vehicle.from_dict(data)

    def create_vehicle(self, vehicle: Union[Vehicle, Dict[str, Any]]) -> Vehicle:
        """POST /vehicles — register a new vehicle (201, 400, 409)."""
        body = vehicle.to_create_payload() if isinstance(vehicle, Vehicle) else dict(vehicle)
        data = self._parse(self._request("POST", "/vehicles", json_body=body))
        return Vehicle.from_dict(data)

    def update_vehicle(
        self, vehicle_id: Union[int, str], changes: Dict[str, Any]
    ) -> Vehicle:
        """PATCH /vehicles/:id — modify a vehicle's attributes (200, 400)."""
        data = self._parse(
            self._request("PATCH", f"/vehicles/{vehicle_id}", json_body=changes)
        )
        return Vehicle.from_dict(data)

    def delete_vehicle(self, vehicle_id: Union[int, str]) -> None:
        """DELETE /vehicles/:id — remove a vehicle (204)."""
        self._request("DELETE", f"/vehicles/{vehicle_id}")

    # -- context manager sugar ---------------------------------------------

    def __enter__(self) -> "VehicleServiceClient":
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.close()

    def close(self) -> None:
        self._session.close()
