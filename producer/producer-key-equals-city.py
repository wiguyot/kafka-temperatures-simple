#!/usr/bin/env python3
import os
import time
import random
import json
from kafka import KafkaProducer

# Chargement des variables d’environnement
city = os.getenv("VILLE")
if not city:
    raise RuntimeError("Environment variable VILLE is required")

interval = os.getenv("INTERVAL")
if not interval:
    raise RuntimeError("Environment variable INTERVAL is required")
try:
    interval = float(interval)
except ValueError:
    raise RuntimeError("INTERVAL must be a number")

bootstrap = os.getenv("BOOTSTRAP_SERVERS")
if not bootstrap:
    raise RuntimeError("Environment variable BOOTSTRAP_SERVERS is required")
bootstrap_list = bootstrap.split(",")

topic = os.getenv("TOPIC_NAME")
if not topic:
    raise RuntimeError("Environment variable TOPIC_NAME is required")


# Création du producteur en ajoutant key_serializer pour la clé
try:
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_list,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8"),
    )
except Exception as e:
    raise RuntimeError(f"Failed to create KafkaProducer: {e}")

print(f"Producing to topic `{topic}` on {bootstrap_list} every {interval}s…")

# Boucle de production
while True:
    temperature = round(random.uniform(15.0, 30.0), 1)
    message = {
        "city": city,
        "temperature": temperature,
        "timestamp": int(time.time() * 1000)
    }
    # On passe maintenant la clé 'city' pour forcer le partitionnement par clé
    producer.send(topic, key=city, value=message)
    print("Produced →", message)
    time.sleep(interval)
