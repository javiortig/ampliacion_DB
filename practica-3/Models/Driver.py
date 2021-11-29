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


# ########

#     @staticmethod
#     def return_to_str(cls,labels: Union[list, str] = "*", orderByAsc: Union[str, None] = None,  orderByDesc: Union[str, None] = None, skip: Union[int,None] = 0, limit: Union[int,None] = None): -> str
# 	   	if orderByAsc is not None and orderByDesc is not None:
#             raise("order by asc, o desc, pero no ambos")
#         result = " return " + _unwind_elements_to_str(elements=labels)
# 	   	if orderByAsc is not None or orderByDesc is not None:
# 	   		result += " order by " + (f'{orderByAsc} asc' if orderByAsc is not None else f'{orderByDesc} desc')
# 	   	if skip > 0:
# 	   		result += f' skip {skip}'
# 	   	if limit is not None:
# 	   		result += f' limit {limit}'
# 	   	return result
    
#     @staticmethod
#     def simple_node_relation_to_str(cls,\
#         node_a_identifier: Union[str, None] = None, node_a_labels: Union[list, str, None] = ['user'], node_a_properties: Union[dict, None] = None,\
#         node_b_identifier: Union[str, None] = None, node_b_labels: Union[list, str, None] = ['user'], node_b_properties: Union[dict, None] = None,\
#         relation_identifier: Union[str, None] = None, relation_labels: Union[list, str, None] = None, relation_properties: Union[dict, None] = None, direction: str = '-',\
#         condition: Union[list,str,None] = None, using: Union[list,str] = None, afterUsingCondition: Union[list,str,None] = None, path: Union[str,None] = None\
#         return_labels: Union[list, str] = "*", orderByAsc: Union[str, None] = None, orderByDesc: Union[str, None] = None, skip: Union[int,None] = 0, limit: Union[int,None] = None): -> str
#         return " match " + (f'{path} = ' if path is not None else "") + " ",\
#             + cls.node_to_str(identifier=node_a_identifier,labels=node_a_labels,properties=node_a_properties),\
#             + cls.relation_to_str(identifier=relation_identifier,labels=relation_labels,properties=relation_properties,direction=direction),\
#             + cls.node_to_str(identifier=node_b_identifier,labels=node_b_labels,properties=node_b_properties),\
#             + (cls.condition_to_str(condition=condition) if condition is not None else ""),\
#             + (cls.using_to_str(using=using) if using is not None else ""),\
#             + (cls.condition_to_str(condition=afterUsingCondition) if afterUsingCondition is not None else ""),\
#             + cls.return_to_str(labels=return_labels,orderByAsc=orderByAsc,orderByDesc=orderByDesc,skip=skip,limit=limit)

#     	# return " match " + cls.node_to_str(labels=['user'], properties=properties) \
#         #     + cls.relation_to_str(labels=labels, direction='-')\
#         #     + cls.condition_to_str(condition=condition) if condition is not None\
#         #     + cls.node_to_str('p', 'user') + db.get_result("distinct p")
   	

#     #Q1
#    	@staticmethod
#    	def friend_and_family_to_str(cls,properties: Union[dict, None] = None): -> str
#         return cls.simple_node_relation_to_str( node_a_properties=properties,\
#                                                 relation_properties='friendship|friend*1',\
#                                                 node_b_identifier="p",\
#                                                 return_labels="distinct p")
#         # return cls._simple_node_relation_to_str(relation_labels='friendship|friend*1', node_a_properties=properties,node_b_identifier="p",)
#    		# return cls._node_relation_to_str(labels='friendship|friend*1',properties=properties)
   		
#     #Q2
#    	@staticmethod
#    	def family_of_family_to_str(cls,properties: Union[dict, None] = None): -> str
#    		return cls.simple_node_relation_to_str( node_a_properties=properties,\
#                                                 relation_properties='friendship*2',\
#                                                 node_b_identifier="p",\
#                                                 return_labels="distinct p")
#         # return cls,_node_relation_to_str(labels='friendship*2',properties=properties)
        
#     @staticmethod
#     def _unwind_elements_to_str(cls, separator: str =",", elements: Union[list,str]): -> str
#         return elements if type(elements) is str else separator.join(elements)

#     @staticmethod
#     def _inner_query_clauses(cls,clause: str, elements: Union[list,str]): -> str
#         res = " " + clause + _unwind_elements_to_str(elements=elements)
#         return res

#     @staticmethod
#     def condition_to_str(cls,condition: Union[list,str]): -> str
#         return cls._inner_query_clauses("where",condition)

#     @staticmethod
#     def using_to_str(cls,using: Union[list,str]): -> str
#         return cls._inner_query_clauses("with",using)

#     #Q3
#     @staticmethod
#     def messages_after_data_to_str(cls,datetime: str,node_a_properties: Union[dict, None] = None, node_b_properties:  Union[dict, None] = None): -> str
#         #TODO el comprobar si ta correcto:
#         if not comprobarDatetime(datetime):
#             raise("The datetime is incorrect")
#         return cls.simple_node_relation_to_str( node_a_properties=node_a_properties,\
#                                                 node_b_properties=node_b_properties,\
#                                                 relation_identifier="r",\
#                                                 relation_labels="message",\
#                                                 direction=">",\
#                                                 condition=f'r.data > datetime({datetime})',\
#                                                 return_labels="r",\
#                                                 orderByAsc="r.data")

#     #Q4
#     @classmethod
#     def conversation_between_users_to_str(cls, node_a_properties: Union[dict, None] = None, node_b_properties:  Union[dict, None] = None): -> str
#         return cls.simple_node_relation_to_str( node_a_properties=node_a_properties,\
#                                                 node_b_properties=node_b_properties,\
#                                                 relation_identifier="r",\
#                                                 relation_labels="message",\
#                                                 return_labels="r",\
#                                                 orderByAsc="r.data")

#     #Q5
#     @classmethod
#     def mentioned_users_with_laboral_relation(cls, properties: Union[dict, None] = None): -> str
#         return " match " + cls.node_to_str(     identifier="publicante",\
#                                                 labels=['user'],\
#                                                 properties=properties)\
#                          + cls.relation_to_str( labels=['publishes'],\
#                                                 direction=">")\
#                          + cls.node_to_str(     labels=['publication'])\
#                          + cls.relation_to_str( labels=['mention'])\
#                          + cls.node_to_str(     identifier="mentioned",\
#                                                 labels=['user'])\
#                          + cls.relation_to_str( labels=['laboral'])\
#                          + cls.node_to_str(     identifier="publicante")\
#                          + cls.relation_to_str( labels="distinct mentioned")

#     #Q6
#     #TODO no estoy seguro sobre el ASC o DESC
#     #TODO camviar lo del roderByAsc por numSaltos
#     @classmethod
#     def distance_new_relationships(cls, distance: int): -> str
#         return cls.simple_node_relation_to_str( path="path",\
#                                                 node_a_identifier="inicio",\
#                                                 node_b_identifier="final",\
#                                                 relation_labels=f'1..{distance}',\
#                                                 direction=">",\
#                                                 condition="inicio < final",\
#                                                 # using=["path", '[[ID(inicio), ID(final)],"Segundo",apoc.coll.pairsMin(nodes(path))[0][1],"Tercero",inicio] as segundos_y_terceros', "length(path) as numSaltos"],\
#                                                 using=["path", '["Segundo",apoc.coll.pairsMin(nodes(path))[0][1],"Tercero",inicio] as segundos_y_terceros', "length(path) as numSaltos"],\
#                                                 afterUsingCondition="numSaltos>1",\
#                                                 return_labels=["numSaltos", "segundos_y_terceros"],\
#                                                 orderByAsc="length(path)",\
#                                                 skip=1)
