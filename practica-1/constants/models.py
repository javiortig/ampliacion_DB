import constants.database as dbK

# studies obligatoria y jobs(trabajo) opcional
# [0]:required. [1]:admissible
# TODO: mirar segun las consultas que es lo más eficiente. Ex: añadir un 
# de teachers en la collection university o consultarlo desde la de persons...
# yo creo que hay que añadir una lista de ids de las otras colleciones sino las
# queries seran muy lentas

MODEL_VARS= {
    dbK.DB_PERSON_KEY: [
    ['name', 'last_name', 'national_id', 'age', 'address', 'studies'],
    ['second_name', 'gender', 'jobs']
    ],
    dbK.DB_UNIVERSITY_KEY: [
        ['name', 'address', 'cif'],
        ['age', 'teachers', 'students']
    ],
    dbK.DB_COMPANY_KEY: [
        ['name', 'address', 'cif'],
        ['age', 'workers', 'shareholders']
    ]
}

juan = {'name': "Juan",
        'national_id': 55423423,
        'studies': [
            {
                'fecha_inicio': 123312,
                'fecha_fin': 2332,
                'course name': 'data'
                id: saddassd
            }
        ]}