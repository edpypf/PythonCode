from abc import ABC, abstractmethod

# Step 1: Define the Subject Interface
class Payment(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

# Step 2: Create the RealSubject
class RealPayment(Payment):
    def process_payment(self, amount):
        print(f"Processing payment of ${amount}")

# Step 3: Implement the Proxy
class PaymentProxy(Payment):
    def __init__(self, real_payment):
        self.real_payment = real_payment
        self.logged_in = False

    def authenticate(self, password):
        # Simulate authentication
        if password == "securepassword":
            self.logged_in = True
            print("Authentication successful")
        else:
            self.logged_in = False
            print("Authentication failed")

    def process_payment(self, amount):
        if self.logged_in:
            print(f"Logging: Payment of ${amount} requested")
            self.real_payment.process_payment(amount)
        else:
            print("Access denied. Please log in first.")

# Client code
if __name__ == '__main__':
    real_payment = RealPayment()
    proxy = PaymentProxy(real_payment)

    # Attempt to process payment without authentication
    proxy.process_payment(100)

    # Authenticate and process payment
    proxy.authenticate("securepassword")
    proxy.process_payment(100)
