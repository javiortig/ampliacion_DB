from pymongo import MongoClient
import datetime
import pprint

"""
año fundacion
num alumnos
num profesores

"""
class Institucion:
    """ Prototipo de la clase modelo
        Copiar y pegar tantas veces como modelos se deseen crear (cambiando
        el nombre Model, por la entidad correspondiente), o bien crear tantas
        clases como modelos se deseen que hereden de esta clase. Este segundo 
        metodo puede resultar mas compleja
    """
    required_vars = []
    admissible_vars = []
    db = None

    def __init__(self, **kwargs):
        #TODO
        pass #No olvidar eliminar esta linea una vez implementado


    def save(self):
        #TODO
        pass #No olvidar eliminar esta linea una vez implementado

    def set(self, **kwargs):
        #TODO
        pass #No olvidar eliminar esta linea una vez implementado
    
    @classmethod
    def find(cls, filter):
        """ Devuelve un cursor de modelos        
        """ 
        #TODO
        # cls es el puntero a la clase
        pass #No olvidar eliminar esta linea una vez implementado

    @classmethod
    def init_class(cls, db, vars_path="model_name.vars"):
        """ Inicializa las variables de clase en la inicializacion del sistema.
        Argumentos:
            db (MongoClient) -- Conexion a la base de datos.
            vars_path (str) -- ruta al archivo con la definicion de variables
            del modelo.
        """
        #TODO
        # cls es el puntero a la clase
        pass #No olvidar eliminar esta linea una vez implementado


client = MongoClient('localhost', 27017)
db = client['redES']

test_collection = db['person']

post = {"author": "Paco",
        "text": "My second blog post!",
        "address": "Haro",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}



test_collection.insert_one(post)

pprint.pprint(test_collection.find_one())

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
    return [location.latitude,location.longitude]

print(getCityGeoJSON("Champ de Mars, Paris, France"))
print(getCityGeoJSON("Huelva"))
