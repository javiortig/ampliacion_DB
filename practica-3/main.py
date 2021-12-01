from Models.Redes import Redes
# USER MUST INSTALL APOC LIBRARY

if __name__ == "__main__":
    db = Redes()
    user1 = 'Margarita F'
    user2 = 'Juana C'
    user3 = 'Andy P'
    user4 = 'Juan Z'
    user5 = 'Josefa Johnson'
    userS1 = "Joe Valdes"
    userT1 = "Joe G"
    userS2 = "Universidad Rey Juan Carlos (URJC)"
    userT2 = "Angela Smith"
    distance = 4
    min_messages = 1

    # Load data to new empty db
    db.query('match (n) detach delete n')
    # ../vs/python_proyects/jotasones/data.json
    db.query(db.load_json("ampliacion-db/ampliacion_DB/practica-3/superdata.json"))
    # db.query(db.load_json("superdata.json"))

    db.query(db.create_publication(user5, "2019-08-12T00:00:01[Europe/Madrid]", "Soy guapa", "Asi soy asi soy jeje", [user1, user4]))
    db.query(db.create_publication(user4, "2019-08-12T00:00:01[Europe/Madrid]", "Juan soy sin mencion", "Asi soy asi soy jeje"))
    db.query(db.create_company("Applesitos"))
    db.query(db.create_company("Googlesitos", Ricos="Si", guapos="También"))
    db.query(db.create_user("Pablo Ramos", Admin="Si"))
    db.query(db.create_university("TBU", Admin="Si"))
    db.query(db.create_university("UUU"))
    db.query(db.delete_user("UUU"))

    db.query(db.new_message_to_str("Hola guapeton", "2019-08-12T00:00:01[Europe/Madrid]", user1, user2))
    db.query(db.new_message_to_str("Que pasa juani", "2020-08-12T00:00:01[Europe/Madrid]", user2, user1))
    db.query(db.new_message_to_str("Hola guapeton segundo", "2021-08-12T00:00:01[Europe/Madrid]", user1, user2))

    db.query(db.new_message_to_str("hola 1", "2019-08-12T00:00:01[Europe/Madrid]", userS2, user3))
    db.query(db.new_message_to_str("hola 2", "2019-08-12T00:00:01[Europe/Madrid]", userS2, user3))
    db.query(db.new_message_to_str("hola 3", "2019-08-12T00:00:01[Europe/Madrid]", user3 , userS1))
    db.query(db.new_message_to_str("hola 4", "2019-08-12T00:00:01[Europe/Madrid]", user3, userS2))


    db.query(db.new_message_to_str("Hola guapeton tercero", "2019-08-12T00:00:01[Europe/Madrid]", userS1, userT1))
    db.query(db.new_message_to_str("Hola guapeton tercero soy simp", "2019-08-12T00:00:01[Europe/Madrid]", userT1, userS1))
    db.query(db.new_message_to_str("Hola guapeton tercero soy simp2", "2019-08-12T00:00:01[Europe/Madrid]", userT1, userS1))
    db.query(db.new_message_to_str("a", "2019-08-12T00:00:01[Europe/Madrid]", userS2, userT2))
    db.query(db.new_message_to_str("b", "2019-08-12T00:00:01[Europe/Madrid]", userS2, userT2))
    db.query(db.new_message_to_str("c", "2019-08-12T00:00:01[Europe/Madrid]", userT2, userS2))
    db.query(db.new_message_to_str("d", "2019-08-12T00:00:01[Europe/Madrid]", userT2, userS2))
    db.query(db.new_message_to_str("e", "2019-08-12T00:00:01[Europe/Madrid]", userT2, userS2))
    db.query(db.new_message_to_str("f", "2019-08-12T00:00:01[Europe/Madrid]", userT2, userS2))
    db.query('match (a:user:basic {username:"'+user5+'"})-[:publishes]->(:publishing)-[:mention]->(b) create (a)-[w:work]->(b)')

    print("Friends and Family of user: " + user1)
    Q1 = db.query(db.friend_and_family_to_str(user1))
    print(Q1)

    print("\n\n\n\n")
    print("Family of family of user: " + user1)
    Q2 = db.query(db.family_of_family_to_str(user1))
    print(Q2)

    print("\n\n\n\n")
    print("Messages after date between users: " + user1 + " and " + user2)
    Q3 = db.query(db.messages_after_date_to_str(username_a=user1, username_b=user2,datetime="2019-09-11T22:43:15[Europe/Madrid]"))
    print(Q3)

    print("\n\n\n\n")
    print("Full chat between users: " + user1 + " and " + user2)
    Q4 = db.query(db.conversation_between_users_to_str(username_a=user1, username_b=user2))
    print(Q4)

    print("\n\n\n\n")
    print("Users mentioned in a plublishing from user " + user5 + " that have a work relationship")
    Q5 = db.query(db.mentioned_users_with_laboral_relation(username=user5))
    print(Q5)

    print("\n\n\n\n")
    print("New relationships for user " + user4 +"  with distance " + str(distance) + " or less")
    Q6 = db.query(db.distance_new_relationships(distance=distance, username=user4))
    print(Q6)

    print("\n\n\n\n")
    print("New relationships for user " + user3 + " based on " + str(min_messages) +  " message interactions")
    print(db.messages_new_relationships(user3,min_messages=min_messages))
    Q7 = db.query(db.messages_new_relationships(user3,min_messages=min_messages))
    print(Q7)

    
