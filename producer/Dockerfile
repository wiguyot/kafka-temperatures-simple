# producer/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copie du script producteur
COPY producer.py .

# Installation de la bibliothèque Kafka
RUN pip install --no-cache-dir kafka-python

# Aucune variable d’environnement fixe ici :
#   CITY et INTERVAL sont injectées via docker-compose
CMD ["python", "producer.py"]
