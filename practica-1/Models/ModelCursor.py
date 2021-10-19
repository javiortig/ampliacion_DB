from pymongo import command_cursor



class ModelCursor:
    """ Cursor para iterar sobre los documentos del resultado de una
    consulta. Los documentos deben ser devueltos en forma de objetos
    modelo.
    """
    def __init__(self, ModelClass, command_cursor):
        """ Inicializa ModelCursor
        Argumentos:
            model_class (class) -- Clase para crear los modelos del 
            documento que se itera.
            command_cursor (CommandCursor) -- Cursor de pymongo
        """
        self.model_class = ModelClass
        self.command_cursor = command_cursor

    
    def next(self):
        # TODO: 
        if self.command_cursor.alive:
            d = self.command_cursor.next()
            return self.model_class(**d)
        else:
            return None
        """ Devuelve el siguiente documento en forma de modelo
        """

    @property
    def alive(self):
        """True si existen más modelos por devolver, False en caso contrario
        """
        return self.command_cursor.alive
