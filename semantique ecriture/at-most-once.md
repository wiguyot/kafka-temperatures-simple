# Sémantique "At-Most-Once"

Pour assurer la sémantique AMO il faut que le ```commit de l'offset intervienne avant le traitement du message.``` Cela garantit que chaque message est consommé **au plus une fois**, mais **il peut être perdu*** si un soucis (crash, dysfonctionnement etc...) intervient juste après le commit et avant ou pendant le traitement.

## Exemple de fonctionnement général 

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'weather',
    bootstrap_servers=['localhost:9092'],
    enable_auto_commit=False,
    group_id='my-group'
)

for message in consumer:
    # ⚠️ Commit avant traitement => at-most-once
    consumer.commit()

    # Traitement du message (non garanti si crash)
    print(f"Reçu : {message.value}")
```

## adaptation de ```consumer-read-then-commit.py```

Attention on inverse la logique traitement du message/commit du message par rapport au fichier initial.


```python
#!/usr/bin/env python3
import os
import json
from kafka import KafkaConsumer

### blablabla

# Initialisation du consommateur Kafka avec commit manuel
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_list,
    group_id=group_id,
    auto_offset_reset="earliest",
    enable_auto_commit=False,  # désactive le commit automatique
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print(f"Consuming from topic `{topic}` on {bootstrap_list} with group `{group_id}`…")

# Boucle de consommation
for record in consumer:
    # ⚠️ Commit avant traitement => at-most-once
    consumer.commit()

    # Traitement du message (non garanti si crash)
    print("Consumed ←", record.value)
```

## adaptation de ```consumer-async-commit.py```

Attention on inverse la logique traitement du message/commit du message par rapport au fichier initial.

```python
#!/usr/bin/env python3
import os
import json
from kafka import KafkaConsumer

# blablabla

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

        # ⚠️ Commit async avant traitement
        consumer.commit_async(callback=on_commit)

         # Traitement du message (non garanti si crash)
        data = msg.value
        print("Consumed ←", data)

except KeyboardInterrupt:
    print("Interrupted, performing final commit…")
    # commit synchrone final
    consumer.commit()
finally:
    consumer.close()
```

## Le cas ```consumer-auto-commit.py```

Il possède : 

```python
enable_auto_commit=True
```

Ce qui signifie que l’offset est automatiquement commit périodiquement (par défaut toutes les 5 secondes via ```auto.commit.interval.ms```). Cela ne garantit pas un vrai at-most-once car :

- certains messages peuvent être traités sans que leur offset soit commité → ils peuvent être rejoués → ```donc at-least-once en pratique.```

| Sémantique         | Commit de l'offset         | Traitement du message        |
|--------------------|----------------------------|-------------------------------|
| **At-least-once**  | ```Après``` le traitement    | Garanti ≥1 fois, ```doublons possibles``` |
| **At-most-once**   | ```Avant``` le traitement    | ```Jamais de doublon, risque de perte``` |
