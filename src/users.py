from flask import request
from flask_restful import Resource
from schema import  SchemaError
from bson import ObjectId

from database.db import db
from database.users import user_schema, update_user_schema
from util.authentication import Authentication as Auth
from util.exception import ExceptionMessages as message
from util.validation import Validation
from datetime import datetime
from util.common import Common

class UsersApi(Resource):
    def get(self):
        try: 
            Auth.check_admin_access(Auth, request.headers.get('authToken'))
            return Common.get_list(Common, request, db.users)
        except Exception as e:
            return {'error': str(e)}, 401

    def post(self):
        try:
            Auth.check_admin_access(Auth, request.headers.get('authToken'))
            body = request.get_json()
            user_schema.validate(body)
            Validation.validate_active_customer(Validation, body['customer_code'])
            body['password'] = Auth.hash_password(Auth, body['password'])
            body['created_at'] = datetime.now()
            body['updated_at'] = datetime.now()
            user =  db.users.insert_one(body)
            return {'message': 'User added successfully', "id": str(user.inserted_id)}, 201
        except SchemaError as e:
            return {'error': message.InvalidRequestSchema, 'details': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 401
        
class UserApi(Resource):
    def put(self, id):
        try:
            Auth.check_admin_access(Auth, request.headers.get('authToken'))
            body = request.get_json()
            update_user_schema.validate(body)
            Validation.validate_active_customer(Validation, body['customer_code'])
            body['updated_at'] = datetime.now()
            if '_id' in body:
                del body['_id']
                del body['password']
            
            result = db.users.update_one({'_id': ObjectId(id)}, {'$set': body})
            
            if result.modified_count == 1:
                return {'message': 'User updated successfully'}, 200
            else:
                return {'error': message.UserNotExist}, 404
        
        except SchemaError as e:
            return {'error': message.InvalidRequestSchema, 'details': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 401
    
    def delete(self, id):
        try:
            Auth.check_admin_access(Auth, request.headers.get('authToken'))
            result = db.users.delete_one({'_id': ObjectId(id)})
            if result.deleted_count == 1:
                return {'message': 'User deleted successfully'}, 200
            else:
                return {'error': message.UserNotExist}, 404
        except Exception as e:
            return {'error': str(e)}, 401

    def get(self, id):
        try:
            Auth.check_admin_access(Auth, request.headers.get('authToken'))
            data = db.users.find_one({'_id': ObjectId(id)})
            if data:
                data['_id'] = str(data['_id'])
                data['created_at'] = str(data['created_at'])
                data['updated_at'] = str(data['updated_at'])
                del data['password']
                return {'data': data}, 200
            else:
                return {'error': message.UserNotExist}, 404
        except Exception as e:
            return {'error': str(e)}, 401
        


