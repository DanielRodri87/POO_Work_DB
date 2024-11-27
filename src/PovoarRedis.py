import redis as r

# Conexão com o Redis
dbRedis = r.StrictRedis(host='localhost', port=6379, db=0)

# Povoando o Redis ID: {Destino, Origem, Peso, Tamanho}
for i in range(1, 1000001):
    dbRedis.hset(i, mapping={
        'Destino': i + 1,
        'Origem': i,
        'Peso': 1,
        'Tamanho': 1
    })

# Listando os 10 primeiros registros
for i in range(1, 11):
    print(dbRedis.hgetall(i))

# Listando os 10 últimos registros
for i in range(999991, 1000001):
    print(dbRedis.hgetall(i))

# Fechando a conexão
dbRedis.connection_pool.disconnect()

# Fim do arquivo PovoarRedis.py
