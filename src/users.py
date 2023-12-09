from flask import request
from flask_restful import Resource
from schema import  SchemaError
from bson import ObjectId

from database.db import db
from database.users import user_schema
from util.authentication import Authentication as Auth
from util.exception import NotAdminException, InvalidCustomerCode, CustomerInactive
from util.validation import Validation
from datetime import datetime

class UsersApi(Resource):
    def get(self):
        try: 
            Auth.check_admin_access(request.headers.get('authToken'))
            users = list(db.users.find())
            for item in users:
                item['_id'] = str(item['_id'])
                item['created_at'] = str(item['created_at'])
                item['updated_at'] = str(item['updated_at'])
            return {'data': users}, 200
        except NotAdminException as e:
            return {'error': str(e)}, 401

    def post(self):
        try:
            Auth.check_admin_access(request.headers.get('authToken'))
            body = request.get_json()
            user_schema.validate(body)
            Validation.validate_active_customer(body['customer_code'])
            body['password'] = Auth.hash_password(body['password'])
            body['created_at'] = datetime.now()
            body['updated_at'] = datetime.now()
            user =  db.users.insert_one(body)
            return {'message': 'User added successfully', "id": str(user.inserted_id)}, 201
        except SchemaError as e:
            return {'error': 'Invalid request data', 'details': str(e)}, 400
        except NotAdminException as e:
            return {'error': str(e)}, 401
        except CustomerInactive as e:
            return {'error': str(e)}, 401
        except InvalidCustomerCode as e:
            return {'error': str(e)}, 401
        
class UserApi(Resource):
    def put(self, id):
        try:
            Auth.check_admin_access(request.headers.get('authToken'))
            body = request.get_json()
            user_schema.validate(body)
            Validation.validate_active_customer(body['customer_code'])
            body['updated_at'] = datetime.now()
            if '_id' in body:
                del body['_id']
            
            result = db.users.update_one({'_id': ObjectId(id)}, {'$set': body})
            
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
    
    def delete(self, id):
        try:
            Auth.check_admin_access(request.headers.get('authToken'))
            result = db.users.delete_one({'_id': ObjectId(id)})
            if result.deleted_count == 1:
                return {'message': 'User deleted successfully'}, 200
            else:
                return {'error': 'User not found'}, 404
        except NotAdminException as e:
            return {'error': str(e)}, 401

    def get(self, id):
        try:
            Auth.check_admin_access(request.headers.get('authToken'))
            data = db.users.find_one({'_id': ObjectId(id)})
            if data:
                data['_id'] = str(data['_id'])
                data['created_at'] = str(data['created_at'])
                data['updated_at'] = str(data['updated_at'])
                return {'data': data}, 200
            else:
                return {'error': 'User not found'}, 404
        except NotAdminException as e:
            return {'error': str(e)}, 401
        


