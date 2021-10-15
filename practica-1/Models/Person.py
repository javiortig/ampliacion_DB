import pymongo

# self.__dict__update(kwargs)
class Model:
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
    def find(cls, filter) -> ModelCursor:
        """ Devuelve un cursor de modelos        
        """ 
        #TODO
        # cls es el puntero a la clase
        pass #No olvidar eliminar esta linea una vez implementado

    @classmethod
    def init_class(cls, db, vars_path="model_name.vars"):
        # se sacan las variables admitidas y requeridas de un archivo separado
        # solo comprobar que existen los datos
        """ Inicializa las variables de clase en la inicializacion del sistema.
        Argumentos:
            db (MongoClient) -- Conexion a la base de datos.
            vars_path (str) -- ruta al archivo con la definicion de variables
            del modelo.
        """
        #TODO
        # cls es el puntero a la clase
        pass