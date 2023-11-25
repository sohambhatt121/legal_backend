from .customers import CustomersApi, CustomerApi, CustomerCodeApi

def initialize_routes(api):
    api.add_resource(CustomersApi, '/api/v1/customer')
    api.add_resource(CustomerApi, '/api/v1/customer/<id>')
    api.add_resource(CustomerCodeApi, '/api/v1/customer_code/<id>')