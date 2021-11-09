import redis
import json
import secrets
import random
from typing import Union
import constants.redis as rdK

class Sesion:
	data_keys = {'username','name','password','privilege'}
	sesion = None

	def __init__(self):
		self.__class__._init_class()

	def createSesion(self,**kwargs) -> Union[dict,None] :
		# Add 'privilege' if does not have it and check that the data is correct before dumping it in self
		if 'privilege' not in kwargs.keys():
			kwargs['privilege'] = 0
		self._filter(**kwargs)
		self.__dict__.update(kwargs)

		#Create the token
		token = secrets.token_hex(16)

		# It saves it on the redis server. If it already existed, it does not change it. 
		res = self.sesion.setnx(token,json.dumps({k:v for k,v in self.__dict__.items() if k in self.data_keys}))

		# In case it already exists, it returns -1. 
		if res == 0:
			return -1
		# If not, it returns token and privilege.
		else:
			self.sesion.expire(token,rdK.SESION_EXPIRATION_TIME)
			return {'token':token, 'privilege':self.__dict__['privilege']}

	# Check local data
	def verDatosUsuario(self) -> Union[dict,None] :
		#solo se comprueba username ya que si esta username, tambien estan el resto
		if 'username' in self.__dict__:
			return {k:v for k,v in self.__dict__.items() if k in self.data_keys}
		return None

	def loadUserData(self,token):
		# Loads user data from the server and dumps it into self
		res = self.sesion.get(token)
		if res is None:
			return -1
		userData = json.loads(res)
		self.__dict__.update(userData)

		return userData

	def updateUserData(self,token="",**kwargs) -> None :
		self._filter(**kwargs)
		
		# Checks that we have passed a correct token to it
		if token=="":
			return None

		# Update the data, and put the ttl back in
			# Although we know it exists because of the ttl, 
			# it is possible that when we get to loadUserData it has expired. 
			# So we check the return value of loadUserData to avoid errors with json.dumps()
		newData = self.loadUserData(token)
		if newData == -1:
			return None
		newData.update(kwargs)
		
		# Saves the remaining pttl of the session
		# If it is -1 it means that it did not exist
		pttlSesion = self.sesion.pttl(token)
		if pttlSesion==-1:
			return None
		
		# Update user data with newData
		self.sesion.set(token,json.dumps(newData))
		self.sesion.pexpire(token,pttlSesion)

	def loginToken(self,token) -> int :
		# Collect the 'privilege' field of the session. 
		# If it does not exist, returns -1
		res = self.sesion.get(token)
		if res is None:
			return -1
		return int(json.loads(res)['privilege'])

	def _filter(self, **kwargs) -> bool:
		args_set = set(kwargs.keys())

		# with set theory we check that |kwargs ∩ data_keys|=|data_keys|
		#if (len(args_set & self.data_keys) != len(self.data_keys)):
		if(not args_set.issubset(self.data_keys)):
			raise Exception('missing required variables on argument')
		return True

	@classmethod
	def _init_class(cls):
		cls.sesion = redis.Redis(host=rdK.DB_ADDRESS, port= rdK.DB_PORT, db=rdK.DB_SESION_INDEX, charset="utf-8", decode_responses=True)
		cls.sesion.config_set(rdK.REDIS_MAXMEM_STR, rdK.MAXMEM)
		cls.sesion.config_set(rdK.REDIS_POLICY_STR, rdK.POLICY)


if __name__ == '__main__':
	s = Sesion()
	sesion = s.createSesion(username='Paco123',name='Francisco',password='1a2b3c',privilege=random.randrange(7))
	print(f'sesion: ',sesion)
	print(f'datos usuario (en el objeto s): ',s.verDatosUsuario())
	print(f'privilege: ',s.loginToken(sesion['token']))
	s.updateUserData(token=sesion['token'],username='Pepe33',name='Jose')
	print(f'user data (loaded): ',s.loadUserData(sesion['token']))
	print(f'datos usuario despues de load-rlo (en el objeto s): ',s.verDatosUsuario())
	
