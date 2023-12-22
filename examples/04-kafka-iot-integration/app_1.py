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
df_infn = spark \
      .readStream \
      .format("kafka") \
      .option("kafka.bootstrap.servers", "192.168.205.3:9092") \
      .option("subscribe", "mqtt.echo") \
      .option("startingOffsets", "earliest") \
      .load() \
      .selectExpr("CAST(key AS STRING)","CAST(value AS STRING)") 

#Definizione del Payload in formato Json
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
                                              StructField("l", DoubleType(), True)])))])
#query per analisi dei topic infn
topic_infn = df_infn.withColumn("key", split(col("key"), "/")).select(col("key")[1].alias("TENANT"), col("key")[2].alias("CONTEXT"), col("key")[3].alias("SCOPE"),\
                       col("key")[4].alias("MESSAGE"),col("key")[5].alias("TYPE 1"),col("key")[6].alias("TYPE 2"),col("key")[7].alias("VALUE")) #.filter(col('MESSAGE')=='snapshot')

#query per analisi del payload infn
message_infn = df_infn.withColumn("data", from_json("value", schema))\
            .select(col('data.type'),col('data.ref'),col('data.m')[0]['k'],col('data.m')[0]['v'],\
                    col('data.m')[1]['k'],col('data.m')[1]['v']) #.filter(col('data.type')=='gasmeter')


'''
#Creazione del DataFrame per tenant demo
df_demo = spark \
      .readStream \
      .format("kafka") \
      .option("kafka.bootstrap.servers", "localhost:9092") \
      .option("subscribe", "demo") \
      .option("startingOffsets", "earliest") \
      .load() \
      .selectExpr("CAST(key AS STRING)","CAST(value AS STRING)") 

topic_demo = df_demo.withColumn("key", split(col("key"), "/")).select(col("key")[1].alias("TENANT DEMO"), col("key")[2].alias("CONTEXT DEMO"), col("key")[3].alias("SCOPE DEMO"),\
                       col("key")[4].alias("MESSAGE DEMO"),col("key")[5].alias("TYPE 1 DEMO"),col("key")[6].alias("TYPE 2 DEMO"),col("key")[7].alias("VALUE DEMO"))

'''


#Start running the query that prints the results to the console

#CONTINUOUS PROCESSING
query_message = message_infn.writeStream.format("console").outputMode("Update").trigger(continuous="1 second").start()
query_topic = topic_infn.writeStream.format("console").outputMode("Update").trigger(continuous="1 second").start()
#query_demo = topic_demo.writeStream.format("console").outputMode("append").trigger(continuous="1 second").start()


#query_message.awaitTermination()
#query_topic.awaitTermination()
spark.streams.awaitAnyTermination()


'''
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.13:3.2.4 \
  app_0.py
'''