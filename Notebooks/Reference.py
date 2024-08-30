# Databricks notebook source
# DBTITLE 1,Databricks Internal Path
import os
os.chdir("/Workspace/Repos/dev-main/Databricks_Enterprise_Investment/6_QA/Fact_Table_Test")
os.system('ls')
os.chdir("/Workspace/Users/vincent.yu@imcoinvest.com/Test/vyu_notebook")
adlsPath = 'abfss://qastatic@stadlsidpdevcanc.dfs.core.windows.net/IDP-1.0/Fact_IDW_Position_Static/*.csv'

# COMMAND ----------

# DBTITLE 1,framework path
tableName = `db-dev-ei`.curated_common.fact_idw_dyn_cash_activity

# COMMAND ----------

# DBTITLE 1,read from files
df_static_Daily_Bmk_Security_Performance_static = (
    spark.read.format("csv")
    .option("Header", "true")
    .option("maxRowsInMemory", 20)
    .option("inferSchema", "true")
    .load(
        "abfss://qastatic@stadlsidpdevcanc.dfs.core.windows.net/IDP-1.0/Daily_Bmk_Security_Performance_static/*.csv"
    )
)

# COMMAND ----------

# DBTITLE 1,mostly used pyspark code
from pyspark.sql.functions import col, date_trunc, countDistinct, when, concat_ws, trim, Row, row_number, regexp_replace, expr, sum as _sum, collect_set, lit, size
from pyspark.sql.types import IntegerType, LongType, FloatType, DoubleType, DecimalType, StructType, StructField, StringType, BooleanType, ArrayType
from pyspark.sql.window import Window
from decimal import Decimal

df_curated = spark.sql("SELECT * FROM `db-dev-ei`.curated_common.${table_name}")
df_static = df_static.withColumn("Effective_Start_Datetime", date_trunc("second", col("Effective_Start_Datetime")))
matched_df = matched_df.withColumn(col_name, when(col(col_name).isNull(), "NULL").otherwise(col(col_name)))
matched_df = matched_df.withColumn("curated_concat_key", concat_ws("~", *[col(col_name) for col_name in curated_columns_list]))
matched_df = matched_df.withColumn("concat_key_match", (col("curated_concat_key") == col("static_concat_key")).cast("boolean"))
df_curated = df_curated.filter(df_curated.Source_Current_Flag == 1)
df_curated = df_curated.toDF(*(col.lower() for col in df_curated.columns))
schema_difference = df_curated.schema.simpleString() != df_curated_filtered.schema.simpleString()
distinct_count = df_curated.select(countDistinct(primary_key)).first()[0]
curated_distinct_df = df_curated_filtered.select(col_name).distinct()
curated_alias = df_curated_renamed.alias("curated")
df_static_renamed = df_static.select([col(col_name).alias(f"static_{col_name}") for col_name in df_static.columns])
df_curated_dim_security = df_curated_dim_security.withColumnRenamed("DIM_SECURITY_KEY", "curated_dim_security_key")
matched_df = df_static_renamed.join(df_curated_renamed, df_static_renamed.primary_key == df_curated_renamed.primary_key, "inner", "leftanti") 
non_matched_curated_sorted = non_matched_curated.orderBy(col("primary_key").asc())
curated_non_match_keys = non_matched_curated_sorted.select("primary_key").dropna()
matching_keys = static_non_match_keys.join(df_curated_full, static_non_match_keys.primary_key == df_curated_full.primary_key, "inner").dropDuplicates(["primary_key"])
display(df_static_full.select("primary_key", "Is_Current_Flag").where(df_static_full.primary_key.isin(['5421865','5421866'])))
static_columns = [col for col in matched_df.columns if col.startswith("static_")]
static_columns = filtered_comparison_df.select("Static Column").collect()
data = [Row(name='Alice', age=30), Row(name='Bob', age=25), Row(name='Catherine', age=29)]
df = spark.createDataFrame(data)
column_values = df.select("age").rdd.flatMap(lambda x: x).collect()
column_name = "age" --> values_list = [row[column_name] for row in df.select(column_name).collect()]
curated_columns_list = curated_columns_df.select("Curated Column").toPandas()["Curated Column"].tolist()
for index, column in enumerate(curated_columns_list):
    matched_df = matched_df.withColumn(f"{column}_matching", when(col(column) == col(static_columns_list[index]), True).otherwise(False))
windowSpec_curated = Window.partitionBy(*primary_key).orderBy(col(duplicate_date_column).desc())
df_curated_filtered = df_curated_filtered.withColumn("row_number", row_number().over(windowSpec_curated)) \
    .filter(col("row_number") == 1) \
    .drop("row_number")
 curated_distinct_values_count = df_curated_filtered.agg(size(collect_set(col_name)).alias("count")).collect()[0]["count"]

# COMMAND ----------

# DBTITLE 1,python
different_columns = list(set(curated_columns) ^ set(static_columns))
curated_columns_list.sort()
comparison_results = []
for static_col, curated_col in zip(static_columns, curated_columns):
    comparison_result = matched_df.filter(col(static_col) != col(curated_col)).count()
    comparison_results.append((static_col, curated_col, comparison_result))
if comparison_results:
    comparison_df = spark.createDataFrame(comparison_results, ["Static Column", "Curated Column", "Mismatch Count"])    

sys.dont_write_bytecode = True
os.chdir("/Workspace/Users/vincent.yu@imcoinvest.com/Test/") 
os.system("PYTHONDONTWRITEBYTECODE=1 python -m pytest -v -p no:cacheprovider -s test_Static_to_raw.py")
for index, (curated_col, static_col) in enumerate(zip(schema1_ordered, schema2_ordered), start=1):
    if curated_col != static_col:
        misaligned_columns.append((index, curated_col, static_col))
 differences = set(curated_values).symmetric_difference(set(static_values))        

# COMMAND ----------

# DBTITLE 1,Frequently used constants
static_table_name = "Fact_Daily_Bmk_Performance_Static"
curated_schema = "Insert_Databricks_Schema"
curated_table_name = "Insert_Databricks_Table_Name"
primary_key = ["Insert_Primary_Key_1", "Insert_Primary_Key_2"]
static_filter = "filter_column == 1"
curated_filter = "filter_column == 1"
duplicate_date_column =  "date_column"

# COMMAND ----------

# DBTITLE 1,Manual create stuff
# Define the schema explicitly
schema = StructType([
    StructField("Column", StringType(), True),
    StructField("Differences", ArrayType(StringType()), True),
    StructField("Number of Differences", StringType(), True)
])

# Convert the dictionary to a list of rows that match the defined schema
rows = []
for k, v in distinct_values_comparison.items():
    row = (k, v['differences'], str(v['num_differences']))
    rows.append(row)

# COMMAND ----------

# DBTITLE 1,userful functions
 # Function to find differences in schemas
def find_schema_differences(schema1: StructType, schema2: StructType):
    schema1_fields = set(schema1.names)
    schema2_fields = set(schema2.names)
    
    schema1_ordered = [field for field in schema1.names if field in schema2_fields]
    schema2_ordered = [field for field in schema2.names if field in schema1_fields]

    misaligned_columns = []
    for index, (curated_col, static_col) in enumerate(zip(schema1_ordered, schema2_ordered), start=1):
        if curated_col != static_col:
            misaligned_columns.append((index, curated_col, static_col))

    order_difference = len(misaligned_columns) > 0

    common_fields = schema1_fields.intersection(schema2_fields)
    
    differences = {}
    for field in common_fields:
        if schema1[field].dataType != schema2[field].dataType:
            differences[field] = (schema1[field].dataType.simpleString(), schema2[field].dataType.simpleString())
    
    only_in_schema1 = schema1_fields - common_fields
    only_in_schema2 = schema2_fields - common_fields
    
    return differences, order_difference, only_in_schema1, only_in_schema2, common_fields

# Display the result of the schema comparison
if schema_difference:
    differences, order_difference, only_in_schema1, only_in_schema2, common_fields = find_schema_differences(df_curated_filtered.schema, df_static_filtered.schema)
    display(f"Schemas orders are not the same: {order_difference}")
    display(f"Only in df_curated_filtered (curated schema): {only_in_schema1}.")
    display(f"Only in df_static_filtered (static schema): {only_in_schema2}.")
else:
    display("Schemas are identical.")
    display(f"Schemas orders are the same: {order_difference}")
