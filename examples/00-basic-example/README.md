# Simple console-based Kafka examples

The examples are the ones of https://kafka.apache.org/quickstart 


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

