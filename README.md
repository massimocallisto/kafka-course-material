# Technologies for Big Data Management - Kafka material

Kafka course material



## Installing Apache Kafka 

See the [installation/README.md](installation/README.md) guide.




Source:
- https://www.linuxtechi.com/how-to-install-apache-kafka-on-ubuntu/

### Requirements
- Ubuntu 18.04 64 bit
- Java JDK 8 (see EDA/Spark Installation)

### Installation 
Add a service kafka user:
```
sudo useradd kafka -m
sudo passwd kafka
sudo adduser kafka sudo
```

Download and unpack in `/opt`
```
wget https://archive.apache.org/dist/kafka/2.5.0/kafka_2.12-2.5.0.tgz
tar -xzf kafka_2.12-2.5.0.tgz
sudo mv kafka_2.12-2.5.0 /opt
cd /opt/
sudo ln -s kafka_2.12-2.5.0 kafka
cd kafka/config/
nano server.properties
```

Add this line:
    
    delete.topic.enable = true

Create two service respectively for Zookeeper and Kafka. For Zookeeper type `sudo nano /etc/systemd/system/zookeeper.service` and add:
```
[Unit]
Requires=network.target remote-fs.target
After=network.target remote-fs.target

[Service]
Type=simple
User=kafka
Environment=JAVA_HOME=/usr/local/java
ExecStart=/opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties
ExecStop=/opt/kafka/bin/zookeeper-server-stop.sh
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
```

For Zookeeper type `sudo nano /etc/systemd/system/kafka.service` and add:
```
[Unit]
Requires=zookeeper.service
After=zookeeper.service

[Service]
Type=simple
User=kafka
Environment=JAVA_HOME=/opt/java
ExecStart=/bin/sh -c '/opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties > /var/log/kafka.log 2>&1'
ExecStop=/opt/kafka/bin/kafka-server-stop.sh
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
```

Then reload the services:

    sudo systemctl daemon-reload

Add permission to kafka user:
    
    sudo chowm -R kafka /opt/kafka*
    sudo touch /var/log/kafka.log
    sudo chowm kafka /var/log/kafka.log

Enable and start the services:
```
sudo systemctl enable zookeeper
sudo systemctl start zookeeper
sudo systemctl status zookeeper
```
```
sudo systemctl enable kafka
sudo systemctl start kafka
sudo systemctl status kafka
```

## Hello World example

Set `KAFKA_HOME=/opt/kafka` and create a topic:

    $KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic TutorialTopic
    $KAFKA_HOME/bin/kafka-topics.sh --zookeeper localhost:2181 --describe

Message Echo:

    echo "Hello, World" | $KAFKA_HOME/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic TutorialTopic > /dev/null

Message dump:

    $KAFKA_HOME/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic TutorialTopic --from-beginning


## Monitoring

You can start from the console  **kafdrop** (https://github.com/obsidiandynamics/kafdrop):
```
# remember to change IP address to your VM IP and hostname 
docker run --rm -p 9000:9000 \
    -e KAFKA_BROKERCONNECT=kafka:9092 \
    -e JVM_OPTS="-Xms32M -Xmx64M" \
    -e SERVER_SERVLET_CONTEXTPATH="/" \
    --name kafdrop \
    --add-host=kafka:192.168.17.128 \
    --add-host=ubuntu:192.168.17.128 \
    obsidiandynamics/kafdrop
```
install_kafka.md
Visualizzazione di install_kafka.md.
