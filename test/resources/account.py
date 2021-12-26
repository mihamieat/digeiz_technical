# -*- coding: utf-8 -*-
"""test account resource."""
from app.app import create_app

import pytest


@pytest.fixture
def client():
    """Client init."""
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        with app.test_client() as client:
            yield client


def test_empty_account_body(client):
    """Start with a blank database."""
    rv = client.get("/account")
    assert b'{"message": {"page": "This field cannot be left blank!"}}\n' in rv.data
