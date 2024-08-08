### An pyspark ETL example using all 26 patterns in python ###
'''
Creating a comprehensive ETL (Extract, Transform, Load) process using PySpark involves 
leveraging various patterns to handle different aspects of data processing. Here, we'll 
outline a simplified example that touches on the 26 design patterns often used in software 
engineering. Given the complexity, the full implementation of each pattern in a real-world 
scenario would be extensive. Instead, this example provides a high-level overview and code 
snippets for each pattern.

<<<<<<<<<<<<<<<<<<<< 1. Factory Method Pattern >>>>>>>>>>>>>>>>>>>>>>>>
encapsulates the logic of instantiating the appropriate class based on certain parameters 
or conditions. It is called a "factory method" because it acts like a factory, producing 
objects based on the given criteria.
***************** Summary **********************
base class - multi actual different format of sources class & read method -
factory class & method to call sources based on condition - provide parameter and run
''' 
from abc import ABC, abstractmethod
#------------------------> abstract base class and abstractmethod --------------------->
from abc import ABC, abstractmethod
from pyspark.sql import DataFrame

class DataExtractor(ABC):
    @abstractmethod
    def extract_data(self, spark) -> DataFrame:
        pass
#------------------------> actual concrete class and method --------------------->
class CSVDataExtractor(DataExtractor):
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_data(self, spark):
        return spark.read.csv(self.file_path, header=True, inferSchema=True)

class JSONDataExtractor(DataExtractor):
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_data(self, spark):
        return spark.read.json(self.file_path, inferSchema=True)

class ParquetDataExtractor(DataExtractor):
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_data(self, spark):
        return spark.read.parquet(self.file_path)
#------------------------> Factory method, instantiate the object based on conditions --------------------->
class DataExtractorFactory:
    @staticmethod
    def get_data_extractor(source_type, file_path):
        if source_type == 'csv':
            return CSVDataExtractor(file_path)
        elif source_type == 'json':
            return JSONDataExtractor(file_path)
        elif source_type == 'parquet':
            return ParquetDataExtractor(file_path)
        else:
            raise ValueError(f"Unknown data source type: {source_type}")
#------------------------> main to use it --------------------->
from pyspark.sql import SparkSession
def main():
    spark = SparkSession.builder \
        .appName("ETL Example") \
        .getOrCreate()

    source_type = 'csv'  # This could come from a configuration file or user input
    file_path = 'data/sample.csv'

    data_extractor = DataExtractorFactory.get_data_extractor(source_type, file_path)
    data = data_extractor.extract_data(spark)
    data.show()

if __name__ == "__main__":
    main()

'''
<<<<<<<<<<<<<<<<<<<<< 2. Singleton Pattern >>>>>>>>>>>>>>>>>>>>>>>>
Ensure a class has only one instance and provide a global point of access to it.
depends on the specific requirements and constraints of your application, choose the right type:
Eager Initialization: Best when resource use is not a concern and simplicity is desired.
Lazy Initialization: Useful when resources are expensive, and you want to ensure they are only used when necessary.
Thread-Safe Singleton: Necessary in multi-threaded environments but comes with a performance cost.
Bill Pugh Singleton: Provides a balance of thread safety and lazy initialization without synchronization overhead.
Metaclasses: Best for Python-specific use cases where elegance and control over class creation are important.
Decorator: Simple and flexible but requires careful handling in multi-threaded environments.
<< 1. Eager Initialization >>
'''
from pyspark.sql import SparkSession

class SingletonEagerDBConnection:
    _instance = None

    @staticmethod
    def get_instance():
        if SingletonEagerDBConnection._instance is None:
            SingletonEagerDBConnection._instance = SingletonEagerDBConnection()
        return SingletonEagerDBConnection._instance

    def __init__(self):
        if SingletonEagerDBConnection._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.spark = SparkSession.builder.appName("Eager Initialization Singleton").getOrCreate()

# Usage
db_conn = SingletonEagerDBConnection.get_instance()
print(db_conn.spark)

<< 2. Lazy Initialization >> 
from pyspark.sql import SparkSession

class SingletonLazyDBConnection:
    _instance = None

    @staticmethod
    def get_instance():
        if SingletonLazyDBConnection._instance is None:
            SingletonLazyDBConnection._instance = SingletonLazyDBConnection()
        return SingletonLazyDBConnection._instance

    def __init__(self):
        if SingletonLazyDBConnection._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.spark = SparkSession.builder.appName("Lazy Initialization Singleton").getOrCreate()

# Usage
db_conn = SingletonLazyDBConnection.get_instance()
print(db_conn.spark)

<< 3. Thread-Safe Singleton >>
import threading
from pyspark.sql import SparkSession

class SingletonThreadSafeDBConnection:
    _instance = None
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if SingletonThreadSafeDBConnection._instance is None:
            with SingletonThreadSafeDBConnection._lock:
                if SingletonThreadSafeDBConnection._instance is None:
                    SingletonThreadSafeDBConnection._instance = SingletonThreadSafeDBConnection()
        return SingletonThreadSafeDBConnection._instance

    def __init__(self):
        if SingletonThreadSafeDBConnection._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.spark = SparkSession.builder.appName("Thread-Safe Singleton").getOrCreate()

# Usage
db_conn = SingletonThreadSafeDBConnection.get_instance()
print(db_conn.spark)

<< 4. Bill Pugh Singleton >>
from pyspark.sql import SparkSession

class SingletonBillPughDBConnection:
    class _SingletonHelper:
        _instance = SingletonBillPughDBConnection()

    @staticmethod
    def get_instance():
        return SingletonBillPughDBConnection._SingletonHelper._instance

    def __init__(self):
        if SingletonBillPughDBConnection._SingletonHelper._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.spark = SparkSession.builder.appName("Bill Pugh Singleton").getOrCreate()

# Usage
db_conn = SingletonBillPughDBConnection.get_instance()
print(db_conn.spark)

<< 5. Using Metaclasses >>
from pyspark.sql import SparkSession

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class SingletonWithMetaDBConnection(metaclass=SingletonMeta):
    def __init__(self):
        self.spark = SparkSession.builder.appName("Metaclass Singleton").getOrCreate()

# Usage
db_conn = SingletonWithMetaDBConnection()
print(db_conn.spark)

# << 6. Decorator way of singleton >> 
from pyspark.sql import SparkSession

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class SingletonWithDecoratorDBConnection:
    def __init__(self):
        self.spark = SparkSession.builder.appName("Decorator Singleton").getOrCreate()

# Usage
db_conn = SingletonWithDecoratorDBConnection()
print(db_conn.spark)

<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 3. Adapter Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
''' Allow incompatible interfaces to work together.
***************** Summary **********************
Adapter Pattern: Use when you need to integrate with legacy systems or third-party libraries with incompatible interfaces. 
It focuses on making interfaces compatible and promoting reuse.
Factory Pattern: Use when you need to manage the complexity of object creation, promoting loose coupling and encapsulating 
the instantiation logic.
''' 
# << 1 - 3rd party Logger Adapter >>
# Existing logger interface
class Logger:
    def log(self, message: str):
        pass

# Third-party logger with a different interface
class ThirdPartyLogger:
    def write_log(self, msg: str):
        print(msg)

# Adapter to make ThirdPartyLogger compatible with Logger interface
class LoggerAdapter(Logger):
    def __init__(self, third_party_logger: ThirdPartyLogger):
        self.third_party_logger = third_party_logger

    def log(self, message: str):
        self.third_party_logger.write_log(message)

# Usage
third_party_logger = ThirdPartyLogger()
logger = LoggerAdapter(third_party_logger)
logger.log("This is a log message.")

# << 2 - New Payment Gateway >>
class PaymentProcessor:
    def process_payment(self, amount: float):
        pass
class NewPaymentGateway:
    def make_payment(self, money: float):
        print(f"Processing payment of ${money} through NewPaymentGateway")
class NewPaymentGatewayAdapter(PaymentProcessor):
    def __init__(self, new_gateway: NewPaymentGateway):
        self.new_gateway = new_gateway

    def process_payment(self, amount: float):
        self.new_gateway.make_payment(amount)
# Existing system usage
def make_payment(payment_processor: PaymentProcessor, amount: float):
    payment_processor.process_payment(amount)

# Integrating the new payment gateway using the adapter
new_gateway = NewPaymentGateway()
adapter = NewPaymentGatewayAdapter(new_gateway)

# Using the adapter to process the payment
make_payment(adapter, 100.0)

'''
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 4. Decorator Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Add responsibilities or features to objects dynamically. 
<< 4.1 Function Decorator >>
'''
def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_execution
def read_data(spark, path):
    return spark.read.csv(path, header=True, inferSchema=True)

df = read_data(spark, "path/to/csv")

<< 4.2 Method Decorator >>
def my_method_decorator(method):
    def wrapper(self, *args, **kwargs):
        print("Something is happening before the method is called.")
        result = method(self, *args, **kwargs)
        print("Something is happening after the method is called.")
        return result
    return wrapper

class MyClass:
    @my_method_decorator
    def say_hello(self):
        print("Hello from a method!")

obj = MyClass()
obj.say_hello()

<< 4.3 Class Decorator >> 
These decorators are applied to classes to modify or extend their behavior.

def my_class_decorator(cls):
    cls.extra_attribute = "I am an extra attribute"
    return cls

@my_class_decorator
class MyClass:
    pass

obj = MyClass()
print(obj.extra_attribute)
'''
<<< 4. Property Decorators >>>
These decorators are used to create getter, setter, and deleter methods for class attributes.
'''
class MyClass:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @value.deleter
    def value(self):
        del self._value

obj = MyClass(10)
print(obj.value)
obj.value = 20
print(obj.value)
del obj.value
'''
<<< 5. Static and Class Method Decorators >>>
These decorators are used to define static methods and class methods.
'''
class MyClass:
    @staticmethod
    def static_method():
        print("This is a static method.")

    @classmethod
    def class_method(cls):
        print("This is a class method.")

MyClass.static_method()
MyClass.class_method()
'''
<< 6. Decorators with Arguments >>
These decorators take arguments themselves, adding a layer of complexity but also flexibility.
''' 
def decorator_with_args(arg):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Decorator argument: {arg}")
            return func(*args, **kwargs)
        return wrapper
    return my_decorator

@decorator_with_args("Hello")
def say_hello():
    print("Hello!")

say_hello()
'''
<< 7. Chained Decorators >>
These involve applying multiple decorators to a single function or method.
'''
def decorator1(func):
    def wrapper(*args, **kwargs):
        print("Decorator 1")
        return func(*args, **kwargs)
    return wrapper

def decorator2(func):
    def wrapper(*args, **kwargs):
        print("Decorator 2")
        return func(*args, **kwargs)
    return wrapper

@decorator1
@decorator2
def say_hello():
    print("Hello!")

say_hello()
'''
<< 8. Context Manager Decorators >>
These are used to manage resources before and after function execution, similar to context managers but as decorators.
In Python, the yield statement is used in a context manager to create a boundary where setup and teardown code can be 
separated. The @contextmanager decorator from the contextlib module uses yield to manage this boundary effectively.
You can create context managers by defining a class with __enter__ and __exit__ methods. This approach doesn’t use 
yield but provides similar functionality.
'''
from contextlib import contextmanager

@contextmanager
def my_context_manager():
    print("Before")
    yield
    print("After")

def my_decorator(func):
    def wrapper(*args, **kwargs):
        with my_context_manager():
            return func(*args, **kwargs)
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
'''
Summary
Decorators in Python can be categorized based on their usage and the type of entity they 
are modifying (functions, methods, classes, properties, etc.). They provide a powerful 
way to extend and modify behavior in a clean and reusable manner.

###################### PySpark ETL examples to show when to use the ##############################3
## Command Pattern, 
## Strategy Pattern, 
## Template Method Pattern, 
## Chain of Responsibility Pattern, 
## Observer Pattern. 
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 5. Command Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Encapsulate a request as an object, thereby allowing for parameterization and queuing of requests.
******************************** Summary *************************************************
support Execute and Undo methods
'''
from abc import ABC, abstractmethod
from pyspark.sql import SparkSession

# Command interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

# Concrete Command for Extraction
class ExtractCommand(Command):
    def __init__(self, spark, path):
        self.spark = spark
        self.path = path
        self.df = None

    def execute(self):
        self.df = self.spark.read.csv(self.path, header=True, inferSchema=True)
        print(f"Extracted data from {self.path}")
        return self.df

    def undo(self):
        self.df = None
        print(f"Undid extraction from {self.path}")

# Concrete Command for Transformation
class TransformCommand(Command):
    def __init__(self, df):
        self.df = df
        self.original_df = df

    def execute(self):
        self.df = self.df.withColumn('new_column', self.df['existing_column'] * 2)
        print("Transformed data by adding new_column")
        return self.df

    def undo(self):
        self.df = self.original_df
        print("Undid transformation")

# Concrete Command for Loading
class LoadCommand(Command):
    def __init__(self, df, path):
        self.df = df
        self.path = path

    def execute(self):
        self.df.write.mode('overwrite').csv(self.path)
        print(f"Loaded data to {self.path}")

    def undo(self):
        # Undo operation for load is tricky; for simplicity, we assume it cannot be undone
        print("Load operation cannot be undone")

# Command Manager
class CommandManager:
    def __init__(self):
        self.history = []

    def execute(self, command):
        result = command.execute()
        self.history.append(command)
        return result

    def undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()
# Main
# Initialize Spark session
spark = SparkSession.builder.appName("ETL Command Pattern").getOrCreate()
command_manager = CommandManager()

# Extract data
extract_command = ExtractCommand(spark, "data/input.csv")
df = command_manager.execute(extract_command)

# Transform data
transform_command = TransformCommand(df)
df = command_manager.execute(transform_command)

# Load data
load_command = LoadCommand(df, "data/output.csv")
command_manager.execute(load_command)

# Undo transformation (if needed)
command_manager.undo()

# Display resulting DataFrame
df.show()

'''
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 6. Strategy Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Define a family of algorithms, encapsulate each one, and make them interchangeable.
******************************************* Summary *************************************************
Inter-changable
'''
from abc import ABC, abstractmethod
from pyspark.sql import SparkSession

# Strategy interface
class TransformationStrategy(ABC):
    @abstractmethod
    def transform(self, df):
        pass

# Concrete Strategy 1: Add Column
class AddColumnStrategy(TransformationStrategy):
    def transform(self, df):
        return df.withColumn('new_column', df['existing_column'] * 2)

# Concrete Strategy 2: Filter Rows
class FilterRowsStrategy(TransformationStrategy):
    def transform(self, df):
        return df.filter(df['existing_column'] > 10)

# Concrete Strategy 3: Drop Column
class DropColumnStrategy(TransformationStrategy):
    def transform(self, df):
        return df.drop('existing_column')
        
# -------- Define the Context Class
class DataFrameTransformer:
    def __init__(self, strategy: TransformationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: TransformationStrategy):
        self._strategy = strategy

    def transform(self, df):
        return self._strategy.transform(df)

# ------------ use it
# Initialize Spark session
spark = SparkSession.builder.appName("ETL Strategy Pattern").getOrCreate()

# Load initial data
df = spark.read.csv("data/input.csv", header=True, inferSchema=True)

# Initialize transformer with a strategy
transformer = DataFrameTransformer(AddColumnStrategy())

# Apply the transformation
transformed_df = transformer.transform(df)

# Show resulting DataFrame
transformed_df.show()

# Change strategy to filter rows
transformer.set_strategy(FilterRowsStrategy())
filtered_df = transformer.transform(df)
filtered_df.show()

# Change strategy to drop column
transformer.set_strategy(DropColumnStrategy())
dropped_df = transformer.transform(df)
dropped_df.show()

'''
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 7. Observer Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Define a one-to-many dependency between objects so that when one object changes state, 
all its dependents are notified and updated automatically.
******************************** Summary *************************************************
'''
from abc import ABC, abstractmethod
from pyspark.sql import SparkSession

# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, event, data):
        pass

# Subject interface
class Subject(ABC):
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, event, data):
        for observer in self._observers:
            observer.update(event, data
                           
# Concrete Observer 1: Logger
class Logger(Observer):
    def update(self, event, data):
        print(f"Logger: Event '{event}' with data {data}")

# Concrete Observer 2: Data Validator
class DataValidator(Observer):
    def update(self, event, data):
        if event == "transform":
            print(f"DataValidator: Validating data...")
            # Example validation logic
            if data.count() == 0:
                print("DataValidator: Validation failed - no rows in DataFrame")
            else:
                print("DataValidator: Validation passed")

# ETL Process (Subject)
class ETLProcess(Subject):
    def __init__(self, spark):
        super().__init__()
        self.spark = spark
        self.df = None

    def extract(self, path):
        self.df = self.spark.read.csv(path, header=True, inferSchema=True)
        self.notify("extract", self.df)
        print(f"Extracted data from {path}")

    def transform(self):
        self.df = self.df.withColumn('new_column', self.df['existing_column'] * 2)
        self.notify("transform", self.df)
        print("Transformed data by adding new_column")

    def load(self, path):
        self.df.write.mode('overwrite').csv(path)
        self.notify("load", self.df)
        print(f"Loaded data to {path}")

# Initialize Spark session
spark = SparkSession.builder.appName("ETL Observer Pattern").getOrCreate()

# Initialize ETL process and observers
etl_process = ETLProcess(spark)
logger = Logger()
validator = DataValidator()

# Attach observers to the ETL process
etl_process.attach(logger)
etl_process.attach(validator)

# Perform ETL steps
etl_process.extract("data/input.csv")
etl_process.transform()
etl_process.load("data/output.csv")

'''
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 8. Template Method Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Define the skeleton of an algorithm in a method, deferring some steps to subclasses.
******************************** Summary *************************************************
The Template Pattern has several unique characteristics that distinguish it from the Strategy, Factory Method, Builder, and Command patterns. Here are some key points that highlight what makes the Template Pattern unique:
Key Characteristics of the Template Pattern

Algorithm Structure:
Template Pattern: Defines the skeleton of an algorithm in a base class method, allowing subclasses to 
override specific steps of the algorithm without changing its structure. This ensures a consistent 
overall process while providing flexibility for customization.
Strategy Pattern: Encapsulates entire algorithms or behaviors in separate classes and makes them 
interchangeable. The focus is on swapping complete strategies rather than customizing parts of a 
single algorithm.
Factory Method Pattern: Focuses on creating objects. It defines a method in the base class for 
creating objects but lets subclasses alter the type of objects created. The emphasis is on object 
creation rather than process flow.
Builder Pattern: Separates the construction of a complex object from its representation. It focuses 
on step-by-step construction of an object, allowing for different representations of the final product.
Command Pattern: Encapsulates a request as an object, thereby allowing for parameterization of 
clients with queues, requests, and operations. It focuses on the action to be performed rather 
than the structure of an algorithm.

Inheritance and Method Overriding:
Template Pattern: Relies heavily on inheritance and method overriding. The base class defines the 
overall structure of the algorithm, while subclasses override specific steps. This pattern promotes 
code reuse by allowing common logic to be defined in the base class.
Strategy Pattern: Uses composition instead of inheritance. The context class delegates the algorithm 
to a strategy object, making it easy to change the algorithm at runtime.
Factory Method Pattern: Uses inheritance to defer the instantiation of objects to subclasses. The 
focus is on the method of creating objects rather than algorithmic steps.
Builder Pattern: Often uses composition. The builder class constructs the product step-by-step, 
and the final product is returned to the client.
Command Pattern: Uses composition. Commands encapsulate actions and are executed by the invoker. 
The focus is on executing requests rather than algorithmic steps.

Customization and Flexibility:
Template Pattern: Provides a predefined structure with specific hooks for customization. Subclasses 
are limited to modifying only certain parts of the algorithm, ensuring a consistent process flow.
Strategy Pattern: Offers high flexibility by allowing the entire algorithm to be replaced. Each 
strategy is a complete implementation that can vary independently.
Factory Method Pattern: Customizes object creation, providing flexibility in the types of objects 
created. The process of object creation can vary independently.
Builder Pattern: Allows flexible and step-by-step construction of complex objects. Different builders 
can produce different representations of the final product.
Command Pattern: Provides flexibility in defining and executing commands. Commands can be parameterized, 
queued, and executed in different contexts.
'''
<<<<<<<<<<<<<<<<<Template Pattern>>
 
from abc import ABC, abstractmethod
from pyspark.sql import SparkSession, DataFrame

spark = SparkSession.builder.appName("ETL Template Pattern").getOrCreate()

class ETLTemplate(ABC):
    def run(self):
        data = self.extract()
        transformed_data = self.transform(data)
        self.load(transformed_data)

    @abstractmethod
    def extract(self) -> DataFrame:
        pass

    @abstractmethod
    def transform(self, data: DataFrame) -> DataFrame:
        pass

    @abstractmethod
    def load(self, data: DataFrame):
        pass

class CSVToParquetETL(ETLTemplate):
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

    def extract(self) -> DataFrame:
        return spark.read.csv(self.input_path, header=True, inferSchema=True)

    def transform(self, data: DataFrame) -> DataFrame:
        return data.withColumnRenamed("old_column_name", "new_column_name")

    def load(self, data: DataFrame):
        data.write.parquet(self.output_path)

class JSONToParquetETL(ETLTemplate):
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

    def extract(self) -> DataFrame:
        return spark.read.json(self.input_path)

    def transform(self, data: DataFrame) -> DataFrame:
        return data.withColumn("new_column", data["existing_column"] + 1)

    def load(self, data: DataFrame):
        data.write.parquet(self.output_path)

# Example usage
csv_etl = CSVToParquetETL("input.csv", "output.parquet")
csv_etl.run()

json_etl = JSONToParquetETL("input.json", "output.parquet")
json_etl.run()

<<<<<<<<<<<<<<<<<Strategy Pattern>>
 from abc import ABC, abstractmethod
from pyspark.sql import SparkSession, DataFrame

spark = SparkSession.builder.appName("ETL Strategy Pattern").getOrCreate()

class ExtractStrategy(ABC):
    @abstractmethod
    def extract(self, path: str) -> DataFrame:
        pass

class CSVExtractStrategy(ExtractStrategy):
    def extract(self, path: str) -> DataFrame:
        return spark.read.csv(path, header=True, inferSchema=True)

class JSONExtractStrategy(ExtractStrategy):
    def extract(self, path: str) -> DataFrame:
        return spark.read.json(path)

class TransformStrategy(ABC):
    @abstractmethod
    def transform(self, data: DataFrame) -> DataFrame:
        pass

class RenameColumnTransformStrategy(TransformStrategy):
    def transform(self, data: DataFrame) -> DataFrame:
        return data.withColumnRenamed("old_column_name", "new_column_name")

class AddColumnTransformStrategy(TransformStrategy):
    def transform(self, data: DataFrame) -> DataFrame:
        return data.withColumn("new_column", data["existing_column"] + 1)

class LoadStrategy(ABC):
    @abstractmethod
    def load(self, data: DataFrame, path: str):
        pass

class ParquetLoadStrategy(LoadStrategy):
    def load(self, data: DataFrame, path: str):
        data.write.parquet(path)

class ETLProcess:
    def __init__(self, extract_strategy: ExtractStrategy, transform_strategy: TransformStrategy, load_strategy: LoadStrategy):
        self.extract_strategy = extract_strategy
        self.transform_strategy = transform_strategy
        self.load_strategy = load_strategy

    def run(self, input_path: str, output_path: str):
        data = self.extract_strategy.extract(input_path)
        transformed_data = self.transform_strategy.transform(data)
        self.load_strategy.load(transformed_data, output_path)

# Example usage
csv_etl = ETLProcess(CSVExtractStrategy(), RenameColumnTransformStrategy(), ParquetLoadStrategy())
csv_etl.run("input.csv", "output.parquet")

json_etl = ETLProcess(JSONExtractStrategy(), AddColumnTransformStrategy(), ParquetLoadStrategy())
json_etl.run("input.json", "output.parquet")

<<<<<<<<<<<<<<<<<Factory Method Pattern>>>
from abc import ABC, abstractmethod
from pyspark.sql import SparkSession, DataFrame

spark = SparkSession.builder.appName("ETL Factory Method Pattern").getOrCreate()

class ETLProcess(ABC):
    @abstractmethod
    def extract(self) -> DataFrame:
        pass

    @abstractmethod
    def transform(self, data: DataFrame) -> DataFrame:
        pass

    @abstractmethod
    def load(self, data: DataFrame):
        pass

    def run(self):
        data = self.extract()
        transformed_data = self.transform(data)
        self.load(transformed_data)

class CSVETLProcess(ETLProcess):
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

    def extract(self) -> DataFrame:
        return spark.read.csv(self.input_path, header=True, inferSchema=True)

    def transform(self, data: DataFrame) -> DataFrame:
        return data.withColumnRenamed("old_column_name", "new_column_name")

    def load(self, data: DataFrame):
        data.write.parquet(self.output_path)

class ETLFactory(ABC):
    @abstractmethod
    def create_etl_process(self, input_path: str, output_path: str) -> ETLProcess:
        pass

class CSVETLFactory(ETLFactory):
    def create_etl_process(self, input_path: str, output_path: str) -> ETLProcess:
        return CSVETLProcess(input_path, output_path)

# Usage
factory = CSVETLFactory()
etl_process = factory.create_etl_process("input.csv", "output.parquet")
etl_process.run()

<<<<<<<<<<<<<<<<<<<Builder Pattern>>
The Builder Pattern constructs a complex ETL process step-by-step.

from pyspark.sql import SparkSession, DataFrame

spark = SparkSession.builder.appName("ETL Builder Pattern").getOrCreate()

class ETLBuilder:
    def __init__(self):
        self.process = ETLProcess()

    def set_input_path(self, input_path: str):
        self.process.input_path = input_path
        return self

    def set_output_path(self, output_path: str):
        self.process.output_path = output_path
        return self

    def set_transformation(self, transformation):
        self.process.transformation = transformation
        return self

    def build(self):
        return self.process

class ETLProcess:
    def __init__(self):
        self.input_path = None
        self.output_path = None
        self.transformation = None

    def run(self):
        data = self.extract()
        transformed_data = self.transformation(data)
        self.load(transformed_data)

    def extract(self) -> DataFrame:
        return spark.read.csv(self.input_path, header=True, inferSchema=True)

    def load(self, data: DataFrame):
        data.write.parquet(self.output_path)

# Usage
def rename_transformation(data: DataFrame) -> DataFrame:
    return data.withColumnRenamed("old_column_name", "new_column_name")

builder = ETLBuilder()
etl_process = (builder
               .set_input_path("input.csv")
               .set_output_path("output.parquet")
               .set_transformation(rename_transformation)
               .build())
etl_process.run()

<<<<<<<<<<<<<<<Command Pattern>>
The Command Pattern encapsulates ETL operations as command objects that can be executed.
'''
from abc import ABC, abstractmethod
from pyspark.sql import SparkSession, DataFrame

spark = SparkSession.builder.appName("ETL Command Pattern").getOrCreate()

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class ExtractCommand(Command):
    def __init__(self, input_path: str):
        self.input_path = input_path
        self.data = None

    def execute(self):
        self.data = spark.read.csv(self.input_path, header=True, inferSchema=True)
        return self.data

class TransformCommand(Command):
    def __init__(self, data: DataFrame):
        self.data = data

    def execute(self):
        return self.data.withColumnRenamed("old_column_name", "new_column_name")

class LoadCommand(Command):
    def __init__(self, data: DataFrame, output_path: str):
        self.data = data
        self.output_path = output_path

    def execute(self):
        self.data.write.parquet(self.output_path)

# Usage
extract_command = ExtractCommand("input.csv")
data = extract_command.execute()

transform_command = TransformCommand(data)
transformed_data = transform_command.execute()

load_command = LoadCommand(transformed_data, "output.parquet")
load_command.execute()
'''
Summary of Differences
Template Pattern: Provides a predefined structure with specific hooks for customization. Subclasses modify parts of the algorithm.
Strategy Pattern: Allows the entire transformation strategy to be swapped. Different strategies implement different transformations.
Factory Method Pattern: Focuses on creating ETL processes for different input formats, allowing the creation process to vary independently.
Builder Pattern: Constructs a complex ETL process step-by-step, allowing for flexible and incremental construction.
Command Pattern: Encapsulates each step of the ETL process as command objects that can be executed independently.
'''
<<<<<<<<<<<<<<<<<<<<<<<<<<<< 9. Builder Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Separate the construction of a complex object from its representation so that the same construction process can create different representations.
class DataFrameBuilder:
    def __init__(self):
        self.df = None
    
    def read_csv(self, spark, path):
        self.df = spark.read.csv(path, header=True, inferSchema=True)
        return self
    
    def filter(self, condition):
        self.df = self.df.filter(condition)
        return self
    
    def build(self):
        return self.df

builder = DataFrameBuilder()
df = builder.read_csv(spark, "path/to/csv").filter("age > 21").build()
  
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 10. Prototype Pattern - deep copy and clone >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.
from abc import ABC, abstractmethod
from pyspark.sql import SparkSession, DataFrame
from copy import deepcopy

spark = SparkSession.builder.appName("ETL Prototype Pattern").getOrCreate()

# Prototype Interface
class ETLProcess(ABC):
    @abstractmethod
    def clone(self):
        pass

    @abstractmethod
    def extract(self) -> DataFrame:
        pass

    @abstractmethod
    def transform(self, data: DataFrame) -> DataFrame:
        pass

    @abstractmethod
    def load(self, data: DataFrame):
        pass

    def run(self):
        data = self.extract()
        transformed_data = self.transform(data)
        self.load(transformed_data)

# Concrete Prototype
class CSVToParquetETL(ETLProcess):
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

    def clone(self):
        return deepcopy(self)

    def extract(self) -> DataFrame:
        return spark.read.csv(self.input_path, header=True, inferSchema=True)

    def transform(self, data: DataFrame) -> DataFrame:
        return data.withColumnRenamed("old_column_name", "new_column_name")

    def load(self, data: DataFrame):
        data.write.parquet(self.output_path)

# Usage
original_etl = CSVToParquetETL("input.csv", "output.parquet")
original_etl.run()

# Clone the original ETL process and modify its configuration
cloned_etl = original_etl.clone()
cloned_etl.input_path = "input2.csv"
cloned_etl.output_path = "output2.parquet"
cloned_etl.run()

<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 11. Chain of Responsibility Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request.


class Handler:
    def set_next(self, handler):
        self.next_handler = handler
        return handler
    
    def handle(self, request):
        if self.next_handler:
            return self.next_handler.handle(request)
        return None

class ReadCSVHandler(Handler):
    def handle(self, request):
        if request == "csv":
            return spark.read.csv("path/to/csv", header=True, inferSchema=True)
        return super().handle(request)

class ReadParquetHandler(Handler):
    def handle(self, request):
        if request == "parquet":
            return spark.read.parquet("path/to/parquet")
        return super().handle(request)

csv_handler = ReadCSVHandler()
parquet_handler = csv_handler.set_next(ReadParquetHandler())
df = csv_handler.handle("csv")
  
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 12. Mediator Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Define an object that encapsulates how a set of objects interact.

class Mediator:
    def notify(self, sender, event):
        pass

class DataMediator(Mediator):
    def notify(self, sender, event):
        if event == "read":
            df = sender.read_data()
            df.show()

class DataComponent:
    def __init__(self, mediator):
        self.mediator = mediator
    
    def read_data(self):
        pass

class CSVDataComponent(DataComponent):
    def read_data(self):
        return spark.read.csv("path/to/csv", header=True, inferSchema=True)

mediator = DataMediator()
component = CSVDataComponent(mediator)
mediator.notify(component, "read")
         
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 13. State Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Allow an object to alter its behavior when its internal state changes.

class State:
    def handle(self, context):
        pass

class ReadingState(State):
    def handle(self, context):
        context.df = spark.read.csv("path/to/csv", header=True, inferSchema=True)
        context.set_state(TransformingState())

class TransformingState(State):
    def handle(self, context):
        context.df = context.df.filter(context.df.age > 21)
        context.set_state(LoadingState())

class LoadingState(State):
    def handle(self, context):
        context.df.write.parquet("path/to/output")
        context.set_state(None)

class Context:
    def __init__(self, state: State):
        self.state = state
        self.df = None
    
    def set_state(self, state: State):
        self.state = state
    
    def request(self):
        if self.state:
            self.state.handle(self)

context = Context(ReadingState())
context.request()
context.request()
context.request()
       
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 14. Memento Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to this state later.


class Memento:
    def __init__(self, state):
        self.state = state

class Originator:
    def __init__(self):
        self.state = None
    
    def set_state(self, state):
        self.state = state
    
    def save_to_memento(self):
        return Memento(self.state)
    
    def restore_from_memento(self, memento):
        self.state = memento.state

originator = Originator()
originator.set_state(spark.read.csv("path/to/csv", header


=True, inferSchema=True))
memento = originator.save_to_memento()

originator.set_state(spark.read.csv("path/to/another/csv", header=True, inferSchema=True))
originator.restore_from_memento(memento)
       
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 15. Interpreter Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Rule based approach

class Expression:
    def interpret(self, context):
        pass

class ReadExpression(Expression):
    def interpret(self, context):
        context.df = spark.read.csv("path/to/csv", header=True, inferSchema=True)

class FilterExpression(Expression):
    def interpret(self, context):
        context.df = context.df.filter("age > 21")

class Context:
    def __init__(self):
        self.df = None

context = Context()
read_expr = ReadExpression()
filter_expr = FilterExpression()

read_expr.interpret(context)
filter_expr.interpret(context)
context.df.show()
           
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 16. Iterator Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation.
class DataFrameIterator:
    def __init__(self, df):
        self.df = df.collect()
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.df):
            result = self.df[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

df = spark.read.csv("path/to/csv", header=True, inferSchema=True)
iterator = DataFrameIterator(df)

for row in iterator:
    print(row)

<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 17. Visitor Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Represent an operation to be performed on the elements of an object structure.
class DataFrameVisitor:
    def visit(self, df):
        pass

class ShowVisitor(DataFrameVisitor):
    def visit(self, df):
        df.show()

class SchemaVisitor(DataFrameVisitor):
    def visit(self, df):
        df.printSchema()

df = spark.read.csv("path/to/csv", header=True, inferSchema=True)
show_visitor = ShowVisitor()
schema_visitor = SchemaVisitor()

show_visitor.visit(df)
schema_visitor.visit(df)

<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 18. Composite Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Compose objects into tree structures to represent part-whole hierarchies.


class Component:
    def operation(self):
        pass

class Leaf(Component):
    def operation(self):
        return spark.read.csv("path/to/csv", header=True, inferSchema=True)

class Composite(Component):
    def __init__(self):
        self.children = []
    
    def add(self, component):
        self.children.append(component)
    
    def operation(self):
        result = []
        for child in self.children:
            result.append(child.operation())
        return result

composite = Composite()
composite.add(Leaf())
composite.add(Leaf())
dataframes = composite.operation()
19. Bridge Pattern
Decouple an abstraction from its implementation so that the two can vary independently.


class DataSource:
    def read(self):
        pass

class CSVSource(DataSource):
    def read(self):
        return spark.read.csv("path/to/csv", header=True, inferSchema=True)

class ParquetSource(DataSource):
    def read(self):
        return spark.read.parquet("path/to/parquet")

class DataReader:
    def __init__(self, source: DataSource):
        self.source = source
    
    def read(self):
        return self.source.read()

csv_reader = DataReader(CSVSource())
df = csv_reader.read()
20. Proxy Pattern
Provide a surrogate or placeholder for another object to control access to it.


class DataFrameProxy:
    def __init__(self, path):
        self.path = path
        self.df = None
    
    def read(self):
        if self.df is None:
            self.df = spark.read.csv(self.path, header=True, inferSchema=True)
        return self.df

proxy = DataFrameProxy("path/to/csv")
df = proxy.read()
21. Flyweight Pattern
Use sharing to support large numbers of fine-grained objects efficiently.


class DataFrameFlyweightFactory:
    _dataframes = {}
    
    @staticmethod
    def get_dataframe(path):
        if path not in DataFrameFlyweightFactory._dataframes:
            DataFrameFlyweightFactory._dataframes[path] = spark.read.csv(path, header=True, inferSchema=True)
        return DataFrameFlyweightFactory._dataframes[path]

df = DataFrameFlyweightFactory.get_dataframe("path/to/csv")
22. Facade Pattern
Provide a unified interface to a set of interfaces in a subsystem.


class DataFrameFacade:
    @staticmethod
    def read_csv(path):
        return spark.read.csv(path, header=True, inferSchema=True)
    
    @staticmethod
    def read_parquet(path):
        return spark.read.parquet(path)

df = DataFrameFacade.read_csv("path/to/csv")
23. Abstract Factory Pattern
Provide an interface for creating families of related or dependent objects without specifying their concrete classes.


class DataReaderFactory:
    def create_reader(self):
        pass

class CSVReaderFactory(DataReaderFactory):
    def create_reader(self):
        return CSVReader()

class ParquetReaderFactory(DataReaderFactory):
    def create_reader(self):
        return ParquetReader()

csv_factory = CSVReaderFactory()
reader = csv_factory.create_reader()
df = reader.read(spark, "path/to/csv")
24. Chain of Responsibility Pattern (Extended)
Allow an object to pass the request along a chain of potential handlers until an object handles the request.


class Handler:
    def set_next(self, handler):
        self.next_handler = handler
        return handler
    
    def handle(self, request):
        if self.next_handler:
            return self.next_handler.handle(request)
        return None

class CSVHandler(Handler):
    def handle(self, request):
        if request == "csv":
            return spark.read.csv("path/to/csv", header=True, inferSchema=True)
        return super().handle(request)

class ParquetHandler(Handler):
    def handle(self, request):
        if request == "parquet":
            return spark.read.parquet("path/to/parquet")
        return super().handle(request)

csv_handler = CSVHandler()
parquet_handler = csv_handler.set_next(ParquetHandler())
df = csv_handler.handle("csv")
25. Template Method Pattern (Extended)
Define the skeleton of an algorithm in the base class and allow subclasses to override specific steps of the algorithm.


class DataProcessor:
    def process(self):
        self.read()
        self.transform()
        self.load()
    
    def read(self):
        raise NotImplementedError
    
    def transform(self):
        raise NotImplementedError
    
    def load(self):
        raise NotImplementedError

class CSVProcessor(DataProcessor):
    def read(self):
        self.df = spark.read.csv("path/to/csv", header=True, inferSchema=True)
    
    def transform(self):
        self.df = self.df.filter("age > 21")
    
    def load(self):
        self.df.write.parquet("path/to/output")

processor = CSVProcessor()
processor.process()
26. Composite Pattern (Extended)
Compose objects into tree structures to represent part-whole hierarchies.


class Component:
    def operation(self):
        pass

class Leaf(Component):
    def operation(self):
        return spark.read.csv("path/to/csv", header=True, inferSchema=True)

class Composite(Component):
    def __init__(self):
        self.children = []
    
    def add(self, component):
        self.children.append(component)
    
    def operation(self):
        result = []
        for child in self.children:
            result.append(child.operation())
        return result

composite = Composite()
composite.add(Leaf())
composite.add(Leaf())
dataframes = composite.operation()
This example provides a high-level overview of how to use various design patterns in the context of a PySpark ETL process. Each pattern is implemented in a simplified form to illustrate its usage.

##*******************************************************************************************##
END to END Solutions

Creating a complete ETL (Extract, Transform, Load) pipeline in PySpark using various design patterns involves integrating multiple components to handle different aspects of data processing efficiently. Here's an end-to-end ETL design that incorporates several design patterns to demonstrate their use in a practical context.

Step-by-Step ETL Design
Singleton Pattern for SparkSession.
Factory Method Pattern for data readers.
Strategy Pattern for different transformation strategies.
Template Method Pattern for defining the ETL process.
Observer Pattern for logging and monitoring.
Implementation
1. Singleton Pattern for SparkSession
Ensure only one SparkSession is created and used throughout the application.


from pyspark.sql import SparkSession

class SingletonSparkSession:
    _instance = None

    @staticmethod
    def get_instance():
        if SingletonSparkSession._instance is None:
            SingletonSparkSession._instance = SparkSession.builder.appName("ETLExample").getOrCreate()
        return SingletonSparkSession._instance

spark = SingletonSparkSession.get_instance()
2. Factory Method Pattern for Data Readers
Create a common interface for reading data from different sources.


class DataReader:
    def read(self, spark, path):
        pass

class CSVReader(DataReader):
    def read(self, spark, path):
        return spark.read.csv(path, header=True, inferSchema=True)

class ParquetReader(DataReader):
    def read(self, spark, path):
        return spark.read.parquet(path)

class DataReaderFactory:
    @staticmethod
    def create_reader(file_type):
        if file_type == "csv":
            return CSVReader()
        elif file_type == "parquet":
            return ParquetReader()
        else:
            raise ValueError("Unsupported file type")
3. Strategy Pattern for Transformations
Define different transformation strategies.


class TransformationStrategy:
    def apply(self, df):
        pass

class FilterAdultsStrategy(TransformationStrategy):
    def apply(self, df):
        return df.filter(df.age > 18)

class SelectColumnsStrategy(TransformationStrategy):
    def apply(self, df):
        return df.select("name", "age")
4. Template Method Pattern for ETL Process
Define the skeleton of the ETL process, allowing subclasses to implement specific steps.


class ETLProcess:
    def __init__(self, reader, transformations, output_path):
        self.reader = reader
        self.transformations = transformations
        self.output_path = output_path

    def execute(self, spark, input_path):
        df = self.extract(spark, input_path)
        df = self.transform(df)
        self.load(df)

    def extract(self, spark, input_path):
        return self.reader.read(spark, input_path)

    def transform(self, df):
        for transformation in self.transformations:
            df = transformation.apply(df)
        return df

    def load(self, df):
        df.write.parquet(self.output_path)
5. Observer Pattern for Logging and Monitoring
Allow for logging and monitoring of the ETL process.


class Observer:
    def update(self, event, data=None):
        pass

class Logger(Observer):
    def update(self, event, data=None):
        print(f"Event: {event}, Data: {data}")

class ETLObservable:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self, event, data=None):
        for observer in self.observers:
            observer.update(event, data)

class ObservableETLProcess(ETLProcess, ETLObservable):
    def __init__(self, reader, transformations, output_path):
        ETLProcess.__init__(self, reader, transformations, output_path)
        ETLObservable.__init__(self)

    def execute(self, spark, input_path):
        self.notify("start", input_path)
        super().execute(spark, input_path)
        self.notify("end", self.output_path)
Putting It All Together

def main():
    spark = SingletonSparkSession.get_instance()

    # Factory to create a data reader
    reader = DataReaderFactory.create_reader("csv")

    # Transformation strategies
    transformations = [
        FilterAdultsStrategy(),
        SelectColumnsStrategy()
    ]

    # Define the output path
    output_path = "path/to/output"

    # Create an observable ETL process
    etl_process = ObservableETLProcess(reader, transformations, output_path)

    # Attach a logger
    logger = Logger()
    etl_process.attach(logger)

    # Execute the ETL process
    input_path = "path/to/input.csv"
    etl_process.execute(spark, input_path)

if __name__ == "__main__":
    main()
Explanation
SingletonSparkSession: Ensures only one instance of SparkSession is created.
DataReaderFactory: Uses the factory method pattern to create appropriate data readers based on the file type.
TransformationStrategy: Different strategies for transforming the DataFrame.
ETLProcess: Defines the ETL process skeleton using the template method pattern.
ObservableETLProcess: Extends ETLProcess and ETLObservable to add observer capabilities for logging and monitoring.
This design ensures a flexible and maintainable ETL pipeline by decoupling different parts of the process and using design patterns to manage the complexity.



