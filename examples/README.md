# Kafka Examples

This directory contains a set of several examples on how to use Kafka, Spark Structured Streaming, etc.


When running the example, if you are experimenting with a Kafka product that never sends messages to Kafka, it may depend on the hostnames.
For example, if you are using the docker compose version of Kafka, the container name is `broker`, which is also a hostname. While this hostname is automatically resolved inside the compose containers, this is not the case externally.

To make the producer aware of the real IP address of this host, you need to modify the `/etc/hosts` file to specify the IP address of the server. For example, in the `/etc/hosts` file you should have a configuration a follows:

```
....
192.168.205.8 broker
...
```