
from db import *
role = {'entity_class': Role,
        'attributes': [
            {'name': 'id',
             'class': None,
             'relationship': 'one'},
            {'name': 'name',
             'class': None,
             'relationship': 'one'},
            ]}


roles = role

entity_pairs = {
    'roles': role
}
