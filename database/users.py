from schema import Schema, And, Or, Optional

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

update_user_schema = Schema({
    Optional('customer_code'): And(str, lambda s: len(s.strip()) > 0),
    Optional('first_name'): And(str, lambda s: len(s.strip()) > 0),
    Optional('middle_name'): And(str, lambda s: len(s.strip()) > 0),
    Optional('last_name'): And(str, lambda s: len(s.strip()) > 0),
    Optional('address'): And(str, lambda s: len(s.strip()) > 0),
    Optional('aadhar_card'): And(str, lambda s: len(s.strip()) > 0),
    Optional('phone'): And(str, lambda s: len(s.strip()) > 0),
    Optional('email'): And(str, lambda s: len(s.strip()) > 0),
    Optional('role'): And(int, Or(1,2,3)),
    Optional('status'): And(int, Or(0,1,2))
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