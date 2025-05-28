#!/usr/bin/env python3
import os
import json
from kafka import KafkaConsumer

# Chargement des variables d’environnement
city = os.getenv("VILLE")
if not city:
    raise RuntimeError("Environment variable VILLE is required")

bootstrap = os.getenv("BOOTSTRAP_SERVERS")
if not bootstrap:
    raise RuntimeError("Environment variable BOOTSTRAP_SERVERS is required")
bootstrap_list = bootstrap.split(",")

topic = os.getenv("TOPIC_NAME")
if not topic:
    raise RuntimeError("Environment variable TOPIC_NAME is required")

group_id = os.getenv("GROUP_ID", f"consumer-{city}")

# Initialisation du consommateur Kafka avec commit manuel
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_list,
    group_id=group_id,
    auto_offset_reset="earliest",
    enable_auto_commit=True,  # active le commit automatique
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print(f"Consuming from topic `{topic}` on {bootstrap_list} with group `{group_id}`…")

# Boucle de consommation
for record in consumer:
    print("Consumed ←", record.value)
