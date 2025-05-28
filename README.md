# Tests simples autour de la façon d'écrire et de lire les topics

1 producer et 1 consumer

```pgsql
┌──────────────────────────┐        ┌────────────────────────┐
│ 1 × Producers Python     │  --->  │  Kafka topic `weather` │
│  (Paris, Reims, …)       │        │  4 partitions, RF = 3  │
└──────────────────────────┘        └─────────┬──────────────┘
                                              │
                 ┌────────────────────────────┴────────────────────────────┐
                 │   3 × Kafka brokers (KRaft, no ZooKeeper)               │
                 │   + internal controller quorum                          │
                 │   + shared volume for each broker (data)                │
                 └─────────────────────────────────────────────────────────┘
                                              │
                       ┌──────────────────────┴──────────────────────┐
                       │         Kafdrop (UI : localhost:9000)       │
                       └──────────────────────┬──────────────────────┘
                                              │
              ┌───────────────────────────────┴────────────────────────────┐
              │ 1 × Consumers Python                                       │
              └────────────────────────────────────────────────────────────┘
```

## Producer

On a le choix, dans ./producer/Dockerfile du producteur qu'on va utiliser. 

  - producer-round-robin.py qui écrit dans le topic sans se préoccuper de la répartition des données dans les partitions.
  - producer-key-equals-city.py qui écrit en utilisant comme clé de partition la valeur de "city".

## Consumer

On a le choix dans ./consumer/Dockerfile du consommateur qu'on va utiliser

- consumer-auto-comit.py qui utilise l'autocommit, c'est à dire autocommit toutes les 5 secondes réglage par défaut.
- consumer-read-then-commit.py désactive l'autocommit et fait un commit à chaque lecture du topic.
- consumer-async-commit.py désactive l'autocommit et fait un commit asynchrone afin de ne pas surcharger les échanges mais avec les risques inhérents à une défaillance du consommateur qui n'aurait pas validé ses lectures.