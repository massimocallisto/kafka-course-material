'''
Run with

docker run --rm \
	--name spark-submit \
	--network=mqtt_default \
	--link spark-master \
	--link spark-worker-1 \
	--add-host=kafka:192.168.17.111 \
	-e ENABLE_INIT_DAEMON=false \
	-v /home/filippetti/examples:/spark/examples \
	bde2020/spark-submit  bash \
	/spark/bin/spark-submit \
	--master spark://spark-master:7077 \
	--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5,org.elasticsearch:elasticsearch-hadoop:7.7.0 \
	/spark/examples/ela.py

'''
from pyspark.sql import SparkSession,SQLContext
from pyspark.sql.functions import *
import pyspark.sql.functions as F
from pyspark.sql.types import *
import json
from pyspark.sql import Row

# Start Spark Session
spark = SparkSession \
      .builder \
      .config("es.index.auto.create", "true") \
      .appName("TEST--ANALYTICS") \
      .getOrCreate()

#.config("es.nodes", "192.168.17.111").config("es.port", "9200")\

# Set log level to (ERROR,INFO,WARNING)
# Comment this line if the script do not perform as expected.
# Indeed in case of exceptions, you cannot see them without this intruction.
spark.sparkContext.setLogLevel("INFO")

# We now create a DataFrame by reading from an existing Kafka topic.
df = spark \
      .readStream \
      .format("kafka") \
      .option("kafka.bootstrap.servers", "192.168.17.111:9092") \
      .option("subscribe", "mqtt.echo") \
      .option("startingOffsets", "earliest") \
      .load() \
      .selectExpr("CAST(key AS STRING)","CAST(value AS STRING)") 

# query 1: topic analysis (see e.g. https://drive.google.com/file/d/1kNAmH2WkcZEi7LyIvn7TqNOBDI7fj26T/view?usp=sharing)
topic = df.withColumn("key", split(col("key"), "/")) \
      .select( \
            col("key")[1].alias("TENANT"),      \
            col("key")[2].alias("CONTEXT"),     \
            col("key")[3].alias("SCOPE"),       \
            col("key")[4].alias("MESSAGE"),     \
            col("key")[5].alias("TYPE 1"),      \
            col("key")[6].alias("TYPE 2"),      \
            col("key")[7].alias("VALUE")        \
      )

# This is the Json Schema for Filippetti devices (see e.g. https://drive.google.com/file/d/1kNAmH2WkcZEi7LyIvn7TqNOBDI7fj26T/view?usp=sharing)
schema = StructType([
      StructField("t", StringType(), True),
      StructField("tz", TimestampType(), True),
      StructField("ref", StringType(), True),
      StructField("uuid", StringType(), True),
      StructField("ruid", StringType(), True),
      StructField("type", StringType(), True),
      StructField("m", ArrayType(StructType([
            StructField("k", StringType(), True),
            StructField("t", StringType(), True),
            StructField("tz", TimestampType(), True),
            StructField("v", DoubleType(), True),
            StructField("u", StringType(), True),
            StructField("x", DoubleType(), True),
            StructField("p", DoubleType(), True),
            StructField("l", DoubleType(), True)
            ]))
      )])

'''

#query analysis for the payloads
message = df.withColumn("data", from_json("value", schema)) \
      .select(
            col('data.type'),
            col('data.ref'),
            col('data.m')[0]['k'],
            col('data.m')[0]['v'],
            col('data.m')[1]['k'],
            col('data.m')[1]['v']
      )

'''

#Start running the query that prints the results to the console
#CONTINUOUS PROCESSING
#query_message = message \
#      .writeStream \
#      .format("console") \
#      .outputMode("Update") \
#      .trigger(continuous="1 second") \
#      .start()
'''
query_topic = topic \
      .writeStream \
      .format("org.elasticsearch.spark.sql") \
      .outputMode("Update") \
      .option("checkpointLocation", "/tmp")\
      .option("es.nodes", "192.168.17.111") \
      .option("es.resource", "index/type") 
      .option("es.mapping.id", "mappingId")
      .trigger(continuous="1 second") \
      .start("index/type")
query_topic = topic \
      .writeStream
      .outputMode("append")
      .format("org.elasticsearch.spark.sql")
      .option("checkpointLocation","/tmp")
      .option("es.resource.write","spark/_doc")
      .option("es.nodes","192.168.17.111")
      .trigger(Trigger.ProcessingTime("10 seconds"))
      .start()
'''

topic.writeStream.outputMode("append").format("org.elasticsearch.spark.sql").option("checkpointLocation","/tmp").option("es.port","9200").option("es.nodes","192.168.17.111").start("spark/_doc").awaitTermination()

#query_message.awaitTermination()
#query_topic.awaitTermination()
