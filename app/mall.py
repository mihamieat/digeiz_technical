# -*- coding: utf-8 -*-
"""mall API."""
import sqlite3
import uuid

from flask_restful import Resource, reqparse


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


class MallCollection(Resource):
    """/mall endpoint."""

    TABLE_NAME = "mall"
    DEFAULT_LIMIT = 10

    parser = reqparse.RequestParser()
    parser.add_argument(
        "page", type=int, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument("limit", type=int)

    def get(self):
        """Return all malls."""
        data = MallCollection.parser.parse_args()
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
        page_data["malls"] = []

        for row in result:
            page_data["malls"].append(
                {
                    "id": row[0],
                    "name": row[1],
                    "account_id": row[2],
                    "place_number": row[3],
                }
            )

        page_data["count"] = len(page_data["malls"])

        connection.close()
        return {"malls": page_data}


class AddMall(Resource):
    """/mall/{account id} endpoint."""

    TABLE_NAME = "mall"

    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "place_number", type=int, required=True, help="This field cannot be left blank!"
    )

    def post(self, account_id):
        """Create a new mall for a given account."""
        data = AddMall.parser.parse_args()
        if Mall.find_by_name(data["name"]) and Mall.find_by_account_id(account_id):
            return {
                "message": "Mall with that name in this account already exists"
            }, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES (?, ?, ?, ?)".format(table=self.TABLE_NAME)
        mall_id = str(uuid.uuid1())
        cursor.execute(query, (mall_id, data["name"], account_id, data["place_number"]))

        connection.commit()
        connection.close()

        return {
            "mall": {
                "id": mall_id,
                "name": data["name"],
                "account_id": account_id,
                "place_number": data["place_number"],
            }
        }, 201


class MallEdit(Resource):
    """/mall/{mall id} endpoint."""

    TABLE_NAME = "mall"

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("place_number", type=int)

    def get(self, mall_id):
        """Return a specific mall."""
        mall = Mall.find_by_id(mall_id)
        if mall:
            return mall
        return {"message": "Mall not found!"}, 404

    def delete(self, mall_id):
        """Delete a specific mal."""
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE id=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (mall_id,))

        connection.commit()
        connection.close()

        return {"message": "Mall deleted."}

    def put(self, mall_id):
        """Modify an specific account."""
        data = MallEdit.parser.parse_args()
        update_mall = {"name": data["name"], "place_number": data["place_number"]}
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "UPDATE {table} SET name=ifnull(?, name), place_number=ifnull(?, place_number) WHERE id=?".format(
            table=self.TABLE_NAME
        )
        cursor.execute(
            query, (update_mall["name"], update_mall["place_number"], mall_id)
        )

        connection.commit()
        connection.close()

        return 201
