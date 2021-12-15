import uuid
from flask import Flask
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
app.secret_key = "4CE1E6FD-BD68-4E73-B920-5EE95FD03FEC"
api = Api(app)

accounts = []

malls = []

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
    
    def post(self):
        """Create an account if not existing."""
        
        data = AddAccount.parser.parse_args()
        if next(filter(lambda x: x['name'] == data['name'], accounts), None) is not None:
            return {'message': "An account with the name '{}' already exists.".format(data['name'])}
        
        new_uuid = str(uuid.uuid1())

        account = {'name': data['name'], 'id': new_uuid}
        accounts.append(account)

        return account, 201

class AddMall(Resource):
    """Create a new mall linked to an account with /mall endpoint."""
    
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self, account_id):
        """Create a new mall if not existing to /mall/{account id}."""
        account =  next(filter(lambda x: x['id'] == account_id, accounts), None)
        
        data = AddMall.parser.parse_args()

        if account:
            if next(filter(lambda x: x['name'] == data['name'] and x['account_id'] == account_id, malls), None) is not None:
                return {'message': "A mall with the name '{}' already exists in '{}' account.".format(data['name'], account['name'])}
            mall_id = str(uuid.uuid1())
            mall = {'name': data['name'], 'id': mall_id, 'account_id': account['id']}
            malls.append(mall)
            return mall, 201
        else:
            return {'message': 'This account does not exist.'}

api.add_resource(AccountList, '/account')
api.add_resource(MallList, '/mall')
api.add_resource(UnitList, '/unit')
api.add_resource(AddAccount, '/account')
api.add_resource(AddMall, '/mall/<string:account_id>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)