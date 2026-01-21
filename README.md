# Real-time-streaming-kafka-spark-lab
This repository contains all hands-on materials used throughout the course Design Real-Time Architectures with Apache Spark &amp; Kafka. It includes a fully configured Kafka environment using Docker, a Spark Structured Streaming script for connecting to Kafka, and a deployment-oriented streaming script, eal-time processing behavior.

## 📂 Repository Contents

| File | Description |
|------|-------------|
| `docker-compose.yml` | Launches a complete Kafka environment + Kafka UI using Docker. |
| `spark_kafka_stream.py` | Spark Structured Streaming job that reads Kafka events, parses JSON, applies transformations, and prints results in real time. |
| `deploy_stream.py` | Deployment-oriented Spark streaming script demonstrating checkpointing, fault tolerance, and monitoring principles. |

---

## 🚀 Getting Started

### 1. Start Kafka + Kafka UI

Make sure you have **Docker** and **Docker Compose** installed.

```bash
docker compose up -d
```
This starts:

Kafka broker at localhost:29092

Kafka UI dashboard at http://localhost:8080

Verify everything is running:

```bash
docker ps
```
### 2. Create a Kafka Topic
```bash
docker exec -it kafka-broker /opt/kafka/bin/kafka-topics.sh \
  --create --topic payments --partitions 3 --replication-factor 1 \
  --bootstrap-server kafka-broker:9092
```
List topics:
```bash
docker exec -it kafka-broker /opt/kafka/bin/kafka-topics.sh \
  --list --bootstrap-server kafka-broker:9092
```

#### 🧪 Producing Test Messages

Optional but useful for testing:
```bash
docker exec -it kafka-broker /opt/kafka/bin/kafka-console-producer.sh \
  --topic payments --bootstrap-server kafka-broker:9092
```
Then type:
```bash
{"amount": 250, "currency": "USD"}
```

### ⚡ Running Spark Streaming Jobs
#### 1. Basic Kafka → Spark Streaming Job

Use this during L2V2 and L2V3 lessons.

```bash
python3 spark_kafka_stream.py
```
This job:

Reads Kafka messages as byte arrays.

Parses JSON into structured columns.

Applies a transformation (amount_usd).

Prints live output to the console.

#### 2. Deployment-Oriented Streaming Job

Used during L3V3 – Deploying, Monitoring & Managing Pipelines.

```bash
python3 deploy_stream.py
```

This job demonstrates:

Checkpointing

Offset recovery

Clean stream parsing

Console output sink

Real-time monitoring behavior

Checkpoint directories will be created automatically:

```bash
./checkpoint-sim/
./checkpoint-deploy-demo/
```
### 📊 Kafka UI Dashboard

Access it here:

```bash
http://localhost:8080
```
You can:

Inspect topics

View partitions & offsets

Browse messages

Monitor consumer lag

Validate real-time ingestion

### 🧱 Requirements

Python 3.9+

PySpark 3.5.x

Docker Desktop

4 GB RAM minimum

Install PySpark:

```bash
pip install pyspark
```
### 📬 Support

If you encounter issues:

Ensure Docker is running

Restart Kafka

Clear old Kafka volumes if needed

```bash
Reset checkpoints (rm -rf checkpoint-*)
```
Confirm PySpark version compatibility
