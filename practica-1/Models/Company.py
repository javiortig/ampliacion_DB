import pymongo

from Models.Model import Model

from constants import models as modelsK
from constants import database as dbK

# self.__dict__update(kwargs)
class Company(Model):
    required_vars = []
    admissible_vars = []
    db = None

    # Los filtros deben lanzar una excepcion
    # Se modifica todo a primer nivel
    def __init__(self, **kwargs): # No guardan en la base de datos
        #TODO
        pass #No olvidar eliminar esta linea una vez implementado


    def save(self): # actualiza en bases de datos unica y exculisavemnte lo que se modifica
        # estas son las querys
        #TODO
        pass #No olvidar eliminar esta linea una vez implementado

    def set(self, **kwargs): # No guardan en la base de datos
        #TODO
        pass #No olvidar eliminar esta linea una vez implementado
    
    @classmethod # classmethod es un metodo estatico. No se llama desde
    # un objeto concreto sino desde Model.find()
    # usar el metodo find de pymongo
    def find(cls, filter):
        """ Devuelve un cursor de modelos        
        """ 
        #TODO
        # cls es el puntero a la clase
        pass #No olvidar eliminar esta linea una vez implementado

    @classmethod
    def _init_class(cls, db):
        super()._init_class(db, model_name=dbK.DB_COMPANY_KEY)