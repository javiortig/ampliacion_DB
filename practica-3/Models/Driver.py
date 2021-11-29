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

    def return_to_str(labels: Union[list, str] = "*", orderByAsc: Union[bool, None] = None, skip: Union[int,None] = 0, limit: Union[int,None] = None):
	   	result = " return "
	   	if type(labels) is str:
	   		result += labels
	   	else:
	   		result = ",".join(labels)
	   	if orderByAsc is not None:
	   		result += " order by"
	   		if orderByAsc:
	   			result += " asc"
	   		else:
	   			result += " desc"
	   	if skip > 0:
	   		result += f' skip {skip}'
	   	if limit is not None:
	   		result += f' limit {limit}'
	   	return result
    
    @staticmethod
    def friend_and_family_to_str(properties: Union[dict, None] = None):
    	return "match " + db.node_to_str(labels=['user'], properties=properties) \
            + db.relation_to_str(labels='friendship|friend*1', direction='-')\
            + db.node_to_str('p', 'user') + db.get_result("distinct p")
        

