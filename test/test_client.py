# -*- coding: utf-8 -*-
"""test client."""
import pytest
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

def test_empty_mall_body(client):
    """Start a blank body."""

    res = client.get('/mall')
    assert res.status_code == 400
    assert b'"This field cannot be left blank!"' in res.data

def test_empty_unit_body(client):
    """Start a blank body."""

    res = client.get('/unit')
    assert res.status_code == 400
    assert b'"This field cannot be left blank!"' in res.data