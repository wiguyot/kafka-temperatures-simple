<img src="docs/assets/sc.png"
     alt="Schéma général"
     width="400">

```pgsql
┌──────────────────────────┐        ┌────────────────────────┐
│ 5 × Producers Python     │  --->  │  Kafka topic `weather` │
│  (Paris, Reims, …)       │        │  4 partitions, RF = 3  │
└──────────────────────────┘        └─────────┬──────────────┘
                                              │
                 ┌────────────────────────────┴────────────────────────────┐
                 │   3 × Kafka brokers (KRaft, no ZooKeeper)               │
                 │   + internal controller quorum                          │
                 │   + shared volume for each broker (data)                │
                 └──────────────────────────────────────────────────────────┘
                                              │
                       ┌──────────────────────┴──────────────────────┐
                       │         Kafdrop (UI : localhost:9000)       │
                       └──────────────────────┬──────────────────────┘
                                              │
             ┌───────────────────────────────┴────────────────────────────┐
             │ 2 × Consumers Python (group A, group B)                    │
             │   - group A → Paris, Reims, Marseille                      │
             │   - group B → Lyon, Clermont-Ferrand                       │
             └─────────────────────────────────────────────────────────────┘
```

```pgsql
.
├── docker-compose.yml
├── init-topic/
│   └── create-topic.sh
├── producer-paris/            (x5 dossiers identiques)
│   ├── Dockerfile
│   └── producer.py
├── producer-reims/
│   └── …
├── consumer-prm/
│   ├── Dockerfile
│   └── consumer.py
└── consumer-lc/
    └── …
```