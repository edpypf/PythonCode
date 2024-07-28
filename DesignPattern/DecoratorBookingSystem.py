from functools import wraps

# Step 1: Define the Base Function
def book_room(room_type, customer_id):
    print(f"Booking {room_type} for customer {customer_id}.")

# Step 2: Create Decorators

# Logging Decorator
def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Logging: {func.__name__} called with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"Logging: {func.__name__} completed")
        return result
    return wrapper

# Authentication Decorator
def auth_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        customer_id = kwargs.get('customer_id', args[1] if len(args) > 1 else None)
        if customer_id == "valid_customer":
            print("Authentication successful.")
            return func(*args, **kwargs)
        else:
            print("Authentication failed.")
            return None
    return wrapper

# Validation Decorator
def validate_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        room_type = kwargs.get('room_type', args[0] if len(args) > 0 else None)
        if room_type in ["single", "double", "suite"]:
            print("Validation successful.")
            return func(*args, **kwargs)
        else:
            print("Validation failed. Invalid room type.")
            return None
    return wrapper

# Applying decorators to the base function
@log_decorator
@auth_decorator
@validate_decorator
def book_room(room_type, customer_id):
    print(f"Booking {room_type} for customer {customer_id}.")

# Testing the decorated function
print("Test 1:")
book_room("single", "valid_customer")

print("\nTest 2:")
book_room("luxury", "valid_customer")

print("\nTest 3:")
book_room("double", "invalid_customer")
