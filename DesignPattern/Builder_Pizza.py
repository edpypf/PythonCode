class Pizza:
    def __init__(self):
        self.size = None
        self.cheese = None
        self.pepperoni = None
        self.veggies = None
    
    def __str__(self):
        ingredients = []
        if self.cheese:
            ingredients.append("cheese")
        if self.pepperoni:
            ingredients.append("pepperoni")
        if self.veggies:
            ingredients.append("veggies")
        return f"Pizza (size: {self.size}, ingredients: {', '.join(ingredients)})"

class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()

    def set_size(self, size):
        self.pizza.size = size
        return self
    
    def add_cheese(self):
        self.pizza.cheese = True
        return self
    
    def add_pepperoni(self):
        self.pizza.pepperoni = True
        return self
    
    def add_veggies(self):
        self.pizza.veggies = True
        return self
    
    def build(self):
        return self.pizza

class Director:
    def __init__(self, builder):
        self._builder = builder
    
    def construct_veggie_pizza(self):
        return self._builder.set_size('medium').add_cheese().add_veggies().build()
    
    def construct_meat_lovers_pizza(self):
        return self._builder.set_size('large').add_cheese().add_pepperoni().build()

if __name__ == "__main__":
    builder = PizzaBuilder()
    director = Director(builder)
    
    veggie_pizza = director.construct_veggie_pizza()
    print(veggie_pizza)
    
    meat_lovers_pizza = director.construct_meat_lovers_pizza()
    print(meat_lovers_pizza)
