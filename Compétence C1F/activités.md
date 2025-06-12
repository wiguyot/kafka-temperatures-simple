# Activités compétence C1F – Partitionnement & clé de partition


Activités suggérées
Type 	Durée 	Contenu
CM démo 	15 min 	Visualisation d’un envoi de 100 k messages : clé fixe vs round-robin vs partitionneur custom.
TD 	1 h 	Créer un topic 6 partitions, écrire un producteur Python :
• clé = userId ⇒ observer ordre mais skew ;
• clé random ⇒ débit équilibré mais ordre perdu.
Mini-projet 	2 h 	Simuler une boutique : partition par customerId, ajouter une sous-clé orderId%2 pour réduire la hot partition, monitorer la répartition sur Grafana. Le code sera écrit en python.

    À retenir : le partitionnement est le levier n°1 pour la scalabilité ET la garantie d’ordre ; la clé de partition doit être choisie avec soin pour éviter les hot partitions tout en conservant la cohérence fonctionnelle.


dans le cadre de cette activités : "Mini-projet 	2 h 	Simuler une boutique : partition par customerId, ajouter une sous-clé orderId%2 pour réduire la hot partition, monitorer la répartition sur Grafana. Le code sera écrit en python simple et clair." Explicite précisément tout cela 



Custom partitionner : 

```python
def custom_partitioner(city_name: str, num_partitions: int) -> int:
    """
    Attribue une partition en fonction du nom de la ville :
    - Les villes commençant par "PARIS" vont en partition 0
    - Les autres sont réparties sur 1..N-1 via hash
    - Si clé absente ou non valide : partition 'num_partitions' (hors bornes)
    """
    if isinstance(city_name, str):
        if city_name.upper().startswith("PARIS"):
            return 0
        else:
            return 1 + (abs(hash(city_name)) % (num_partitions - 1))
    else:
        # Cas d’erreur explicite : on renvoie un index invalide
        return num_partitions
```
Paris est toujours affecté à la partition 0, les autres villes sont réparties aléatoirement. La valeur de retour est entre 0 et N-1. Si c'est N c'est qu'on a rencontré un soucis. 