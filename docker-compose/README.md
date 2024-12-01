# Running Kafka with Docker

Source: derived from https://github.com/confluentinc/cp-all-in-one/tree/7.5.0-post/cp-all-in-one-community

Tis folder contains a docker-compose file to run the following Kafka components:
* zookeeper service for Kafka
* broker a single Kafka cluster node
* schema-registry
* connect as single Kafka Connector
* ksqldb-server
* ksqldb-cli
* ksql-datagen
* rest-proxy
* ui as simple User interface for Kafka

**Note**: The [mqtt example](../examples/03-kafka-connetors/README.md) configures a connector to stream MQTT messages to Kafka. For this example, the connector needs to connect to an MQTT broker such as the one started with the https://github.com/massimocallisto/iot-simulator project. To allow the container to connect to the external service, edit the following line in docker compose by replacing the IP address with the IP address where the MQTT broker is running:

```
extra_hosts:
  - "mqtt-broker:192.168.205.8"
```




## Start the cluster

Just run the following command to start all the components:

    docker-compose up

The project is already configured to execute the provided [examples](../examples/).

When the services have started, checkout the web ui at http://localhost:7777 replacing localhost if needed.


