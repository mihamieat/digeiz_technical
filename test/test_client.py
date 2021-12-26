# -*- coding: utf-8 -*-
"""test client."""
import os

from app.app import create_app
from app.models.account import AccountModel
from app.models.mall import MallModel
from app.models.unit import UnitModel

import pytest

os.remove("app/test.db")


@pytest.fixture
def client():
    """Client init."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

    with app.app_context():
        with app.test_client() as client:
            yield client


def test_empty_account_body(client):
    """Start a blank body."""
    res = client.get("/account")
    assert res.status_code == 400
    assert b'"This field cannot be left blank!"' in res.data


def test_create_account(client):
    """Create an account."""
    res = client.post("/account", data={"name": "dummy", "location": "somewhere"})
    assert res.status_code == 201


def test_recreate_same_account(client):
    """Recreate an existing account."""
    res = client.post("/account", data={"name": "dummy", "location": "somewhere"})
    assert res.status_code == 400


def test_edit_account(client):
    """Edit an account."""
    account = AccountModel("some_name", "some_location", "7cbb0b7e-667b-11ec-a387-acde48001122")
    account.save_to_db()
    res = client.put("/account/7cbb0b7e-667b-11ec-a387-acde48001122", data={"name": "new_name", "location": "Paris"})
    assert res.status_code == 200


def test_get_a_false_account(client):
    """Retrieve a non existing account."""
    res = client.get("/account/09876")
    assert res.status_code == 404


def test_get_a_false_mall(client):
    """Retrieve a non existing mall."""
    res = client.get("/mall/09876")
    assert res.status_code == 404


def test_get_a_false_unit(client):
    """Retrieve a non existing unit."""
    res = client.get("/unit/09876")
    assert res.status_code == 404


def test_empty_mall_body(client):
    """Start a blank body."""
    res = client.get("/mall")
    assert res.status_code == 400
    assert b'"Page field cannot be left blank!"' in res.data


def test_create_mall(client):
    """Create a mall."""
    res = client.post("/mall/7cbb0b7e-667b-11ec-a387-acde48001122", data={"name": "mall2", "place_number": 2})
    assert res.status_code == 201


def test_recreate_same_mall(client):
    """Recreate an existing account."""
    res = client.post("/mall/12345", data={"name": "mall2", "mall2": 4})
    assert res.status_code == 400


def test_edit_mall(client):
    """Edit a mall."""
    mall = MallModel("some_mall", 44, "64230578-6681-11ec-bfcb-acde48001122", "7cbb0b7e-667b-11ec-a387-acde48001122")
    mall.save_to_db()
    res = client.put("/mall/64230578-6681-11ec-bfcb-acde48001122", data={"name": "new_name"})
    assert res.status_code == 200


def test_empty_unit_body(client):
    """Start a blank body."""
    res = client.get("/unit")
    assert res.status_code == 400
    assert b'"This field cannot be left blank!"' in res.data


def test_create_unit(client):
    """Create a unit."""
    res = client.post("/unit/64230578-6681-11ec-bfcb-acde48001122", data={"name": "t-shirt", "price": 200})
    assert res.status_code == 201


def test_recreate_same_unit(client):
    """Recreate an existing unit."""
    res = client.post("/unit/64230578-6681-11ec-bfcb-acde48001122", data={"name": "t-shirt", "price": 200})
    assert res.status_code == 400


def test_edit_unit(client):
    """Edit a unit."""
    unit = UnitModel("unit", 123.99, "fa396f66-6681-11ec-a3ba-acde48001122", "64230578-6681-11ec-bfcb-acde48001122")
    unit.save_to_db()
    res = client.put("/unit/fa396f66-6681-11ec-a3ba-acde48001122", data={"name": "new_name"})
    assert res.status_code == 201


def test_delete_account(client):
    """Delete a given account."""
    res = client.delete("/account/7cbb0b7e-667b-11ec-a387-acde48001122")
    assert res.status_code == 200


def test_delete_mall(client):
    """Delete a given mall."""
    res = client.delete("/mall/64230578-6681-11ec-bfcb-acde48001122")
    assert res.status_code == 200


def test_delete_unit(client):
    """Delete a given unit."""
    res = client.delete("/unit/fa396f66-6681-11ec-a3ba-acde48001122")
    assert res.status_code == 200
