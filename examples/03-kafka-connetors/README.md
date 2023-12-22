# Elasticsearch sink example

Source:
- https://docs.confluent.io/current/connect/kafka-connect-elasticsearch/index.html
- https://www.confluent.io/blog/kafka-elasticsearch-connector-tutorial/?_ga=2.136982519.634568600.1590446777-227719131.1589011689


## Requirements

### Kafka Cluster 
It is assemed that Kafka is already running and listening on port 9092.
Set also in console the following variable.

    KAFKA_HOME=/opt/kafka
  
Install also this package (JSON processor):
    
    sudo apt-get install jq

### Elastic search
It is assumed that you are running an Elasticsearch cluster listening on http://localhost:9200.
For a quickstart see `docker-compose.yml` (the mqtt-bridge is optional).
In order to preserve mapping you should also created an index (named mqtt according to the example below). 
This is not necessary but if you have nested fields it would be better to do it.
To post an index you can perform the following index post creation:

```
curl -s -X PUT -H 'Content-Type: application/json' http://192.168.17.111:9200/mqtt -d @'{
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

## Mongo plugin installation

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

Download source package from https://www.confluent.io/hub/confluentinc/kafka-connect-elasticsearch/ and unpack in some folder `ELA_CONNECTOR`.
Copy the content of `ELA_CONNECTOR/lib into /opt/kafka/plugins/elasticsearch-connector`

**Note**: in kafka 2.5.x there is no guava library and the connector rises an error (e.g. https://stackoverflow.com/questions/62015340/elasticsearch-connector-doesnt-work-java-lang-noclassdeffounderror-com-googl). 
As a workaround, Copy the jar manually (guava-20.0. jar) from the previous Kafka distribution.

Start/restart the distributed connector and check if the plugin is now available:

    curl localhost:8083/connector-plugins | jq

If you can read `io.confluent.connect.elasticsearch.ElasticsearchSinkConnector` then it is ok.

## Run the connector

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
