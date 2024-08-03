from abc import ABC, abstractmethod
from pyspark.sql import SparkSession, DataFrame
import time
import logging

# Initialize Spark session
spark = SparkSession.builder \
    .appName("ETL with Proxy Pattern") \
    .getOrCreate()

# Subject Interface
class ETLProcess(ABC):
    
    @abstractmethod
    def run(self):
        pass

# RealSubject: Concrete ETL Process
class RealETLProcess(ETLProcess):
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
    
    def run(self):
        df = spark.read.csv(self.input_path, header=True, inferSchema=True)
        # Example transformation
        df_transformed = df.withColumnRenamed("old_column_name", "new_column_name")
        df_transformed.write.parquet(self.output_path, mode="overwrite")

# Proxy: Controls access to the RealSubject
class ETLProcessProxy(ETLProcess):
    
    def __init__(self, real_etl_process: RealETLProcess):
        self._real_etl_process = real_etl_process
    
    def run(self):
        # Add logging and performance tracking
        logging.info("ETL process started.")
        start_time = time.time()
        
        try:
            self._real_etl_process.run()
        except Exception as e:
            logging.error(f"ETL process failed: {e}")
        finally:
            end_time = time.time()
            logging.info(f"ETL process completed in {end_time - start_time:.2f} seconds.")

# Client Code
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create the real ETL process
    real_etl = RealETLProcess("data/input.csv", "data/output.parquet")
    
    # Create the proxy for the ETL process
    etl_proxy = ETLProcessProxy(real_etl)
    
    # Run the ETL process through the proxy
    etl_proxy.run()

# Stop Spark session
spark.stop()
