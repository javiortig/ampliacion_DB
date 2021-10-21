import pymongo

from Models.Model import Model

from constants import models as modelsK
from constants import database as dbK

# self.__dict__update(kwargs)
class Person(Model):

    def save(self):
        if (not self.data):
            raise Exception('no data to save on the person collection')

        # # Update it in university too, if exists
        # if ('studies' in self.data):
        #     university_index = modelsK[dbK.DB_UNIVERSITY_KEY][0]
        #     for s in self.data['studies']:
        #         # Check if university exists in collection. 
        #         query = {university_index: s}
        #         res = self.collection.find_one(query)
        #         if (self.db[dbK.DB_UNIVERSITY_KEY]):

        
        super().save()

    @classmethod
    def _init_class(cls, db):
        super()._init_class(db, model_name=dbK.DB_PERSON_KEY)