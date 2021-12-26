# -*- coding: utf-8 -*-
"""test account model."""
import pytest

from app.models.account import AccountModel


@pytest.fixture
def account():
    """Test account model."""
    account = AccountModel("some_name", "some_location", "7cbb0b7e-667b-11ec-a387-acde48001122")
    