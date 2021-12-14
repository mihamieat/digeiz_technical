from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
app.secret_key = "4CE1E6FD-BD68-4E73-B920-5EE95FD03FEC"
api = Api(app)

accounts = [
    {
        'name': 'some_account',
        'id': 1
    }
]

malls = [
    {
        'name': 'some_mall',
        'id': 1
    }
]

units = [
    {
        'name': 'some_unit',
        'id': 1
    }
]

class AccountList(Resource):
    """Resource to get all accounts list from /account endpoint."""
    def get(self):
        """Get the account list method."""
        return {'accounts': accounts}

class MallList(Resource):
    """Resource to get all malls list from /mall endpoint."""
    def get(self):
        """Get the account list method."""
        return {'malls': malls}

class UnitList(Resource):
    """Resource to get all unit list from /unit endpoint."""
    def get(self):
        """Get the account list method."""
        return {'units': units}

api.add_resource(AccountList, '/account')
api.add_resource(MallList, '/mall')
api.add_resource(UnitList, '/unit')

if __name__ == '__main__':
    app.run(debug=True)