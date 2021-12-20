# -*- coding: utf-8 -*-
"""test client."""
import os
import pytest

os.remove('data.db')

from app.app import create_app

@pytest.fixture
def client():
    """Client init."""
    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as client:
            yield client

def test_empty_account_body(client):
    """Start a blank body."""
    res = client.get('/account')
    assert res.status_code == 400
    assert b'"This field cannot be left blank!"' in res.data

def test_create_account(client):
    """Create an account"""
    res = client.post('/account', data={"name": "dummy", "location": "somewhere"})
    assert res.status_code == 201

def test_recreate_same_account(client):
    """Recreate an existing account."""
    res = client.post('/account', data={"name": "dummy", "location": "somewhere"})
    assert res.status_code == 400

def test_edit_account(client):
    """Edit an account."""
    res = client.put("/account/1234", data={"name": "new_name", "location": "Paris"})
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
    res = client.get('/mall')
    assert res.status_code == 400
    assert b'"This field cannot be left blank!"' in res.data

def test_create_mall(client):
    """Create an account"""
    res = client.post('/mall/12345', data={"name": "mall2", "place_number": 2})
    assert res.status_code == 201

def test_recreate_same_mall(client):
    """Recreate an existing account."""
    res = client.post('/mall/12345', data={"name": "mall2", "mall2": 4})
    assert res.status_code == 400

def test_edit_mall(client):
    """Edit a mall."""
    res = client.put("/account/6789", data={"name": "new_name"})
    assert res.status_code == 200

def test_empty_unit_body(client):
    """Start a blank body."""
    res = client.get('/unit')
    assert res.status_code == 400
    assert b'"This field cannot be left blank!"' in res.data

def test_create_unit(client):
    """Create a unit."""
    res = client.post('/unit/6789', data={"name": "t-shirt", "price": 200})
    assert res.status_code == 201

def test_recreate_same_unit(client):
    """Recreate an existing unit."""
    res = client.post('/unit/6789', data={"name": "t-shirt", "price": 200})
    assert res.status_code == 400

def test_edit_unit(client):
    """Edit a unit."""
    res = client.put("/unit/10111213", data={"name": "new_name"})
    assert res.status_code == 200

def test_delete_account(client):
    """Delete a given account."""
    res = client.delete("/account/1234")
    assert res.status_code == 200

def test_delete_mall(client):
    """Delete a given mall."""
    res = client.delete("/account/6789")
    assert res.status_code == 200

def test_delete_unit(client):
    """Delete a given unit."""
    res = client.delete("/unit/10111213")
    assert res.status_code == 200