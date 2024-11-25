import redis as r
import psycopg2 as pg
import AplicacaoPrincipal as ap

class Conections:
    def __init__(self):
        self.dbRedis = r.StrictRedis(host='localhost', port=6379, db=0)
        self.dbPostgre = pg.connect(
            dbname="mydatabase",
            user="postgre",
            password="admin1234",
            host="localhost",
            port="5432"
        )
    
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
                    pacote[b'Destino'].decode('utf-8'),
                    pacote[b'Origem'].decode('utf-8'),
                    pacote[b'Peso'].decode('utf-8'),
                    pacote[b'Tamanho'].decode('utf-8')
                ))
                
                if i % 1000 == 0:
                    self.dbPostgre.commit()
                    print(f"{i} registros transferidos.")
            
            self.dbPostgre.commit() 
            print("Transferência concluída com sucesso.")
            
        except Exception as e:
            print(f"Erro durante a transferência de dados: {e}")

        
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