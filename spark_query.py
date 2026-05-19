from pyspark.sql import SparkSession

# Создаём сессию
spark = SparkSession.builder \
    .appName("TransportProject") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

# Уменьшаем шум логов
spark.sparkContext.setLogLevel("WARN")

# Читаем CSV из HDFS с автоопределением схемы
drivers_df = spark.read.load(
    "hdfs://localhost:9000/user/hduser/course_project/drivers.csv",
    format="csv", sep=",", inferSchema="true", header="true"
)
cars_df = spark.read.load(
    "hdfs://localhost:9000/user/hduser/course_project/cars.csv",
    format="csv", sep=",", inferSchema="true", header="true"
)
trips_df = spark.read.load(
    "hdfs://localhost:9000/user/hduser/course_project/trips.csv",
    format="csv", sep=",", inferSchema="true", header="true"
)

# Регистрируем как временные таблицы
drivers_df.createOrReplaceTempView("drivers")
cars_df.createOrReplaceTempView("cars")
trips_df.createOrReplaceTempView("trips")

# Запрос: водитель и машина с максимальной длительностью поездки
# ВАЖНО: кириллические имена колонок должны быть в обратных кавычках (`)
query = """
SELECT d.`персональные_данные_водителя` AS `Водитель`,
       c.`регистрационный_номер` AS `Машина`,
       t.`длительность_поездки` AS `Длительность`
FROM trips t
JOIN drivers d ON t.`id_водителя` = d.`id_водителя`
JOIN cars c ON t.`id_машины` = c.`id_машины`
WHERE t.`длительность_поездки` = (SELECT MAX(`длительность_поездки`) FROM trips)
"""

result = spark.sql(query)
result.show()

# Пауза для просмотра монитора Spark
input("Enter для завершения сессии Spark...")

spark.stop()
