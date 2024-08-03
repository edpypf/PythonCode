'''
Scenario 1: Large Number of Objects with Shared State
Imagine you need to handle a large number of data transformations where many of them share similar configurations. For instance, you have a dataset with numerous columns, and you need to apply various transformations like renaming columns, converting types, or handling missing values.

Problem with Reusable Functions
With reusable functions, each transformation might require a new function or significant parameterization, and memory efficiency is not managed. For example, if you have different column renaming transformations, you'd end up creating a new transformation object or function for each unique renaming operation.

Example with Reusable Functions:
'''
from pyspark.sql import DataFrame

def rename_column(df: DataFrame, old_name: str, new_name: str) -> DataFrame:
    return df.withColumnRenamed(old_name, new_name)

# Assuming a DataFrame with many columns
df = spark.createDataFrame([(1, "Alice", 30), (2, "Bob", 25)], ["id", "name", "age"])

# Create multiple renaming transformations
df_renamed1 = rename_column(df, "name", "full_name")
df_renamed2 = rename_column(df_renamed1, "age", "years_old")
# ... many more similar operations

'''
Memory Inefficiency: Each function call creates a new DataFrame, potentially leading to a lot of temporary objects.
Lack of Shared State: No mechanism to reuse or share transformation logic efficiently.
Flyweight Pattern Solution:

With the Flyweight Pattern, you can share transformation logic, reducing memory usage and reusing objects.

Example with Flyweight Pattern:
'''

from abc import ABC, abstractmethod
from pyspark.sql import DataFrame
from typing import Dict

class Transformation(ABC):
    @abstractmethod
    def apply(self, df: DataFrame) -> DataFrame:
        pass

class ColumnRenamingTransformation(Transformation):
    def __init__(self, old_name: str, new_name: str):
        self.old_name = old_name
        self.new_name = new_name
    
    def apply(self, df: DataFrame) -> DataFrame:
        return df.withColumnRenamed(self.old_name, self.new_name)

class TransformationFactory:
    _transformations: Dict[str, Transformation] = {}
    
    @staticmethod
    def get_transformation(old_name: str, new_name: str) -> Transformation:
        key = f"{old_name}_{new_name}"
        if key not in TransformationFactory._transformations:
            TransformationFactory._transformations[key] = ColumnRenamingTransformation(old_name, new_name)
        return TransformationFactory._transformations[key]

# Usage
df = spark.createDataFrame([(1, "Alice", 30), (2, "Bob", 25)], ["id", "name", "age"])

# Get shared transformation instances
rename_transformation1 = TransformationFactory.get_transformation("name", "full_name")
rename_transformation2 = TransformationFactory.get_transformation("age", "years_old")

df_transformed = rename_transformation2.apply(rename_transformation1.apply(df))
df_transformed.show()

'''
Memory Efficiency: The factory ensures only one instance of each unique transformation configuration is created.
Shared State: Transforms are managed centrally, avoiding duplication of logic.
'''

'''
Scenario 2: Extending Functionality with Minimal Code Changes
Suppose you need to add new types of transformations or additional behaviors to your existing transformations without altering the existing code significantly.

Problem with Reusable Functions
Adding new transformation types would require modifying or adding new functions, which could involve significant changes to the existing codebase. For example, adding a new type of transformation like data normalization would require creating a new function and potentially modifying all parts of the code that handle transformations.

Example with Reusable Functions:
'''
def rename_column(df: DataFrame, old_name: str, new_name: str) -> DataFrame:
    return df.withColumnRenamed(old_name, new_name)

def normalize_column(df: DataFrame, column_name: str) -> DataFrame:
    max_val = df.agg({column_name: "max"}).collect()[0][0]
    min_val = df.agg({column_name: "min"}).collect()[0][0]
    return df.withColumn(column_name, (col(column_name) - min_val) / (max_val - min_val))

# Applying transformations
df = spark.createDataFrame([(1, "Alice", 30), (2, "Bob", 25)], ["id", "name", "age"])

df_renamed = rename_column(df, "name", "full_name")
df_normalized = normalize_column(df_renamed, "age")
df_normalized.show()

'''
Code Changes: Adding new transformations requires creating new functions and potentially altering existing code.
Flyweight Pattern Solution:

With the Flyweight Pattern, you can extend functionality by adding new transformation classes and updating the factory to handle them. The core logic remains unchanged, and new transformations can be added with minimal modifications.

Example with Flyweight Pattern:
'''
class NormalizationTransformation(Transformation):
    def __init__(self, column_name: str):
        self.column_name = column_name
    
    def apply(self, df: DataFrame) -> DataFrame:
        max_val = df.agg({self.column_name: "max"}).collect()[0][0]
        min_val = df.agg({self.column_name: "min"}).collect()[0][0]
        return df.withColumn(self.column_name, (col(self.column_name) - min_val) / (max_val - min_val))

class TransformationFactory:
    _transformations: Dict[str, Transformation] = {}
    
    @staticmethod
    def get_transformation(trans_type: str, *args) -> Transformation:
        key = f"{trans_type}_{'_'.join(args)}"
        if key not in TransformationFactory._transformations:
            if trans_type == "rename":
                TransformationFactory._transformations[key] = ColumnRenamingTransformation(*args)
            elif trans_type == "normalize":
                TransformationFactory._transformations[key] = NormalizationTransformation(*args)
            else:
                raise ValueError(f"Transformation type '{trans_type}' not recognized.")
        return TransformationFactory._transformations[key]

# Usage
df = spark.createDataFrame([(1, "Alice", 30), (2, "Bob", 25)], ["id", "name", "age"])

# Get transformations from factory
rename_transformation = TransformationFactory.get_transformation("rename", "name", "full_name")
normalize_transformation = TransformationFactory.get_transformation("normalize", "age")

df_transformed = normalize_transformation.apply(rename_transformation.apply(df))
df_transformed.show()

'''
Extensibility: New transformation types can be added by creating new classes and updating the factory with minimal changes to existing code.
Centralized Control: The factory handles all transformations, making it easy to manage and extend.
Summary
Flyweight Pattern helps with memory efficiency by reusing shared objects, whereas reusable functions create new instances each time.
Flyweight Pattern facilitates extensibility by allowing new types of transformations to be added with minimal changes, compared to 
reusable functions that require modifying or adding new functions.
In scenarios with many similar objects or the need for efficient management and extensibility, the Flyweight Pattern provides a robust 
and scalable solution. both approaches—using reusable functions and employing the Flyweight Pattern—require adding new code when introducing 
new functionality. However, the Flyweight Pattern offers distinct advantages in terms of memory efficiency, extensibility, and management, 
which can be particularly beneficial in more complex scenarios. 
'''
