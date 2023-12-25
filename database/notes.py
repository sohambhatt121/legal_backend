from schema import Schema, And

note_schema = Schema({
    'customer_code': And(str, lambda s: len(s.strip()) > 0),
    'case_id': And(str, lambda s: len(s.strip()) > 0),
    'note': And(str, lambda s: len(s.strip()) >= 0)
})
