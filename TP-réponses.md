# Exemples de réponses acceptables

Ce n'est pas exhaustif.

1. Quel est le nom du topic utilisé dans ce TP ?
=> Topic : temperatures (tel qu’employé dans le dépôt).

2.	Quels sont les trois champs envoyés par le producteur dans chaque message ?
=> Champs : ville, temperature, timestamp.

3.	Quelle clé de partition est utilisée par le producteur et pourquoi ?
=>	Clé de partition : ville → garantit l’ordre par ville et regroupe les messages d’une même ville.  ￼

4.	Que garantit Kafka sur l’ordre des messages au sein d’une partition ?
=>	Ordre garanti : Kafka ne garantit l’ordre qu’à l’intérieur d’une partition (pas entre partitions).  ￼

5.	Que se passe-t-il quand vous lancez un deuxième consumer dans le même consumer group ?
=>	2ᵉ consumer dans le même group : rebalance ; les partitions se répartissent entre les consumers (1 consumer actif par partition).  
￼
6.	Comment démarrer l’environnement avec Docker Compose (commande exacte) ?
=>	Démarrage Compose : docker compose up -d.

7.	À quoi sert le consumer lag (que mesure-t-il) en une phrase ? 
=>	Consumer lag (définition courte) : écart entre le dernier offset écrit et le dernier offset commit par le group.  ￼

8.	Citez un moyen simple d’observer le lag (outil ou commande).
=>	Observer le lag : kafka-consumer-groups --describe --group <g>. On peut aussi le voir sur KafDrop ￼

9.	Quel est l’effet attendu quand on passe le topic de 1 à 4 partitions ?
=>	Passer de 1 → 4 partitions : ↑ parallélisme/débit, mais l’ordre n’est plus global (reste par partition).  ￼

10.	À quoi servent les paramètres de topic retention.ms et segment.bytes (une phrase chacun) ?
=> 	retention.ms : durée de rétention avant suppression ; segment.bytes : taille des fichiers de segment avant “roll”.  ￼

11.	Dans consumer-auto-commit.py, quel est le risque principal sur la livraison (expliquer en une phrase) ?
=> Auto-commit : risque : si crash avant l’auto-commit suivant, re-lecture/duplication possible (et selon l’enchaînement des poll(), risque at-most-once).  
￼
12.	Dans consumer-async-commit.py, pourquoi parle-t-on d’un commit “après traitement” et en quoi est-ce différent de l’auto-commit ?
=>	Async-commit “après traitement” vs auto-commit : on traite puis commit explicitement (mieux maîtrisé) au lieu de laisser un timer d’auto-commit ; le message peut être traité deux fois sauf si idempotence côté sink.  ￼

13.	Dans consumer-read-then-commit.py, quel est l’avantage et quel est l’inconvénient du commit synchrone ?
=>.	Read-then-commit (synchrone) : avantage = plus robuste (on attend l’ack) ; inconvénient = bloquant → ↓ débit.  ￼

14.	Donnez un cas d’usage réaliste pour chacun des trois modes :

     • auto-commit → monitoring / logs best-effort.

     • async-commit → débit élevé avec tolérance aux doublons (idempotence conseillée).  ￼

     • read-then-commit → opérations sensibles/side-effects non idempotents (cohérence > perf).  ￼

15.	Si la clé de partition devenait aléatoire à chaque message, quel effet cela aurait-il sur l’ordre et la répartition des messages ?
=> répartition quasi uniforme mais ordre éclaté entre partitions (plus d’ordre global).  ￼