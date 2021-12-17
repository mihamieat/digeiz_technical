# -*- coding: utf-8 -*-
"""API app."""
import uuid

from account import AccountCollection, AccountEdit

from create_table import create_table

from flask import Flask

from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
app.secret_key = "4CE1E6FD-BD68-4E73-B920-5EE95FD03FEC"
api = Api(app)

accounts = []

malls = []

units = []


class MallList(Resource):
    """/mall endpoint."""

    def get(self):
        """Get the account list method."""
        return {"malls": malls}


class UnitList(Resource):
    """/unit endpoint."""

    def get(self):
        """Get the account list method."""
        return {"units": units}


class AddMall(Resource):
    """/mall/{account id} endpoint."""

    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank!"
    )

    def post(self, account_id):
        """Create a new mall if not existing."""
        account = next(filter(lambda x: x["id"] == account_id, accounts), None)

        data = AddMall.parser.parse_args()

        if account:
            if (
                next(
                    filter(
                        lambda x: x["name"] == data["name"]
                        and x["account_id"] == account_id,
                        malls,
                    ),
                    None,
                )
                is not None
            ):
                return {
                    "message": "A mall with the name '{}' already exists in '{}' account.".format(
                        data["name"], account["name"]
                    )
                }
            mall_id = str(uuid.uuid1())
            mall = {"name": data["name"], "id": mall_id, "account_id": account["id"]}
            malls.append(mall)
            return mall, 201
        else:
            return {"message": "This account does not exist."}


class AddUnit(Resource):
    """/unit/{mall id} endpoint."""

    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank!"
    )

    def post(self, mall_id):
        """Create a new unit if not existing."""
        mall = next(filter(lambda x: x["id"] == mall_id, malls), None)

        data = AddUnit.parser.parse_args()

        if mall:
            if (
                next(
                    filter(
                        lambda x: x["name"] == data["name"] and x["mall_id"] == mall_id,
                        units,
                    ),
                    None,
                )
                is not None
            ):
                return {
                    "message": "A unit with the name '{}' already exists in '{}' mall.".format(
                        data["name"], mall["name"]
                    )
                }
            unit_id = str(uuid.uuid1())
            unit = {"name": data["name"], "id": unit_id, "mall_id": mall["id"]}
            units.append(unit)
            return unit, 201
        else:
            return {"message": "This mall does not exist."}


class Mall(Resource):
    """/mall/{mall id} endpoint."""

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("category", type=str)
    parser.add_argument("surface", type=float)

    def get(self, mall_id):
        """Return a specific mall."""
        mall = next(filter(lambda x: x["id"] == mall_id, malls), None)
        return {"mall": mall}, 200 if mall else 404

    def delete(self, mall_id):
        """Delete a specific mall."""
        global malls
        malls = list(filter(lambda x: x["id"] != mall_id, malls))
        return {"message": "mall deleted"}

    def put(self, mall_id):
        """Modify an specific mall."""
        mall = next(filter(lambda x: x["id"] == mall_id, malls), None)
        if mall is None:
            return {"message": "There is no such mall!"}

        data = Mall.parser.parse_args()
        data = {k: v for k, v in data.items() if v is not None}
        mall.update(data)
        return mall, 201


class Unit(Resource):
    """/unit/{unit id} endpoint."""

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("type", type=str)
    parser.add_argument("price", type=float)

    def get(self, unit_id):
        """Return a specific unit."""
        unit = next(filter(lambda x: x["id"] == unit_id, units), None)
        return {"unit": unit}, 200 if unit else 404

    def delete(self, unit_id):
        """Delete a specific unit."""
        global units
        units = list(filter(lambda x: x["id"] != unit_id, units))
        return {"message": "unit deleted"}

    def put(self, unit_id):
        """Modify an specific unit."""
        unit = next(filter(lambda x: x["id"] == unit_id, units), None)
        if unit is None:
            return {"message": "There is no such unit!"}

        data = Unit.parser.parse_args()
        data = {k: v for k, v in data.items() if v is not None}
        unit.update(data)
        return unit, 201


api.add_resource(AccountCollection, "/account")
api.add_resource(MallList, "/mall")
api.add_resource(UnitList, "/unit")
api.add_resource(AddMall, "/mall/<string:account_id>")
api.add_resource(AddUnit, "/unit/<string:mall_id>")
api.add_resource(AccountEdit, "/account/<string:account_id>")
api.add_resource(Mall, "/mall/<string:mall_id>")
api.add_resource(Unit, "/unit/<string:unit_id>")

if __name__ == "__main__":
    create_table()
    app.run(port=5000, debug=True)
