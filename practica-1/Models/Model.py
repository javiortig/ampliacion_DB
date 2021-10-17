import pymongo
from pprint import pprint

from constants import database as dbK
from constants import models as modelsK
from Models.ModelCursor import ModelCursor
# self.__dict__update(kwargs)
class Model:
    """ Prototipo de la clase modelo
        Copiar y pegar tantas veces como modelos se deseen crear (cambiando
        el nombre Model, por la entidad correspondiente), o bien crear tantas
        clases como modelos se deseen que hereden de esta clase. Este segundo 
        metodo puede resultar mas compleja
    """
    required_vars = None
    admissible_vars = None
    collection = None
    data = None
    last_data_saved = None # Last data saved on the DB
    index = ''

    # Los filtros deben lanzar una excepcion
    # Se modifica todo a primer nivel
    def __init__(self, **kwargs): # No guardan en la base de datos
        #TODO
        self.set(**kwargs)
        #self.save(kwargs)

    # Filters kwargs with required_vars and admissible_vars
    def _filter(self, **kwargs) -> bool:
        args_set = set(kwargs.keys())
        # with set theory we check that |kwargs ∩ required|=|required|
        if (len(args_set & self.required_vars) != len(self.required_vars)):
            raise Exception('missing required variables on argument')
        
        # (args - required)not⊆(admissible)
        if(not (args_set - self.required_vars).issubset(self.admissible_vars)):
            raise Exception('invalid admisible variables on argument')

        return True


    def save(self): # actualiza en bases de datos unica y exculisavemnte lo que se modifica
        #TODO guardar en la base de datos:
        # si existe objeto -> update
        # si no existe -> save
        if (not self.data):
            raise Exception('no data to save on the collection')

        # Check if exists in document
        res = self.collection.find_one({self.index: self.data[self.index]})
        # Inserts object if it doesnt exist
        if(not res):
            self.collection.insert_one(self.data)

        #TODO finish update


    def set(self, **kwargs): # No guardan en la base de datos
        self._filter(**kwargs)
        self.data = kwargs

    def print(self):
        print(self.data)

    # def ubicate(self):
    #     #TODO
    #     address = self.ke
    #     return getCityGeoJSON(address)
    #     pass #No olvidar eliminar esta linea una vez implementado
    
    @classmethod # classmethod es un metodo estatico. No se llama desde
    # un objeto concreto sino desde Model.find()
    # usar el metodo find de pymongo
    def find(cls, filter) -> ModelCursor:
        """ Devuelve un cursor de modelos        
        """ 
        cursor = cls.db.cars.find(filter)
        return ModelCursor(cls,cursor)

    @classmethod
    def _init_class(cls, db, model_name = ''):
        # se sacan las variables admitidas y requeridas de un archivo separado
        # solo comprobar que existen los datos
        """ Inicializa las variables de clase en la inicializacion del sistema.
        """
        cls.collection = db[model_name]
        cls.required_vars = set(modelsK.MODEL_VARS[model_name][0])
        cls.admissible_vars = set(modelsK.MODEL_VARS[model_name][1])

        # Creates an index in the collection if not exists
        cls.index = modelsK.MODEL_VARS[model_name][0][0]
        cls.collection.create_index(cls.index, unique=True)
