# -*- coding: utf-8 -*-
"""mall API."""
import uuid

from flask_restful import Resource, reqparse

from app.models.account import AccountModel
from app.models.mall import MallModel


class MallCollection(Resource):
    """/mall endpoint."""

    DEFAULT_LIMIT = 10

    parser = reqparse.RequestParser()
    parser.add_argument(
        "page", type=int, required=True, help="Page field cannot be left blank!"
    )
    parser.add_argument("limit", type=int)

    def get(self):
        """Return all malls collection."""
        data = MallCollection.parser.parse_args()
        page = data["page"]
        limit = data["limit"] if data["limit"] else self.DEFAULT_LIMIT

        malls = list(map(lambda x: x.json(), MallModel.get_all()))

        list_of_mall_list = [malls[i:i + limit] for i in range(0, len(malls), limit)]

        try:
            malls_page = list_of_mall_list[page - 1]
        except IndexError:
            return {"message": "Page out of range!"}, 400
        return {
            "page": page,
            "limit": limit,
            "total": len(malls_page),
            "malls": malls_page,
        }


class AddMall(Resource):
    """/mall/{account uuid} endpoint."""

    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="Name field cannot be left blank!"
    )
    parser.add_argument(
        "place_number",
        type=int,
        required=True,
        help="Place Number field cannot be left blank!",
    )

    def post(self, account_uuid):
        """Create a new mall for a given account."""
        data = AddMall.parser.parse_args()
        if MallModel.find_by_name(data["name"]) and AccountModel.find_by_uuid(
            account_uuid
        ):
            return {
                "message": "Mall with that name in this account already exists."
            }, 400
        if MallModel.find_by_place_number(
            data["place_number"]
        ) and AccountModel.find_by_uuid(account_uuid):
            return {"message": "This place is already occupied."}, 400

        mall_uuid = str(uuid.uuid1())

        mall = MallModel(data["name"], data["place_number"], mall_uuid, account_uuid)
        mall.save_to_db()

        return {"message": "Mall created successfully."}, 201

class MallBulk(Resource):
    """/mall/bulk/{account uuid} endpoint."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="name' field cannot be left blank!", action="append"
    )
    parser.add_argument(
        "place_number",
        type=int,
        required=True,
        help="'Place number' field cannot be left blank!",
        action="append"
    )
    def post(self, account_uuid):
        """Post bulk mall list."""
        data = self.parser.parse_args()
        name_list = data["name"]
        place_list = data["place_number"]

        mall_object_list = []

        for i in range(0, len(name_list)):
            mall_uuid = str(uuid.uuid1())
            mall = MallModel(name_list[i], place_list[i], mall_uuid, account_uuid)
            mall_object_list.append(mall)
        
        MallModel.bulk_insert(mall_object_list)

        return 200


class Mall(Resource):
    """/mall/{mall id} endpoint."""

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("place_number", type=str)

    def get(self, mall_uuid):
        """Return a specific mall."""
        mall = MallModel.find_by_uuid(mall_uuid)
        if mall:
            return mall.json()
        return {"message": "Mall not found"}, 404

    def delete(self, mall_uuid):
        """Delete a specific mall."""
        mall = MallModel.find_by_uuid(mall_uuid)
        if mall:
            mall.delete_from_db()
            return {"message": "Mall deleted."}
        return {"message": "Mall not found."}, 404

    def put(self, mall_uuid):
        """Modify an specific mall."""
        data = Mall.parser.parse_args()
        mall = MallModel.find_by_uuid(mall_uuid)
        if mall:
            if data["name"]:
                mall.name = data["name"]
            if data["place_number"]:
                mall.place_number = data["place_number"]

            mall.save_to_db()
            return {"mall": mall.json()}
        return {"message": "Mall not found"}, 404
