from .Driver import Driver
from constants import neo4j as dbK

from typing import Union

# This class will be accessed from the user

#TODO: hacer mejor que sea una herencia
class Redes(Driver):
    def __init__(self):
        super().__init__(dbK.ADDRESS, dbK.USERNAME, dbK.PASSWORD)

        # Create username index and constraint: 
        #TODO: crear indexado para las fechas de los mensajes
        self.query('CREATE CONSTRAINT IF NOT EXISTS ON (u:user) ASSERT u.username IS UNIQUE')

    def _add_user(self, type, username: str, properties: Union[dict, None] = None):
        labels = ['user']


        if (type == 'university'):
            labels.append('university')
        elif (type == 'company'):
            labels.append('company')
        else:
            Exception('Internal error handling users')

        if(properties):
            properties['username'] = username

        query = "CREATE " + self.node_to_str(labels=labels, properties=properties)
        self.query(query)

    def delete_user(self, username: str):
        query = "DELETE DETATCH " + self.node_to_str(labels='user', properties={'username': username})
        self.query(query)
    
    # username must be unique
    def create_user(self, username: str, **kwargs):
        self._add_user('basic', username, kwargs)

    def create_university(self, username: str, **kwargs):
        self._add_user('university', username, kwargs)

    def create_company(self, username: str, **kwargs):
        self._add_user('company', username, kwargs)
    
    @staticmethod
    def new_message_to_str(cls,message: str, datetime: str, node_a_properties: Union[dict, None] = None, node_b_properties:  Union[dict, None] = None) -> str :
        #TODO el comprobar si ta correcto:
        if not cls.comprobarDatetime(datetime):
            raise("The datetime is incorrect")
        return ' match ' + cls.node_to_str(     identifier="a",\
                                                labels="user",\
                                                properties=node_a_properties)\
                        + "," +\
                        + cls.node_to_str(  identifier="b",\
                                                labels="user",\
                                                properties=node_b_properties)\
                        + cls.merge_to_str(     merge=  cls.node_to_str(        labels="a")\
                                                        + cls.relation_to_str(  labels="converInfo",\
                                                                                direction=">")\
                                                        + cls.node_to_str(      identifier="convNode",\
                                                                                labels="Conversation")\
                                                        + cls.relation_to_str(  labels="converInfo",\
                                                                                direction="<")\
                                                        + cls.node_to_str(      labels="b"),\
                                                on_create=  {"convNode.num_seq":"0"},\
                                                on_match=   {"convNode.num_seq":"convNode.num_seq + 1"})\
                        + cls.create_to_str(    create=[    cls.node_to_str(identifier="a")\
                                                            + cls.relation_to_str(      labels="message",\
                                                                                        properties={    "text":message,\
                                                                                                        "datetime":f'datetime({datetime})',\
                                                                                                        "num_seq":"convNode.num_seq"})\
                                                            + cls.node_to_str(identifier="b")])
        
        # return " match (a:User {" + cls._dict_to_str(elements=node_a_properties,separator_dict=":") + "}),(b:User {" + cls._dict_to_str(elements=node_b_properties,separator_dict=":") + "}) merge (a)-[:converInfo]->(convNode:Conversacion)<-[:converInfo]-(b) on create set convNode.numSeq = 0 on match set convNode.numSeq = convNode.numSeq + 1 create (a)-[:message {text:" + message + ",numSeq:convNode.numSeq,data:datetime(" + datetime + ")}]->(b)"



    #Q1
   	@staticmethod
   	def friend_and_family_to_str(cls,properties: Union[dict, None] = None) -> str :
        # return cls.simple_node_relation_to_str( node_a_properties=properties,\
                                                # relation_labels='friendship|friend*1',\
                                                # node_b_identifier="p",\
                                                # return_labels="distinct p")
        return " match " + cls.node_to_str(     labels=['user'],\
                                                properties=properties)\
                            + cls.relation_to_str( labels='friendship|friend*1',\
                                                direction='-')\
                            + cls.node_to_str(     labels=['user'],\
                                                identifier="p")\
                            + cls.return_to_str(   labels="distinct p")
   		
    #Q2
   	@staticmethod
   	def family_of_family_to_str(cls,properties: Union[dict, None] = None) -> str :
   		# return cls.simple_node_relation_to_str( node_a_properties=properties,\
        #                                         relation_labels='friendship*2',\
        #                                         node_b_identifier="p",\
        #                                         return_labels="distinct p")
        return " match " + cls.node_to_str(     labels=['user'],\
                                                properties=properties)\
                        + cls.relation_to_str( labels='friendship*2',\
                                                direction='-')\
                        + cls.node_to_str(     identifier="p",\
                                                labels=['user'])\
                        + cls.return_to_str(   labels="distinct p") 
    
    #Q3
    @staticmethod
    def messages_after_data_to_str(cls,datetime: str,node_a_properties: Union[dict, None] = None, node_b_properties:  Union[dict, None] = None) -> str :
        #TODO el comprobar si ta correcto:
        if not cls.comprobarDatetime(datetime):
            raise("The datetime is incorrect")
        # return cls.simple_node_relation_to_str( node_a_properties=node_a_properties,\
        #                                         node_b_properties=node_b_properties,\
        #                                         relation_identifier="r",\
        #                                         relation_labels="message",\
        #                                         direction=">",\
        #                                         condition=f'r.data > datetime({datetime})',\
        #                                         return_labels="r",\
        #                                         orderByAsc="r.data")
        return " match " + cls.node_to_str(     labels=['user'],\
                                                properties=node_a_properties)\
                        + cls.relation_to_str( identifier="r",\
                                                labels="message",\
                                                direction=">")\
                        + cls.node_to_str(     labels=['user'],\
                                                properties=node_b_properties)\
                        + cls.condition_to_str(condition=f'r.data > datetime({datetime})')\
                        + cls.return_to_str(   labels="r",orderByAsc="r.data")

    #Q4
    @classmethod
    def conversation_between_users_to_str(cls, node_a_properties: Union[dict, None] = None, node_b_properties:  Union[dict, None] = None) -> str :
    # match (a:Prueba {nork:1})-[r:mensaje]-(b:Prueba {nork:7}) return r order by r.num_seq asc
        # return cls.simple_node_relation_to_str( node_a_properties=node_a_properties,\
        #                                         node_b_properties=node_b_properties,\
        #                                         relation_identifier="r",\
        #                                         relation_labels="message",\
        #                                         return_labels="r",\
        #                                         orderByAsc="r.data")
        return " match " + cls.node_to_str(     labels=['user'],\
                                                properties=node_a_properties)\
                        + cls.relation_to_str( identifier="r",\
                                                labels="message",\
                                                direction='-')\
                        + cls.node_to_str(     labels=['user'],\
                                                properties=node_b_properties)\
                        + cls.return_to_str(   labels="r",\
                                                orderByAsc="r.num_seq")

    #Q5
    @classmethod
    def mentioned_users_with_laboral_relation(cls, properties: Union[dict, None] = None) -> str :
        return " match " + cls.node_to_str(     identifier="publicante",\
                                                labels=['user'],\
                                                properties=properties)\
                        + cls.relation_to_str( labels=['publishes'],\
                                                direction=">")\
                        + cls.node_to_str(     labels=['publication'])\
                        + cls.relation_to_str( labels=['mention'])\
                        + cls.node_to_str(     identifier="mentioned",\
                                                labels=['user'])\
                        + cls.relation_to_str( labels=['laboral'])\
                        + cls.node_to_str(     identifier="publicante")\
                        + cls.relation_to_str( labels="distinct mentioned")

    #Q6
    #TODO no estoy seguro sobre el ASC o DESC
    #TODO camviar lo del roderByAsc por numSaltos
    @classmethod
    def distance_new_relationships(cls, distance: int) -> str :
        # return cls.simple_node_relation_to_str( path="path",\
        #                                         node_a_identifier="inicio",\
        #                                         node_b_identifier="final",\
        #                                         relation_labels=f'1..{distance}',\
        #                                         direction=">",\
        #                                         condition="inicio < final",\
        #                                         # using=["path", '[[ID(inicio), ID(final)],"Segundo",apoc.coll.pairsMin(nodes(path))[0][1],"Tercero",inicio] as segundos_y_terceros', "length(path) as numSaltos"],\
        #                                         using=["path", '["Segundo",apoc.coll.pairsMin(nodes(path))[0][1],"Tercero",inicio] as segundos_y_terceros', "length(path) as numSaltos"],\
        #                                         afterUsingCondition="numSaltos>1",\
        #                                         return_labels=["numSaltos", "segundos_y_terceros"],\
        #                                         orderByAsc="length(path)",\
        #                                         skip=1)
        return " match path=" + cls.node_to_str(identifier="inicio",\
                                                labels="['user']")\
                        + cls.relation_to_str(  labels=f'1..{distance}',\
                                                direction=">")\
                        + cls.node_to_str(      identifier="final",\
                                                labels="['user']")\
                        + cls.condition_to_str( condition="inicio < final")\
                        + cls.using_to_str(     using=["path", '["Segundo",apoc.coll.pairsMin(nodes(path))[0][1],"Tercero",inicio] as segundos_y_terceros', "length(path) as numSaltos"])\
                        + cls.condition_to_str( condition="numSaltos>1")\
                        + cls.return_to_str(    labels=["numSaltos", "segundos_y_terceros"],\
                                                orderByAsc="length(path)",\
                                                skip=1)

# MATCH path = (inicio:Prueba)-[rs*1..6]->(final:Prueba)
# where inicio < final
# with path, [[ID(inicio), ID(final)],"Segundo",apoc.coll.pairsMin(nodes(path))[0][1],"Tercero",inicio] as segundos_y_terceros, length(path) as numSaltos where numSaltos>1
# RETURN numSaltos, segundos_y_terceros as Segundos ORDER BY length(path) skip 1 
