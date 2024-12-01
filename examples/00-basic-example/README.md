# Simple console-based Kafka examples

The examples are the ones of https://kafka.apache.org/quickstart 

## Docker execution
Note that if you are running the cluster with Docker, you will need to run the following commands from the Broker container.

1. Login to the container:

		docker exec -it broker bash

2. In each commend remove `./bin/`, replace `localhost:9092` with `broker:29092`. For instance:

```
kafka-topics.sh --create \
	--topic quickstart-events \
	--bootstrap-server broker:29092
```


## Command execution

Create a topic `quickstart-events`

```
./bin/kafka-topics.sh --create \
	--topic quickstart-events \
	--bootstrap-server localhost:9092
```

Get some statistics form the created topic.

```
./bin/kafka-topics.sh --describe \
	--topic quickstart-events \
	--bootstrap-server localhost:9092
```

Send some message on the example topic.

```
./bin/kafka-console-producer.sh \
	--topic quickstart-events \
	--bootstrap-server localhost:9092
```

The below example will print the new messages in the console.

```
./bin/kafka-console-consumer.sh \
	--topic quickstart-events \
	--from-beginning \
	--bootstrap-server localhost:9092
```

Execute the previous command without the option `--from-beginning`. This time the consumer lists also the existing messages.

```
./bin/kafka-console-consumer.sh \
	--topic quickstart-events \
	--bootstrap-server localhost:9092
```

