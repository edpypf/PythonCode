from abc import ABC, abstractmethod
from pyspark.sql import SparkSession, DataFrame
import time
import logging
from functools import wraps

# Initialize Spark session
spark = SparkSession.builder \
    .appName("ETL with Decorator Pattern") \
    .getOrCreate()

# Component Interface
class ETLProcess(ABC):
    
    @abstractmethod
    def run(self):
        pass

# Concrete Component
class BasicETLProcess(ETLProcess):
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
    
    def run(self):
        df = spark.read.csv(self.input_path, header=True, inferSchema=True)
        # Example transformation
        df_transformed = df.withColumnRenamed("old_column_name", "new_column_name")
        df_transformed.write.parquet(self.output_path, mode="overwrite")

# Decorator Functions
def logging_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("ETL process started.")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"ETL process completed in {end_time - start_time:.2f} seconds.")
        return result
    return wrapper

def performance_tracking_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("Performance tracking started.")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Performance tracking completed in {end_time - start_time:.2f} seconds.")
        return result
    return wrapper

def data_validation_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        etl_process = args[0]
        logging.info("Data validation started.")
        
        # Read the DataFrame to validate
        df = spark.read.csv(etl_process.input_path, header=True, inferSchema=True)
        
        def validate(df: DataFrame) -> bool:
            # Example validation: Check for null values in a specific column
            return df.filter(df["some_column"].isNull()).count() == 0
        
        if not validate(df):
            raise ValueError("Data validation failed: Null values found.")
        
        logging.info("Data validation passed.")
        return func(*args, **kwargs)
    
    return wrapper

# Applying decorators
@logging_decorator
@performance_tracking_decorator
@data_validation_decorator
def run_etl_process(etl_process: ETLProcess):
    etl_process.run()

# Client Code
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create a basic ETL process
    basic_etl = BasicETLProcess("data/input.csv", "data/output.parquet")
    
    # Run the decorated ETL process
    run_etl_process(basic_etl)

# Stop Spark session
spark.stop()
