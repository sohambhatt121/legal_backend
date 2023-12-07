from flask import request
from flask_restful import Resource
from schema import  SchemaError
from bson import ObjectId

from database.db import db
from database.clients import client_schema
from util.authentication import Authentication as Auth
from util.exception import NotAdminException, InvalidCustomerCode, CustomerInactive, AuthTokenExpired
from util.exception import UserNotExist, UserInactive, InvaliAuthToken, UnauthorizedUser
from datetime import datetime
from util.validation import Validation

class ClientApi(Resource):
    def get(self):
        try: 
            user_id = Auth.validate_token(request.headers.get('auth_token'))
            customer_code = request.args.get('customer_code')
            user_customer_code = Validation.get_customer_by_user(user_id)
            if customer_code != user_customer_code:
                raise UnauthorizedUser("User is UnAthorized")
            
            clients = list(db.clients.find({'customer_code': customer_code}))
            for item in clients:
                item['_id'] = str(item['_id'])
                item['created_at'] = str(item['created_at'])
                item['updated_at'] = str(item['updated_at'])
            return {'data': clients}, 200
        except NotAdminException as e:
            return {'error': str(e)}, 401
        except UnauthorizedUser as e:
            return {'error': str(e)}, 401
        except UserInactive as e:
            return {'error': str(e)}, 401
        except UserNotExist as e:
            return {'error': str(e)}, 401

    def post(self):
        try:
            user_id = Auth.validate_token(request.headers.get('auth_token'))
            body = request.get_json()
            client_schema.validate(body)
            Validation.validate_active_customer(body['customer_code'])
            Validation.validate_user_customer_relation(user_id, body['customer_code'])
            body['user_id'] = user_id
            body['created_at'] = datetime.now()
            body['updated_at'] = datetime.now()
            client =  db.clients.insert_one(body)
            return {'message': 'Client added successfully', "id": str(client.inserted_id)}, 201
        except SchemaError as e:
            return {'error': 'Invalid request data', 'details': str(e)}, 400
        except NotAdminException as e:
            return {'error': str(e)}, 401
        except CustomerInactive as e:
            return {'error': str(e)}, 401
        except InvalidCustomerCode as e:
            return {'error': str(e)}, 401
        except AuthTokenExpired as e:
            return {'error': str(e)}, 401
        except InvaliAuthToken as e:
            return {'error': str(e)}, 401
        except UserInactive as e:
            return {'error': str(e)}, 401
        except UserNotExist as e:
            return {'error': str(e)}, 401
        
class ClientsApi(Resource):
    def put(self, id):
        try:
            user_id = Auth.validate_token(request.headers.get('auth_token'))
            body = request.get_json()
            client_schema.validate(body)
            data = db.clients.find_one({'_id': ObjectId(id)})
            Validation.validate_user_customer_relation(user_id, data['customer_code'])
            body['updated_at'] = datetime.now()
            body['user_id'] = user_id
            if '_id' in body:
                del body['_id']
            
            result = db.clients.update_one({'_id': ObjectId(id)}, {'$set': body})
            
            if result.modified_count == 1:
                return {'message': 'User updated successfully'}, 200
            else:
                return {'error': 'User not found'}, 404
        
        except SchemaError as e:
            return {'error': 'Invalid request data', 'details': str(e)}, 400
        except NotAdminException as e:
            return {'error': str(e)}, 401
        except CustomerInactive as e:
            return {'error': str(e)}, 401
        except InvalidCustomerCode as e:
            return {'error': str(e)}, 401
        except UserInactive as e:
            return {'error': str(e)}, 401
        except UserNotExist as e:
            return {'error': str(e)}, 401
    
    def delete(self, id):
        try:
            user_id = Auth.validate_token(request.headers.get('auth_token'))
            data = db.clients.find_one({'_id': ObjectId(id)})
            Validation.validate_user_customer_relation(user_id, data['customer_code'])
            
            result = db.clients.delete_one({'_id': ObjectId(id)})
            if result.deleted_count == 1:
                return {'message': 'Client deleted successfully'}, 200
            else:
                return {'error': 'Client not found'}, 404
        except NotAdminException as e:
            return {'error': str(e)}, 401
        except UserInactive as e:
            return {'error': str(e)}, 401
        except UserNotExist as e:
            return {'error': str(e)}, 401
        except InvalidCustomerCode as e:
            return {'error': str(e)}, 401

    def get(self, id):
        try:
            user_id = Auth.validate_token(request.headers.get('auth_token'))
            data = db.clients.find_one({'_id': ObjectId(id)})
            Validation.validate_user_customer_relation(user_id, data['customer_code'])
            
            if data:
                data['_id'] = str(data['_id'])
                data['created_at'] = str(data['created_at'])
                data['updated_at'] = str(data['updated_at'])
                return {'data': data}, 200
            else:
                return {'error': 'Client not found'}, 404
        except NotAdminException as e:
            return {'error': str(e)}, 401
        except UnauthorizedUser as e:
            return {'error': str(e)}, 401
        except UserInactive as e:
            return {'error': str(e)}, 401
        except UserNotExist as e:
            return {'error': str(e)}, 401
        except InvalidCustomerCode as e:
            return {'error': str(e)}, 401
        


