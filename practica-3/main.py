from Models.Redes import Redes


if __name__ == "__main__":
    db = Redes()
    datos = 'match (n) detach delete n\
    call apoc.load.json("../vs/python_proyects/jotasones/data.json") yield value\
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
    db.query(datos)
    
    Q1 = db.query(db.friend_and_family_to_str("Maria Q"))
    Q2 = db.query(db.family_of_family_to_str("Maria Q"))
    Q3 = db.query(db.messages_after_data_to_str(username_a="Maria Q", username_b="Joe Orti, Garcia",datetime="2007-10-17T21:43:15[Europe/Madrid]"))
    Q4 = db.query(db.conversation_between_users_to_str(username_a="Maria Q", username_b="Joe Orti, Garcia"))
    Q5 = db.query(db.mentioned_users_with_laboral_relation(username="Open University of Catalonia"))
    Q6 = db.query(db.distance_new_relationships(distance=4))
    Q7 = db.query(db.messages_new_relationships("Maria Q",min_messages=2))

