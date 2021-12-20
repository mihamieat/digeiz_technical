# -*- coding: utf-8 -*-
"""Unit model."""
import sqlite3

class Unit:
    """Search a unit in the database."""

    TABLE_NAME = "unit"

    def __init__(self, name, _id, mall_id, price):
        """Init Acount with name and location."""
        self.name = name
        self._id = _id
        self.mall_id = mall_id
        self.price = price

    @classmethod
    def find_by_name(cls, name):
        """Find a unit in table by its name."""
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {"unit": {"id": row[0], "name": row[1], "price": row[2]}}

    @classmethod
    def find_by_id(cls, _id):
        """Find a unit in table by its id."""
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"account": {"id": row[0], "name": row[1], "price": row[2]}}

    @classmethod
    def find_by_mall_id(cls, mall_id):
        """Find all unit of a mall."""
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE mall_id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (mall_id,))

        units = []
        for row in result:
            units.append({"id": row[0], "name": row[1], "mall_id": row[2]})

        connection.close()
        return {"units": units}