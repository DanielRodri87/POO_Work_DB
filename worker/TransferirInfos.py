import redis # Biblioteca para interação com o Redis
import psycopg2 # Biblioteca para conexão com PostgreSQL
from time import sleep # Função para aguardo de tentativas de conexão
import os # Biblioteca para acesso de variáveis de ambiente
import redis.exceptions # Exceções relacionadas ao Redis


'''
summary
    Este script gerencia conexões com Redis e PostgreSQL, realiza a transferência de dados 
    do Redis para o PostgreSQL e cria a tabela no banco de dados PostgreSQL, caso necessário.
    
attributes
    dbRedis : redis.Redis
        Conexão com o banco de dados Redis.
    dbPostgre : psycopg2.connection
        Conexão com o banco de dados PostgreSQL.
'''


class Conections:

    '''
    summary
        A classe Conections é responsável por gerenciar conexões com Redis e PostgreSQL, 
        criar a tabela no banco de dados PostgreSQL e transferir dados do Redis para PostgreSQL.
    
    methods
        fecharConexoes() -> None
            Fecha as conexões com Redis e PostgreSQL.
        tranferirinfos() -> None
            Transfere informações do Redis para PostgreSQL.
        CriaTabela() -> None
            Cria a tabela no PostgreSQL.
    '''


    def __init__(self):

        '''
        summary
            Inicializa conexões com Redis e PostgreSQL.
            Para o Redis, utiliza uma variável de ambiente `HOST_TO_REDIS` para obter o host,
            com valor padrão 'localhost'. 
            Para o PostgreSQL, utiliza uma variável de ambiente `HOST_TO_POSTGRES` para obter o host,
            com valor padrão 'localhost'.
            
        parameters
            None
            
        return
            None
        '''

        # Define o host do Redis pela variável de ambiente ou usa 'localhost'
        redis_host = os.getenv('HOST_TO_REDIS', 'localhost')
        # Configura a conexão com o Redis
        self.dbRedis = redis.Redis(host=redis_host, port=6379, decode_responses=True)

        # Loop para tentar estabelecer conexão com o PostgreSQL
        while True:
            try:
                # Define o host do PostgreSQL pela variável de ambiente ou usa 'localhost'
                post_host = os.getenv('HOST_TO_POSTGRES', 'localhost')
                self.dbPostgre = psycopg2.connect(
                    dbname="mydatabase", # Nome do banco de dados
                    user="root", # Usuário do banco de dados
                    password="root", # Senha do banco de dados
                    host=post_host, # Host do banco de dados
                    port="5432" # Porta do banco de dados
                )
                print("Conexao estabelecida")
                break # Saída do loop
            # Exceção caso a conexão com PostgreSQL falhe
            except psycopg2.OperationalError:
                print('Nao foi possivel conectar')
                sleep(2) # Espera de 2 segundos antes de tentar novamente
    
    def fecharConexoes(self):
        '''
        summary
            Fecha as conexões ativas com o Redis e o PostgreSQL.
        
        parameters
            None
            
        return
            None
        '''
        self.dbRedis.close() # Fecha a conexão com o Redis
        self.dbPostgre.close() # Fecha a conexão com o PostgreSQL
    
    def tranferirinfos(self):

        '''
        summary
            Transfere os dados armazenados no Redis para a tabela `pacotes` no PostgreSQL.
            Cada registro no Redis é inserido na tabela utilizando um loop iterativo.
            Em caso de erro, a transação é revertida.
        
        parameters
            None
            
        return
            None
        '''

        # Cria um cursor para executar comandos no PostgreSQL
        cursor = self.dbPostgre.cursor()
        try:
            # Itera sobre os registros de 1 até 1.000.000
            for i in range(1, 1000001):
                # Obtém os dados do Redis para o ID atual
                pacote = self.dbRedis.hgetall(i)
                cursor.execute("""
                    INSERT INTO pacotes (Destino, Origem, Peso, Tamanho)
                    VALUES (%s, %s, %s, %s)
                """, (
                    pacote['Destino'], # Insere o campo 'Destino'
                    pacote['Origem'], # Insere o campo 'Origem'
                    pacote['Peso'], # Insere o campo 'Peso'
                    pacote['Tamanho'] # Insere o campo 'Tamanho'
                ))
                
                
                self.dbPostgre.commit()
                print(f"{i} registros transferidos.")
            
            # Realiza o commit final após transferência de todos os registros
            self.dbPostgre.commit() 
            print("Transferência concluída com sucesso.")
            
        except Exception as e:

            '''
            summary
                Trata erros ocorridos durante a transferência de dados do Redis para PostgreSQL.
                Exibe a mensagem do erro e realiza rollback para desfazer transações parciais.
            
            parameters
                e : Exception
                    Exceção gerada durante a execução.
            
            return
                None
            '''

            print(f"Erro durante a transferência de dados: {e}")
            # Desfaz transações parciais em caso de erro
            self.dbPostgre.rollback()
        finally:
            # Fecha o cursor após a execução
            cursor.close() 

    def CriaTabela(self):

        '''
        summary
            Cria a tabela `pacotes` no PostgreSQL, caso ela não exista. 
            A tabela contém os campos: Destino, Origem, Peso e Tamanho.
        
        parameters
            None
            
        return
            None
        '''

        # Cria um cursor para executar comandos no PostgreSQL
        cursor = self.dbPostgre.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacotes (
                Destino VARCHAR(50),
                Origem VARCHAR(50),
                Peso VARCHAR(50),
                Tamanho VARCHAR(50)
            )
        """)

        # Realiza o commit após criação da tabela
        self.dbPostgre.commit()
        # Fecha o cursor após a execução
        cursor.close() 

# Execução principal
if __name__ == "__main__":
    con = Conections() # Instância da classe Conections
    con.CriaTabela() # Cria a tabela no PostgreSQL
    con.tranferirinfos() # Transfere os dados do Redis para PostgreSQL
    con.fecharConexoes() # Fecha as conexões ativas