import redis
import json
from typing import Union
import constants.redis as rdK

class HelpDesk:
    helpDesk = None
    zname = "peticiones"

    #TODO la prioridad debe de estar dada por el usuario, o se le da por otros medios?
    @classmethod
    def realizarPeticion(cls,user_id,priority):
        self.helpDesk.zadd(self.zname,{user_id,priority},nx=True)

    @classmethod
    def obtenerPeticion(cls) ->str:
        #timeout=0 espera indefinidamente
        #el [1] es porque devuelve [key,value,score], lo que en este caso seria ["peticiones",id_usuario,prioridad]
        return self.helpDesk.bzpopmax(self.zname,timeout=0)[1]

    @classmethod
    def _init_class(cls):
        # cls.helpDesk = redis.Redis(host=redisK.DB_ADDRESS, port= redisK.DB_PORT, db=redisK.DB_INDEX)
        # cls.helpDesk.config_set(redisK.REDIS_MAXMEM_STR, redisK.MAXMEM)
        # cls.helpDesk.config_set(redisK.REDIS_POLICY_STR, redisK.POLICY)
        cls.helpDesk = redis.Redis(host=rdK.DB_ADDRESS, port= rdK.DB_PORT, db=rdK.HELPDESK_INDEX)
        cls.helpDesk.config_set(rdK.REDIS_MAXMEM_STR, rdK.MAXMEM)
        cls.helpDesk.config_set(rdK.REDIS_POLICY_STR, rdK.POLICY)
