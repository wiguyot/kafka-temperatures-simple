# En quoi ce projet valide la sémantique d'écriture "At-Least-Once" ?

Il faut deux conditions à remplir pour assurer une sémantique ALO : 
- Avoir une **politique d'écriture des messages (Producteur) qui garantisse l'écriture du message (```acks=all ou acks=1```).**
- Avoir une **polique de lecture des messages (Consommateur) qui garantisse le ```commit d'un offset après le traitement d'un message et donc ne pas utiliser l'autocommit.```

Cependant plusieurs éléments viennent limiter la garantie ALO : 
- **Producteur** : la politique ```acks=1``` accepte un risque de perte si le leader tombe avant réplication complète. Généralement suffisant pour une garantie « at-least-once » côté consommation, mais pas totalement sécurisé contre certaines défaillances.
- **Consommateur** : 
  - ```enable.auto.commit``` : Si activé, Kafka commit automatiquement les offsets à intervalles réguliers, ce qui peut mener à des duplications si les messages sont traités après que l'offset ait été automatiquement commit.
  - ```auto.commit.interval.ms``` : L’intervalle de temps entre deux commits automatiques, qui influence aussi les risques de duplication.
  - ```Traitement des erreurs côté consommateur``` : La stratégie de retry du consommateur, en cas d'erreurs dans le traitement des messages, influence aussi la fréquence de duplications potentielles.

Le cas du producteur ```acks=0``` implique un risque élevé de perte de message donc on ne satisfait par le besoin de délivrance au moins une fois du message.

En cas de charge un peu élevée de délivrance de message la politique ```acks=1``` peut rester acceptable en fonction de la criticité du contenu des messages versus les contraintes de validation des followers du leader de la partition.

## Exemple de traitement général de la lecture d'un message 

```python

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_list,
    group_id=group_id,
    auto_offset_reset="earliest",
    enable_auto_commit=False,  # désactive le commit automatique
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

for message in consumer:
    # Traitement complet du message
    process_message(message)

    # Commit explicite après le traitement
    consumer.commit()
```

## Exemple ```consumer-read-then-commit.py```

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
    print("Consumed ←", record.value)
    # commit manuel de l’offset immédiatement après traitement
    consumer.commit()
```

## exemple ```consumer-async-commit.py```

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
```