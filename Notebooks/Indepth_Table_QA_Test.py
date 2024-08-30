# Databricks notebook source
from pyspark.sql.functions import col, row_number, countDistinct, when, concat_ws, trim, date_trunc, regexp_replace, expr, sum as _sum, collect_set, lit, size
from pyspark.sql.types import IntegerType, LongType, FloatType, DoubleType, DecimalType, StructType, StructField, StringType, BooleanType, ArrayType
from pyspark.sql.window import Window
from decimal import Decimal

# COMMAND ----------

# MAGIC %run "../../Config"

# COMMAND ----------

# This code block initializes variables for table names, primary keys, filters, and a date column for handling duplicates.
# - static_table_name: Name of the static table to be processed.
# - curated_schema: Schema name for the curated table in Databricks.
# - curated_table_name: Name of the curated table to be processed.
# - primary_key: List of columns that form the primary key for deduplication.
# - static_filter: Filter expression to apply on the static table.
# - curated_filter: Filter expression to apply on the curated table.
# - duplicate_date_column: Column name used for ordering records when removing duplicates.

static_table_name = "insert_static_table"
curated_schema = "Insert_Databricks_Schema"
curated_table_name = "Insert_Databricks_Table_Name"
primary_key = ["Insert_Primary_Key_1", "Insert_Primary_Key_2"]
static_filter = "filter_column == 1"
curated_filter = "filter_column == 1"
duplicate_date_column =  "date_column"

# COMMAND ----------



df_static_full_row_count = ""
df_static_filtered_row_count = ""
df_static_full = (
    spark.read.format("csv")
    .option("Header", "true")
    .option("maxRowsInMemory", 20)
    .option("inferSchema", "true")
    .load(
        f"abfss://qastatic@stadlsidp{env}canc.dfs.core.windows.net/IDP-1.0/{static_table_name}/*.csv"
    )
)

df_static_full_row_count = df_static_full.count()

display(f"Full static table row count: {df_static_full_row_count}")

df_static_filtered = df_static_full.filter(static_filter)

df_static_filtered_row_count = df_static_filtered.count()

display(f"Filtered {static_filter} static table row count: {df_static_filtered_row_count}")

# COMMAND ----------



df_curated_full_row_count = ""
df_curated_filtered_row_count = ""
df_curated_full = spark.table(f"`db-{env}-ei`.{curated_schema}.{curated_table_name}")

df_curated_full_row_count = df_curated_full.count()

print(f"Full curated table row count: {df_curated_full_row_count}")

df_curated_filtered = df_curated_full.filter(curated_filter)

df_curated_filtered_row_count = df_curated_filtered.count()

print(f"Filtered {curated_filter} curated table row count: {df_curated_filtered_row_count}")


# COMMAND ----------

# Calculate the delta
delta = df_curated_filtered_row_count - df_static_filtered_row_count

# Determine which table is the cause of the delta
if delta > 0:
    cause_of_delta = "Curated table has more rows than static table"
elif delta < 0:
    cause_of_delta = "Static table has more rows than curated table"
else:
    cause_of_delta = "Both tables have the same number of rows"

if delta < 0:
    delta = abs(delta)

# Descriptive output of the comparison
output_message = f"Curated table row count: {df_curated_filtered_row_count}, Static table row count: {df_static_filtered_row_count}, delta: {delta}, Cause: {cause_of_delta}"
display(output_message)

# COMMAND ----------

# Convert column names to lowercase for df_curated_filtered and df_static_filtered DataFrames
df_curated_filtered = df_curated_filtered.toDF(*[col.lower() for col in df_curated_filtered.columns])
df_static_filtered = df_static_filtered.toDF(*[col.lower() for col in df_static_filtered.columns])

# Convert primary key column names to lowercase
primary_key = [col.lower() for col in primary_key]

# COMMAND ----------

# Compare the schemas of df_curated_filtered and df_static_filtered
schema_difference = df_curated_filtered.schema.simpleString() != df_static_filtered.schema.simpleString()

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

# COMMAND ----------

# Unpack the list of column names for countDistinct
distinct_count_curated = df_curated_filtered.select(countDistinct(*[col(name) for name in primary_key])).first()[0]
duplicated_count_curated = df_curated_filtered.count() - distinct_count_curated

distinct_count_static = df_static_filtered.select(countDistinct(*[col(name) for name in primary_key])).first()[0]
duplicated_count_static = df_static_filtered.count() - distinct_count_static

# For displaying, you might need to adjust the display function to handle dictionary properly
# Here's a simple workaround using print for demonstration
print(f"Curated Total Count: {df_curated_filtered.count()}, Curated Distinct Count: {distinct_count_curated}, Curated Duplicated Count: {duplicated_count_curated}")
print(f"Static Total Count: {df_static_filtered.count()}, Static Distinct Count: {distinct_count_static}, Static Duplicated Count: {duplicated_count_static}")

if duplicated_count_curated == 0 & duplicated_count_static == 0: 
    print(f"No duplicates found based on primary key(s): {primary_key}")

if duplicated_count_curated > 0: 
    windowSpec_curated = Window.partitionBy(*primary_key).orderBy(col(duplicate_date_column).desc())

    # Use row_number to assign a unique sequential number starting from 1 for each group of duplicates, ordered by 'dedup_date' in descending order
    df_curated_filtered = df_curated_filtered.withColumn("row_number", row_number().over(windowSpec_curated)) \
        .filter(col("row_number") == 1) \
        .drop("row_number")

if duplicated_count_static > 0: 

    windowSpec_static = Window.partitionBy(*primary_key).orderBy(col(duplicate_date_column).desc())

    df_static_filtered = df_static_filtered.withColumn("row_number", row_number().over(windowSpec_static)) \
        .filter(col("row_number") == 1) \
        .drop("row_number")

# COMMAND ----------

# Compare the distinct values in specific columns between the curated and static DataFrames.
# It identifies columns that have a single unique value in each DataFrame, as well as columns that have a single unique value of -1.
# The code then checks if the columns with a single unique value are the same between the curated and static DataFrames,
# and also checks if the columns with a single unique value of -1 are the same between the curated and static DataFrames.


dim_columns_all = [c for c in common_fields if c.startswith("dim_")]

columns_with_single_value_curated = []
columns_with_single_value_static = []
columns_with_single_value_curated_minus_one = []
columns_with_single_value_static_minus_one = []

for col_name in dim_columns_all:
    curated_distinct_df = df_curated_filtered.select(col_name).distinct()
    static_distinct_df = df_static_filtered.select(col_name).distinct()
    
    curated_count = curated_distinct_df.count()
    static_count = static_distinct_df.count()
    
    if curated_count == 1:
        if curated_distinct_df.collect()[0][0] == -1:
            columns_with_single_value_curated_minus_one.append(col_name)
        else:
            columns_with_single_value_curated.append(col_name)
    if static_count == 1:
        if static_distinct_df.collect()[0][0] == -1:
            columns_with_single_value_static_minus_one.append(col_name)
        else:
            columns_with_single_value_static.append(col_name)

# Check if columns_with_single_value_curated has the same columns as columns_with_single_value_static
if set(columns_with_single_value_curated) == set(columns_with_single_value_static):
    display("static and curated have the same columns.")
else:
    display("static and curated have different columns.")    

# Check if columns_with_single_value_curated_minus_one has the same columns as columns_with_single_value_static_minus_one
if set(columns_with_single_value_curated_minus_one) == set(columns_with_single_value_static_minus_one):
    display("static and curated of columns with a single unique value of -1 have the same columns.")
else:
    display("static and curated of columns with a single unique value of -1 have different columns.")    

display({"Columns with a single unique value in curated": columns_with_single_value_curated, 
         "Columns with a single unique value in static": columns_with_single_value_static, 
         "Columns with a single unique value of -1 in curated": columns_with_single_value_curated_minus_one,
         "Columns with a single unique value of -1 in static": columns_with_single_value_static_minus_one})

# COMMAND ----------



# This code compares the distinct values in specified columns between the curated and static DataFrames. 
# It checks if the number of distinct values in a column is below a certain threshold for both DataFrames. 
# If the threshold condition is met, it fetches the distinct values for that column in each DataFrame 
# and determines the differences between them. The results are displayed in a DataFrame.

comparison_columns = common_fields

# Initialize an empty list to hold columns that pass the comparison checks
compared_columns = []

# Get the total row count of the dataset
total_rows_curated = df_curated_filtered.count()
total_rows_static = df_static_filtered.count()

distinct_values_comparison = {}

percentage_threshold = .01

# Define the schema explicitly
schema = StructType([
    StructField("Column", StringType(), True),
    StructField("Differences", ArrayType(StringType()), True),
    StructField("Number of Differences", StringType(), True)
])

for col_name in comparison_columns:
    # Use size() to avoid collecting large datasets
    curated_distinct_values_count = df_curated_filtered.agg(size(collect_set(col_name)).alias("count")).collect()[0]["count"]
    static_distinct_values_count = df_static_filtered.agg(size(collect_set(col_name)).alias("count")).collect()[0]["count"]
    
    # Calculate the thresholds based on the defined percentage
    curated_threshold = total_rows_curated * percentage_threshold
    static_threshold = total_rows_static * percentage_threshold
    
    # Check if the number of distinct values is less than the calculated thresholds
    if curated_distinct_values_count < curated_threshold and static_distinct_values_count < static_threshold:
        # Fetch distinct values only if the threshold condition is met
        curated_values = df_curated_filtered.select(collect_set(col_name).alias(f"{col_name}_curated")).collect()[0][0]
        static_values = df_static_filtered.select(collect_set(col_name).alias(f"{col_name}_static")).collect()[0][0]
        
        # Determine the differences
        differences = set(curated_values).symmetric_difference(set(static_values))
        
        distinct_values_comparison[col_name] = {
            "differences": list(differences),  # Store the differences
            "num_differences": len(differences),
        }
        # Add the column name to the list of compared columns
        compared_columns.append(col_name)
    else:
        print(f"Column {col_name} has a number of distinct values exceeding {(percentage_threshold) * 100}% of the dataset size.")

# Convert the dictionary to a list of rows that match the defined schema
rows = []
for k, v in distinct_values_comparison.items():
    row = (k, v['differences'], str(v['num_differences']))
    rows.append(row)

# Update comparison_columns to only include columns that were actually compared
comparison_columns = compared_columns

# Create the DataFrame using the defined schema
distinct_values_comparison_df = spark.createDataFrame(rows, schema=schema)

display(distinct_values_comparison_df)

# COMMAND ----------


numeric_types = ["integer", "long", "float", "double", "decimal"]
potential_numeric_columns = [col for col in common_fields if col not in comparison_columns]
numeric_columns = []

# Convert columns in comparison_columns to DecimalType for both DataFrames
for col_name in potential_numeric_columns:
        try: 
                df_curated_filtered_test = df_curated_filtered.withColumn(col_name, col(col_name).cast(DecimalType()))
                df_static_filtered_test = df_static_filtered.withColumn(col_name, col(col_name).cast(DecimalType()))
                numeric_columns.append(col_name)    
        except Exception as e: 
                print(f"Column {col_name} cannot be casted to decimal type. Skipping.")

numeric_columns += [field.name for field in df_curated_filtered_test.schema.fields if field.dataType.simpleString() in numeric_types]
numeric_columns += [field.name for field in df_static_filtered_test.schema.fields if field.dataType.simpleString() in numeric_types]

# Filter the numeric columns that are common to both DataFrames
common_numeric_columns = [col_name for col_name in numeric_columns if col_name in common_fields]

# Sum all common numeric fields for both DataFrames, dropping NA values before summing
sum_curated = df_curated_filtered_test.na.fill(0, subset=common_numeric_columns).groupBy().agg(*[_sum(col(c)).alias(c) for c in common_numeric_columns])
sum_static = df_static_filtered_test.na.fill(0,subset=common_numeric_columns).groupBy().agg(*[_sum(col(c)).alias(c) for c in common_numeric_columns])

print(f"Numeric columns: {common_numeric_columns}")
for col_name in common_numeric_columns:
    curated_value = sum_curated.select(col_name).collect()[0][0]
    static_value = sum_static.select(col_name).collect()[0][0]
    
    # Convert static_value to Decimal if it's not already one
    try:
        if not isinstance(static_value, Decimal):
            static_value = Decimal(static_value)
        if not isinstance(curated_value, Decimal):
            curated_value = Decimal(curated_value)
        difference = curated_value - static_value
        curated_sum = curated_value
        static_sum = static_value
        delta_percentage = (difference / static_sum) if static_sum != 0 else Decimal('0') 
        print(col_name, curated_sum, static_sum)
        print(f"Difference in summed value between curated and static for {col_name}: {difference:.2f}, {delta_percentage:.2%}")
    except Exception as e:
        print(f"Error calculating difference for {col_name}. Skipping.")

# COMMAND ----------

# Rename columns in df_static_filtered with a check to avoid prefix duplication and excluding primary_key
df_static_filtered_renamed = df_static_filtered.select([col(col_name).alias(f"static_{col_name}" if not col_name.startswith("static_") and col_name not in primary_key else col_name) for col_name in df_static_filtered.columns])

# Rename columns in df_curated_filtered with a check to avoid prefix duplication and excluding primary_key
df_curated_filtered_renamed = df_curated_filtered.select([col(col_name).alias(f"curated_{col_name}" if not col_name.startswith("curated_") and col_name not in primary_key else col_name) for col_name in df_curated_filtered.columns])

# COMMAND ----------

# Function to apply cleaning, replacement, and truncation based on column data type
def clean_and_truncate_column(df, col_name):
    df = df.withColumn(col_name, trim(col(col_name)))
    df = df.withColumn(col_name, expr(f"replace({col_name}, ' ', '')"))
    df = df.withColumn(col_name, when(col(col_name) == "", None).otherwise(col(col_name)))
    df = df.withColumn(col_name, when(col(col_name).isNull(), "NULL").otherwise(col(col_name)))
    df = df.withColumn(col_name, regexp_replace(col(col_name), '"', ''))
    if 'datetime' in col_name:  
        df = df.withColumn(col_name, date_trunc("second", col(col_name)))
    if 'date' in col_name: 
        df = df.withColumn(col_name, col(col_name).cast("string"))    
    return df

for col_name in primary_key:
    df_static_filtered_renamed_alias = clean_and_truncate_column(df_static_filtered_renamed, col_name)
    df_curated_filtered_renamed_alias = clean_and_truncate_column(df_curated_filtered_renamed, col_name)

# Alias assignment remains the same
df_static_filtered_renamed_alias = df_static_filtered_renamed_alias.alias("static")
df_curated_filtered_renamed_alias = df_curated_filtered_renamed_alias.alias("curated")

# COMMAND ----------

#Joins static and curated table based on defined primary key 

# Adjust the join condition to use the aliases
condition = [col(f"static.{col_name}") == col(f"curated.{col_name}") for col_name in primary_key]
matched_df = df_static_filtered_renamed_alias.join(
    df_curated_filtered_renamed_alias, 
    on=condition, 
    how="inner"
)

# For non-matched DataFrames, use the same aliasing approach
non_matched_curated = df_curated_filtered_renamed_alias.join(
    df_static_filtered_renamed_alias, 
    on=condition, 
    how="left_anti"
)

non_matched_static = df_static_filtered_renamed_alias.join(
    df_curated_filtered_renamed_alias, 
    on=condition, 
    how="left_anti"
)

# Calculate row count for non_matched_curated, non_matched_static, and matched_df
non_matched_curated_count = non_matched_curated.count()
non_matched_static_count = non_matched_static.count()
matched_df_count = matched_df.count()

# Display row count for non_matched_curated, non_matched_static, and matched_df
display({"Row count for non_matched_curated": non_matched_curated_count, 
         "Row count for non_matched_static": non_matched_static_count, 
         "Row count for matched_df": matched_df_count})

# COMMAND ----------

# Get the list of column names from the static and curated dataframes in the exact same order
static_columns = []
curated_columns = []
for col_name in common_fields:
    if f"static_{col_name}" in matched_df.columns:
        static_columns.append(f"static_{col_name}")
    if f"curated_{col_name}" in matched_df.columns:
        curated_columns.append(f"curated_{col_name}")

static_columns.sort()
curated_columns.sort()

# COMMAND ----------

# Compare the values between the static and curated columns
comparison_results = []

for static_col, curated_col in zip(static_columns, curated_columns):
    comparison_result = matched_df.filter(col(static_col) != col(curated_col)).count()
    if comparison_result > 0:
        comparison_results.append((static_col, curated_col, comparison_result))

# Check if comparison_results is not empty
if comparison_results:
    # Create a dataframe from the comparison results
    comparison_df = spark.createDataFrame(comparison_results, ["Static Column", "Curated Column", "Mismatch Count"])
    
    # Sort the dataframe by Mismatch Count in descending order
    comparison_df = comparison_df.orderBy(col("Mismatch Count").desc())
    
    display(comparison_df)
else:
    print("No value mismatches found between static and curated.")


# COMMAND ----------

# Get the row count of matched_df
matched_df_row_count = matched_df.count()

# Filter comparison_df where Mismatch Count is not the same as matched_df_row_count
filtered_comparison_df = comparison_df.filter(comparison_df["Mismatch Count"] != matched_df_row_count)

# Create a list of static and curated column names from filtered_comparison_df
static_columns = [row["Static Column"] for row in filtered_comparison_df.select("Static Column").collect()]
column_names = [row["Static Column"].replace("static_", "") for row in filtered_comparison_df.select("Static Column").collect()]

# Create a list of static and curated column names from filtered_comparison_df
static_columns = [row["Static Column"] for row in filtered_comparison_df.select("Static Column").collect()]
curated_columns = [row["Curated Column"] for row in filtered_comparison_df.select("Curated Column").collect()]

column_names = [row["Static Column"].replace("static_", "") for row in filtered_comparison_df.select("Static Column").collect()]

ordered_curated_columns = []
ordered_static_columns = []

for column_name in column_names: 
    ordered_curated_columns.append(f"curated_{column_name}")
    ordered_static_columns.append(f"static_{column_name}")

static_columns = ordered_static_columns
curated_columns = ordered_curated_columns

# Check if each column name in `column_names` matches the corresponding index in static and curated columns
subset_check_results = []

for index, col_name in enumerate(column_names):
    static_check = col_name in static_columns[index] 
    curated_check = col_name in curated_columns[index] 
    subset_check_results.append((col_name, static_check and curated_check))

# Convert the results to a DataFrame
subset_check = spark.createDataFrame(subset_check_results, ["Column Name", "Is Subset"])
all_subsets = subset_check.agg({"Is Subset": "min"}).collect()[0][0]
all_subsets

print(f"All column names are matched between curated and static: {all_subsets}")

# COMMAND ----------



comparison_results_cleaned = []

# Function to apply cleaning, replacement, and truncation based on column data type
def clean_and_truncate_column(df, col_name):
    df = df.withColumn(col_name, trim(col(col_name)))
    df = df.withColumn(col_name, when(col(col_name) == "", None).otherwise(col(col_name)))
    df = df.withColumn(col_name, when(col(col_name).isNull(), "NULL").otherwise(col(col_name)))
    df = df.withColumn(col_name, regexp_replace(col(col_name), '"', ''))
    df = df.withColumn(col_name, expr(f"replace({col_name}, ' ', '')"))
    if 'datetime' in col_name:  
        df = df.withColumn(col_name, date_trunc("second", col(col_name)))
    return df

# Apply cleaning, replacement, and truncation for static_columns
for col_name in static_columns:
    matched_df = clean_and_truncate_column(matched_df, col_name)

# Apply cleaning, replacement, and truncation for curated_columns
for col_name in curated_columns:
    matched_df = clean_and_truncate_column(matched_df, col_name)

for static_col, curated_col in zip(static_columns, curated_columns):
    comparison_result = matched_df.filter(col(static_col) != col(curated_col)).count()
    if comparison_result > 0:
        comparison_results_cleaned.append((static_col, curated_col, comparison_result))

# Check if comparison_results_cleaned is not empty
if comparison_results_cleaned:
    # Create a dataframe from the comparison results
    comparison_results_cleaned_df = spark.createDataFrame(comparison_results_cleaned, ["Static Column", "Curated Column", "Mismatch Count"])
    
    # Sort the dataframe by Mismatch Count in descending order
    comparison_results_cleaned_df = comparison_results_cleaned_df.orderBy(col("Mismatch Count").desc())
    
    display(comparison_results_cleaned_df)
else:
    print("No mismatches found after cleaning.")

# COMMAND ----------

# Get the row count of matched_df
matched_df_row_count = matched_df.count()

# Filter comparison_results_cleaned_df where Mismatch Count is not the same as matched_df_row_count
filtered_comparison_df = comparison_results_cleaned_df.filter(comparison_results_cleaned_df["Mismatch Count"] != matched_df_row_count)

# Create a list of static and curated column names from filtered_comparison_df
static_columns = [row["Static Column"] for row in filtered_comparison_df.select("Static Column").collect()]
curated_columns = [row["Curated Column"] for row in filtered_comparison_df.select("Curated Column").collect()]

column_names = [row.replace("static_", "") for row in static_columns]

ordered_curated_columns = []
ordered_static_columns = []

for column_name in column_names: 
    ordered_curated_columns.append(f"curated_{column_name}")
    ordered_static_columns.append(f"static_{column_name}")

static_columns = ordered_static_columns
curated_columns = ordered_curated_columns



# COMMAND ----------



# Assuming curated_columns_list is a list of curated column names
matched_df = matched_df.withColumn("curated_concat_key", concat_ws("~", *[col(col_name) for col_name in curated_columns]))



# COMMAND ----------

# Strip whitespace and replace empty strings with null in matched_df
for col_name in static_columns:
    matched_df = matched_df.withColumn(col_name, trim(col(col_name)))
    matched_df = matched_df.withColumn(col_name, when(col(col_name) == "", None).otherwise(col(col_name)))
    matched_df = matched_df.withColumn(col_name, when(col(col_name).isNull(), "NULL").otherwise(col(col_name)))

# Concatenate the values of the static columns in matched_df using a delimiter
matched_df = matched_df.withColumn("static_concat_key", concat_ws("~", *[col(col_name) for col_name in static_columns]))



# COMMAND ----------

# Add a column to matched_df to check if curated_concat_key and static_concat_key match
matched_df = matched_df.withColumn("concat_key_match", (col("curated_concat_key") == col("static_concat_key")).cast("boolean"))

# COMMAND ----------

selected_df = matched_df.select(
    *[col(f"curated.{name}") for name in primary_key], 
    "curated_concat_key", 
    "static_concat_key", 
    "concat_key_match"
)

true_count = selected_df.filter(col("concat_key_match")).count()
false_count = selected_df.filter(~col("concat_key_match")).count()

print(f"True count: {true_count}")
print(f"False count: {false_count}")



# COMMAND ----------

# Filter selected_df where concat_key_match is false
filtered_df = selected_df.filter(col("concat_key_match") == False)



# Display the filtered_df
display(filtered_df)



# COMMAND ----------


