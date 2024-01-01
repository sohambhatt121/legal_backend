from schema import Schema, And, Or, Optional

client_schema = Schema({
    'customer_code': And(str, lambda s: len(s.strip()) > 0),
    'name': And(str, lambda s: len(s.strip()) > 0),
    'address': And(str, lambda s: len(s.strip()) > 0),
    'contact_person': {
        'name': And(str, lambda s: len(s.strip()) > 0),
        'phone': And(str, lambda s: len(s.strip()) > 0),
        'email': And(str, lambda s: len(s.strip()) > 0),
        'aadhar_card': And(str, lambda s: len(s.strip()) >= 0),
    },
    'client_type': And(int, Or(1,2)),
    'status': And(int, Or(0,1,2))
})

update_client_schema = Schema({
    Optional('name'): And(str, lambda s: len(s.strip()) > 0),
    Optional('address'): And(str, lambda s: len(s.strip()) > 0),
    Optional('contact_person'): {
        'name': And(str, lambda s: len(s.strip()) > 0),
        'phone': And(str, lambda s: len(s.strip()) > 0),
        'email': And(str, lambda s: len(s.strip()) > 0),
        'aadhar_card': And(str, lambda s: len(s.strip()) >= 0),
    },
    Optional('client_type'): And(int, Or(1,2)),
    Optional('status'): And(int, Or(0,1,2))
})

client_type = {
    1: "individual",
    2: "corporate"
}

client_status = {
    0: "inactive",
    1: "active",
    2: "deleted"
}