from abc import ABC, abstractmethod

# Subject Interface
class DatabaseConnection(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute_query(self, query):
        pass

    @abstractmethod
    def disconnect(self):
        pass
      
-- Real Subject
import sqlite3

class RealDatabaseConnection(DatabaseConnection):
    def __init__(self, database):
        self.database = database
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.database)
            print(f"Connected to database: {self.database}")
        else:
            print(f"Already connected to database: {self.database}")

    def execute_query(self, query):
        if self.connection is None:
            raise Exception("Database not connected")
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        return cursor.fetchall()

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print(f"Disconnected from database: {self.database}")
        else:
            print("No connection to close")

# Proxy Implementation
class DatabaseConnectionProxy(DatabaseConnection):
    def __init__(self, real_connection):
        self.real_connection = real_connection
        self.logged_in = False

    def authenticate(self, password):
        # Simulate authentication
        if password == "securepassword":
            self.logged_in = True
            print("Authentication successful")
        else:
            self.logged_in = False
            print("Authentication failed")

    def connect(self):
        if self.logged_in:
            self.real_connection.connect()
        else:
            print("Access denied. Please authenticate first.")

    def execute_query(self, query):
        if self.logged_in:
            return self.real_connection.execute_query(query)
        else:
            raise Exception("Access denied. Please authenticate first.")

    def disconnect(self):
        if self.logged_in:
            self.real_connection.disconnect()
        else:
            print("Access denied. Please authenticate first.")

# Client Code
if __name__ == '__main__':
    real_db_connection = RealDatabaseConnection("example.db")
    proxy = DatabaseConnectionProxy(real_db_connection)

    # Attempt to connect to the database without authentication
    proxy.connect()

    # Authenticate and connect to the database
    proxy.authenticate("securepassword")
    proxy.connect()

    # Execute a query
    try:
        result = proxy.execute_query("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        print("Table created successfully")
    except Exception as e:
        print(e)

    # Disconnect from the database
    proxy.disconnect()
