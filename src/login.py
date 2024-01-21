from flask import request
from flask_restful import Resource
from schema import  SchemaError
from bson import ObjectId
import os

from database.db import db
from util.authentication import Authentication as Auth
from util.exception import ExceptionMessages as message
from datetime import datetime
from util.validation import Validation
from util.common import Common
import jwt
from datetime import datetime, timedelta


class LoginApi(Resource):
    def post(self):
        try:
            data = request.get_json()
            customer_code = data.get('customer_code')
            email = data.get('email')
            password = data.get('password')
            
            Validation.validate_active_customer(Validation, customer_code)
            user = db.users.find_one({'customer_code': customer_code, 'email': email})
            if user is None:
                return {"message": "Invalid user credentials"}, 401
            
            # this line is for not allowing multiple login
            #x = db.auth_token.delete_many({"user_id": str(user['_id'])})
            
            if Auth.authenticate_user(Auth, user, password):
                token = Auth.generate_auth_token(Auth, user['_id'])
                return {"message": "Login successful", "token": token, "user_id": str(user['_id'])}, 200
            else:
                return {"message": "Invalid Password"}, 401
            
        except SchemaError as e:
            return {'error': message.InvalidRequestSchema, 'details': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 401
        
    def delete(self):
        token = request.headers.get('authToken')
        if Auth.user_logout(Auth, token):
            return {"message": "Logout successful"}, 200
        else:
            return {'error': 'Invalid request'}, 400
        
class ForgotPasswordApi(Resource):
    def get(self, email):
        try:
            user = db.users.find_one({"email": email})
            if not user:
                raise Exception("Invalid User Email")
            
            key = Helper.generate_forgot_password_key(Helper, user['_id'])
            return {"message": "Forgot Password Key", "key": key}, 200

        except Exception as e:
            return {'error': str(e)}, 401
        
class ResetPasswordApi(Resource):
    def post(self):
        try:
            data = request.get_json()
            key = data.get('key')
            new_password = data.get('password')
            user_id = Common.user_id_from_token(Common, key)
            if user_id:
                user = db.users.find_one({"_id": ObjectId(user_id)})
                result = Helper.reset_password(Helper, user_id, user, new_password)
                if result.modified_count == 1:
                    Auth.delete_user_login(Auth, user_id)
                    Helper.delete_forgot_password_key(Helper, key)
                    return {'message': 'Password updated successfully'}, 200
                else:
                    return {'error': 'Error in updating password'}, 400
            else:
                raise Exception(message.UserNotExist)
        except SchemaError as e:
            return {'error': message.InvalidRequestSchema, 'details': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 401
        
class ChangePasswordApi(Resource):
    def put(self, id):
        try:
            user_id = Auth.validate_token(Auth, request.headers.get('authToken'))
            data = request.get_json()
            new_password = data.get('password')

            if user_id != id:
                return {'error': 'Invalid user id'}, 400
            
            user = db.users.find_one({"_id": ObjectId(id)})
            result = Helper.reset_password(Helper, id, user, new_password)
            if result.modified_count == 1:
                Auth.user_logout(Auth, request.headers.get('authToken'))
                return {'message': 'Password updated successfully'}, 200
            else:
                return {'error': 'Error in updating password'}, 400
        except SchemaError as e:
            return {'error': message.InvalidRequestSchema, 'details': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 401
        
class Helper():
    def generate_forgot_password_key(self, user_id):
        key = jwt.encode({
                    'user_id': str(user_id),
                    'exp': datetime.utcnow() + timedelta(hours=24)
                }, os.getenv("SECRET_KEY"), algorithm='HS256')
        
        body = {}
        body['user_id'] = str(user_id)
        body['key'] = key
        body['exp_time'] = datetime.utcnow() + timedelta(hours=24)
        db.forgot_password.insert_one(body)
        return key
    
    def reset_password(self, user_id, user, new_password):
        if user:
            user['password'] = Auth.hash_password(Auth, new_password)
            user['updated_at'] = datetime.now()
            if '_id' in user:
                del user['_id']
            
            result = db.users.update_one({'_id': ObjectId(user_id)}, {'$set': user})
            return result
        else:
            raise Exception(message.UserNotExist)
        
    def delete_forgot_password_key(self, key):
        result = db.forgot_password.delete_many({'key': key})
        if result.deleted_count > 0:
            return True
        return False
        