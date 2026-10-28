"""Demo app that exercises the full Vehicle Service lifecycle using the client.

Run it against your running service (or the Vehicle Service Mock):

    export VEHICLE_API_BASE_URL="http://localhost:<mock-port>"
    export VEHICLE_API_KEY="<your-api-key>"
    python -m app.main

It walks the CRUD lifecycle defined by the collection:
create -> list -> retrieve -> update -> delete, printing each step.
"""

from __future__ import annotations

import sys

from vehicle_service import (
    VehicleServiceClient,
    Vehicle,
    VehicleServiceError,
    NotFoundError,
)


def run() -> int:
    try:
        client = VehicleServiceClient()  # reads base URL + API key from env
    except RuntimeError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    with client:
        print("1) Listing existing vehicles...")
        vehicles = client.list_vehicles()
        print(f"   Found {len(vehicles)} vehicle(s).")

        print("\n2) Creating a new vehicle...")
        new_vehicle = Vehicle(
            nickName="The Lisa Marie",
            vin="4M2DV11W4RDJ53329",
            make="Mercury",
            model="Villager",
            year="1994",
            miles=159864,
        )
        try:
            created = client.create_vehicle(new_vehicle)
            print(f"   Created vehicle id={created.id} ({created.nickName}).")
            vehicle_id = created.id
        except VehicleServiceError as exc:
            print(f"   Create failed: {exc}")
            return 1

        print("\n3) Retrieving the vehicle...")
        fetched = client.get_vehicle(vehicle_id)
        print(f"   {fetched.to_dict()}")

        print("\n4) Updating the odometer...")
        updated = client.update_vehicle(vehicle_id, {"miles": 160000})
        print(f"   miles is now {updated.miles}.")

        print("\n5) Deleting the vehicle...")
        client.delete_vehicle(vehicle_id)
        print("   Deleted.")

        print("\n6) Confirming deletion...")
        try:
            client.get_vehicle(vehicle_id)
            print("   Vehicle still present (unexpected).")
        except NotFoundError:
            print("   Vehicle no longer exists (404 as expected).")

    print("\nLifecycle complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
