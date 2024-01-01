from schema import Schema, And, Optional

note_schema = Schema({
    'customer_code': And(str, lambda s: len(s.strip()) > 0),
    'case_id': And(str, lambda s: len(s.strip()) > 0),
    'note': And(str, lambda s: len(s.strip()) >= 0)
})

update_note_schema = Schema({
    Optional('case_id'): And(str, lambda s: len(s.strip()) > 0),
    Optional('note'): And(str, lambda s: len(s.strip()) >= 0)
})
