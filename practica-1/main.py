__author__ = 'Nombres_y_Apellidos'

from pymongo import MongoClient
import constants.database as dbK
from Models.Model import Model

if __name__ == '__main__':
    #TODO
    # primero conectar la base de datos y pasarla a los 3 modelos en el init_class
    # ejecutar los 3 init_class
    # las consultas todas con aggregate

    client = MongoClient(dbK.DB_ADDRESS, dbK.DB_PORT)
    db = client[dbK.DB_NAME]

    # Initializate the models:
    Model._init_class(db, dbK.DB_PERSON_KEY) # Person
    
    pass #No olvidar eliminar esta linea una vez implementado

