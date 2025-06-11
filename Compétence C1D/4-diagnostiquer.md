# Diagnostiquer 

Définition

    Une partition est “under-replicated” quand elle a moins de réplicas ISR que le facteur de réplication attendu (RF).

Diagnostic

Commande à utiliser :

```bash
docker exec kafka-4 kafka-topics.sh --bootstrap-server kafka-4:9092 --describe
```

On pourrait observer le champ ISR plus court que la liste des réplicas : 

```yaml
    Topic: test-perf  Partition: 0  Leader: 1  Replicas: 4,5,6  Isr: 4,6
```
Ici, le broker 5 n’est plus ISR (partition sous-répliquée).

Métriques/alertes :

    Metric JMX : kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions

Surveillez ce compteur dans Grafana ou Prometheus.

À simuler pour un TP :

    Arrête un broker follower, observe que la partition passe en under-replicated.