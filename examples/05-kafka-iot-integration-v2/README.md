# MQTT to Kafka Bridge with Spark Integration
This project demonstrates how to build a data pipeline that connects an MQTT broker to Kafka, processes data with Apache Spark, and stores the processed messages in a MongoDB server.

A Python application `main.py` subscribes to MQTT topics and forwards received messages to a Kafka topic.
Dockerized using a Dockerfile and orchestrated with `docker-compose.yml`.

A Spark application `spark_job.py` reads messages from Kafka, processes them, and writes them to a MongoDB server.

## Prerequisites
* Docker and Docker Compose installed on your machine.
* Python 3.9+ installed if running outside Docker.
* Apache Spark configured for running `spark_job.py`

## Run the MQTT to Kafka 

The following env variables are used in the `docker-compose.yml` file:

```
...
    environment:
      MQTT_BROKER: "broker"
      MQTT_PORT: 1883
      MQTT_TOPIC: "#"
      KAFKA_BROKER: "broker:29092"
      KAFKA_TOPIC: "mqtt"
...
```

Change them according to you environment and execute the compose:

    docker-compose up --build

You can connect to kafka ith a console consumer to chck if the messages arrives:

```
kafka-console-consumer \
    --topic mqtt \
    --bootstrap-server broker:29092
```

## Run the Spark job

Ensure mongo s running. Change the mongo db address if needed in the command below. Remember also to create a database `datalake` and a collection `iot` in mongo:

```
spark-submit \
  --master spark://192.168.205.8:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:10.4.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 \
  --conf "spark.mongodb.write.connection.uri=mongodb://192.168.205.8/datalake.iot" \
  spark_job.py
```

Use a Mongo client to check if the messages are fowarded as expected-