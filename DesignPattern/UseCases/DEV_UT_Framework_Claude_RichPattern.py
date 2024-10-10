Thank you for providing the detailed plan for creating a PySpark testing framework for ETL processes across different layers. To make this framework flexible, simple, efficient, 
and with less code, we can leverage several Python design patterns. Let's explore how we can structure this framework:

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pyspark.sql import DataFrame, SparkSession

class TestCase(ABC):
    @abstractmethod
    def run(self, df: DataFrame) -> bool:
        pass

class DuplicateCheck(TestCase):
    def __init__(self, key_columns: List[str]):
        self.key_columns = key_columns

    def run(self, df: DataFrame) -> bool:
        distinct_count = df.select(*self.key_columns).distinct().count()
        total_count = df.count()
        return distinct_count == total_count

class CountCheck(TestCase):
    def __init__(self, expected_count: int):
        self.expected_count = expected_count

    def run(self, df: DataFrame) -> bool:
        return df.count() == self.expected_count

class LayerTest:
    def __init__(self, layer_name: str):
        self.layer_name = layer_name
        self.test_cases: List[TestCase] = []

    def add_test(self, test_case: TestCase):
        self.test_cases.append(test_case)

    def run_tests(self, df: DataFrame) -> Dict[str, bool]:
        results = {}
        for test_case in self.test_cases:
            test_name = type(test_case).__name__
            results[test_name] = test_case.run(df)
        return results

class ETLTestingFramework:
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.layers: Dict[str, LayerTest] = {}

    def add_layer(self, layer_name: str):
        self.layers[layer_name] = LayerTest(layer_name)

    def add_test_to_layer(self, layer_name: str, test_case: TestCase):
        if layer_name not in self.layers:
            self.add_layer(layer_name)
        self.layers[layer_name].add_test(test_case)

    def run_tests(self, layer_data: Dict[str, DataFrame]) -> Dict[str, Dict[str, bool]]:
        results = {}
        for layer_name, layer_test in self.layers.items():
            if layer_name in layer_data:
                results[layer_name] = layer_test.run_tests(layer_data[layer_name])
            else:
                print(f"Warning: No data provided for layer {layer_name}")
        return results

# Example usage
spark = SparkSession.builder.appName("ETLTestingFramework").getOrCreate()

framework = ETLTestingFramework(spark)

# Add tests for each layer
for layer in ["raw", "enrich", "fact", "tv", "ev", "bv", "sf"]:
    framework.add_test_to_layer(layer, DuplicateCheck(["id"]))
    framework.add_test_to_layer(layer, CountCheck(1000))  # Example expected count

# Run tests
layer_data = {
    "raw": spark.read.parquet("path/to/raw/data"),
    "enrich": spark.read.parquet("path/to/enrich/data"),
    # ... load other layer data
}

results = framework.run_tests(layer_data)
print(results)

```

This framework uses several Python design patterns to achieve flexibility, simplicity, and efficiency:

1. Abstract Factory Pattern: The `TestCase` abstract base class serves as a factory for creating different types of tests. This allows easy extension of the framework with new test types.

2. Composite Pattern: The `LayerTest` class composes multiple `TestCase` objects, allowing you to treat individual tests and groups of tests uniformly.

3. Strategy Pattern: Each concrete `TestCase` implementation (like `DuplicateCheck` and `CountCheck`) encapsulates a specific testing algorithm. This makes it easy to swap or add new testing strategies.

4. Facade Pattern: The `ETLTestingFramework` class provides a simplified interface to the complex subsystem of layers and tests.

5. Builder Pattern: The methods `add_layer` and `add_test_to_layer` in `ETLTestingFramework` allow for step-by-step construction of the testing suite.

To make this framework even more flexible and cover the specific requirements you mentioned, we can add more test cases:



```python
from pyspark.sql import functions as F

class KeyHashCheck(TestCase):
    def __init__(self, key_columns: List[str], hash_column: str):
        self.key_columns = key_columns
        self.hash_column = hash_column

    def run(self, df1: DataFrame, df2: DataFrame) -> bool:
        df1_stats = df1.groupBy(*self.key_columns).agg(F.collect_set(self.hash_column).alias("hashes"))
        df2_stats = df2.groupBy(*self.key_columns).agg(F.collect_set(self.hash_column).alias("hashes"))
        
        diff = df1_stats.exceptAll(df2_stats)
        return diff.count() == 0

class AggregationCheck(TestCase):
    def __init__(self, group_by_columns: List[str], agg_column: str, agg_function: str):
        self.group_by_columns = group_by_columns
        self.agg_column = agg_column
        self.agg_function = agg_function

    def run(self, df1: DataFrame, df2: DataFrame) -> bool:
        df1_agg = df1.groupBy(*self.group_by_columns).agg({self.agg_column: self.agg_function})
        df2_agg = df2.groupBy(*self.group_by_columns).agg({self.agg_column: self.agg_function})
        
        diff = df1_agg.exceptAll(df2_agg)
        return diff.count() == 0

class ContentMatchCheck(TestCase):
    def run(self, df1: DataFrame, df2: DataFrame) -> bool:
        diff = df1.exceptAll(df2)
        if diff.count() > 0:
            print("Differences found:")
            diff.show()
            return False
        return True

class DeletedRecordsCheck(TestCase):
    def __init__(self, key_columns: List[str]):
        self.key_columns = key_columns

    def run(self, old_df: DataFrame, new_df: DataFrame) -> bool:
        deleted = old_df.select(*self.key_columns).exceptAll(new_df.select(*self.key_columns))
        if deleted.count() > 0:
            print("Deleted records:")
            deleted.show()
            return False
        return True

class ChangedRecordsCheck(TestCase):
    def __init__(self, key_columns: List[str], compare_columns: List[str]):
        self.key_columns = key_columns
        self.compare_columns = compare_columns

    def run(self, old_df: DataFrame, new_df: DataFrame) -> bool:
        joined = old_df.join(new_df, self.key_columns, "inner")
        changed = joined.filter(" OR ".join([f"old.{col} != new.{col}" for col in self.compare_columns]))
        if changed.count() > 0:
            print("Changed records:")
            changed.show()
            return False
        return True

# Extend the ETLTestingFramework to handle layer comparisons
class ETLTestingFramework:
    # ... (previous code remains the same)

    def run_layer_comparison(self, layer1: str, layer2: str, df1: DataFrame, df2: DataFrame, tests: List[TestCase]) -> Dict[str, bool]:
        results = {}
        for test in tests:
            test_name = type(test).__name__
            results[test_name] = test.run(df1, df2)
        return results

# Example usage for layer comparisons
framework = ETLTestingFramework(spark)

# Add layer comparison tests
raw_enrich_tests = [
    KeyHashCheck(["id"], "hash_diff"),
    ContentMatchCheck()
]

enrich_fact_tests = [
    AggregationCheck(["category"], "amount", "sum"),
    DeletedRecordsCheck(["id"]),
    ChangedRecordsCheck(["id"], ["amount", "category"])
]

# Run layer comparison tests
raw_data = spark.read.parquet("path/to/raw/data")
enrich_data = spark.read.parquet("path/to/enrich/data")
fact_data = spark.read.parquet("path/to/fact/data")

raw_enrich_results = framework.run_layer_comparison("raw", "enrich", raw_data, enrich_data, raw_enrich_tests)
enrich_fact_results = framework.run_layer_comparison("enrich", "fact", enrich_data, fact_data, enrich_fact_tests)

print("Raw to Enrich comparison results:", raw_enrich_results)
print("Enrich to Fact comparison results:", enrich_fact_results)

```

This extended framework now covers all the specific requirements you mentioned, including:

1. Individual checks for duplicates and counts across all layers.
2. Key and hash comparisons between raw and enrich layers.
3. Aggregation checks between layers.
4. Content matching, including showing differences when found.
5. Checks for deleted and changed records.

The framework remains flexible and can be easily extended to cover dimension and bridge tables as well. You can create specific test cases for these table types by subclassing the `TestCase` class and implementing the `run` method.

To make the framework even more efficient and reduce code duplication, you could consider the following enhancements:

1. Implement a caching mechanism for DataFrames to avoid recomputing the same data multiple times.
2. Use broadcast joins for small DataFrames when comparing layers.
3. Implement parallel execution of tests using PySpark's built-in parallelism.

To apply this framework to dimension and bridge tables, you can simply create new test cases specific to these table types and add them to the framework in the same way as the fact table tests.

This design allows for easy extension, reusability, and maintainability of your ETL testing framework. You can add new test cases or modify existing ones without changing the core structure of the framework.

Certainly! I'll extend the framework to include examples for dimension and bridge tables. This will demonstrate how the framework can be applied across different table types in a data warehouse environment.



```python
from pyspark.sql import functions as F

# ... (previous code remains the same)

# New test cases specific to dimension tables
class SlowlyChangingDimensionCheck(TestCase):
    def __init__(self, key_columns: List[str], tracked_columns: List[str]):
        self.key_columns = key_columns
        self.tracked_columns = tracked_columns

    def run(self, old_df: DataFrame, new_df: DataFrame) -> bool:
        joined = old_df.join(new_df, self.key_columns, "full_outer")
        
        # Check for new records
        new_records = joined.filter(f"old.{self.key_columns[0]} IS NULL")
        
        # Check for updated records
        updated_records = joined.filter(" OR ".join([f"old.{col} != new.{col}" for col in self.tracked_columns]))
        
        if new_records.count() > 0 or updated_records.count() > 0:
            print("New records:")
            new_records.show()
            print("Updated records:")
            updated_records.show()
            return False
        return True

# New test case specific to bridge tables
class BridgeTableIntegrityCheck(TestCase):
    def __init__(self, left_key: str, right_key: str):
        self.left_key = left_key
        self.right_key = right_key

    def run(self, bridge_df: DataFrame, left_df: DataFrame, right_df: DataFrame) -> bool:
        # Check if all keys in bridge table exist in respective dimension tables
        left_integrity = bridge_df.join(left_df, self.left_key, "left_anti").count() == 0
        right_integrity = bridge_df.join(right_df, self.right_key, "left_anti").count() == 0
        
        if not (left_integrity and right_integrity):
            print("Bridge table integrity check failed")
            return False
        return True

# Extend the ETLTestingFramework to handle different table types
class ETLTestingFramework:
    # ... (previous code remains the same)

    def run_dimension_tests(self, old_dim: DataFrame, new_dim: DataFrame, tests: List[TestCase]) -> Dict[str, bool]:
        results = {}
        for test in tests:
            test_name = type(test).__name__
            results[test_name] = test.run(old_dim, new_dim)
        return results

    def run_bridge_tests(self, bridge_df: DataFrame, left_df: DataFrame, right_df: DataFrame, tests: List[TestCase]) -> Dict[str, bool]:
        results = {}
        for test in tests:
            test_name = type(test).__name__
            results[test_name] = test.run(bridge_df, left_df, right_df)
        return results

# Example usage including fact, dimension, and bridge tables
spark = SparkSession.builder.appName("ETLTestingFramework").getOrCreate()

framework = ETLTestingFramework(spark)

# Fact table tests (as before)
fact_tests = [
    DuplicateCheck(["id"]),
    CountCheck(1000),
    AggregationCheck(["category"], "amount", "sum")
]

# Dimension table tests
dim_tests = [
    DuplicateCheck(["dim_id"]),
    CountCheck(500),
    SlowlyChangingDimensionCheck(["dim_id"], ["attribute1", "attribute2"])
]

# Bridge table tests
bridge_tests = [
    DuplicateCheck(["left_id", "right_id"]),
    CountCheck(1500),
    BridgeTableIntegrityCheck("left_id", "right_id")
]

# Load data
fact_data = spark.read.parquet("path/to/fact/data")
old_dim_data = spark.read.parquet("path/to/old_dim/data")
new_dim_data = spark.read.parquet("path/to/new_dim/data")
bridge_data = spark.read.parquet("path/to/bridge/data")
left_dim_data = spark.read.parquet("path/to/left_dim/data")
right_dim_data = spark.read.parquet("path/to/right_dim/data")

# Run tests
fact_results = framework.run_tests({"fact": fact_data})
dim_results = framework.run_dimension_tests(old_dim_data, new_dim_data, dim_tests)
bridge_results = framework.run_bridge_tests(bridge_data, left_dim_data, right_dim_data, bridge_tests)

print("Fact table test results:", fact_results)
print("Dimension table test results:", dim_results)
print("Bridge table test results:", bridge_results)

# Layer comparison tests (as before)
raw_enrich_tests = [
    KeyHashCheck(["id"], "hash_diff"),
    ContentMatchCheck()
]

enrich_fact_tests = [
    AggregationCheck(["category"], "amount", "sum"),
    DeletedRecordsCheck(["id"]),
    ChangedRecordsCheck(["id"], ["amount", "category"])
]

# Run layer comparison tests
raw_data = spark.read.parquet("path/to/raw/data")
enrich_data = spark.read.parquet("path/to/enrich/data")

raw_enrich_results = framework.run_layer_comparison("raw", "enrich", raw_data, enrich_data, raw_enrich_tests)
enrich_fact_results = framework.run_layer_comparison("enrich", "fact", enrich_data, fact_data, enrich_fact_tests)

print("Raw to Enrich comparison results:", raw_enrich_results)
print("Enrich to Fact comparison results:", enrich_fact_results)

```

This extended framework now includes examples for testing dimension and bridge tables, in addition to the fact tables and layer comparisons we had before. Here's a breakdown of the new additions:

1. Dimension Tables:
   - We've added a `SlowlyChangingDimensionCheck` to detect new and updated records in dimension tables.
   - The `run_dimension_tests` method in the `ETLTestingFramework` class allows for comparing old and new versions of a dimension table.

2. Bridge Tables:
   - We've introduced a `BridgeTableIntegrityCheck` to ensure that all keys in the bridge table exist in their respective dimension tables.
   - The `run_bridge_tests` method in the `ETLTestingFramework` class allows for testing bridge tables along with their related dimension tables.

3. Example Usage:
   - The example now includes loading and testing fact, dimension, and bridge tables.
   - It demonstrates how to use the framework for different table types and layer comparisons.

This framework maintains the flexibility, simplicity, and efficiency we aimed for earlier, while extending its capabilities to cover all table types in a typical data warehouse. The use of design patterns like Strategy (for different test cases) and Composite (for grouping tests) allows for easy extension and modification of the framework.

To further improve this framework, consider:

1. Implementing parallel execution of tests using PySpark's capabilities.
2. Adding more specific test cases for dimension and bridge tables based on your specific business rules.
3. Implementing a reporting mechanism to generate detailed test reports.
4. Adding configuration options to customize test behavior without changing the code.

This framework provides a solid foundation for comprehensive ETL testing across different table types and data layers. You can easily extend it with more specific test cases as needed for your particular data warehouse architecture and business requirements.
