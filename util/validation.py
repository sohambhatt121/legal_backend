from util.exception import ExceptionMessages as message
from database.db import db
from bson import ObjectId

class Validation():
    def validate_active_customer(self, customer_code):
        customer = db.customers.find_one({'customer_code': customer_code})
        if customer:
            if customer['status'] == 1:
                return True
            else:
                raise Exception(message.CustomerInactive)
        else:
            raise Exception(message.InvalidCustomerCode)
        
    def validate_active_user(self, user_id):
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            if user['status'] == 1:
                return True
            else:
                raise Exception(message.CustomerInactive)
        else:
            raise Exception(message.InvalidCustomerCode)
        
    def validate_user_customer_relation(self, user_id, customer_code):
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            if user['status'] != 1:
                raise Exception(message.UserInactive)
            elif user['customer_code'] != customer_code:
                raise Exception(message.UnauthorizedUser)
            else:
                return True
        else:
            raise Exception(message.UserNotExist)
        
    def validate_active_client(self, client_id):
        client = db.clients.find_one({"_id": ObjectId(client_id)})
        if client:
            if client['status'] == 1:
                return True
            else:
                raise Exception(message.ClientInactive)
        else:
            raise Exception(message.ClientNotExist)