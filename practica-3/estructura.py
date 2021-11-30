# This will be the structure of the json where data will be loaded:
# username, type that can be: [basic, company, university]
# publishings with title, body and date.

# After users, their relations:
# relations [{user 1, user 2, type}]. El type de relations puede ser family, friend, work, academic
# academic > work > family > friend

{
    "users": [
        {    
            "username": "Pepito",
            "type": "basic"
        },
        {    
            "username": "Marga",
            "type": "basic"
        },
        {    
            "username": "Peluso",
            "type": "basic"
        },
        {    
            "username": "Apple",
            "type": "company"
        },
        {
            "username": "UPM",
            "type": "university"
        }
    ],
    "relations": [
                {
                    "from": "Apple",
                    "to": "Pepito",
                    "type": "work"
                },
                {
                    "from": "Apple",
                    "to": "UPM",
                    "type": "academic"
                },
                {
                    "from": "Marga",
                    "to": "Pepito",
                    "type": "family"
                },
                {
                    "from": "Peluso",
                    "to": "Pepito",
                    "type": "friend"
                }
            ],
    
    "chats": [
        {
            "sec": "2", 
            "from": "UPM",
            "to": "Marga",
            "messages":[
                {
                    "from": "UPM",
                    "to": "Marga",
                    "body": "persona, estudia en la upm",
                    "date": "2019-01-01T12:00:01[Europe/Madrid]",
                    "sec" : "0"
                },
                {
                    "from": "Marga",
                    "to": "UPM",
                    "body": "no me gusta estudiar",
                    "date": "2019-01-01T13:00:01[Europe/Madrid]",
                    "sec" : "1"
                },
                {
                    "from": "UPM",
                    "to": "Marga",
                    "body": "estudiar es weno. Espabila",
                    "date": "2019-01-01T14:00:01[Europe/Madrid]",
                    "sec" : "2"
                }
            ]
        },
        {
            
            "sec": "0", 
            "from": "Apple",
            "to": "UPM",
            "messages":[
                {
                    "from": "Apple",
                    "to": "UPM",
                    "body": "hola universidad, pasame gente",
                    "date": "2014-01-01T00:00:01[Europe/Madrid]",
                    "sec" : "0"
                }
            ]
        }
        
    ],

    "publishings": [
        {
            "author": "Pepito",
            "title": "Wood is brown",
            "date": "2019-01-01T00:00:01[Europe/Madrid]",
            "body": "blablablablablablablablablablablablablablablablablablablabla",
            "mentions": [
                "Marga"
            ]
        },
        {
            "author": "Pepito",
            "title": "Electricity is expensive",
            "date": "2021-11-11T00:00:01[Europe/Madrid]",
            "body": "Corrupcion, escasez. Corrupcion, escasez. Corrupcion, escasez. Corrupcion, escasez. Corrupcion, escasez. Corrupcion, escasez. Corrupcion, escasez. Corrupcion, escasez. "
        },
        {
            "author": "Marga",
            "title": "Ola que ase",
            "date": "2019-08-12T00:00:01[Europe/Madrid]",
            "body": "Ctemasoooo ",
            "mentions": [
                "Pepito", "UPM", "Apple"
            ]
        }
    ]

}


#db.query("LOAD CSV FROM 'file:////user_data.csv' AS data create (a:user {username:data[1]})") 

# Queries:
'''
match (n) detach delete n

call apoc.load.json("../vs/python_proyects/jotasones/data.json") yield value
unwind value.users as users

call apoc.merge.node(['user', users.type], {username: users.username}) yield node 

unwind value.relations as relations
match (f:user {username: relations.from})
match (t:user {username: relations.to}) 
call apoc.merge.relationship(f, relations.type, null, null, t, {}) yield rel 

unwind value.publishings as pubs
with distinct pubs, value
match (auth:user {username: pubs.author})
create (auth)-[:publishes]->(p:publishing {author: pubs.author, title: pubs.title, body: pubs.body, date: datetime(pubs.date)})

with distinct pubs, value, p
unwind pubs.mentions as mentions
match (men:user {username: mentions})
create (p)-[:mention]->(men)


with value
unwind value.chats as chats
with chats, value
match (m_f:user {username: chats.from})
match (m_t:user {username: chats.to}) 
merge (m_f)-[r1_chat:chats_with]->(c:chat {sec: chats.sec})<-[r2_chat:chats_with]-(m_t)

with value, chats
unwind chats.messages as messages
match (m_f:user {username: messages.from})
match (m_t:user {username: messages.to}) 
create (m_f)-[:message {body: messages.body, date: datetime(messages.date), sec: messages.sec}]->(m_t)

return count(chats)        

'''