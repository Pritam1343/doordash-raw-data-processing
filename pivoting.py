from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark=SparkSession.builder.appName("pivoting").getOrCreate()

df=spark.read.format("csv").option("header","true").option("inferschema","true").load("D:\CSV_files\marks.csv")
df.show(truncate=False)

pivot_df=df.groupBy("StudentID").pivot("Subject").agg(sum("Score").alias("Score")).orderBy("StudentID")
pivot_df.show(truncate=False)