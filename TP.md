# TP — Producteur/Consommateur Kafka (exemple températures)

TP (travaux pratiques) Kafka centré sur un flux de mesures de température. Il illustre les fondamentaux producer/consumer, l’impact de la clé de partition sur l’ordre intra-partition, la gestion du consumer lag, et l’effet des réglages de rétention et du nombre de partitions.

## Objectifs

•	Comprendre et démontrer :

	•	le rôle de la clé de partition et l’ordre garanti au sein d’une partition ;

	•	la répartition et le rebalance d’un consumer group ;

	•	la mesure puis la réduction du consumer lag via le parallélisme ;

	•	l’impact de retention.ms et segment.bytes sur la rétention/purge et le lag.

## Prérequis

- Docker + Docker Compose.

## Différentes méthodes de consommer

- auto commit du client : tolérants à la perte/duplication
- async commit : commit après traitement. On tolère une relecture occasionnelle
- read puis comit => sûr mais lent car attente de ack broker.


## Démarrage rapide
```bash
git clone <ce dépôt>
cd kafka-temperatures-simple
docker compose up 
```

## TP pas à pas

Pour répondre aux questions vous devrez préalablement utiliser les 3 consommateurs (fichiers .py) du répertoire consumer. Nous vous est nécessaire de comprendre leurs fonctionnements. Pour mettre en oeuvre ces consommateurs il vous faudra modifier la ligne 6 du fichier consumer/Dockerfile : 

```bash
COPY consumer-auto-commit.py ./consumer.py     
```
Et vous remplacerez consumer-auto-commit.py par le fichier que vous souhaitez tester. Bien entendu avant de faire cette modification vous aurez arrêté les services par :

```bash
docker compose down -v
```

vous faites les modifications puis vous relancez par 

```bash
docker compose up
```


1. Quel est le nom du topic utilisé dans ce TP ?

2.	Quels sont les trois champs envoyés par le producteur dans chaque message ?

3.	Quelle clé de partition est utilisée par le producteur et pourquoi ?

4.	Que garantit Kafka sur l’ordre des messages au sein d’une partition ?

5.	Que se passe-t-il quand vous lancez un deuxième consumer dans le même consumer group ?

6.	Comment démarrer l’environnement avec Docker Compose (commande exacte) ?

7.	À quoi sert le consumer lag (que mesure-t-il) en une phrase ?

8.	Citez un moyen simple d’observer le lag (outil ou commande).

9.	Quel est l’effet attendu quand on passe le topic de 1 à 4 partitions ?

10.	À quoi servent les paramètres de topic retention.ms et segment.bytes (une phrase chacun) ?

11.	Dans consumer-auto-commit.py, quel est le risque principal sur la livraison (expliquer en une phrase) ?

12.	Dans consumer-async-commit.py, pourquoi parle-t-on d’un commit “après traitement” et en quoi est-ce différent de l’auto-commit ?

13.	Dans consumer-read-then-commit.py, quel est l’avantage et quel est l’inconvénient du commit synchrone ?

14.	Donnez un cas d’usage réaliste pour chacun des trois modes :

	•	auto-commit

	•	async-commit

	•	read-then-commit (synchrone)

15.	Si la clé de partition devenait aléatoire à chaque message, quel effet cela aurait-il sur l’ordre et la répartition des messages ?