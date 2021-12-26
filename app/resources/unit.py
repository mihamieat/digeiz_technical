# -*- coding: utf-8 -*-
"""Unit API."""
import uuid

from flask_restful import Resource, reqparse

from app.models.mall import MallModel
from app.models.unit import UnitModel


class UnitCollection(Resource):
    """/unit endpoint."""

    DEFAULT_LIMIT = 10

    parser = reqparse.RequestParser()
    parser.add_argument(
        "page", type=int, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument("limit", type=int)

    def get(self):
        """Return all munitsalls collection."""
        data = UnitCollection.parser.parse_args()
        page = data["page"]
        limit = data["limit"] if data["limit"] else self.DEFAULT_LIMIT

        units = list(map(lambda x: x.json(), UnitModel.get_all()))

        list_of_unit_list = [units[i:i + limit] for i in range(0, len(units), limit)]

        try:
            unit_page = list_of_unit_list[page - 1]
        except IndexError:
            return {"message": "Page out of range!"}, 400
        return {
            "page": page,
            "limit": limit,
            "total": len(unit_page),
            "units": unit_page,
        }


class AddUnit(Resource):
    """/unit/{mall uuid} endpoint."""

    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="Name field cannot be left blank!"
    )
    parser.add_argument(
        "price", type=int, required=True, help="Price field cannot be left blank!"
    )

    def post(self, mall_uuid):
        """Create a new unit for a given mall."""
        data = AddUnit.parser.parse_args()
        if UnitModel.find_by_name(data["name"]) and MallModel.find_by_uuid(mall_uuid):
            return {"message": "Unit with that name in this mall already exists."}, 400

        unit_uuid = str(uuid.uuid1())

        unit = UnitModel(data["name"], data["price"], unit_uuid, mall_uuid)
        unit.save_to_db()

        return {"message": "Unit created successfully."}, 201

class UnitBulk(Resource):
    """/unit/bulk/{mall uuid} endpoint."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="name' field cannot be left blank!", action="append"
    )
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="'Price' field cannot be left blank!",
        action="append"
    )
    def post(self, mall_uuid):
        """Post bulk unit list."""
        data = self.parser.parse_args()
        name_list = data["name"]
        price_list = data["price"]

        unit_object_list = []

        for i in range(0, len(name_list)):
            unit_uuid = str(uuid.uuid1())
            unit = UnitModel(name_list[i], price_list[i], unit_uuid, mall_uuid)
            unit_object_list.append(unit)
        
        UnitModel.bulk_insert(unit_object_list)

        return 200

class Unit(Resource):
    """/unit/{unit id} endpoint."""

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("price", type=str)

    def get(self, unit_uuid):
        """Return a specific unit."""
        unit = UnitModel.find_by_uuid(unit_uuid)
        if unit:
            return unit.json()
        return {"message": "Unit not found"}, 404

    def delete(self, unit_uuid):
        """Delete a specific unit."""
        unit = UnitModel.find_by_uuid(unit_uuid)
        if unit:
            unit.delete_from_db()
            return {"message": "Unit deleted."}
        return {"message": "Unit not found."}, 404

    def put(self, unit_uuid):
        """Modify an specific mall."""
        data = Unit.parser.parse_args()
        unit = UnitModel.find_by_uuid(unit_uuid)
        if unit:
            if data["name"]:
                unit.name = data["name"]
            if data["price"]:
                unit.place_number = data["price"]

            unit.save_to_db()
            return {"unit": unit.json()}, 201
        return {"message": "Unit not found"}, 404
