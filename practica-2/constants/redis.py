DB_PORT = 6379
DB_ADDRESS = 'localhost'
DB_INDEX = 2

REDIS_MAXMEM_STR = 'maxmemory'
MAXMEM = '150mb'

REDIS_POLICY_STR = "maxmemory-policy"
POLICY = "volatile-ttl"
EXPIRATION_TIME = 86400

KEY_SEP_C = ';'
PERSON_C = 'p'
STUDIES_C = 's'
JOBS_C = 'j'


# una persona tendra una key 'p;12344' siendo el numero su dni.
# Su universidad 's;12344' y sus trabajos 'j;12344'
# TODO: como guardar los studies de una persona?? como un array pero las fechas...
# a mi se me ocurre que el array tenga esta estructura: ['nombre_universidad;fecha_final']
# lo mismo para jobs