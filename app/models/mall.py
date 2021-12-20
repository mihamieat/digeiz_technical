# -*- coding: utf-8 -*-
"""Account model."""
import sqlite3

class Mall:
    """Search a mall in the database."""

    TABLE_NAME = "mall"

    def __init__(self, name, _id, account_id, place_number):
        """Init mall with name and location."""
        self.name = name
        self._id = _id
        self.account_id = account_id
        self.place_number = place_number

    @classmethod
    def find_by_name(cls, name):
        """Find an mall in table by its name."""
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {
                "mall": {
                    "id": row[0],
                    "name": row[1],
                    "account_id": row[2],
                    "place_number": row[3],
                }
            }

    @classmethod
    def find_by_id(cls, _id):
        """Find a mall in table by its id."""
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        connection.close()

        if row:
            return {
                "mall": {
                    "id": row[0],
                    "name": row[1],
                    "account_id": row[2],
                    "place_number": row[3],
                }
            }

    @classmethod
    def find_by_account_id(cls, account_id):
        """Find all mall of an account."""
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE account_id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (account_id,))

        malls = []
        for row in result:
            malls.append({"id": row[0], "name": row[1], "account_id": row[2]})

        connection.close()
        return {"malls": malls}