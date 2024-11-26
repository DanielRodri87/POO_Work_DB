import psycopg2 as pg

class Postgre:
    def __init__(self):
       self.dbPostgre = pg.connect(
            dbname="mydatabase",
            user="postgre",
            password="admin1234",
            host="localhost",
            port="5432"
        )
    
    def CriarTabela(self):
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

    def fecharConexao(self):
        self.dbPostgre.close()

