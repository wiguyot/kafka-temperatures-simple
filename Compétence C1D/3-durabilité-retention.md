# Durabilité et rétention



## Durabilité : dure jusqu'à l'application d'un délai de rétention

Définition :
La durabilité d’un message signifie que Kafka garantit que le message est stocké de manière fiable sur disque et qu’il ne sera pas perdu, même si un ou plusieurs brokers tombent en panne.

Garantie de durabilité : 

- Il a été écrit sur disque sur le leader (via un flush/fsync).
- Il a été répliqué sur tous les brokers de l’ISR (In-Sync Replicas), après ack=all.

```Tant que le message existe sur au moins 1 ISR, il ne peut pas être perdu, même en cas de crash du leader ou d’un follower.```

    


## Rétention : “nettoyé après N jours” ou après avoir atteint la taille maximale

Définition :
La rétention définit combien de temps ou combien d’espace disque Kafka va conserver les messages sur ses logs, même si personne ne les lit.

Paramètres typiques :
- retention.ms (durée en millisecondes, ex : 7 jours)
- retention.bytes (taille maximale à conserver sur disque)
- ```Compactage : (cas spécial) conserve seulement le dernier message pour chaque clé.```


## Suppression des messages

Quand la période de rétention est dépassée (ex : 7 jours), ou la taille limite atteinte, le log cleaner de Kafka va supprimer définitivement les anciens messages.

```Effet : Même un message parfaitement durable et répliqué peut être supprimé, une fois la rétention expirée.```