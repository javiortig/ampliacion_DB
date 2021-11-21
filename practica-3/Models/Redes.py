from .Driver import Driver
from constants import neo4j as neo4jK

# This class will be accessed from the user

class Redes:
    def __init__(self):
        self.driver = Driver(neo4jK.ADDRESS, neo4jK.USERNAME, neo4jK.PASSWORD)

    def _add_user(self, type, username: str, kwargs):
        query_text = "CREATE (:" + username + ")"
        if (type == 'basic'):
            self.driver.query(query_text)
        elif (type == 'university'):
            pass
        elif (type == 'job'):
            pass



    # username must be unique
    def create_user(self, username: str, **kwargs):
        self._add_user('basic', username, kwargs)
