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
    enable_auto_commit=False,  # désactive le commit automatique
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

def on_commit(err, partitions):
    if err:
        print(f"Commit failed: {err}")

print(f"Consuming from topic `{topic}` on {bootstrap} with group `consumer-{city}`…")

try:
    for msg in consumer:
        data = msg.value
        print("Consumed ←", data)
        # commit non-bloquant après chaque message
        consumer.commit_async(callback=on_commit)
except KeyboardInterrupt:
    print("Interrupted, performing final commit…")
    # commit synchrone final
    consumer.commit()
finally:
    consumer.close()