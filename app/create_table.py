# -*- coding: utf-8 -*-
"""Table creation."""

import sqlite3


def create_table():
    """Create a SQL table for account mall and unit."""
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    # account table
    create_table = "CREATE TABLE IF NOT EXISTS account (id, name  text, location text)"
    cursor.execute(create_table)

    # mall table
    create_table = (
        "CREATE TABLE IF NOT EXISTS mall (id, name  text, account_id, place_number)"
    )
    cursor.execute(create_table)

    # unit table
    create_table = "CREATE TABLE IF NOT EXISTS unit (name text PRIMARY KEY, price real)"
    cursor.execute(create_table)

    connection.commit()

    connection.close()
