from flask import request
from flask_restful import Resource
from schema import  SchemaError
from bson import ObjectId

from database.db import db
from database.customers import customer_schema
from util.authentication import Authentication as Auth
from util.exception import NotAdminException
from datetime import datetime

class CustomersApi(Resource):
    def get(self):
        try: 
            Auth.check_admin_access(request.headers.get('authToken'))
            query = Helper.get_query_params(request.args)
            customers = list(db.customers.find(query))
            for item in customers:
                item['_id'] = str(item['_id'])
                item['created_at'] = str(item['created_at'])
                item['updated_at'] = str(item['updated_at'])
            return {'data': customers}, 200
        except NotAdminException as e:
            return {'error': str(e)}, 401

    def post(self):
        try:
            Auth.check_admin_access(request.headers.get('authToken'))
            body = request.get_json()
            customer_schema.validate(body)
            body['created_at'] = datetime.now()
            body['updated_at'] = datetime.now()
            customers =  db.customers.insert_one(body)
            return {'message': 'Data added successfully', "id": str(customers.inserted_id)}, 201
        except SchemaError as e:
            return {'error': 'Invalid request data', 'details': str(e)}, 400
        except NotAdminException as e:
            return {'error': str(e)}, 401
        
class CustomerApi(Resource):
    def put(self, id):
        try:
            Auth.check_admin_access(request.headers.get('authToken'))
            body = request.get_json()
            customer_schema.validate(body)
            body['updated_at'] = datetime.now()
            if '_id' in body:
                del body['_id']
            
            result = db.customers.update_one({'_id': ObjectId(id)}, {'$set': body})
            
            if result.modified_count == 1:
                return {'message': 'Data updated successfully'}, 200
            else:
                return {'error': 'Data not found'}, 404
        
        except SchemaError as e:
            return {'error': 'Invalid request data', 'details': str(e)}, 400
        except NotAdminException as e:
            return {'error': str(e)}, 401
    
    def delete(self, id):
        try:
            Auth.check_admin_access(request.headers.get('authToken'))
            result = db.customers.delete_one({'_id': ObjectId(id)})
            if result.deleted_count == 1:
                return {'message': 'Data deleted successfully'}, 200
            else:
                return {'error': 'Data not found'}, 404
        except NotAdminException as e:
            return {'error': str(e)}, 401

    def get(self, id):
        try:
            Auth.check_admin_access(request.headers.get('authToken'))
            data = db.customers.find_one({'_id': ObjectId(id)})
            if data:
                data['_id'] = str(data['_id'])
                data['created_at'] = str(data['created_at'])
                data['updated_at'] = str(data['updated_at'])
                return {'data': data}, 200
            else:
                return {'error': 'Data not found'}, 404
        except NotAdminException as e:
            return {'error': str(e)}, 401
        
class CustomerCodeApi(Resource):
    def get(self, id):
        try:
            Auth.check_admin_access(request.headers.get('authToken'))
            data = db.customers.find_one({'customer_code': id})
            if data:
                data['_id'] = str(data['_id'])
                data['created_at'] = str(data['created_at'])
                data['updated_at'] = str(data['updated_at'])
                return {'data': data}, 200
            else:
                return {'error': 'Data not found'}, 404
        except NotAdminException as e:
            return {'error': str(e)}, 401
        
class Helper():
    def get_query_params(args):
        query = {}
        status = args.get('status')
        if status is None:
            query['status'] = 1
        
        return query