from kafka import KafkaConsumer

# Create a KafkaConsumer instance
consumer = KafkaConsumer(
    bootstrap_servers=['primary:9092'], 
    auto_offset_reset='earliest', 
    enable_auto_commit=False
)

# Subscribe to a specific topic
consumer.subscribe(topics=['my-topic'])

# Poll for new messages
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
'''
/opt/kafka/bin/kafka-console-producer.sh \
	--topic my-topic \
	--bootstrap-server localhost:9092
'''
