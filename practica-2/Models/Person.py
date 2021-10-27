import pymongo
import redis

from Models.Model import Model

from constants import models as modelsK
from constants import database as dbK
from constants import redis as redisK

# self.__dict__update(kwargs)
class Person(Model):
    cache = None


    def save(self):
        if (not self.data):
            raise Exception('no data to save on the person collection')

        # save it in cache
        person_cache_key = redisK.PERSON_C + redisK.KEY_SEP_C + str(self.data['national_id'])
        self.cache.hmset(person_cache_key, self.data)
        self.cache.expire(person_cache_key, redisK.EXPIRATION_TIME)
        #TODO: guardar los arrays aparte ya que en redis no se puede anidar


        # and then in the DB
        super().save()

    
    def find_by_id(self, national_id):
        pass

    @classmethod
    def _init_class(cls, db):
        # configure redis
        cls.cache = redis.Redis(host=redisK.DB_ADDRESS, port= redisK.DB_PORT, db=redisK.DB_INDEX)
        cls.cache.config_set(redisK.REDIS_MAXMEM_STR, redisK.MAXMEM)
        cls.cache.config_set(redisK.REDIS_POLICY_STR, redisK.POLICY)

        super()._init_class(db, model_name=dbK.DB_PERSON_KEY)

    