import constants.database as dbK

# indexes are national_id, name and name respectively
MODEL_VARS= {
    # studies = [{'university':'Utad','final':'ISODate("2015-04-02T01:23:40Z'}]
    dbK.DB_PERSON_KEY: [
    ['national_id', 'name', 'last_name', 'age', 'city', 'studies'],
    ['second_name', 'gender', 'jobs']
    ],
    dbK.DB_UNIVERSITY_KEY: [
        ['name', 'cif', 'city' ],
        ['age']
    ],
    dbK.DB_COMPANY_KEY: [
        ['name', 'cif', 'city'],
        ['age']
    ]
}
