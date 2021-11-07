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

# TODO: hacerlo todo serializado con un json y no hace falta dividirlo en 3
# una persona tendra una key 'p;12344' siendo el numero su dni.
# Su estudios 's;12344' y sus trabajos 'j;12344'
# a mi se me ocurre que el array tenga esta estructura: ['nombre_universidad;fecha_final']
# lo mismo para jobs