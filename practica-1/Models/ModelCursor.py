from pymongo import command_cursor

class ModelCursor:
    """ Cursor para iterar sobre los documentos del resultado de una
    consulta. Los documentos deben ser devueltos en forma de objetos
    modelo.
    """
#     model_class = None
#     command_cursor = None
    def __init__(self, model_class, command_cursor):
        """ Inicializa ModelCursor
        Argumentos:
            model_class (class) -- Clase para crear los modelos del 
            documento que se itera.
            command_cursor (CommandCursor) -- Cursor de pymongo
        """
        self.model_class = model_class
        self.command_cursor = command_cursor
        pass #No olvidar eliminar esta linea una vez implementado
    
    def __iter__(self):
        return self.model_class.__init__(self.command_cursor)
    
    def next(self):
        """ Devuelve el siguiente documento en forma de modelo
        """
        if(self.alive()):
            return self.model_class.__init__(self.command_cursor)
        else:
            return None
        self.command_cursor.next()

    @property
    def alive(self):
        """True si existen más modelos por devolver, False en caso contrario
        """
        return self.command_cursor.alive
        pass #No olvidar eliminar esta linea una vez implementado
