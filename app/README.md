# Vehicle Service — Python App

A Python implementation of the Vehicle Service API client, generated directly
from the **Vehicle Service Collection** Postman contract (the SDK-generation
service was unavailable, so this is a hand-written `requests`-based client that
serves the same purpose).

## Structure

```
app/
├── vehicle_service/        # the hand-written client package (SDK replacement)
│   ├── __init__.py
│   ├── client.py           # VehicleServiceClient — one method per endpoint
│   ├── models.py           # Vehicle dataclass
│   ├── exceptions.py       # typed errors (400/401/404/409/500)
│   └── config.py           # env-based config (no hardcoded secrets)
├── main.py                 # demo app: full create→list→get→update→delete flow
├── requirements.txt
└── .env.example
```

## Endpoints covered

| Method | Path | Client method |
|--------|------|---------------|
| GET | `/vehicles` | `list_vehicles()` |
| GET | `/vehicles/:id` | `get_vehicle(id)` |
| POST | `/vehicles` | `create_vehicle(vehicle)` |
| PATCH | `/vehicles/:id` | `update_vehicle(id, changes)` |
| DELETE | `/vehicles/:id` | `delete_vehicle(id)` |

## Setup & run

```bash
cd app
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# Point at your running service / the Vehicle Service Mock, and set your key.
export VEHICLE_API_BASE_URL="http://localhost:59141"
export VEHICLE_API_KEY="<your-api-key>"

python main.py
```

## Using the client in your own code

```python
from vehicle_service import VehicleServiceClient, Vehicle

client = VehicleServiceClient()  # reads base URL + API key from the environment

vehicle = client.create_vehicle(Vehicle(
    nickName="Dolly", vin="JN8AZ2KR1AT169594",
    make="Nissan", model="Cube", year="2010", miles=59000,
))
print(client.get_vehicle(vehicle.id).to_dict())
```

## Security

The API key is read from the `VEHICLE_API_KEY` environment variable at runtime
and sent in the `X-API-Key` header. It is never hardcoded or committed — keep
your real `.env` out of version control (it is already git-ignored).
