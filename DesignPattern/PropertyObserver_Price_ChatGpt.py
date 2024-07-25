from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, stock_name, price):
        pass

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, stock_name, price):
        for observer in self._observers:
            observer.update(stock_name, price)

class Stock(Subject):
    def __init__(self, name, price):
        super().__init__()
        self._name = name
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        self._price = new_price
        self.notify(self._name, new_price)

class Investor(Observer):
    def __init__(self, name):
        self._name = name

    def update(self, stock_name, price):
        print(f"Investor {self._name} notified: {stock_name} price changed to {price}")

# Create stock instances (subjects)
apple_stock = Stock("Apple", 150)
google_stock = Stock("Google", 2800)

# Create investor instances (observers)
investor1 = Investor("Alice")
investor2 = Investor("Bob")

# Attach investors to stocks
apple_stock.attach(investor1)
apple_stock.attach(investor2)
google_stock.attach(investor1)

# Change stock prices and notify observers
apple_stock.price = 155  # Output:
                         # Investor Alice notified: Apple price changed to 155
                         # Investor Bob notified: Apple price changed to 155

google_stock.price = 2900  # Output:
                           # Investor Alice notified: Google price changed to 2900

# Detach an investor and change stock price
apple_stock.detach(investor2)
apple_stock.price = 160  # Output:
                         # Investor Alice notified: Apple price changed to 160
