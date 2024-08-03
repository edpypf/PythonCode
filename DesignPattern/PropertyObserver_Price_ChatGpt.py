from typing import List

# Observer Interface
class Investor:
    def update(self, stock_name: str, new_price: float):
        pass

# Concrete Observer 1
class IndividualInvestor(Investor):
    def __init__(self, name: str):
        self._name = name
    
    def update(self, stock_name: str, new_price: float):
        print(f"{self._name} received notification: {stock_name} price changed to {new_price}")

# Concrete Observer 2
class InstitutionalInvestor(Investor):
    def __init__(self, name: str):
        self._name = name
    
    def update(self, stock_name: str, new_price: float):
        print(f"{self._name} (Institutional) received notification: {stock_name} price changed to {new_price}")

# Subject Interface
class Stock:
    def __init__(self, name: str):
        self._name = name
        self._price = 0.0
        self._investors: List[Investor] = []
    
    def attach(self, investor: Investor):
        if investor not in self._investors:
            self._investors.append(investor)
    
    def detach(self, investor: Investor):
        if investor in self._investors:
            self._investors.remove(investor)
    
    def notify(self):
        for investor in self._investors:
            investor.update(self._name, self._price)
    
    def set_price(self, new_price: float):
        self._price = new_price
        self.notify()

# Concrete Subject
class ConcreteStock(Stock):
    def __init__(self, name: str):
        super().__init__(name)

# Usage
if __name__ == "__main__":
    # Create stocks
    apple_stock = ConcreteStock("Apple")
    google_stock = ConcreteStock("Google")
    
    # Create investors
    john = IndividualInvestor("John Doe")
    acme_investments = InstitutionalInvestor("Acme Investments")
    
    # Attach investors to stocks
    apple_stock.attach(john)
    apple_stock.attach(acme_investments)
    
    google_stock.attach(acme_investments)
    
    # Update stock prices
    apple_stock.set_price(150.75)
    google_stock.set_price(2800.10)
    
    # Detach an investor and update stock price again
    apple_stock.detach(john)
    apple_stock.set_price(155.00)
