from abc import ABC, abstractmethod
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col

# Initialize Spark session
spark = SparkSession.builder \
    .appName("ETL with Composite Pattern") \
    .getOrCreate()

# Component Interface
class Transformation(ABC):
    
    @abstractmethod
    def apply(self, df: DataFrame) -> DataFrame:
        pass

# Leaf: Single transformation step
class AddColumn(Transformation):
    
    def __init__(self, column_name: str, value):
        self.column_name = column_name
        self.value = value
    
    def apply(self, df: DataFrame) -> DataFrame:
        return df.withColumn(self.column_name, lit(self.value))

# Leaf: Single transformation step
class RenameColumn(Transformation):
    
    def __init__(self, old_name: str, new_name: str):
        self.old_name = old_name
        self.new_name = new_name
    
    def apply(self, df: DataFrame) -> DataFrame:
        return df.withColumnRenamed(self.old_name, self.new_name)

# Composite: Combination of multiple transformations
class CompositeTransformation(Transformation):
    
    def __init__(self):
        self.transformations = []
    
    def add(self, transformation: Transformation):
        self.transformations.append(transformation)
    
    def apply(self, df: DataFrame) -> DataFrame:
        for transformation in self.transformations:
            df = transformation.apply(df)
        return df

# Client Code
if __name__ == "__main__":
    # Sample data
    data = [
        (1, "Alice"),
        (2, "Bob"),
        (3, "Charlie")
    ]
    
    # Create DataFrame
    df = spark.createDataFrame(data, ["id", "name"])
    
    # Create individual transformations
    add_column = AddColumn("age", 30)
    rename_column = RenameColumn("name", "full_name")
    
    # Create a composite transformation
    composite_transformation = CompositeTransformation()
    composite_transformation.add(add_column)
    composite_transformation.add(rename_column)
    
    # Apply transformations
    transformed_df = composite_transformation.apply(df)
    transformed_df.show()

# Stop Spark session
spark.stop()
