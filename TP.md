# TP — Producteur/Consommateur Kafka (exemple températures)

## Objectifs
- Maîtriser **producer/consumer**, **clé de partition**, **ordre intra-partition**.
- Mesurer et réduire le **consumer lag**.
- Manipuler **rétention** et **#partitions**.

## Prérequis
- Docker + Docker Compose.
- Accès :
  - Broker : `<KAFKA_BROKER_HOST>:<KAFKA_BROKER_PORT>`  <!-- TODO -->
  - Kafdrop (option) : `http://<HOST>:<KAFDROP_PORT>`  <!-- TODO -->

## Démarrage rapide
```bash
git clone <ce dépôt>
cd kafka-temperatures-simple
docker compose up -d
# (Option) Producteur Python si fourni :
# python producer.py
```

## TP pas à pas

	1.	Créer topic temperatures (p=1, rf adapté).
	2.	Lancer un producer : messages (ville, temp, ts) avec clé=ville.
	3.	Lancer 1 puis 2 consumers dans le même group → observer le rebalance.
	4.	Passer p=1 → p=4 ; vérifier l’impact sur ordre et débit.
	5.	Ajuster retention.ms / segment.bytes ; constater purge/lag.


## Critères de réussite

	•	Démonstration claire de l’ordre intra-partition.
	•	Lag expliqué puis réduit via le parallélisme.
	•	Mini-rapport décrivant les effets des réglages.