from schema import Schema, And, Or, Optional

case_schema = Schema({
    'customer_code': And(str, lambda s: len(s.strip()) > 0),
    'client_id': And(str, lambda s: len(s.strip()) > 0),
    'title': And(str, lambda s: len(s.strip()) > 0),
    'Description': And(str, lambda s: len(s.strip()) > 0),
    'case_type' : And(int, Or(1,2,3,4,5,6,7,8)),
    'court_type': And(int, Or(1,2,3,4,5)),
    'status': And(int, Or(0,1,2)),
    Optional('opposition'): {
        Optional('name'): And(str, lambda s: len(s.strip()) > 0),
        Optional('phone'): And(str, lambda s: len(s.strip()) >= 0),
        Optional('email'): And(str, lambda s: len(s.strip()) >= 0),
        Optional('address'): And(str, lambda s: len(s.strip()) >= 0),
        Optional('type'): And(int, Or(1,2))
    },
    Optional('opposition_lawyer'): {
        Optional('name'): And(str, lambda s: len(s.strip()) > 0),
        Optional('phone'): And(str, lambda s: len(s.strip()) >= 0),
        Optional('email'): And(str, lambda s: len(s.strip()) >= 0),
        Optional('address'): And(str, lambda s: len(s.strip()) >= 0),
    }
})

update_case_schema = Schema({
    Optional('client_id'): And(str, lambda s: len(s.strip()) > 0),
    Optional('title'): And(str, lambda s: len(s.strip()) > 0),
    Optional('Description'): And(str, lambda s: len(s.strip()) > 0),
    Optional('case_type'): And(int, Or(1,2,3,4,5,6,7,8)),
    Optional('court_type'): And(int, Or(1,2,3,4,5)),
    Optional('status'): And(int, Or(0,1,2)),
    Optional('opposition'): {
        'name': And(str, lambda s: len(s.strip()) > 0),
        'phone': And(str, lambda s: len(s.strip()) >= 0),
        'email': And(str, lambda s: len(s.strip()) >= 0),
        'address': And(str, lambda s: len(s.strip()) >= 0),
        'type': And(int, Or(0,1,2))
    },
    Optional('opposition_lawyer'): {
        'name': And(str, lambda s: len(s.strip()) > 0),
        'phone': And(str, lambda s: len(s.strip()) >= 0),
        'email': And(str, lambda s: len(s.strip()) >= 0),
        'address': And(str, lambda s: len(s.strip()) >= 0),
    }
})

case_status = {
    0: "inactive",
    1: "active",
    2: "deleted"
}

court_type = {
    1: "Supreme Court of India",
    2: "High Courts",
    3: "District Courts",
    4: "Specialized Courts",
    5: "Tribunals"
}

case_type = {
    1: "Civil Cases",
    2: "Criminal Cases",
    3: "Constitutional Cases",
    4: "Matrimonial Cases",
    5: "Labour and Employment Cases",
    6: "Consumer Disputes",
    7: "Intellectual Property Cases",
    8: "Tax Cases"
}

opposition_type = {
    1: "individual",
    2: "corporate"
}