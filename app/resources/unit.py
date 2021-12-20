# -*- coding: utf-8 -*-
"""unit API."""
import sqlite3
import uuid

from app.models.unit import Unit

from flask_restful import Resource, reqparse


class UnitCollection(Resource):
    """/unit endpoint."""

    TABLE_NAME = "unit"
    DEFAULT_LIMIT = 10

    parser = reqparse.RequestParser()
    parser.add_argument(
        "page", type=int, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument("limit", type=int)

    def get(self):
        """Return all units."""
        data = UnitCollection.parser.parse_args()
        page = data["page"]
        limit = data["limit"] if data["limit"] else self.DEFAULT_LIMIT
        offset = limit * (page - 1)

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM {table} LIMIT ? OFFSET ?".format(table=self.TABLE_NAME)
        result = cursor.execute(query, (limit, offset))

        page_data = {}
        page_data["page_number"] = page
        page_data["limit"] = limit
        page_data["units"] = []
        for row in result:
            page_data["units"].append(
                {"id": row[0], "name": row[1], "mall_id": row[2], "price": row[3]}
            )

        page_data["count"] = len(page_data["units"])

        connection.close()
        return {"units": page_data}


class AddUnit(Resource):
    """/unit/{account id} endpoint."""

    TABLE_NAME = "unit"

    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "price", type=int, required=True, help="This field cannot be left blank!"
    )

    def post(self, mall_id):
        """Create a new unit for a given account."""
        data = AddUnit.parser.parse_args()
        if Unit.find_by_name(data["name"]) and Unit.find_by_mall_id(mall_id):
            return {"message": "Unit with that name in this mall already exists"}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES (?, ?, ?, ?)".format(table=self.TABLE_NAME)
        unit_id = str(uuid.uuid1())
        cursor.execute(query, (unit_id, data["name"], mall_id, data["price"]))

        connection.commit()
        connection.close()

        return {
            "unit": {
                "id": unit_id,
                "name": data["name"],
                "mall_id": mall_id,
                "price": data["price"],
            }
        }, 201


class UnitEdit(Resource):
    """/unit/{unit id} endpoint."""

    TABLE_NAME = "unit"

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("price", type=int)

    def get(self, unit_id):
        """Return a specific unit."""
        unit = Unit.find_by_id(unit_id)
        if unit:
            return unit
        return {"message": "Unit not found!"}, 404

    def delete(self, unit_id):
        """Delete a specific mal."""
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE id=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (unit_id,))

        connection.commit()
        connection.close()

        return {"message": "Unit deleted."}

    def put(self, unit_id):
        """Modify an specific account."""
        data = UnitEdit.parser.parse_args()
        update_unit = {"name": data["name"], "price": data["price"]}
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "UPDATE {table} SET name=ifnull(?, name), price=ifnull(?, price) WHERE id=?".format(
            table=self.TABLE_NAME
        )
        cursor.execute(query, (update_unit["name"], update_unit["price"], unit_id))

        connection.commit()
        connection.close()

        return 201
