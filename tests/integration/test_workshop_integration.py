"""Testing workshop - integration tier.

Copied exercise test plus the new test required by the workshop:
"Write your own integration test that deletes one car without affecting another."
"""

import pytest

from app import database
from app.schemas import CarInput

pytestmark = pytest.mark.integration


def test_saved_car_can_be_read_from_sqlite(database_path):
    """Copied from the workshop (Step A)."""
    database.initialize(database_path)
    saved = database.create_car(
        database_path,
        CarInput(make="Toyota", model="Yaris", year=2020, color="Blue"),
    )
    loaded = database.get_car(database_path, saved.id)
    assert loaded is not None
    assert loaded.id == saved.id
    assert loaded.make == "Toyota"
    assert loaded.year == 2020


def test_deleting_one_car_keeps_the_other(database_path):
    """My own test (Step D): deleting one car must not touch the other."""
    database.initialize(database_path)
    first = database.create_car(
        database_path,
        CarInput(make="Ford", model="Fiesta", year=2018, color="Black"),
    )
    second = database.create_car(
        database_path,
        CarInput(make="Mazda", model="MX-5", year=2020, color="Red"),
    )

    assert database.delete_car(database_path, first.id) is True

    assert database.get_car(database_path, first.id) is None
    remaining = database.get_car(database_path, second.id)
    assert remaining is not None
    assert remaining.id == second.id

    cars = database.list_cars(database_path)
    assert len(cars) == 1
    assert cars[0].id == second.id
