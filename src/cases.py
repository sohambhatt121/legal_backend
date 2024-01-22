from flask import request
from flask_restful import Resource
from schema import  SchemaError
from bson import ObjectId
from flask import jsonify

from database.db import db
from database.cases import case_schema, update_case_schema
from util.authentication import Authentication as Auth
from util.exception import ExceptionMessages as message
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
                raise Exception(message.UnauthorizedUser)
            
            return Common.get_list(Common, request, db.cases)
        except Exception as e:
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
            return {'error': message.InvalidRequestSchema, 'details': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 401
        
class CasesApi(Resource):
    def put(self, id):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            body = request.get_json()
            update_case_schema.validate(body)
            data = db.cases.find_one({'_id': ObjectId(id)})
            if data:
                Validation.validate_user_customer_relation(Validation, user_id, data['customer_code'])
            else:
                return {'error': message.CaseNotExist}, 404
            
            body['updated_at'] = datetime.now()
            result = db.cases.update_one({'_id': ObjectId(id)}, {'$set': body})
            
            if result.modified_count == 1:
                return {'message': 'Case updated successfully'}, 200
            else:
                return {'error': message.CaseNotExist}, 404
        
        except SchemaError as e:
            return {'error': message.InvalidRequestSchema, 'details': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 401
    
    def delete(self, id):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            data = db.cases.find_one({'_id': ObjectId(id)})
            if data:
                Validation.validate_user_customer_relation(Validation, user_id, data['customer_code'])
            else:
                return {'error': message.CaseNotExist}, 404
            
            result = db.cases.delete_one({'_id': ObjectId(id)})
            if result.deleted_count == 1:
                return {'message': 'Case deleted successfully'}, 200
            else:
                return {'error': message.CaseNotExist}, 404
        except Exception as e:
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
                return {'error': message.CaseNotExist}, 404
        except Exception as e:
            return {'error': str(e)}, 401
        
class Helper():    
    def list_cases(self, request):
        per_page = int(request.args.get('per_page', 10))
        page_number = int(request.args.get('page_number', 1))
        sort_by = request.args.get('sort_by', '_id')
        order = request.args.get('order', 'asc')

        match_stage = Common.prepare_filter(Common, request)
        
        pipeline = [
            {'$match': match_stage},
            {'$sort': {sort_by: 1 if order == 'asc' else -1}},
            {'$skip': (page_number - 1) * per_page},
            {'$limit': per_page}
        ]

        cases = db.cases.aggregate(pipeline)

        total = db.cases.count_documents(match_stage)
        cases_list = list(cases)
        Common.make_JSON_serializable(Common, cases_list)
        
        return jsonify({
            'data': cases_list,
            'per_page': per_page,
            'current_page': page_number,
            'total': total
        })