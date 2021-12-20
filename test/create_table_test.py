# -*- coding: utf-8 -*-
"""Table creation."""

import sqlite3


def create_table_test():
    """Create a SQL table for account mall and unit."""
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    # account table
    insert_values = "INSERT INTO account VALUES (12345, 'account1', 'Lilles')"
    cursor.execute(insert_values)

    # mall table
    insert_values = "INSERT INTO mall VALUES (6789, 'mall1', 12345, 1)"
    cursor.execute(insert_values)

    # unit table
    insert_values = "INSERT INTO unit VALUES (10111213, 'unit1', 6789, 100)"
    cursor.execute(insert_values)

    connection.commit()

    connection.close()

create_table_test()