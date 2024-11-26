import redis as r
import psycopg2 as pg

class Conections:
    '''
    summary
        A classe Conections é responsável por criar as conexões com o banco de dados Redis e Postgre,
        além de transferir os dados do Redis para o Postgre.
        
    attributes 
        dbRedis : r.StrictRedis
            Conexão com o Redis.
        dbPostgre : pg.connect
            Conexão com o Postgre.
        
    methods 
        fecharConexoes() -> None
            Fecha as conexões com o Redis e Postgre.
        tranferirinfos() -> None
            Transfere os dados do Redis para o Postgre.
        CriaTabela() -> None
            Cria a tabela no Postgre
    '''
    def __init__(self) -> None:
        '''
        summary
            Inicializa as conexões com o Redis e Postgre, levando em consideração os parâmetros de conexão
            de cada banco de dados.
            
        parameters 
            None
                
        return
            None
        '''
        self.dbRedis = r.StrictRedis(host='localhost', port=6379, db=0)
        self.dbPostgre = pg.connect(
            dbname="mydatabase",
            user="postgre",
            password="admin1234",
            host="localhost",
            port="5432"
        )
    
    def fecharConexoes(self) -> None:
        '''
        summary
            Fecha as conexões com o Redis e Postgre, através do método close().
        
        parameters
            None
            
        attributes
            dbRedis : r.StrictRedis
            dbPostgre : pg.connect
            
        return
            None
        '''
        self.dbRedis.close()
        self.dbPostgre.close()
    
    def tranferirinfos(self) -> None:
        '''
        summary
            Transfere os dados do Redis para o Postgre, através de um loop que percorre os dados do Redis
            e insere no Postgre.
            
        parameters
            None
            
        attributes
            cursor : pg.cursor
            i : int
            pacote : dict
            
        return
            None
            
        raise
            Exception : Erro durante a transferência de dados.
        '''
        cursor = self.dbPostgre.cursor()
        try:
            for i in range(1, 1000001):
                pacote = self.dbRedis.hgetall(i)
                cursor.execute("""
                    INSERT INTO pacotes (id, Destino, Origem, Peso, Tamanho)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    i,
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

    def CriaTabela(self) -> None:
        '''
        summary
            Cria a tabela no Postgre, caso ela não exista. Para isso
            é utilizado o método execute() do cursor, que executa um comando SQL.

        parameters
            None
            
        attributes
            cursor : pg.cursor
            
        return
            None
        '''
        cursor = self.dbPostgre.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacotes (
                id SERIAL PRIMARY KEY,
                Destino VARCHAR(50),
                Origem VARCHAR(50),
                Peso VARCHAR(50),
                Tamanho VARCHAR(50)
            )
        """)
        self.dbPostgre.commit()
        cursor.close()

if __name__ == "__main__":
    '''
    summary
        Função principal que cria a tabela no Postgre, transfere os dados do Redis para o Postgre e fecha as conexões.
        
    parameters
        None
        
    return
        None
    '''
    con = Conections()
    con.CriaTabela()
    con.tranferirinfos()
    con.fecharConexoes()
