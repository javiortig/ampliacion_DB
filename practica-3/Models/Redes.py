from .Driver import Driver
from constants import neo4j as dbK

from typing import Union

# This class will be accessed from the user
class Redes(Driver):
    def __init__(self):
        super().__init__(dbK.ADDRESS, dbK.USERNAME, dbK.PASSWORD)

        # Create username index and constraint: 
        self.query('CREATE CONSTRAINT IF NOT EXISTS ON (u:user) ASSERT u.username IS UNIQUE')

    @classmethod
    def load_json(cls, url: str) ->str:
        load_json_query = 'call apoc.load.json("'+ url +'") yield value\
        unwind value.users as users\
        call apoc.merge.node([\'user\', users.type], {username: users.username}) yield node \
        unwind value.relations as relations\
        match (f:user {username: relations.from})\
        match (t:user {username: relations.to})\
        call apoc.merge.relationship(f, relations.type, null, null, t, {}) yield rel\
        unwind value.publishings as pubs\
        with distinct pubs, value\
        match (auth:user {username: pubs.author})\
        create (auth)-[:publishes]->(p:publishing {author: pubs.author, title: pubs.title, body: pubs.body, date: datetime(pubs.date)})\
        with distinct pubs, value, p\
        unwind pubs.mentions as mentions\
        match (men:user {username: mentions})\
        create (p)-[:mention]->(men)\
        with value\
        unwind value.chats as chats\
        with chats, value\
        match (m_f:user {username: chats.from})\
        match (m_t:user {username: chats.to})\
        merge (m_f)-[r1_chat:chats_with]->(c:chat {sec: chats.sec})<-[r2_chat:chats_with]-(m_t)\
        with value, chats\
        unwind chats.messages as messages\
        match (m_f:user {username: messages.from})\
        match (m_t:user {username: messages.to})\
        merge (m_f)-[:message {body: messages.body, date: datetime(messages.date), sec: messages.sec}]->(m_t)\
        return count(chats)'
        return load_json_query

    @classmethod
    def _add_user(cls, type, username: str, properties: Union[dict, None] = None):
        labels = ['user']

        if (type == 'university' or type == 'company' or type == 'basic'):
            labels.append(type)
        else:
            Exception('Internal error handling users')

        if(properties):
            properties['username'] = username
        else:
            properties = {'username': username}

        query = "CREATE " + cls.node_to_str(labels=labels, properties=properties)
        return query

    @classmethod
    def delete_user(cls, username: str):
        query = "MATCH " +cls.node_to_str(identifier='u',labels='user', properties={'username': username}) +" DETACH DELETE " + cls.node_to_str(identifier='u')
        return query

        
    # username must be unique
    @classmethod
    def create_user(cls, username: str, **kwargs):
        return cls._add_user('basic', username, kwargs)

    @classmethod
    def create_university(cls, username: str, **kwargs):
        return cls._add_user('university', username, kwargs)

    @classmethod
    def create_company(cls, username: str, **kwargs):
        return cls._add_user('company', username, kwargs)

    @classmethod
    def create_publication(cls, author: str, date: str, title: str, body: str, mentioned_usernames: Union[list,str,None] = None ) -> str:
        query_text = 'match (_author:user  {username:"'+author+'"}) '
        query_text_mentions = ""
        if mentioned_usernames is not None:
            if type(mentioned_usernames) is list:
                for u in mentioned_usernames:
                    query_text += (",("+u.replace(" ", "_")+":user {username:\""+u+"\"}) " if type(u) is str else "")
                    query_text_mentions += ",("+u.replace(" ", "_")+")<-[:mention]-(_p)"
            else:
                query_text += (",("+mentioned_usernames.replace(" ", "_")+":user {username:\""+author+"\"} " if mentioned_usernames is not None else "")
                query_text_mentions += ",("+mentioned_usernames.replace(" ", "_")+")<-[:mention]-(_p)"
        query_text += ' create (_author)-[:publishes]->(_p:publishing  {author:"'+ author +'",title:"'+ title +'",body:"'+ body +'",date:"'+ date +'"})'
        query_text += query_text_mentions

        return query_text
        
    @classmethod
    def username_dict(cls, username: str) -> str :
        return {"username":username}
    
    @classmethod
    # Create new message
    def new_message_to_str(cls, message: str, datetime: str, sender_username: str, receiver_username:  str ) -> str :
        # cls._dict_to_str(elements=node_b_properties,separator_dict=":")
        # When there is a new message, the sequence number stored in the "chat" node increments.
        # If there is still no message between the two, one is created and starts with the sequence number at 0.
        return " match (a:user {username: \""+ sender_username +"\"}),(b:user {username: \""+ receiver_username +"\"}) \
            merge (a)-[:chatInfo]->(convNode:chat)<-[:chatInfo]-(b) on create set convNode.sec = 0 on match set convNode.sec = convNode.sec + 1 create (a)-[:message {body:\"" + message + "\",sec:convNode.sec,date:datetime(\"" + datetime + "\")}]->(b)"

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
    def messages_after_date_to_str(cls,datetime: str,username_a: str, username_b: str) -> str :
        return " match "+\
            cls.node_to_str(labels=['user'], properties=cls.username_dict(username_a))+\
            cls.relation_to_str( identifier="r", labels="message",direction=">")+\
            cls.node_to_str(labels=['user'], properties=cls.username_dict(username_b))+\
            " where r.date > datetime(\""+datetime+"\") "+\
            cls.return_to_str(labels="r.date", orderByAsc="r.date")

    #Q4
    @classmethod
    # Obtain the complete conversation between two specific users
    def conversation_between_users_to_str(cls, username_a: str, username_b: str) -> str :
        # match (a:Prueba {nork:1})-[r:mensaje]-(b:Prueba {nork:7}) return r order by r.num_seq asc
        return " match "+\
            cls.node_to_str(labels=['user'], properties=cls.username_dict(username_a))+\
            cls.relation_to_str(identifier="r", labels="message", direction='-')+\
            cls.node_to_str(labels=['user'], properties=cls.username_dict(username_b))+\
            cls.return_to_str(labels="r.date", orderByAsc="r.sec")

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
    def distance_new_relationships(cls, distance: int, username: str) -> str :
    # cls.using_to_str(     using=["path", '["Segundo",apoc.coll.pairsMin(nodes(path))[0][1],"Tercero",inicio] as segundos_y_terceros', "length(path) as numSaltos"])\
        return " match "+\
            cls.node_to_str(identifier="f", labels=['user'], properties=cls.username_dict(username))+\
            " , " + cls.node_to_str(identifier="s", labels=['user'])+\
            " , " + cls.node_to_str(identifier="t", labels=['user'])+\
            " where not "+\
                cls.node_to_str(identifier="f")+\
                cls.relation_to_str(labels="friend|family|academic|work")+\
                cls.node_to_str(identifier="t")+\
                " and "+\
                cls.node_to_str(identifier="s")+\
                cls.relation_to_str(labels="friend|family|academic|work")+\
                cls.node_to_str(identifier="t")+\
                " and f <> t "+\
            " match p1 = "+\
                cls.node_to_str("f")+\
                cls.relation_to_str(labels=f'friend|family|academic|work*1..{distance}')+\
                cls.node_to_str("s")+\
            " with s, length(p1) as saltos, collect(t) as t2 "+\
            cls.return_to_str(labels=["s","saltos+1","t2"],orderByAsc="saltos")

    # MATCH path = (inicio:Prueba)-[rs*1..6]->(final:Prueba)
    # where inicio < final
    # with path, [[ID(inicio), ID(final)],"Segundo",apoc.coll.pairsMin(nodes(path))[0][1],"Tercero",inicio] as segundos_y_terceros, length(path) as numSaltos where numSaltos>1
    # RETURN numSaltos, segundos_y_terceros as Segundos ORDER BY length(path) skip 1 

    #Q7
    @classmethod
    def messages_new_relationships(cls, username: str, min_messages: int) -> str :
        return " match "+\
            cls.node_to_str(identifier="f", labels=['user'], properties=cls.username_dict(username))+\
            " , " + cls.node_to_str(identifier="s", labels=['user'])+\
            " , " + cls.node_to_str(identifier="t", labels=['user'])+\
            " where not "+\
                cls.node_to_str(identifier="f")+\
                cls.relation_to_str(labels="friend|family|academic|work")+\
                cls.node_to_str(identifier="t")+\
                " and "+\
                cls.node_to_str(identifier="s")+\
                cls.relation_to_str(labels="friend|family|academic|work")+\
                cls.node_to_str(identifier="t")+\
                " and "+\
                cls.node_to_str(identifier="f")+\
                cls.relation_to_str(labels="friend|family|academic|work")+\
                cls.node_to_str(identifier="s")+\
                " and f<>t "+\
            " match "+\
                cls.node_to_str(identifier="f")+\
                cls.relation_to_str()+\
                cls.node_to_str(identifier="c1", labels=['chat'])+\
                cls.relation_to_str()+\
                cls.node_to_str(identifier="s")+\
                " , "+\
                cls.node_to_str(identifier="s")+\
                cls.relation_to_str()+\
                cls.node_to_str(identifier="c2", labels=['chat'])+\
                cls.relation_to_str()+\
                cls.node_to_str(identifier="t")+\
            f' where c1.sec + 1 > {min_messages} and c2.sec + 1 > {min_messages} '+\
            " with f, s, t, c1, c2 "+\
            cls.return_to_str(labels="t", orderByAsc="c1.sec , c2.sec")


    # match (f:user {username: 'Angela Smith'}), (s:user), (t:user), (f:user)-[:friend|family|academic|work]-(s:user), 
    # (f)--(c1:chat)--(s), (s)--(c2:chat)--(t)
    # where c1.sec > 2 and c2.sec > 2 and
    # not(f)-[:friend|family|academic|work]-(t)
    # return t 
    # order by c1.sec desc, c2.sec desc
