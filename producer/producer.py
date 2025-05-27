import os, json, random, time, datetime
from kafka import KafkaProducer

city      = os.getenv("CITY")                       # ex. Paris
interval  = float(os.getenv("INTERVAL", "1"))       # ex. 1, 5, 20 …
bootstrap = os.getenv("BOOTSTRAP_SERVERS",
                      "kafka-1:9092").split(",")

producer = KafkaProducer(
    bootstrap_servers=bootstrap,
    key_serializer   = lambda k: k.encode(),
    value_serializer = lambda v: json.dumps(v).encode(),
)

while True:
    record = {
        "city":        city,
        "temperature": round(random.uniform(-10, 40), 1),
        "timestamp":   datetime.datetime.utcnow().isoformat() + "Z",
    }
    producer.send("weather", key=city, value=record)
    producer.flush()
    time.sleep(interval)          # ← tempo paramétrable
