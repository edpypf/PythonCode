from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def pay(self, amount: float) -> None:
        print(f'Processing credit card payment of ${amount} with card {self.card_number}.')

class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> None:
        print(f'Processing PayPal payment of ${amount} to email {self.email}.')

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.payment_strategy: PaymentStrategy = None

    def add_item(self, item: str, price: float) -> None:
        self.items.append((item, price))

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        self.payment_strategy = strategy

    def checkout(self) -> None:
        total_amount = sum(price for _, price in self.items)
        print(f'Total amount to be paid: ${total_amount}')
        if self.payment_strategy:
            self.payment_strategy.pay(total_amount)
        else:
            print('No payment method set.')

if __name__ == '__main__':
    cart = ShoppingCart()
    cart.add_item('Laptop', 1200)
    cart.add_item('Mouse', 25)

    # Choose payment method: Credit Card
    credit_card_payment = CreditCardPayment('1234-5678-9876-5432')
    cart.set_payment_strategy(credit_card_payment)
    cart.checkout()

    # Choose payment method: PayPal
    paypal_payment = PayPalPayment('user@example.com')
    cart.set_payment_strategy(paypal_payment)
    cart.checkout()
