from flask import Response, request
from database.db import db
from flask_restful import Resource
from schema import Schema, And, SchemaError
from database.customers import customer_schema
from bson import ObjectId, json_util

class CustomersApi(Resource):
    def get(self):
        customers = list(db.customers.find())
        for item in customers:
            item['_id'] = str(item['_id'])
        return {'data': customers}, 200

    def post(self):
        try:
            body = request.get_json()
            customer_schema.validate(body)
            customers =  db.customers.insert_one(body)
            return {'message': 'Data added successfully', "id": str(customers.inserted_id)}, 201
        except SchemaError as e:
            return {'error': 'Invalid request data', 'details': str(e)}, 400
        
        
class CustomerApi(Resource):
    def put(self, id):
        try:
            updated_data = request.get_json()
            customer_schema.validate(updated_data)
            if '_id' in updated_data:
                del updated_data['_id']
            
            result = db.customers.update_one({'_id': ObjectId(id)}, {'$set': updated_data})
            
            if result.modified_count == 1:
                return {'message': 'Data updated successfully'}, 200
            else:
                return {'error': 'Data not found'}, 404
        
        except SchemaError as e:
            return {'error': 'Invalid request data', 'details': str(e)}, 400
    
    def delete(self, id):
        result = db.customers.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return {'message': 'Data deleted successfully'}, 200
        else:
            return {'error': 'Data not found'}, 404

    def get(self, id):
        data = db.customers.find_one({'_id': ObjectId(id)})
        if data:
            data['_id'] = str(data['_id'])
            return {'data': data}, 200
        else:
            return {'error': 'Data not found'}, 404
        
class CustomerCodeApi(Resource):
    def get(self, id):
        data = db.customers.find_one({'customer_code': id})
        if data:
            data['_id'] = str(data['_id'])
            return {'data': data}, 200
        else:
            return {'error': 'Data not found'}, 404
        