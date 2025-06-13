# Compétence C1D – Logs distribués & durabilité des messages

Dans ce répertoire on s'attache à expliquer les notions de logs distribués et de durabilité des messages, la pertormance etc...

1) **sequence leader-followers** : 
On va expliquer la logique de l'envoie de message, ses réplications sur les followers du leader et les politiques d'acquittement.

2) **mesure de la latence** :
On va utiliser des outils de créations de jeux de test et mesurer les éléments de latence autour de la notion précédente (envois de messages et politiques d'acquittement)

3) **Durabilité et rétention** :
Quelles sont les garanties de rétention des messages acquittés. Pendant combien de temps garde t on les messages. Qu'est-ce que le compactage des topics.

4) **Diagnostic des partitions en difficulté** : 
Examen de la notion d'ISR et la distribution des brokers dans les ISR des partitions.

Dans le fichier ```activités```on va retrouver des petits projets pour mieux comprendre les questions de logs distribués et leur optimisation

- On explore la notion de flush 
- On met en oeuvre un petit cluster et on regarde/étudie : 
    - son comportement quand il pert un broker et ses performances à ce moment là
    - ses performances en fonction du nombre de partition qu'on met dans un topic
    - ses performances quand on fait les valeurs de flush en durée et en taille.