# -*- coding: utf-8 -*-
"""Account model."""
import sqlite3


class Account:
    """Search an account in the database."""

    TABLE_NAME = "account"

    def __init__(self, name, _id, location):
        """Init Acount with name, id and location."""
        self.name = name
        self._id = _id
        self.location = location

    @classmethod
    def find_by_name(cls, name):
        """Find an account in table by its name."""
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {"account": {"id": row[0], "name": row[1], "location": row[2]}}

    @classmethod
    def find_by_id(cls, _id):
        """Find an account in table by its id."""
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"account": {"id": row[0], "name": row[1], "location": row[2]}}
