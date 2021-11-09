import redis
import json
from typing import Union
import constants.redis as rdK

class Sesion:
    data_keys = ['username','name','password','privilege']
    sesion = None

    def _crearSesion(self,sobreescribir=False,**kwargs) -> dict :
        self._filter(**kwargs)

        sesion_data = kwargs
        sesion_data['privilege'] = 123
        token = '1d84n1sd491ds7k'

        #TODO si ya existe que no haga nada?
        if sobreescribir or 0 == self.sesion.exists(token):
            pipeline = redis.pipeline()
            pipeline.set(token,json.dumps(sesion_data))
            pipeline.ttl(token)
            pipeline.execute()
        
        self.__dict__.update(sesion_data)
        return sesion_data
        
    #Para comprobar que funciona bien despues borrar(?)
    def verDatosUsuario(self) -> Union[dict,None] :
        #solo se comprueba username ya que si esta username, tambien estan el resto
        if 'username' in self.__dict__:
            return {k:v for k,v in self.__dict__.items() if k in self.data_keys}
        return None

    def actualizarDatosUsuario(self,**kwargs) -> None :
        args_set = set(kwargs.keys())

        # rellenamos los datos que noe estamos actualizando con los que tenemos
        if args_set.issubset(self.data_keys): # and (self.data_keys - args_set) in self.__dict__
            for k in (self.data_keys - args_set):
                kwargs[k] = self.__dict__[k]

        self._crearSesion(sobreescribir=True,**kwargs)

    def loginNuevo(self,**kwargs) -> dict :
        return self._crearSesion(**kwargs)
    
    def loginToken(self,token) -> int :
        return self.sesion.get(token,'privilege')

    def _filter(self, **kwargs) -> bool:
        args_set = set(kwargs.keys())

        # with set theory we check that |kwargs ∩ data_keys|=|data_keys|
        if (len(args_set & self.data_keys) != len(self.data_keys)):
            raise Exception('missing required variables on argument')
        return True

    @classmethod
    def _init_class(cls):
        # cls.sesion = redis.Redis(host=redisK.DB_ADDRESS, port= redisK.DB_PORT, db=redisK.DB_INDEX)
        # cls.sesion.config_set(redisK.REDIS_MAXMEM_STR, redisK.MAXMEM)
        # cls.sesion.config_set(redisK.REDIS_POLICY_STR, redisK.POLICY)
        cls.sesion = redis.Redis(host=rdK.DB_ADDRESS, port= rdK.DB_PORT, db=rdK.SESION_INDEX)
        cls.sesion.config_set(rdK.REDIS_MAXMEM_STR, rdK.MAXMEM)
        cls.sesion.config_set(rdK.REDIS_POLICY_STR, rdK.POLICY)
