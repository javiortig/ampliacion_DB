from Models.Redes import Redes


if __name__ == "__main__":
    db = Redes()
    # db.create_user('Javi')
    # db.create_university('Utad')
    query = db.node_to_str(None, ['user', 'university'], {'username': 'Utad'}) \
            + db.relation_to_str(None, 'friendship', {'since': '1999'}, direction='<')\
            + db.node_to_str('b', 'user', {'username': 'Javi', 'age': '24'})
    
    print(query)
    