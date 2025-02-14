# Usar uma imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos necessários para o container
COPY . /app

# Instalar as dependências do sistema necessárias para o rembg
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar as dependências Python necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Expôr a porta onde o Streamlit irá rodar
EXPOSE 8501

# Definir o comando para rodar o Streamlit
CMD ["streamlit", "run", "Editor.py"]