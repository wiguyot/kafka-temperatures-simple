#!/bin/bash

# Script robuste : crée le topic seulement s’il n’existe pas
kafka-topics.sh \
  --bootstrap-server kafka-1:9092 \
  --create \
  --if-not-exists \
  --topic weather \
  --partitions 4 \
  --replication-factor 3

# Marqueur pour signaler que le topic est bien créé
touch /tmp/topic-created
