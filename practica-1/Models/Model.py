import pymongo

from constants import database as dbK
from constants import models as modelsK
# self.__dict__update(kwargs)
class Model:
    """ Prototipo de la clase modelo
        Copiar y pegar tantas veces como modelos se deseen crear (cambiando
        el nombre Model, por la entidad correspondiente), o bien crear tantas
        clases como modelos se deseen que hereden de esta clase. Este segundo 
        metodo puede resultar mas compleja
    """
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
    def _init_class(cls, db, model_name = ''):
        # se sacan las variables admitidas y requeridas de un archivo separado
        # solo comprobar que existen los datos
        """ Inicializa las variables de clase en la inicializacion del sistema.
        """
        
        cls.db = db
        cls.required_vars = modelsK.MODEL_VARS[model_name][0]
        cls.admissible_vars = modelsK.MODEL_VARS[model_name][1]