import redis
import json
from typing import Union
import constants.redis as rdK

class HelpDesk:
    helpDesk = None
    zname = "peticiones"
    
    @classmethod
    def realizarPeticion(cls,user_id="null",numTicket="",priority=-1):
		# Stores user_id;numTicket, where ";" (rdK.KEY_SEP_C) is the separator
    	# nx=True -> if any, does not update the priority
    	cls.helpDesk.zadd(cls.zname,{user_id+rdK.KEY_SEP_C+str(numTicket):priority},nx=True)
    
    @classmethod
    def obtenerPeticion(cls) -> str :
    	# timeout=0 -> waits indefinitely
        # bzpopmax returns [key,value,score]
        return cls.helpDesk.bzpopmax(cls.zname,timeout=0)[1]

    @classmethod
    def init_class(cls):
        cls.helpDesk = redis.Redis(host=rdK.DB_ADDRESS, port= rdK.DB_PORT, db=rdK.DB_HELPDESK_INDEX, charset="utf-8", decode_responses=True)
        cls.helpDesk.config_set(rdK.REDIS_MAXMEM_STR, rdK.MAXMEM)
        cls.helpDesk.config_set(rdK.REDIS_POLICY_STR, rdK.POLICY)

if __name__ == '__main__':
	HelpDesk.init_class()
	
	print("Formato del ejemplo: userNUM;ticketNUM, el num de despues del ; no es la prioridad")
	HelpDesk.realizarPeticion("user3",3,7)
	HelpDesk.realizarPeticion("user4",4,6)      
	HelpDesk.realizarPeticion("user1",5,12)
	HelpDesk.realizarPeticion("user2","6",8)

	print(HelpDesk.obtenerPeticion())
	print(HelpDesk.obtenerPeticion())
	print(HelpDesk.obtenerPeticion())
	print(HelpDesk.obtenerPeticion())
	# Con el quinto se queda esperando indefinidamente a que haya un dato para obtener, ya que solo le metimos user1, 2, 3 y 4.
	# print(HelpDesk.obtenerPeticion())
