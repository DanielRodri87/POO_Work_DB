import redis # Biblioteca para interação com o Redis
import redis.exceptions # Exceções relacionadas ao Redis
from time import sleep # Função para aguardo de tentativas de conexão
import os # Biblioteca para acesso de variáveis de ambiente

'''
summary
    Este script realiza a conexão com o banco de dados Redis e insere dados fictícios.
    
attributes
    dbRedis : redis.Redis
        Conexão com o banco de dados Redis.
        
'''

# Loop para tentar estabelecer conexão com o Redis
while True:
    try: 

        '''
        summary
            Estabelece a conexão com o Redis. Caso o host do Redis não esteja especificado em uma
            variável de ambiente (`HOST_TO_REDIS`), utiliza o valor padrão 'localhost'.

        parameters
            None

        return
            redis.Redis
                Instância da conexão com o banco de dados Redis.
        '''
       
        # Obtém o host do Redis de uma variável de ambiente; se não estiver definida, usa 'localhost'
        redis_host = os.getenv('HOST_TO_REDIS', 'localhost')
        # Configura a conexão com o Redis
        dbRedis = redis.Redis(
                    host=redis_host, port=6379, decode_responses=True)
        print("Conexao estabelecida")
        break # Saída do loop
   
    # Tratamento de erro de conexão
    except redis.exceptions.ConnectionError:

        '''
        summary
            Caso ocorra uma exceção de conexão, exibe uma mensagem de erro e aguarda
            2 segundos antes de tentar novamente.

        parameters
            None

        return
            None
        '''

        print("Erro ao conectar")
        sleep(2) # Espera de 2 segundos antes de tentar novamente

# Povoamento do Redis com dados fictícios
# Estrutura: ID -> {Destino, Origem, Peso, Tamanho}
for i in range(1, 1000001):

    '''
    summary
        Insere 1.000.000 de registros fictícios no Redis utilizando hashes.
        Cada registro contém os seguintes campos:
        - Destino: ID + 1
        - Origem: ID
        - Peso: 1
        - Tamanho: 1

    parameters
        i : int
            Chave identificadora do hash no Redis.

    return
        None
    '''
    
    # i = Chave do hash no Redis
    dbRedis.hset(i, mapping={
        'Destino': i + 1, # Definição do campo 'Destino' como o ID + 1
        'Origem': i, # Definição do campo 'Origem' como o ID atual
        'Peso': 1, # Definição do campo 'Peso' como 1
        'Tamanho': 1 # Definição do campo 'Tamanho' como 1
    })

    