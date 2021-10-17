__author__ = 'Javier_Orti__Ekaitz'

from pymongo import MongoClient, collection

import constants.database as dbK

from Models.Person import Person
from Models.University import University
from Models.Company import Company

models = [Person, University, Company]

if __name__ == '__main__':
    #TODO
    # primero conectar la base de datos y pasarla a los 3 modelos en el init_class
    # ejecutar los 3 init_class
    # las consultas todas con aggregate

    client = MongoClient(dbK.DB_ADDRESS, dbK.DB_PORT)
    db = client[dbK.DB_NAME]

    # Initializate the models:
    for m in models:
        m._init_class(db)
    
    datos = {
        'name': 'Javi',
        'last_name': 'Orti',
        'national_id': '12312x'
    }

    javi = Person(
        name = 'Javi',
        last_name ='Orti',
        gender = 'm',
        national_id = 22333123,
        age=1, 
        city = 'Huelva',
        studies = 'mates',
        #inventao= 2
    )

    javi.print()



# Comprobamos que funcionó
    # for m in models:
    #     print(m.required_vars)
    #     print(m.admissible_vars)

    # print("Empieza aca\n")
    # javi = Person()
    # javi.set()

    # # print(javi.admissible_vars)

    # # col = db['person']
    # # colFind = col.find({'author':'Juan'})
    # # for x in colFind:
    # #     print(x)
    # #     type(x)
    
    # # print(colFind)

    # Q1 = db['person'].find({'address':'Huelva'})
    # for x in Q1:
    #     print(x)
    #     type(x)

