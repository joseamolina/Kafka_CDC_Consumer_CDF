set -e

sleep 5

# Create user (idempotent usually, or ignore error)
rpk acl user create myuser -p mypass --api-urls redpanda:9644 || true

rpk topic create "$TOPIC" --brokers "$KAFKA_BROKER" --user myuser --password mypass --sasl-mechanism SCRAM-SHA-256 || true

python3 ./python_producer.py $TOPIC $KAFKA_BROKER $MIN_VALUE $MAX_VALUE $EVENTS_PER_SEC
