from abc import ABC, abstractmethod

class ChatMediator(ABC):
    @abstractmethod
    def send_message(self, message, user):
        pass

    @abstractmethod
    def add_user(self, user):
        pass

class ChatRoom(ChatMediator):
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def send_message(self, message, sender):
        for user in self.users:
            if user != sender:
                user.receive_message(message, sender)

class User:
    def __init__(self, name, mediator):
        self.name = name
        self.mediator = mediator
        self.mediator.add_user(self)

    def send_message(self, message):
        print(f"{self.name} sends: {message}")
        self.mediator.send_message(message, self)

    def receive_message(self, message, sender):
        print(f"{self.name} receives message from {sender.name}: {message}")

# Create the chat room mediator
chat_room = ChatRoom()

# Create users (colleagues) and register them with the chat room
alice = User("Alice", chat_room)
bob = User("Bob", chat_room)
charlie = User("Charlie", chat_room)

# Users send messages through the chat room (mediator)
alice.send_message("Hello, everyone!")
bob.send_message("Hi Alice!")
charlie.send_message("Hey Alice and Bob!")
