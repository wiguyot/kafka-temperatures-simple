FROM python:3.12-slim

WORKDIR /app

# CHOOSE THE PRODUCER round-robin or key-equals-city
COPY producer-key-equals-city.py ./producer.py
#COPY producer-round-robin.py ./producer.py        



COPY wait-for-kafka.sh ./wait-for-kafka.sh

# install deps + make wait script executable
RUN pip install --no-cache-dir kafka-python \
 && chmod +x wait-for-kafka.sh

# first run wait-for-kafka, then hand off to python
ENTRYPOINT ["./wait-for-kafka.sh"]
CMD ["python", "./producer.py"]        