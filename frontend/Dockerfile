# Dockerfile-frontend

# Imagem base
FROM python:3.9

# Definir o diretório de trabalho no container
WORKDIR /app

ENV FRONTEND_URL='http://localhost:8501'
ENV BACKEND_URL='http://localhost:7000'
ENV BACKEND_URL_INTERNAL='http://backend:7000'

# Copiar os arquivos de dependências e instalar
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copiar o restante dos arquivos do projeto
COPY . /app

# Expose port
EXPOSE 8501

# Comando para executar a aplicação
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false"]
