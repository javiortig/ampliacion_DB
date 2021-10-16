__author__ = 'Javier_Orti__Ekaitz'

from pymongo import MongoClient

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
    
    # Comprobamos que funcionó
    for m in models:
        print(m.required_vars)
        print(m.admissible_vars)

    javi = Person()