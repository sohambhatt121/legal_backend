from .customers import CustomersApi, CustomerApi, CustomerCodeApi
from .users import UserApi, UsersApi
from .login import LoginApi

def initialize_routes(api):

    # customer model
    api.add_resource(CustomersApi, '/api/v1/customer')
    api.add_resource(CustomerApi, '/api/v1/customer/<id>')
    api.add_resource(CustomerCodeApi, '/api/v1/customer_code/<id>')

    #user model
    api.add_resource(UsersApi, '/api/v1/user')
    api.add_resource(UserApi, '/api/v1/user/<id>')

    #login model
    api.add_resource(LoginApi, '/api/v1/login')