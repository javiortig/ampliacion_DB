import pymongo
from pprint import pprint

from constants import database as dbK
from constants import models as modelsK

from Models.ModelCursor import ModelCursor
# self.__dict__update(kwargs)

#TODO: poder crear empty Model.
#TODO: si se intenta crear un modelo que ya existe(existe su index), lanzar un error.
# para ello proporcionar una funcion load que carque un modelo existente
class Model:
    """ Prototipo de la clase modelo
        Copiar y pegar tantas veces como modelos se deseen crear (cambiando
        el nombre Model, por la entidad correspondiente), o bien crear tantas
        clases como modelos se deseen que hereden de esta clase. Este segundo 
        metodo puede resultar mas compleja
    """
    required_vars = set()
    admissible_vars = set()
    collection = None
    index = ''

    # Los filtros deben lanzar una excepcion
    # Se modifica todo a primer nivel
    def __init__(self, **kwargs): # No guardan en la base de datos
        kwargs.pop('_id', None) # Deleetes _id if exists
        self._filter(full=True, **kwargs)
        # Initialize object attributes:
        self.modified_data = list(kwargs.keys())
        self.data = dict()
        self.data.update(kwargs)
        

    # Filters kwargs with required_vars and admissible_vars
    # full= True will check that every required field is met
    def _filter(self, full=False, **kwargs) -> bool:
        args_set = set(kwargs.keys())

        if (full):
            # with set theory we check that |kwargs ∩ required|=|required|
            if (len(args_set & self.required_vars) != len(self.required_vars)):
                raise Exception('missing required variables on argument')
            
            # (args - required)¬⊆(admissible)
            if(not (args_set - self.required_vars).issubset(self.admissible_vars)):
                raise Exception('invalid admisible variables on argument')

        else:
            # (args)¬⊆(required ∪ admissible)
            if(not args_set.issubset(self.required_vars | self.admissible_vars)):
                raise Exception('invalid keys for aruments')

        return True

    # Everytime save is executed, self.data syncs with its corresponding document
    # in the collection
    def save(self): # actualiza en bases de datos unica y exculisavemnte lo que se modifica
        # comprueba si existe la ciudad en citys
        # si existe -> citys.find('Huelva').id
        # no existe ->  
        if (not self.data):
            raise Exception('no data to save on the collection')

        # Check if exists in document
        query = {self.index: self.data[self.index]}
        res = self.collection.find_one(query)
        # Inserts object if it doesnt exist
        if(not res):
            # insert_one modifies self.data
            self.collection.insert_one(self.data)
            print("inserto")
        # If exists, update only the modified fields
        else:
            query_values = {k:v for (k,v) in self.data.items() if k in self.modified_data}
            #res = self.collection.update_one(query, {'$set': query_values})
            self.data = self.collection.find_one_and_update(
                query, 
                {'$set': query_values},
                return_document=pymongo.ReturnDocument.AFTER
            )

        
        self.data.pop('_id')
        
    def set(self, **kwargs): # No guardan en la base de datos
        self._filter(full=False, **kwargs)
        
        self.modified_data = list(kwargs.keys())
        self.data.update(kwargs)

    def print(self):
        print(self.data)

    # def ubicate(self):
    #     #TODO
    #     address = self.ke
    #     return getCityGeoJSON(address)
    #     pass #No olvidar eliminar esta linea una vez implementado
    
    @classmethod
    def load(cls, index):
        #TODO: si alguien quiere cargar un modelo existente de la db
        pass

    @classmethod # classmethod es un metodo estatico. No se llama desde
    # un objeto concreto sino desde Model.find()
    # usar el metodo find de pymongo
    def find(cls, filter) -> ModelCursor:
        """ Devuelve un cursor de modelos        
        """ 
        result_cursor = cls.collection.aggregate(filter)
        return ModelCursor(cls, result_cursor)

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


# TODO: definir geocity()