import redis as r
import psycopg2 as pg

# Conexão com o Redis
dbRedis = r.StrictRedis(host='localhost', port=6379, db=0)

# Conectar-se ao PostgreSQL inicialmente para verificar e criar o banco
dbPostgre = pg.connect(
    dbname="postgres",
    user="postgre",       
    password="admin1234",        
    host="localhost",      
    port="5432"          
)

cursor = dbPostgre.cursor()

# Criar banco de dados se não existir
cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'mydatabase'")
exists = cursor.fetchone()

if not exists:
    cursor.execute("CREATE DATABASE mydatabase")

dbPostgre.commit()
cursor.close()
dbPostgre.close()

# Conectar-se ao banco de dados 'mydatabase' depois de garantir que existe
dbPostgre = pg.connect(
    dbname="mydatabase", 
    user="postgre", 
    password="admin1234", 
    host="localhost", 
    port="5432"
)

cursor = dbPostgre.cursor()

# Criar a tabela
def criarTabela():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacotes (
            ID SERIAL PRIMARY KEY,
            Destino VARCHAR(100) NOT NULL,
            Origem VARCHAR(100) NOT NULL, 
            Peso INT NOT NULL,
            Tamanho INT NOT NULL
        )
    """)
    dbPostgre.commit()

# Transferir os dados do Redis para o PostgreSQL
def transferirInfos():
    try:
        for i in range(1, 1000001):
            pacote = dbRedis.hgetall(i)
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
                dbPostgre.commit()
                print(f"{i} registros transferidos.")
        
        dbPostgre.commit() 
        print("Transferência concluída com sucesso.")
        
    except Exception as e:
        print(f"Erro durante a transferência de dados: {e}")

# Fechar a conexão com o Redis e o PostgreSQL
def fecharConexao():
    dbRedis.close()
    cursor.close()
    dbPostgre.close()

# Chamada das funções
criarTabela()
transferirInfos()

# Listando os 10 primeiros registros
cursor.execute("SELECT * FROM pacotes LIMIT 10")
print(cursor.fetchall())

# Listando os 10 últimos registros
cursor.execute("SELECT * FROM pacotes ORDER BY ID DESC LIMIT 10")
print(cursor.fetchall())

# Fechar as conexões
fecharConexao()
