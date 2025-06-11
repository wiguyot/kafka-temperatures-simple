# Mesure de la latence d'un topic


## Création d'un topic de test de la latence

Liste des topics : 

```bash
docker exec kafka-4 kafka-topics.sh --list --bootstrap-server kafka-4:9092
```

Effacement du topic qui existerait déjà : 
```bash
docker exec kafka-4 kafka-topics.sh --bootstrap-server kafka-4:9092 --delete --topic test-perf
```

Création du topic test-perf : 
```bash
docker exec kafka-4 kafka-topics.sh --create --topic test-perf --bootstrap-server kafka-4:9092 --partitions 16 --replication-factor 3 --config min.insync.replicas=2
```

## Test de performance : ack=all

```bash
docker exec kafka-4 kafka-producer-perf-test.sh --topic test-perf --throughput -1 --num-records 10000 --record-size 100 --producer-props bootstrap.servers=kafka-4:9092 acks=all
```

Le résultat de la commande pourrait être : 

```yaml
10000 records sent, 44247.8 records/sec (4.22 MB/sec), 35.28 ms avg latency, 150.00 ms max latency, 33 ms 50th, 57 ms 95th, 60 ms 99th, 60 ms 99.9th.
```
- 10000 enregistrements envoyés
- chaque seconde le cluster peut absorber 44247 enregistrements
- la latence moyenne par message est 35.28 ms
- la latence max observée était de 150 ms
- 99.99% des enregistrements avaient une latence ne dépassant pas 60 ms

## Test de performance : ack=1

```bash
docker exec kafka-1 kafka-producer-perf-test.sh --topic test-perf --throughput -1 --num-records 10000 --record-size 100 --producer-props bootstrap.servers=kafka-1:9092 acks=1
```

Le résultat de la commande pourrait être : 

```yaml
10000 records sent, 57471.3 records/sec (5.48 MB/sec), 7.16 ms avg latency, 134.00 ms max latency, 6 ms 50th, 14 ms 95th, 16 ms 99th, 17 ms 99.9th.
```

- 10000 enregistrements envoyés
- chaque seconde le cluster peut absorber 57471 enregistrements
- la latence moyenne par message est 7.16 ms
- la latence max observée était de 134 ms
- 99.99% des enregistrements avaient une latence ne dépassant pas 17 ms


## Test de performance : ack=0

```bash
docker exec kafka-1 kafka-producer-perf-test.sh --topic test-perf --throughput -1 --num-records 10000 --record-size 100 --producer-props bootstrap.servers=kafka-1:9092 acks=0
```

Le résultat de la commande pourrait être : 

```yaml
10000 records sent, 60606.1 records/sec (5.78 MB/sec), 1.77 ms avg latency, 128.00 ms max latency, 1 ms 50th, 7 ms 95th, 9 ms 99th, 9 ms 99.9th.
```

- 10000 enregistrements envoyés
- chaque seconde le cluster peut absorber 60606 enregistrements
- la latence moyenne par message est 1.77 ms
- la latence max observée était de 128 ms
- 99.99% des enregistrements avaient une latence ne dépassant pas 9 ms

## On fait varier les valeurs de flush en temps et taille en octets

      - KAFKA_LOG_FLUSH_INTERVAL_MS=1 à 100000
  

  | flush interval | records/sec | MB/sec | avg latency (ms) | max latency (ms) | 50th (ms) | 95th (ms) | 99th (ms) | 99.9th (ms) |
|:--------------:|:-----------:|:------:|:----------------:|:----------------:|:---------:|:---------:|:---------:|:-----------:|
| 1        | 23255.8   | 2.22   | 259.39      | 393     | 259     | 274     | 275     | 276       |
| 10       | 22573.4   | 2.15   | 258.96      | 383     | 258     | 284     | 290     | 290       |
| 100      | 22522.5   | 2.15   | 247.95      | 389     | 247     | 274     | 278     | 278       |
| 1000     | 23364.5   | 2.23   | 252.87      | 385     | 251     | 270     | 272     | 274       |
| 10000    | 31948.9   | 3.05   | 140.89      | 276     | 142     | 152     | 154     | 154       |
| 100000   | 23753.0   | 2.27   | 247.77      | 382     | 250     | 261     | 265     | 265       |


    - KAFKA_LOG_FLUSH_INTERVAL_BYTES=0 à 41943040

| flush bytes   | records/sec | MB/sec | avg latency (ms) | max latency (ms) | 50th (ms) | 95th (ms) | 99th (ms) | 99.9th (ms) |
|:-------------:|:-----------:|:------:|:----------------:|:----------------:|:---------:|:---------:|:---------:|:-----------:|
| 0         | 32467.5   | 3.10   | 135.27      | 268     | 138     | 147     | 147     | 149       |
| 1048576   | 23640.7   | 2.25   | 247.34      | 378     | 248     | 262     | 266     | 266       |
| 2097152   | 23419.2   | 2.23   | 250.28      | 391     | 251     | 263     | 266     | 266       |
| 4194304   | 31055.9   | 2.96   | 143.35      | 281     | 144     | 159     | 164     | 164       |
| 41943040  | 32154.3   | 3.07   | 137.09      | 266     | 138     | 154     | 155     | 156       |


