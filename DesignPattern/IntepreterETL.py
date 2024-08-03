from abc import ABC, abstractmethod
from typing import Dict, Any

# Expression Interface
class Expression(ABC):
    
    @abstractmethod
    def interpret(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass

# Terminal Expression: Apply a simple rule (e.g., converting a value)
class ConvertToUpperCase(Expression):
    
    def __init__(self, field_name: str):
        self.field_name = field_name
    
    def interpret(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if self.field_name in context:
            context[self.field_name] = context[self.field_name].upper()
        return context

# Terminal Expression: Apply a simple rule (e.g., adding a new field)
class AddPrefix(Expression):
    
    def __init__(self, field_name: str, prefix: str):
        self.field_name = field_name
        self.prefix = prefix
    
    def interpret(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if self.field_name in context:
            context[self.field_name] = self.prefix + context[self.field_name]
        return context

# Non-Terminal Expression: Combine multiple rules
class CompositeRule(Expression):
    
    def __init__(self, *rules: Expression):
        self.rules = rules
    
    def interpret(self, context: Dict[str, Any]) -> Dict[str, Any]:
        for rule in self.rules:
            context = rule.interpret(context)
        return context

# Context and Client
if __name__ == "__main__":
    # Define transformation rules
    rule1 = ConvertToUpperCase("name")
    rule2 = AddPrefix("email", "user_")
    composite_rule = CompositeRule(rule1, rule2)
    
    # Example data
    data = {
        'name': 'alice',
        'email': 'alice@example.com'
    }
    
    # Apply transformations
    transformed_data = composite_rule.interpret(data)
    
    print("Transformed data:", transformed_data)
