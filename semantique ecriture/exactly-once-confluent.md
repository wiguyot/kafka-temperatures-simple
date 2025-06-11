# Exactly Once Semantique (EOS)

Exactly-once : chaque message est livré exactement 1 fois sans perte et sans doublon. Cela nécessite : 
- un producteur idempotent : 
  - transaction kafka
  - commit d'offset dans la même transaction



Les **producteurs** (producer-\*.py) et **consommateurs** (consumer-\*.py) :

- Utilisent kafka-python, qui ne supporte pas les transactions (init_transactions, send_offsets_to_transaction, etc.).

- Ne committent pas d’offsets dans des transactions (impossible avec kafka-python).

- Il faudrait définir ```enable.idempotence=True (et acks=all)```, ce qui est requis même en préambule à l’EOS.

**Donc la sémantique Exactly-once n’est pas atteinte.**

## Support des transactions et des commits en ```java```

Producteur : chaque envoi de message doit être encadré par un ```beginTransaction``` et un ```commitTransaction```

Consommateur : chaque lecture et traitement d'un message doit être encadré par un ```beginTransaction``` et un ```commitTransaction```


## Exemple java d'un producteur EOS

IL FAUT VALIDER CET EXEMPLE !!!

```python 

```

## Exemple java d'un consommateur EOS

IL FAUT VALIDER CET EXEMPLE !!!

Dans l'exemple suivant on a pas de transaction au niveau du consommateur donc on va utiliser un "dummyProducer" pour avoir la notion de transaction. Les transactions seront utilisée pour enregistrement l'avancement de l'offset. 

Cela reste logique d'utiliser un dummyProducer pour initialiser la transaction car l'avancement de l'offset de consommation est bien écrit dans le topic.

Exemple de consommateur EOS simplifié (sans la gestion des erreurs). L'atomicité de ces transactions varie de 1 à de 10 ou alors c'est le nombre d'enregistrements lus en au plus 1000 millisecondes.

```python
from confluent_kafka import Producer, Consumer, TopicPartition
import uuid

BOOTSTRAP_SERVERS = "localhost:9092"
INPUT_TOPIC = "mon_topic"
GROUP_ID = "groupe_eos"

def process(msg):
    print(f"Traitement: clé={msg.key()} valeur={msg.value()} offset={msg.offset()}")

def main():
    consumer = Consumer({
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
        'isolation.level': 'read_committed',
    })

    producer = Producer({
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'transactional.id': f"eos-consume-{uuid.uuid4()}"
    })

    producer.init_transactions()
    consumer.subscribe([INPUT_TOPIC])

    while True:
        records = consumer.consume(num_messages=10, timeout=1.0)
        if not records:
            continue

        producer.begin_transaction()

        for msg in records:
            process(msg)

        offsets = []
        for msg in records:
            topic = msg.topic()
            partition = msg.partition()
            offset = msg.offset() + 1
            tp = TopicPartition(topic, partition, offset)
            offsets.append(tp)

        producer.send_offsets_to_transaction(
            offsets,
            consumer.consumer_group_metadata()
        )
        producer.commit_transaction()

    consumer.close()

if __name__ == "__main__":
    main()
```

