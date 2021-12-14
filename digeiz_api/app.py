from flask import Flask
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
app.secret_key = "4CE1E6FD-BD68-4E73-B920-5EE95FD03FEC"
api = Api(app)

accounts = []

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

class AddAccount(Resource):
    """Create a new account from /account endpoint."""
    
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    
    def post(self):
        """Create an account if not existing."""
        
        data = AddAccount.parser.parse_args()
        if next(filter(lambda x: x['name'] == data['name'], accounts), None) is not None:
            return {'message': "An account with the name '{}' already exists".format(data['name'])}

        account = {'name': data['name'], 'password': data['password']}
        accounts.append(account)

        return account, 201

api.add_resource(AccountList, '/account')
api.add_resource(MallList, '/mall')
api.add_resource(UnitList, '/unit')
api.add_resource(AddAccount, '/account')

if __name__ == '__main__':
    app.run(port=5000, debug=True)