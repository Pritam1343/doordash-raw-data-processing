from pyspark.sql import SparkSession
from pyspark.sql.functions import * 
from pyspark.sql.types import IntegerType, StringType,StructType, StructField,DoubleType

schema=StructType([
    StructField("emp_id",IntegerType(),True),
    StructField("emp_name",StringType(),True),
    StructField("dept_id",IntegerType(),True),
    StructField("salary",DoubleType(),True)
])

spark=SparkSession.builder.appName("read_csv").getOrCreate()
df=spark.read.format("CSV").schema(schema).load("D:\CSV_files\emp.csv")
df1=df.withColumn("Salary_category",when(df['salary']<30000,"Low").when(df['salary'].between(31000,40000),"Medium").otherwise("High"))
df2=df1.groupby(df1['Salary_category']).agg(count(df1['emp_id']).alias("Count_of_employees"),sum(df1['salary']).alias("Total_salary"),avg(df1['salary']).alias("Average_salary"))
df2.show(truncate=False)

