class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ConfigurationManager(metaclass=Singleton):
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        # Simulate loading configuration from a file or database
        return {
            "database": "sqlserver",
            "timeout": 30,
            "retries": 3
        }

    def get_config(self, key):
        return self.config.get(key)

# Usage
if __name__ == "__main__":
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()

    print(config1.get_config("database"))  # Output: sqlserver
    print(config1 == config2)              # Output: True
    print(config1.get_config("timeout"))   # Output: 30
    print(config2.get_config("retries"))   # Output: 3
