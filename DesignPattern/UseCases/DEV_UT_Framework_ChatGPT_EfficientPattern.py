To make the framework more efficient, cleaner, and simpler while leveraging the most appropriate design patterns, we can streamline certain aspects:
Improvements:
1.	Simplified Strategy Usage: Instead of creating separate executor classes for each check, we can integrate the strategy pattern directly within the test case classes.
2.	Refactor Factory Pattern: The factory can be refactored to reduce redundant conditionals for different table types.
3.	Avoid Redundancy in Chain of Responsibility: Rather than creating multiple Check classes, we can directly use the strategy pattern for checks, as the checks are not truly dependent on one another.
4.	Unified Test Case Classes: Since fact, dimension, and bridge tables all share similar logic for checks, we can use a base test case class for all table types and extend only when necessary.

from abc import ABC, abstractmethod

# ---------- Logging Decorator for Simplicity ---------- #
def logging_decorator(test_func):
    def wrapper(*args, **kwargs):
        print(f"Running test: {test_func.__name__}")
        result = test_func(*args, **kwargs)
        print(f"Test result: {result}")
        return result
    return wrapper

# ---------- Strategy Pattern for Reusable Checks ---------- #
class DupCheckStrategy:
    def execute(self, df):
        return df.dropDuplicates()

class CountCheckStrategy:
    def execute(self, df1, df2):
        return df1.count() == df2.count()

class KeyCheckStrategy:
    def execute(self, df1, df2, key_column):
        return df1.select(key_column).distinct().count() == df2.select(key_column).distinct().count()

class ContentCheckStrategy:
    def execute(self, df1, df2):
        return df1.exceptAll(df2).count() == 0 and df2.exceptAll(df1).count() == 0

# ---------- Unified Test Case Class for All Tables ---------- #
class BaseETLTest(ABC):
    def __init__(self, table_type, layer, key_column):
        self.table_type = table_type
        self.layer = layer
        self.key_column = key_column

    def run_test(self, df1, df2):
        self.duplicate_check(df1)
        self.key_check(df1, df2)
        self.content_check(df1, df2)

    @logging_decorator
    def duplicate_check(self, df):
        dup_check = DupCheckStrategy().execute(df)
        print(f"Duplication Check Passed: {dup_check.count() == df.count()}")

    @logging_decorator
    def key_check(self, df1, df2):
        result = KeyCheckStrategy().execute(df1, df2, self.key_column)
        print(f"Key Check Passed: {result}")

    @logging_decorator
    def content_check(self, df1, df2):
        result = ContentCheckStrategy().execute(df1, df2)
        print(f"Content Check Passed: {result}")

# ---------- Factory Pattern for Test Creation ---------- #
class TestCaseFactory:
    @staticmethod
    def create_test_case(table_type, layer):
        key_column_map = {
            "fact": "fact_key",
            "dimension": "dimension_key",
            "bridge": "bridge_key"
        }
        key_column = key_column_map.get(table_type, "key_column")
        return BaseETLTest(table_type, layer, key_column)

# ---------- Simplified Test Execution Strategy ---------- #
from pyspark.sql import SparkSession
from pyspark.sql import Row

spark = SparkSession.builder.master("local").appName("ETL Testing").getOrCreate()

# Sample DataFrames for testing
raw_df = spark.createDataFrame([Row(fact_key=1, value=100), Row(fact_key=2, value=200)])
enrich_df = spark.createDataFrame([Row(fact_key=1, value=100), Row(fact_key=2, value=200)])

# Example 1: Unified Test for Fact Table from Raw to Enrich
fact_test = TestCaseFactory.create_test_case("fact", "raw_enrich")
fact_test.run_test(raw_df, enrich_df)

# Example 2: Unified Test for Dimension Table from Raw to Enrich
dimension_test = TestCaseFactory.create_test_case("dimension", "raw_enrich")
dimension_test.run_test(raw_df, enrich_df)

# Example 3: Unified Test for Bridge Table from Raw to Enrich
bridge_test = TestCaseFactory.create_test_case("bridge", "raw_enrich")
bridge_test.run_test(raw_df, enrich_df)

1.	Unified Test Case Class (BaseETLTest): This class now handles all layers and table types with a single implementation for checks (duplication, key, content), with specific adjustments based on the key column for different table types.
2.	Factory Pattern: The factory now assigns the correct key column based on the table type (fact, dimension, bridge) and returns a single BaseETLTest instance, greatly simplifying the code.
3.	Single Responsibility for Checks: Each check is a simple method in the BaseETLTest, which directly uses the strategy pattern for logic without needing multiple executor classes.
4.	Logging Decorator: Applied consistently to the key methods (duplicate_check, key_check, and content_check) to ensure we log every step with minimal code.
Benefits:
•	Simpler Code: The framework has fewer classes, no need for extra executor or check classes, and everything is handled in a single BaseETLTest.
•	Efficiency: By directly using strategies and simplifying the factory logic, we've reduced complexity and improved maintainability.
•	Flexibility: The table type and layer-specific logic are abstracted in the factory, allowing easy expansion without adding extra classes or methods.
This refactored design keeps the code flexible, reusable, and easy to understand, while still providing all the checks you need for ETL testing across fact, dimension, and bridge tables.
