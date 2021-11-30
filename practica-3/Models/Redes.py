from .Driver import Driver
from constants import neo4j as dbK

from typing import Union

# This class will be accessed from the user
class Redes(Driver):
    def __init__(self):
        super().__init__(dbK.ADDRESS, dbK.USERNAME, dbK.PASSWORD)

        # Create username index and constraint: 
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
        
    @classmethod
    def username_dict(cls, username: str) -> str :
        return " {username:\""+username+"\"} "

    @classmethod 
    def create_publication(cls, author: str, date: str, title: str, body: str, mentioned_usernames: Union[list,str,None] = None ) -> str:
        query_text = 'match (_author:user  {username:"'+author+'"}) '
        query_text_mentions = ""
        
        # Match of the mentioned users AND creation of the mention
        if mentioned_usernames is not None:
            if type(mentioned_usernames) is list:
                for u in mentioned_usernames:
                    query_text += (",("+u+":user {username:\""+u+"\"}) " if type(u) is str else "")
                    query_text_mentions += ",("+u+")<-[:mention]-(_p)"
            else:
                query_text += (",("+mentioned_usernames+":user {username:\""+author+"\"} " if mentioned_usernames is not None else "")
                query_text_mentions += ",("+mentioned_usernames+")<-[:mention]-(_p)"
        query_text += ' create (_author)-[:publishes]->(_p:publishing  {author:"'+ author +'",title:"'+ title +'",body:"'+ body +'",date:"'+ date +'"})'
        query_text += query_text_mentions
        
        cls.query(query_text)
        return query_text
    
    @classmethod
    # Create new message
    def new_message_to_str(cls, message: str, datetime: str, sender_username: str, receiver_username:  str ) -> str :
        # cls._dict_to_str(elements=node_b_properties,separator_dict=":")
        # When there is a new message, the sequence number stored in the "chat" node increments.
        # If there is still no message between the two, one is created and starts with the sequence number at 0.
        return " match (a:user "+cls.username_dict(sender_username)+"),(b:user "+cls.username_dict(receiver_username)+") \
            merge (a)-[:chatInfo]->(convNode:chat)<-[:chatInfo]-(b) on create set convNode.sec = 0 on match set convNode.sec = convNode.sec + 1 create (a)-[:message {text:\"" + message + "\",sec:convNode.sec,date:datetime(\"" + datetime + "\")}]->(b)"

    #Q1
    @classmethod
    # Get the friends and family of a given user
    def friend_and_family_to_str(cls, username: str) -> str :
        return " match "+\
            cls.node_to_str(labels=['user'], properties=cls.username_dict(username))+\
            cls.relation_to_str( labels='family|friend*1', direction='-')+\
            cls.node_to_str(labels=['user'], identifier="p")+\
            cls.return_to_str(labels="distinct p")
        
    #Q2
    @classmethod
    # Obtain the relatives of the relatives of a given user
    def family_of_family_to_str(cls, username: str) -> str :
        return " match "+\
            cls.node_to_str(labels=['user'], properties=cls.username_dict(username))+\
            cls.relation_to_str( labels='family*2', direction='-')+\
            cls.node_to_str(identifier="p", labels=['user'])+\
            cls.return_to_str(labels="distinct p")
        
    #Q3
    @classmethod
    # Get all messages sent from a given user to a given user after a specified date
    def messages_after_data_to_str(cls,datetime: str,username_a: str, username_b: str) -> str :
        return " match "+\
            cls.node_to_str(labels=['user'], properties=cls.username_dict(username_a))+\
            cls.relation_to_str( identifier="r", labels="message",direction=">")+\
            cls.node_to_str(labels=['user'], properties=cls.username_dict(username_b))+\
            " where r.date > datetime(\""+datetime+"\") "+\
            cls.return_to_str(labels="r", orderByAsc="r.date")

    #Q4
    @classmethod
    # Obtain the complete conversation between two specific users
    def conversation_between_users_to_str(cls, username_a: str, username_b: str) -> str :
    # match (a:Prueba {nork:1})-[r:mensaje]-(b:Prueba {nork:7}) return r order by r.num_seq asc
        return " match "+\
            cls.node_to_str(labels=['user'], properties=cls.username_dict(username_a))+\
            cls.relation_to_str(identifier="r", labels="message", direction='-')+\
            cls.node_to_str(labels=['user'], properties=cls.username_dict(username_b))+\
            cls.return_to_str(labels="r", orderByAsc="r.sec")

    #Q5
    @classmethod
    # Get all users mentioned by a given user who have a working relationship with the user who mentioned them.
    def mentioned_users_with_laboral_relation(cls, username: str) -> str :
        return " match "+\
            cls.node_to_str(identifier="publicante", labels=['user'], properties=cls.username_dict(username))+\
            cls.relation_to_str(labels=['publishes'], direction=">")+\
            cls.node_to_str(labels=['publishing'])+\
            cls.relation_to_str(labels=['mention'])+\
            cls.node_to_str(identifier="mentioned", labels=['user'])+\
            cls.relation_to_str(labels=['work'])+\
            cls.node_to_str(identifier="publicante")+\
            cls.return_to_str(labels="distinct mentioned")

    #Q6
    @classmethod
    def distance_new_relationships(cls, distance: int) -> str :
    # cls.using_to_str(     using=["path", '["Segundo",apoc.coll.pairsMin(nodes(path))[0][1],"Tercero",inicio] as segundos_y_terceros', "length(path) as numSaltos"])\
        return " match path = "+\
            cls.node_to_str(identifier="inicio", labels=['user'])+\
            cls.relation_to_str(labels=f'1..{distance}', direction=">")+\
            cls.node_to_str(identifier="final", labels=['user'])+\
            ' where inicio < final'+\
            ' with path, ["Segundo",apoc.coll.pairsMin(nodes(path))[0][1],"Tercero",inicio] as segundos_y_terceros, length(path) as numSaltos'+\
            ' where numSaltos>1'+\
            cls.return_to_str(labels=["numSaltos", "segundos_y_terceros"], orderByAsc="length(path)", skip=1)

    # MATCH path = (inicio:Prueba)-[rs*1..6]->(final:Prueba)
    # where inicio < final
    # with path, [[ID(inicio), ID(final)],"Segundo",apoc.coll.pairsMin(nodes(path))[0][1],"Tercero",inicio] as segundos_y_terceros, length(path) as numSaltos where numSaltos>1
    # RETURN numSaltos, segundos_y_terceros as Segundos ORDER BY length(path) skip 1 

    #6
    @classmethod
    def messages_new_relationships(cls, username: str, min_messages: int) -> str :
        return " match "+\
            cls.node_to_str(identifier="f", labels=['user'], properties=cls.username_dict(username))+\
            " , " + cls.node_to_str(identifier="s")+\
            " , " + cls.node_to_str(identifier="t")+\
            " , " + cls.node_to_str(identifier="f") + cls.relation_to_str(direction="-", labels="friend|family|academic|work") + cls.node_to_str(identifier="s", labels=['user'])+\
            " , " + cls.node_to_str(identifier="f") + cls.relation_to_str() + cls.node_to_str(identifier="c1",labels=['chat']) + cls.relation_to_str() + cls.node_to_str(identifier="s")+\
            " , " + cls.node_to_str(identifier="s") + cls.relation_to_str() + cls.node_to_str(identifier="c2",labels=['chat']) + cls.relation_to_str() + cls.node_to_str(identifier="t")+\
            f' where c1.sec > {min_messages} and c2.sec > {min_messages} and not ' + cls.node_to_str(identifier="f") + cls.relation_to_str(labels="friend|family|academic|work") + cls.node_to_str(identifier="t")+\
            " return t order by c1.sec desc, c2.sec desc "


    # match (f:user {username: 'Angela Smith'}), (s:user), (t:user), (f:user)-[:friend|family|academic|work]-(s:user), 
    # (f)--(c1:chat)--(s), (s)--(c2:chat)--(t)
    # where c1.sec > 2 and c2.sec > 2 and
    # not(f)-[:friend|family|academic|work]-(t)
    # return t 
    # order by c1.sec desc, c2.sec desc
