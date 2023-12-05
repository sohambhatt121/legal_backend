from schema import Schema, And, Or

customer_schema = Schema({
    'customer_code': And(str, lambda s: len(s.strip()) > 0),
    'name': And(str, lambda s: len(s.strip()) > 0),
    'address': And(str, lambda s: len(s.strip()) > 0),
    'contact': {
        'name': And(str, lambda s: len(s.strip()) > 0),
        'phone': And(str, lambda s: len(s.strip()) > 0),
        'email': And(str, lambda s: len(s.strip()) > 0)
    },
    'status': And(int, Or(0,1,2)),
})

customer_status = {
    0: "inactive",
    1: "active",
    2: "deleted"
}
