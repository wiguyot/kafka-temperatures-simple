# consumer/Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY consumer.py .
RUN pip install --no-cache-dir kafka-python

# CITY et INTERVAL seront passées par docker-compose
CMD ["python", "consumer.py"]
