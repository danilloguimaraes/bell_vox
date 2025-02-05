# Usar uma imagem base leve do Python
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do repositório para dentro do container
COPY . /app

# Instalar dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Definir variável de ambiente para evitar buffer no log
ENV PYTHONUNBUFFERED=1

# Expor a porta padrão do Flask
EXPOSE 5000

# Comando para rodar a aplicação Flask
CMD ["python", "app/main/main.py"]
