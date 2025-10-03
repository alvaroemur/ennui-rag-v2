# Dockerfile-backend

# Imagem base
FROM python:3.9

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN pip install --upgrade fastapi
COPY . /app

COPY .env /app/.env
COPY *.json /app/

EXPOSE 7000

CMD ["python", "start_with_processor.py"]