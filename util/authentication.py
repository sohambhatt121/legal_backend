import os
import bcrypt
from util.exception import NotAdminException, UserInactive, UserNotExist, AuthTokenExpired, InvaliAuthToken
from database.db import db
from util.validation import Validation
import jwt
from datetime import datetime, timedelta
from bson import ObjectId


class Authentication():
    def check_admin_access(token):
        temp = os.getenv("ADMIN_KEY")
        if token == os.getenv("ADMIN_KEY"):
            return True
        else:
            raise NotAdminException("User is not an admin " + str(temp) + str(token))
        
    def validate_token(token):
        if token == os.getenv("ADMIN_KEY"):
            return True
        
        token_details = db.auth_token.find_one({'token': token})
        if token_details:
            decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
            user_id = decoded_token.get('user_id')
            token_exp = decoded_token.get('exp')
            current_time = datetime.utcnow()
            Validation.validate_active_user(user_id)
            if current_time < datetime.utcfromtimestamp(token_exp):
                return user_id
            else:
                raise AuthTokenExpired("Token has expired")
        else:
            raise InvaliAuthToken("Invalid Auth Token")

    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
    
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    
    def authenticate_user(user, password):
        if user:
            if user['status'] != 1:
                raise UserInactive("User is not active")
            
            return bcrypt.checkpw(password.encode('utf-8'), user['password'])
        else:
            raise UserNotExist("User Not Exist")
        
    def generate_auth_token(user_id):
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
    
    def user_logout(token):
        decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
        #user_id = decoded_token.get('user_id')
        result = db.auth_token.delete_many({'token': token})
        if result.deleted_count > 0:
            return True
        return False
    
    def delete_user_login(user_id):
        result = db.auth_token.delete_many({'user_id': ObjectId(user_id)})
        if result.deleted_count > 0:
            return True
        return False




        
