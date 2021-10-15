__author__ = 'Nombres_y_Apellidos'

from pymongo import MongoClient
import constants
from Models.Model import Model

if __name__ == '__main__':
    #TODO
    # primero conectar la base de datos y pasarla a los 3 modelos en el init_class
    # ejecutar los 3 init_class
    # las consultas todas con aggregate

    client = MongoClient(constants.DB_ADDRESS, constants.DB_PORT)
    db = client[constants.DB_NAME]

    # Initializate the models:
    Model._init_class(db, constants.DB_PERSON_KEY)
    
    pass #No olvidar eliminar esta linea una vez implementado

