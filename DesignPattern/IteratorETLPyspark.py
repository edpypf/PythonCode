from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from typing import Iterator, List

# Initialize Spark session
spark = SparkSession.builder \
    .appName("ETL with Iterator Pattern") \
    .getOrCreate()

# Define the Iterator interface
class IteratorInterface(Iterator):
    def __iter__(self):
        return self
    
    def __next__(self):
        raise NotImplementedError

# Concrete Iterator for PySpark DataFrame
class DataFrameIterator(IteratorInterface):
    def __init__(self, df: DataFrame, batch_size: int):
        self.df = df
        self.batch_size = batch_size
        self.num_rows = df.count()
        self.current_index = 0
    
    def __next__(self) -> DataFrame:
        if self.current_index >= self.num_rows:
            raise StopIteration
        
        end_index = min(self.current_index + self.batch_size, self.num_rows)
        batch_df = self.df.limit(end_index).subtract(self.df.limit(self.current_index))
        self.current_index = end_index
        return batch_df

# Transformation function to be applied to each batch
def transform(df: DataFrame) -> DataFrame:
    # Example transformation: Add a new column with some computed value
    from pyspark.sql.functions import col, lit
    return df.withColumn("new_column", lit(1))

# Load function to simulate loading data to a destination
def load(df: DataFrame):
    # Example action: Show the transformed data (you might write it to a file or database)
    df.show()

# Main ETL process
def main():
    # Create sample data
    data = [
        (1, "Alice"),
        (2, "Bob"),
        (3, "Charlie"),
        (4, "David"),
        (5, "Eve"),
        # Add more rows as needed
    ]
    
    # Create DataFrame
    df = spark.createDataFrame(data, ["id", "name"])
    
    # Create an iterator for the DataFrame
    batch_size = 2
    iterator = DataFrameIterator(df, batch_size)
    
    # Process data in batches
    for batch_df in iterator:
        transformed_df = transform(batch_df)
        load(transformed_df)

# Run the ETL process
if __name__ == "__main__":
    main()

# Stop Spark session
spark.stop()
