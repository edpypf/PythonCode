from abc import ABC, abstractmethod

class CaffeineBeverage(ABC):
    
    def prepare_recipe(self):
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        self.add_condiments()
    
    @abstractmethod
    def brew(self):
        pass
    
    @abstractmethod
    def add_condiments(self):
        pass
    
    def boil_water(self):
        print("Boiling water")
    
    def pour_in_cup(self):
        print("Pouring into cup")
    
    def customer_wants_condiments(self):
        return True  # Hook method, can be overridden by subclasses if needed


class Tea(CaffeineBeverage):
    
    def brew(self):
        print("Steeping the tea")
    
    def add_condiments(self):
        print("Adding lemon")
    
    def customer_wants_condiments(self):
        return True  # Customize behavior if needed


class Coffee(CaffeineBeverage):
    
    def brew(self):
        print("Dripping coffee through filter")
    
    def add_condiments(self):
        print("Adding sugar and milk")


# Usage
if __name__ == "__main__":
    tea = Tea()
    coffee = Coffee()
    
    print("Making tea:")
    tea.prepare_recipe()
    
    print("\nMaking coffee:")
    coffee.prepare_recipe()
