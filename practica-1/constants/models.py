import constants.database as dbK


# TODO: mirar segun las consultas que es lo más eficiente. Ex: añadir un 
# de teachers en la collection university o consultarlo desde la de persons...
# yo creo que hay que añadir una lista de ids de las otras colleciones sino las
# queries seran muy lentas

# indexes are national_id, name and name respectively
MODEL_VARS= {
    # studies = [{'university':'Utad','final':'ISODate("2015-04-02T01:23:40Z'}]
    dbK.DB_PERSON_KEY: [
    ['national_id', 'name', 'last_name', 'age', 'city', 'studies'],
    ['second_name', 'gender', 'jobs']
    ],
    dbK.DB_UNIVERSITY_KEY: [
        ['name', 'cif', 'city' ],
        ['age', 'teachers', 'students']
    ],
    dbK.DB_COMPANY_KEY: [
        ['name', 'cif', 'city'],
        ['age', 'workers', 'shareholders']
    ]
}
