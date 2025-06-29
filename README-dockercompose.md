# Tests simples autour de la façon d'écrire et de lire les topics

1 producer et 1 consumer à choisir
```URL http://localhost:9000 pour accéder au kafdrop après une attente d'une minute nécessaire pour que tous les éléments de l'applications soient prêts.```

```pgsql
┌──────────────────────────┐        ┌────────────────────────┐
│ 1 × Producer Python      │  --->  │  Kafka topic `weather` │
│                          │        │  4 partitions, RF = 3  │
└──────────────────────────┘        └─────────┬──────────────┘
                                              │
                 ┌────────────────────────────┴────────────────────────────┐
                 │   3 × Kafka brokers (KRaft, no ZooKeeper)               │
                 │   + internal controller quorum                          │
                 └─────────────────────────────────────────────────────────┘
                                              │
                       ┌──────────────────────┴──────────────────────┐
                       │         Kafdrop (UI : localhost:9000)       │
                       └──────────────────────┬──────────────────────┘
                                              │
              ┌───────────────────────────────┴────────────────────────────┐
              │ 1 × Consumer  Python                                       │
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