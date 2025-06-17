# compétences abordées dans ce dépot kafka-temperatures-simple

A la base ce dépot montre un fonctionne simple d'un producteur qui écrit dans un cluster Kafka répliqué 3 fois. Il va servir de base d'apprentissage et de visualisation pour les compétences C1D et C1F. Si nécessaire dans les répertoires des compétences on peut avoir des docker compose complémentaires.

Ce dépot montre : 

README-docker-compose.md : un prototype de cluster fonctionnel qui montre quelques éléments basiques autour de Kafka. On y trouvera la dynamique entre un producteur et un consommateur.

C1D : 
- fonctionnement général des leaders/followers
- observer les latences au moyen de l'outil fourni par Apache Kafka
- la relation entre durabilité et rétention
- diagnostiquer les problèmes problèmes liés à l'ISR
- un petit projet ou TP dans Compétence C1D/activités.md

C1C : sémantique de traitement des messages

C1F : 
- approfondir les partitions et les clés de partitions
- les différents types de partionneurs
- **Un projet plus ambitieux (10-15 heures ?) dans Compétence C1F**