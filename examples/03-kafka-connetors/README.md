# Kafka Connectors Example

## Requirements

**Kafka Cluster**
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

## Submit the configuration via Postman
Import the [Kafka.postman_collection.json](Kafka.postman_collection.json) in Pstman to submit the configuration described below. Remember to replace the IP address with your VM IP address. 

## MQTT Connector
- https://www.confluent.io/hub/confluentinc/kafka-connect-mqtt

**Note**: the connector require a license key. However, you can use this connector for a 30-day trial period without a license key.

Download the connector from https://www.confluent.io/hub/confluentinc/kafka-connect-mqtt, unpack and copy the lib content in `/opt/kafka/plugins` (create a sub-folder `mqtt-connector`).

The post the connector configuration:

```
{
  "name": "mqtt-source",
  "config": {
    "connector.class": "io.confluent.connect.mqtt.MqttSourceConnector",
    "tasks.max": "1",
    "mqtt.server.uri": "tcp://localhost:1883",
    "mqtt.topics": "/#",
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

    curl -s -X POST -H 'Content-Type: application/json' http://localhost:8083/connectors -d @./mqtt_connector.json

The below example will allow print the new messages in the console.

```
./bin/kafka-console-consumer.sh \
	--topic mqtt.echo \
	--bootstrap-server localhost:9092
```

## File sink
- https://docs.confluent.io/platform/current/connect/filestream_connector.html

Copy jar from `/opt/kafka/libs/connect-file-3.6.1.jar` to `/opt/kafka/plugins`. Then post the following JSON:

```
{
    "name": "file-sink",
    "config": {
        "connector.class": "org.apache.kafka.connect.file.FileStreamSinkConnector",
        "tasks.max": "1",
        "file": "/tmp/test.sink.txt",
        "key.converter": "org.apache.kafka.connect.storage.StringConverter",
        "value.converter": "org.apache.kafka.connect.storage.StringConverter",
        "topics": "mqtt.echo"
    }
}
```

Then submit to the worker:

    curl -s -X POST -H 'Content-Type: application/json' http://localhost:8083/connectors -d @./filesink_connector.json
    curl -s -X GET -H 'Content-Type: application/json' http://localhost:8083/connectors/file-sink/status

Then check the file content:

    tail -f /tmp/test.sink.txt


## Mongo plugin installation
- https://contact-rajeshvinayagam.medium.com/mongodb-kafka-connectors-a-peek-561e2ed151a9

Download source package from https://www.confluent.io/hub/mongodb/kafka-connect-mongodb/ and unpack in some folder `MONGO_CONNECTOR`.
Copy the content of `MONGO_CONNECTOR/lib into /opt/kafka/plugins/mongodb-connector`

Start/restart the distributed connector and check if the plugin is now available:

    curl localhost:8083/connector-plugins | jq

If you can read `com.mongodb.kafka.connect.MongoSinkConnector` then it is ok.

## Run the connector

First provide a configuration as JOSN file to submit to the worker connector. Save it as `~/mongo_connector.json`

```json
{
    "name": "mongo-sink",
    "config": {
      "connector.class": "com.mongodb.kafka.connect.MongoSinkConnector",
      "key.converter": "org.apache.kafka.connect.storage.StringConverter",
      "value.converter": "org.apache.kafka.connect.storage.StringConverter",
      "topics": "mqtt.echo",
      "connection.uri": "mongodb://localhost",
      "database": "mqtt_echo",
      "collection": "data",
      "schema.enable": "false"
    }
  }

```

Then submit to the worker:

    curl -s -X POST -H 'Content-Type: application/json' http://localhost:8083/connectors -d @./mongo_connector.json

Verify that it is working:

    curl -s "http://localhost:8083/connectors"
    curl -s "http://localhost:8083/connectors/mongo-sink/status"

The connetor is already running. You should not create the topic `mqtt.echo`

Finally connect to Mongo to see if the data is persisted (e.g. you can use DBeaver).

To stop and delete the connector run:

    curl -s -X DELETE -H 'Content-Type: application/json' "http://localhost:8083/connectors/mongo-sink"


## Elastic plugin installation (to validate)
Source:
- https://docs.confluent.io/current/connect/kafka-connect-elasticsearch/index.html
- https://www.confluent.io/blog/kafka-elasticsearch-connector-tutorial/?_ga=2.136982519.634568600.1590446777-227719131.1589011689

**Note**: you need a running instance of Elasticsearch. See e.g. https://github.com/massimocallisto/elastic_iot_poc/tree/main/single_instance

### Elastic search configuration
In order to preserve mapping you should also created an index (named mqtt.echo according to the example below). 
This is not necessary but if you have nested fields it would be better to do it.
To post an index you can perform the following index post creation:

```
curl -s -X PUT -H 'Content-Type: application/json' http://localhost:9200/mqtt.echo -d @'{
  "settings": {
    "index": {
      "number_of_shards": 5,
      "number_of_replicas": 1
    }
  },
  "mappings": {
    "properties": {
      "m": {
        "type": "nested"
      },
      "r": {
        "type": "nested"
      }
    }
  }
}'
```

### Plugin configuration

Download source package from https://www.confluent.io/hub/confluentinc/kafka-connect-elasticsearch/ and unpack in some folder `ELA_CONNECTOR`.
Copy the content of `ELA_CONNECTOR/lib into /opt/kafka/plugins/elasticsearch-connector`

**Note**: in kafka 2.5.x there is no guava library and the connector rises an error (e.g. https://stackoverflow.com/questions/62015340/elasticsearch-connector-doesnt-work-java-lang-noclassdeffounderror-com-googl). 
As a workaround, Copy the jar manually (guava-20.0. jar) from the previous Kafka distribution.

Start/restart the distributed connector and check if the plugin is now available:

    curl localhost:8083/connector-plugins | jq

If you can read `io.confluent.connect.elasticsearch.ElasticsearchSinkConnector` then it is ok.

### Run the connector

First provide a configuration as JOSN file to submit to the worker connector. Save it as `~/ela_connector.json`

```json
see the json

```

Then submit to the worker:

    curl -s -X POST -H 'Content-Type: application/json' http://localhost:8083/connectors -d @./ela_connector.json

Verify that it is working:

    curl -s "http://localhost:8083/connectors"
    curl -s "http://localhost:8083/connectors/ela/status"

The connetor is already running. You should not create the topic `mqtt.echo`

Finally connect to Kibana or Elastic to check incoming messages.

To stop and delete the connector run:

    curl -s -X DELETE -H 'Content-Type: application/json' "http://localhost:8083/connectors/ela"
