from neo4j import GraphDatabase
from typing import Union

from neo4j.work import result

#TODO: hacer una session x query/transaction o hacer unaa session para toda la clase??
class Driver:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, input: str):
        with self.driver.session() as session:
            query_result = session.run(input)
            return query_result.values()


    @classmethod
    # assemblies node variables to a query string format
    def node_to_str(cls, identifier: Union[str, None] = None, labels: Union[list, str, None] = None, properties: Union[dict, None] = None)-> str:
        result = '('

        # Adds identifier
        if identifier:
            result += identifier

        # Adds labels
        if not labels:
            result += ''
        elif type(labels) == list:
            for l in labels:
                result += ':' + l
        else: 
            result += ':' + labels
        
        # Adds properties:
        if(properties):
            result += ' {'
            for k, v in properties.items():
                result += k + ': "' + v + '",'

            result = result[:-1] + '}'


        return result + ')'


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