from kafka import KafkaConsumer

# Create a KafkaConsumer instance
consumer = KafkaConsumer(
    bootstrap_servers=['192.168.205.3:9092'], 
    auto_offset_reset='earliest', 
    enable_auto_commit=False
)

# Subscribe to a specific topic
consumer.subscribe(topics=['my-topic'])

# Poll for new messages
while True:
    #for message in consumer:
    #   print(message)                                                  
    msg = consumer.poll(timeout_ms=10000)
    if msg:
        for tp, messages in msg.items():
            for message in messages:
                # message value and key are raw bytes -- decode if necessary!
                # e.g., for unicode: `message.value.decode('utf-8')`
                print ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
                                                  message.offset, message.key,
                                                  message.value))
    else:
        print("No new messages")
'''
/opt/kafka/bin/kafka-console-producer.sh \
	--topic my-topic \
	--bootstrap-server localhost:9092
'''
