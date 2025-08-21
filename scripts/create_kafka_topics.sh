#!/usr/bin/env bash
set -euo pipefail

# Creates topics used by examples
docker compose exec -T kafka kafka-topics.sh --bootstrap-server kafka:9092 --create --if-not-exists --topic input-words --partitions 1 --replication-factor 1
docker compose exec -T kafka kafka-topics.sh --bootstrap-server kafka:9092 --create --if-not-exists --topic output-counts --partitions 1 --replication-factor 1

echo "Existing topics:"
docker compose exec -T kafka kafka-topics.sh --bootstrap-server kafka:9092 --list