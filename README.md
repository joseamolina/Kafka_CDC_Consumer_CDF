# Kafka CDC Consumer CDF

This project simulates a **Change Data Capture (CDC)** data pipeline. It uses a Python producer to generate random database events (INSERT, UPDATE, DELETE) and sends them to a Kafka topic (Redpanda). A consumer based on **PySpark Structured Streaming** reads these events in real-time for processing.

## 🚀 Architecture

The system consists of three main parts:

1.  **Producer (Python)**:
    - Generates simulated user transactions (ID, Name, Balance).
    - Creates CDC events with operations `c` (create), `u` (update), `d` (delete).
    - Sends data in JSON format to the `r023hf` topic.
    - Runs inside a Docker container.

2.  **Broker (Redpanda)**:
    - Acts as the Kafka broker.
    - Manages the topic and message transmission.

3.  **Consumer (PySpark)**:
    - `pyspark_test_stream.py`: Local script that connects to Redpanda.
    - Reads the Kafka stream, parses the JSON, and displays changes in the console.

## 📋 Prerequisites

*   **Docker** and **Docker Compose**.
*   **Python 3.8+** (to run the consumer locally).
*   **Java 8/11** (required by Apache Spark).
*   Python libraries (see `producer/requirements.txt` for docker, and manuals for local).

## 🛠️ Installation and Usage

### 1. Start the Infrastructure (Producer + Broker)

Use Docker Compose to start Redpanda and the Event Producer:

```bash
docker-compose up -d
```

This will start:
*   `redpanda`: Listening on port `9092`.
*   `kafka-producer`: continuously generating events.

You can verify that the containers are running with:

```bash
docker ps
```

### 2. Run the Consumer (PySpark)

To process streaming data from your local machine:

1.  Ensure you have PySpark installed and the Kafka dependencies for Spark.
    The `pyspark_test_stream.py` script is already configured to download the `spark-sql-kafka-0-10` package.

2.  Run the script:

```bash
python3 pyspark_test_stream.py
```

> **Note**: If you encounter connection errors, ensure your `/etc/hosts` has an entry for `redpanda` pointing to `127.0.0.1` or modify the script to use `localhost:9092`. In `docker-compose.yml`, Redpanda exposes port 9092.

## 📂 Project Structure

*   `docker-compose.yml`: Service definition (Redpanda and Producer).
*   `producer/`: Source code for the event producer.
    *   `python_producer.py`: Logic for generating CDC events.
    *   `entrypoint.sh`: Container entrypoint script.
    *   `Dockerfile`: Producer image definition.
*   `pyspark_test_stream.py`: PySpark consumer to visualize the data.

## ⚙️ Configuration

Environment variables in `docker-compose.yml` control data generation:

*   `TOPIC`: Kafka topic name (default: `r023hf`).
*   `MIN_VALUE` / `MAX_VALUE`: Ranges for random values (not directly used in current logic, but passed as args).
*   `EVENTS_PER_SEC`: Event rate per second.
