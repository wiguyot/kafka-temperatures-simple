# Partitions
Partition => Shard physique d’un topic, numérotée 0…N-1, stockée comme un log append-only. 	Débit linéaire : plus de partitions => plus de parallelisme producteur/consommateur.

## Shard physique d'un topic

**shard** : portion/partie des données du topic
- Chaque topic est divisé en N partitions (shards), numérotées 0…N-1, ce n'est pas un fichier unique.
- Chacune de ces partitions reçoit un sous-ensemble des messages.
- C'est l’unité de parallélisme, d’ordre local, et de distribution du topic.
- Un shard est une « partie physique », un fragment réel de données.


**à ne pas confondre avec le réplica** : 
- C’est une copie exacte d’une partition, pour la redondance et la tolérance aux pannes.
- Chaque partition peut avoir plusieurs réplicas : un leader + des followers.
- Tous les réplicas stockent les mêmes données pour une partition donnée, sur différents brokers.


numérotée 0…N-1
- Chaque partition d’un topic reçoit un numéro unique qui commence à 0 et va jusqu’à N-1 (N étant le nombre total de partitions pour ce topic).
- Exemple : si un topic a 4 partitions, elles sont numérotées 0, 1, 2, 3.

stockée comme un log append-only
- Chacune de ces partitions est stockée comme un fichier journal (log) sur disque :
  - append-only veut dire : on ajoute toujours à la fin, on ne modifie ni n’efface le début du fichier.
  - Les nouveaux messages sont simplement append (ajoutés) à la suite du dernier, dans l’ordre d’arrivée.
  

## Activité montrant l'augmentation du débit linéaire et du parallélisme avec l'augmentation des partitions

Construire un mini-projet : 

Attention dans les mesures réalisées il faudra se poser la question des effets de cache et de reproductibilité 

### Matériel

- Un cluster Kafka fonctionnel (inspiré des précédents docker-compose.yml)
- 1 à 4 producteurs et 1 à 4 consommateurs simples (ex : Python avec confluent_kafka)
- Un script de mesure du débit (messages/seconde ou temps pour consommer 100 000 messages)

### exemple de création de topics 

Créer trois topics identiques mais avec un nombre de partitions différent :
- test-1p (1 partition)
- test-2p (2 partitions)
- test-4p (4 partitions)

```bash
kafka-topics.sh --create --topic test-1p --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092
kafka-topics.sh --create --topic test-2p --partitions 2 --replication-factor 1 --bootstrap-server localhost:9092
kafka-topics.sh --create --topic test-4p --partitions 4 --replication-factor 1 --bootstrap-server localhost:9092
```

### Script producteur

- Un script envoie 100 000 messages sur chacun des topics, le plus vite possible 
  - clé fixée ou aléatoire 
  - round-robin (absence de clé)
- S'inspirer d'un programme python déjà précédement utilisé.


### Scripts consommateur

- Lancer un consommateur unique et mesurer le temps pour lire 100 000 messages sur chaque topic.
- Puis lancer N consommateurs (N = nombre de partitions) en mode groupe (group.id commun), et refaire la mesure.

Exemple de code simpliste dont vous pouvez vous inspirer et à adapter à votre cas d'usage : 

```python
import multiprocessing
from confluent_kafka import Consumer
import time

def consumer_worker(consumer_id, topic, group_id, bootstrap_servers):
    conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',   # lit tout depuis le début
        'enable.auto.commit': True,
    }
    consumer = Consumer(conf)
    consumer.subscribe([topic])

    print(f"[{consumer_id}] Démarré.")
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"[{consumer_id}] Erreur: {msg.error()}")
                continue
            print(f"[{consumer_id}] Partition {msg.partition()} | {msg.value().decode(errors='replace')}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        print(f"[{consumer_id}] Arrêté.")

if __name__ == "__main__":
    # Paramètres à adapter
    TOPIC = "weather"
    NUM_PARTITIONS = 4         # adapte ici au nombre réel de partitions du topic
    BOOTSTRAP_SERVERS = "localhost:9092"
    GROUP_ID = "demo-group"

    # Crée N consommateurs (un par partition)
    processes = []
    for i in range(NUM_PARTITIONS):
        p = multiprocessing.Process(
            target=consumer_worker,
            args=(i, TOPIC, GROUP_ID, BOOTSTRAP_SERVERS)
        )
        processes.append(p)
        p.start()

    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("Arrêt demandé (Ctrl+C)")
        for p in processes:
            p.terminate()
            p.join()

```

### Observations & analyses

Comparer le temps total pour lire tous les messages selon le nombre de partitions ET de consommateurs.

Vérifier :
- Avec 1 seule partition, un seul consommateur lit tous les messages : débit limité.
- Avec N partitions et N consommateurs, chaque consommateur reçoit une partition → parallélisme maximal, temps de traitement ≈ divisé par N.

Expliquer pourquoi : 
-  il ne sert à rien d’avoir 4 consommateurs sur un topic à une seule partition
