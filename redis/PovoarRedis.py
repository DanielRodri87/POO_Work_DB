import redis

import redis.exceptions
from time import sleep

import os
# Conexão com o Redis
while True:
    try:
        redis_host = os.getenv('HOST_TO_REDIS', 'localhost')
        dbRedis = redis.Redis(
                    host=redis_host, port=6379, decode_responses=True)
        print("Conexao estabelecida")
        break
    except redis.exceptions.ConnectionError:
        print("Erro ao conectar")
        sleep(2)

# Povoando o Redis ID: {Destino, Origem, Peso, Tamanho}
for i in range(1, 1000001):
    dbRedis.hset(i, mapping={
        'Destino': i + 1,
        'Origem': i,
        'Peso': 1,
        'Tamanho': 1
    })