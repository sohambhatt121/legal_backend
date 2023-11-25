from schema import Schema, And

user_schema = Schema({
    'customer_code': And(str, lambda s: len(s.strip()) > 0),
    'first_name': And(str, lambda s: len(s.strip()) > 0),
    'middle_name': And(str, lambda s: len(s.strip()) >= 0),
    'last_name': And(str, lambda s: len(s.strip()) > 0),
    'address': And(str, lambda s: len(s.strip()) > 0),
    'aadhar_card': And(str, lambda s: len(s.strip()) > 0),
    'phone': And(str, lambda s: len(s.strip()) > 0),
    'email': And(str, lambda s: len(s.strip()) > 0),
    'password': And(str, lambda s: len(s.strip()) > 0),
    'role': And(str, lambda s: len(s.strip()) > 0),
    'status': And(str, lambda s: len(s.strip()) > 0),
})