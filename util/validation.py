from .exception import CustomerInactive, InvalidCustomerCode, UserInactive, UserNotExist, ClientInactive, ClientNotExist
from database.db import db
from bson import ObjectId

class Validation():
    def validate_active_customer(self, customer_code):
        customer = db.customers.find_one({'customer_code': customer_code})
        if customer:
            if customer['status'] == 1:
                return True
            else:
                raise CustomerInactive("Customer is Inactive")
        else:
            raise InvalidCustomerCode("Invalid Customer Code")
        
    def validate_active_user(self, user_id):
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            if user['status'] == 1:
                return True
            else:
                raise UserInactive("Customer is Inactive")
        else:
            raise UserNotExist("Invalid Customer Code")
        
    def validate_user_customer_relation(self, user_id, customer_code):
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            if user['status'] != 1:
                raise UserInactive("User is Inactive")
            elif user['customer_code'] != customer_code:
                raise InvalidCustomerCode("Unauthorized User")
            else:
                return True
        else:
            raise UserNotExist("User not exist")
        
    def validate_active_client(self, client_id):
        client = db.clients.find_one({"_id": ObjectId(client_id)})
        if client:
            if client['status'] == 1:
                return True
            else:
                raise ClientInactive("Client is Inactive")
        else:
            raise ClientNotExist("Client not exist")