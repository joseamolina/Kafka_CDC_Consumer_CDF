set -e

sleep 5

rpk topic create "$TOPIC" --brokers "$KAFKA_BROKER" || true

python3 ./python_producer.py $TOPIC $KAFKA_BROKER $MIN_VALUE $MAX_VALUE $EVENTS_PER_SEC
