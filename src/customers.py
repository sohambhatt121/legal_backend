from flask import request
from flask_restful import Resource
from schema import  SchemaError
from bson import ObjectId

from database.db import db
from database.customers import customer_schema, update_customer_schema
from util.authentication import Authentication as Auth
from util.exception import ExceptionMessages as message
from datetime import datetime
from util.common import Common

class CustomersApi(Resource):
    def get(self):
        try: 
            Auth.check_admin_access(Auth, request.headers.get('authToken'))
            return Common.get_list(Common, request, db.customers)
        except Exception as e:
            return {'error': str(e)}, 401

    def post(self):
        try:
            Auth.check_admin_access(Auth, request.headers.get('authToken'))
            body = request.get_json()
            customer_schema.validate(body)
            body['created_at'] = datetime.now()
            body['updated_at'] = datetime.now()
            customers =  db.customers.insert_one(body)
            return {'message': 'Data added successfully', "id": str(customers.inserted_id)}, 201
        except SchemaError as e:
            return {'error': message.InvalidRequestSchema, 'details': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 401
        
class CustomerApi(Resource):
    def put(self, id):
        try:
            Auth.check_admin_access(Auth, request.headers.get('authToken'))
            body = request.get_json()
            update_customer_schema.validate(body)
            body['updated_at'] = datetime.now()
            
            result = db.customers.update_one({'_id': ObjectId(id)}, {'$set': body})
            
            if result.modified_count == 1:
                return {'message': 'Data updated successfully'}, 200
            else:
                return {'error': message.CustomerNotExist}, 404
        
        except SchemaError as e:
            return {'error': message.InvalidRequestSchema, 'details': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 401
    
    def delete(self, id):
        try:
            Auth.check_admin_access(Auth, request.headers.get('authToken'))
            result = db.customers.delete_one({'_id': ObjectId(id)})
            if result.deleted_count == 1:
                return {'message': 'Data deleted successfully'}, 200
            else:
                return {'error': message.CustomerNotExist}, 404
        except Exception as e:
            return {'error': str(e)}, 401

    def get(self, id):
        try:
            Auth.check_admin_access(Auth, request.headers.get('authToken'))
            data = db.customers.find_one({'_id': ObjectId(id)})
            if data:
                data['_id'] = str(data['_id'])
                data['created_at'] = str(data['created_at'])
                data['updated_at'] = str(data['updated_at'])
                return {'data': data}, 200
            else:
                return {'error': message.CustomerNotExist}, 404
        except Exception as e:
            return {'error': str(e)}, 401
        
class CustomerCodeApi(Resource):
    def get(self, id):
        try:
            Auth.check_admin_access(Auth, request.headers.get('authToken'))
            data = db.customers.find_one({'customer_code': id})
            if data:
                data['_id'] = str(data['_id'])
                data['created_at'] = str(data['created_at'])
                data['updated_at'] = str(data['updated_at'])
                return {'data': data}, 200
            else:
                return {'error': message.CustomerNotExist}, 404
        except Exception as e:
            return {'error': str(e)}, 401
