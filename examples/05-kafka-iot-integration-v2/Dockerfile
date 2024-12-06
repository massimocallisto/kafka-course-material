# Use Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY main.py main.py
COPY requirements.txt requirements.txt

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Define default environment variables
ENV MQTT_BROKER=localhost
ENV MQTT_PORT=1883
ENV MQTT_TOPIC="#"
ENV KAFKA_BROKER=localhost:9092
ENV KAFKA_TOPIC=mqtt

# Set the entry point
CMD ["python", "-u", "main.py"]
