from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

def write_mongo_row(df, epoch_id):
    # mongoURL = "mongodb://localhost:27017/sentiment.sentiment2"
    # df.write.format("mongodb").mode("append").option("uri",mongoURL).save()
    df.write.format("mongodb").mode("append").save()
    pass


if __name__ == "__main__":
    # create Spark session
    # spark = SparkSession.builder.master("spark://master:7077").appName("TwitterSentimentAnalysis").getOrCreate()
    spark = SparkSession.builder.appName("MQTTForwarder").getOrCreate()

    # read the tweet data from socket
    # lines = spark.readStream.format("socket").option("host", "0.0.0.0").option("port", 5555).load()
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "192.168.205.8:29092") \
        .option("subscribe", "mqtt") \
        .load()
    kafka_df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    lines = kafka_df.select(col("value")).alias("lines")

    # words = words.repartition(1)
    # https://medium.com/globant/multiple-sinks-in-spark-structured-streaming-38997d9a59e9
    # https://stackoverflow.com/questions/45618489/executing-separate-streaming-queries-in-spark-structured-streaming
    query = lines.writeStream.queryName("all_messages") \
        .outputMode("update").format("console") \
        .option("checkpointLocation", "./check") \
        .trigger(processingTime='5 seconds').start()

    query2=lines.writeStream.foreachBatch(write_mongo_row).start()

    # query.awaitTermination()
    # query2.awaitTermination()
    spark.streams.awaitAnyTermination()

'''
spark-submit \
  --master spark://192.168.205.8:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:10.4.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 \
  --conf "spark.mongodb.write.connection.uri=mongodb://192.168.205.8/datalake.iot" \
  spark_job.py
'''