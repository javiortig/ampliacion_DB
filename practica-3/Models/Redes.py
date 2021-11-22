from .Driver import Driver
from constants import neo4j as dbK

from typing import Union

# This class will be accessed from the user

#TODO: hacer mejor que sea una herencia
class Redes:
    def __init__(self):
        self.driver = Driver(dbK.ADDRESS, dbK.USERNAME, dbK.PASSWORD)

    def _add_user(self, type, username: str, properties: Union[dict, None] = None):
        labels = ['user']

        if (type == 'basic'):
            pass 
        elif (type == 'university'):
            labels.append('university')
        elif (type == 'company'):
            labels.append('company')
        else:
            Exception('Internal error handling users')


        self.driver.query()


    # username must be unique
    def create_user(self, username: str, **kwargs):
        self._add_user('basic', username, kwargs)

    def create_university(self, username: str, **kwargs):
        self._add_user('university', username, kwargs)

    def create_company(self, username: str, **kwargs):
        self._add_user('company', username, kwargs)

    @classmethod
    def node_to_str(cls)
