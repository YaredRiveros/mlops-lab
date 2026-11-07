"""Test de contrato de la API: schemas.py debe rechazar requests incompletos o inválidos."""
import pytest
from pydantic import ValidationError

from src.api.schemas import HousePredictionRequest

VALID = {"sqft": 1527, "bedrooms": 2, "bathrooms": 1.5,
         "location": "Suburb", "year_built": 1956, "condition": "Good"}


def test_valid_request_is_accepted():
    assert HousePredictionRequest(**VALID).location == "Suburb"


@pytest.mark.parametrize("field", list(VALID))
def test_missing_field_is_rejected(field):
    body = {k: v for k, v in VALID.items() if k != field}
    with pytest.raises(ValidationError) as exc:
        HousePredictionRequest(**body)
    assert exc.value.errors()[0]["type"] == "missing"
    assert exc.value.errors()[0]["loc"] == (field,)


def test_unknown_location_is_rejected():
    with pytest.raises(ValidationError):
        HousePredictionRequest(**{**VALID, "location": "Beach"})
