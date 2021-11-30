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

    def comprobarDatetime(cls,datetime: str) -> bool :
        return True

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
    
    @staticmethod
    def _dict_to_str(cls,elements: dict, separator_dict: str ="="):
        return cls._elements_to_str([cls._elements_to_str(separator=separator_dict,elements=a) for a in [(k,v) for k,v in elements.items()]])

    @staticmethod
    def merge_to_str(cls,merge: Union[list, str], on_create: Union[dict, str, None] = None, on_match: Union[dict, str, None] = None):
        return " merge " +cls._elements_to_str(elements=merge)\
                        + (" on create set " + (on_create if type(on_create) is str else (cls._dict_to_str(elements=on_create) if on_create is not None else "")))\
                        + (" on match set " + (on_match if type(on_match) is str else (cls._dict_to_str(elements=on_match) if on_match is not None else "")))

    @staticmethod
    def return_to_str(cls,labels: Union[list, str] = "*", orderByAsc: Union[str, None] = None,  orderByDesc: Union[str, None] = None, skip: Union[int,None] = 0, limit: Union[int,None] = None) -> str :
        if orderByAsc is not None and orderByDesc is not None:
            raise("order by asc, o desc, pero no ambos")

        result = " return " + cls._elements_to_str(elements=labels)
        if orderByAsc is not None or orderByDesc is not None:
            result += " order by " + (f'{orderByAsc} asc' if orderByAsc is not None else f'{orderByDesc} desc')
        if skip > 0:
            result += f' skip {skip}'
        if limit is not None:
            result += f' limit {limit}'
        return result

    # @staticmethod
    # def simple_node_relation_to_str(cls,\
    #     node_a_identifier: Union[str, None] = None, node_a_labels: Union[list, str, None] = ['user'], node_a_properties: Union[dict, None] = None,\
    #     node_b_identifier: Union[str, None] = None, node_b_labels: Union[list, str, None] = ['user'], node_b_properties: Union[dict, None] = None,\
    #     relation_identifier: Union[str, None] = None, relation_labels: Union[list, str, None] = None, relation_properties: Union[dict, None] = None, direction: str = '-',\
    #     condition: Union[list,str,None] = None, using: Union[list,str] = None, afterUsingCondition: Union[list,str,None] = None, path: Union[str,None] = None\
    #     return_labels: Union[list, str] = "*", orderByAsc: Union[str, None] = None, orderByDesc: Union[str, None] = None, skip: Union[int,None] = 0, limit: Union[int,None] = None) -> str :
    #     return " match " + (f'{path} = ' if path is not None else "") + " ",\
    #         + cls.node_to_str(identifier=node_a_identifier,labels=node_a_labels,properties=node_a_properties),\
    #         + cls.relation_to_str(identifier=relation_identifier,labels=relation_labels,properties=relation_properties,direction=direction),\
    #         + cls.node_to_str(identifier=node_b_identifier,labels=node_b_labels,properties=node_b_properties),\
    #         + (cls.condition_to_str(condition=condition) if condition is not None else ""),\
    #         + (cls.using_to_str(using=using) if using is not None else ""),\
    #         + (cls.condition_to_str(condition=afterUsingCondition) if afterUsingCondition is not None else ""),\
    #         + cls.return_to_str(labels=return_labels,orderByAsc=orderByAsc,orderByDesc=orderByDesc,skip=skip,limit=limit)
   	
    @staticmethod
    def _elements_to_str(cls, elements: Union[list,str], separator: str =",") -> str :
        return elements if type(elements) is str else separator.join(elements)

    @staticmethod
    def _inner_query_clauses(cls,clause: str, elements: Union[list,str]) -> str :
        res = " " + clause + cls._elements_to_str(elements=elements)
        return res

    @staticmethod
    def condition_to_str(cls,condition: Union[list,str]) -> str :
        return cls._inner_query_clauses("where",condition)

    @staticmethod
    def using_to_str(cls,using: Union[list,str]) -> str :
        return cls._inner_query_clauses("with",using)
    
    @staticmethod
    def create_to_str(cls,create: Union[list,str]) -> str :
        return cls._inner_query_clauses("create",create)

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
    


