from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Inicializar SparkSession en modo local
spark = SparkSession.builder \
    .appName("EjemploLocal") \
    .master("local[*]") \
    .config("spark.executor.memory", "70g") \
    .config("spark.driver.memory", "50g") \
    .config("spark.memory.offHeap.enabled", "true") \
    .config("spark.memory.offHeap.size", "16g") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.3") \
    .getOrCreate()

kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("kafka.security.protocol", "SASL_PLAINTEXT")
    .option("kafka.sasl.mechanism", "SCRAM-SHA-256")
    .option("kafka.sasl.jaas.config", 'org.apache.kafka.common.security.scram.ScramLoginModule required username="myuser" password="mypass";')
    .option("subscribe", "r023hf")
    .option("startingOffsets", "earliest")
    .load()
)

parsed_df = kafka_df.select(
    col("key").cast("string"),
    col("value").cast("string"),
    col("timestamp")
)

query = (
    parsed_df
    .writeStream
    .outputMode("append")
    .format("console")
    .option("truncate", "false")
    .start()
)

query.awaitTermination()

# Detener SparkSession
spark.stop()
