# Clé de partition


Clé de partition 	Champ (ou fonction) dont le hash décide de la partition cible. 	Garantit l’ordre des messages portant la même clé (≈ même client, commande, capteur …).

Attention au déséquilibre de partition : 

## Skew

**Skew** désigne un déséquilibre dans la répartition des données, des charges ou du trafic sur un cluster ou un système distribué.


## Skew des partitions :

C’est le cas où certaines partitions reçoivent beaucoup plus de messages que d’autres.

Cela entraîne qu’un ou quelques brokers (ceux qui hébergent ces partitions) doivent traiter plus de données, écrire plus sur le disque, faire plus de réplications, etc.

## Skew de consommation :

Si un consommateur doit traiter la partition “hot”, il sera surchargé comparé aux autres.


## Conséquences d’un skew

- Diminution du débit global (le cluster n’est plus limité par la moyenne, mais par la partition la plus chargée).
- Augmentation du lag (retard) sur les partitions “hot”.
- Risque de saturation (CPU, disque, réseau) sur un sous-ensemble des brokers, tandis que d’autres sont sous-utilisés.
- Pertes potentielles de performance et de fiabilité.

## Causes classiques du skew dans Kafka

- **Clé de partition mal choisie** : Par exemple, une valeur de clé beaucoup plus fréquente que les autres (ex : beaucoup de messages “PARIS” et très peu “LILLE”).
- **Hot key** (“clé chaude”) : Un seul client ou type de message inonde une ou deux partitions.
- **Nombre de partitions trop faible ou pas assez de variation dans la clé.**


```Le skew dans Kafka, c’est le fait que la charge ou les messages ne sont pas uniformément répartis entre les partitions ou les brokers, ce qui limite la scalabilité, augmente la latence et peut causer des points de congestion ("hot partitions"). Le partitionnement est donc le levier principal pour éviter le skew.```