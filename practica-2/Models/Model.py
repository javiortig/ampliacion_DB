import pymongo
from pprint import pprint
from typing import Union

from constants import database as dbK
from constants import models as modelsK

from Models.ModelCursor import ModelCursor

#TODO: poder crear empty Model.
class Model:
    """ Prototipo de la clase modelo
        Copiar y pegar tantas veces como modelos se deseen crear (cambiando
        el nombre Model, por la entidad correspondiente), o bien crear tantas
        clases como modelos se deseen que hereden de esta clase. Este segundo 
        metodo puede resultar mas compleja
    """
    required_vars = set()
    admissible_vars = set()
    db = None
    collection = None
    index = ''

    def __init__(self, **kwargs): # 
        kwargs.pop(dbK.MONGO_ID_STR, None)
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
    # All queries here are O(1)
    def save(self): 
        # Check if self.data contains city:
        # We will use this to save as many API calls as possible. 
        if dbK.DB_CITY_KEY in self.data:
            #check if city exists in city collection. If it doesn't, insert it
            #TODO: terminar de comprobar que funciona bn
            query = {dbK.DB_CITY_NAME_STR: self.data[dbK.DB_CITY_KEY]}
            res = self.db[dbK.DB_CITY_KEY].find_one(query)
            if (not res):
                # If no city in collection, we have no choice but to call the API
                coordinates = getCityGeoJSON(self.data[dbK.DB_CITY_KEY])

                self.db[dbK.DB_CITY_KEY].insert_one({
                    dbK.DB_CITY_NAME_STR: self.data[dbK.DB_CITY_KEY],
                    dbK.DB_CITY_LOCATION_STR: {
                        dbK.MONGO_TYPE_STR: dbK.MONGO_TYPE_POINT_STR, 
                        dbK.MONGO_TYPE_COORDINATES_STR: coordinates
                    }
                })

        # Check if exists in document
        query = {self.index: self.data[self.index]}
        res = self.collection.find_one(query)

        # Inserts object if it doesnt exist
        if(not res):
            # insert_one modifies self.data
            er = self.collection.insert_one(self.data)
            print("inserto mongo")
        # If exists, update only the modified fields
        else:
            query_values = {k:v for (k,v) in self.data.items() if k in self.modified_data}
            #res = self.collection.update_one(query, {'$set': query_values})
            self.data = self.collection.find_one_and_update(
                query, 
                {'$set': query_values},
                return_document=pymongo.ReturnDocument.AFTER
            )
            print("updateo mongo")

        
        self.data.pop(dbK.MONGO_ID_STR)
        
    def set(self, **kwargs): # No guardan en la base de datos
        self._filter(full=False, **kwargs)
        
        self.modified_data = list(kwargs.keys())
        self.data.update(kwargs)

    def print(self):
        print(self.data)
    
    # Loads an existing model from the collection
    @classmethod
    def load(cls, index) ->Union['Model', None]:
        query = {cls.index: index}
        res = cls.collection.find_one(query)
        return cls(**res) if res else None

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
        """ Inicializa las variables de clase en la inicializacion del sistema.
        """
        cls.db = db
        cls.collection = db[model_name]
        cls.required_vars = set(modelsK.MODEL_VARS[model_name][0])
        cls.admissible_vars = set(modelsK.MODEL_VARS[model_name][1])

        # Creates an index in the collection if not exists
        cls.index = modelsK.MODEL_VARS[model_name][0][0]
        cls.collection.create_index(cls.index, unique=True)


def getCityGeoJSON(address):
    """ Devuelve las coordenadas de una direcciion a partir de un str de la direccion
    Cuidado, la API tiene un limite de peticiones.
    Argumentos:
        address (str) -- Direccion
    Return:
        (str) -- GeoJSON
    """
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="geocoder")
    location = geolocator.geocode(address)
    if (not location):
        raise Exception('Invalid location name')
    return [location.latitude,location.longitude]
