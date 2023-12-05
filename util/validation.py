from .exception import CustomerInactive, InvalidCustomerCode
from database.db import db

class Validation():
    
    def validate_active_customer(customer_code):
        customer = db.customers.find_one({'customer_code': customer_code})
        if customer:
            if customer['status'] == 1:
                return True
            else:
                raise CustomerInactive("Customer is Inactive")
        else:
            raise InvalidCustomerCode("Invalid Customer Code")