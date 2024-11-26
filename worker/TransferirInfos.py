import redis
import psycopg2
# import AplicacaoPrincipal as ap
from time import sleep

import os

import redis.exceptions

class Conections:
    def __init__(self):
        redis_host = os.getenv('HOST_TO_REDIS', 'localhost')
        self.dbRedis = redis.Redis(host=redis_host, port=6379, decode_responses=True)

        while True:
            try:
                post_host = os.getenv('HOST_TO_POSTGRES', 'localhost')
                self.dbPostgre = psycopg2.connect(
                    dbname="mydatabase",
                    user="root",
                    password="root",
                    host=post_host,
                    port="5432"
                )
                print("Conexao estabelecida")
                break
            except psycopg2.OperationalError:
                print('Nao foi possivel conectar')
                sleep(2)
    
    def fecharConexoes(self):
        self.dbRedis.close()
        self.dbPostgre.close()
    
    def tranferirinfos(self):
        cursor = self.dbPostgre.cursor()
        try:
            for i in range(1, 1000001):
                pacote = self.dbRedis.hgetall(i)
                cursor.execute("""
                    INSERT INTO pacotes (Destino, Origem, Peso, Tamanho)
                    VALUES (%s, %s, %s, %s)
                """, (
                    pacote['Destino'],
                    pacote['Origem'],
                    pacote['Peso'],
                    pacote['Tamanho']
                ))
                
                self.dbPostgre.commit()
                print(f"{i} registros transferidos.")
            
            self.dbPostgre.commit() 
            print("Transferência concluída com sucesso.")
            
        except Exception as e:
            print(f"Erro durante a transferência de dados: {e}")
            self.dbPostgre.rollback()
        finally:
            cursor.close()

    def CriaTabela(self):
        cursor = self.dbPostgre.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacotes (
                Destino VARCHAR(50),
                Origem VARCHAR(50),
                Peso VARCHAR(50),
                Tamanho VARCHAR(50)
            )
        """)
        self.dbPostgre.commit()
        cursor.close()

if __name__ == "__main__":
    con = Conections()
    con.CriaTabela()
    con.tranferirinfos()
    con.fecharConexoes()