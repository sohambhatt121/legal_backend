from util.exception import ExceptionMessages as message
from database.db import db
from bson import ObjectId
import jwt
from datetime import datetime, timedelta
import os
from flask import jsonify

class Common():
    def user_id_from_token(self, token):
        decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        if user_id:
            return user_id
        else:
            return False
        
    def get_customer_by_user(self, user_id):
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            return user['customer_code']
        else:
            raise Exception(message.UserNotExist)
        
    def make_JSON_serializable(self, data):
        for item in data:
            item['_id'] = str(item['_id'])
            item['created_at'] = str(item['created_at'])
            item['updated_at'] = str(item['updated_at'])
            
            if 'password' in item:
                del item['password']

    def prepare_filter(self, request, collection):
        filters = {}
        if request.args.get('client_id'):
            filters['client_id'] = request.args.get('client_id')
        if request.args.get('added_by'):
            filters['added_by'] = request.args.get('added_by')
        if request.args.get('opposition_name'):
            filters['opposition.name'] = request.args.get('opposition_name')
        if request.args.get('opposition_lawyer_name'):
            filters['opposition_lawyer.name'] = request.args.get('opposition_lawyer_name')
        if request.args.get('court_type'):
            filters['court_type'] = int(request.args.get('court_type'))
        if request.args.get('customer_code'):
            filters['customer_code'] = request.args.get('customer_code')
        if request.args.get('case_type'):
            filters['case_type'] = int(request.args.get('case_type'))
        if request.args.get('status'):
            filters['status'] = int(request.args.get('status'))
        if request.args.get('client_type'):
            filters['client_type'] = int(request.args.get('client_type'))
        if request.args.get('role'):
            filters['role'] = int(request.args.get('role'))
        if request.args.get('case_id'):
            filters['case_id'] = request.args.get('case_id')
        if request.args.get('name'):
            filters['name'] = request.args.get('name')
        if request.args.get('contact_name'):
            filters['contact.name'] = request.args.get('contact_name')
        if request.args.get('contact_person_name'):
            filters['contact_person.name'] = request.args.get('contact_person_name')

        if 'status' in filters:
            if filters['status'] == -1:
                filters['status'] = {'$ne': 2}
            elif filters['status'] == -2:
                del filters['status']
        else:
            if collection in [db.users, db.clients, db.customers, db.cases]:
                filters['status'] = 1

        if 'role' in filters:
            if filters['role'] == 4:
                del filters['role']

        if 'client_type' in filters:
            if filters['client_type'] == 3:
                del filters['client_type']

        return filters
    
    def get_list(self, request, collection):
        per_page = int(request.args.get('per_page', 10))
        page_number = int(request.args.get('page_number', 1))
        sort_by = request.args.get('sort_by', '_id')
        order = request.args.get('order', 'asc')

        match_stage = self.prepare_filter(self, request, collection)
        
        pipeline = [
            {'$match': match_stage},
            {'$sort': {sort_by: 1 if order == 'asc' else -1}},
            {'$skip': (page_number - 1) * per_page},
            {'$limit': per_page}
        ]

        data = collection.aggregate(pipeline)
        total = collection.count_documents(match_stage)
        data_list = list(data)
        self.make_JSON_serializable(self, data_list)
        
        return jsonify({
            'data': data_list,
            'per_page': per_page,
            'current_page': page_number,
            'total': total
        })