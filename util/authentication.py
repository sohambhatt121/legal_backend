import os
import bcrypt
from util.exception import InvaliAuthToken
from util.exception import ExceptionMessages as message
from database.db import db
from util.validation import Validation
import jwt
from datetime import datetime, timedelta
from bson import ObjectId


class Authentication():
    def check_admin_access(self, token):
        temp = os.getenv("ADMIN_KEY")
        if token == os.getenv("ADMIN_KEY"):
            return True
        else:
            raise Exception(message.NotAdminException)
        
    def validate_token(self, token):
        try:
            if token == os.getenv("ADMIN_KEY"):
                return True
            
            token_details = db.auth_token.find_one({'token': token})
            if token_details is None:
                raise InvaliAuthToken(message.InvaliAuthToken)
            
            decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
            user_id = decoded_token.get('user_id')
            return user_id
                
        except InvaliAuthToken as e:
            raise Exception(message.InvaliAuthToken)
        except Exception as e:
            raise Exception(message.AuthTokenExpired)
        

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
    
    def verify_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    
    def authenticate_user(self, user, password):
        if user:
            if user['status'] != 1:
                raise Exception(message.UserInactive)
            
            return bcrypt.checkpw(password.encode('utf-8'), user['password'])
        else:
            raise Exception(message.UserNotExist)
        
    def generate_auth_token(self, user_id):
        token = jwt.encode({
                    'user_id': str(user_id),
                    'exp': datetime.utcnow() + timedelta(hours=24)
                }, os.getenv("SECRET_KEY"), algorithm='HS256')
        
        body = {}
        body['user_id'] = str(user_id)
        body['token'] = token
        body['exp_time'] = datetime.utcnow() + timedelta(hours=24)
        db.auth_token.insert_one(body)
        return token
    
    def user_logout(self, token):
        decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
        #user_id = decoded_token.get('user_id')
        result = db.auth_token.delete_many({'token': token})
        if result.deleted_count > 0:
            return True
        return False
    
    def delete_user_login(self, user_id):
        result = db.auth_token.delete_many({'user_id': ObjectId(user_id)})
        if result.deleted_count > 0:
            return True
        return False




        
