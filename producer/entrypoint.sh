set -e

sleep 5

echo "Starting topic creation..."
rpk topic create "$TOPIC" --brokers "$KAFKA_BROKER" --tls-enabled --tls-truststore /etc/kafka-producer/certs/ca.crt || true
echo "Topic creation step finished."

echo "Starting Python producer..."
python3 -u ./python_producer.py $TOPIC $KAFKA_BROKER $MIN_VALUE $MAX_VALUE $EVENTS_PER_SEC
