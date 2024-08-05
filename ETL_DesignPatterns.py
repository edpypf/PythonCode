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

<< 6. Decorator >> 
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


<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 4. Decorator Pattern >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Add responsibilities to objects dynamically.


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
5. Command Pattern
Encapsulate a request as an object, thereby allowing for parameterization and queuing of requests.


class Command:
    def execute(self):
        pass

class ReadCSVCommand(Command):
    def __init__(self, spark, path):
        self.spark = spark
        self.path = path
    
    def execute(self):
        return self.spark.read.csv(self.path, header=True, inferSchema=True)

read_command = ReadCSVCommand(spark, "path/to/csv")
df = read_command.execute()
6. Strategy Pattern
Define a family of algorithms, encapsulate each one, and make them interchangeable.


class ReadStrategy:
    def read(self, spark, path):
        pass

class CSVReadStrategy(ReadStrategy):
    def read(self, spark, path):
        return spark.read.csv(path, header=True, inferSchema=True)

class ParquetReadStrategy(ReadStrategy):
    def read(self, spark, path):
        return spark.read.parquet(path)

class DataReader:
    def __init__(self, strategy: ReadStrategy):
        self.strategy = strategy
    
    def read(self, spark, path):
        return self.strategy.read(spark, path)

csv_reader = DataReader(CSVReadStrategy())
df = csv_reader.read(spark, "path/to/csv")
7. Observer Pattern
Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.


class DataObserver:
    def update(self, df):
        pass

class PrintObserver(DataObserver):
    def update(self, df):
        df.show()

class DataSubject:
    def __init__(self):
        self.observers = []
    
    def attach(self, observer: DataObserver):
        self.observers.append(observer)
    
    def notify(self, df):
        for observer in self.observers:
            observer.update(df)

subject = DataSubject()
observer = PrintObserver()
subject.attach(observer)
df = spark.read.csv("path/to/csv", header=True, inferSchema=True)
subject.notify(df)
8. Template Method Pattern
Define the skeleton of an algorithm in a method, deferring some steps to subclasses.


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

class CSVDataProcessor(DataProcessor):
    def read(self):
        self.df = spark.read.csv("path/to/csv", header=True, inferSchema=True)
    
    def transform(self):
        self.df = self.df.filter(self.df.age > 21)
    
    def load(self):
        self.df.write.parquet("path/to/output")

processor = CSVDataProcessor()
processor.process()
9. Builder Pattern
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
10. Prototype Pattern
Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.


class DataFramePrototype:
    def __init__(self, df):
        self.df = df
    
    def clone(self):
        return self.df

prototype = DataFramePrototype(spark.read.csv("path/to/csv", header=True, inferSchema=True))
df_clone = prototype.clone()
11. Chain of Responsibility Pattern
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
12. Mediator Pattern
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
13. State Pattern
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
14. Memento Pattern
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
15. Interpreter Pattern
Given a language, define a representation for its grammar along with an interpreter that uses the representation to interpret sentences in the language.


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
16. Iterator Pattern
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
17. Visitor Pattern
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
18. Composite Pattern
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



