from flask import request
from flask_restful import Resource
from schema import  SchemaError
from bson import ObjectId
from flask import jsonify

import uuid
from database.db import db
from database.notes import note_schema
from util.authentication import Authentication as Auth
from util.exception import ExceptionMessages as message
from datetime import datetime
from util.validation import Validation
from util.common import Common

class NoteApi(Resource):
    def get(self):
        try: 
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            customer_code = request.args.get('customer_code')
            user_customer_code = Common.get_customer_by_user(Common, user_id)
            if customer_code != user_customer_code:
                raise Exception(message.UnauthorizedUser)
            
            return Helper.list_notes(Helper, request)
        except Exception as e:
            return {'error': str(e)}, 401

    def post(self):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            body = request.get_json()
            note_schema.validate(body)
            
            Validation.validate_active_customer(Validation, body['customer_code'])
            Validation.validate_user_customer_relation(Validation, user_id, body['customer_code'])

            body['added_by'] = user_id
            body['created_at'] = datetime.now()
            body['updated_at'] = datetime.now()

            note = db.notes.insert_one(body)
            return {'message': 'Note added successfully', "id": str(note.inserted_id)}, 201
        except SchemaError as e:
            return {'error': message.InvalidRequestSchema, 'details': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 401
        
class NotesApi(Resource):
    def put(self, id):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            body = request.get_json()
            note_schema.validate(body)
            data = db.notes.find_one({'_id': ObjectId(id)})
            print(data)
            if data:
                Validation.validate_active_customer(Validation, body['customer_code'])
                Validation.validate_user_customer_relation(Validation, user_id, data['customer_code'])
            else:
                return {'error': message.NotesNotExist}, 404
            
            body['updated_at'] = datetime.now()
            if '_id' in body:
                del body['_id']
            
            result = db.notes.update_one({'_id': ObjectId(id)}, {'$set': body})
            
            if result.modified_count == 1:
                return {'message': 'Notes updated successfully'}, 200
            else:
                return {'error': message.NotesNotExist}, 404
        
        except SchemaError as e:
            return {'error': message.InvalidRequestSchema, 'details': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 401
    
    def delete(self, id):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            data = db.notes.find_one({'_id': ObjectId(id)})
            if data:
                Validation.validate_active_customer(Validation, data['customer_code'])
                Validation.validate_user_customer_relation(Validation, user_id, data['customer_code'])
            else:
                return {'error': message.NotesNotExist}, 404
            
            result = db.notes.delete_one({'_id': ObjectId(id)})
            if result.deleted_count == 1:
                return {'message': 'Document deleted successfully'}, 200
            else:
                return {'error': message.NotesNotExist}, 404
        except Exception as e:
            return {'error': str(e)}, 401

    def get(self, id):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            data = db.notes.find_one({'_id': ObjectId(id)})
            
            if data:
                Validation.validate_user_customer_relation(Validation, user_id, data['customer_code'])
                data['_id'] = str(data['_id'])
                data['created_at'] = str(data['created_at'])
                data['updated_at'] = str(data['updated_at'])
                return {'data': data}, 200
            else:
                return {'error': message.NotesNotExist}, 404
        except Exception as e:
            return {'error': str(e)}, 401


class Helper():    
    def list_notes(self, request):
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

        notes = db.notes.aggregate(pipeline)

        total = db.notes.count_documents(match_stage)
        notes_list = list(notes)
        Common.make_JSON_serializable(Common, notes_list)
        
        return jsonify({
            'data': notes_list,
            'per_page': per_page,
            'current_page': page_number,
            'total': total
        })

