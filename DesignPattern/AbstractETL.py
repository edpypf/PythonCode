'''
Here’s an example where we use the Abstract Factory Pattern to build ETL pipelines for different types of data sources 
(e.g., JSON and CSV). We will define abstract factories for creating the different components 
(extractors, transformers, loaders) for each type of data source.

Define the Abstract Factory
Abstract Factory: Defines methods for creating different types of components.
Concrete Factories: Implement the creation methods for specific types of data sources.
Abstract Components: Define interfaces for the components that the factories produce.
Concrete Components: Implement the interfaces with specific functionality.
ETLPipeline: Uses the factory to create and run the ETL process.
Abstract Factory and Components
'''

from pyspark.sql import DataFrame
from abc import ABC, abstractmethod

# Abstract Factory
class ETLFactory(ABC):
    @abstractmethod
    def create_extractor(self):
        pass
    
    @abstractmethod
    def create_transformer(self):
        pass
    
    @abstractmethod
    def create_loader(self):
        pass

# Abstract Components
class Extractor(ABC):
    @abstractmethod
    def extract(self) -> DataFrame:
        pass

class Transformer(ABC):
    @abstractmethod
    def transform(self, df: DataFrame) -> DataFrame:
        pass

class Loader(ABC):
    @abstractmethod
    def load(self, df: DataFrame):
        pass

# Concrete Components for JSON
class JSONExtractor(Extractor):
    def extract(self) -> DataFrame:
        print("Extracting data from JSON...")
        return spark.read.json("/path/to/json")

class JSONTransformer(Transformer):
    def transform(self, df: DataFrame) -> DataFrame:
        print("Transforming JSON data...")
        return df.withColumn("transformed", df["value"] * 2)

class JSONLoader(Loader):
    def load(self, df: DataFrame):
        print("Loading JSON data...")
        df.write.mode("overwrite").parquet("/path/to/output/json")

# Concrete Components for CSV
class CSVExtractor(Extractor):
    def extract(self) -> DataFrame:
        print("Extracting data from CSV...")
        return spark.read.csv("/path/to/csv", header=True, inferSchema=True)

class CSVTransformer(Transformer):
    def transform(self, df: DataFrame) -> DataFrame:
        print("Transforming CSV data...")
        return df.withColumn("transformed", df["value"] * 2)

class CSVLoader(Loader):
    def load(self, df: DataFrame):
        print("Loading CSV data...")
        df.write.mode("overwrite").parquet("/path/to/output/csv")

# Concrete Factories
class JSONFactory(ETLFactory):
    def create_extractor(self):
        return JSONExtractor()
    
    def create_transformer(self):
        return JSONTransformer()
    
    def create_loader(self):
        return JSONLoader()

class CSVFactory(ETLFactory):
    def create_extractor(self):
        return CSVExtractor()
    
    def create_transformer(self):
        return CSVTransformer()
    
    def create_loader(self):
        return CSVLoader()

class ETLPipeline:
    def __init__(self, factory: ETLFactory):
        self.extractor = factory.create_extractor()
        self.transformer = factory.create_transformer()
        self.loader = factory.create_loader()
    
    def run(self):
        df = self.extractor.extract()
        df_transformed = self.transformer.transform(df)
        self.loader.load(df_transformed)

from pyspark.sql import SparkSession

def main():
    global spark
    spark = SparkSession.builder \
        .appName("AbstractFactoryPatternETL") \
        .getOrCreate()

    # Choose the factory based on data source
    data_source = "json"  # or "csv"
    if data_source == "json":
        factory = JSONFactory()
    elif data_source == "csv":
        factory = CSVFactory()
    else:
        raise ValueError("Unknown data source type")
    
    # Create the ETL pipeline using the selected factory
    pipeline = ETLPipeline(factory)
    pipeline.run()

    # Stop Spark session
    spark.stop()

if __name__ == "__main__":
    main()

'''
Explanation
Abstract Factory:

ETLFactory: Defines the interface for creating extractors, transformers, and loaders.
Abstract Components:

Extractor, Transformer, Loader: Define the interfaces for the components that handle data extraction, transformation, and loading, respectively.
Concrete Components:

JSONExtractor, JSONTransformer, JSONLoader: Implement the interfaces for handling JSON data.
CSVExtractor, CSVTransformer, CSVLoader: Implement the interfaces for handling CSV data.
Concrete Factories:

JSONFactory: Creates components for JSON data processing.
CSVFactory: Creates components for CSV data processing.
ETLPipeline:

__init__: Initializes with an ETLFactory and uses it to create components.
run: Executes the ETL process using the created components.
Client Code:

main: Chooses the appropriate factory based on the data source, creates the ETL pipeline, and runs it.
'''
