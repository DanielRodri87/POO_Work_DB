import psycopg2 as pg

class Postgre:
    """
    summary
        Classe responsável por gerenciar a conexão e operações no banco de dados PostgreSQL.
    
    methods
        CriarTabela()
            Cria a tabela 'pacotes' no banco de dados.
        inserirPacote(destino, origem, peso, tamanho)
            Insere um novo pacote na tabela 'pacotes'.
        consultarPacotes()
            Retorna todos os pacotes armazenados no banco de dados.
        atualizarPacote(destino, peso_novo, tamanho_novo)
            Atualiza o peso e tamanho de um pacote com base no destino.
        deletarPacote(destino)
            Remove um pacote da tabela com base no destino.
        fecharConexao()
            Fecha a conexão com o banco de dados PostgreSQL.
    """
    def __init__(self):
        """
        summary
            Inicializa a conexão com o banco de dados PostgreSQL.
        
        parameters
            None
        """
        self.dbPostgre = pg.connect(
            dbname="mydatabase",  # Nome do banco de dados
            user="root",          # Usuário do banco de dados
            password="root",      # Senha do banco de dados
            host="localhost",     # Host onde o banco está rodando
            port="5432"           # Porta de conexão do PostgreSQL
        )
    
    def CriarTabela(self):
        """
        summary
            Cria a tabela 'pacotes' no banco de dados, caso não exista.
        
        parameters
            None
        
        return
            None
        """
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

    def inserirPacote(self, destino, origem, peso, tamanho):
        """
        summary
            Insere um novo pacote no banco de dados.
        
        parameters
            destino : str
                Destino do pacote.
            origem : str
                Origem do pacote.
            peso : str
                Peso do pacote.
            tamanho : str
                Tamanho do pacote.
        
        return
            None
        """
        cursor = self.dbPostgre.cursor()
        cursor.execute("""
            INSERT INTO pacotes (Destino, Origem, Peso, Tamanho) 
            VALUES (%s, %s, %s, %s)
        """, (destino, origem, peso, tamanho))
        self.dbPostgre.commit()
        cursor.close()

    def consultarPacotes(self):
        """
        summary
            Consulta e retorna todos os pacotes cadastrados na tabela.
        
        parameters
            None
        
        return
            list
                Lista com os pacotes cadastrados.
        """
        cursor = self.dbPostgre.cursor()
        cursor.execute("SELECT * FROM pacotes")
        pacotes = cursor.fetchall()
        cursor.close()
        return pacotes
    
    def atualizarPacote(self, destino, peso_novo, tamanho_novo):
        """
        summary
            Atualiza o peso e tamanho de um pacote com base no destino.
        
        parameters
            destino : str
                Destino do pacote a ser atualizado.
            peso_novo : str
                Novo peso do pacote.
            tamanho_novo : str
                Novo tamanho do pacote.
        
        return
            None
        """
        cursor = self.dbPostgre.cursor()
        cursor.execute("""
            UPDATE pacotes 
            SET Peso = %s, Tamanho = %s
            WHERE Destino = %s
        """, (peso_novo, tamanho_novo, destino))
        self.dbPostgre.commit()
        cursor.close()

    def deletarPacote(self, destino):
        """
        summary
            Remove um pacote da tabela com base no destino.
        
        parameters
            destino : str
                Destino do pacote a ser deletado.
        
        return
            None
        """
        cursor = self.dbPostgre.cursor()
        cursor.execute("""
            DELETE FROM pacotes 
            WHERE Destino = %s
        """, (destino,))
        self.dbPostgre.commit()
        cursor.close()

    def fecharConexao(self):
        """
        summary
            Fecha a conexão com o banco de dados PostgreSQL.
        
        parameters
            None
        
        return
            None
        """
        self.dbPostgre.close()

def exibir_menu():
    """
    summary
        Exibe o menu principal do sistema para o usuário.
    
    parameters
        None
    
    return
        None
    """
    print("\n")
    print("=====================================")
    print("         Sistema de Pacotes")
    print("=====================================")
    print("1. Inserir Pacote")
    print("2. Consultar Pacotes")
    print("3. Atualizar Pacote")
    print("4. Deletar Pacote")
    print("5. Sair")
    print("=====================================")

def main():
    """
    summary
        Função principal do programa. Controla o fluxo do sistema de pacotes.
    
    parameters
        None
    
    return
        None
    """
    db = Postgre()
    db.CriarTabela()  # Garante que a tabela exista no banco
    
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            destino = input("Digite o destino do pacote: ")
            origem = input("Digite a origem do pacote: ")
            peso = input("Digite o peso do pacote: ")
            tamanho = input("Digite o tamanho do pacote: ")
            db.inserirPacote(destino, origem, peso, tamanho)
            print("Pacote inserido com sucesso!")

        elif opcao == '2':
            pacotes = db.consultarPacotes()
            if pacotes:
                print("Pacotes cadastrados:")
                for pacote in pacotes:
                    print(f"Destino: {pacote[0]}, Origem: {pacote[1]}, Peso: {pacote[2]}, Tamanho: {pacote[3]}")
            else:
                print("Nenhum pacote encontrado.")

        elif opcao == '3':
            destino = input("Digite o destino do pacote a ser atualizado: ")
            peso_novo = input("Digite o novo peso do pacote: ")
            tamanho_novo = input("Digite o novo tamanho do pacote: ")
            db.atualizarPacote(destino, peso_novo, tamanho_novo)
            print("Pacote atualizado com sucesso!")

        elif opcao == '4':
            destino = input("Digite o destino do pacote a ser deletado: ")
            db.deletarPacote(destino)
            print("Pacote deletado com sucesso!")

        elif opcao == '5':
            db.fecharConexao()
            print("Conexão encerrada. Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
