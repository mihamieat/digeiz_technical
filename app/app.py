# -*- coding: utf-8 -*-
"""API app."""
from app.create_table import create_table
from app.resources.account import AccountCollection, AccountEdit, AddAccount
from app.resources.mall import AddMall, MallCollection, MallEdit
from app.resources.unit import AddUnit, UnitCollection, UnitEdit

from flask import Flask

from flask_restful import Api


def create_app():
    """Create the Flask appliction."""
    app = Flask(__name__)
    app.secret_key = "4CE1E6FD-BD68-4E73-B920-5EE95FD03FEC"
    api = Api(app)

    api.add_resource(AccountCollection, "/account")
    api.add_resource(AddAccount, "/account")
    api.add_resource(AccountEdit, "/account/<string:account_id>")

    api.add_resource(MallCollection, "/mall")
    api.add_resource(AddMall, "/mall/<string:account_id>")
    api.add_resource(MallEdit, "/mall/<string:mall_id>")

    api.add_resource(UnitCollection, "/unit")
    api.add_resource(AddUnit, "/unit/<string:mall_id>")
    api.add_resource(UnitEdit, "/unit/<string:unit_id>")

    create_table()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)
