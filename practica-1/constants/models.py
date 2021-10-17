import constants.database as dbK

# studies obligatoria y jobs(trabajo) opcional
# [0]:required. [1]:admissible
# TODO: mirar segun las consultas que es lo más eficiente. Ex: añadir un 
# de teachers en la collection university o consultarlo desde la de persons...
# yo creo que hay que añadir una lista de ids de las otras colleciones sino las
# queries seran muy lentas

# indexes are national_id, cif and cif respectively
MODEL_VARS= {
    dbK.DB_PERSON_KEY: [
    ['national_id', 'name', 'last_name', 'age', 'city', 'studies'],
    ['second_name', 'gender', 'jobs']
    ],
    dbK.DB_UNIVERSITY_KEY: [
        ['cif','name', 'city' ],
        ['age', 'teachers', 'students']
    ],
    dbK.DB_COMPANY_KEY: [
        ['cif', 'name', 'city'],
        ['age', 'workers', 'shareholders']
    ]
}

# juan = {'name': "Juan",
#         'national_id': 55423423,
#         'studies': [
#             {
#                 'fecha_inicio': 123312,
#                 'fecha_fin': 2332,
#                 'course name': 'data'
#                 id: saddassd
#             }
#         ]}