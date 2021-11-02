import pymongo
import redis
from datetime import datetime

from Models.Model import Model

from constants import models as modelsK
from constants import database as dbK
from constants import redis as redisK

# self.__dict__update(kwargs)
class Person(Model):
    cache = None

    #TODO: optimizar haciendo algunas variables en el constructor: ex person_cache_keys
    def save(self):
        if (not self.data):
            raise Exception('no data to save on the person collection')

        # save it in cache TODO: NO LO HE PROBADO
        # Creates the person key, studies key and jobs key used with redis
        person_cache_keys = []
        person_cache_keys.append(redisK.PERSON_C + redisK.KEY_SEP_C + str(self.data['national_id']))
        person_cache_keys.append(redisK.STUDIES_C + redisK.KEY_SEP_C + str(self.data['national_id']))
        person_cache_keys.append(redisK.JOBS_C + redisK.KEY_SEP_C + str(self.data['national_id']))

        # Structure the data for our cache scheme
        temp_data = self.data.copy()
        temp_studies = temp_data.pop('studies')
        if 'jobs' in temp_data:
            temp_jobs = temp_data.pop('jobs')
        else:
            temp_jobs = None

        # Makes sures all the required variables exists
        if (not temp_studies):
            raise Exception('no studies array provided')
        
        # Save persons general data in cache
        self.cache.hmset(person_cache_keys[0], temp_data)
        
        #studies = [{'university':'Utad','final':datetime.strptime('19/04/2000', "%d/%m/%Y")}]
        #On Redis: ['nombre_universidad;fecha_final']
        # First deletes the old list
        self.cache.delete(person_cache_keys[1])
        for s in temp_studies:
            self.cache.rpush(person_cache_keys[1], s['university'] + redisK.KEY_SEP_C + str(s['final']))

        # Save jobs array if exists TODO:
        if temp_jobs:
            for j in temp_jobs:
                self.cache.rpush(person_cache_keys[2], j)
        
        # Set the expiration time:
        for key in person_cache_keys:
            self.cache.expire(key, redisK.EXPIRATION_TIME)


        # and then save data in the main DB
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

    