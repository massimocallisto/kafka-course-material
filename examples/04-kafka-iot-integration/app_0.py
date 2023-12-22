from pyspark.sql import SparkSession,SQLContext
from pyspark.sql.functions import *
import pyspark.sql.functions as F
from pyspark.sql.types import *
import json
from pyspark.sql import Row

#Avvio sessione Spark
spark = SparkSession \
    .builder \
    .appName("TEST--ANALYTICS") \
    .getOrCreate()

#Set del livello di Log (ERROR,INFO,WARNING)
# Comment this line if the script do not perform as expected.
# Indeed in case of exceptions, you cannot see them without this intruction.
spark.sparkContext.setLogLevel("ERROR")

#Creazione del DataFrame per leggere i dati del tenant infn.it
kafka_df = spark \
      .readStream \
      .format("kafka") \
      .option("kafka.bootstrap.servers", "192.168.205.3:9092") \
      .option("subscribe", "mqtt.echo") \
      .option("startingOffsets", "earliest") \
      .load() \
      .selectExpr("CAST(key AS STRING)","CAST(value AS STRING)") 

#query per analisi del payload infn
topic = kafka_df.select(col("key")).alias("topic")
message_infn = kafka_df.select(col("value")).alias("message_infn")


#Start running the query that prints the results to the console

#CONTINUOUS PROCESSING
query_message = message_infn.writeStream.format("console").outputMode("Update").trigger(continuous="1 second").start()
query_topic = topic.writeStream.format("console").outputMode("Update").trigger(continuous="1 second").start()
#query_demo = topic_demo.writeStream.format("console").outputMode("append").trigger(continuous="1 second").start()


spark.streams.awaitAnyTermination()

'''
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.13:3.2.4 \
  app_0.py
'''

