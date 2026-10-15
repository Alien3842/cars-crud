"""Testing workshop - API tier.

Copied exercise test plus the new test required by the workshop:
"Write your own API test that rejects an invalid year without saving data."
"""

import pytest

pytestmark = pytest.mark.api


def test_post_car_returns_201_and_json(client):
    """Copied from the workshop (Step A)."""
    payload = {
        "make": "Ford",
        "model": "Fiesta",
        "year": 2018,
        "color": "Black",
    }
    response = client.post("/api/cars", json=payload)
    assert response.status_code == 201
    car = response.json()
    assert car["id"] > 0
    assert car["make"] == "Ford"
    assert car["model"] == "Fiesta"
    assert response.headers["location"] == f"/api/cars/{car['id']}"


def test_invalid_year_is_not_saved(client):
    """My own test (Step D): a year below 1886 must be rejected and not stored."""
    payload = {
        "make": "Ford",
        "model": "Fiesta",
        "year": 1800,
        "color": "Black",
    }
    response = client.post("/api/cars", json=payload)
    assert response.status_code == 422

    listing = client.get("/api/cars")
    assert listing.status_code == 200
    assert listing.json() == []
