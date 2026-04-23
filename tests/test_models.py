import pytest
from pydantic import ValidationError

from data_contract_validator.models import UserContract


def test_valid_user_contract():
    user = UserContract(
        id=1,
        name="Anna",
        email="anna@example.com",
        age=30,
    )

    assert user.id == 1
    assert user.name == "Anna"
    assert user.email == "anna@example.com"
    assert user.age == 30


def test_invalid_email_raises_validation_error():
    with pytest.raises(ValidationError):
        UserContract(
            id=1,
            name="Anna",
            email="not-an-email",
            age=30,
        )


def test_underage_user_raises_validation_error():
    with pytest.raises(ValidationError):
        UserContract(
            id=1,
            name="Anna",
            email="anna@example.com",
            age=16,
        )
