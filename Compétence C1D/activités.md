# Activités compétence C1D – Logs distribués & durabilité des messages


## Questions

« Pourquoi un flush forcé toutes les 100 ms augmente-t-il la latence p95 ? » : 

Un flush forcé toutes les 100 ms (via log.flush.interval.ms = 100) oblige le leader à exécuter un appel système fsync() pour forcer l’écriture physique des messages du segment sur disque, indépendamment du fait que le buffer mémoire soit plein ou non.
Or, l’opération de flush (fsync) est coûteuse en temps : elle attend la confirmation du disque que toutes les données du buffer d’écriture sont bien persistées. Cette opération peut prendre de quelques ms à plusieurs dizaines de ms selon la charge disque et l’infrastructure sous-jacente.

Dans Kafka, lorsqu’un producteur attend un acks=all, le message n’est reconnu qu’une fois écrit sur disque (et répliqué dans l’ISR), donc il subit la latence d’un éventuel flush.

    Plus le flush est fréquent, plus il y a de chances qu’un message doive attendre la fin du flush précédent ou soit "pris en sandwich" entre deux flushs.

    Les opérations de flush venant s’intercaler dans le traitement normal, les messages qui arrivent juste avant un flush forcé vont subir une latence supplémentaire aléatoire correspondant à la durée du flush.

    La latence p95 (95e percentile) est sensible à ces "pics" de latence, car elle mesure la queue supérieure des messages les plus lents.

Donc : en forçant un flush toutes les 100 ms, on introduit régulièrement des pics de latence qui élèvent la p95, même si la moyenne reste basse.


## TD 

Mini projet  : 

- Créer un cluster basés sur 3 brokers Kraft avec un kafdrop 
- créer topic RF 3, Partions 8, ISR 2 en ligne de commande
- envoyer 10 K messages avec acks=all, tuer le leader ; observer la réélection et vérifier la non-perte.
- mesurer les performances avec graphiques à l'appui en faisant varier partitions de 3 à 10, acks [0,1,all]. Performances : débit messages par secondes et latence moyenne, max et 95th
- Pour le topic du second point faites varier les valeurs de flush en milli-secondes puis pour une valeur par défaut du flush en ms faites varier la taille du flush en octets. Essayez de trouver le sweet-point qui semble optimiser les deux valeurs de flush.

