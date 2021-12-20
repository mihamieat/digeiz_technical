# Digeiz api technical test
## Quick start
### Set up the environment
```shell
pipenv install
pipenv shell
export FLASK_APP=./app/app.py
```
### Run the application
```
flask run
```
### Run the test
```
tox
```
## Rest API
### Account
#### Get accounts list
```GET /account```
##### Body
```
{
    "page": int,
    "limit", int
}
```
##### Request
```
curl -i -H 'Accept: application/json' -H 'Content-Type: application/json' -X GET -d '{"page": 2, "limit": 2}' http://127.0.0.1:5000/account
```
##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 171
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Sat, 18 Dec 2021 17:33:01 GMT

{
    "accounts": {
        "page_number": 2,
        "limit": 2,
        "accounts": [
            {
                "id": "da2fc5d6-6029-11ec-9755-acde48001122",
                "name": "gamma",
                "location": "paris"
            },
            {
                "id": "462e5afe-602a-11ec-9755-acde48001122",
                "name": "new_name",
                "location": "Tours"
            }
        ],
        "count": 2
    }
}
```
#### Create a new account
```POST /account```
##### Body
```
{
    "name": "string",
    "location": "string"
}
```
##### Request
```
curl -i -H 'Accept: application/json' -X POST  -H 'Content-Type: application/json' -d '{"nale": "new_store", "location": "Nantes"}' http://127.0.0.1:5000/account
```
##### Response
```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 139
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Sat, 18 Dec 2021 17:48:38 GMT

{
    "account": {
        "id": "badc692c-602a-11ec-9755-acde48001122",
        "name": "new_store",
        "location": "Nantes"
    }
}
```
#### Return a specific account
```GET /account/{account id}```
##### Request
```
curl -H 'Accept: application/json' -X GET http://127.0.0.1:5000/account/da2fc5d6-6029-11ec-9755-acde48001122
```
##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 134
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Sun, 19 Dec 2021 21:38:37 GMT

{
    "account": {
        "id": "da2fc5d6-6029-11ec-9755-acde48001122",
        "name": "gamma",
        "location": "paris"
    }
}
```
#### Edit an account
```PUT /account/{account id}```
##### Body
```
{
    "name": "string",
    "location": "string"
}
```
##### Request
```
curl -H 'Accept: application/json' -H 'Content-Type: application/json' -X PUT  -d '{"nam": "new_name", "location": "Tours}' http://127.0.0.1:5000/account/badc692c-602a-11ec-9755-acde48001122
```
##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 4
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Sat, 18 Dec 2021 18:01:27 GMT

201
```
#### Delete an account
```DELETE /account/{account id}```
##### Request
```
curl -i -H 'Accept: application/json' -X DELETE http://127.0.0.1:5000/account/badc692c-602a-11ec-9755-acde48001122
```
##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 38
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Sat, 18 Dec 2021 17:51:36 GMT

{
    "message": "Account deleted."
}
```

### Mall
#### Get malls list
```GET /mall```
##### Bode
```
{
    "page": int,
    "limit", int
}
```
##### Request
```
curl -i -H 'Accept: application/json' -H 'Content-Type: application/json' -X GET -d '{"page": 1}' http://127.0.0.1:5000/mall
```
##### Response
```
{
    "malls": {
        "page_number": 1,
        "limit": 10,
        "malls": [
            {
                "id": "004e1a1a-6020-11ec-80cf-acde48001122",
                "name": "tesla",
                "account_id": "f9db2aec-601f-11ec-80cf-acde48001122",
                "place_number": 32
            },
            {
                "id": "946552aa-610a-11ec-bab0-acde48001122",
                "name": "shoppingmall",
                "account_id": "906c0d88-603d-11ec-99b7-acde48001122",
                "place_number": 1
            }
        ],
        "count": 2
    }
}
```
#### Create a new mall
```POST /mall/{account id}```
##### Body
```
{
    "name": "string",
    "place_number": "string"
}
```
##### Request
```
curl -i -H 'Accept: application/json' -H 'Content-Type: application/json' -X POST -d '{"name": "my_new_mall", "place_number": 2}' http://127.0.0.1:5000/mall/906c0d88-603d-11ec-99b7-acde48001122
```
##### Response
```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 197
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Sun, 19 Dec 2021 21:18:01 GMT

{
    "mall": {
        "id": "25cece64-6111-11ec-8996-acde48001122",
        "name": "my_new_mall",
        "account_id": "906c0d88-603d-11ec-99b7-acde48001122",
        "place_number": 2
    }
}
```
#### Retur a specific mall
```GET /mall/{mall id}```
##### Request
```
curl -i -H 'Accept: application/json' -X GET http://127.0.0.1:5000/mall/946552aa-610a-11ec-bab0-acde48001122
```
##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 173
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Sun, 19 Dec 2021 21:24:00 GMT

{
    "mall": {
        "id": "946552aa-610a-11ec-bab0-acde48001122",
        "name": "shoppingmall",
        "account_id": "906c0d88-603d-11ec-99b7-acde48001122",
        "place_number": 1
    }
}
```
#### Edit a mall
```PUT /mall/{mall id}```
##### Body
```
{
    "name": "string",
    "place_number": "string"
}
```
##### Request
```
curl -i -H 'Accept: application/json' -H 'Content-Type: application/json' -X PUT -d '{"name": "new_name", "place_number": 3}' http://127.0.0.1:5000/mall/f6062616-610e-11ec-bab0-acde48001122
```
##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 4
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Sun, 19 Dec 2021 21:19:34 GMT

201
```
#### Delete a mall
```DELETE /mall/{mall id}```
##### Request
```
curl -i -H 'Accept: application/json' -X DELETE http://127.0.0.1:5000/mall/946552aa-610a-11ec-bab0-acde48001122
```
##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 169
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Sun, 19 Dec 2021 21:21:00 GMT

{
    "mall": {
        "id": "946552aa-610a-11ec-bab0-acde48001122",
        "name": "shoppingmall",
        "account_id": "906c0d88-603d-11ec-99b7-acde48001122",
        "place_number": 1
    }
}
```

### Unit
#### Get units list
```GET /unit```
##### Request
```
curl -i -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"page":1}' -X GET http://127.0.0.1:5000/unit
```
##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 339
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Sun, 19 Dec 2021 21:43:33 GMT

{
    "units": {
        "page_number": 1,
        "limit": 10,
        "units": [
            {
                "id": "be848a3a-6022-11ec-91f2-acde48001122",
                "name": "belt",
                "mall_id": "004e1a1a-6020-11ec-80cf-acde48001122",
                "price": 100
            }
        ],
        "count": 1
    }
}
```
#### Create a new unit
```POST /unit/{mall id}```
##### Body
```
{
    "name": "string",
    "price": int
}
```
##### Request
```
curl -i -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name":"t-shirt", "price": 70}' -X POST http://127.0.0.1:5000/unit/269745e4-610f-11ec-b7b9-acde48001122
```
##### Response
```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 184
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Sun, 19 Dec 2021 21:47:28 GMT

{
    "unit": {
        "id": "42eb4bcc-6115-11ec-a4fa-acde48001122",
        "name": "t-shirt",
        "mall_id": "269745e4-610f-11ec-b7b9-acde48001122",
        "price": 70
    }
}
```
#### Return a specific unit
```GET /unit/{unit id}```
##### Request
```
curl -i -H 'Accept: application/json' -X GET http://127.0.0.1:5000/unit/42eb4bcc-6115-11ec-a4fa-acde48001122
```
##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 164
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Sun, 19 Dec 2021 21:48:58 GMT

{
    "account": {
        "id": "42eb4bcc-6115-11ec-a4fa-acde48001122",
        "name": "t-shirt",
        "price": "269745e4-610f-11ec-b7b9-acde48001122"
    }
}
```
#### Edit a unit
```PUT /unit/{unit id}```
##### Body
```
{
    "name": "string",
    "price": int
}
```
##### Request
```
curl -i -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name":"new_name", "price": 65}' -X POST http://127.0.0.1:5000/unit/42eb4bcc-6115-11ec-a4fa-acde48001122
```
##### Response
```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 185
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Sun, 19 Dec 2021 21:51:25 GMT

{
    "unit": {
        "id": "d00a6204-6115-11ec-a4fa-acde48001122",
        "name": "new_name",
        "mall_id": "42eb4bcc-6115-11ec-a4fa-acde48001122",
        "price": 65
    }
}
```
#### Delete a unit
```DELETE /unit/{unit id}```
##### Request
```
curl -i -H 'Accept: application/json' -X DELETE http://127.0.0.1:5000/unit/42eb4bcc-6115-11ec-a4fa-acde48001122
```
##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 35
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Sun, 19 Dec 2021 21:52:42 GMT

{
    "message": "Unit deleted."
}
```
