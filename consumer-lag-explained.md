# Explication du lag de consommation du topic


## Pourquoi ce lag peut monter jusqu’à 5

- **Production plus rapide que consommation**
  
Si votre producer poste (par ex. toutes les secondes) 1 message et que votre boucle de consommation poll() / commit() met un petit peu plus de temps (traitement, envoi de commit back-ground, etc.), il peut y avoir plusieurs messages “en attente” pendant ce laps de temps.

- **Offsets commis par lot**

Par défaut, Kafka commite les offsets en arrière-plan toutes les **5 000 ms (paramètre auto.commit.interval.ms)**. Pendant cet intervalle, même si votre code a déjà lu 10 messages, il n’aura peut-être commité que le 1er, et Kafdrop vous affichera donc un lag qui correspond aux 9 autres.

- **Polling et back-off**

Votre boucle for record in consumer: fait un poll() en bloc, bloque jusqu’à recevoir au moins un message, puis repart. Si plusieurs messages arrivent en une fois après un temps de repos, vous verrez un pic de lag avant le prochain poll().

- **Commit asynchrone**
  
Le commit d’offset est asynchrone : la lecture et l’avancement de l’offset local ne sont pas immédiatement reflétés côté broker. Kafdrop se base sur l’offset commité côté broker, pas forcément sur ce que votre client a déjà consommé en mémoire.

## En pratique

    Lag court (quelques messages) est normal tant que votre consumer rattrape le rythme du producteur.

    Si vous voulez voir le véritable “nombre de messages lus” sans attendre le commit, baissez enable.auto.commit et gérez manuellement vos commits après chaque poll().

    Pour un consumer à flux temps-réel, vous pouvez aussi :

        Réduire auto.commit.interval.ms (ex. 1000 ms)

        Traiter chaque message dès réception plutôt que par lots

        Augmenter le nombre de threads/instances consommant la même partition (si c’est pertinent)

En résumé, un lag à 5 reflète juste que, au moment où Kafdrop interroge le broker, votre consumer n’a pas encore commité les 5 derniers messages qu’il a lus ou qu’il va bientôt lire.

## consommateur avec validation du commit par auto.commit.interval.ms=5000

```python
# Initialisation du consommateur Kafka avec commit manuel
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_list,
    group_id=group_id,
    auto_offset_reset="earliest",
    enable_auto_commit=True,  # active le commit automatique
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print(f"Consuming from topic `{topic}` on {bootstrap_list} with group `{group_id}`…")

# Boucle de consommation
for record in consumer:
    print("Consumed ←", record.value)
```

## consommateur temps réel

```python
# Initialisation du consommateur Kafka avec commit manuel
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_list,
    group_id=group_id,
    auto_offset_reset="earliest",
    enable_auto_commit=False,  # désactive le commit automatique
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print(f"Consuming from topic `{topic}` on {bootstrap_list} with group `{group_id}`…")

# Boucle de consommation
for record in consumer:
    print("Consumed ←", record.value)
    # commit manuel de l’offset immédiatement après traitement
    consumer.commit()
```

## Usage de commit non bloquant 

Un commit non bloquant (consumer.commit_async()) fait exactement la même requête de sauvegarde d’offset auprès du broker qu’un consumer.commit(), mais sans bloquer la boucle de votre programme en attendant la réponse du serveur. Concrètement :

    consumer.commit()

        Envoie la requête de commit d’offset.

        Bloque jusqu’à réception de l’accusé de réception du broker (ou d’une exception).

        Garantit que, quand la méthode retourne, l’offset a bien été pris en compte (ou qu’une erreur vous est remontée).

    consumer.commit_async()

        Envoie la requête de commit d’offset.

        Retourne immédiatement, sans attendre la réponse.

        Vous pouvez (optionnellement) passer un callback pour être notifié en cas de succès ou d’échec du commit.

```python
# commit non bloquant avec callback
def on_commit(err, partitions):
    if err:
        print("Commit failed:", err)
    else:
        # partitions est la liste des TopicPartition confirmés
        pass

consumer.commit_async(callback=on_commit)
```

Pourquoi l’utiliser ?

    Moindre latence dans votre boucle de consommation : vous ne temporalisez plus à chaque appel de commit().

    Débit plus élevé si vous lisez / traitez beaucoup de messages par seconde.