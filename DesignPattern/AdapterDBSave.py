# Step 1: Define the Target Interface
class DataStorage:
    def save(self, data):
        pass

# Step 2: Implement Adapters for Each Storage System

# Adapter for SQL Database
class SQLDatabase:
    def insert(self, data):
        print(f"Data inserted into SQL database: {data}")

class SQLDatabaseAdapter(DataStorage):
    def __init__(self, sql_database):
        self.sql_database = sql_database
    
    def save(self, data):
        self.sql_database.insert(data)

# Adapter for NoSQL Database
class NoSQLDatabase:
    def add(self, data):
        print(f"Data added to NoSQL database: {data}")

class NoSQLDatabaseAdapter(DataStorage):
    def __init__(self, nosql_database):
        self.nosql_database = nosql_database
    
    def save(self, data):
        self.nosql_database.add(data)

# Adapter for Cloud Storage
class CloudStorage:
    def upload(self, data):
        print(f"Data uploaded to cloud storage: {data}")

class CloudStorageAdapter(DataStorage):
    def __init__(self, cloud_storage):
        self.cloud_storage = cloud_storage
    
    def save(self, data):
        self.cloud_storage.upload(data)

# Step 3: Use Adapters in Your Application

# Create instances of the storage systems
sql_database = SQLDatabase()
nosql_database = NoSQLDatabase()
cloud_storage = CloudStorage()

# Create adapters for the storage systems
sql_database_adapter = SQLDatabaseAdapter(sql_database)
nosql_database_adapter = NoSQLDatabaseAdapter(nosql_database)
cloud_storage_adapter = CloudStorageAdapter(cloud_storage)

# Save data through the adapters
def store_data(data_storage, data):
    data_storage.save(data)

# Using the adapters to store data
store_data(sql_database_adapter, "SQL data")           # Output: Data inserted into SQL database: SQL data
store_data(nosql_database_adapter, "NoSQL data")       # Output: Data added to NoSQL database: NoSQL data
store_data(cloud_storage_adapter, "Cloud data")        # Output: Data uploaded to cloud storage: Cloud data
