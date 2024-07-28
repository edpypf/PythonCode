from abc import ABC, abstractmethod

# Step 1: Define the Component Interface
class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass
    
    @abstractmethod
    def description(self):
        pass

# Step 2: Create Concrete Component
class BasicCoffee(Coffee):
    def cost(self):
        return 5  # Basic coffee cost is $5
    
    def description(self):
        return "Basic Coffee"

# Step 3: Create Decorator Class
class CoffeeDecorator(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee
    
    @abstractmethod
    def cost(self):
        pass
    
    @abstractmethod
    def description(self):
        pass

# Step 4: Create Concrete Decorators
class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 1  # Adding milk costs $1
    
    def description(self):
        return self._coffee.description() + ", Milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 0.5  # Adding sugar costs $0.5
    
    def description(self):
        return self._coffee.description() + ", Sugar"

class WhippedCreamDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 1.5  # Adding whipped cream costs $1.5
    
    def description(self):
        return self._coffee.description() + ", Whipped Cream"

# Creating a basic coffee order
basic_coffee = BasicCoffee()
print(f"{basic_coffee.description()} costs ${basic_coffee.cost()}")

# Adding milk to the coffee
milk_coffee = MilkDecorator(basic_coffee)
print(f"{milk_coffee.description()} costs ${milk_coffee.cost()}")

# Adding milk and sugar to the coffee
milk_sugar_coffee = SugarDecorator(milk_coffee)
print(f"{milk_sugar_coffee.description()} costs ${milk_sugar_coffee.cost()}")

# Adding milk, sugar, and whipped cream to the coffee
milk_sugar_whipped_coffee = WhippedCreamDecorator(milk_sugar_coffee)
print(f"{milk_sugar_whipped_coffee.description()} costs ${milk_sugar_whipped_coffee.cost()}")

##-------------------------------------------- using @ decorator ---------------------------------------##
from functools import wraps

# Step 1: Define the Base Class and Method
class Coffee:
    def cost(self):
        return 5  # Basic coffee cost is $5
    
    def description(self):
        return "Basic Coffee"

# Step 2: Create Decorators

# Logging Decorator
def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Logging: {func.__name__} called with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"Logging: {func.__name__} completed with result: {result}")
        return result
    return wrapper

# Milk Decorator
def milk_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs) + 1  # Adding milk costs $1
        self._description += ", Milk"
        return result
    return wrapper

# Sugar Decorator
def sugar_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs) + 0.5  # Adding sugar costs $0.5
        self._description += ", Sugar"
        return result
    return wrapper

# Whipped Cream Decorator
def whipped_cream_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs) + 1.5  # Adding whipped cream costs $1.5
        self._description += ", Whipped Cream"
        return result
    return wrapper

# Step 3: Applying Decorators to the Base Class Methods

class CustomCoffee(Coffee):
    def __init__(self):
        self._description = super().description()

    @log_decorator
    @milk_decorator
    @sugar_decorator
    @whipped_cream_decorator
    def cost(self):
        return super().cost()

    def description(self):
        return self._description

# Step 4: Create a Custom Coffee Order

# Creating a custom coffee order with milk, sugar, and whipped cream
custom_coffee = CustomCoffee()
print(f"{custom_coffee.description()} costs ${custom_coffee.cost()}")

# Adding more customization
class MoreCustomCoffee(CustomCoffee):
    @milk_decorator
    def cost(self):
        return super().cost()

# Creating a more custom coffee order with extra milk
more_custom_coffee = MoreCustomCoffee()
print(f"{more_custom_coffee.description()} costs ${more_custom_coffee.cost()}")

