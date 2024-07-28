# Design Pattern

![Project Logo](images/designPattern.png)
Design Patter is used in OOP programming, this page listed all the patterns, logic and example code, here's the index of it.

# Pattern Category 🚀
| Category       | Description                                                                                                                                                  |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Creational     | to create objects in a manner suitable for the situation. solve design problem by controlling the object creation process                                    |
| Structural     | deal with object composition, creating relationships between objects to form larger structures, ensure no impact to other part if one part of system changed |
| Behavioral     | managing complex control flows in a system with algorithms and the assignment of responsibilities between objects                                            |

## List of Patterns
-  Creational Patterns：- [Singleton](#singleton) - [Factory](#factory) - [Abstract](#abstract) - [Builder](#builder) - [Prototype](#prototype) 
-  Structural Patterns：- [Adapter](#AdapterPattern) - [Bridge](#BridgePattern) - [Composite](#composite) - [Flyweight](#flyweight) - [Decorator](#decorator) - [Proxy](#proxy) - [Facade](#facade)
-  Behavioral Patterns：- [Visitor](#VisitorPattern) - [Template](#TemplatePattern) - [Strategy](#StrategyPattern) - [State](#StatePattern) - [observer](#ObserverPattern) - [Memento](#MementoPattern) - [Mediator](#MediatorPattern) - [Command](#command) - [Chain of Responsibility](#chainofresponsibility) - [Interpreter](#interpreter) - [Iterator](#IteratorPattern)
## -----------------------------------<->**Behavioral** <-> **Behavioral** -----------------------------------
## VisitorPattern  
The visitor pattern fits for the situation of : **Hierarchy of elements X multi features**
[Visitor-Employee Hierarchy Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/Visitor.py)
- **Element Interface**: (Employee): Declares the accept method.
- **Concrete Element**: (Engineer, Manager): Implement the accept method to accept a visitor and call the appropriate visit method.
- **Visitor Interface**: (EmployeeVisitor): Defines methods for visiting engineers and managers.
- **Concrete Visitor**: (CompensationVisitor, DetailsVisitor): Implement the specific operations for calculating total compensation and collecting details.

## TemplatePattern 
define the skeleton of an algorithm in a base class but allows subclasses to provide specific implementations for some of the steps. 
The Template pattern fits for the situation of : **creating a fixed sequence of steps in an algorithm while allowing some flexibility in how individual steps are executed.**
[Template Game Chess Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/TemplateGameChess.py)
- **Template Method**: (Employee): **Abstract Class** typically consists of a sequence of method calls, including both concrete and abstract methods. <ABC, abstractmethod, > for **Primitive Operaations**
  ```class Game(ABC):
    def run(self):
        self.start()
        while not self.have_winner:
            self.take_turn()
        print(f'Player {self.winning_player} wins!')

    @abstractmethod
    def start(self): pass

    @property
    @abstractmethod
    def have_winner(self): pass

    @abstractmethod
    def take_turn(self): pass

    @property
    @abstractmethod
    def winning_player(self): pass```
- **Concrete Class**: (Chess):  It customizes the behavior of the algorithm by providing specific details for some of the steps in the subclass.
  ```
  class Chess(Game):
    def __init__(self):
        super().__init__()
        self.max_turns = 10
        self.turn = 1

    def start(self):
        print('Starting a game of chess.')

    @property
    def have_winner(self):
        return self.turn > self.max_turns

    def take_turn(self):
  
## StrategyPattern  
The Strategy Pattern is used to define a family of algorithms, encapsulate each one, and make them interchangeable. It allows the client to select an algorithm at runtime.
The Strategy pattern fits for the situation of : **a list of option methods can be provided, and up to client to choose at runtime**
[Strategy Pattern - Payment Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/StrategyPayment.py)
- **Strategy Interface**: (PaymentStrategy): base class with ABC, abstractmethod.
- **Concrete Strategies**: (CreditCardPayment, PayPalPayment): Each concrete strategy provides a element and derived method(same name) on top of base class
- **Context**: (ShopperingCart--> set_payment_strategy): Defines methods for visiting engineers and managers.

## StatePattern  
The State Pattern allows an object to change its behavior when its internal state changes. Instead of managing state transitions within a single class, the State Pattern delegates this responsibility to state-specific classes.
Fits situation of : **It is useful for objects that need to exhibit different behaviors based on their current state.**
[State TCP Connection Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/StateTCP.py), [State Manual Phone Script using Enum](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/StatePhoneManual.py)
- **State Enum**: (tcp state): base class with ABC, abstractmethod.
- **State Interface**: (tcp ABC, abstratctmethod--> open, close, send): base class with ABC, abstractmethod. only method of open, close and send
- **Concrete State**: (ClosedState, ListeningState, EstablishedState): Implement the behavior associated with a particular state. using the Enum to manage transitions.
- **Context**: (TCPConnection--> set_state): Manages the current state using a dictionary of states.
```In Python, the notation context: 'TCPConnection' is a type hint that specifies the type of the context parameter as TCPConnection. The quotes around 'TCPConnection' are used to indicate a forward reference, which is necessary when the TCPConnection class is referenced before it is fully defined.```

## ObserverPattern  
Subscription mechanism that allows multiple objects (observers) to listen to and react to events or changes in the state of the subject.
Fits situation of : **used in scenarios where changes in one object need to be propagated to one or more dependent objects, such as in GUI frameworks, event handling systems, and real-time data updates.**
[Property Observer - Age for Vote Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/property_dependencies_age.py), [Property Observer - Age for drive Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/property_observers.py), [Property Price Observer - Stock ChatGpt Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/PropertyObserver_Price_ChatGpt.py) 
- **Subject Interface**: (tcp state): base class with ABC, abstractmethod.
- **Concrete Subject**: (tcp ABC, abstratctmethod--> open, close, send): base class with ABC, abstractmethod. only method of open, close and send
- **Observer Interface**: (ClosedState, ListeningState, EstablishedState): Implement the behavior associated with a particular state. using the Enum to manage transitions.
- **Concrete Observer**: (TCPConnection--> set_state): Manages the current state using a dictionary of states.
- **Advantages**
Decoupling: The observer pattern promotes loose coupling between the subject and the observers.
Flexibility: Observers can be added or removed at runtime.
Reusability: The same observer can be used with different subjects.
- **Disadvantages**
Memory Leaks: If observers are not properly removed, they can cause memory leaks.
Complexity: The pattern can add complexity to the system due to the need for managing multiple observers and their notifications.
- **Event based observer**
'''class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)

```# Observer interface
class Observer:
    def update(self, event_data):
        pass

```# Concrete Observer
class ConcreteObserver(Observer):
    def __init__(self, name):
        self._name = name

    def update(self, event_data):
        print(f'{self._name} received event: {event_data}')

```# Subject with custom event
class Subject:
    def __init__(self):
        self._event = Event()

    def attach(self, observer):
        self._event.append(observer.update)

    def detach(self, observer):
        self._event.remove(observer.update)

    def generate_event(self, event_data):
        print(f'Generating event: {event_data}')
        self._event(event_data)

```# Usage
subject = Subject()

observer1 = ConcreteObserver("Observer1")
observer2 = ConcreteObserver("Observer2")

subject.attach(observer1)
subject.attach(observer2)

subject.generate_event("Event 1")
subject.generate_event("Event 2")

- **Classic Observer**
```# Observer interface
class Observer:
    def update(self, event_data):
        pass

# Concrete Observer
class ConcreteObserver(Observer):
    def __init__(self, name):
        self._name = name

    def update(self, event_data):
        print(f'{self._name} received event: {event_data}')

# Subject
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, event_data):
        for observer in self._observers:
            observer.update(event_data)

    def generate_event(self, event_data):
        print(f'Generating event: {event_data}')
        self.notify(event_data)

# Usage
subject = Subject()

observer1 = ConcreteObserver("Observer1")
observer2 = ConcreteObserver("Observer2")

subject.attach(observer1)
subject.attach(observer2)

subject.generate_event("Event 1")
subject.generate_event("Event 2")
```
## MementoPattern  
The Memento pattern fits for the situation of : **scenarios where maintaining and restoring object states is crucial, such as in undo/redo functionality in applications.**
[Memento-Bank Balance Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/MementoBalance.py) | [Memento-Bank Balances redo/undo Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/MementoBalanceUndoRedo.py) | [Memento-TextEditor ChatGpt Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/MementoTextEditor_ChatGpt.py)
- **Memento**: (Memento): The Memento Pattern ensures that the state of an object is saved and restored without violating its encapsulation. The internal state is only accessible through the Memento, and only the Originator can create and use Mementos.
- **Originator**: (TextEditor): The object whose state needs to be saved and restored.
- **Caretaker**: (Caretaker): Defines undo and redo.
- **Drawback**: Memory Overhead: Storing multiple Mementos can consume a significant amount of memory, especially if the state objects are large or if there are many states to save. Complexity: Implementing the Memento Pattern can add complexity to the code, particularly in managing the Caretaker and ensuring that Mementos are properly created and used.

## MediatorPattern  
The Mediator pattern fits for the situation of : **scenarios where multiple objects need to communicate in a complex manner, and to maintain a clean and decoupled architecture.**
[Mediator-Chatroom Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/MediatorChatRoom.py) | [Mediator-with Event Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/MediatorWithEvent.py) | [Mediator-Chatroom ChatGpt Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/MediatorChatroom_ChatGpt.py)
- **Mediator**: (ABC used by chatroom): Defines an interface for communication between Colleague objects..
- **ConcreteMediator**: (chatroom): the Mediator interface and coordinates communication between Colleague objects.
- **Users**: (colleague):Represents a user in the chat room. It communicates with other users through the ChatRoom mediator.
- **Drawback**: **Mediator Complexity**: The mediator can become a complex, monolithic class as it handles more interactions and behavior. **Single Point of Failure**: The mediator is a central component; if it fails, the whole system’s communication may be disrupted.

## command  
The Command pattern fits for the situation of : **encapsulates requests as objects, allowing for parameterization, queuing, logging, and support for undoable operations, thereby decoupling the sender from the receiver of the request.**
[Basic Command Example](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/BankAccountCommand_basic.py) | [Composite Command Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/CompositeCommand.py) | [Command TextEditor ChatGpt Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/Command_TextEdit_Chatgpt.py)
- **Command Interface**: (ABC,abstractmethod for execute/undo methods)
- **ConcreteCommand**: (TypeTextCommand, DeleteTextCommand): concrete implementations of the Command interface. They each perform specific actions on a TextEditor object and can undo those actions.
- **Invoker**: (TextEditorInvoker):invoker class that stores commands and handles execution, undo, and redo operations.
- **Context or Client**:  The client code creates instances of the TextEditor and command classes, assigns them to the invoker, and triggers their execution, undo, and redo operations.

## chainofresponsibility
The Chain of Responsibility pattern fits for the situation of : **allows multiple objects to handle a request in a sequential chain, decoupling the sender from the receiver and enabling each handler to process the request or pass it to the next handler.**
[Chain Basic Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/ChainMethod.py) | [ChainOR Broker Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/Chain_Broker.py) | [ChainOR_Support ChatGpt Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/ChainOfResponsibility_ChatGpt.py)
- **EventCaller**: __call__ for item in self: item(*args, **kwargs)
- **Handler Interface**: (CreatureModifier): Base class for all handlers, This class registers itself with the Game's queries event, defines a abstract method 'handle', __exit__ to remove the queries 
- **ConcreteHandler**: (DoubleAttackModifier; IncreaseDefenseModifier): modify the query based on specific conditions.
- **Request**: (Query) represents a request that contains the information needed to perform the action (e.g., creature_name, what_to_query, default_value).
- **Chain**: (list of handlers): Handlers are added to the Game's queries event, forming a chain.  Each handler can either handle the query or pass it to the next handler in the chain. When perform_query is called, it triggers all handlers in the chain.
- **Usage**:
  ```if __name__ == '__main__':
    game = Game()
    goblin = Creature(game, 'Strong Goblin', 2, 2)
    print(goblin)  # Initial state

    with DoubleAttackModifier(game, goblin):
        print(goblin)  # Attack doubled

        with IncreaseDefenseModifier(game, goblin):
            print(goblin)  # Attack doubled and defense increased
    print(goblin)  # Back to initial state
## interpreter
The Mediator pattern fits for the situation of : **Configurable systems where behavior is defined by expressions or rules|Expression evaluation|Language parsing**.
[Interpreter Discount Strategy Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/InterpreterDiscountStrategy.py) 
- **Rules or Operations**: (Business rules, Grammar or Math Operators): (PercentageDiscount, FlatDiscount, Conditionaldiscount) | (Literal, Variable, Rule according to Grammar) | (+, -, *, Number) 
- **Abstract Expressions**: (DiscountExpression): Abstract base class DiscountExpression for applying discounts.
- **Concrete EXpressions**: (PercentageDiscount, FlatDiscount): Concrete classes for specific discount types 
- **How it works**: (main):Represents a user in the chat room. It communicates with other users through the ChatRoom mediator.
 ```Define Rules: Create concrete discount expressions (e.g., PercentageDiscount, FlatDiscount, ConditionalDiscount).
**Apply Rules**: Sequentially apply these discount expressions to the total price. Each discount modifies the price according to its specific rule.
Evaluate Final Price: After applying all discount expressions, compute and return the final price.
Example:
**Construct Discounts**: Define discount rules such as a 10% discount, a $5 discount, and a conditional 20% discount if the total price exceeds $50.
Apply Discounts: For a total price of $60, apply the discounts to get the final price.
**Benefits**:
Flexibility: Easily add or modify discount rules without changing the core logic.
Extensibility: Supports the addition of new types of discounts by implementing new expression classes.
```
## IteratorPattern  
The Iterator pattern fits for the situation of : **scenarios where you need to process a collection of items in a specific way without exposing the internal structure of the collection.**
[Iterator Business Order Processing Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/IteratorBusinessOrder.py)
- **Object Class**: (Order): Represents a customer order with attributes like order_id, customer_name, and total_amount.
- **Iterator Class**: (OrderIterator): Implements the iterator pattern to allow sequential access to orders in the collection. It handles the iteration logic and maintains the current index.providing the __next__() method to fetch the next order.
- **Obj Collection**: (OrderCollection ): Manages a collection of orders and provides an iterator to traverse through them. exposes an iterator through __iter__().
When iterating over order_collection, the for loop uses the iterator to access each Order object. This separation allows the OrderCollection class to focus on managing the orders, while the OrderIterator class handles the iteration logic.

## -------------------------------<-> **Structural** <-> **Structural** <-> -------------------------------
## AdapterPattern    
The Adapter pattern fits for the situation of : **a powerful way to integrate different systems and components, ensuring compatibility and enhancing the flexibility of your application.**
[Adapter DB Save Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/AdapterDBSave.py)
- **TargetInterface**: (DataStorage): The interface that the client expects and interacts with. DataStorage with a method save(data)
- **Adaptee**: (SQLDatabase, NoSQLDatabase, and CloudStorage): The existing class with an incompatible interface. Different storage systems like SQLDatabase, NoSQLDatabase, and CloudStorage with different methods for storing data.
- **Adapter**: (SQLDatabaseAdapter, NoSQLDatabaseAdapter, and CloudStorageAdapter): A class that implements the target interface and translates the client's requests into calls to the adaptee's methods. implement DataStorage and translate save calls to the respective methods of the storage systems.
```# Define the Target Interface
class TargetInterface:
    def method(self, param):
        pass

```# Define the Adaptee
class Adaptee:
    def incompatible_method(self, param):
        # Implementation
        pass

```# Define the Adapter
class Adapter(TargetInterface):
    def __init__(self, adaptee):
        self.adaptee = adaptee
    
    def method(self, param):
        self.adaptee.incompatible_method(param)

```# Using the Adapter
adaptee = Adaptee()
adapter = Adapter(adaptee)
adapter.method("example_param") 
```
## BridgePattern  
The Bridge pattern fits for the situation of : **you can create a more flexible, scalable, and maintainable system architecture, especially in complex applications with multiple variations of abstractions and implementations.**
[Bridge Notification Sender Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/BridgeNotificationSender.py)
- **Abstraction**: (Notification): Defines the high-level interface and maintains a reference to an Implementor object.
- **Refined Abstratction**: (AlertNotification, ReminderNotification): extend the abstraction for specific notification types
- **Implementor interface**: (MessageSender): This is the low-level interface for sending notifications through various channels.
- **Concrete Implementor**: (EmailSender, SMSSender) These implement the notification sending methods for specific channels
- **Bridge the Abstraction and Implementor**: The abstraction (Notification) maintains a reference to the implementor (MessageSender), allowing different combinations of notification types and message channels.
``` alert_notification_with_email = AlertNotification(email_sender); reminder_notification_with_sms = ReminderNotification(sms_sender)

