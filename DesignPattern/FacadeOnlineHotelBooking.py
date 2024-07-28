# Step 1: Define Subsystem Classes

class RoomBooking:
    def book_room(self, room_type, customer_id):
        print(f"Room booked: {room_type} for customer {customer_id}")
        return True

class Payment:
    def process_payment(self, amount, customer_id):
        print(f"Payment of ${amount} processed for customer {customer_id}")
        return True

class Notification:
    def send_confirmation(self, customer_id):
        print(f"Confirmation email sent to customer {customer_id}")
        return True

# Step 2: Create the Facade

class HotelBookingFacade:
    def __init__(self):
        self.room_booking = RoomBooking()
        self.payment = Payment()
        self.notification = Notification()

    def book_room(self, room_type, customer_id):
        if self.room_booking.book_room(room_type, customer_id):
            if self.payment.process_payment(100, customer_id):  # Assume a fixed amount for simplicity
                self.notification.send_confirmation(customer_id)
                print("Room booking completed successfully")
                return True
        print("Room booking failed")
        return False

# Step 3: Use the Facade

# Client code
facade = HotelBookingFacade()
facade.book_room("single", "customer123")
