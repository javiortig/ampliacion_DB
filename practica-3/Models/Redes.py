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

    
    
    
#  familia, amistad, académico o laboral

# "match (username: javi)-[m:message fecha]-(username: javi)"
# "order by m.date"
# "return m"