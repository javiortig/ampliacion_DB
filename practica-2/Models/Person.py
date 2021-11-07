import pymongo
import redis
from datetime import datetime
from typing import Union
import json

from Models.Model import Model

from constants import models as modelsK
from constants import database as dbK
from constants import redis as redisK

class Person(Model):
    cache = None

    @classmethod
    def _generate_redis_key(cls, national_id):
        return redisK.PERSON_C + redisK.KEY_SEP_C + str(national_id)

    def save(self):
        if (not self.data):
            raise Exception('no data to save on the person collection')

        # Save in cache serialized:
        person_serialized = json.dumps(self.data, default=str)
        self.cache.set(self._generate_redis_key(self.data['national_id']), person_serialized)

        # and then save data in the main DB
        super().save()

    # load = find_by_id
    @classmethod
    def load(cls, index) ->Union['Model', None]:
        # Extract person    
        person = cls.cache.get(cls._generate_redis_key(index))

        # Cache miss, load from mongo
        if not person:
            return super().load(index)

        # Else, we load from redis cache
        return Person(**json.loads(person))

    @classmethod
    def _init_class(cls, db):
        # configure redis
        cls.cache = redis.Redis(host=redisK.DB_ADDRESS, 
            port= redisK.DB_PORT,
            db=redisK.DB_INDEX,
            #Charset and decode to get byte results as string from redis
            charset="utf-8", 
            decode_responses=True)
        cls.cache.config_set(redisK.REDIS_MAXMEM_STR, redisK.MAXMEM)
        cls.cache.config_set(redisK.REDIS_POLICY_STR, redisK.POLICY)
        
        super()._init_class(db, model_name=dbK.DB_PERSON_KEY)

    