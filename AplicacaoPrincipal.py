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
                ID SERIAL PRIMARY KEY,
                Destino VARCHAR(50),
                Origem VARCHAR(50),
                Peso VARCHAR(50),
                Tamanho VARCHAR(50)
            )
        """)
        self.dbPostgre.commit()
        cursor.close()

    def inserirPacote(self, destino, origem, peso, tamanho):
        cursor = self.dbPostgre.cursor()
        cursor.execute("""
            INSERT INTO pacotes (Destino, Origem, Peso, Tamanho) 
            VALUES (%s, %s, %s, %s)
        """, (destino, origem, peso, tamanho))
        self.dbPostgre.commit()
        cursor.close()

    def consultarPacotes(self):
        cursor = self.dbPostgre.cursor()
        cursor.execute("SELECT * FROM pacotes")
        pacotes = cursor.fetchall()
        cursor.close()
        return pacotes
    
    def atualizarPacote(self, id, peso_novo, tamanho_novo):
        cursor = self.dbPostgre.cursor()
        cursor.execute("""
            UPDATE pacotes 
            SET Peso = %s, Tamanho = %s
            WHERE ID = %s
        """, (peso_novo, tamanho_novo, id))
        self.dbPostgre.commit()
        cursor.close()

    def deletarPacote(self, id):
        cursor = self.dbPostgre.cursor()
        cursor.execute("""
            DELETE FROM pacotes 
            WHERE ID = %s
        """, (id,))
        self.dbPostgre.commit()
        cursor.close()

    def fecharConexao(self):
        self.dbPostgre.close()

def exibir_menu():
    print("\n")
    print("=====================================")
    print("         Sistema de Pacotes")
    print("=====================================")
    print("1. Criar Tabela")
    print("2. Inserir Pacote")
    print("3. Consultar Pacotes")
    print("4. Atualizar Pacote")
    print("5. Deletar Pacote")
    print("6. Sair")
    print("=====================================")

def main():
    db = Postgre()
    db.CriarTabela()
    
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("Tabela 'pacotes' verificada ou criada com sucesso!")
        
        elif opcao == '2':
            destino = input("Digite o destino do pacote: ")
            origem = input("Digite a origem do pacote: ")
            peso = input("Digite o peso do pacote: ")
            tamanho = input("Digite o tamanho do pacote: ")
            db.inserirPacote(destino, origem, peso, tamanho)
            print("Pacote inserido com sucesso!")

        elif opcao == '3':
            pacotes = db.consultarPacotes()
            if pacotes:
                print("Pacotes cadastrados:")
                for pacote in pacotes:
                    print(f"ID: {pacote[0]}, Destino: {pacote[1]}, Origem: {pacote[2]}, Peso: {pacote[3]}, Tamanho: {pacote[4]}")
            else:
                print("Nenhum pacote encontrado.")

        elif opcao == '4':
            id_pacote = input("Digite o ID do pacote a ser atualizado: ")
            peso_novo = input("Digite o novo peso do pacote: ")
            tamanho_novo = input("Digite o novo tamanho do pacote: ")
            db.atualizarPacote(id_pacote, peso_novo, tamanho_novo)
            print("Pacote atualizado com sucesso!")

        elif opcao == '5':
            id_pacote = input("Digite o ID do pacote a ser deletado: ")
            db.deletarPacote(id_pacote)
            print("Pacote deletado com sucesso!")

        elif opcao == '6':
            db.fecharConexao()
            print("Conexão encerrada. Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
