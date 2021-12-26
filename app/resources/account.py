# -*- coding: utf-8 -*-
"""Account API."""
import uuid

from flask_restful import Resource, reqparse

from app.models.account import AccountModel


class AccountCollection(Resource):
    """/account endpoint."""

    DEFAULT_LIMIT = 10

    parser = reqparse.RequestParser()
    parser.add_argument(
        "page", type=int, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument("limit", type=int)

    def get(self):
        """Return all accounts collection."""
        data = AccountCollection.parser.parse_args()
        page = data["page"]
        limit = data["limit"] if data["limit"] else self.DEFAULT_LIMIT
        accounts = list(map(lambda x: x.json(), AccountModel.get_all()))
        list_of_acc_list = [
            accounts[i:i + limit] for i in range(0, len(accounts), limit)
        ]
        try:
            accounts_page = list_of_acc_list[page - 1]
        except IndexError:
            return {"message": "Page out of range!"}, 400
        return {
            "page": page,
            "limit": limit,
            "total": len(accounts_page),
            "accounts": accounts_page,
        }


class AddAccount(Resource):
    """/account endpoint."""

    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="'Name' field cannot be left blank!"
    )
    parser.add_argument(
        "location",
        type=str,
        required=True,
        help="'Location' field cannot be left blank!",
    )

    def post(self):
        """Create an account if not existing."""
        data = AddAccount.parser.parse_args()

        if AccountModel.find_by_name(data["name"]):
            return {"message": "An account with this name already exists."}, 400

        acc_uuid = str(uuid.uuid1())

        account = AccountModel(data["name"], data["location"], acc_uuid)
        account.save_to_db()

        return {"message": "Account created successfully."}, 201


class AccountBulk(Resource):
    """/account/bulk endpoint."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="name' field cannot be left blank!", action="append"
    )
    parser.add_argument(
        "location",
        type=str,
        required=True,
        help="'Location' field cannot be left blank!",
        action="append"
    )

    def post(self):
        """Post bulk account list."""
        data = self.parser.parse_args()
        name_list = data["name"]
        location_list = data["location"]

        account_object_list = []

        for i in range(0, len(name_list)):
            acc_uuid = str(uuid.uuid1())
            account = AccountModel(name_list[i], location_list[i], acc_uuid)
            account_object_list.append(account)

        AccountModel.bulk_insert(account_object_list)

        return 200


class Account(Resource):
    """/account/{account id} endpoint."""

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("location", type=str)

    def get(self, account_uuid):
        """Return a specific account."""
        account = AccountModel.find_by_uuid(account_uuid)
        if account:
            return account.json()
        return {"message": "Account not found"}, 404

    def delete(self, account_uuid):
        """Delete a specific account."""
        account = AccountModel.find_by_uuid(account_uuid)
        if account:
            account.delete_from_db()
            return {"message": "Account deleted."}
        return {"message": "Account not found."}, 404

    def put(self, account_uuid):
        """Modify an specific account."""
        data = Account.parser.parse_args()
        account = AccountModel.find_by_uuid(account_uuid)
        if account:
            if data["name"]:
                account.name = data["name"]
            if data["location"]:
                account.location = data["location"]

            account.save_to_db()
            return {"account": account.json()}
        return {"message": "Account not found"}, 404
