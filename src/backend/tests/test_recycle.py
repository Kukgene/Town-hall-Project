# pylint: disable=redefined-outer-name
"""Testing module for /recycle endpoint"""
from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import text
from pydantic import ValidationError
from app.schemas.recycle_user import (
    ItemRecycleUserCreate,
    ItemRecycleUser,
)


def test_recycle_user_model():
    """Test ItemRecycleUser model"""
    try:
        ItemRecycleUserCreate(name="test", phone_number="010-1234-5678", bags=2)
    except ValidationError:
        assert False, "`id` and `created_at` must be defined automatically"

    # Check if error raises on bags > 3 or bags < 1
    with pytest.raises(ValueError):
        ItemRecycleUserCreate(id=1, name="test", phone_number="010-1234-5678", bags=4)
        ItemRecycleUserCreate(id=1, name="test", phone_number="010-1234-5678", bags=0)
        ItemRecycleUser(id=1, name="test", phone_number="010-1234-5678", bags=4)
        ItemRecycleUser(id=1, name="test", phone_number="010-1234-5678", bags=0)

    # Check if error raises on invalid phone number
    with pytest.raises(ValueError):
        ItemRecycleUserCreate(id=1, name="test", phone_number="01012345678", bags=1)
        ItemRecycleUserCreate(id=1, name="test", phone_number="this-is-test", bags=1)
        ItemRecycleUser(id=1, name="test", phone_number="01012345678", bags=1)
        ItemRecycleUser(id=1, name="test", phone_number="this-is-test", bags=1)

    # Check if error raises on required value missing
    with pytest.raises(ValueError):
        ItemRecycleUser(name="test", phone_number="01012345678", bags=1)
        ItemRecycleUser(
            name="test", phone_number="01012345678", bags=1, created_at=datetime.now()
        )
        ItemRecycleUser(id=1, name="test", phone_number="this-is-test", bags=1)


def test_create_recycle_user(client: TestClient, session: Session):
    """Test post endpoint"""
    session.execute(text("DROP TABLE IF EXISTS recycle_users;"))
    session.execute(
        text(
            """
    CREATE TABLE recycle_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    bags INTEGER NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """
        )
    )
    response = client.post(
        "/recycle",
        json=ItemRecycleUserCreate(
            id=1, name="test", phone_number="010-1234-5678", bags=3
        ).model_dump_json(),
    )
    assert (
        session.execute(text("SELECT * FROM recycle_users WHERE id=1;")).fetchone()
        is not None
    ), "Data has not been recorded"
    assert response.json()["id"] is not None, "Endpoint must return created object"
    response = client.post(
        "/recycle",
        json=ItemRecycleUserCreate(
            id=1, name="test", phone_number="010-1234-5678", bags=3
        ).model_dump_json(),
    )
    assert response.status_code == 422
    response = client.post(
        "/recycle",
        json=ItemRecycleUserCreate(
            name="test1", phone_number="010-1234-5678", bags=3
        ).model_dump_json(),
    )
    assert (
        session.execute(text("SELECT * FROM recycle_users WHERE id=2;")).fetchone()
        is not None
    ), "Data has not been recorded"
    assert response.status_code == 201
