from abc import ABC, abstractmethod

class SupportHandler(ABC):
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    @abstractmethod
    def handle_request(self, request):
        pass

class LowLevelSupport(SupportHandler):
    def handle_request(self, request):
        if request == "low":
            print("LowLevelSupport: Handling low level request.")
        elif self.next_handler:
            self.next_handler.handle_request(request)

class MidLevelSupport(SupportHandler):
    def handle_request(self, request):
        if request == "mid":
            print("MidLevelSupport: Handling mid level request.")
        elif self.next_handler:
            self.next_handler.handle_request(request)

class HighLevelSupport(SupportHandler):
    def handle_request(self, request):
        if request == "high":
            print("HighLevelSupport: Handling high level request.")
        elif self.next_handler:
            self.next_handler.handle_request(request)

if __name__ == "__main__":
    low_support = LowLevelSupport()
    mid_support = MidLevelSupport()
    high_support = HighLevelSupport()

    low_support.set_next(mid_support).set_next(high_support)

    # Send various requests
    low_support.handle_request("low")
    low_support.handle_request("mid")
    low_support.handle_request("high")
    low_support.handle_request("unknown")  # Will not be handled
