from Models.Redes import Redes


if __name__ == "__main__":
    db = Redes()
    # db.create_user('Javi')
    # db.create_university('Utad')

    print(db.driver.node_to_str(None, ['user', 'university'], {'username': 'Utad'}))