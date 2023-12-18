from flask import request
from flask_restful import Resource
from schema import  SchemaError
from bson import ObjectId

from database.db import db
from database.cases import case_schema
from util.authentication import Authentication as Auth
from util.exception import NotAdminException, InvalidCustomerCode, CustomerInactive, AuthTokenExpired
from util.exception import UserNotExist, UserInactive, InvaliAuthToken, UnauthorizedUser
from util.exception import ClientInactive, ClientNotExist
from datetime import datetime
from util.validation import Validation
from util.common import Common

class CaseApi(Resource):
    def get(self):
        try: 
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            customer_code = request.args.get('customer_code')
            user_customer_code = Common.get_customer_by_user(Common, user_id)
            if customer_code != user_customer_code:
                raise UnauthorizedUser("User is UnAthorized")
            
            cases = list(db.cases.find({'customer_code': customer_code}))
            for item in cases:
                item['_id'] = str(item['_id'])
                item['created_at'] = str(item['created_at'])
                item['updated_at'] = str(item['updated_at'])
            return {'data': cases}, 200
        except NotAdminException as e:
            return {'error': str(e)}, 401
        except UnauthorizedUser as e:
            return {'error': str(e)}, 401
        except UserInactive as e:
            return {'error': str(e)}, 401
        except UserNotExist as e:
            return {'error': str(e)}, 401
        except InvaliAuthToken as e:
            return {'error': str(e)}, 401
        except AuthTokenExpired as e:
            return {'error': str(e)}, 401

    def post(self):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            body = request.get_json()
            case_schema.validate(body)
            Validation.validate_active_customer(Validation, body['customer_code'])
            Validation.validate_user_customer_relation(Validation, user_id, body['customer_code'])
            Validation.validate_active_client(Validation, body['client_id'])
            body['added_by'] = user_id
            body['created_at'] = datetime.now()
            body['updated_at'] = datetime.now()
            client =  db.cases.insert_one(body)
            return {'message': 'Case added successfully', "id": str(client.inserted_id)}, 201
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
        except ClientInactive as e:
            return {'error': str(e)}, 401
        except ClientNotExist as e:
            return {'error': str(e)}, 401
        
class CasesApi(Resource):
    def put(self, id):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            body = request.get_json()
            case_schema.validate(body)
            data = db.cases.find_one({'_id': ObjectId(id)})
            if data:
                Validation.validate_user_customer_relation(Validation, user_id, data['customer_code'])
            else:
                return {'error': 'Case not found'}, 404
            
            body['updated_at'] = datetime.now()
            if '_id' in body:
                del body['_id']
            
            result = db.cases.update_one({'_id': ObjectId(id)}, {'$set': body})
            
            if result.modified_count == 1:
                return {'message': 'Case updated successfully'}, 200
            else:
                return {'error': 'Case not found'}, 404
        
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
        except InvaliAuthToken as e:
            return {'error': str(e)}, 401
        except AuthTokenExpired as e:
            return {'error': str(e)}, 401
    
    def delete(self, id):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            data = db.cases.find_one({'_id': ObjectId(id)})
            if data:
                Validation.validate_user_customer_relation(Validation, user_id, data['customer_code'])
            else:
                return {'error': 'Case not found'}, 404
            
            result = db.cases.delete_one({'_id': ObjectId(id)})
            if result.deleted_count == 1:
                return {'message': 'case deleted successfully'}, 200
            else:
                return {'error': 'Case not found'}, 404
        except NotAdminException as e:
            return {'error': str(e)}, 401
        except UserInactive as e:
            return {'error': str(e)}, 401
        except UserNotExist as e:
            return {'error': str(e)}, 401
        except InvalidCustomerCode as e:
            return {'error': str(e)}, 401
        except InvaliAuthToken as e:
            return {'error': str(e)}, 401
        except AuthTokenExpired as e:
            return {'error': str(e)}, 401

    def get(self, id):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            data = db.cases.find_one({'_id': ObjectId(id)})
            
            if data:
                Validation.validate_user_customer_relation(Validation, user_id, data['customer_code'])
                data['_id'] = str(data['_id'])
                data['created_at'] = str(data['created_at'])
                data['updated_at'] = str(data['updated_at'])
                return {'data': data}, 200
            else:
                return {'error': 'Case not found'}, 404
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
        except InvaliAuthToken as e:
            return {'error': str(e)}, 401
        except AuthTokenExpired as e:
            return {'error': str(e)}, 401