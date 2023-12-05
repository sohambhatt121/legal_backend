from schema import Schema, And, Or

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
    'role': And(int, Or(1,2,3)),
    'status': And(int, Or(0,1,2))
})

users_role = {
    1: "admin",
    2: "operations_manager",
    3: "employee"
}

users_status = {
    0: "inactive",
    1: "active",
    2: "deleted"
}