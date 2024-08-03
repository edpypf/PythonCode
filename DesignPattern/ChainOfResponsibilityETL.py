from abc import ABC, abstractmethod
from typing import List, Dict, Any

# Handler Interface
class ETLHandler(ABC):
    
    def __init__(self, successor: 'ETLHandler' = None):
        self._successor = successor
    
    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def set_successor(self, successor: 'ETLHandler'):
        self._successor = successor
    
    def _process_successor(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if self._successor:
            return self._successor.process(data)
        return data

# Concrete Handler 1: Filtering Data
class FilterHandler(ETLHandler):
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        print("Filtering data")
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return self._process_successor(filtered_data)

# Concrete Handler 2: Normalizing Data
class NormalizeHandler(ETLHandler):
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        print("Normalizing data")
        normalized_data = {key: str(value).strip().lower() for key, value in data.items()}
        return self._process_successor(normalized_data)

# Concrete Handler 3: Enriching Data
class EnrichHandler(ETLHandler):
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        print("Enriching data")
        enriched_data = data.copy()
        enriched_data['enriched'] = True  # Example enrichment
        return self._process_successor(enriched_data)

# Client
if __name__ == "__main__":
    # Set up the chain of responsibility
    filter_handler = FilterHandler()
    normalize_handler = NormalizeHandler()
    enrich_handler = EnrichHandler()
    
    filter_handler.set_successor(normalize_handler)
    normalize_handler.set_successor(enrich_handler)
    
    # Example data
    raw_data = {
        'name': '  Alice  ',
        'age': None,
        'email': 'ALICE@EXAMPLE.COM'
    }
    
    # Process data through the chain
    final_data = filter_handler.process(raw_data)
    
    print("Final processed data:", final_data)
