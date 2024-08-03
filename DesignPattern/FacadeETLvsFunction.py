'''
You're correct that in the More Complex Example, the DataProcessingFacade appears to only wrap the run_pipeline() method from DataPipeline,
which might seem redundant. To better illustrate the true value of the Facade Pattern, let's expand on its benefits and use it in a more 
nuanced scenario where it provides real advantages beyond simply calling an existing method.

Expanded Example with Real Benefits
To fully leverage the Facade Pattern, let's consider a scenario where the facade does more than just call an existing method. We'll add 
additional functionalities such as configuration handling, error management, and logging. This expanded example will show how the facade 
can manage complexity and provide a clean API.

Expanded Subsystem Classes
We'll introduce more detailed functionality, including configuration and error handling.
'''
class DataExtractor:
    def extract(self):
        print("Extracting data...")
        # Simulating data extraction
        return "Extracted data"

class DataCleaner:
    def clean(self, data):
        print("Cleaning data...")
        # Simulating data cleaning
        return f"Cleaned {data}"

class DataTransformer:
    def transform(self, data):
        print("Transforming data...")
        # Simulating data transformation
        return f"Transformed {data}"

class DataLoader:
    def load(self, data):
        print("Loading data...")
        # Simulating data loading
        print(f"Loaded {data}")

class ErrorLogger:
    def log_error(self, error):
        print(f"Error: {error}")

class DataPipeline:
    def __init__(self):
        self.extractor = DataExtractor()
        self.cleaner = DataCleaner()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
        self.error_logger = ErrorLogger()

    def run_pipeline(self):
        try:
            data = self.extractor.extract()
            cleaned_data = self.cleaner.clean(data)
            transformed_data = self.transformer.transform(cleaned_data)
            self.loader.load(transformed_data)
        except Exception as e:
            self.error_logger.log_error(str(e))

'''
Facade Class with Enhanced Functionality
The facade class will handle additional tasks such as configuration, logging, and error management.
'''
class DataProcessingFacade:
    def __init__(self, config):
        self.config = config
        self.pipeline = DataPipeline()
    
    def configure_pipeline(self):
        # Apply configuration settings if needed
        print(f"Applying configuration: {self.config}")
        # Example: self.pipeline.some_setting = self.config.get('some_setting')
    
    def process_data(self):
        print("Starting data processing...")
        self.configure_pipeline()
        try:
            self.pipeline.run_pipeline()
            print("Data processing completed successfully.")
        except Exception as e:
            print(f"Processing failed: {e}")

if __name__ == "__main__":
    config = {"some_setting": "value"}  # Example configuration
    facade = DataProcessingFacade(config)
    facade.process_data()
