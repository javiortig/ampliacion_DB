import redis
import json
import secrets
from typing import Union
import constants.redis as rdK

class Sesion:
    data_keys = ['username','name','password','privilege']
    sesion = None

    def createSesion(self,privilege=0,**kwargs) -> Union[dict,None] :
        # Add 'privilege' and check that the data is correct before dumping it in self
        kwargs['privilege'] = privilege
        self._filter(**kwargs)
        self.__dict__.update(kwargs)
        
        #Create the token
        token = secrets.token_hex(16)

        # It saves it on the redis server. If it already existed, it does not change it. 
        res = self.sesion.setnx(token,json.dumps({k:v for k,v in self.__dict__.items() if k in self.data_keys}))
        
        # In case it already exists, it returns -1. 
        if res == 0:
            return 1
        # If it exists, it returns token and privilege.
        else:
            self.sesion.expire(token,rdK.SESION_EXPIRATION_TIME)
            return {'token':token, 'privilege':self.__dict__['privilege']}
        
    #Para comprobar que funciona bien despues borrar(?)
    def verDatosUsuario(self) -> Union[dict,None] :
        #solo se comprueba username ya que si esta username, tambien estan el resto
        if 'username' in self.__dict__:
            return {k:v for k,v in self.__dict__.items() if k in self.data_keys}
        return None
    
    def loadUserData(self,token):
        # Loads user data from the server and dumps it into self
        userData = json.loads(self.sesion.get(token))
        self.__dict__.update(userData)

        return userData

    def updateUserData(self,token="",**kwargs) -> None :
        # Checks that we have passed a correct token to it
        if token=="":
            return None

        # Saves the remaining ttl of the session
        # If it is -1 it means that it did not exist
        ttlSesion = self.sesion.ttl(token)
        if ttlSesion==-1:
            return None
        
        # Update the data, and put the ttl back in
        self.sesion.set(token,self.loadUserData())
        self.sesion.expire(token,ttlSesion)
    
    def loginToken(self,token) -> int :
        # Collect the 'privilege' field of the session. 
        # If it does not exist, returns -1
        res = self.sesion.get(token,'privilege')
        if res is None:
            res = -1
        return int(res)

    def _filter(self, **kwargs) -> bool:
        args_set = set(kwargs.keys())

        # with set theory we check that |kwargs ∩ data_keys|=|data_keys|
        if (len(args_set & self.data_keys) != len(self.data_keys)):
            raise Exception('missing required variables on argument')
        return True

    @classmethod
    def _init_class(cls):
        cls.sesion = redis.Redis(host=rdK.DB_ADDRESS, port= rdK.DB_PORT, db=rdK.DB_SESION_INDEX)
        cls.sesion.config_set(rdK.REDIS_MAXMEM_STR, rdK.MAXMEM)
        cls.sesion.config_set(rdK.REDIS_POLICY_STR, rdK.POLICY)
