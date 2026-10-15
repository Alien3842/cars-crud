"""Testing workshop - unit tier.

Copied exercise test plus the new test required by the workshop:
"Write your own unit test that rejects a blank model."
"""

import pytest
from pydantic import ValidationError

from app.schemas import CarInput

pytestmark = pytest.mark.unit


def test_car_text_fields_are_trimmed():
    """Copied from the workshop (Step A)."""
    car = CarInput(
        make="  Mazda  ",
        model="  MX-5  ",
        year=2020,
        color="  Red  ",
    )
    assert car.make == "Mazda"
    assert car.model == "MX-5"
    assert car.color == "Red"


def test_blank_model_is_rejected():
    """My own test (Step D): a whitespace-only model must be rejected."""
    with pytest.raises(ValidationError):
        CarInput(make="Mazda", model=" ", year=2020)
