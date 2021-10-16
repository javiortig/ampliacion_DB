import pymongo

from Models.Model import Model

from constants import models as modelsK
from constants import database as dbK

# self.__dict__update(kwargs)
class Company(Model):
    @classmethod
    def _init_class(cls, db):
        super()._init_class(db, model_name=dbK.DB_COMPANY_KEY)
        #uwu