class Order:
    def __init__(self, order_id, customer_name, total_amount):
        self.order_id = order_id
        self.customer_name = customer_name
        self.total_amount = total_amount

    def __repr__(self):
        return f'Order(order_id={self.order_id}, customer_name="{self.customer_name}", total_amount={self.total_amount})'

class OrderIterator:
    def __init__(self, orders):
        self._orders = orders
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._orders):
            order = self._orders[self._index]
            self._index += 1
            return order
        else:
            raise StopIteration

class OrderCollection:
    def __init__(self):
        self._orders = []

    def add_order(self, order):
        self._orders.append(order)

    def __iter__(self):
        return OrderIterator(self._orders)

# Usage
order_collection = OrderCollection()
order_collection.add_order(Order(1, "Alice", 250.0))
order_collection.add_order(Order(2, "Bob", 150.0))
order_collection.add_order(Order(3, "Charlie", 300.0))

# Processing orders
for order in order_collection:
    # Here you can process each order, e.g., generate invoices or update inventory
    print(f"Processing order: {order}")
    # Example processing logic
    # generate_invoice(order)
    # update_inventory(order)
