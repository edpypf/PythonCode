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
