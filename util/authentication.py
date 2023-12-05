import os
import bcrypt
from util.exception import NotAdminException, UserInactive, UserNotExist
from database.db import db
import jwt
from datetime import datetime, timedelta


class Authentication():
    def check_admin_access(token):
        if token == os.getenv("ADMIN_KEY"):
            return True
        else:
            raise NotAdminException("User is not an admin")
        
    def validate_token(token):
        if token == os.getenv("ADMIN_KEY"):
            return True
        
        user = db.auth_token.find_one({'token': token})

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



        
