from abc import ABC, abstractmethod

# Abstract Expression
class DiscountExpression(ABC):
    @abstractmethod
    def apply(self, total_price):
        pass

# Terminal Expression for Percentage Discount
class PercentageDiscount(DiscountExpression):
    def __init__(self, percentage):
        self.percentage = percentage

    def apply(self, total_price):
        return total_price * (1 - self.percentage / 100)

# Terminal Expression for Flat Discount
class FlatDiscount(DiscountExpression):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, total_price):
        return total_price - self.amount

# Non-Terminal Expression for Conditional Discount
class ConditionalDiscount(DiscountExpression):
    def __init__(self, condition, discount):
        self.condition = condition
        self.discount = discount

    def apply(self, total_price):
        if self.condition(total_price):
            return self.discount.apply(total_price)
        return total_price

# Condition function for conditional discount
def price_exceeds_threshold(threshold):
    return lambda total_price: total_price > threshold

# Function to apply discounts
def apply_discounts(total_price, discounts):
    for discount in discounts:
        total_price = discount.apply(total_price)
    return total_price

# Main function
def main():
    # Create discount expressions
    discounts = [
        PercentageDiscount(10),  # 10% discount
        FlatDiscount(5),         # $5 discount
        ConditionalDiscount(price_exceeds_threshold(50), PercentageDiscount(20))  # 20% discount if total price > $50
    ]
    
    total_price = 60  # Example total price
    final_price = apply_discounts(total_price, discounts)
    print(f'Final Price after discounts: ${final_price:.2f}')  # Expected output: $44.00

if __name__ == '__main__':
    main()
