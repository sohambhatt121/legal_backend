from flask import request
from flask_restful import Resource
from schema import  SchemaError
from bson import ObjectId
from flask import jsonify

import uuid
import magic
import mimetypes
from database.db import db
from database.docs import doc_schema, update_doc_schema
from util.authentication import Authentication as Auth
from util.exception import ExceptionMessages as message
from datetime import datetime
from util.validation import Validation
from util.common import Common
from util.s3_client import S3_Client

class DocApi(Resource):
    def get(self):
        try: 
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            customer_code = request.args.get('customer_code')
            user_customer_code = Common.get_customer_by_user(Common, user_id)
            if customer_code != user_customer_code:
                raise Exception(message.UnauthorizedUser)
            
            return Helper.list_documents(Helper, request)
        except Exception as e:
            return {'error': str(e)}, 401

    def post(self):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            body = Helper.get_post_request_body(Helper, request)
            doc_schema.validate(body)
            file = request.files['document']
            if file is None:
                return {'error': message.FileUploadFail, 'details': str(e)}, 400
            
            Validation.validate_active_customer(Validation, body['customer_code'])
            Validation.validate_user_customer_relation(Validation, user_id, body['customer_code'])

            file_extension = file.filename.rsplit('.', 1)
            if len(file_extension) > 1:
                file_name = f"{str(uuid.uuid4())}.{file_extension[1]}"
            else:
                file_name = f"{str(uuid.uuid4())}"
            folder_name = f"documents/{body['case_id']}"

            file_type = Helper.get_file_content_type(file)

            S3_Client.upload(S3_Client, file, folder_name, file_name, file_type)
            body['file_url'] = f"{folder_name}/{file_name}"
            body['added_by'] = user_id
            body['created_at'] = datetime.now()
            body['updated_at'] = datetime.now()

            doc = db.docs.insert_one(body)
            return {'message': 'Document added successfully', "id": str(doc.inserted_id)}, 201
        except SchemaError as e:
            return {'error': message.InvalidRequestSchema, 'details': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 401
        
class DocsApi(Resource):
    def put(self, id):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            body = Helper.get_put_request_body(Helper, request)
            update_doc_schema.validate(body)
            file = None
            if 'document' in request.files:
                file = request.files['document']
            
            data = db.docs.find_one({'_id': ObjectId(id)})
            if data:
                Validation.validate_user_customer_relation(Validation, user_id, data['customer_code'])
            else:
                return {'error': message.DocumentNotExist}, 404
            
            body['updated_at'] = datetime.now()
            
            if file:
                old_file = data['file_url']
                file_extension = file.filename.rsplit('.', 1)
                if len(file_extension) > 1:
                    file_name = f"{str(uuid.uuid4())}.{file_extension[1]}"
                else:
                    file_name = f"{str(uuid.uuid4())}"
                
                if 'case_id' in body:
                    folder_name = f"documents/{body['case_id']}"
                else:
                    folder_name = f"documents/{data['case_id']}"
                
                S3_Client.upload(S3_Client, file, folder_name, file_name)
                S3_Client.delete(S3_Client, old_file)
                body['file_url'] = f"{folder_name}/{file_name}"
            
            result = db.docs.update_one({'_id': ObjectId(id)}, {'$set': body})           
            if result.modified_count == 1:
                return {'message': 'Document updated successfully'}, 200
            else:
                return {'error': message.DocumentNotExist}, 404
        
        except SchemaError as e:
            return {'error': message.InvalidRequestSchema, 'details': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 401
    
    def delete(self, id):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            data = db.docs.find_one({'_id': ObjectId(id)})
            if data:
                Validation.validate_active_customer(Validation, data['customer_code'])
                Validation.validate_user_customer_relation(Validation, user_id, data['customer_code'])
            else:
                return {'error': message.DocumentNotExist}, 404
            
            S3_Client.delete(S3_Client, data['file_url'])
            result = db.docs.delete_one({'_id': ObjectId(id)})
            if result.deleted_count == 1:
                return {'message': 'Document deleted successfully'}, 200
            else:
                return {'error': message.DocumentNotExist}, 404
        except Exception as e:
            return {'error': str(e)}, 401

    def get(self, id):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            data = db.docs.find_one({'_id': ObjectId(id)})
            
            if data:
                Validation.validate_user_customer_relation(Validation, user_id, data['customer_code'])
                case_data = db.cases.find_one({'_id': ObjectId(data['case_id'])})
                data['case_title'] = case_data['title'] if case_data else ''
                data['_id'] = str(data['_id'])
                data['created_at'] = str(data['created_at'])
                data['updated_at'] = str(data['updated_at'])
                return {'data': data}, 200
            else:
                return {'error': message.DocumentNotExist}, 404
        except Exception as e:
            return {'error': str(e)}, 401

class AccessDocs(Resource):
    def get(self, id):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            data = db.docs.find_one({'_id': ObjectId(id)})
            if not data:
                return {'error': message.DocumentNotExist}, 404

            url = S3_Client.get_access(S3_Client, data['file_url'], 3600)
            return {'url': url}, 200 

        except Exception as e:
            return {'error': str(e)}, 401

class Helper():
    def get_post_request_body(self, request):
        body = {}
        body['title'] = request.form['title']
        body['note'] = request.form['note']
        body['customer_code'] = request.form['customer_code']
        body['case_id'] = request.form['case_id']
        return body
    
    def get_put_request_body(self, request):
        body = {}
        if 'title' in request.form and request.form['title'] != "":
            body['title'] = request.form['title']
        if 'note' in request.form and request.form['note'] != "":
            body['note'] = request.form['note']
        if 'case_id' in request.form and request.form['case_id'] != "":
            body['case_id'] = request.form['case_id']
        return body
    
    def get_file_content_type(file):
        specific_content_type, _ = mimetypes.guess_type(file.filename)
        if specific_content_type:
            return specific_content_type
        else:
            raise Exception(message.FileTypeNotAllowed)

    def list_documents(self, request):
        per_page = int(request.args.get('per_page', 10))
        page_number = int(request.args.get('page_number', 1))
        sort_by = request.args.get('sort_by', '_id')
        order = request.args.get('order', 'asc')

        match_stage = Common.prepare_filter(Common, request, db.docs)

        pipeline = [
            { '$match': match_stage},
            {
                '$addFields': {
                    'case_id_ObjectId': {
                        '$toObjectId': '$case_id'
                    }
                }
            },
            {
                '$lookup': {
                    'from': 'cases',
                    'localField': 'case_id_ObjectId',
                    'foreignField': '_id',
                    'as': 'case_info'
                }
            },
            {
                '$unwind': '$case_info'
            },
            {
                '$project': {
                    '_id': 1,
                    'title': 1,
                    'note': 1,
                    'case_title': '$case_info.title',
                    'customer_code': 1,
                    'case_id': 1,
                    'added_by': 1,
                    'created_at': 1,
                    'updated_at': 1,
                    'file_url': 1
                }
            },
            {'$sort': {sort_by: 1 if order == 'asc' else -1}},
            {'$skip': (page_number - 1) * per_page},
            {'$limit': per_page}
        ]

        documents = db.docs.aggregate(pipeline)

        total = db.docs.count_documents(match_stage)
        document_list = list(documents)
        Common.make_JSON_serializable(Common, document_list)
        
        return jsonify({
            'data': document_list,
            'per_page': per_page,
            'current_page': page_number,
            'total': total
        })

