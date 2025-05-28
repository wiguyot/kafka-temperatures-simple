#!/usr/bin/env bash
set -euo pipefail

# allow overriding via env
HOST=${KAFKA_HOST:-kafka-1}
PORT=${KAFKA_PORT:-9092}

echo "⏳ Waiting for Kafka at $HOST:$PORT…"

# bash builtin test
while ! bash -c ">/dev/tcp/$HOST/$PORT"; do
  echo "  still waiting…"
  sleep 1
done

echo "✅ Kafka is up!"
exec "$@"
