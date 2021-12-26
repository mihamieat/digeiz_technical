# -*- coding: utf-8 -*-
"""API app."""
from flask import Flask

from flask_restful import Api

from app.resources.account import Account, AccountBulk, AccountCollection, AddAccount
from app.resources.mall import AddMall, Mall, MallBulk, MallCollection
from app.resources.unit import AddUnit, Unit, UnitBulk, UnitCollection


def create_app():
    """Create the Flask appliction."""
    from app.db import db

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.secret_key = "4CE1E6FD-BD68-4E73-B920-5EE95FD03FEC"
    api = Api(app)

    @app.before_first_request
    def create_tables():
        """Initialy create the tables."""
        db.create_all()

    db.init_app(app)

    api.add_resource(AccountCollection, "/account")
    api.add_resource(AddAccount, "/account")
    api.add_resource(Account, "/account/<string:account_uuid>")
    api.add_resource(AccountBulk, "/account/bulk")

    api.add_resource(MallCollection, "/mall")
    api.add_resource(AddMall, "/mall/<string:account_uuid>")
    api.add_resource(Mall, "/mall/<string:mall_uuid>")
    api.add_resource(MallBulk, "/mall/bulk/<string:account_uuid>")

    api.add_resource(UnitCollection, "/unit")
    api.add_resource(AddUnit, "/unit/<string:mall_uuid>")
    api.add_resource(Unit, "/unit/<string:unit_uuid>")
    api.add_resource(UnitBulk, "/unit/bulk/<string:mall_uuid>")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)
