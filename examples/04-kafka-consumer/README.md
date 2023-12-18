# MQTT dumper example

Source:
- https://github.com/kaiwaehner/kafka-connect-iot-mqtt-connector-example/blob/master/live-demo-kafka-connect-iot-mqtt-connector.adoc
- https://github.com/kaiwaehner/kafka-connect-iot-mqtt-connector-example/blob/master/live-demo-kafka-connect-iot-mqtt-connector.adoc


## Requirements
It is assemed that Kafka is already running and listening on port 9092.
Set also in console the following variable.

    KAFKA_HOME=/opt/kafka

Install also this package (JSON processor):
    
    sudo apt-get install jq

## Start connector
One can start a standalone connector that takes in input a config file with main parameters or a distributed connector that will wait for incoming request via REST API calls. In this example we are going to use a distribute connector.

    $KAFKA_HOME/bin/connect-distributed.sh $KAFKA_HOME/config/connect-distributed.properties

Then open a new terminal to interact with the connector. For xample you can type the following curls:
- https://docs.confluent.io/current/connect/managing/monitoring.html

```
curl localhost:8083/ | jq
curl localhost:8083/connector-plugins | jq
curl localhost:8083/connectors
```

## MQTT plugin installation

Source:
- https://docs.confluent.io/current/connect/managing/community.html

Download source package from https://www.confluent.io/hub/confluentinc/kafka-connect-mqtt and unpack in some folder MQTT_CONNECTOR.

    wget https://d1i4a15mxbxib1.cloudfront.net/api/plugins/confluentinc/kafka-connect-mqtt/versions/1.6.0/confluentinc-kafka-connect-mqtt-1.6.0.zip
    unzip confluentinc-kafka-connect-mqtt-1.6.0.zip

Copy the content of `confluentinc-kafka-connect-mqtt-1.6.0/lib` into `/opt/kafka/plugins/mqtt-connector`

    sudo mkdir -p /opt/kafka/plugins/mqtt-connector
    cd confluentinc-kafka-connect-mqtt-1.6.0/lib
    sudo cp -R *  /opt/kafka/plugins/mqtt-connector

Also set the plugin directory by editing the file `/opt/kafka/config/connect-distributed.properties`

    # Examples: 
    plugin.path=/usr/local/share/java,/usr/local/share/kafka/plugins,/opt/connectors,
    plugin.path=/opt/kafka/plugins

Start/restart the distributed connector and check if the plugin is now available:

    curl localhost:8083/connector-plugins | jq

If you can read `io.confluent.connect.mqtt.MqttSinkConnector` then it is ok.

## Run MQTT connector
- https://github.com/kaiwaehner/kafka-connect-iot-mqtt-connector-example/blob/master/live-demo-kafka-connect-iot-mqtt-connector.adoc

To run the connector we have to define a configuration as JOSN file to submit to the worker connector. Save it as `~/mqtt_connect.json`

```
{
  "name": "mqtt-source",
  "config": {
    "connector.class": "io.confluent.connect.mqtt.MqttSourceConnector",
    "tasks.max": "1",
    "mqtt.server.uri": "tcp://localhost:1883",
    "mqtt.topics": "#",
    "kafka.topic": "mqtt.echo",
    "value.converter":"org.apache.kafka.connect.converters.ByteArrayConverter",
    "key.converter":"org.apache.kafka.connect.storage.StringConverter",
    "key.converter.schemas.enable" : "false",
    "value.converter.schemas.enable" : "false",
    "confluent.topic.bootstrap.servers": "localhost:9092",
    "confluent.topic.replication.factor": "1",
    "confluent.license": ""
  }
}

```

Then submit to the worker:

    curl -s -X POST -H 'Content-Type: application/json' http://localhost:8083/connectors -d @/home/filippetti/~/mqtt_connect.json

Verify that it is working:

    curl -s "http://localhost:8083/connectors"
    curl -s "http://localhost:8083/connectors/mqtt-source/status"

The connetor is already running. You should not create the topic `mqtt.echo`

    $KAFKA_HOME/bin/kafka-topics.sh --zookeeper localhost:2181 --describe

If none create it:

    $KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic mqtt.echo


# MQTT broker
Using docker just run:

    docker run -it --name mosquitto -p 1883:1883 eclipse-mosquitto


# Dump messages
From the console if you subscribe with a simple consumer you should see messages sent to the broker

    $KAFKA_HOME/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic mqtt.echo --from-beginning

From a mqtt client publish some message:

    mqtt_pub -h localhost -t "atopic" -m "a message"