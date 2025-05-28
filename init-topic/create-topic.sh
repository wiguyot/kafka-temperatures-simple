#!/bin/bash
set -e

# 1. Wait until Kafka is reachable
while ! bash -c "echo > /dev/tcp/kafka-1/9092"; do
  echo "⏳ Waiting for Kafka at kafka-1:9092…"
  sleep 1
done
echo "✅ Kafka is up!"

# 2. Delete the topic "weather" if it already exists
if kafka-topics.sh \
     --bootstrap-server kafka-1:9092 \
     --list | grep -q "^weather$"; then
  echo "⚠️ Deleting existing topic 'weather'…"
  kafka-topics.sh \
    --bootstrap-server kafka-1:9092 \
    --delete \
    --topic weather

  # wait for the deletion to propagate
  while kafka-topics.sh \
          --bootstrap-server kafka-1:9092 \
          --list | grep -q "^weather$"; do
    echo "⏳ Waiting for topic 'weather' to be fully deleted…"
    sleep 1
  done
  echo "✅ Old topic 'weather' deleted"
fi

# 3. Create the topic with 4 partitions and replication factor 3
kafka-topics.sh \
  --bootstrap-server kafka-1:9092 \
  --create \
  --topic weather \
  --partitions 4 \
  --replication-factor 3

# 4. Signal that the topic was created
touch /tmp/topic-created
