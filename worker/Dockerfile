# Base image com Python
FROM python:3.10

# Instala o htop
RUN apt-get update && apt-get install -y htop && apt-get clean

# Configura o diretório de trabalho
WORKDIR /app

# Copia o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instala as dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código para o contêiner
COPY . .

ENV HOST_TO_REDIS=redis
ENV HOST_TO_POSTGRES=postgres

# Comando padrão para executação
CMD ["python", "TransferirInfos.py"]