from collections import namedtuple

DB_PERSON_KEY = 'person'
DB_UNIVERSITY_KEY = 'university'
DB_COMPANY_KEY = 'company'

DB_PORT = 27017
DB_ADDRESS = 'localhost'
DB_NAME = 'redES' 

# studies obligatoria y jobs(trabajo) opcional
_Model_vars_class =  namedtuple('_Model_vars_class', ['required_vars', 'admissible_vars'])
MODEL_CONSTANTS = dict()
MODEL_CONSTANTS[DB_PERSON_KEY] = _Model_vars_class(
    ['name', 'last_name', 'id', 'age', 'address', 'studies'],
    ['second_name', 'gender', 'jobs']
)

#MODEL_CONSTANTS[DB_PERSON_KEY].admissible_vars = 
