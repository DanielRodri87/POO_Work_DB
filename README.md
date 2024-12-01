# 📄 Implementação Parcial do Sistema Gerenciador de Porto, Envolvendo os Bancos de Dados Redis e PostGreSQL

Esse repositório contém os arquivos necessários para rodar a atividade que consiste em implementar uma solução para simular a migração de dados entre serviços utilizando PostgreSQL como banco principal e Redis como fila de mensagens. Durante a execução do sistema, todos os componentes devem funcionar simultaneamente, demonstrando integração, processamento assíncrono e o uso eficiente de recursos limitados.

## 🔗 Ambiente de desenvolvimento

🔧 Python
```
Python 3.12.6
```

🔧 VSCode
```
1.95.3
f1a4fb101478ce6ec82fe9627c43efbf9e98c813
x64
```

## 🔗 História dos Releases
* 0.1
  * CREATE: PovoarRedis.py
  * CREATE: TransferirInfos.py
* 0.1.1
  * CHANGE: Refatorando o TransferirInfos.py
* 0.2
  * CREATE: AplicacaoPrincipal.py
* 0.3
  * CREATE: Arquivos e funções docker
* 0.3.1
  * CHANGE: Resolvendo conflitos do docker
* 0.4
  * ADD: documentação da aplicação
* 1.0
  * Etapa finalizada

## 🔗 Funcionamento e aplicabilidade

A aplicação consiste nas seguintes etapas:
1. Povoar o Redis com um número de registros pré-definidos
2. Após isso, o worker será responsável por pegar os dados no Redis e transferir para o PostGreSQL
3. Enquanto os dadso são transferidos, a aplicação principal (PostGreSQL) continua funcionando com algumas operações comuns

Após o povoamento, espera-se os seguintes cenários:
- O worker fazendo a transferência de dados do Redis para o PostGreSQL
![WhatsApp Image 2024-12-01 at 15 16 06](https://github.com/user-attachments/assets/b8c7dfde-dbc6-4fc5-ba94-9fa365472bdc)

- Menu da aplicação
![WhatsApp Image 2024-12-01 at 15 18 39](https://github.com/user-attachments/assets/b7643464-936c-42e0-ae38-d430669a32f6)

- Executando a operação de consulta, por exemplo
![WhatsApp Image 2024-12-01 at 15 19 13](https://github.com/user-attachments/assets/b258dfb4-1102-40d4-bba6-65492e03da02)

- Execução do htop
![WhatsApp Image 2024-12-01 at 15 21 48](https://github.com/user-attachments/assets/a4833b53-288d-45ad-8761-9193b8b01a63)

- Execução do docker stats
![WhatsApp Image 2024-12-01 at 15 22 35](https://github.com/user-attachments/assets/b9c4a1f8-7d96-4bba-bbc5-30803b12c9f1)

## 🔗Aproveite o sistema
1. Clone o repositório em sua máquina
```
git clone https://github.com/DanielRodri87/POO_Work_DB/
```
2. Garanta que tenha instalado a biblioteca necessária para o PostGreSQL
```
pip install psycopg2
```
3. Inicie o docker
```
docker compose up --build
```
4. Rode o arquivo para criar a fila de mensagens no Redis
```
python3 PovoarRedis.py
```
5. Rode o arquivo para transferir informações ao PostGreSQL
```
python3 TransferirInfos.py
```
6. Rode a aplicação principal
```
python3 AplicacaoPrincipal.py
```
7. Em um novo terminal, verifique a usabilidade da aplicação na máquina
```
htop
```
8. E o uso do Docker
```
docker stats
```
9. Explore a aplicação principal e se divirta!

## Detalhes
🔧 Desenvolvedores
1. Iago Roberto - iago.roberto@ufpi.edu.br
2. Luis Gustavo - luis.ramos@ufpi.edu.br
3. Daniel Rodrigues - daniel.sousa@ufpi.edu.br
4. Rita de Cássia - ritarodriguesilva19@gmail.com
5. Francinaldo de Sousa - francinaldo.barbosa@ufpi.edu.br

🔧 Licença

Essa aplicação está regida sobre a licença definida em `LICENSE`
