class FlightBooking:
    def book_flight(self, flight_details):
        print(f"Flight booked: {flight_details}")
        return True

class HotelBooking:
    def book_hotel(self, hotel_details):
        print(f"Hotel booked: {hotel_details}")
        return True

class CarRental:
    def rent_car(self, car_details):
        print(f"Car rented: {car_details}")
        return True

class TravelBookingFacade:
    def __init__(self):
        self.flight_booking = FlightBooking()
        self.hotel_booking = HotelBooking()
        self.car_rental = CarRental()

    def book_trip(self, flight_details, hotel_details, car_details):
        if self.flight_booking.book_flight(flight_details):
            if self.hotel_booking.book_hotel(hotel_details):
                if self.car_rental.rent_car(car_details):
                    print("Travel booking completed successfully")
                    return True
        print("Travel booking failed")
        return False

# Client code
facade = TravelBookingFacade()
facade.book_trip("NY to LA", "Hilton", "Sedan")
