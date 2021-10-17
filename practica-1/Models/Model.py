import pymongo

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
    db = None
    data = None

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
        pass #No olvidar eliminar esta linea una vez implementado

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
        cls.db = db
        cls.required_vars = set(modelsK.MODEL_VARS[model_name][0])
        cls.admissible_vars = set(modelsK.MODEL_VARS[model_name][1])