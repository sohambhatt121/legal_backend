from util.exception import ExceptionMessages as message
from database.db import db
from bson import ObjectId
import jwt
from datetime import datetime, timedelta
import os

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

    def prepare_filter(self, request):
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
        if request.args.get('case_id'):
            filters['case_id'] = request.args.get('case_id')

        return filters