import os, json, time
from kafka import KafkaConsumer

city      = os.getenv("CITY")                      # ex. Paris
interval  = float(os.getenv("INTERVAL", "1"))      # ex. 1, 5, 20
group_id  = os.getenv("GROUP_ID", f"group-{city}") # un groupe par ville
bootstrap = os.getenv("BOOTSTRAP_SERVERS",
                      "kafka-1:9092").split(",")

consumer = KafkaConsumer(
    "weather",
    bootstrap_servers=bootstrap,
    group_id=group_id,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    key_deserializer   = lambda k: k.decode() if k else None,
    value_deserializer = lambda v: json.loads(v.decode()),
)

for msg in consumer:
    if msg.value["city"] == city:
        print(msg.value, flush=True)
    time.sleep(interval)
