# Activités compétence C1F – Partitionnement & clé de partition


## définition du projet 

**Objet** : Simuler l’activité d’une boutique en ligne, en envoyant dls commandes à Kafka, pour illustrer le rôle du partitionnement sur la scalabilité et la répartition de charge. On mènera une analyse des métriques avec des comparaisons si on utilise des clés unique ou des clés composées. L'idée est de montrer l'apport de la métrologie, de la bonne organisation des partitions et des clés que l'on utilise.

L'analyse/visualisation se fera aussi bien sur la production que la consommation des messages.

La consommation des messages permettra par exemple de répondre à des questions telles que l'historiques annuel des commandes par client ou au total, le montant annuel des commandes pour un client donné.

**Hypothèse** : une commande = un message, associé à un customerId et un orderId. Chaque commande comprendra notamment : 
- prix payé HT de la commande
- année de commande 

**Attention** :

* Si on utilisait uniquement customerId comme clé de partition, tous les messages du même client iraient dans la même partition. Du coup si certains clients sont très actifs, une partition sera “hot” (= surchargée), ce qui crée un “skew” de charge et de débit.


**Visualisation/analyse**

À observer sur influxdb ou Grafana si vous préférez : 
- Histogramme des messages/partitions (doivent être plus équilibrés qu’avec clé unique)
- Heatmap ou graphique du lag pour repérer d’éventuelles partitions “hot”

On pourra librement s'inspirer du bootstrap suivant faisant de la métrologie sur cluster Kafka Kraft au moyen de : 
- telegraf
- influxdb

https://github.com/wiguyot/bootstrap-kafka-metrology



**Ordre de grandeur**

Il faudra peut être avoir des centaines de milliers ou millions de commandes pour arriver à mettre en valeur les contraintes de skew/hot partitions et leurs conséquences.


## Suggestion

Ajouter une **sous-clé orderId%2** pour réduire la hot partition”. %2 désigne modulo

#### Sous-Clé

La clé de partion peut être composée de plusieurs éléments (ou “compound key”) : (customerId, orderId%2)

    orderId%2 : le reste de la division entière de l’orderId par 2 (donc, 0 ou 1).

Le but est de diviser la charge :

        Plutôt que d’envoyer toutes les commandes d’un même client sur 1 seule partition, on les répartit sur 2 partitions différentes, grâce à la sous-clé orderId%2.

        Ça réduit la probabilité qu’une seule partition devienne un point chaud (“hot partition”).

Concrètement

    Pour un customerId donné, ses commandes seront hashées sur :

        (customerId, 0) → partition X

        (customerId, 1) → partition Y

    Si on a 6 partitions Kafka, l’algorithme de partitionnement va mieux répartir les commandes de chaque client sur 2 partitions différentes, réduisant la saturation.

Pourquoi pas seulement orderId ?

    Si on partitionne uniquement sur orderId, on perds l’ordre des commandes pour chaque client (un besoin métier fréquent).

    Avec (customerId, orderId%2), on garde une certaine cohérence :

        L’ordre est garanti par client dans chacune des deux partitions,

        Mais on sacrifie l'ordre stricte pour améliorer le débit et l’équilibrage. Il faudra trouver un moyen de ré-ordonner les commandes.