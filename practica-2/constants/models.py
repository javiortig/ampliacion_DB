import constants.database as dbK

# indexes are national_id, name and name respectively
MODEL_VARS= {
    # studies = [{'university':'Utad','final':datetime.strptime('19/04/2000', "%d/%m/%Y")}]
    #TODO: como van a ser los jobs
    dbK.DB_PERSON_KEY: [
    ['national_id', 'name', 'last_name', 'age', 'city', 'studies'],
    ['second_name', 'gender', 'jobs']
    ],
    dbK.DB_UNIVERSITY_KEY: [
        ['name', 'cif', 'city'],
        ['age', 'public', 'courses'] # public is a bool. courses is a list []
    ],
    dbK.DB_COMPANY_KEY: [
        ['name', 'cif', 'city'],
        ['age']
    ]
}
