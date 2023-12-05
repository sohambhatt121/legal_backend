from flask import request
from flask_restful import Resource
from schema import  SchemaError

from database.db import db
from util.authentication import Authentication as Auth
from util.exception import InvalidPassword, InvalidCustomerCode, CustomerInactive, UserNotExist, UserInactive
from datetime import datetime
from util.validation import Validation

class LoginApi(Resource):
    def post(self):
        try:
            data = request.get_json()
            customer_code = data.get('customer_code')
            email = data.get('email')
            password = data.get('password')
            
            Validation.validate_active_customer(customer_code)
            user = db.users.find_one({'customer_code': customer_code, 'email': email})

            existing_token = db.auth_token.find_one({"user_id": str(user['_id'])})
            if existing_token:
                token = existing_token['token']
                return {"message": "Login successful", "token": token}, 200
            
            if Auth.authenticate_user(user, password):
                token = Auth.generate_auth_token(user['_id'])
                return {"message": "Login successful", "token": token}, 200
            else:
                return {"message": "Invalid Password"}, 401
            
        except SchemaError as e:
            return {'error': 'Invalid request data', 'details': str(e)}, 400
        except UserNotExist as e:
            return {'error': str(e)}, 401
        except CustomerInactive as e:
            return {'error': str(e)}, 401
        except InvalidCustomerCode as e:
            return {'error': str(e)}, 404
        except UserInactive as e:
            return {'error': str(e)}, 401
        
    def get(self):
        token = request.headers.get('auth_token')
        if Auth.user_logout(token):
            return {"message": "Logout successful"}, 200
        else:
            return {'error': 'Invalid request'}, 400