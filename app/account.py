# -*- coding: utf-8 -*-
"""Account API."""
import sqlite3
import uuid

from flask_restful import Resource, reqparse


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


class AccountCollection(Resource):
    """/account endpoint."""

    TABLE_NAME = "account"

    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "location", type=str, required=True, help="This field cannot be left blank!"
    )

    def get(self):
        """Return all accounts."""
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        accounts = []
        for row in result:
            accounts.append({"id": row[0], "name": row[1], "location": row[2]})
        connection.close()

        return {"accounts": accounts}

    def post(self):
        """Create an account if not existing."""
        data = AccountCollection.parser.parse_args()
        if Account.find_by_name(data["name"]):
            return {"message": "Account with that username already exists."}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES (?, ?, ?)".format(table=self.TABLE_NAME)
        account_id = str(uuid.uuid1())
        cursor.execute(query, (account_id, data["name"], data["location"]))

        connection.commit()
        connection.close()

        return {
            "account": {
                "id": account_id,
                "name": data["name"],
                "location": data["location"],
            }
        }, 201


class AccountEdit(Resource):
    """/account/{account id} endpoint."""

    TABLE_NAME = "account"

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("location", type=str)

    def get(self, account_id):
        """Return a specific account."""
        account = Account.find_by_id(account_id)
        if account:
            return account
        return {"message": "account not found!"}, 404

    def delete(self, account_id):
        """Delete a specific account."""
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE id=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (account_id,))

        connection.commit()
        connection.close()

        return {"message": "Account deleted."}

    def put(self, account_id):
        """Modify an specific account."""
        data = AccountEdit.parser.parse_args()
        update_account = {"name": data["name"], "location": data["location"]}
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "UPDATE {table} SET name=ifnull(?, name), location=ifnull(?, location) WHERE id=?".format(
            table=self.TABLE_NAME
        )
        cursor.execute(
            query, (update_account["name"], update_account["location"], account_id)
        )

        connection.commit()
        connection.close()

        return 201
