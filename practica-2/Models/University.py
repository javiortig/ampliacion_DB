import pymongo

from Models.Model import Model

from constants import models as modelsK
from constants import database as dbK

# self.__dict__update(kwargs)
class University(Model):

    def save(self):
        if (not self.data):
            raise Exception('no data to save on the university collection')
        
        super().save()

    @classmethod
    def _init_class(cls, db):
        super()._init_class(db, model_name=dbK.DB_UNIVERSITY_KEY)