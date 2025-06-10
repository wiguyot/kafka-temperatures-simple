# Exactly Once Semantique (EOS)

Exactly-once : chaque message est livré exactement 1 fois sans perte et sans doublon. Cela nécessite : 
- un producteur idempotent : 
  - transaction kafka
  - commit d'offset dans la même transaction



Les **producteurs** (producer-\*.py) et **consommateurs** (consumer-\*.py) :

- Utilisent kafka-python, qui ne supporte pas les transactions (init_transactions, send_offsets_to_transaction, etc.).

- Ne committent pas d’offsets dans des transactions (impossible avec kafka-python).

- Il faudrait définir ```enable.idempotence=True (et acks=all)```, ce qui est requis même en préambule à l’EOS.

**Donc la sémantique Exactly-once n’est pas atteinte.**

## Support des transactions et des commits en ```java```

Producteur : chaque envoi de message doit être encadré par un ```beginTransaction``` et un ```commitTransaction```

Consommateur : chaque lecture et traitement d'un message doit être encadré par un ```beginTransaction``` et un ```commitTransaction```


## Exemple java d'un producteur EOS

IL FAUT VALIDER CET EXEMPLE !!!

```java
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;

public class WeatherProducerEOS {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, "true");
        props.put(ProducerConfig.RETRIES_CONFIG, Integer.toString(Integer.MAX_VALUE));
        props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, "5");
        props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "weather-transaction-1");

        KafkaProducer<String, String> producer = new KafkaProducer<>(props);
        producer.initTransactions();

        try {
            producer.beginTransaction();

            ProducerRecord<String, String> record = new ProducerRecord<>("weather", "Paris", "23°C");
            producer.send(record);

            // Ajoutez d'autres envois ici...

            producer.commitTransaction();
        } catch (Exception e) {
            producer.abortTransaction();
            e.printStackTrace();
        } finally {
            producer.close();
        }
    }
}
```

## Exemple java d'un consommateur EOS

IL FAUT VALIDER CET EXEMPLE !!!

```java
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;

import java.time.Duration;
import java.util.*;

public class WeatherConsumerEOSMinimal {
    public static void main(String[] args) {
        String inputTopic = "weather";
        String groupId = "weather-consumer-group";

        // Configuration du consommateur
        Properties consumerProps = new Properties();
        consumerProps.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        consumerProps.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        consumerProps.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        consumerProps.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);
        consumerProps.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        consumerProps.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");

        // Configuration du producteur pour la transaction (même sans produire de messages)
        Properties producerProps = new Properties();
        producerProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        producerProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        producerProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        producerProps.put(ProducerConfig.ACKS_CONFIG, "all");
        producerProps.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, "true");
        producerProps.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "weather-consumer-eos");

        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(consumerProps);
        KafkaProducer<String, String> dummyProducer = new KafkaProducer<>(producerProps); // pas utilisé pour send()

        consumer.subscribe(Collections.singletonList(inputTopic));
        dummyProducer.initTransactions();

        while (true) {
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));
            if (records.isEmpty()) continue;

            try {
                dummyProducer.beginTransaction();

                Map<TopicPartition, OffsetAndMetadata> offsets = new HashMap<>();

                for (ConsumerRecord<String, String> record : records) {
                    // Traitement simulé uniquement
                    System.out.println("Traitement de " + record.key() + " -> " + record.value());

                    offsets.put(
                        new TopicPartition(record.topic(), record.partition()),
                        new OffsetAndMetadata(record.offset() + 1)
                    );
                }

                // Envoie des offsets dans la transaction (sans produire de message)
                dummyProducer.sendOffsetsToTransaction(offsets, groupId);
                dummyProducer.commitTransaction();

            } catch (Exception e) {
                dummyProducer.abortTransaction();
                e.printStackTrace();
            }
        }
    }
}
```

