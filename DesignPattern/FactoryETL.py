'''
Define the Components
Transformation Interface: Defines a common interface for all transformations.
Concrete Transformations: Implements different types of transformations.
TransformationFactory: Factory class to create instances of transformations based on input parameters.
ETLPipeline: Uses the factory to apply transformations.
Transformation Classes
'''
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

class Transformation:
    def apply(self, df: DataFrame) -> DataFrame:
        raise NotImplementedError("Subclass must implement this method")

class RenameColumnsTransformation(Transformation):
    def __init__(self, renaming_map):
        self.renaming_map = renaming_map
    
    def apply(self, df: DataFrame) -> DataFrame:
        for old_name, new_name in self.renaming_map.items():
            df = df.withColumnRenamed(old_name, new_name)
        return df

class NormalizeColumnsTransformation(Transformation):
    def __init__(self, columns):
        self.columns = columns
    
    def apply(self, df: DataFrame) -> DataFrame:
        for column in self.columns:
            df = df.withColumn(column, col(column) / 100)  # Example normalization
        return df

class TransformationFactory:
    @staticmethod
    def create_transformation(transformation_type, *args):
        if transformation_type == "rename":
            return RenameColumnsTransformation(*args)
        elif transformation_type == "normalize":
            return NormalizeColumnsTransformation(*args)
        else:
            raise ValueError(f"Unknown transformation type: {transformation_type}")

class ETLPipeline:
    def __init__(self, extractor, transformer_factory, transformations, loader):
        self.extractor = extractor
        self.transformer_factory = transformer_factory
        self.transformations = transformations
        self.loader = loader
    
    def run(self):
        df = self.extractor.extract()
        for transformation_type, *params in self.transformations:
            transformer = self.transformer_factory.create_transformation(transformation_type, *params)
            df = transformer.apply(df)
        self.loader.load(df)

from pyspark.sql import SparkSession

class DataExtractor:
    def extract(self) -> DataFrame:
        print("Extracting data...")
        return spark.createDataFrame([("Alice", 34, 2500), ("Bob", 45, 3000)], ["name", "age", "salary"])

class DataLoader:
    def __init__(self, output_path):
        self.output_path = output_path
    
    def load(self, df: DataFrame):
        print(f"Loading data to {self.output_path}...")
        df.write.csv(self.output_path)

def main():
    global spark
    spark = SparkSession.builder \
        .appName("FactoryPatternETL") \
        .getOrCreate()
    
    # Define the transformations using the factory
    transformations = [
        ("rename", {"salary": "income"}),
        ("normalize", ["age", "income"])
    ]
    
    # Create the ETL pipeline
    extractor = DataExtractor()
    loader = DataLoader("/path/to/output")
    pipeline = ETLPipeline(extractor, TransformationFactory, transformations, loader)
    
    # Run the ETL pipeline
    pipeline.run()

    # Stop Spark session
    spark.stop()

if __name__ == "__main__":
    main()
