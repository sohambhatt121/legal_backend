from .exception import CustomerInactive, InvalidCustomerCode, UserInactive, UserNotExist
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
            raise UserNotExist("User not exist")