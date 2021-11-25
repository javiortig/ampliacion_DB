from neo4j import GraphDatabase
from typing import Union

from neo4j.work import result

# TODO: Como hacer las queries atomicas?? iniciar una sesion e ir haciendo transacciones
# o hacer una pipeline que sea una lista de string con las queries y ejecutarla al final
# o hacer una unica megatransaccion...
class Driver:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))


    # Close connection  
    def close(self):
        self.driver.close()

    def query(self, input: str):
        with self.driver.session() as session:
            query_result = session.run(input)
            return query_result.values()

        
    def execute(self):
        pass
    @classmethod
    # This function is used just to reuse code
    def _inner_query_str_values(cls, identifier: Union[str, None] = None, labels: Union[list, str, None] = None, properties: Union[dict, None] = None)-> str:
        result = ''

        # Adds identifier
        if identifier:
            result += identifier

        # Adds labels
        if type(labels) == list:
            for l in labels:
                result += ':' + l
        elif type(labels) == str: 
            result += ':' + labels
        
        # Adds properties:
        if(properties):
            result += ' {'
            for k, v in properties.items():
                result += k + ': "' + v + '",'

            result = result[:-1] + '}'

        return result

    @classmethod
    # assemblies node variables to a query string format
    def node_to_str(cls, identifier: Union[str, None] = None, labels: Union[list, str, None] = None, properties: Union[dict, None] = None)-> str:
        return '(' + cls._inner_query_str_values(identifier, labels, properties) + ')'

    # Relations direction can be '<', '>' or '-'
    @classmethod
    def relation_to_str(cls, identifier: Union[str, None] = None, labels: Union[list, str, None] = None, properties: Union[dict, None] = None, direction: str = '>'):
        result = '-'
        
        if(identifier or labels or properties):
            result += '['
            result += cls._inner_query_str_values(identifier, labels, properties)
            result += ']'

        
        result += '-'

        # Adds direction
        if(direction == '>'):
            result += '>'
     
        elif(direction == '<'):
            result = '<' + result   

        return result
        

    def print_greeting(self, message: str):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]