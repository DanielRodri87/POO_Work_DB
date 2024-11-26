FROM python:3.10

# Instalação do htop
RUN apt-get update && apt-get install -y htop && apt-get clean

# Configura o diretório de trabalho
WORKDIR /app

# Copie os arquivos requirements.txt e o código para o diretório de trabalho
COPY requeriments.txt .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requeriments.txt

# Copie o código para o diretório de trabalho
COPY TransferirInfos.py .

# Execute o código
CMD ["python", "TransferirInfos.py"]
