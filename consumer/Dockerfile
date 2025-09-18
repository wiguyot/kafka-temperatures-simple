FROM python:3.12-slim

WORKDIR /app

# CHOOSE THE CONSUMMER consumer-auto-commit OR read-then-commit OR async-commit
COPY consumer-read-then-commit.py ./consumer.py     
# COPY consumer-read-then-commit.py ./consumer.py     
# COPY consumer-async-commit.py ./consumer.py     



COPY wait-for-kafka.sh ./wait-for-kafka.sh

# install deps + make wait script executable
RUN pip install --no-cache-dir kafka-python \
 && chmod +x wait-for-kafka.sh

# first run wait-for-kafka, then hand off to python
ENTRYPOINT ["./wait-for-kafka.sh"]
CMD ["python","./consumer.py"]
